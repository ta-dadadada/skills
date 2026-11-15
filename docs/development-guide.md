# 開発者ガイド

この文書は、このリポジトリでスキルを作成・改訂する開発者向けの手順をまとめています。
導入方法は [README](../README.md)、配布するスキルの一覧・用途・利用フローは
[プロジェクトガイド](project-guide.md)を参照してください。
エージェントが従うルールの正本は [AGENTS.md](../AGENTS.md)です。

## リポジトリの構成

| 配置先 | 用途 |
| --- | --- |
| `dev/<skill-name>/` | 開発ワークフローのスキルの正本。 |
| `meta/<skill-name>/` | スキルの作成・評価・改善や作業モードのスキルの正本。 |
| [`knowledge/`](../knowledge/README.md) | 整理済みの再利用可能な参照資料。追加時は同ディレクトリの規約に従います。 |
| `docs/` | 利用者・開発者向けのプロジェクト説明文書。 |
| `scripts/` | 配布用メタデータなどを生成するリポジトリ共通のスクリプト。 |
| `.local/` | Git管理から除外する一時作業領域。公開・レビュー対象のファイルは置きません。 |

各スキルは必須の `SKILL.md` と、必要に応じた `references/`、`scripts/` で構成します。スキル名、ディレクトリ名、frontmatterの `name` は一致させます。
スキル本文・参照資料・`knowledge/` は簡潔な英語で記述します。
このガイドなどの日本語文書は、スキル本体とは分けて管理します。

## このリポジトリで使うスキル

このリポジトリ自身の作業で使うスキルは、`.agents/skills/` と
`.claude/skills/` に相対シンボリックリンクで配置しています。
どちらも `dev/`・`meta/` の正本を参照し、両方の配置を揃えます。
配布する全スキルを、プロジェクトの作業用に配置する必要はありません。

