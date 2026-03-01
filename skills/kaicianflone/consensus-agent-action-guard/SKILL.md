---
name: consensus-agent-action-guard
description: 针对高风险代理操作的预执行治理机制：在引发外部影响或不可逆的副作用之前，该机制采用基于角色权重（persona-weighted consensus）的共识机制来决定是否允许（ALLOW）、阻止（BLOCK）或要求重新编写（REQUIRE_REWRITE）相关操作，并生成由董事会直接管理的审计记录（audit artifacts）。
homepage: https://github.com/kaicianflone/consensus-agent-action-guard
source: https://github.com/kaicianflone/consensus-agent-action-guard
metadata:
  {"openclaw": {"requires": {"bins": ["node", "tsx"]}}}
---
# consensus-agent-action-guard

`consensus-agent-action-guard` 是在执行自主操作之前的最后一道安全关卡。

## 该组件的功能

- 评估提议的代理操作（包括风险、不可逆性以及可能产生的副作用）；
- 应用严格的阻止规则和基于权重的共识机制；
- 返回以下三种结果之一：`ALLOW`（允许执行）、`BLOCK`（阻止执行）或 `require_REWRITE`（需要重新编写操作）；
- 触发必要的后续操作（例如，请求人工确认）；
- 将决策结果以及相关的人员信息更新写入到董事会的记录系统中。

## 重要性

大多数灾难性的自动化故障都发生在执行阶段。该组件通过在操作执行前实施明确的治理机制来防止潜在问题。

## 在生态系统中的作用

该组件基于与通信和合并控制组件相同的共识框架构建，从而为所有代理操作提供统一的策略管理机制。

## 常见用途

- 控制可能具有破坏性的操作；
- 管理对外部消息的发送或发布；
- 对于高风险且不可逆的操作，要求人工确认。

## 运行时环境、权限要求及网络行为

- 运行时使用的二进制文件：`node`、`tsx`；
- 在该组件的决策过程中不涉及任何网络调用；
- 不需要任何特殊权限；
- 所有数据写入操作都会保存到配置好的董事会状态存储路径中。

## 依赖关系管理

- `consensus-guard-core` 是该组件在执行过程中依赖的核心共识模块；
- 所有版本信息都会在 `package.json` 中明确标注，以确保可重复的安装；
- 该组件不会请求系统的全局权限，也不会修改其他组件的行为。

## 快速入门

```bash
node --import tsx run.js --input ./examples/input.json
```

## 与其他组件的集成

该组件通过共享的 `consensus-guard-core` 接口与其他组件进行交互：
- `readBoardPolicy`：读取董事会的策略信息；
- `getLatestPersonaSet`/`getPersonaSet`：获取当前的人员信息；
- `writeArtifact`/`writeDecision`：将决策结果写入记录系统；
- 提供幂等的决策查询功能。

这些接口确保了不同组件之间的协调一致性。

## 调用方式

该组件提供了一个标准的接口：
- `invoke(input, opts?) -> Promise<OutputJson | ErrorJson>`：该接口用于启动决策流程，并通过共享的 `consensus-guard-core` 接口与董事会操作进行交互。

## 外部代理模式

该组件支持两种运行模式：
- `mode="external_agent"`：调用者需要提供来自代理、人类用户或模型的投票结果，以便进行统一的决策；
- `mode="persona"`：此时需要提供一个已存在的人员信息 ID；该组件不会自行生成人员信息。