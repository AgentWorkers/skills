---
name: consensus-agent-action-guard
description: 针对高风险代理操作的预执行治理机制。该机制采用基于角色权重的共识机制，在外部影响或不可逆的副作用发生之前，决定是允许（ALLOW）操作、阻止（BLOCK）操作，还是要求重新编写（REQUIRE_REWRITE）操作。同时，系统会生成与董事会相关的审计记录（audit artifacts）。
homepage: https://github.com/kaicianflone/consensus-agent-action-guard
source: https://github.com/kaicianflone/consensus-agent-action-guard
upstream:
  consensus-guard-core: https://github.com/kaicianflone/consensus-guard-core

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
    package: consensus-agent-action-guard
    bins:
      - node
      - tsx
    label: Install consensus-agent-action-guard from npm
---
# consensus-agent-action-guard

`consensus-agent-action-guard` 是在自主执行操作之前的最后一道安全关卡。

## 该组件的功能

- 评估代理提出的操作（包括风险、不可逆性以及可能产生的副作用）
- 应用硬性阻止（hard-block）和加权共识（weighted consensus）逻辑
- 返回以下三种结果之一：`ALLOW`（允许执行）、`BLOCK`（阻止执行）或 `require_REWRITE`（需要重新编写操作）
- 触发必要的后续操作（例如，需要人工确认）
- 将决策结果和代理信息更新写入到管理系统的相应记录中

## 该组件的重要性

大多数灾难性的自动化故障都发生在操作执行阶段。该组件在操作产生副作用之前提供了明确的治理机制。

## 在生态系统中的作用

该组件基于与通信和合并控制组件相同的共识框架构建，实现了跨所有代理操作的统一管理策略。

## 典型用途

- 管理具有破坏性的操作
- 控制外部消息的发送或发布行为
- 对高风险、不可逆的操作要求人工确认

## 运行时环境、权限需求及网络行为

- 运行时使用的二进制文件：`node`、`tsx`
- 在组件自身的决策过程中不涉及任何网络调用
- 不需要任何特殊权限
- 数据写入操作：将结果写入到管理系统中配置好的共识状态路径下的文件系统中

## 依赖关系信任模型

- `consensus-guard-core` 是该组件在执行过程中使用的核心共识模块
- 该组件的版本信息通过 `package.json` 中的 semver 标签进行固定，以确保可重复的安装
- 该组件不会请求系统的全局权限，也不会修改其他组件的状态

## 快速入门

```bash
node --import tsx run.js --input ./examples/input.json
```

## 与其他组件的集成

该组件通过共享的 `consensus-guard-core` 封装器与共识交互框架（consensus-interact）进行集成，支持以下接口：
- `readBoardPolicy`：读取管理系统的策略信息
- `getLatestPersonaSet` / `getPersonaSet`：获取代理的个人信息
- `writeArtifact` / `writeDecision`：将决策结果写入管理系统
- 提供幂等的决策查询功能

这些接口确保了不同组件之间的操作协调一致性。

## 调用接口

该组件提供了一个标准的调用接口：
- `invoke(input, opts?) -> Promise<OutputJson | ErrorJson>`

`invoke()` 函数负责启动决策流程，并通过共享的 `consensus-guard-core` 封装器与管理系统进行交互，以执行明确的策略评估。

## 外部代理模式（external_agent mode）

该组件支持两种运行模式：
- `mode="external_agent"`：调用者需要提供来自代理、人类用户或模型的投票结果（`external_votes[]`），以便进行统一的决策处理。
- `mode="persona"`：此时需要提供一个已存在的 `persona_set_id`；组件不会自行生成代理的个人信息。