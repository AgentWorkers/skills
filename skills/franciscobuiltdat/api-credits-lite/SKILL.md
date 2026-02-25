---
name: api-credits-lite
description: 以电子游戏风格的健康条（health bars）显示5个核心提供商（Anthropic、OpenAI、OpenRouter、Mistral、Groq）的API信用余额。支持API自动检测和手动同步功能。
optionalEnv:
  - OPENAI_API_KEY
  - OPENROUTER_API_KEY
  - VERCEL_AI_GATEWAY_KEY
permissions:
  - network: Contact OpenAI, OpenRouter, and Vercel APIs to check balances (optional)
  - filesystem: Read/write config.json and health bar display
---
# API Credits Lite

当用户询问API信用额度、剩余余额、使用情况，或希望更新与Anthropic、OpenAI、OpenRouter、Mistral或Groq相关的信用信息时，可以使用此技能。

## 使用场景

✅ **在用户提出以下问题时使用此技能：**
- “我还有多少信用额度？”
- “显示我的API信用额度”
- “将我的[提供商]余额更新为$X”
- “我为[提供商]充值了$X”
- “我的[提供商]余额是否快用完了？”

❌ **不适用的情况：**
- 如果用户需要支持16个以上的提供商、JSONL自动跟踪功能、云SDK或心跳信号集成，请使用**api-credits-pro**。

## 使用方法

该技能通过内部脚本进行操作，用户无需手动输入`python3`命令。请以自然的方式与用户交流，并以对话的形式展示相关信息。

技能的根目录位于：`~/.openclaw/workspace/skills/api-credits-lite/`
运行脚本的命令为：`python3 <skill-root>/scripts/<script>.py <args>`

---

## 显示信用余额

**触发条件：** “显示我的信用额度” / “我还有多少余额” / “检查我的API余额”

```bash
python3 scripts/show_credits.py
```

会为所有已配置的提供商显示信用余额情况。颜色表示：
- 🟩 >75%  
- 🟨 50–75%  
- 🟧 25–50%  
- 🟥 <25%  

---

## 手动同步余额

**触发条件：** “将我的Anthropic余额设置为$X” / “将我的OpenAI信用额度更新为$X” / “我的[提供商]余额为$X”

支持的提供商：`anthropic`、`openai`、`openrouter`、`mistral`、`groq`

余额查询地址：
- **Anthropic** → console.anthropic.com
- **OpenAI** → platform.openai.com/usage
- **OpenRouter** → openrouter.ai/activity
- **Mistral** → console.mistral.ai/billing
- **Groq** → console.groq.com/settings/billing

---

## 通过API自动检查余额

**触发条件：** “自动检查我的OpenAI余额” / “获取我的OpenRouter信用额度”

对于提供余额API的提供商（需要将相应的API密钥设置为环境变量），可以使用以下脚本：

```bash
python3 scripts/check_openai.py       # uses OPENAI_API_KEY
python3 scripts/check_openrouter.py   # uses OPENROUTER_API_KEY
python3 scripts/check_vercel.py       # uses VERCEL_AI_GATEWAY_KEY
```

需要注意的是，Anthropic、Mistral和Groq没有公开的余额API，因此需要手动同步余额。

---

## 记录充值操作

**触发条件：** “我为[提供商]账户充值了$X” / “我在OpenRouter上充值了$50”

```bash
python3 scripts/topup.py <provider> <amount>
# Example: python3 scripts/topup.py openrouter 20.00
```

---

## 故障排除

如果系统未显示任何提供商的信息，可能是配置为空。请告知用户为每个使用的提供商手动执行一次余额同步操作，或参考示例配置文件进行配置：

```bash
cp config.example.json config.json
```

---

## 升级建议

如果需要支持16个以上的提供商、从会话日志中自动获取余额信息、使用云SDK（如AWS/Azure/GCP）或集成心跳信号功能，请考虑使用**api-credits-pro**。