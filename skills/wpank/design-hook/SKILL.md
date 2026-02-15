---
name: design-hook
description: >-
  Design a Uniswap V4 hook architecture without code generation. Use when user
  wants to plan a hook, understand which callbacks to use, or review an
  architecture before building. Returns a design document, not code.
allowed-tools: >-
  Read, Glob, Grep,
  Task(subagent_type:hook-builder),
  mcp__uniswap__get_supported_chains
model: opus
---

# 设计钩子（Design Hook）

## 概述

该功能用于设计 Uniswap V4 的钩子架构，但不生成任何代码。它通过仅限设计的模式将任务委托给 `hook-builder` 代理，以生成一份全面的设计文档。该文档涵盖以下内容：所需回调函数、钩子配置参数的要求、状态管理方法、Gas 费用估算、安全考虑因素以及架构决策。您可以使用此功能在构建之前进行规划，或评估某个钩子的可行性。

## 使用场景

当用户提出以下问题时，请激活此功能：
- “为……设计一个钩子”
- “我需要哪些回调函数来实现……”
- “……的钩子架构是什么”
- “能否构建一个……的钩子”
- “动态费用钩子的实现方式是怎样的？”
- “帮我梳理一下钩子的设计思路”
- “TWAMM 需要哪些配置参数？”

## 参数

| 参数          | 是否必填 | 默认值 | 说明                          |
|--------------|---------|---------|---------------------------------------------|
| behavior       | 是       | --       | 钩子的具体行为（例如：限价单、动态费用、预言机定价）             |
| constraints     | 否       | --       | Gas 预算、安全要求或其他特定的设计约束                |
| integrations    | 否       | --       | 钩子需要交互的外部系统（预言机、治理机制、质押等）           |

## 工作流程

1. **从用户请求中提取参数**：确定钩子的具体行为、约束条件以及任何需要集成的外部系统。
2. **以仅限设计的模式委托给 hook-builder**：调用 `Task(subagent_type:hook-builder)`，并明确指示仅生成设计文档（不生成代码、不写入任何文件）。`hook-builder` 将执行以下操作：
   - 分析需求并确定所需的 V4 回调函数
   - 将回调函数与钩子配置参数关联并验证其组合是否合理
   - 设计状态管理方案（包括使用何种存储方式、数据结构）
   - 估算每个回调函数的 Gas 费用
   - 识别与该钩子设计相关的安全问题
   - 评估可行性并指出潜在问题
3. **向用户展示设计文档**，内容包括：
   - 所需的回调函数及其用途
   - 钩子配置参数及其含义
   - 状态管理方案（存储变量、数据结构、访问模式）
   - Gas 费用估算及对性能的影响
   - 安全考虑因素及相应的缓解措施
   - 架构决策及其理由
   （如适用）与其他方案的比较

## 输出格式

输出一份结构化的设计文档：

```text
V4 Hook Design: Dynamic Fee Hook

  Callbacks Required:
    - beforeSwap: Read volatility oracle, calculate dynamic fee
    - beforeInitialize: Set initial fee parameters and oracle address

  Hook Flags: BEFORE_SWAP_FLAG | BEFORE_INITIALIZE_FLAG
  Bitmask: 0x2080

  State Management:
    - volatilityOracle: IVolatilityOracle (immutable, set in constructor)
    - baseFee: uint24 (configurable by owner)
    - maxFee: uint24 (cap to prevent excessive fees)
    - feeMultiplier: uint24 (scales with volatility)

  Gas Estimates:
    beforeSwap: ~30,000 gas (oracle read + fee calculation)
    beforeInitialize: ~25,000 gas (one-time setup)

  Security Considerations:
    - Oracle manipulation: Use TWAP, not spot price
    - Fee cap: Enforce maxFee to protect traders
    - Owner control: Fee parameters updatable by owner only

  Architecture Decisions:
    - Using beforeSwap (not afterSwap) to set fee before execution
    - External oracle for volatility data rather than on-chain calculation
    - Fee bounded between baseFee and maxFee for predictability

  Alternative Approaches:
    - On-chain volatility calculation (higher gas, no oracle dependency)
    - Fixed fee tiers with governance voting (simpler, less responsive)
```

## 重要说明

- 该功能仅生成设计文档，不生成代码也不写入任何文件。
- 设计文档提供了足够的细节，以便用户在准备好后使用 `build-hook` 功能进行后续开发。
- 如果钩子设计不可行（例如，需要的回调函数不被 V4 支持），系统会明确告知用户。
- Gas 费用估算基于典型实现情况，实际费用可能因实现细节而有所不同。

## 错误处理

| 错误类型            | 向用户显示的消息 | 建议的操作                        |
|------------------|------------------|-------------------------------------------|
| `VAGUE_REQUIREMENTS`     | “需要更多关于所需钩子行为的详细信息。” | 请提供更具体的行为描述（例如：“在时间节点执行限价单”）       |
| `UNSUPPORTED_CALLBACK`     | “V4 不支持所请求的回调函数。” | 请查看 V4 支持的回调函数并调整需求             |
| `INFEASIBLE_DESIGN`     | “当前的 V4 功能无法实现该钩子设计。” | 请简化需求或考虑其他解决方案                |