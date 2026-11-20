# Agent Skills

このリポジトリは、[Agent Skills](https://agentskills.io) 形式の再利用可能な
スキルを配布します。各スキルは `SKILL.md` を含むディレクトリです。

## 収録スキル

スキル一覧・簡単な説明・おすすめの利用フローは
[プロジェクトガイド（日本語）](docs/project-guide.md)を参照してください。

## GitHub からインストールする

以下では、GitHub リポジトリを `<owner>/<repository>`、スキル名を
`<skill-name>` と表記します。たとえば、`pr-handoff` を導入する場合は
`<skill-name>` を `pr-handoff` に置き換えます。

### `skills` CLI（推奨）

[`skills`](https://github.com/vercel-labs/skills) CLI は、検出した対応エージェントの
スキルディレクトリにインストールします。

```bash
npx skills add <owner>/<repository> --skill <skill-name>
```

例:

```bash
npx skills add ta-dadadada/skills --skill pr-handoff
```

### apm

[`apm`](https://github.com/microsoft/apm)（Agent Package Manager）でも、
各スキルディレクトリを `SKILL.md` を含む "skill bundle" としてそのまま
インストールできます。各スキルディレクトリには `apm.yml` を同梱しており、
スキル名・説明・ライセンスが apm 側にも渡ります。

#### 全スキルをまとめてインストールする

リポジトリ直下の [`apm.yml`](apm.yml) が全スキルを依存として列挙した
集約パッケージになっているため、リポジトリを 1 つ指定するだけで収録
スキルすべてがインストールされます。

```bash
apm install ta-dadadada/skills
```

#### 個別のスキルをインストールする

```bash
apm install <owner>/<repository>/<skill-path>
```

例:

```bash
apm install ta-dadadada/skills/dev/pr-handoff
```

`apm.yml` で依存として宣言する場合:

```yaml
dependencies:
  apm:
    - ta-dadadada/skills/dev/pr-handoff
```

その後 `apm install` を実行します。

バージョンを固定したい場合は、コミット SHA を参照に含めます
（このリポジトリはリリースタグを運用していないため、SHA 参照を使って
ください）。

```bash
apm install ta-dadadada/skills/dev/pr-handoff#<commit-sha>
```

```yaml
dependencies:
  apm:
    - ta-dadadada/skills/dev/pr-handoff#<commit-sha>
```

対象を明示したい場合や CLI を利用しない場合は、次のツール別の配置先へ
スキルディレクトリをコピーします。GitHub のリポジトリをそのまま取得するには
[`degit`](https://github.com/Rich-Harris/degit) を利用できます。

```bash
npx degit <owner>/<repository>/<skill-path> <destination>
```

`<skill-path>` はリポジトリ内のスキルディレクトリです。例えば
`pr-handoff` は `dev/pr-handoff` です。

## ツール別の配置先

| ツール | 個人用（全プロジェクト） | プロジェクト用（リポジトリで共有） | 補足 |
| --- | --- | --- | --- |
| Codex CLI | `$CODEX_HOME/skills/<skill-name>`（通常は `~/.codex/skills/<skill-name>`） | `.agents/skills/<skill-name>` | `CODEX_HOME` を設定している場合はその配下を使用する。 |
| Claude Code | `~/.claude/skills/<skill-name>` | `.claude/skills/<skill-name>` | スキルは自動選択または `/skill-name` で利用できる。 |
| GitHub Copilot | `~/.copilot/skills/<skill-name>` または `~/.agents/skills/<skill-name>` | `.github/skills/<skill-name>`、`.agents/skills/<skill-name>`、または `.claude/skills/<skill-name>` | Copilot CLI、VS Code の Agent mode、Copilot coding agent で利用できる。 |
| Cursor | `~/.cursor/skills/<skill-name>` | `.cursor/skills/<skill-name>` または `.agents/skills/<skill-name>` | Cursor を再起動するか、新しい Agent セッションを開始して認識させる。 |

### 手動インストール例

```bash
# Codex CLI
npx degit ta-dadadada/skills/dev/pr-handoff ~/.codex/skills/pr-handoff

# Claude Code
npx degit ta-dadadada/skills/dev/pr-handoff ~/.claude/skills/pr-handoff

# GitHub Copilot（個人用）
npx degit ta-dadadada/skills/dev/pr-handoff ~/.copilot/skills/pr-handoff

# Cursor（プロジェクト用。実行場所は対象プロジェクトのルート）
npx degit ta-dadadada/skills/dev/pr-handoff .cursor/skills/pr-handoff
```

プロジェクト用スキルは、コピー後に `.agents/skills/` などの対象ディレクトリを
コミットしてください。チーム全員がリポジトリを取得すると同じスキルを利用できます。

## 常用するルールを導入する

Claude Code 向けに、設計の判断基準とプロジェクト文書の書き方を配布しています。

**エージェントから導入する場合**は、`install-agent-rules` スキルを起動し、表示された候補から導入・更新したいルールを選びます。ルール名を指定して「このプロジェクトに `software-design` を導入して」と依頼することもできます。

**ターミナルから直接導入する場合**は、対象プロジェクトのルートで次を実行し、表示されたルール ID を入力します。macOS または Linux で Git、curl、Python 3.11 以上が必要です。

```sh
curl -fsSL https://raw.githubusercontent.com/ta-dadadada/skills/HEAD/scripts/install-agent-rules.sh | sh
```

配置したルールは Claude Code が自動で読み込みます。Codex でも同じインストーラーで配置できますが、利用するには `AGENTS.md` にルールを読む指示を追加してください。記載例と、[ルールの導入手順](docs/rules-guide.md)を参照してください。

## 利用時の注意

- 導入前に `SKILL.md`、同梱スクリプト、参照ファイルを確認する。スキルはエージェントの行動やコマンド実行に影響する。
- コミット SHA を指定すると、チームで同じ版を再現しやすい。
- 非公開リポジトリは、利用環境で GitHub 認証を済ませたうえで `git clone` してからコピーする。

## 開発に参加する

スキルの作成・改訂、このリポジトリのスキル設定、生成・検証・公開の手順は
[開発者ガイド](docs/development-guide.md)を参照してください。
