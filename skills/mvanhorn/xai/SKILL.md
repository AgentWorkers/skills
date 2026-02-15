---
name: xai
description: 通过 xAI API 与 Grok 模型进行交互。支持 Grok-3、Grok-3-mini、vision 等多种模型。
homepage: https://docs.x.ai
user-invocable: true
disable-model-invocation: true
triggers:
  - grok
  - xai
  - ask grok
metadata:
  clawdbot:
    emoji: "🤖"
    primaryEnv: XAI_API_KEY
    requires:
      bins: [node]
      env: [XAI_API_KEY]
---

# xAI / Grok

您可以与 xAI 的 Grok 模型进行交流，这些模型支持文本处理和图像分析功能。

## 设置

```bash
export XAI_API_KEY="xai-YOUR-KEY"
```

请在以下链接获取您的 API 密钥：https://console.x.ai

## 命令

### 与 Grok 进行对话
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

该功能通过 `x_search` 工具使用 xAI 的响应 API 来搜索 X 和 Twitter 上的实时帖子，并提供相关引用。

### 可用模型列表
```bash
node {baseDir}/scripts/models.js
```

- `grok-3`：功能最强大，适合处理复杂任务
- `grok-3-mini`：快速且高效
- `grok-3-fast`：针对速度进行了优化
- `grok-2-vision-1212`：用于图像理解的视觉模型

## 使用示例

**用户：**“询问 Grok 对 AI 安全性的看法”
**操作：**运行 `chat.js` 并输入相应提示。

**用户：**“使用 Grok 分析这张图片”（需附上图片文件）
**操作：**运行 `chat.js` 并使用 `--image` 标志。

**用户：**“有哪些可用的 Grok 模型？”
**操作：**运行 `models.js`。

## API 参考文档

xAI API 文档：https://docs.x.ai/api

## 环境变量

- `XAI_API_KEY`：您的 xAI API 密钥（必需）
- `XAI_MODEL`：默认使用的模型（可选，默认为 `grok-3`）

## 安全性与权限

**该功能的用途：**
- 将聊天请求发送到 xAI 的 API（地址：`api.x.ai`）
- 在图像分析模式下，会将图片发送给 xAI 进行处理
- `scripts/models.js` 文件用于列出所有可用模型（仅限读取）

**该功能不支持的操作：**
- 不会读取任意本地文件；`--image` 参数仅接受具有图像扩展名（`.jpg`、`.jpeg`、`.png`、`.gif`、`.webp`）的文件
- 不会读取配置文件或访问指定的图片路径之外的文件系统
- 不会存储对话历史记录或日志
- 不会将任何凭据发送到除 `api.x.ai` 之外的任何端点
- 该功能无法被代理程序自动调用（`disable-model-invocation: true`）

**包含的脚本：**
- `scripts/chat.js`（用于聊天）
- `scripts/models.js`（用于列出可用模型）
- `scripts/search-x.js`（用于 X 搜索）

首次使用前，请先查看这些脚本以确保其正常运行。