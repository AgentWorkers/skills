---
name: clawzempic
version: 2.3.4
description: "价格最高可降低95%，且质量毫无损失。这一优势已在59个经过盲测的提示中得到验证。该工具是一款即插即用的LLM代理，具备智能路由、提示缓存功能，支持零配置的使用方式，并内置了多种安全防护机制。"
author: Clawzempic
homepage: https://clawzempic.ai
license: MIT
keywords: [llm, proxy, routing, caching, cost-optimization, memory, openrouter, openai, openclaw, anthropic, api-proxy, smart-routing, prompt-caching, claude, opus, sonnet, haiku, cheaper, save-money, reduce-costs, agent-memory, cursor, claude-code, vibe-coding]
metadata:
  openclaw:
    emoji: "⚡"
    category: ai-tools
    requires:
      env: []
---

# Clawzempic

**价格最高可节省95%，且质量毫无损失。别被大型语言模型（LLM）提供商坑了！**

经过59个提示的A/B评估，由GPT-4o进行盲评：

```
Quality:  4.53 (Clawzempic) vs 4.52 (direct Opus) — statistically tied!
Cost:     up to 95% cheaper
Win rate: 28-28-3 (dead even)
```

立即获取Clawzempic，打造属于您的OpenClaw机器人：智能路由、提示缓存、零配置的顶级性能以及内置的安全防护机制。整个安装过程仅需30秒！

Clawzempic兼容**OpenRouter**（支持300多种模型）、**OpenAI**和**Anthropic**的API密钥。

```
OpenClaw → Clawzempic proxy → Your LLM Provider (OpenRouter, OpenAI, or Anthropic)
           ├─ Routes simple tasks to cheaper models (saves up to 95%)
           ├─ Caches repeated context (prompt caching breakpoints)
           ├─ Adds memory across sessions (5-tier, zero config)
           └─ Built-in safety guardrails for sensitive data
```

## 安装

### 推荐使用OpenClaw插件

```bash
openclaw plugins install clawzempic
openclaw models auth login --provider clawzempic
```

安装流程会为您创建账户、注册4个模型，并将`clawzempic/auto`设置为默认路由方式。30秒后，您就能开始节省费用了！

### 独立的命令行界面（CLI）

```bash
npx clawzempic
```

## 路由机制

每个请求的复杂度会在<2毫秒内被评估，并被路由到最合适的模型。

**Clawzempic支持OpenRouter上的任何模型（涵盖所有提供商的300多种模型），同时也支持直接使用Anthropic和OpenAI的API密钥**。您只需选择所需的提供商，Clawzempic会自动完成路由选择。

| 路由层级 | 流量类型 | 路由方式 | 节省费用 |
|------|---------|--------------|---------|
| **简单** | 约45% | 路由到最便宜的可用模型 | 高达95% |
| **中等** | 约25% | 路由到中等性能的模型 | 高达80% |
| **复杂** | 约20% | 路由到顶级性能的模型 | 0%（保持完整质量） |
| **推理** | 约10% | 使用顶级模型并进行扩展推理 | 0% |

*以OpenRouter为例：简单请求 → GPT-4o-mini（0.15美元/次）；中等请求 → Gemini Flash（0.60美元/次）；复杂请求 → Claude Opus（15美元/次）。Clawzempic支持OpenRouter上的所有模型（包括DeepSeek、Llama、Mistral等），同时也支持直接使用Anthropic和OpenAI的API密钥。*

分类机制采用加权多维度评分系统：考虑词汇复杂性、结构深度、领域相关性以及推理能力等因素。如果需要多次使用同一工具，系统会自动升级为更复杂的路由方式。在处理请求的过程中，不会使用任何大型语言模型（LLM）进行辅助判断。

## 零配置内存管理

大多数内存管理方案都需要通过指令告诉代理将数据写入文件；但如果代理跳过某些步骤或在数据刷新前压缩数据，内存就会丢失。

Clawzempic采用**服务器端**内存管理机制：您的代理无需额外“记忆”数据。无需安装任何插件或额外的API密钥，也无需进行复杂配置。

