---
name: gradient-inference
description: 这是一个关于 DigitalOcean Gradient AI Serverless Inference 的社区技能（非官方）。你可以使用该技能来查找可用的模型和价格信息，运行聊天完成功能（chat completions），或者通过响应 API（Responses API）实现提示缓存（prompt caching），同时还能生成图像。该技能兼容 OpenAI。
files: ["scripts/*"]
homepage: https://github.com/Rogue-Iteration/TheBigClaw
metadata:
  clawdbot:
    emoji: "🧠"
    primaryEnv: GRADIENT_API_KEY
    requires:
      env:
        - GRADIENT_API_KEY
      bins:
        - python3
  author: Rogue Iteration
  version: "0.1.0"
  tags: ["gradient", "inference", "llm", "do", "digitalocean"]
---
# 🦞 **Gradient AI — 无服务器推理服务**

> ⚠️ **这是一个非官方的社区技能工具**，并非由 DigitalOcean 提供维护。使用该工具需自行承担风险。

> “既然海洋中已有资源，为何还要自己去管理 GPU 呢？”——这是一句古老的龙虾谚语。

利用 DigitalOcean 的 [Gradient 无服务器推理服务](https://docs.digitalocean.com/products/gradient-ai-platform/how-to/use-serverless-inference/)，无需管理基础设施即可调用大型语言模型。该 API 与 OpenAI 兼容，因此标准 SDK 和开发模式均可直接使用——只需指向 `https://inference.do-ai.run/v1` 即可开始使用。

## **身份验证**

所有请求都必须在 `Authorization: Bearer` 头部包含一个 **模型访问密钥**。

**获取模型访问密钥的方法：** [DigitalOcean 控制台](https://cloud.digitalocean.com) → Gradient AI → 模型访问密钥 → 创建密钥。

📖 *[完整身份验证文档](https://docs.digitalocean.com/products/gradient-ai-platform/how-to/use-serverless-inference/#create-a-model-access-key)*

---

## **工具**

### 🔍 **可用模型列表**

在使用模型之前，先浏览一下可用的大型语言模型（LLMs）。

**直接调用 API：**
**（代码示例未提供）**

📖 *[模型参考文档](https://docs.digitalocean.com/products/gradient-ai-platform/details/models/)*

---

### 💬 **聊天式问答功能**

发送结构化消息（系统/用户/助手角色），即可获得响应。该功能与 OpenAI 兼容，因此你可能已经熟悉其工作原理。

**直接调用 API：**
**（代码示例未提供）**

📖 *[聊天式问答功能文档](https://docs.digitalocean.com/products/gradient-ai-platform/how-to/use-serverless-inference/#chat-completions)*

---

### ⚡ **响应 API（推荐使用）**

对于新的集成项目，建议使用 DigitalOcean 推荐的 [响应 API](https://docs.digitalocean.com/products/gradient-ai-platform/how-to/use-serverless-inference/#responses-api)。该 API 的请求格式更简单，并支持 **提示缓存** 功能——避免重复计算相同的数据。

**直接调用 API：**
**（代码示例未提供）**

**使用场景对比：**
| 功能          | 聊天式问答 | 响应 API       |
|---------------|---------|--------------|
| 请求格式        | 带有角色标签的消息数组 | 单个 `input` 字符串   |
| 提示缓存        | 不支持     | 支持（通过 `store: true`）   |
| 多步骤操作      | 手动操作   | 内置支持       |
| 最适合的场景     | 结构化对话   | 简单查询       |

📖 *[响应 API 文档](https://docs.digitalocean.com/products/gradient-ai-platform/how-to/use-serverless-inference/#responses-api)*

---

### 🖼️ **图像生成**

将文本提示转换为图像。有时候，一张图表比文字更直观。

**直接调用 API：**
**（代码示例未提供）**

📖 *[图像生成文档](https://docs.digitalocean.com/products/gradient-ai-platform/how-to/use-serverless-inference/#image-generation)*

---

## **模型选择指南**

并非所有模型都适合所有场景。请谨慎选择：

| 模型            | 最适合的场景        | 处理速度      | 图像质量      | 对上下文的要求   |
|-----------------|------------------|-------------|-------------|-------------------|
| `openai-gpt-oss-120b`     | 复杂推理、分析、写作       | 中等          | ★★★★★       | 128K             |
| `llama3.3-70b-instruct`    | 通用任务、指令执行       | 快速          | ★★★★         | 128K             |
| `deepseek-r1-distill-llama-70b`   | 数学计算、代码生成、逐步推理    | 较慢          | ★★★★★       | 128K             |
| `qwen3-32b`         | 快速任务处理         | 最快          | ★★★          | 32K             |

> **专业提示：** 根据需求选择模型。可以先使用性能较快的模型（如 `qwen3-32b`）进行初步处理或任务分类，只有在需要更高性能时再升级到更强大的模型（如 `openai-gpt-oss-120b`）。对于重复使用的场景，启用提示缓存功能可提高效率。

请务必运行 `python3 gradient_models.py` 命令查看当前可用的模型列表——模型列表会定期更新。

📖 *[可用模型列表](https://docs.digitalocean.com/products/gradient-ai-platform/details/models/)*

---

### 💰 **模型价格查询**

在使用服务前，请先查看各模型的价格。价格信息来自 DigitalOcean 的官方页面（无需 API 密钥）。

**查询方法：**
- 从 DigitalOcean 的文档页面获取实时价格信息（无需身份验证）
- 结果会缓存到 `/tmp/gradient_pricing_cache.json` 文件中（有效期 24 小时）
- 如果实时数据获取失败，系统会回退到之前的缓存数据

> **专业提示：** 在选择模型之前，运行 `python3 gradient_pricing.py --model "gpt-oss"` 命令，查看 `gpt-oss-120b`（每 100 万个令牌 0.10 美元）和 `gpt-oss-20b`（每 100 万个令牌 0.05 美元）的价格差异。

📖 *[价格文档](https://docs.digitalocean.com/products/gradient-ai-platform/details/pricing/)*

---

## **命令行接口（CLI）**

所有脚本都支持使用 `--json` 选项以生成机器可读的输出格式。

---

## **外部 API 端点**

| 端点            | 功能                |
|-----------------|-------------------|
| `https://inference.do-ai.run/v1/models` | 查看可用模型列表       |
| `https://inference.do-ai.run/v1/chat/completions` | 聊天式问答 API         |
| `https://inference.do-ai.run/v1/responses` | 响应 API（推荐使用）       |
| `https://inference.do-ai.run/v1/images/generations` | 图像生成 API         |
| `https://docs.digitalocean.com/.../pricing/` | 官方价格页面（数据抓取）     |

## **安全与隐私**

- 所有请求都会发送到 DigitalOcean 自有的 `inference.do-ai.run` 端点 |
- 你的 `GRADIENT_API_KEY` 会以 Bearer 令牌的形式包含在 `Authorization` 头部中 |
- 无其他敏感信息会被泄露 |
- 模型访问密钥仅用于推理任务，不会用于管理你的 DigitalOcean 账户 |
- 提示缓存数据仅保存在用户账户内，并会自动过期

## **信任声明**

> 使用此工具时，你的提示内容和数据会被发送到 DigitalOcean 的 Gradient Inference API。
> 仅在你信任 DigitalOcean 并对其处理的数据安全有信心时，才建议安装此工具。

## **重要注意事项**

- 在使用某个模型之前，请务必运行 `python3 gradient_models.py` 命令确认模型是否可用（模型列表会定期更新） |
- 所有脚本在执行失败时都会以代码 1 结束，并将错误信息输出到标准错误日志（stderr）中。