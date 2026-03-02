---
name: consensus-agent-action-guard
description: 针对高风险代理操作的预执行治理机制：在产生外部影响或不可逆的副作用之前，该机制通过基于角色权重的共识机制来决定是否允许（ALLOW）、阻止（BLOCK）或要求重新编写（REQUIRE_REWRITE）相关操作，并生成由董事会管理的审计记录（audit artifacts）。
version: 1.1.13
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
        package: consensus-agent-action-guard
        bins:
          - node
          - tsx
---
# consensus-agent-action-guard

`consensus-agent-action-guard` 是在执行自主操作之前的最后一道安全关卡。

## 该组件的功能

- 评估代理提出的操作（包括风险、不可逆性以及可能产生的副作用）；
- 应用硬性阻止（hard-block）和加权共识（weighted consensus）逻辑；
- 返回以下三种结果之一：`ALLOW`（允许操作）、`BLOCK`（阻止操作）或 `require_REWRITE`（要求重新编写操作脚本）；
- 触发必要的后续操作（例如，需要人工确认）；
- 将决策结果以及代理的个人信息更新写入到董事会的相关记录中。

## 重要性

大多数灾难性的自动化故障都发生在操作执行阶段。该组件通过在操作产生副作用之前实施明确的治理机制，有效防止了这些故障的发生。

## 在生态系统中的作用

该组件基于与通信和合并控制机制相同的共识框架构建，从而为所有代理操作提供统一的策略管理语言。

## 常见用途

- 控制可能造成破坏性的操作；
- 管理外部消息发送或发布行为；
- 对于高风险且不可逆的操作，要求人工确认。

## 运行时环境、权限需求及网络行为

- 运行时使用的二进制文件：`node`、`tsx`；
- 在该组件的决策过程中不涉及任何网络调用；
- 文件系统写入操作：将决策结果及代理信息保存到配置好的共识状态路径下的文件中。

## 依赖关系管理

- `consensus-guard-core` 是该组件执行过程中使用的核心共识库；
- 该组件的版本信息通过 `package.json` 中的 semver 标签进行固定，以确保可重复的安装；
- 该组件不会请求系统的全局权限，也不会修改其他组件的状态。

## 快速入门

```bash
node --import tsx run.js --input ./examples/input.json
```

## 与其他组件的集成

该组件与共识交互合约（consensus-interact）进行了集成（在适用的情况下，通过共享的 `consensus-guard-core` 封装器进行交互）：
- `readBoardPolicy`：读取董事会的策略配置；
- `getLatestPersonaSet`/`getPersonaSet`：获取代理的个人信息集合；
- `writeArtifact`/`writeDecision`：将决策结果写入记录；
- 提供幂等的决策查询功能。

这样的设计确保了不同组件之间的协同工作更加标准化。

## 调用接口

该组件提供了一个标准的调用接口：
```javascript
invoke(input, opts?) -> Promise<OutputJson | ErrorJson>
```
`invoke()` 函数会启动决策流程，并通过共享的 `consensus-guard-core` 封装器与董事会的操作进行交互，以执行明确的策略评估。

## 外部代理模式（external_agent mode）

该组件支持两种运行模式：
- `mode="external_agent"`：调用者需要提供来自代理、人类用户或模型的 `external_votes` 数组，以便进行统一的决策计算；
- `mode="persona"`：该模式下系统会使用已存在的 `persona_set_id`，不会自行生成新的个人信息集合。