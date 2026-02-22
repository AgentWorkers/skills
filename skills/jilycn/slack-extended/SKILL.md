---
name: slack-extended
description: 在 Slack 中上传文件、管理画布以及管理书签。当您需要在 Slack 频道中分享文件、创建/编辑画布或添加/整理链接书签时，可以使用此功能。它补充了核心的 Slack 功能（如处理消息、反应和固定消息）。
metadata: { "openclaw": { "emoji": "📎", "requires": { "config": ["channels.slack"] }, "credentials": { "source": "~/.openclaw/openclaw.json", "keys": ["channels.slack.botToken"], "scopes": ["files:write", "canvases:write", "bookmarks:write", "bookmarks:read"] } } }
---
# Slack 扩展功能

该扩展功能为基本的 `slack` 能力增加了文件上传和画布管理功能。它使用 Python 脚本，通过 `~/.openclaw/openclaw.json` 中的机器人令牌直接调用 Slack API。

**所需 OAuth 权限范围：** `files:write`, `canvases:write`（如未授权，请在 api.slack.com 上添加这些权限）。

## 文件上传

将本地文件上传到 Slack 频道：

```bash
python3 /mnt/openclaw/skills/slack-extended/scripts/slack_file_upload.py \
  --channel C123ABC \
  --file /path/to/file.png \
  --title "Q4 Report" \
  --message "Here's the latest report"
```

**参数：**
- `--channel`（必选）：用于分享文件的频道 ID
- `--file`（必选）：本地文件的路径
- `--title`：显示的标题（默认为文件名）
- `--message`：随文件一起发布的评论

返回包含 `file_id`, `permalink`, 和 `channel` 的 JSON 数据。

**常见用法：**
- 共享生成的图表：`--file /tmp/chart.png --title "性能图表"`
- 共享文本文件：`--file ./notes.txt --title "会议笔记"`
- 带有说明的文件分享：`--message "GEM v2 的回测结果" --file results.csv`

## 画布操作

管理 Slack 画布（协作文档）：

### 创建画布

```bash
python3 /mnt/openclaw/skills/slack-extended/scripts/slack_canvas.py create \
  --title "Sprint Notes" \
  --markdown "## Goals\n- Ship feature X\n- Fix bug Y"
```

### 编辑画布

- 添加内容：```bash
python3 /mnt/openclaw/skills/slack-extended/scripts/slack_canvas.py edit \
  --canvas-id F07ABCD1234 \
  --operation insert_at_end \
  --markdown "## Update\nNew section added"
```
- 替换画布中的部分内容：```bash
python3 /mnt/openclaw/skills/slack-extended/scripts/slack_canvas.py edit \
  --canvas-id F07ABCD1234 \
  --section-id temp:C:abc123 \
  --operation replace \
  --markdown "## Revised Section\nUpdated content"
```

**操作选项：** `insert_at_start`, `insert_at_end`, `insert_after`, `replace`, `delete`

### 查找画布中的部分内容

```bash
python3 /mnt/openclaw/skills/slack-extended/scripts/slack_canvas.py sections \
  --canvas-id F07ABCD1234
```

### 删除画布

```bash
python3 /mnt/openclaw/skills/slack-extended/scripts/slack_canvas.py delete \
  --canvas-id F07ABCD1234
```

### 设置画布访问权限

```bash
python3 /mnt/openclaw/skills/slack-extended/scripts/slack_canvas.py access \
  --canvas-id F07ABCD1234 \
  --channel C123ABC \
  --level edit
```

## 画布 Markdown 支持的功能

画布支持以下格式：加粗、斜体、下划线、标题（h1-h3）、项目符号/有序列表、复选列表、代码块、代码片段、链接、表格（最多 300 个单元格）、块引用、分隔符和表情符号。

**引用用户/频道：** `![](@USER_ID)` 用于引用用户，`![](#CHANNEL_ID)` 用于引用频道。

## 书签

管理 Slack 频道顶部书签栏中的书签。

**限制：** Slack API 仅支持 **链接** 书签。文件夹仅通过用户界面创建，无法通过 API 操作。

**所需 OAuth 权限范围：** `bookmarks:write`, `bookmarks:read`

### 列出书签

```bash
python3 /mnt/openclaw/skills/slack-extended/scripts/slack_bookmark.py list \
  --channel C123ABC
```

### 添加书签

```bash
python3 /mnt/openclaw/skills/slack-extended/scripts/slack_bookmark.py add \
  --channel C123ABC \
  --title "Design Docs" \
  --link "https://example.com" \
  --emoji ":link:"
```

### 编辑书签

```bash
python3 /mnt/openclaw/skills/slack-extended/scripts/slack_bookmark.py edit \
  --channel C123ABC \
  --bookmark-id Bk123 \
  --title "New Title"
```

### 删除书签

```bash
python3 /mnt/openclaw/skills/slack-extended/scripts/slack_bookmark.py remove \
  --channel C123ABC \
  --bookmark-id Bk123
```

## 常见问题解决方法：**

- **`missing_scope` 错误**：在 api.slack.com 上添加所需的权限范围（`files:write` 或 `canvases:write`），然后重新安装应用程序到工作空间。
- **`channel_not_found`：使用频道 ID（例如 `C07ABC123`），而不是频道名称。
- **`not_authed`：机器人令牌可能已更改，请检查 `~/.openclaw/openclaw.json` 文件。
- **画布编辑失败**：请先查找画布中的部分内容以获取有效的 `section_id` 值。
- **书签权限问题**：在 api.slack.com 上添加 `bookmarks:write` 和 `bookmarks:read` 权限，然后重新安装应用程序。
- **文件夹不支持**：Slack API 不支持创建文件夹——只能通过用户界面创建文件夹。