---
name: usememos-api
version: "1.0.0"
description: 与 UseMemos 交互——这是一个轻量级的、自托管的备忘录管理工具。您可以创建、搜索、查看备忘录列表，并上传附件。
tags: ["memos", "notes", "self-hosted", "knowledge-base", "attachments"]
homepage: https://github.com/minstn/usememos
source: https://github.com/minstn/usememos
metadata:
  openclaw:
    requires:
      env:
        - USEMEMOS_URL
        - USEMEMOS_TOKEN
      bins:
        - python3
    primaryEnv: USEMEMOS_TOKEN
---
# UseMemos

## 设置

需要 `.env` 文件中的环境变量：
- `USEMEMOS_URL` — 实例 URL（例如：`http://localhost:5230`）
- `USEMEMOS_TOKEN` — 来自“设置”>“我的账户”的访问令牌

## 脚本

| 脚本 | 用法 | 描述 |
|--------|-------|-------------|
| `create_memo.py` | `<内容> [可见性]` | 创建备忘录（可见性：私有/受保护/公开） |
| `list_memos.py` | `[限制] [标签]` | 列出最近的备忘录（默认：10 条） |
| `search_memos.py` | `<查询> [限制]` | 按内容搜索备忘录 |
| `upload_attachment.py` | `<文件路径> [文件名] [类型]` | 上传文件附件 |
| `upload_and_link_attachment.py` | `<备忘录ID> <文件路径> [文件名> [类型]` | 上传附件并将其链接到备忘录 |

所有脚本都位于 `scripts/` 目录中，可以通过 `python3 scripts/<脚本名>` 来运行。

## 示例

```bash
# Create a memo with tags
python3 scripts/create_memo.py "Meeting notes from standup #work"

# List recent memos
python3 scripts/list_memos.py 5

# Search memos
python3 scripts/search_memos.py "website redesign"

# Upload attachment standalone
python3 scripts/upload_attachment.py photo.jpg "sale_photo.jpg" "image/jpeg"

# Create memo then attach a file
python3 scripts/create_memo.py "Sale: Stromer Charger #eBike #income"
# Use the memo ID from output:
python3 scripts/upload_and_link_attachment.py <memo_id> charger_photo.jpg
```

## 注意事项

- 备忘录的 ID 是简短的字符串，例如 `3UZ7uBbHsLEAwdYE5HKhjd`（而不是 `memos/3UZ7uBbHsLEAwdYE5HKhjd`）
- 标签使用 `#标签` 语法直接插入备忘录内容中
- 附件的默认 MIME 类型为 `image/jpeg`；对于其他文件，请明确指定类型

## API 参考

有关端点文档，请参阅 [references/api.md](references/api.md)。