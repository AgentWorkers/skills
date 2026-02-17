---
name: astrai-inference-router
description: 通过智能路由和隐私控制功能，将所有大型语言模型（LLM）的调用都通过 Astrai 进行路由，从而实现超过 40% 的成本节省。
version: 1.0.0
homepage: https://github.com/beee003/astrai-openclaw
metadata:
  clawdbot:
    emoji: "⚡"
    requires:
      env: ["ASTRAI_API_KEY", "ANTHROPIC_API_KEY"]
    primaryEnv: "ASTRAI_API_KEY"
    files: ["plugin.py", "config.example.toml"]
tags: [inference, routing, privacy, cost-optimization, gdpr, eu, savings, llm-gateway]
---
# Astrai 推理路由器

所有大型语言模型（LLM）的调用都会通过 Astrai 的智能路由系统进行路由。使用该服务可节省超过 40% 的 API 使用成本，并且内置了隐私保护功能。

## 功能介绍

- **智能路由**：根据任务类型（代码编写、研究、聊天、创意创作等）选择最合适的模型。
- **成本优化**：通过贝叶斯算法找到符合质量要求的最低成本服务提供商。
- **自动故障转移**：当某个服务提供商出现故障时，系统会自动切换到备用提供商。
- **个人身份信息保护**：在数据传输前会删除所有个人身份信息（PII）。
- **欧盟专用路由**：支持欧盟地区的用户，符合 GDPR 法规。
- **预算限制**：设置每日使用上限，防止费用失控。
- **实时监控**：可实时查看每条请求的节省金额。

## 设置方法

1. 在 [as-trai.com](https://as-trai.com) 获取免费的 API 密钥。
2. 在您的环境配置或技能配置中设置 `ASTRAI_API_KEY`。
3. 选择隐私模式（默认为 `enhanced`）。
4. 设置完成——之后所有 LLM 调用都将通过 Astrai 进行路由。

## 隐私模式

- **standard**：具备完整的路由功能，进行常规日志记录。
- **enhanced**：删除个人身份信息，仅记录元数据，并强制使用欧盟地区的服务提供商。
- **max**：不保留任何数据，仅支持欧盟地区的服务，删除所有个人身份信息，不记录提示内容。

## 环境变量

| 变量 | 是否必需 | 描述 | 默认值 |
| --- | --- | --- | --- |
| `ASTRAI_API_KEY` | 是 | 从 as-trai.com 获取的 API 密钥 | — |
| `PRIVACY_MODE` | 否 | 可选：standard, enhanced, max | enhanced |
| `REGION` | 否 | 可选：any, eu, us | any |
| `DAILY_BUDGET` | 否 | 每日最大花费上限（单位：美元，0 表示无限制） | 10 |

## 外部端点

| 端点 | 功能 | 发送的数据 |
| --- | --- | --- |
| `https://as-trai.com/v1/chat/completions` | LLM 推理路由 | 提示内容（在 `enhanced` 或 `max` 模式下会删除个人身份信息） |
| `https://as-trai.com/v1/signup` | 注册免费 API 密钥 | 电子邮件地址 |

## 安全性与隐私保护

- 所有请求均通过 API 密钥在请求头中进行身份验证。
- 在数据离开您的设备之前，`enhanced` 或 `max` 模式会先删除所有个人身份信息。
- **欧盟专用路由**：确保提示内容不会离开欧盟地区的基础设施。
- 在 `max` 隐私模式下，系统不保留任何数据。
- 该技能不会存储任何用户凭证，仅通过环境变量保存您的 API 密钥。
- 源代码完全公开：[github.com/beee003/astrai-openclaw](https://github.com/beee003/astrai-openclaw)

## 模型调用机制

该技能会拦截所有出站的 LLM API 调用，并将其重新路由到 Astrai 网关。Astrai 网关会根据任务类型、成本和质量选择最合适的提供商和模型。您的提示内容将由第三方 LLM 提供商（如 Anthropic、OpenAI、Google、Mistral 等）根据您的地区和隐私设置进行处理。

## 定价方案

- **免费版**：每天 1,000 次请求，支持智能路由和自动故障转移功能。
- **专业版**（每月 49 美元）：无限请求量，支持欧盟地区路由和个人身份信息删除功能，提供分析报告。
- **企业版**（每月 199 美元）：支持多代理管理面板、合规性报告和 SLA 服务。