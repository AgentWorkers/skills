# Bland AI — 语音通话技能

通过 Bland AI API 进行并管理由 AI 驱动的电话通话。

## 快速入门

```bash
# Make a call
bland call +14155551234 --task "Call and ask about their hours"

# Check call status
bland call-status <call_id>

# Get transcript after call
bland transcript <call_id>
```

## 命令

| 命令 | 描述 |
|---------|-------------|
| `bland call <电话号码> [选项]` | 发起一个外拨 AI 电话 |
| `bland call-status <通话ID>` | 获取通话的状态/详细信息 |
| `bland calls [--limit N]` | 列出最近的通话记录 |
| `bland stop <通话ID>` | 中止正在进行的通话 |
| `bland stop-all` | 中止所有正在进行的通话 |
| `bland recording <通话ID>` | 获取通话的录音 URL |
| `bland transcript <通话ID>` | 获取格式化的通话记录文本 |
| `bland voices` | 列出可用的语音选项 |
| `bland numbers` | 列出拥有的来电号码 |
| `bland buy-number [--area-code 415]` | 购买一个来电号码 |
| `bland setup-inbound <电话号码> --task "提示"` | 配置来电客服 |
| `bland balance` | 查看账户余额 |
| `bland analyze <通话ID> --goal "问题"` | 对通话进行 AI 分析 |

## 通话选项

```
--task "prompt"           AI agent instructions (required for useful calls)
--voice "josh"            Voice to use (default: josh)
--first-sentence "Hi!"    First thing the AI says
--from "+1234567890"      Caller ID (must own the number)
--wait-for-greeting       Wait for the other party to speak first
--wait                    Poll until call completes, then show transcript
--model "base"            Model to use (default: base)
```

## 示例

```bash
# Restaurant reservation
bland call +14155551234 --task "Make a reservation for 2 at 7pm tonight under Joshua"

# Call and wait for result
bland call +14155551234 --task "Ask about store hours" --wait

# Screen inbound calls
bland setup-inbound +14155551234 --task "You are a call screener. Ask who is calling and why."

# Analyze a completed call
bland analyze abc123 --goal "Did they confirm the appointment?"
```

## 环境配置

- **API 密钥：** `BLAND_API_KEY`，位于 `/root/clawd/.env` 文件中 |
- **API 基址：** `https://api.bland.ai/v1` |
- **脚本：** `/root/clawd/skills/bland/scripts/bland.sh`

## 注意事项

- 电话号码必须采用 E.164 格式，例如：`+14155551234` |
- 通话需要付费——在使用前请先查看账户余额（`bland balance`） |
- 可使用 `--wait` 选项等待通话结束后再自动显示通话记录 |
- 录音 URL 是临时生成的——如需保存请自行下载