---
name: design-integration
description: >-
  Design a Uniswap integration architecture. Use when user is building a
  project that needs to integrate Uniswap and wants recommendations on
  integration method (Trading API vs SDK vs direct contract), architecture
  patterns, required dependencies, and security considerations.
allowed-tools: >-
  Read, Write, Edit, Glob, Grep,
  Task(subagent_type:integration-architect),
  mcp__uniswap__get_supported_chains
model: opus
---

# 设计集成

## 概述

该服务为任何项目设计完整的Uniswap集成架构，通过将任务委托给`integration-architect`代理来实现。生成的蓝图涵盖以下内容：集成方法建议（使用Trading API、Universal Router SDK、直接调用合约或V4钩子）、组件架构、带有版本的依赖项列表、安全审查及相应的缓解措施，以及有序的实施计划。

## 使用场景

当用户提出以下问题时，可激活该服务：
- “帮我集成Uniswap”
- “设计一个交换集成方案”
- “构建去中心化交易所（DEX）聚合器的架构”
- “如何构建套利机器人”
- “Uniswap集成计划”
- “如何将Uniswap功能添加到我的去中心化应用（dApp）中？”
- “在后台系统中集成Uniswap的最佳方式是什么？”
- “使用Uniswap的去中心化金融（DeFi）协议的架构设计”
- “我应该使用哪种Uniswap SDK？”

## 参数

| 参数            | 是否必填 | 默认值 | 说明                          |
|------------------|--------|---------|-------------------------------------------|
| projectType      | 是      | --      | 项目类型（例如：“DeFi仪表盘”、“套利机器人”、“钱包应用”、“DeFi协议”） |
| functionality    | 是      | --      | 所需的Uniswap功能：“交换（swap）”、“流动性池（LP）”或“两者兼有” |
| environment     | 否      | 自动检测   | 执行环境：“前端（frontend）”、“后端（backend）”、“智能合约（smart contract）”或“全栈（full-stack）” |
| chains         | 否      | ethereum | 目标链（单个链名或用逗号分隔的链列表）             |
| scale          | 否      | --      | 预期规模：交易量、并发用户数、延迟要求               |

## 工作流程

1. **从用户请求中提取参数**：确定项目类型、所需功能、目标环境和规模要求。如果用户有现有的代码库，请告知代理以便分析。
2. **委托给integration-architect**：使用`Task(subagent_type=integration-architect)`调用该服务，并提供所有相关信息。代理将：
   - 理解项目背景和需求
   - 评估集成方法并推荐主要方案及备用方案
   - 设计组件架构及数据流
   - 识别所有依赖项（NPM包、API、基础设施）
   - 进行安全审查，分析潜在攻击途径及相应的缓解措施
   - 制定有序的实施计划，并估算工作量
3. **向用户展示蓝图**：内容包括：
   - 带有明确理由的集成方法建议
   - 组件架构概览（包括各组件及其数据流）
   - 完整的依赖项列表（包括版本和用途）
   - 安全考虑因素及具体的缓解措施
   - 逐步实施的顺序及工作量估算
   - 整体复杂度评估

## 输出格式

以结构化格式呈现集成蓝图：

```text
Integration Blueprint: DeFi Dashboard with Swap (Ethereum + Base)

  Recommended Method: Trading API (primary), Universal Router SDK (fallback)
  Rationale: Trading API provides optimized routing with minimal frontend
             complexity. Fallback to SDK for advanced use cases or API downtime.

  Architecture:
    User -> QuoteService -> ApprovalManager -> SwapExecutor -> Wallet -> Chain
    
    Components:
      QuoteService:      Fetches and caches quotes from Trading API
      ApprovalManager:   Manages Permit2 approvals and allowances
      SwapExecutor:      Constructs and submits swap transactions
      ChainManager:      Multi-chain config and RPC connections

  Dependencies:
    @uniswap/sdk-core    ^5.8.0    Token and price primitives
    viem                 ^2.21.0   Ethereum client
    wagmi                ^2.14.0   React wallet hooks
    @tanstack/react-query ^5.0.0   Data fetching and caching

  Security:
    - Stale quotes: Refresh every 15s, enforce deadline (block.timestamp + 300s)
    - Approvals: Permit2 with exact amounts and 30-min expiry
    - Key management: wagmi wallet connection only, never handle keys

  Implementation Order:
    1. Wallet connection (wagmi)           — 1 day
    2. Chain configuration                 — 0.5 days
    3. Quote fetching service              — 1 day
    4. Permit2 approval flow               — 1 day
    5. Swap execution and tracking         — 1.5 days
    6. Error handling and retry logic      — 1 day

  Complexity: Medium
```

## 重要说明

- 该服务完全委托给`integration-architect`代理处理，不会直接调用MCP工具。
- 蓝图是根据具体项目类型和需求定制的，而非通用模板。
- 对于已有代码库的情况，代理会分析现有代码并推荐适合的集成方案。
- 实施顺序会考虑组件之间的依赖关系，以确保开发过程顺利进行。
- 严格遵循项目规范，使用`viem`（而非`ethers.js`）和`Permit2`（而非旧版本的`approve`）。

## 错误处理

| 错误类型            | 向用户显示的提示信息 | 建议的操作                          |
|------------------|------------------|-------------------------------------------|
| `VAGUE_PROJECT`     | “需要更多关于您项目的详细信息才能推荐集成方案。” | 请描述项目类型及所需的Uniswap功能         |
| `DEPRECATED_APPROACH`    | “请求的集成方法已过时。建议使用替代方案。” | 请遵循更新的推荐方案                   |
| `UNSUPPORTEDCHAIN`     | “Uniswap未在指定的链上部署。” | 请从支持的11个链中选择目标链             |
| `CONFLICTING_REQUIREMENTS` | “需求之间存在冲突（例如，同时需要前端和直接调用合约）。” | 请明确执行环境并调整期望                         |