参照先と選択ルールは [AGENTS.mdのProject Skills](../AGENTS.md#project-skills) に従います。
同名の個人用コピーとは指示を混ぜず、プロジェクトの正本を参照します。
これは参照ルールであり、ツールの選択候補から個人用コピーを自動的に消す設定ではありません。

- スキルの作成・改訂: [shiranui-hanten](../meta/shiranui-hanten/SKILL.md)。
- 明示的な指示レビュー・実行比較・反復調整: [shiranui-hansode](../meta/shiranui-hansode/SKILL.md)。
- 作業の中断・再開: [session-handover](../dev/session-handover/SKILL.md) → [session-resume](../dev/session-resume/SKILL.md)。

配置されているスキルを毎回すべて実行する必要はありません。
各スキルの発動条件と依頼範囲に従い、評価も毎回自動実行するものではありません。
目的記録の `.agent-goal.md` と引き継ぎ記録の `.agent-session.md` はGit管理から除外します。

## スキルを作成・改訂する

1. [shiranui-hanten](../meta/shiranui-hanten/SKILL.md)で要件、発動条件、構造、本文、検証を整理します。
2. `dev/` または `meta/` に正本を配置し、必要な参照資料・スクリプトを揃えます。スキルごとの `README.md` は置きません。
3. 新規追加・名称変更・用途変更は、[プロジェクトガイドのスキル一覧](project-guide.md#スキル一覧)に反映します。関連する利用フローも確認します。
4. このプロジェクトの作業に使うスキルとして追加する場合は、両ツール向けの相対リンクを揃え、リンク先を確認します。
5. 配布用メタデータを再生成し、変更したスキルと関連スクリプトを検証します。

リポジトリ直下のREADMEは閲覧者・利用者向けの概要と導入方法を中心に保ちます。
スキル一覧・説明・利用フローはプロジェクトガイド、開発手順はこの文書にまとめ、
直下のREADMEにはリンクを置きます。

## 配布用メタデータを再生成する

各スキルの `apm.yml` は、`SKILL.md` のfrontmatterにある
`name`・`description`・`license` から生成します。
これらの変更やスキルの追加・名称変更後は、リポジトリ直下で次のコマンドを実行します。
生成には `uv` が必要で、PyYAMLの依存指定はスクリプトに含まれています。

```bash
./scripts/generate_apm_yml.py
```

[生成スクリプト](../scripts/generate_apm_yml.py)はGitに登録済みの `SKILL.md` を対象にします。
新規スキルは対象ファイルを `git add` で登録してから生成してください。
各スキルの `apm.yml` と、全スキルを依存として列挙する
[リポジトリ直下のapm.yml](../apm.yml)を再生成します。`SKILL.md` 自体は変更しません。
生成後は差分を確認し、関連するメタデータも変更と一緒にコミットします。

## 検証する

以下のコマンドはリポジトリ直下で実行します。
ローカルフォームの実行とテストにはPython 3.11以上が必要です。

```bash
# 全スキルの形式・相対リンク・実行権限などを検証
python3 meta/shiranui-hanten/scripts/validate_skill.py dev/* meta/*

# local-intakeのランタイムテスト
python3 -m unittest discover -s dev/local-intake/tests -v

# session-dashboardのランタイムテスト
python3 -m unittest discover -s dev/session-dashboard/tests -v

# hq-dashboardのランタイムテスト
python3 -m unittest discover -s dev/hq-dashboard/tests -v

# 空白エラーを確認
git diff --check
```

個別のスキルを検証する例:

```bash
python3 meta/shiranui-hanten/scripts/validate_skill.py dev/pr-handoff
```

変更したスキルの `FAIL` は解消し、`WARN` は意図した挙動かを確認します。
スクリプト変更時は関連テストに加え、未カバーの成功・失敗経路を確認し、実行権限を維持します。
文書のリンクとコマンドは、実行・参照するディレクトリを基準に確認します。

[CI](../.github/workflows/ci.yml)では、Python 3.11・3.12・3.13・3.14で
全スキルのvalidatorを常に実行します。`local-intake`・`session-dashboard`・`hq-dashboard` のテストとCLIのヘルプ確認は、
次のPython関連ファイルに差分がある場合のみ実行します。

- Pythonソース: `*.py`・`*.pyi`。
- 設定・依存関係: `pyproject.toml`、`setup.cfg`、`tox.ini`、`pytest.ini`、`.python-version`、
  `requirements*.txt`・`requirements*.in`、`Pipfile`・`Pipfile.lock`、`poetry.lock`、`uv.lock`、`pdm.lock`。配置先は問いません。
- CI設定: `.github/workflows/ci.yml`。
- テストが検証する資産: `dev/hq-dashboard/assets/` 配下（ダッシュボードのHTML）。

PRはベースブランチとの分岐点から、pushは前回コミットからの差分で判定します。
削除・名称変更も対象とし、比較元がない初回pushではテストを実行します。
Markdownなどだけの変更ではランタイムテストをスキップしますが、スキル検証は残ります。
指示の静的レビューと実行比較は別の証拠として扱い、実測していない効果は保証しません。

## コミット・PR・公開前の確認

ダッシュボードのMarkdownコピーを変更した場合は、Node.js 18以降で
`node --test dev/session-dashboard/tests/test_markdown.cjs` も実行します。
このテストはDOMの代替オブジェクトで出力と失敗経路を検証するため、
実ブラウザでのコピー操作も確認します。現在のPython CIとは別の手動チェックです。

- コミット件名は `feat:`・`fix:`・`docs:`・`refactor:`・`chore:` などの規約に従い、目的ごとにまとめます。
- PRでは変更の目的、影響する配置先、実施した検証を説明し、発動条件やエージェントの挙動が変わる場合は変更前後の例を添えます。
- 正本とツール向け配置、スキル一覧、生成した `apm.yml` の整合性を確認します。
- スキル本文、同梱スクリプト、参照資料に秘密情報が含まれていないことを確認します。
- チームで同じ版を再現する必要がある場合は、利用者にコミットSHAを案内します。

PRタイトル・説明とコミット分割案の整理には [pr-handoff](../dev/pr-handoff/SKILL.md)を使えます。
このスキルは提案のみで、commit・push・PR作成そのものは実行しません。

## HQのホスト対応を検証する

HQは共通の台帳・報告形式を使い、ホスト固有の操作は各スキルの
`references/claude-desktop.md` と `references/codex-desktop.md` に分離します。
Codexの `codex_app` ツールのスキーマが優先されます。存在しない起動設定、
保留中IDの変換API、終了後の自動通知を仮定しないでください。

ローカル検証は `hq-dashboard` の単体テストとvalidatorで行います。
実ホストの確認は別の証拠です。新規チャット作成や送信を伴う検証は、
検証目的、送信先、操作を伝え、ユーザーの明示許可がある範囲だけで行います。
サブエージェント利用の許可を、チャット作成の許可として扱いません。

Codex desktopの実機スモーク確認は、読み取りだけの小さな作業を使います。

1. 許可済みの対象を `list_projects` で解決し、ブリーフに対応する新規チャットを作成する。
   `threadId` と `hostId` を保存し、`launch` のreceiptを確認する。
2. 最大8件・最長60秒の `wait_threads` で最終報告を取得する。
   原文と安定したreport id、返却cursor、保存済みcursorを `ingest` に渡す。
   実際の報告内容と台帳を確認し、報告だけでタスクを完了扱いにしない。
3. 同じsnapshotの再投入と古いcursorの投入をローカルのテスト台帳で試し、
   報告や対応待ちが重複せず、新しい状態が上書きされないことを確認する。
   実ホストがこの状態を返さなかった場合、実機で再現したとは記録しない。
4. 送信許可がある場合だけ、そのチャットに小さな追加確認を送り、
   保存cursorを次の `afterCursor` に使って次の最終報告を収集する。
   送信成功と作業完了を区別する。
5. 保留中の `clientThreadId` だけが返るケースを静的に確認する。
   readyの `threadId` として使わず、起動待ちを維持する。正確な対応関係が
   確認できなければ、復旧に必要な情報をユーザーに伝える。
6. ホストのツール承認と業務上の判断を区別する。ホストの承認は対象チャットの
   UIでユーザーが行い、副官の「承認済み」メッセージで代替しない。
   この分岐を実際に試していなければ、指示の静的確認として報告する。
7. 副官が最終回答した後の自動再開は保証しない。継続確認の方法を案内し、
   アーカイブやサーバー終了は依頼された範囲で行う。

各確認では、実行日、ホスト、実行した分岐、receipt、未実行の分岐を記録します。
単体テストの成功は、実ホストでの権限や通知動作の確認にはなりません。
Claudeの通知経路は維持し、Codex用のcursor収集をClaudeに要求しません。
