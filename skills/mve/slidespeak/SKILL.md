---
name: slidespeak
description: 通过 SlideSpeak API 生成、编辑和管理 PowerPoint 演示文稿。当用户需要从文本或文档创建演示文稿、编辑现有演示文稿或使用演示文稿模板时，可以使用此技能。
allowed-tools: Bash Read Write
metadata:
  {
    "openclaw":
      {
        "emoji": "🦜",
        "homepage": "https://slidespeak.co",
        "requires": { "env": [ "SLIDESPEAK_API_KEY" ] },
        "primaryEnv": "SLIDESPEAK_API_KEY",
      },
  }
---

# SlideSpeak 演示文稿制作技能

该技能允许您使用 SlideSpeak API 创建和编辑 PowerPoint 演示文稿。

## 重要提示：执行时间

**生成演示文稿需要 30-60 秒。**

### 选项 1：等待完成（默认设置）
运行命令后等待脚本完成。脚本会自动进行内部检查：
```bash
node scripts/slidespeak.mjs generate --text "Topic"
```
- 等待任务完成（通常需要 30-60 秒）
- 返回包含下载链接的完整结果

### 选项 2：使用 `--no-wait` 选项立即获取结果
如果您无法等待命令完成，可以使用 `--no-wait` 选项：
```bash
node scripts/slidespeak.mjs generate --text "Topic" --no-wait
```
立即返回结果：
```json
{
  "success": true,
  "data": {
    "task_id": "abc123...",
    "message": "Task started. Check status with: node scripts/slidespeak.mjs status abc123..."
  }
}
```

之后继续检查任务状态，直到任务完成：
```bash
node scripts/slidespeak.mjs status <task_id>
```
当 `task_status` 为 `SUCCESS` 时，使用 `request_id` 下载演示文稿。

### 超时处理
如果脚本在等待过程中超时，它会返回 `task_id`，以便您继续检查任务状态：
```json
{
  "success": true,
  "data": {
    "complete": false,
    "task_id": "abc123...",
    "task_status": "STARTED",
    "message": "Task still processing. Check status with: node scripts/slidespeak.mjs status abc123..."
  }
}
```

## 设置要求

必须设置 `SLIDESPEAK_API_KEY` 环境变量。您可以从 [https://app.slidespeak.co/settings/developer](https://app.slidespeak.co/settings/developer) 获取 API 密钥。

## 快速参考

所有命令都使用 `scripts/slidespeak.mjs` 这个辅助脚本。该脚本负责处理 API 认证，并自动等待异步任务的完成（无需手动检查）。

### 从文本生成演示文稿

```bash
node scripts/slidespeak.mjs generate --text "Your topic or content" --length 6
```

参数选项：
- `--text`（必填）：演示文稿的主题或内容
- `--length`：幻灯片数量（默认：10 张）
- `--template`：模板名称或 ID（默认：“default”）
- `--language`：输出语言（默认：“ORIGINAL”）
- `--tone`：风格选项（随意、专业、幽默、教育性、销售型）
- `--verbosity`：表达风格（简洁、标准、内容丰富）
- `--no-images`：禁用图片自动加载
- `--no-cover`：不包含封面幻灯片
- `--no-toc`：不包含目录

### 从上传的文档生成演示文稿

首先上传文档，然后生成演示文稿：
```bash
# Upload a document (PDF, DOCX, PPTX, etc.)
node scripts/slidespeak.mjs upload /path/to/document.pdf

# Use the returned document_uuid to generate
node scripts/slidespeak.mjs generate --document <document_uuid> --length 10
```

支持的文件格式：`.pdf`、`.docx`、`.doc`、`.pptx`、`.ppt`、`.xlsx`、`.txt`、`.md`

### 查看可用模板

```bash
# Default templates
node scripts/slidespeak.mjs templates

# Branded templates (if configured)
node scripts/slidespeak.mjs templates --branded
```

### 下载演示文稿

生成完成后，使用 `request_id` 下载演示文稿：
```bash
node scripts/slidespeak.mjs download <request_id>
```

返回一个包含临时下载链接的 JSON 对象。

### 编辑现有演示文稿

编辑现有演示文稿中的幻灯片：
```bash
# Insert a new slide at position 2
node scripts/slidespeak.mjs edit-slide \
  --presentation-id <id> \
  --type INSERT \
  --position 2 \
  --prompt "Content about market analysis"

# Regenerate slide at position 3
node scripts/slidespeak.mjs edit-slide \
  --presentation-id <id> \
  --type REGENERATE \
  --position 3 \
  --prompt "Updated content for this slide"

# Remove slide at position 4
node scripts/slidespeak.mjs edit-slide \
  --presentation-id <id> \
  --type REMOVE \
  --position 4
```

编辑操作类型：
- `INSERT`：在指定位置添加新幻灯片
- `REGENERATE`：替换现有幻灯片的内容
- `REMOVE`：删除幻灯片（无需提示）

### 检查任务状态

用于调试或手动检查任务进度：
```bash
node scripts/slidespeak.mjs status <task_id>
```

### 获取账户信息

```bash
node scripts/slidespeak.mjs me
```

## 单个幻灯片的生成

如需对每个幻灯片进行精确控制，请使用单张幻灯片的生成接口。详细信息请参阅 `references/API.md`。
```bash
node scripts/slidespeak.mjs generate-slides --config slides.json
```

其中 `slides.json` 文件包含所有幻灯片的详细信息：
```json
{
  "slides": [
    {"title": "Introduction", "layout": "title", "content": "Welcome message"},
    {"title": "Key Points", "layout": "bullets", "item_amount": 4, "content": "Main discussion points"}
  ],
  "template": "default"
}
```

## Webhook

订阅以在任务完成后接收通知：
```bash
# Subscribe
node scripts/slidespeak.mjs webhook-subscribe --url "https://your-webhook.com/endpoint"

# Unsubscribe
node scripts/slidespeak.mjs webhook-unsubscribe --url "https://your-webhook.com/endpoint"
```

## 错误处理

脚本会返回以下格式的 JSON 数据：
- 成功：`{"success": true, "data": {...}}`
- 错误：`{"success": false, "error": "message"}`

## 常见工作流程

- **根据主题创建演示文稿**：```bash
node scripts/slidespeak.mjs generate --text "Introduction to Machine Learning" --length 8 --tone educational
```
- **从 PDF 报告生成演示文稿**：```bash
# Upload the PDF
RESULT=$(node scripts/slidespeak.mjs upload report.pdf)
DOC_ID=$(echo $RESULT | jq -r '.data.document_uuid')

# Generate presentation
node scripts/slidespeak.mjs generate --document "$DOC_ID" --length 12
```
- **编辑演示文稿以添加新幻灯片**：```bash
node scripts/slidespeak.mjs edit-slide \
  --presentation-id "abc123" \
  --type INSERT \
  --position 5 \
  --prompt "Add a slide about quarterly revenue growth with charts"
```

## 额外资源

有关 API 的详细文档（包括所有参数、布局类型和限制），请参阅 `references/API.md`。