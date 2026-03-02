---
name: consensus-persona-generator
description: 生成并保存可重用的角色面板（persona_set artifacts），以支持共识决策工作流程。该功能用于为下游的审核人员（guards）初始化评估者的多样性；角色的持续声誉更新由共识角色引擎（consensus-persona-engine）负责管理。
version: 1.1.14
homepage: https://github.com/kaicianflone/consensus-persona-generator
source: https://github.com/kaicianflone/consensus-persona-generator
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
        package: consensus-persona-generator
---
# consensus-persona-generator

`consensus-persona-generator` 是 Consensus.Tools 生态系统中用于确保评估者多样性的核心组件。

## 功能概述

- 创建 N 个具有不同决策特征的评估者角色（包括角色、偏见、风险态度和投票风格）；
- 为这些评估者分配初始的声誉值（这些声誉值会由 `consensus-persona-engine` 持续更新）；
- 将这些评估者的信息以版本化的形式保存到系统的状态存储中；
- 在可能的情况下重用现有的评估者角色集，以减少系统的不稳定性。

## 重要性

大多数自动化流程失败的原因在于某个模型会自我批准自己的输出结果。`consensus-persona-generator` 的作用是首先引入结构化的分歧意见，从而为后续的多视角审查提供依据。

## 在生态系统中的位置

在 Consensus.Tools 生态系统中，该组件的层级结构如下：
```
consensus-tools -> consensus-interact pattern -> consensus-persona-generator -> domain guards -> consensus-persona-engine
```
- **consensus-tools**：负责管理董事会、任务和提交流程的基础组件；
- **consensus-interact**：提供董事会级别的协调服务；
- **persona-generator**：负责初始化多个评估者角色的轻量级模块；
- **persona-engine**：负责更新评估者的声誉值并管理他们的角色生命周期。

## 输入/输出格式（支持自动化）

- 输入数据为严格的 JSON 格式，包含 `board_id`、`task_context`、`n_personas` 等参数；
- 输出数据同样为严格的 JSON 格式，包含 `persona_set_id`、`personas[]` 以及用于更新系统状态的引用信息；
- 在可行的情况下，确保行为具有确定性和可重现性。

## 常见应用场景

- 为负责邮件处理、发布、支持、合并或执行操作的评估者角色生成初始数据；
- 根据领域或风险特征重新生成评估者角色集；
- 为长期运行的自动化流程创建可重复使用的治理角色模型。

## 运行时要求、权限及网络交互

- 运行时使用的二进制文件包括 `node` 和 `tsx`；
- 该组件本身不涉及任何网络调用；
- 需要读取的环境配置文件包括 `CONSENSUS_STATE_FILE` 和 `CONSENSUS_STATE_ROOT`；
- 所有数据都会写入到系统配置的共识状态路径下的文件系统中。

## 依赖关系

- 该组件的运行时依赖项为 `consensus-guard-core`；
- 通过 `package.json` 中的 semver 版本管理来确保依赖关系的稳定性；
- 该组件不会请求全局系统权限，也不会修改其他组件的状态。

## 安装方法

```bash
npm i consensus-persona-generator
```

## 快速入门指南

```bash
node --import tsx run.js --input ./examples/persona-input.json
```

## 与其他组件的集成方式

该组件通过 `consensus-guard-core` 的接口与其它组件进行交互：
- 可以调用 `readBoardPolicy`、`getLatestPersonaSet`、`writeArtifact` 和 `writeDecision` 等方法；
- 这些方法确保了不同组件之间的协调一致性。

## 调用接口

该组件提供了一个标准的接口：
```javascript
invoke(input, opts?) -> Promise<OutputJson | ErrorJson>
```
`invoke()` 方法用于初始化或重用评估者角色集，并通过 `consensus-guard-core` 的接口执行董事会相关的操作。它本身不负责更新评估者的声誉值，这些操作由 `consensus-persona-engine` 负责完成。