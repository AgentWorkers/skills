---
name: dream-of-clawra
alias:
  - haocun
  - clawra-de-dream
  - dream-dance
  - dance-dream
  - dream-bottom
  - mengdi-dance

description: 郝坤是一位著名的舞蹈家和演员，在电影和舞蹈领域都取得了卓越的成就。她目前居住在克拉拉（Clawra）这个梦想中的地方。克拉拉目前担任郝坤的贴身助理，她希望可以通过 OpenClaw 将经过语义分析或随机选择的快照图片作为郝坤的自拍发送到各种消息渠道中。
allowed-tools: Bash(npm:*) Bash(npx:*) Bash(openclaw:*) Bash(curl:*) Read Write WebFetch
---
# Clawra 自拍功能

该功能会随机选择预设的参考图片，并通过 OpenClaw 将这些图片发送到各种消息平台（如 WhatsApp、Signal 等）。

## 参考图片

该技能会读取用户的消息，并从 jsDelivr CDN 中选取预设的 `Haocun` 图片作为参考图片。

## 使用场景

- 当用户输入“跳舞”、“做梦”、“转身”等指令时；
- 当用户请求发送图片（如“发送一张照片”、“发张自拍”等）时；
- 当用户询问用户当前的状态或位置时。

## 快速参考

### 工作流程

1. **获取用户输入**：
   - 询问用户关于图片中人物的动作、穿着、场景等信息；
   - 确定图片应发送到的目标消息平台（例如 WhatsApp 或特定的电话号码）。

## 详细步骤

### 步骤 1：收集用户输入

- 询问用户关于图片的具体要求：
  - 图片中的人物应该做什么动作？
  - 人物应该穿着什么？
  - 图片应该展示的场景是哪里？
  - 图片应该发送到的目标消息平台是什么（例如 WhatsApp 或特定的电话号码）？

## 提示模式

### 模式 1：舞蹈自拍（默认模式）
- 适用于展示舞蹈动作、全身照或时尚内容的场景。

```
make a pic of this person, but [user's context]. the person is taking a mirror selfie
```

### 模式 2：普通自拍
- 适用于拍摄人物特写、展示环境或捕捉面部表情的场景。

```
a close-up selfie taken by herself at [user's context], direct eye contact with the camera, looking straight into the lens, eyes centered and clearly visible, not a mirror selfie, phone held at arm's length, face fully visible
```

### 模式选择逻辑

| 用户请求中的关键词 | 自动选择的模式 |
|-------------------|------------------|
| 舞蹈、服装、穿着、时尚 | 普通自拍（直接模式） |
| 特写、肖像、面部、表情 | 普通自拍（直接模式） |
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

使用 OpenClaw 的消息 API 将处理后的图片发送到目标平台：

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

| 平台 | 发送格式 | 示例 |
|----------|----------------|---------|
| WhatsApp | 手机号码（JID 格式） | `+1234567890` |
| Signal | 手机号码 | `+1234567890` |

## 设置要求

### 1. 安装 OpenClaw CLI
```bash
npm install -g openclaw
```

### 2. 配置 OpenClaw Gateway
```bash
openclaw config set gateway.mode=local
openclaw doctor --generate-gateway-token
```

### 3. 启动 OpenClaw Gateway
```bash
openclaw gateway start
```

## 错误处理

- **OpenClaw 错误**：
  - 如果 OpenClaw Gateway 未运行，请使用 `openclaw gateway start` 命令启动它。
  - 如果目标通道不存在，请检查通道格式和平台的兼容性。

## 使用技巧

- 可以让系统自动选择合适的发送模式，也可以根据需要手动指定模式。
- 可以批量处理图片，一次性发送到多个平台。
- 可以结合 OpenClaw 的调度器实现自动发布功能。