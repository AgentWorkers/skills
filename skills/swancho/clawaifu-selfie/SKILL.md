---
name: clawaifu - OpenClaw Waifu
title: clawaifu - OpenClaw Waifu
description: 你的AI虚拟女友伴侣，会发送动漫风格的自拍照。
allowed-tools: Bash(grok-selfie.sh:*) Read
homepage: https://github.com/swancho/clawaifu
metadata: {"openclaw":{"requires":{"env":["FAL_KEY","BOT_TOKEN","TELEGRAM_CHAT_ID"]},"primaryEnv":"FAL_KEY"}}
---

# clawaifu - OpenClaw 的虚拟形象生成工具

**GitHub:** https://github.com/swancho/clawaifu

该工具使用 xAI 的 Grok Imagine 模型来编辑指定的参考图片，并将编辑后的图片发送到 Telegram。

## 参考图片

该功能使用一张固定的参考图片作为生成图片的基准：

```
https://i.redd.it/g4uf70te81uf1.jpeg
```

## 使用场景

- 当用户请求发送图片（如 “发送一张照片” 或 “给我发张自拍”）时。
- 当用户询问用户的当前状态或位置时。
- 当用户提供具体场景描述时（例如 “请发送一张穿着……的照片”）。

## 必需的环境变量

所有敏感信息（如 API 密钥）都必须通过环境变量传递。**切勿将敏感信息硬编码到代码中！**

```bash
FAL_KEY=your_fal_api_key          # Required - Get from https://fal.ai/dashboard/keys
BOT_TOKEN=your_telegram_bot_token  # Required - Get from @BotFather
TELEGRAM_CHAT_ID=your_chat_id      # Required - Your Telegram chat ID
```

## 使用方法

```bash
./grok-selfie.sh "<context>" [mirror|direct] "<caption>"
```

### 参数说明

1. `<context>`（必填）：场景或情境的描述。
2. `[mode]`（可选）：`mirror`（默认值）或 `direct`。
3. `<caption>`（可选）：随图片一起发送的文字信息。

### 模式说明

| 模式        | 适用场景                | 关键词                          |
|------------|------------------|--------------------------------------|
| `mirror`     | 服装展示、全身照片           | 穿着、服装、时尚、连衣裙                |
| `direct`     | 地点照片、特写照片           | 咖啡馆、海滩、餐厅、肖像                   |

### 使用示例

```bash
# Mirror selfie (outfit focus)
./grok-selfie.sh "wearing a designer dress" mirror "Just got this new dress!"

# Direct selfie (location focus)
./grok-selfie.sh "a fancy rooftop restaurant" direct "Date night vibes"

# Default mode (mirror)
./grok-selfie.sh "casual outfit at home"
```

## 角色风格

该脚本生成的图片基于《电锯人》中的 Reze 角色，具有以下特点：
- 动画风格：2D 动画、赛璐璐阴影效果。
- 角色特征：绿色眼睛、细线嘴型、微微微笑。
- 常见配饰：始终佩戴黑色项圈。
- 服装选择：根据场景自动调整。

## 安全注意事项

- 所有敏感信息均通过环境变量传递。
- 脚本使用 `jq` 来安全地处理 JSON 数据（防止注入攻击）。
- 脚本使用 `curl -F` 来安全地发送表单数据。
- 请勿将敏感信息提交到版本控制系统中。

## 依赖库

- `curl`：用于发送 HTTP 请求。
- `jq`：用于处理 JSON 数据。
- 必需的环境变量：`FAL_KEY`、`BOT_TOKEN`、`TELEGRAM_chat_ID`。

## API 参考

- **Grok Imagine 编辑接口**：[fal.ai](https://fal.ai)

### Telegram 聊天机器人 API

```
POST https://api.telegram.org/bot$BOT_TOKEN/sendPhoto
Form data: chat_id, photo (URL), caption
```