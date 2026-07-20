# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Language

- Skill bodies (`SKILL.md`), `references/`, and `knowledge/` content are English — these are read by agents and by other maintainers, and are the material Agent Skills syndicates outside this repository.
- ユーザとのやり取りは日本語で行うこと。
- 例外: ユーザー向け運用文書（この `CLAUDE.md` 自身、リポジトリ直下 `README.md`）と、明示的なローカライズ版（`*-ja.md` などファイル名で示された翻訳）は日本語可。スキル本体の言語を変えるものではない。

## このリポジトリについて

コーディングエージェント（Claude Code / Codex / GitHub Copilot / Cursor）向けの、エージェントスキル・サブエージェント設定・プロンプトファイルなどを管理するリポジトリ。ビルドやテストの仕組みはなく、成果物は Markdown ベースの設定・プロンプトファイル群。

## ディレクトリ規約

- `.local/` — gitignore 済み。ローカル専用の作業ファイル置き場。コミット対象のファイルをここに置かないこと。
- `knowledge/` — 参考資料を体系化した知識ベース（英語）。運用ルールは `knowledge/README.md` を参照。生の調査レポートは `.local/` に留め、ここには再利用価値のある蒸留版のみを置く。
- ツールごとにディレクトリを分けて管理する想定。新しい種類の成果物を追加する際は、対象ツールが実際に読み込むパス規約に合わせること：
  - Claude Code スキル: `SKILL.md`（frontmatter に `name` と `description`）を持つディレクトリ
  - Claude Code サブエージェント: frontmatter 付き Markdown（`.claude/agents/*.md` 形式）
  - Cursor: `.cursor/rules/` 形式のルールファイル
  - GitHub Copilot: `copilot-instructions.md` 形式

## 作業上の注意

- スキルの新規作成・更新時は、このリポジトリの `meta/shiranui-hanten` スキル（`meta/shiranui-hanten/SKILL.md`）に従うこと。組み込みの skill-creator ではなくこちらを正とする。
- 各ファイルは特定のツールに配置（コピー/シンボリックリンク）されて初めて機能する。ファイルを追加・改名した場合、配置方法や参照元への影響を確認すること。
