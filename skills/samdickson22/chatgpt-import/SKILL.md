---
name: chatgpt-import
description: 将 ChatGPT 的对话历史导入 OpenClaw 的内存搜索系统。此功能可用于在从 ChatGPT 迁移数据时，让 OpenClaw 访问旧对话记录，或构建可搜索的过去聊天记录档案。
---

# 将 ChatGPT 对话导入 OpenClaw 以支持内存搜索

将您的 ChatGPT 对话导入 OpenClaw，以便可以通过内存搜索功能进行查找。

## 工作流程

### 1. 从 ChatGPT 导出对话数据

按照 [references/export-guide.md](references/export-guide.md) 的说明下载 `conversations.json` 文件。

### 2. 将数据转换为 Markdown 格式

```bash
python3 scripts/convert_chatgpt.py \
  --input /path/to/conversations.json \
  --output /path/to/chatgpt-history
```

选项：`--min-messages N` 可用于跳过无关紧要的对话（默认值：2）。

### 3. 将数据嵌入到 SQLite 数据库中

```bash
export OPENAI_API_KEY=sk-...
python3 scripts/bulk_embed.py \
  --history-dir /path/to/chatgpt-history \
  --db /path/to/chatgpt-memory.sqlite
```

选项：`--model`、`--batch-size`、`--max-workers`、`--chunk-size`、`--api-key`。

### 4. 配置 OpenClaw

在 OpenClaw 的配置文件中添加一个新的搜索路径：

```yaml
memorySearch:
  extraPaths:
    - /path/to/chatgpt-memory.sqlite
```

然后重启 OpenClaw 服务：

```bash
openclaw gateway restart
```

## 重要说明

- **需要 OpenAI API 密钥。** 嵌入脚本会将对话内容发送到 `api.openai.com` 进行处理。如果对话中包含敏感信息，请先进行过滤或使用受限范围的 API 密钥。
- **数据不会被存储。** 生成的数据库不会保存您的 API 密钥。
- **请先备份数据。** 嵌入脚本不会覆盖现有的数据库文件。
- **嵌入服务需要付费。** 使用 `text-embedding-3-small` 服务，大约 2,400 条对话的费用约为 0.15 美元。