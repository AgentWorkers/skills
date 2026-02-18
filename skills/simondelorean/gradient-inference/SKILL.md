---
name: gradient-inference
description: 这是一个关于 DigitalOcean Gradient AI Serverless Inference 的社区技能（非官方）。你可以使用该技能来查找可用的模型和价格信息，运行基于提示缓存的聊天完成功能（chat completions），或者通过 Responses API 来生成图像。该技能兼容 OpenAI。
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
      pip:
        - requests>=2.31.0
        - beautifulsoup4>=4.12.0
  author: Rogue Iteration
  version: "0.1.3"
  tags: ["digitalocean", "gradient-ai", "inferencing", "llm", "chat-completions", "image-generation"]
---
# 🦞 Gradient AI — 无服务器推理服务

> ⚠️ **此功能属于非官方社区资源，不由 DigitalOcean 提供维护。使用该功能需自行承担风险。**

> “既然海洋已经提供了资源，为何还要自己去管理GPU呢？”——古老的龙虾谚语

利用 DigitalOcean 的 [Gradient 无服务器推理服务](https://docs.digitalocean.com/products/gradient-ai-platform/how-to/use-serverless-inference/)，无需管理基础设施即可调用大型语言模型。该 API 与 OpenAI 兼容，因此标准 SDK 和开发模式均可直接使用——只需指向 `https://inference.do-ai.run/v1` 即可开始使用。

## 认证

所有请求都必须在 `Authorization: Bearer` 头部包含一个 **模型访问密钥**。

```bash
export GRADIENT_API_KEY="your-model-access-key"
```

**获取模型访问密钥的位置：** [DigitalOcean 控制台](https://cloud.digitalocean.com) → Gradient AI → 模型访问密钥 → 创建密钥

📖 *[完整认证文档](https://docs.digitalocean.com/products/gradient-ai-platform/how-to/use-serverless-inference/#create-a-model-access-key)*

---

## 工具

### 🔍 可用模型列表

在使用模型之前，请先查看可用的语言模型（LLMs）。

```bash
python3 gradient_models.py                    # Pretty table
python3 gradient_models.py --json             # Machine-readable
python3 gradient_models.py --filter "llama"   # Search by name
```

建议不要直接硬编码模型 ID，因为模型会随着时间更新或被淘汰。

**直接 API 调用：**
```bash
curl -s https://inference.do-ai.run/v1/models \
  -H "Authorization: Bearer $GRADIENT_API_KEY" | python3 -m json.tool
```

📖 *[模型参考文档](https://docs.digitalocean.com/products/gradient-ai-platform/details/models/)*

---

### 💬 聊天补全功能

这是一个经典的功能：发送结构化消息（系统/用户/助手角色），然后获取响应。该功能与 OpenAI 兼容，您可能已经熟悉其工作原理。

```bash
python3 gradient_chat.py \
  --model "openai-gpt-oss-120b" \
  --system "You are a helpful assistant." \
  --prompt "Explain serverless inference in one paragraph."

# Different model
python3 gradient_chat.py \
  --model "llama3.3-70b-instruct" \
  --prompt "Write a haiku about cloud computing."
```

**直接 API 调用：**
```bash
curl -s https://inference.do-ai.run/v1/chat/completions \
  -H "Authorization: Bearer $GRADIENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "openai-gpt-oss-120b",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "Hello!"}
    ],
    "temperature": 0.7,
    "max_tokens": 1000
  }'
```

📖 *[聊天补全功能文档](https://docs.digitalocean.com/products/gradient-ai-platform/how-to/use-serverless-inference/#chat-completions)*

---

### ⚡ 响应 API（推荐使用）

对于新的集成项目，建议使用 DigitalOcean 推荐的 [响应 API](https://docs.digitalocean.com/products/gradient-ai-platform/how-to/use-serverless-inference/#responses-api)。该 API 的请求格式更简单，并支持 **提示缓存**，避免重复计算相同的数据。

**直接 API 调用：**
```bash
curl -s https://inference.do-ai.run/v1/responses \
  -H "Authorization: Bearer $GRADIENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "openai-gpt-oss-120b",
    "input": "Explain prompt caching.",
    "store": true
  }'
```

**使用场景对比：**
| | 聊天补全 | 响应 API |
|---|---|---|
| **请求格式** | 包含角色信息的消息数组 | 单个 `input` 字符串 |
| **提示缓存** | 不支持 | 支持（通过 `store: true` 配置） |
| **多步骤任务处理** | 需手动处理 | 内置支持 |
| **适用场景** | 结构化对话 | 简单查询，节省成本 |

📖 *[响应 API 文档](https://docs.digitalocean.com/products/gradient-ai-platform/how-to/use-serverless-inference/#responses-api)*

---

### 🖼️ 生成图片

可以将文本提示转换为图片。有时候，一张图表比文字更直观。

**直接 API 调用：**
```bash
curl -s https://inference.do-ai.run/v1/images/generations \
  -H "Authorization: Bearer $GRADIENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "dall-e-3",
    "prompt": "A lobster analyzing candlestick charts",
    "n": 1
  }'
```

📖 *[图片生成文档](https://docs.digitalocean.com/products/gradient-ai-platform/how-to/use-serverless-inference/#image-generation)*

---

## 🧠 模型选择指南

并非所有模型都适合所有场景。请谨慎选择：

| 模型 | 适用场景 | 计算速度 | 图像质量 | 对上下文的要求 |
|-------|----------|-------|---------|---------|
| `openai-gpt-oss-120b` | 复杂推理、分析、写作 | 中等 | ★★★★★ | 128K 内存 |
| `llama3.3-70b-instruct` | 通用任务、指令执行 | 快速 | ★★★★ | 128K 内存 |
| `deepseek-r1-distill-llama-70b` | 数学计算、代码编写、逐步推理 | 较慢 | ★★★★ | 128K 内存 |
| `qwen3-32b` | 快速任务处理、简单查询 | 最快 | ★★★ | 32K 内存 |

> **专业提示：** 根据需求选择合适的模型。可以先使用性能较快的模型（如 `qwen3-32b`）进行初步处理或任务分类，只有在需要更高计算能力时再切换到更强大的模型（如 `openai-gpt-oss-120b`）。对于重复使用的场景，建议启用提示缓存功能。

请务必运行 `python3 gradient_models.py` 命令查看当前可用的模型列表——模型列表会定期更新。

📖 *[可用模型列表](https://docs.digitalocean.com/products/gradient-ai-platform/details/models/)*

---

### 💰 模型定价查询

在使用模型之前，请先查看其价格。价格信息来自 DigitalOcean 的官方页面（无需 API 密钥）。

**获取价格信息的方法：**
- 从 DigitalOcean 的文档中获取实时价格信息（无需认证）
- 将结果缓存到 `/tmp/gradient_pricing_cache.json` 文件中（缓存有效期为 24 小时）
- 如果实时获取失败，系统会回退到之前的缓存数据

> **专业提示：** 在选择模型之前，运行 `python3 gradient_pricing.py --model "gpt-oss"` 命令，查看 `gpt-oss-120b`（每 100 万个令牌 0.10 美元）和 `gpt-oss-20b`（每 100 万个令牌 0.05 美元）的价格差异。

📖 *[定价文档](https://docs.digitalocean.com/products/gradient-ai-platform/details/pricing/)*

---

## 命令行接口（CLI）参考

所有脚本都支持使用 `--json` 选项以生成机器可读的输出格式。

```
gradient_models.py   [--json] [--filter QUERY]
gradient_chat.py     --prompt TEXT [--model ID] [--system TEXT]
                     [--responses-api] [--cache] [--temperature F]
                     [--max-tokens N] [--json]
gradient_image.py    --prompt TEXT [--model ID] [--output PATH]
                     [--size WxH] [--json]
gradient_pricing.py  [--json] [--model QUERY] [--no-cache]
```

---

## 外部接口

| 接口地址 | 功能 |
|----------|---------|
| `https://inference.do-ai.run/v1/models` | 查看可用模型 |
| `https://inference.do-ai.run/v1/chat/completions` | 聊天补全 API |
| `https://inference.do-ai.run/v1/responses` | 响应 API（推荐使用） |
| `https://inference.do-ai.run/v1/images/generations` | 图片生成 API |
| `https://docs.digitalocean.com/.../pricing/` | 官方定价页面（数据来源） |

## 安全性与隐私

- 所有请求都会发送到 DigitalOcean 自带的 `inference.do-ai.run` 端点 |
- 您的 `GRADIENT_API_KEY` 会以 Bearer 令牌的形式包含在 `Authorization` 头部 |
- 无其他敏感信息或本地数据会被泄露 |
- 模型访问密钥仅用于推理任务，不会用于管理您的 DigitalOcean 账户 |
- 提示缓存数据仅保存在您的账户内，并会自动过期

## 信任声明

> 使用此功能时，您发送的提示和数据会直接传输到 DigitalOcean 的 Gradient Inference API。
> 请确保您信任 DigitalOcean，才能将其内容发送给他们的模型。

## 重要注意事项

- 在使用任何模型之前，请先运行 `python3 gradient_models.py` 命令确认模型是否可用（模型列表会定期更新） |
- 所有脚本在执行失败时都会以代码 1 结束，并将错误信息输出到标准错误日志（stderr）中。