---
name: lightningprox
description: 这是一个按使用量计费的AI服务网关，支持通过Bitcoin Lightning协议调用5家提供商提供的19种模型。无需API密钥或账户注册——只需支付相应的费用（以sats为单位），即可立即使用模型进行推理。该服务支持Anthropic、OpenAI、Together.ai（Llama 4）、Mistral和Google Gemini等模型。
acceptLicenseTerms: true
metadata:
  clawdbot:
    emoji: "⚡"
    homepage: https://lightningprox.com
    requires:
      env:
        - LIGHTNINGPROX_SPEND_TOKEN
---
# LightningProx — 一个基于 Lightning 的原生 AI 服务网关

通过比特币 Lightning 的微支付方式，按使用次数计费，可访问来自 5 家提供商的 19 个 AI 模型。无需 API 密钥、无需订阅、也无需创建账户。只需支付相应的费用，即可使用这些 AI 模型进行推理。

## 使用场景

- 在没有提供商 API 密钥的情况下访问 AI 模型
- 使用 Lightning 支付功能进行自主推理
- 比较多个提供商提供的模型输出结果
- 通过开源模型（如 Llama 4、Mistral、DeepSeek）实现低成本推理
- 执行视觉任务（Pixtral）
- 生成代码（Codestral、Devstral）
- 进行推理任务（Magistral）

## 支持的模型（共 19 个）

| 模型 | 提供商 | 类型 |
|-------|----------|------|
| `claude-opus-4-5-20251101` | Anthropic | 聊天 |
| `gpt-4-turbo` | OpenAI | 聊天 |
| `meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8` | Together.ai | 聊天 |
| `meta-llama/Llama-3.3-70B-Instruct-Turbo` | Together.ai | 聊天 |
| `meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo` | Together.ai | 聊天 |
| `mistralai/Mixtral-8x7B-Instruct-v0.1` | Together.ai | 聊天 |
| `deepseek-ai/DeepSeek-V3` | Together.ai | 聊天 |
| `mistral-large-latest` | Mistral | 聊天 |
| `mistral-medium-latest` | Mistral | 聊天 |
| `mistral-small-latest` | Mistral | 聊天 |
| `open-mistral-nemo` | Mistral | 聊天 |
| `codestral-latest` | Mistral | 代码生成 |
| `devstral-latest` | Mistral | 代码生成（代理模式） |
| `pixtral-large-latest` | Mistral | 视觉任务 |
| `magistral-medium-latest` | Mistral | 推理任务 |
| `gemini-2.5-flash` | Google | 聊天 |
| `gemini-2.5-pro` | Google | 聊天 |
| `gemini-3-flash-preview` | Google | 聊天 |
| `gemini-3-pro-preview` | Google | 聊天 |

## 支付流程

### 选项 A — 使用代币（推荐用于重复使用）
```bash
# 1. 在 lightningprox.com/topup 进行充值，获取代币
# 2. 直接使用代币进行请求
curl -X POST https://lightningprox.com/v1/messages \
  -H "Content-Type: application/json" \
  -H "X-Spend-Token: $LIGHTNINGPROX_SPEND_TOKEN" \
  -d '{
    "model": "claude-opus-4-5-20251101",
    "messages": [{"role": "user", "content": "Hello"}],
    "max_tokens": 1000
  }'
```

### 选项 B — 按每次请求付费
```bash
# 1. 不使用代币发送请求 → 获取支付账单
curl -X POST https://lightningprox.com/v1/messages \
  -H "Content-Type: application/json" \
  -d '{"model": "gemini-2.5-flash", "messages": [{"role": "user", "content": "Hello"}], "max_tokens": 100}'

# 2. 支付返回的 Lightning 支付账单
# 3. 重新发送请求时添加 `X-Payment-Hash` 头部信息
```

## 替代 OpenAI SDK 的方案

```bash
npm install lightningprox-openai
```

```javascript
// 之前的代码：
import OpenAI from 'openai';

// 现在的代码：
import OpenAI from 'lightningprox-openai';
const client = new OpenAI({ apiKey: process.env.LIGHTNINGPROX_SPEND_TOKEN });

// 其他代码保持不变：
const response = await client.chat.completions.create({
  model: 'claude-opus-4-5-20251101',
  messages: [{ role: 'user', content: 'Hello' }
});
```

只需修改这两行代码，其他部分均无需更改。

## 查看可用模型
```bash
curl https://lightningprox.com/api/capabilities
```

## 安全性说明

| 权限 | 范围 | 原因 |
|------------|-------|--------|
| 网络访问 | lightningprox.com | 用于 AI 推理的 API 调用 |
| 读取环境变量 | LIGHTNINGPROX_SPEND_TOKEN | 预付费请求的认证所需 |

## 信任声明

LightningProx 由 LPX Digital Group LLC 运营。所有支付操作均需通过认证完成；数据仅存储在请求日志中，不保存用户账户信息或进行任何身份验证（KYC）流程。所有服务均通过 lightningprox.com 提供。