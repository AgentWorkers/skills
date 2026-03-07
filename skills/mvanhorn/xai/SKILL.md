---
name: xai
version: "1.1.0"
description: 通过 xAI API 与 Grok 模型进行交互。支持 Grok-4、Grok-4.20、Grok-3、Grok-3-mini、视觉识别功能以及实时 X 搜索。
author: mvanhorn
license: MIT
repository: https://github.com/mvanhorn/clawdbot-skill-xai
homepage: https://docs.x.ai
triggers:
  - grok
  - xai
  - ask grok
metadata:
  openclaw:
    emoji: "🤖"
    requires:
      env:
        - XAI_API_KEY
    primaryEnv: XAI_API_KEY
    tags:
      - xai
      - grok
      - llm
      - vision
      - x-search
---
# xAI / Grok

您可以与 xAI 的 Grok 模型进行交流，这些模型支持文本处理和图像分析功能。

## 设置

请在技能配置文件中设置您的 API 密钥：

```bash
# Via openclaw config
openclaw config set skills.entries.xai.apiKey "xai-YOUR-KEY"

# Or environment variable
export XAI_API_KEY="xai-YOUR-KEY"
```

您可以在以下链接获取 API 密钥：https://console.x.ai

## 命令

### 与 Grok 进行交流
```bash
node {baseDir}/scripts/chat.js "What is the meaning of life?"
```

### 使用特定模型
```bash
node {baseDir}/scripts/chat.js --model grok-3-mini "Quick question: 2+2?"
```

### 图像分析
```bash
node {baseDir}/scripts/chat.js --image /path/to/image.jpg "What's in this image?"
```

### 🔍 实时搜索 X/Twitter
```bash
node {baseDir}/scripts/search-x.js "Remotion video framework"
node {baseDir}/scripts/search-x.js --days 7 "Claude AI tips"
node {baseDir}/scripts/search-x.js --handles @remotion_dev "updates"
```

该功能通过 `x_search` 工具使用 xAI 的响应 API 来搜索 X（Twitter）上的帖子，并提供相关引用。

### 可用模型列表
```bash
node {baseDir}/scripts/models.js
```

- `grok-3`：功能最强大，适合处理复杂任务
- `grok-3-mini`：快速且高效
- `grok-3-fast`：专为提高速度而优化
- `grok-2-vision-1212`：用于图像理解的视觉模型

## 使用示例

**用户：**“询问 Grok 对人工智能安全的看法”
**操作：**运行 `chat.js` 并输入相应的提示。

**用户：**“使用 Grok 分析这张图片”（需附带图片文件）
**操作：**运行 `chat.js` 并使用 `--image` 标志。

**用户：**“有哪些可用的 Grok 模型？”
**操作：**运行 `models.js`。

## API 参考文档

xAI API 文档：https://docs.x.ai/api

## 环境变量

- `XAI_API_KEY`：您的 xAI API 密钥（必填）
- `XAI_MODEL`：默认使用的模型（可选，默认为 `grok-3`）