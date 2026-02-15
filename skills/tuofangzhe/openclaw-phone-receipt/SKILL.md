---
name: openclaw-phone-receipt
description: 通过 ElevenLabs+Twilio 触发和管理 OpenClaw 的出站电话记录功能，以实现任务完成/失败的通知。适用于以下场景：用户完成任务后或任务失败后请求拨打电话、请求启用/禁用固定命令（如 “phone-receipt=on/off”）、请求测试通话质量，或请求在会话之间保持电话记录行为的连续性。
---

# OpenClaw 电话回拨通知功能

使用此功能来管理电话回拨通知。

## 可使用的命令：

- `phone-receipt=on` → 启用电话回拨通知功能
- `phone-receipt=off` → 禁用电话回拨通知功能

状态文件：
- `memory/phone-receipt-state.json`

## 默认行为：

1. 如果用户要求在任务完成或失败时接收回拨通知，则将 `enabled` 设置为 `true`。
2. 默认设置如下：
   - `policy.onComplete=false`
   - `policy.onFailure=true`
   - `policy.onUrgent=true`
3. 将状态信息保存到 `memory/phone-receipt-state.json` 文件中。
4. 如需立即进行测试呼叫，请运行 `scripts/trigger_call.sh`。

## 呼叫触发策略（必须遵循）：

- 仅在以下情况下触发电话呼叫：
  - 1) 任务失败；
  - 2) 用户明确将任务标记为紧急（例如：“紧急/高优先级”）。
- 对于其他非紧急且成功的任务：
  - 仅发送 Telegram 文本摘要（不进行电话呼叫）。

当策略未要求进行电话通知时，使用 Telegram 文本消息作为默认的通知方式。

## 工具/脚本：

- 切换电话回拨通知状态：
  - `python3 skills/openclaw-phone-receipt/scripts/set_phonereceipt_state.py on`
  - `python3 skills/openclaw-phone-receipt/scripts/set_phonereceipt_state.py off`
- 立即触发呼叫：
  - `bash skills/openclaw-phone-receipt/scripts/trigger_call.sh`

## 呼叫所需的前提条件：

需要 `.env.elevenlabs-call` 文件，其中包含以下参数：
- `ELEVENLABS_AGENT_ID`
- `ELEVENLABS_OUTBOUND_PHONE_ID`
- `TO_NUMBER`

`ELEVENLABS_API_KEY` 可以从 shell 环境变量或 `.env.elevenlabs-call` 文件中获取。

有关完整设置（Twilio 购买/验证、ElevenLabs 库的导入、权限设置以及故障排除的详细信息，请参阅：
- `references/setup.md`

有关 ClawHub 上传的详细要求（版本、变更日志、文件大小等），请参阅：
- `references/publish-clawhub.md`

## 故障处理：

如果呼叫失败，需返回详细的根本原因及后续操作建议：
- 目标号码未验证（可能是 Twilio 试用账户）；
- 缺少 ConvAI 相关权限（`convai_read`）；
- 缺少代理/电话号码信息。