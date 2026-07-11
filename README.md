# Agent Skills

このリポジトリは、[Agent Skills](https://agentskills.io) 形式の再利用可能な
スキルを配布します。各スキルは `SKILL.md` を含むディレクトリです。

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
npx skills add example/agent-skills --skill pr-handoff
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
npx degit example/agent-skills/dev/pr-handoff ~/.codex/skills/pr-handoff

# Claude Code
npx degit example/agent-skills/dev/pr-handoff ~/.claude/skills/pr-handoff

# GitHub Copilot（個人用）
npx degit example/agent-skills/dev/pr-handoff ~/.copilot/skills/pr-handoff

# Cursor（プロジェクト用。実行場所は対象プロジェクトのルート）
npx degit example/agent-skills/dev/pr-handoff .cursor/skills/pr-handoff
```

プロジェクト用スキルは、コピー後に `.agents/skills/` などの対象ディレクトリを
コミットしてください。チーム全員がリポジトリを取得すると同じスキルを利用できます。

## 公開・更新時の運用

- スキル名はディレクトリ名と `SKILL.md` の frontmatter にある `name` を一致させる。
- 導入前に `SKILL.md`、同梱スクリプト、参照ファイルを確認する。スキルはエージェントの行動やコマンド実行に影響する。
- GitHub のリリースタグまたはコミット SHA を指定すると、チームで同じ版を再現しやすい。
- 非公開リポジトリは、利用環境で GitHub 認証を済ませたうえで `git clone` してからコピーする。

## 収録スキル

- `dev/backend-api-implementation`
- `dev/pr-handoff`
- `dev/purpose-driven-software-design`
- `dev/terraform-implementation`
- `meta/empirical-prompt-tuning`
- `meta/skill-creation`
