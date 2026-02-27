---
name: ai-twitter-digest
description: "监控一个精心挑选的AI/科技类Twitter账号列表，利用大型语言模型（LLM）汇总当天的关键帖子，并将格式化后的摘要发送到Discord频道。适用场景包括：(1) 自动生成每日来自Twitter/X的AI新闻简报；(2) 安排或一次性向Discord发送Twitter摘要；(3) 管理或更新被监控的账号列表、摘要生成规则或发送格式。"
---
# AI Twitter Digest

该工具通过 AISA API 获取来自 AI/科技领域 influencer 的推文，使用可用的 LLM（Claude、OpenAI 或 Gemini）将其内容翻译成中文，并通过 Discord 发送两部分的摘要：

- **消息 1**：包含推文文本摘要及原始链接的超链接（不提供嵌入预览）。
- **消息 2**：显示前 5 条推文的链接，以 Discord 卡片的形式进行预览。

## 设置

### 1. 运行设置向导（首次使用前必读）

```bash
python3 scripts/setup.py
```

设置向导会：
- 自动从您的环境变量和 OpenClaw 配置中检测 API 密钥。
- 提示您输入缺失的密钥（AISA、LLM、Discord 频道相关密钥）。
- 测试与 AISA 以及您选择的 LLM 提供者的连接。
- 生成一个 `.env` 文件——无需手动编辑。

> 如果您更喜欢手动设置，请在 `scripts/` 目录下创建 `env` 文件，并填写以下内容：
>
> ```env
> AISA_API_KEY=your_aisa_key_here
> DELIVERY_CHANNEL=discord
> DELIVERY_TARGET=channel:your_channel_id_here
> SUMMARY_LANGUAGE=Chinese
> ANTHROPIC_API_KEY=
> OPENAI_API_KEY=
> GEMINI_API_KEY=
> # STATE_FILE=~/.ai-twitter-sent.json
> # MAX_STORED_IDS=500
> # CARD_PREVIEWS=true
> ```

**所需配置参数：**

| 参数 | 说明 |
|--------|--------|
| `AISA_API_KEY` | 用于访问 Twitter 数据的 API 密钥（来源：[aisa.one](https://aisa.one) |
| `DELIVERY_CHANNEL` | 发送摘要的目标渠道（可选：Discord、WhatsApp、Telegram、Slack、Signal） |
| `DELIVERY_TARGET` | 需要发送摘要的具体频道（参见下表） |
| `ANTHROPIC_API_KEY` / `OPENAI_API_KEY` / `GEMINI_API_KEY` | 用于生成摘要的 LLM 的 API 密钥 |
| `SUMMARY_LANGUAGE` | 摘要的语言（默认：中文、英文、日文、韩文、西班牙文、法文、德文或其他语言） |

**目标渠道的发送格式：**

| 渠道 | 发送格式 | 示例 |
|------|---------|------|
| Discord | `channel:<id>` | `channel:1234567890` |
| WhatsApp | E.164 电话号码或 `group:<id>` | `+1234567890` |
| Telegram | `@username` 或聊天 ID | `@mychannel` |
| Slack | `#channel-name` | `#ai-digest` |
| Signal | E.164 电话号码 | `+1234567890` |

> 仅支持 Discord 的卡片预览功能；在其他渠道中该功能会被自动禁用。

### 2. 手动运行

```bash
python3 scripts/monitor.py
```

### 3. 使用 OpenClaw 的 cron 任务定时执行

```bash
# Daily at 3:30 PM Eastern
openclaw cron add "AI Twitter Digest" "30 15 * * *" \
  "python3 /path/to/ai-twitter-digest/scripts/monitor.py" \
  --timezone "America/New_York"
```

## 自定义账户设置

请编辑 `scripts/monitor.py` 文件中的 `ACCOUNTS` 列表。有关默认账户列表及建议的添加内容，请参阅 `references/accounts.md`。

## 输出格式

**消息 1（摘要）：**
```
📊 **AI 每日简报** — 2026年02月26日

- Karpathy 发布了神经网络教程 | [原文链接](...)

- Sam Altman 表示 GPT-5 今年发布 | [原文链接](...)
```

**消息 2（卡片预览）：**
```
🔗 **今日精选链接**

https://x.com/karpathy/status/...
https://x.com/sama/status/...
```

## 工作原理：

1. 每个账户最多获取 20 条符合关键词条件的推文（若未找到符合条件的推文，则使用所有推文）。
2. 通过 `STATE_FILE` 文件来避免重复推送相同的推文（存储数量上限为 `MAX_STORED_IDS`）。
3. 使用可用的 LLM 服务对推文内容进行翻译。
4. 在 Discord 上发布两条消息：一条是文本摘要，另一条是推文的卡片预览链接。
5. 更新 `STATE_FILE` 文件以记录推送状态。