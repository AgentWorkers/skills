---
name: consensus-deployment-guard
description: 发布及基础设施部署请求的预部署治理机制。当代理或工作流程提议将代码、配置或基础设施变更推送至测试环境（staging）或生产环境（production）时，该机制可确保决策过程具有确定性（允许/禁止/要求重写），同时提供严格的模式验证（schema validation）、幂等性（idempotency）以及由董事会直接管理的审计记录（board-native audit artifacts）。
homepage: https://github.com/kaicianflone/consensus-deployment-guard
source: https://github.com/kaicianflone/consensus-deployment-guard
upstream:
  consensus-guard-core: https://github.com/kaicianflone/consensus-guard-core
---
# consensus-deployment-guard

`consensus-deployment-guard` 是部署执行前的最后一道安全关卡。

## 功能概述

- 根据严格的 JSON 模式验证部署请求（拒绝未知字段）；
- 评估与发布风险相关的硬阻止（hard-block）和重写策略（rewrite policy）标志；
- 执行基于角色权重的投票（ persona-weighted voting）或汇总外部投票结果；
- 返回以下三种决策之一：`ALLOW`、`BLOCK` 或 `require_REWRITE`；
- 生成用于回放/审计的决策记录。

## 决策策略示例

**硬阻止（Hard-block）情况：**
- 必须通过的测试未通过；
- 持续集成（CI）状态失败；
- 在需要时缺少回滚所需的文件；
- 模式迁移不兼容；
- 错误预算已被超出。

**重写策略（Rewrite policy）情况：**
- 生产环境部署未使用“金丝雀测试”（canary test）（尽管策略要求使用）；
- 初始部署的比例超过了策略规定的限制；
- 生产环境部署缺少明确的人工确认步骤；
- 持续集成（CI）流程仍在进行中；
- 模式兼容性未知。

## 运行时与安全模型

- 运行时使用的二进制文件：`node`、`tsx`；
- 不需要任何凭据；
- 该组件不涉及任何网络行为；
- 该组件读取的环境配置文件：`CONSENSUS_STATE_FILE`、`CONSENSUS_STATE_ROOT`；
- 文件系统写入操作：将决策结果写入配置好的状态路径下的文件中。

## 合同调用方式

- `invoke(input, opts?) -> Promise<OutputJson | ErrorJson>`

**调用模式：**
- `mode="persona"`（默认）：使用本地预设的角色权重进行内部投票；
- `mode="external_agent"`：读取外部投票结果（`external_votes[]`），进行汇总并执行策略规定。

## 安装方法

```bash
npm i consensus-deployment-guard
```

## 快速入门指南

```bash
node --import tsx run.js --input ./examples/input.json
```

## 测试内容

测试内容包括：模式验证、硬阻止情况、重写情况、允许情况、幂等重试机制以及外部代理的汇总行为。

**另请参阅：** `SECURITY-ASSURANCE.md`，以了解威胁模型、运行时限制和部署安全加固指南。