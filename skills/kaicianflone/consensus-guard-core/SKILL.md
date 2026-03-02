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

- 统一的硬性规则分类体系（hard-block taxonomy）
- 确定的 `aggregateVotes()` 策略函数
- 具有限制机制的确定性声誉更新规则（deterministic reputation update rules with clamping）
- 用于确保重试安全性的幂等性密钥生成机制（idempotent key generation for retry-safe execution）
- 用于严格验证未知字段的辅助函数
- 用于高效查找工件（artifacts）的索引化辅助函数

## 重要性

如果没有一个统一的核心框架，每个组件都可能采用不兼容的策略逻辑。该包确保了各组件之间的行为一致性、可重放性以及可比较性。

## 在生态系统中的作用

`consensus-guard-core` 被 publish、support、merge、action 等组件所使用，应被视为策略基础设施，而非面向最终用户的工作流程工具。

## 对大型语言模型（LLM）编排的好处

- 降低集成风险（lower integration drift）
- 确保不同工作流程中的决策语义一致性（consistent decision semantics across workflows）
- 便于审计和跨技能分析（easier auditing and cross-skill analytics）

## 运行时、凭证和网络行为

- 运行时二进制文件：`node`、`tsx`
- 该包的核心决策/路径辅助函数不涉及网络调用（network calls: none in this package’s core decision/path helpers）
- 该包不要求任何凭证（credentials: none required by this package）
- 该包读取的环境配置文件：`CONSENSUS_STATE_FILE`、`CONSENSUS_STATE_ROOT`（用于解析板状态路径）
- 当调用者使用写入辅助函数（例如 `writeArtifact`）时，数据会写入配置的共识状态路径下的文件系统中

## 依赖关系信任模型

- `consensus-guard-core` 是一个第一方的共识相关包（first-party consensus package）
- 版本通过 `package.json` 中的 semver 标签进行固定，以确保可重复的安装（versions are semver-pinned in `package.json` for reproducible installs）
- 该技能不请求全局权限，也不会修改其他技能的功能（this skill does not request host-wide privileges and does not mutate other skills）
- 注意：对于间接依赖的包，消费者需要单独审核其依赖关系树（note: Dependency trees should be audited separately by consumers for transitive packages）

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

该技能通过共享的 `consensus-guard-core` 封装器与共识交互合约（consensus-interact contract）进行集成（where applicable）：
- `readBoardPolicy`
- `getLatestPersonaSet` / `getPersonaSet`
- `writeArtifact` / `writeDecision`
- 幂等性决策查找（idempotent decision lookup）

这确保了各组件之间的板级编排标准化。

## 调用合约

该技能提供了一个标准的入口点：

- `invoke(input, opts?) -> Promise<OutputJson | ErrorJson>`

`invoke()` 仅处理原始数据，并将控制权委托给调用者提供的处理函数。它不负责生成用户角色（personas）或调用模型/提供者（model/provider）。