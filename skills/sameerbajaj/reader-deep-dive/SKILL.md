---
name: reader-deep-dive
description: 每日简报将您最近阅读的内容与您的长期资料库联系起来。
metadata: {"clawdbot":{"emoji":"🤿","requires":{"env":["READWISE_TOKEN"]}}}
---

# 深度阅读功能 🤿

你的阅读列表不应该只是一个仅供阅读的“记忆库”。这个功能会检查你最近保存的内容，从你的阅读记录中（无论是最近3天、3个月还是几年前的内容）找出相关的主题，并向你发送一份包含背景信息的简报，告诉你为什么应该重新阅读这些内容。

它将“我把这个内容保存在某个地方了”转化为“这是你关于这个主题的思考时间线”。

## 工作原理

1. **扫描最近的阅读记录**：检查你的Readwise Reader应用程序中“新文件”文件夹中过去24小时内添加的文件。
2. **识别阅读主题**：使用你系统的默认大型语言模型（LLM）来分析你当前关注的主题。
3. **时间背景信息**：搜索你的阅读历史记录，找出不同时间框架下的相关内容。
4. **发送简报**：通过WhatsApp发送一条简报，将你当前的阅读内容与过去的阅读记录联系起来。

## 设置

1. 从 [readwise.io/access_token](https://readwise.io/access_token) 获取你的访问令牌。
2. 将访问令牌设置到你的环境中：
    ```bash
    export READWISE_TOKEN="your_token_here"
    ```

## 使用方法

**手动触发**：
```bash
bash scripts/brief.sh
```

**定时任务（Cron）**：
每天下午2点自动运行：
```bash
clawdbot cron add --id reader_brief --schedule "0 14 * * *" --command "bash scripts/brief.sh"
```

## 自定义

如果你想更改简报的语气或格式，可以在 `prompts/briefing.txt` 文件中进行调整。默认情况下，简报采用简洁、适合WhatsApp发送的格式。