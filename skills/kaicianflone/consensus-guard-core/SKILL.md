---
name: consensus-guard-core
description: Shared deterministic guard primitives for the Consensus.Tools skill family: hard-block taxonomy, weighted vote aggregation, reputation updates, idempotency keys, strict schema enforcement, and indexed board artifact access.
homepage: https://github.com/kaicianflone/consensus-guard-core
source: https://github.com/kaicianflone/consensus-guard-core
requires:
  bins:
    - node
    - tsx
  env:
    - CONSENSUS_STATE_FILE
    - CONSENSUS_STATE_ROOT
install:
  - id: npm
    kind: node
    package: consensus-guard-core
    bins:
      - node
      - tsx
    label: Install consensus-guard-core from npm
metadata:
  openclaw:
    requires:
      bins:
        - node
        - tsx
      env:
        - CONSENSUS_STATE_FILE
        - CONSENSUS_STATE_ROOT
    install:
      - id: npm
        kind: node
        package: consensus-guard-core
        bins:
          - node
          - tsx
        label: Install consensus-guard-core from npm
---

# consensus-guard-core

`consensus-guard-core` 是 Consensus Guard 生态系统中通用的策略引擎。

## 该技能/包提供的功能

- 统一的硬性规则分类体系（hard-block taxonomy）
- 确定的 `aggregateVotes()` 策略函数
- 具有限制机制的确定性声誉更新规则（deterministic reputation update rules with clamping）
- 用于确保重试安全性的幂等性密钥生成机制（idempotent key generation for retry-safe execution）
- 用于严格验证未知字段的辅助函数
- 用于高效查找工件（artifact）的索引化辅助函数

## 重要性

如果没有一个统一的核心框架，各个组件之间的策略逻辑可能会变得不兼容。该包确保了各个组件的行为一致性、可重放性以及跨领域的可比性。

## 在生态系统中的作用

`consensus-guard-core` 被 publish、support、merge、action 等组件所使用，应被视为策略基础设施，而非面向最终用户的工作流技能。

## 对大型语言模型（LLM）编排的好处

- 降低集成风险（lower integration drift）
- 确保不同工作流中的决策语义一致性（consistent decision semantics across workflows）
- 便于审计和跨技能分析（easier auditing and cross-skill analytics）

## 运行时、凭证和网络行为

- 运行时二进制文件：`node`、`tsx`
- 该包的核心决策/路径辅助函数不涉及任何网络调用（network calls not involved）
- 该包不要求任何凭证（credentials not required）
- 该包读取的环境配置文件：`CONSENSUS_STATE_FILE`、`CONSENSUS_STATE_ROOT`（用于解析工作板状态路径）
- 当调用者使用写入辅助函数（如 `writeArtifact`）时，数据会写入配置的共识状态路径下的文件系统中

## 依赖关系信任模型

- `consensus-guard-core` 是一个第一方的共识包（first-party consensus package）
- 版本信息通过 `package.json` 中的 semver 标签进行固定，以确保可重复的安装（versions are semver-pinned in `package.json` for reproducible installs）
- 该技能不请求全局权限（does not request host-wide privileges），也不会修改其他组件
- 注意：对于依赖该包的第三方组件，应单独审核其依赖关系树（note: Dependency trees should be audited separately by consumers for transitive packages）

## 快速入门

```bash
npm test
```

## 工具调用集成

该技能与共识交互契约（consensus-interact contract）的边界进行了集成（通过共享的 `consensus-guard-core` 封装器实现）：
- `readBoardPolicy`
- `getLatestPersonaSet` / `getPersonaSet`
- `writeArtifact` / `writeDecision`
- 幂等性决策查询（idempotent decision lookup）

这确保了不同组件之间的工作流编排标准化。

## 调用契约（Invoke Contract）

该技能提供了一个标准的入口点：
- `invoke(input, opts?) -> Promise<OutputJson | ErrorJson>`

`invoke()` 函数仅处理基本操作，并将任务委托给调用者提供的处理程序。它不负责生成用户角色（persona）或调用模型/提供者（model/provider）。