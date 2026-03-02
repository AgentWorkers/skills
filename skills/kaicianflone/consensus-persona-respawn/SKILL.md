---
name: consensus-persona-respawn
description: 基于Ledger数据的角色生命周期管理机制：通过分析董事会决策历史中的错误模式，用新的角色替换表现不佳的角色，从而确保长期自动化流程中的治理机制能够持续适应变化。角色的声誉更新由共识角色引擎（Consensus-Persona-Engine）负责计算。
version: 1.1.13
homepage: https://github.com/kaicianflone/consensus-persona-respawn
source: https://github.com/kaicianflone/consensus-persona-respawn
upstream:
  consensus-guard-core: https://github.com/kaicianflone/consensus-guard-core
requires:
  bins:
    - node
    - tsx
  env:
    - CONSENSUS_STATE_FILE
    - CONSENSUS_STATE_ROOT
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
      - kind: node
        package: consensus-persona-respawn
---
# consensus-persona-respawn

`consensus-persona-respawn` 是一个用于 persona（角色）管理的自适应维护工具。

## 功能概述

- 通过触发条件或声誉阈值来识别失效/表现不佳的 persona；
- 从历史决策记录中挖掘错误模式；
- 根据这些错误情况生成新的 persona 配置文件；
- 更新 `persona_respawn` 和 `persona_set` 等相关文件；
- 防止治理流程的质量停滞不前。

## 重要性

静态的评估面板会随着时间的推移而失效；该工具通过实现 persona 的生命周期管理，确保治理质量得以提升而非下降。

## 在生态系统中的作用

该工具会利用 persona 引擎的输出数据进行长期适应性调整，并与董事会的记录系统（board-ledger）直接关联。

## 最适合的应用场景

- 长期运行的代理团队；
- 需要反复做出决策且经常出现错误的领域；
- 需要定期维护评估机制的自主系统。

## 运行时和网络行为

- 运行时使用的二进制文件：`node`、`tsx`；
- 该工具的逻辑中不涉及任何网络调用；
- 该工具读取的环境配置文件：`CONSENSUS_STATE_FILE`、`CONSENSUS_STATE_ROOT`；
- 该工具会将更新后的数据写入文件系统（位于配置的共识状态路径下）。

## 依赖关系管理

- `consensus-guard-core` 是运行时执行所依赖的核心共识包；
- 该工具的版本信息在 `package.json` 中使用 semver 标签进行固定，以确保可重复的安装；
- 该工具不会请求系统的全局权限，也不会修改其他工具的功能。

## 安装方法

```bash
npm i consensus-persona-respawn
```

## 快速入门

```bash
node --import tsx run.js --input ./examples/input.json
```

## 与其他工具的集成

该工具与共识交互框架（consensus-interact）进行了集成（通过共享的 `consensus-guard-core` 封装器）：
- 提供 `readBoardPolicy`、`getLatestPersonaSet`、`writeArtifact`、`writeDecision` 等接口；
- 支持幂等的决策查询功能。

这些集成确保了不同工具之间的协同工作更加标准化。

## 调用接口

该工具提供了一个标准的接口：
- `invoke(input, opts?) -> Promise<OutputJson | ErrorJson>`

`invoke()` 函数根据 persona 的历史记录和错误模式来执行替换操作。该函数会从 `consensus-persona-engine` 的输出中获取声誉变化数据。