import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
import unittest
from unittest.mock import patch
from urllib.error import HTTPError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts/dashboard.py'
spec = importlib.util.spec_from_file_location('dashboard', SCRIPT)
d = importlib.util.module_from_spec(spec)
spec.loader.exec_module(d)


class DashboardTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.store = d.Store(self.temp.name)
        self.snapshot = json.loads((ROOT / 'assets/example.json').read_text())
        self.store.init('test-session', self.snapshot)

    def report(self, rid='one', revision=0, reason='', snapshot=None):
        return {'id': rid, 'expected_revision': revision, 'reason': reason,
                'snapshot': copy.deepcopy(snapshot or self.snapshot)}

    def test_durable_inbox_and_idempotent_retry(self):
        report = self.report()
        self.store.submit(report)
        restarted = d.Store(self.temp.name)
        self.assertEqual(restarted.state()['pending_reports'], ['one'])
        self.assertEqual(restarted.state()['revision'], 0)
        restarted.submit(report)
        self.assertEqual(restarted.apply('one'), 1)
        self.assertEqual(restarted.apply('one'), 1)
        self.assertEqual(len(restarted.state()['history']), 2)
        self.assertEqual(restarted.state()['pending_reports'], [])
        report['reason'] = 'different'
        with self.assertRaisesRegex(ValueError, 'different content'):
            restarted.submit(report)

    def test_stale_report_cannot_overwrite_and_can_be_withdrawn(self):
        self.store.submit(self.report())
        self.store.submit(self.report('two'))
        self.store.apply('one')
        with self.assertRaisesRegex(ValueError, 'Stale'):
            self.store.apply('two')
        self.store.withdraw('two', 'Reconciled with newer work')
        with self.assertRaisesRegex(ValueError, 'withdrawn'):
            self.store.apply('two')
        self.assertEqual(self.store.state()['pending_reports'], [])
        self.assertIn('Reconciled', self.store.state()['history'][-1]['reason'])

    def test_plan_changes_require_reason(self):
        for change in ('goal', 'owner', 'cancelled', 'removed'):
            with self.subTest(change=change):
                s = copy.deepcopy(self.snapshot)
                if change == 'goal':
                    s['goal'] = 'Changed purpose'
                elif change == 'owner':
                    s['phases'][0]['todos'][1]['owner'] = 'other'
                elif change == 'cancelled':
                    s['phases'][0]['todos'][1]['status'] = 'cancelled'
                else:
                    s['phases'][0]['todos'].pop()
                self.store.submit(self.report(change, snapshot=s))
                with self.assertRaisesRegex(ValueError, 'reason'):
                    self.store.apply(change)
                self.assertEqual(self.store.state()['revision'], 0)
        self.store.submit(self.report('explained', reason='Scope changed after research', snapshot=s))
        self.store.apply('explained')
        self.assertIn('Scope changed', (Path(self.temp.name) / 'report.html').read_text())

    def test_invalid_completion_and_references(self):
        s = copy.deepcopy(self.snapshot)
        s['status'] = 'completed'
        s['summary'] = 'All done'
        with self.assertRaisesRegex(ValueError, 'unfinished'):
            d.validate(s)
        s['phases'][0]['todos'][1]['status'] = 'done'
        s['phases'][0]['todos'][1]['result'] = 'Verified'
        with self.assertRaisesRegex(ValueError, 'open requests'):
            d.validate(s)
        s['requests'][0].update(status='resolved', resolution='Approved in chat')
        d.validate(s)
        s['requests'][0]['blocks'] = ['nonexistent']
        with self.assertRaisesRegex(ValueError, 'reference'):
            d.validate(s)

    def test_lifecycle_is_filtered_and_never_completes_todos(self):
        event = {'session_id': 'wrong', 'hook_event_name': 'SubagentStop', 'agent_id': 'worker'}
        self.store.hook(event)
        self.assertEqual(self.store.state()['runtime_agents'], {})
        event.update(session_id='test-session', agent_type='general-purpose', transcript_path='SECRET')
        self.store.hook(event)
        state = self.store.state()
        self.assertEqual(state['snapshot'], self.snapshot)
        self.assertEqual(state['revision'], 0)
        self.assertEqual(state['runtime_agents']['worker']['event'], 'SubagentStop')
        self.assertNotIn('SECRET', json.dumps(state))
        self.assertIn('TODOの完了を意味しません', d.page(state))

    def test_concurrent_reports_have_one_winner(self):
        self.store.submit(self.report('one'))
        self.store.submit(self.report('two'))
        def apply(rid):
            try:
                return self.store.apply(rid)
            except ValueError:
                return 'stale'
        with ThreadPoolExecutor(2) as pool:
            outcomes = list(pool.map(apply, ['one', 'two']))
        self.assertCountEqual(outcomes, [1, 'stale'])
        exported = json.loads((Path(self.temp.name) / 'state.json').read_text())
        self.assertEqual(exported, self.store.state())

    def test_export_recovers_and_escapes_untrusted_text(self):
        s = copy.deepcopy(self.snapshot)
        s['goal'] = '<script>alert("x")</script>'
        self.store.submit(self.report(reason='Display hostile text literally', snapshot=s))
        self.store.apply('one')
        exported = Path(self.temp.name) / 'report.html'
        self.assertNotIn('<script>alert', exported.read_text())
        self.assertIn('&lt;script&gt;', exported.read_text())
        exported.unlink()
        self.store.export()
        self.assertIn('保存された作業記録', exported.read_text())
        self.assertIn('location.protocol', exported.read_text())

    def test_init_never_overwrites_existing_record(self):
        with self.assertRaises(FileExistsError):
            self.store.init('different', self.snapshot)
        self.assertEqual(self.store.state()['session_id'], 'test-session')

    def test_http_read_only_and_no_directory_exposure(self):
        process = subprocess.Popen([sys.executable, str(SCRIPT), '--directory', self.temp.name, 'serve'],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        self.addCleanup(process.stderr.close)
        self.addCleanup(process.stdout.close)
        def stop():
            process.terminate()
            process.wait(timeout=5)
        self.addCleanup(stop)
        url = process.stdout.readline().strip()
        self.assertTrue(url.startswith('http://127.0.0.1:'))
        with urlopen(url, timeout=3) as response:
            self.assertIn('frame-ancestors', response.headers['Content-Security-Policy'])
            self.assertIn('作業計画', response.read().decode())
        for path, method, status in [('session.sqlite3', 'GET', 404), ('../state.json', 'GET', 404), ('', 'POST', 501)]:
            with self.assertRaises(HTTPError) as error:
                urlopen(Request(url + path, method=method), timeout=3)
            self.assertEqual(error.exception.code, status)
            error.exception.close()
        with self.assertRaises(HTTPError) as error:
            urlopen(Request(url, headers={'Host': 'attacker.example'}), timeout=3)
        self.assertEqual(error.exception.code, 403)
        error.exception.close()
        with urlopen(url + 'view.json', timeout=3) as response:
            initial = json.load(response)
            before = initial['version']
            self.assertIn('分', initial['elapsed'])
        with urlopen(url + 'view.json', timeout=3) as response:
            self.assertEqual(json.load(response)['version'], before)
        self.store.submit(self.report())
        with urlopen(url + 'view.json', timeout=3) as response:
            after = json.load(response)
        self.assertNotEqual(before, after['version'])
        self.assertIn('反映待ち', after['html'])

    def test_completed_record_survives_server_shutdown(self):
        s = copy.deepcopy(self.snapshot)
        s['status'] = 'completed'
        s['summary'] = 'Verified updates. No remaining work. Screen reader unverified.'
        s['phases'][0]['todos'][1].update(status='done', result='Observed update')
        s['requests'][0].update(status='resolved', resolution='Reviewed in chat')
        self.store.submit(self.report(snapshot=s))
        self.store.apply('one')
        restarted = d.Store(self.temp.name)
        restarted.export()
        saved = (Path(self.temp.name) / 'report.html').read_text()
        self.assertIn('Screen reader unverified', saved)
        self.assertIn('Reviewed in chat', saved)
        self.assertEqual(restarted.state()['snapshot']['status'], 'completed')

    def test_empty_sections_and_long_plain_text(self):
        s = copy.deepcopy(self.snapshot)
        s.update(phases=[], requests=[], agents=[], current_work='Long text ' * 200)
        self.store.submit(self.report(reason='Initial planning has not started', snapshot=s))
        self.store.apply('one')
        text = d.page(self.store.state())
        self.assertIn('作業計画はまだ報告されていません', text)
        self.assertIn('判断・レビューの依頼はありません', text)
        self.assertIn('担当状況の報告はまだありません', text)

    def test_metrics_unknown_zero_scope_and_escaping(self):
        self.assertIn('未取得', d.body(self.store.state()))
        s = copy.deepcopy(self.snapshot)
        s['metrics'] = {'models': ['model-a', '<model-b>'], 'total_tokens': 0,
                        'scope': 'Main agent only', 'source': 'Host response',
                        'reported_at': '2026-09-27T12:00:00Z'}
        self.store.submit(self.report(snapshot=s))
        self.store.apply('one')
        text = d.body(self.store.state())
        self.assertIn('<dd>0</dd>', text)
        self.assertIn('model-a / &lt;model-b&gt;', text)
        self.assertIn('Main agent only', text)
        self.assertIn('Host response', text)
        self.assertEqual(json.loads((Path(self.temp.name) / 'state.json').read_text())['snapshot']['metrics'], s['metrics'])

    def test_metrics_reject_invalid_counts_and_missing_provenance(self):
        for tokens in [-1, True, 1.5, '100']:
            s = copy.deepcopy(self.snapshot)
            s['metrics'] = {'models': [], 'total_tokens': tokens, 'scope': 'main',
                            'source': 'host', 'reported_at': '2026-09-27T12:00:00Z'}
            with self.assertRaisesRegex(ValueError, 'total_tokens'):
                d.validate(s)
        s['metrics']['total_tokens'] = None
        d.validate(s)
        s['metrics']['source'] = ''
        with self.assertRaisesRegex(ValueError, 'scope, source'):
            d.validate(s)

    def test_elapsed_live_frozen_and_legacy_record(self):
        state = self.store.state()
        state['history'][0]['at'] = '2026-09-27T12:00:00Z'
        self.assertIn('1時間 2分 3秒', d.usage_widgets(state, '2026-09-27T13:02:03Z'))
        state['snapshot']['status'] = 'paused'
        state.pop('finished_at', None)
        state['applied_at'] = '2026-09-27T12:01:30Z'
        self.assertIn('1分 30秒', d.usage_widgets(state, '2026-09-27T13:02:03Z'))
        state['finished_at'] = '2026-09-27T12:02:00Z'
        self.assertIn('2分 0秒', d.usage_widgets(state, '2026-09-27T13:02:03Z'))

    def test_late_metrics_do_not_extend_frozen_duration_and_resume_clears_stop(self):
        s = copy.deepcopy(self.snapshot)
        s['status'] = 'paused'
        self.store.submit(self.report(snapshot=s))
        with patch.object(d, 'now', return_value='2026-09-27T13:00:00Z'):
            self.store.apply('one')
        self.store.submit(self.report('two', revision=1, snapshot=s))
        with patch.object(d, 'now', return_value='2026-09-27T14:00:00Z'):
            self.store.apply('two')
        self.assertEqual(self.store.state()['finished_at'], '2026-09-27T13:00:00Z')
        s['status'] = 'active'
        self.store.submit(self.report('three', revision=2, snapshot=s))
        self.store.apply('three')
        self.assertIsNone(self.store.state()['finished_at'])

    def test_session_identity_roundtrip_and_unknown_legacy(self):
        legacy = d.body(self.store.state())
        self.assertIn('セッション開始</dt><dd>未取得', legacy)
        self.assertIn('ダッシュボード起動', legacy)
        s = copy.deepcopy(self.snapshot)
        s['session_context'] = {'started_at': '2026-09-27T09:00:00+09:00',
                                'cwd': '/workspace/<example>/project'}
        self.store.submit(self.report(snapshot=s))
        self.store.apply('one')
        text = d.body(self.store.state())
        self.assertIn('2026-09-27T09:00:00+09:00', text)
        self.assertIn('/workspace/&lt;example&gt;/project', text)
        self.assertEqual(self.store.state()['snapshot']['session_context'], s['session_context'])

    def test_session_identity_rejects_ambiguous_timestamp(self):
        for timestamp in ['yesterday', '2026-09-27T12:00:00', 42]:
            s = copy.deepcopy(self.snapshot)
            s['session_context'] = {'started_at': timestamp, 'cwd': None}
            with self.assertRaises(ValueError):
                d.validate(s)
        s['session_context']['started_at'] = None
        d.validate(s)

    def test_cli_failure_is_nonzero_and_preserves_record(self):
        result = subprocess.run([sys.executable, str(SCRIPT), '--directory', self.temp.name, 'hook'],
                                input='not json', capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn('dashboard:', result.stderr)
        self.assertEqual(self.store.state()['revision'], 0)


if __name__ == '__main__':
    unittest.main()
