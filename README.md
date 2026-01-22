# NotebookLM Claude Code Skill

**Claude CodeからNotebookLMに直接質問し、ドキュメントに基づいた回答を取得**

[![Claude Code Skill](https://img.shields.io/badge/Claude%20Code-Skill-purple.svg)](https://www.anthropic.com/news/skills)

---

## ⚠️ 重要

**ローカルの[Claude Code](https://github.com/anthropics/claude-code)でのみ動作します。Web UIでは動作しません。**

---

## インストール

```bash
# スキルディレクトリにクローン
mkdir -p ~/.claude/skills
cd ~/.claude/skills
git clone https://github.com/PleasePrompto/notebooklm-skill notebooklm

# Claude Codeで確認
"What skills do I have?"
```

初回使用時に自動で環境セットアップ（.venv作成、依存関係インストール）されます。

---

## 使い方

### 1. 認証（初回のみ）

```
"Set up NotebookLM authentication"
```

Chromeが開くのでGoogleアカウントでログイン。

### 2. ノートブック作成

[notebooklm.google.com](https://notebooklm.google.com) でノートブックを作成し、ドキュメントをアップロード。

**共有設定:** ⚙️ Share → Anyone with link → Copy

### 3. ライブラリに追加

```
"Add this NotebookLM to my library: [URL]"
```

### 4. 質問

```
"What does my React docs say about hooks?"
```

---

## 主な機能

- **ソースに基づいた回答** - ハルシネーションを大幅削減
- **直接統合** - コピペ不要
- **ノートブック管理** - 複数ノートブックをライブラリ化
- **自動認証** - 一度ログインすれば持続

---

## 制限事項

- ローカルClaude Code専用（Web UIでは動作しない）
- レート制限あり（無料アカウント: 50クエリ/日）
- ドキュメントは手動でNotebookLMにアップロード必要

---

## トラブルシューティング

| 問題 | 解決策 |
|-----|-------|
| 認証エラー | `"Reset NotebookLM authentication"` |
| ブラウザクラッシュ | `"Clear NotebookLM browser data"` |

---

## 免責事項

ブラウザ自動化を使用しています。専用のGoogleアカウントの使用を推奨します。

---

[NotebookLM MCP Server](https://github.com/PleasePrompto/notebooklm-mcp) の Claude Code Skill 版です。