```
┌─────────────────────────────────────────────────────────┐
│                    5-TIER MEMORY                         │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────┐  Tier 1: Recent Activity               │
│  │  Last 10 msgs │  Per-session, auto-injected            │
│  └──────────────┘                                        │
│  ┌──────────────┐  Tier 2: Scratchpad                    │
│  │  Working notes │  Cross-session, current task context   │
│  └──────────────┘                                        │
│  ┌──────────────┐  Tier 3: Working Memory                │
│  │  Active window │  Smart context windowing per-request   │
│  └──────────────┘                                        │
│  ┌──────────────┐  Tier 4: Core Memory                   │
│  │  Preferences  │  Permanent: facts, decisions, prefs    │
│  └──────────────┘                                        │
│  ┌──────────────┐  Tier 5: Long-term                     │
│  │  Episodic     │  Permanent: embedding-based recall      │
│  └──────────────┘                                        │
│                                                          │
│  All tiers injected automatically. Nothing to configure.  │
│  Memory travels with your account — new infra, same brain.│
└─────────────────────────────────────────────────────────┘
```

**与仅依赖内存管理的方案相比：**  
- 无需额外的API密钥。  
- 无需安装任何插件。  
- 无需依赖WAL协议（一种数据存储协议）。  
- 由于数据在服务器端进行处理和检索，因此系统始终能稳定运行，而无需依赖代理是否记得将数据写入文件。

## 安全防护机制

Clawzempic拥有七重安全防护机制，可自动保护您的代理：

- **敏感数据保护**：在数据传输到模型之前，会自动屏蔽其中的敏感信息和令牌。  
- **输入验证**：检查输入内容是否存在可疑模式。  
- **工具输出审核**：确保工具返回的响应不包含不必要的信息。  
- **策略引擎**：可根据客户需求配置安全规则（即将推出自助配置功能）。  

无需任何额外配置，您的代理就能获得更高的安全性。

## 可用的模型

| 模型 | ID | 适用场景 |  
|-------|-----|----------|  
| Auto（推荐） | `clawzempic/auto` | 根据请求自动选择最佳模型 |  

使用OpenRouter的API密钥，您可以访问所有主要提供商提供的300多种模型；同时也可以使用Anthropic的API密钥。

## 验证效果

```bash
npx clawzempic doctor    # Check config + test connection
npx clawzempic status    # Usage stats
npx clawzempic savings   # Savings dashboard (24h, 7d, 30d)
```

## 节省费用的示例

```
  ⚡ Clawzempic Savings Dashboard

  Last 24h:  $2.41 saved  (82% reduction)
  Last 7d:   $18.93 saved (71% reduction)
  Last 30d:  $64.21 saved (73% reduction)

  Routing breakdown (example):
    Simple:    847 requests → Gemini Flash   (95% saved)
    Mid:       412 requests → GPT-4o-mini    (80% saved)
    Complex:   198 requests → your top model (full quality)
```

## 功能对比

| | Clawzempic | 仅依赖路由器的工具（如ClawRouter、RelayPlane） | 仅依赖内存管理的工具（如Elite、Triple Memory） |  
|---|---|---|---|  
| 质量保障 | 经过59个提示的A/B评估（由GPT-4o盲评） | 无官方基准测试 | 无 |  
| 智能路由 | 服务器端处理，评分速度快（<2毫秒），采用加权评分机制 | 依赖本地代理或规则配置 | 否 |  
| 提示缓存 | 自动设置断点 | 否 | 否 |  
| 内存管理 | 五层内存管理机制，零配置，服务器端处理 | 否 | 需要安装插件和额外的API密钥，且依赖代理的配合 |  
| 安全性 | 通过113项安全评估 | 否 | 否 |  
| 配置难度 | 仅需一条命令 | 安装、配置并运行守护进程 | 需要安装多个工具、进行复杂配置并使用API密钥 |  

---

*由[@naveenspark](https://x.com/naveenspark)开发：我曾在昂贵的LLM提供商上浪费了数千美元，还厌倦了不断安装各种工具和插件。现在，我的经验可以帮到您！*

## 链接：

- **支持与社区**：https://t.me/+VmQpi5WWPx0wOWZh  
- **控制面板**：https://www.clawzempic.ai/dash  
- **官方网站**：https://clawzempic.ai  
- **npm包**：https://www.npmjs.com/package/clawzempic