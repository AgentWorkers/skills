---
name: outbound-call
description: 通过 ElevenLabs 语音代理和 Twilio 发起出站电话呼叫
metadata:
  clawdbot:
    requires:
      env:
        - ELEVENLABS_API_KEY
        - ELEVENLABS_AGENT_ID
        - ELEVENLABS_PHONE_NUMBER_ID
    primaryEnv: ELEVENLABS_API_KEY
---
# 出站呼叫

> **源代码及设置指南：** [github.com/humanjesse/hostinger-openclaw-guides](https://github.com/humanjesse/hostinger-openclaw-guides)

使用 ElevenLabs 语音代理通过 Twilio 发起出站电话呼叫。该语音代理在通话过程中会依赖 OpenClaw 来处理通话逻辑——这与处理入站呼叫的方式相同。

## 使用场景

当用户要求您执行以下操作时：
- 给某人打电话
- 拨打电话号码
- 铃响某人的电话
- 向某个号码发起呼叫

## 使用方法

使用 E.164 格式的电话号码运行呼叫脚本：

```bash
python3 skills/outbound-call/call.py +1XXXXXXXXXX
```

（可选）自定义开场白（即代理在接听方接听电话时说的话）：

```bash
python3 skills/outbound-call/call.py +1XXXXXXXXXX "Hi John, I'm calling about your appointment tomorrow."
```

（可选）传递呼叫上下文信息（作为动态变量给代理）：

```bash
python3 skills/outbound-call/call.py +1XXXXXXXXXX "Hi, this is a quick follow-up call." "Customer requested callback about billing issue #4521"
```

## 电话号码格式

- 美国电话号码：以 +1 开头，后跟 10 位数字，例如：+15551234567
- 如果用户提供的号码格式为 555-123-4567 或 (555) 123-4567，请将其转换为 +15551234567 的格式
- 在拨打电话前务必与用户确认电话号码的格式是否正确

## 规则

- 在拨打电话前务必与用户确认电话号码
- 未经用户明确同意，严禁擅自发起呼叫
- 呼叫成功后需将结果告知用户（提供会话 ID）；失败时需报告错误详情
- 如果呼叫失败，需向用户解释原因并建议解决方案