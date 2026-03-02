---
name: consensus-permission-escalation-guard
description: >
  **IAM（身份与访问管理）及权限升级变更的预执行治理机制**  
  当代理或工作流提议授予、扩展或使用更高权限时，本机制可确保决策过程具有确定性（即“允许/拒绝/要求重写”），同时提供严格的模式验证、幂等性（即多次执行相同操作的结果相同），以及基于董事会的审计记录。
homepage: https://github.com/kaicianflone/consensus-permission-escalation-guard
source: https://github.com/kaicianflone/consensus-permission-escalation-guard
upstream:
  consensus-guard-core: https://github.com/kaicianflone/consensus-guard-core
---
# consensus-permission-escalation-guard

`consensus-permission-escalation-guard` 是在权限提升被应用之前的最后一道安全关卡。

## 该组件的功能

- 根据严格的输入规范验证权限提升请求（拒绝未知字段）；
- 评估与身份和访问管理（IAM）风险相关的硬阻止（hard-block）策略和重写策略（rewrite policy）；
- 执行基于用户角色加权的投票（或汇总外部投票结果）；
- 返回以下三种结果之一：`ALLOW`（允许权限提升）、`BLOCK`（拒绝权限提升）或 `REQUIRE_REWRITE`（需要重写权限提升策略）；
- 生成用于回放和审计的决策记录。

## 决策策略示例

**硬阻止（hard-block）的情况：**
- 使用通配符权限（`*`、`: *`）；
- 在需要时缺少工单引用；
- 未经事件记录的紧急权限提升请求；
- 职责分离冲突（例如，同时拥有创建和批准权限）。

**需要重写权限提升策略（rewrite policy）的情况：**
- 提供的权限提升理由不充分或不可执行；
- 权限提升的临时持续时间超过政策规定的限制；
- 生产环境中的权限提升请求需要明确的人工确认。

## 运行时和安全模型

- 运行时使用的二进制文件：`node`、`tsx`；
- 无需提供任何凭据；
- 该组件在运行时不会影响网络行为；
- 该组件会读取以下环境配置文件：`CONSENSUS_STATE_FILE`、`CONSENSUS_STATE_ROOT`；
- 该组件会将决策结果写入配置好的状态路径下的文件系统中。

## 调用该组件的方式

- `invoke(input, opts?) -> Promise<OutputJson | ErrorJson>`

**调用模式：**
- `mode="persona"`（默认）：使用本地默认的用户角色信息进行内部投票；
- `mode="external_agent"`：读取外部投票结果（`external_votes[]`），然后汇总并严格执行相应的策略。

## 安装方法

```bash
npm i consensus-permission-escalation-guard
```

## 快速入门指南

```bash
node --import tsx run.js --input ./examples/input.json
```

## 测试内容

测试内容包括：验证输入数据的格式是否符合规范、检查是否存在硬阻止的情况、验证权限提升请求是否需要重写策略、测试权限提升请求是否被允许，以及检查外部投票结果的汇总行为。

**注意：**  
该组件依赖于 `consensus-guard-core` 来提供汇总和状态管理功能。请同时查看该组件，以确保整个系统的运行时可审计性。

**另请参阅：**  
`SECURITY-ASSURANCE.md`，以了解威胁模型、运行时边界和部署安全加固指南。