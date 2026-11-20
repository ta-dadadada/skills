# ルールの導入・更新・アンインストール

`install-agent-rules` は、同梱するルールをClaude Codeの `.claude/rules/` に配置するスキルです。
配布するルールは、設計の判断基準をまとめた `software-design` と、README・仕様書などの情報配置と更新を扱う `project-documentation` です。以下の例では使いたいルールのIDを指定してください。
スキルをインストールしただけではrulesは配置されません。導入を依頼するか、スクリプトを実行します。

## Claude CodeとCodexでの読み込み

Claude Codeは導入先の `.claude/rules/` を自動で読み込みます。Codexなど別のエージェントからスクリプトを実行しても配置先は同じです。Codexで利用する場合は、導入できたルールについて、プロジェクトの `AGENTS.md` に次のように追記してください。

```markdown
- 設計・実装・レビュー時は `.claude/rules/ta-dadadada-software-design.md` を読み、その判断基準を使う。
- プロジェクト文書を作成・更新するときは `.claude/rules/ta-dadadada-project-documentation.md` を読む。
```

ユーザー単位で導入した場合は、Codexのユーザー指示（通常は `~/.codex/AGENTS.md`）から、インストーラーが返した配置先の絶対パスを参照します。インストーラーは指示ファイルを編集しないため、アンインストール時は対応する参照行も手動で削除してください。ほかのエージェントでは、そのツールが読み込む指示ファイルから参照します。

## エージェントに依頼する

通常の[スキル導入方法](../README.md#github-からインストールする)で `install-agent-rules` を導入し、次のように依頼します。

```text
install-agent-rules で、このプロジェクトに software-design を導入してください。
```

```text
install-agent-rules で、このプロジェクトの software-design を更新してください。
```

```text
install-agent-rules で、このプロジェクトから software-design をアンインストールしてください。
```

ルール名を省略すると、エージェントが候補と説明を示し、選択を待ちます。選択後、スクリプトを実行して結果を説明します。
導入先の読取り、差分判定、書込み、削除、管理情報の更新はすべてスクリプトが行います。
衝突があってもエージェントが直接ファイルを編集して解決することはありません。

## GitHubから直接実行する

macOS・Linuxの端末でGit、curl、Python 3.11以上を使用します。対象プロジェクトのルートで次を実行すると、一覧から入力したIDのルールを導入・更新します。空入力でキャンセルできます。

```sh
curl -fsSL https://raw.githubusercontent.com/ta-dadadada/skills/HEAD/scripts/install-agent-rules.sh | sh
```

引数を渡す場合は末尾の `sh` を、一覧なら `sh -s -- list`、計画の確認なら `sh -s -- plan --rule software-design --project .`、削除なら `sh -s -- uninstall --rule software-design --project .` に置き換えます。各回で既定ブランチを一時取得し、導入と削除には同じ取得内容で計画・適用を行います。

## スクリプトを直接使う

Python 3.11以上、macOSまたはLinuxが必要です。外部Pythonパッケージやネットワーク接続は不要です。
以下はリポジトリ直下からの例です。スキルだけ導入した場合は、そのスキルのディレクトリにある `scripts/install_rules.py` を指定します。

```bash
# 配布物の一覧
python3 dev/install-agent-rules/scripts/install_rules.py list

# 導入・更新の計画（書込みなし）
python3 dev/install-agent-rules/scripts/install_rules.py plan \
  --rule software-design --project /absolute/project

# 結果に含まれるplan_idを指定して適用
python3 dev/install-agent-rules/scripts/install_rules.py apply \
  --rule software-design --project /absolute/project --plan-id RETURNED_ID
```

更新も同じコマンドです。新しいスキルパッケージを取得してから計画・適用します。
全プロジェクトへ適用する場合は、両コマンドの `--project /absolute/project` を `--user` に置き換えます。
配置先は `~/.claude/rules/ta-dadadada-software-design.md` になります。

アンインストールは両コマンドに `--operation uninstall` を指定します。

```bash
python3 dev/install-agent-rules/scripts/install_rules.py plan \
  --rule software-design --project /absolute/project --operation uninstall
python3 dev/install-agent-rules/scripts/install_rules.py apply \
  --rule software-design --project /absolute/project --operation uninstall --plan-id RETURNED_ID
```

配布するファイル名には配布元の `ta-dadadada-` を付けます。試作版で `software-design.md` を導入済みの場合は、旧版でアンインストールしてから新版を導入してください。

## 衝突時の動作

前回導入時の内容と現在のファイルを比較し、ローカル変更があれば更新・削除を停止します。
管理履歴のない別内容も上書きしません。計画後に原本・配置先・管理情報が変わった場合は、再計画が必要です。
強制上書きや自動マージはありません。他のrulesや `CLAUDE.md` との意味上の矛盾を自動判定するものではありません。

管理情報は `.claude/.agent-rules-<id>.json` に保存します。プロジェクトのrulesをGitで共有する場合は、
この管理情報も一緒に共有すると導入時の基準を引き継げます。内容にはハッシュのみを記録し、絶対パスは含めません。
`.claude/.agent-rules-<id>.lock` は実行時の排他制御用で、Git管理は不要です。
スクリプトは `.gitignore` を編集しません。

アンインストールは対象ルールと管理情報だけを削除します。ロックファイルとディレクトリは残します。
途中で停止した場合の復旧方法、各状態・終了コードは[導入契約](../dev/install-agent-rules/references/installer-contract.md)を参照してください。
