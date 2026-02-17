---
name: openclaw-voice-gpt-realtime
description: 通过 OpenAI 的实时 API，使用您的 OpenClaw 代理进行真实的电话通话。延迟约为 200-300 毫秒，语音质量自然，支持 IVR 导航功能以及语音邮件检测。
version: 0.1.2
homepage: https://github.com/connorcallison/openclaw-voice-gpt-realtime
metadata:
  openclaw:
    emoji: "\U0001F4DE"
    requires:
      bins:
        - bun
    install:
      - kind: node
        package: openclaw-voice-gpt-realtime
---
# 语音通话（OpenAI 实时）

通过您的 OpenClaw 代理进行真实的电话通话。您可以让它预订餐厅、查询店铺营业时间、安排预约等——它会拨打电话、处理通话内容，并以结构化的方式返回结果。

该功能使用 OpenAI 的实时语音转文本（Realtime API）技术，实现单模型语音转语音（speech-to-speech）功能，响应延迟约为 200-300 毫秒。无需单独的语音转文本（STT）或文本转语音（TTS）服务——所有功能都由同一个模型完成。

## 设置

使用此功能需要一个 Twilio 账户以及具有实时 API 访问权限的 OpenAI API 密钥。

1. 在插件配置中设置您的凭据（通过 OpenClaw 设置或 `openclaw.json` 文件）：
   - `twilio.accountSid`：您的 Twilio 账户 SID
   - `twilio.authToken`：您的 Twilio 认证令牌
   - `fromNumber`：支持语音通话的 Twilio 电话号码（E.164 格式，例如 `+17075551234`
   - `openai.apiKey`：您的 OpenAI API 密钥
   - `publicUrl`：指向插件服务器的公共 HTTPS 地址（默认端口为 3335）。不能使用 `localhost`、`private` 或 `internal` 等地址。

2. 设置一个通道（如 Cloudflare Tunnel、ngrok、Tailscale Funnel 等），以便 Twilio 能够连接到 Webhook 服务器。

3. 验证设置：
```bash
openclaw voicecall-rt status
```

## 使用方法

只需告诉代理要拨打的电话号码以及通话目的：

> “拨打 +14155551234，为周五晚上 7 点预订一个四人桌位”
> “拨打 +14155559876，预订周六早上的理发服务”
> “拨打 +14155550000，询问是否有 iPhone 16 Pro 在售”

代理会为语音 AI 生成相应的提示信息，然后拨打电话。语音 AI 会自动处理整个通话过程，包括操作电话菜单（DTMF 音频信号）、检测语音邮件等，并报告通话结果。该插件会对提示信息进行安全处理，防止任何欺诈行为。

### 命令行接口（CLI）

```bash
openclaw voicecall-rt call -n +14155551234 -t "Check store hours"
openclaw voicecall-rt status
openclaw voicecall-rt active
```

### 收到来电

您可以通过启用 `inbound.enabled` 选项并设置相应的策略（`open` 或 `allowlist`）来接收来电。默认情况下该功能是禁用的。

## 费用

每次通话费用约为 0.31 美元（其中 0.06 美元用于 OpenAI 语音转文本服务，0.24 美元用于 OpenAI 语音合成服务，0.014 美元用于 Twilio 服务）。一次典型的 5 分钟通话费用约为 1.55 美元。

## 注意事项：

- 语音 AI 会在对方说话之前先等待（“先听后说”），避免通话开始时的尴尬沉默。
- 服务器默认绑定到 `127.0.0.1` 地址。只有通过设置的通道才能访问该服务器。
- 默认情况下最多支持 5 个并发通话（可通过 `calls.maxConcurrent` 配置进行调整）。
- 调试模式（`debug: true`）可启用通话录音、详细日志记录和延迟指标；录音文件/文字记录可能包含敏感信息。