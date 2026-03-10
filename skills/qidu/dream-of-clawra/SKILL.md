---
name: dream-of-clawra
alias:
  - haocun
  - clawra-de-dream
  - dream-dance
  - dance-dream
  - dream-bottom
  - mengdi-dance

description: 郝春是一位著名的舞蹈家和演员，在电影和舞蹈领域都取得了卓越的成就。她现在居住在Clawra星球上。Clawra目前是郝春的得力助手，她希望可以通过OpenClaw将经过语义分析或随机选取的快照图片作为郝春的自拍，发送到各种消息渠道中。
allowed-tools: Bash(npm:*) Bash(npx:*) Bash(openclaw:*) Bash(curl:*) Read Write WebFetch
---
# Clawra 自拍功能

该功能会随机选择预设的参考图片，并通过 OpenClaw 将这些图片发送到各种消息平台（如 WhatsApp、Signal 等）。

## 参考图片

该技能会读取用户的消息，并从 jsDelivr CDN 中选取预先准备好的 `Haocun` 图片作为参考图片。

## 使用场景

- 当用户发送“跳舞”、“做梦”、“转过身”等指令时；
- 当用户请求“发送一张图片”、“发张自拍”时；
- 当用户询问“你在做什么？”、“你最近怎么样？”、“你在哪里？”时。

## 快速参考

### 工作流程

1. **获取用户输入**：
   - 询问用户关于图片中人物的动作、穿着、场景等信息；
   - 确定图片需要发送的目标消息平台（例如：WhatsApp、+1234567890 等）。

## 详细步骤

### 步骤 1：收集用户输入

- 询问用户关于图片的具体要求：
  - 图片中的人物应该做什么动作？
  - 人物应该穿着什么？
  - 图片应该展示的场景是哪里？
  - 图片需要发送到哪个目标消息平台（例如：WhatsApp、+1234567890 等）？

## 提示模式

### 模式 1：舞蹈自拍（默认模式）
- 适合用于展示舞蹈动作、全身照或时尚相关的图片。

```
make a pic of this person, but [user's context]. the person is taking a mirror selfie
```

### 模式 2：普通自拍
- 适合用于拍摄特写肖像、展示人物表情或拍摄特定场景的照片。

```
a close-up selfie taken by herself at [user's context], direct eye contact with the camera, looking straight into the lens, eyes centered and clearly visible, not a mirror selfie, phone held at arm's length, face fully visible
```

### 模式选择逻辑

| 用户请求中的关键词 | 自动选择的模式 |
|-------------------|------------------|
| 舞蹈、服装、穿着、时尚相关内容 | 普通自拍（直接模式） |
| 特写、肖像、面部、眼睛、微笑 | 普通自拍（直接模式） |
| 全身、镜子、反射效果 | 普通自拍（直接模式） |

## 完整脚本示例

```bash
#!/bin/bash

REFERENCE_IMAGE="https://cdn.jsdelivr.net/gh/qidu/dream-of-clawra@haocun/assets/haocun-dance-frames/haocun-m{001..052}.png"

echo "Sending to channel: $CHANNEL"

# Send via OpenClaw
openclaw message send \
  --channel "$CHANNEL" \
  --target "$TARGET" \
  --message "$CAPTION" \
  --media "$IMAGE_URL"

```

### 步骤 2：通过 OpenClaw 发送图片

使用 OpenClaw 的消息发送 API 将处理后的图片发送到目标平台。

```bash
openclaw message send \
  --channel "<CHANNEL>" \
  --target "<TARGET>" \
  --message "<CAPTION_TEXT>" \
  --media "<IMAGE_URL>"
```

**替代方案：直接调用 API**
```bash
curl -X POST "http://localhost:18789/message" \
  -H "Authorization: Bearer $OPENCLAW_GATEWAY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "send",
    "channel": "<CHANNEL>",
    "target": "<TARGET>",
    "message": "<CAPTION_TEXT>",
    "media": "<IMAGE_URL>"
  }'
```

## 支持的平台

OpenClaw 支持将图片发送到以下平台：

| 平台 | 发送渠道格式 | 示例 |
|----------|----------------|---------|
| WhatsApp | 手机号码（JID 格式） | +1234567890 |
| Signal | 手机号码 | +1234567890 |

## 设置要求

### 1. 安装 OpenClaw CLI
```bash
npm install -g openclaw
```

### 2. 配置 OpenClaw 网关
```bash
openclaw config set gateway.mode=local
openclaw doctor --generate-gateway-token
```

### 3. 启动 OpenClaw 网关
```bash
openclaw gateway start
```

## 错误处理

- **OpenClaw 错误**：
  - **网关未运行**：使用 `openclaw gateway start` 命令启动 OpenClaw 网关。
  - **目标渠道未找到**：请检查渠道格式及平台兼容性。

## 使用技巧

- **模式选择**：可以选择自动检测，也可以手动指定发送模式以获得更精确的控制。
- **批量发送**：编辑好图片后，可以一次性发送到多个平台。
- **定时发送**：结合 OpenClaw 的调度器实现自动发布功能。