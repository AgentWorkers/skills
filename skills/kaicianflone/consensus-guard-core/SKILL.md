---
name: consensus-guard-core
description: Shared deterministic guard primitives for the Consensus.Tools skill family: hard-block taxonomy, weighted vote aggregation, reputation updates, idempotency keys, strict schema enforcement, and indexed board artifact access.
homepage: https://github.com/kaicianflone/consensus-guard-core
source: https://github.com/kaicianflone/consensus-guard-core
upstream:
  consensus-tools: https://github.com/kaicianflone/consensus-tools
---

# consensus-guard-core

`consensus-guard-core` 是 Consensus Guard 生态系统中通用的策略引擎。

## 该技能/包提供的功能

- 统一的硬性规则分类体系
- 确定的 `aggregateVotes()` 策略函数
- 具有限制机制的确定性声誉更新规则
- 用于确保重试安全性的幂等性密钥生成机制
- 用于严格验证未知字段的辅助函数
- 基于索引的董事会读取辅助函数，以支持可扩展的工件查找

## 重要性

如果没有一个统一的核心框架，每个保护机制（guard）的策略逻辑都可能变得不兼容。该包确保了跨不同领域的行为一致性、可重放性和可比较性。

## 在生态系统中的作用

`consensus-guard-core` 被 publish/support/merge/action 等保护机制所使用，应被视为策略基础设施，而不是面向最终用户的工作流程技能。

## 对大型语言模型（LLM）编排的好处

- 降低集成风险
- 确保不同工作流程中的决策语义一致性
- 便于审计和跨技能分析

## 运行时、凭证和网络行为

- 运行时二进制文件：`node`、`tsx`
- 该包的核心决策/路径辅助函数不涉及网络调用
- 该包不要求任何凭证
- 该包读取的环境配置文件：`CONSENSUS_STATE_FILE`、`CONSENSUS_STATE_ROOT`（用于解析董事会/状态路径）
- 当调用者使用写入辅助函数（例如 `writeArtifact`）时，数据会写入配置的共识状态路径下的文件系统中

## 依赖关系信任模型

- `consensus-guard-core` 是一个第一方的共识包
- 版本在 `package.json` 中使用 semver 进行固定，以确保可重复的安装
- 该技能不请求全局权限，也不会修改其他技能
- 注意：对于依赖的第三方包，其依赖关系树需要由使用者单独进行审计

## 安装

```bash
npm i consensus-guard-core
```

## 快速入门

```bash
npm test
```

## 导入合约

使用包的根目录进行导入（稳定的公共 API）：

```js
import { aggregateVotes, writeArtifact, resolveStatePath } from 'consensus-guard-core';
```

请勿在依赖的技能中导入内部路径（如 `consensus-guard-core/src/index.mjs`）。

## 工具调用集成

该技能通过共享的 `consensus-guard-core` 包装器与共识交互合约（consensus-interact contract）进行集成（在适用的情况下）：
- `readBoardPolicy`
- `getLatestPersonaSet` / `getPersonaSet`
- `writeArtifact` / `writeDecision`
- 幂等性决策查找功能

这确保了董事会编排在不同技能之间的标准化。

## 调用合约

该技能提供了一个标准的入口点：

- `invoke(input, opts?) -> Promise<OutputJson | ErrorJson>`

`invoke()` 仅处理基本数据类型，并将控制权委托给调用者提供的处理函数。它不负责生成 persona 或调用模型/提供者。

另请参阅：`SECURITY-ASSURANCE.md`，以了解威胁模型、运行时边界和安全性加固指南。