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

各スキルは必須の `SKILL.md` と、必要に応じた `README.md`、`references/`、
`scripts/` で構成します。スキル名、ディレクトリ名、frontmatterの `name` は一致させます。
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
2. `dev/` または `meta/` に正本を配置し、必要な参照資料・スクリプト・READMEを揃えます。
3. 新規追加・名称変更・用途変更は、[プロジェクトガイドのスキル一覧](project-guide.md#スキル一覧)に反映します。関連する利用フローも確認します。
4. このプロジェクトの作業に使うスキルとして追加する場合は、両ツール向けの相対リンクを揃え、リンク先を確認します。
5. 配布用メタデータを再生成し、変更したスキルと関連スクリプトを検証します。

READMEは閲覧者・利用者向けの概要と導入方法を中心に保ちます。
スキル一覧・説明・利用フローはプロジェクトガイド、開発手順はこの文書にまとめ、
READMEにはリンクを置きます。

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
全スキルのvalidatorを常に実行します。`local-intake` のテストとCLIのヘルプ確認は、
次のPython関連ファイルに差分がある場合のみ実行します。

- Pythonソース: `*.py`・`*.pyi`。
- 設定・依存関係: `pyproject.toml`、`setup.cfg`、`tox.ini`、`pytest.ini`、`.python-version`、
  `requirements*.txt`・`requirements*.in`、`Pipfile`・`Pipfile.lock`、`poetry.lock`、`uv.lock`、`pdm.lock`。配置先は問いません。
- CI設定: `.github/workflows/ci.yml`。

PRはベースブランチとの分岐点から、pushは前回コミットからの差分で判定します。
削除・名称変更も対象とし、比較元がない初回pushではテストを実行します。
Markdownなどだけの変更ではランタイムテストをスキップしますが、スキル検証は残ります。
指示の静的レビューと実行比較は別の証拠として扱い、実測していない効果は保証しません。

## コミット・PR・公開前の確認

- コミット件名は `feat:`・`fix:`・`docs:`・`refactor:`・`chore:` などの規約に従い、目的ごとにまとめます。
- PRでは変更の目的、影響する配置先、実施した検証を説明し、発動条件やエージェントの挙動が変わる場合は変更前後の例を添えます。
- 正本とツール向け配置、スキル一覧、各README、生成した `apm.yml` の整合性を確認します。
- スキル本文、同梱スクリプト、参照資料に秘密情報が含まれていないことを確認します。
- チームで同じ版を再現する必要がある場合は、利用者にコミットSHAを案内します。

PR説明とコミット分割案の整理には [pr-handoff](../dev/pr-handoff/SKILL.md)を使えます。
このスキルは提案のみで、commit・push・PR作成そのものは実行しません。
