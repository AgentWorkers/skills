---
name: clawzempic
version: 2.3.5
description: 通过智能路由、缓存和内存管理，可以将大型语言模型（LLM）的运行成本降低70%至95%。
author: Clawzempic
homepage: https://clawzempic.ai
license: MIT
keywords: [llm, proxy, routing, caching, cost-optimization, memory, anthropic, openrouter]
metadata:
  openclaw:
    emoji: "⚡"
    category: ai-tools
    requires:
      env: []
---

# Clawzempic

这是一个即插即用的大型语言模型（LLM）代理工具，它可以将简单的请求路由到成本更低的模型，缓存重复出现的上下文信息，并提供跨会话的数据存储功能。该工具支持使用 Anthropic 和 OpenRouter 的 API 密钥进行访问。

## 安装

```bash
openclaw plugins install clawzempic
```

该插件会自动处理用户的注册、身份验证以及模型注册流程。

或者，您也可以选择单独安装该插件：

```bash
npx clawzempic
```

## 工作原理

系统会在 <2 毫秒内评估每个请求的复杂性，并将其路由到相应的处理层级：

| 处理层级 | 流量占比 | 节省成本 |
|------|---------|---------|
| 简单请求 | 约 45% | 高达 95% |
| 中等复杂度请求 | 约 25% | 高达 80% |
| 复杂请求 | 约 20% | 0%（保持原始服务质量） |
| 推理类请求 | 约 10% | 0%（保持原始服务质量） |

系统中没有专门用于分类请求的 LLM 模型；路由决策由一个基于多维度的评分系统来完成。

## 数据存储

所有数据都存储在服务器端，并实现跨会话的持久化。无需额外的插件或 API 密钥，用户代理无需进行任何额外的配置。

- 最近的活动记录（每个会话独立保存）
- 临时工作区（跨会话使用的笔记）
- 上下文信息（每个请求单独保存）
- 核心数据（永久性的事实和用户偏好设置）
- 长期记忆（基于嵌入技术的存储）

## 验证方法

```bash
npx clawzempic doctor    # Check config + test connection
npx clawzempic savings   # Savings dashboard
```

## 链接

- 官网：https://clawzempic.ai
- 仪表盘：https://www.clawzempic.ai/dash
- npm 包：https://www.npmjs.com/package/clawzempic