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
npx skills add ta-dadadada/skills --skill pr-handoff
```

### apm

[`apm`](https://github.com/microsoft/apm)（Agent Package Manager）でも、
各スキルディレクトリを `SKILL.md` を含む "skill bundle" としてそのまま
インストールできます。各スキルディレクトリには `SKILL.md` の frontmatter
（`name`・`description`・`license`）から自動生成した `apm.yml` を同梱して
おり、`name`・`description`・`license` が apm 側にも渡ります
（生成スクリプトは [`scripts/generate_apm_yml.py`](scripts/generate_apm_yml.py)、
`SKILL.md` を編集したら再実行してください。リポジトリ直下の `apm.yml`
も同スクリプトが再生成します）。

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

## 公開・更新時の運用

- スキル名はディレクトリ名と `SKILL.md` の frontmatter にある `name` を一致させる。
- 導入前に `SKILL.md`、同梱スクリプト、参照ファイルを確認する。スキルはエージェントの行動やコマンド実行に影響する。
- GitHub のリリースタグまたはコミット SHA を指定すると、チームで同じ版を再現しやすい。
- 非公開リポジトリは、利用環境で GitHub 認証を済ませたうえで `git clone` してからコピーする。

## 収録スキル

- `dev/backend-api-implementation`
- `dev/business-ui-design`
- `dev/characterization-testing`
- `dev/doc-sync`
- `dev/domain-modeling`
- `dev/frontend-ui-design`
- `dev/frontend-ui-implementation`
- `dev/hypothesis-driven-debugging`
- `dev/issue-kickoff`
- `dev/local-intake`
- `dev/pr-handoff`
- `dev/purpose-driven-software-design`
- `dev/session-goal`
- `dev/session-handover`
- `dev/session-resume`
- `dev/terraform-implementation`
- `dev/work-report`
- `meta/shiranui-hansode`
- `meta/shiranui-hanten`
- `meta/skill-opportunity-review`

UI設計のみには `frontend-ui-design` を単独で利用できます。実装まで行う場合は
`frontend-ui-implementation` も導入してください。前者が設計契約と
アクセシビリティ要件を決め、後者がHTML・ARIA・CSS・JSで実現し、実UIを検証します。
設計契約が確定している実装作業には実装スキルから入れます。

業務ツールの情報構造やレコード操作も設計する場合は `business-ui-design` を追加します。
業務UIの実装は `business-ui-design` → `frontend-ui-design` →
`frontend-ui-implementation` の順に、同じ設計記録と受入ケースを引き継ぎます。
個別インストールでは必要な各スキルを導入してください。ルートのAPMパッケージは
3スキルを含む全収録スキルをインストールします。
