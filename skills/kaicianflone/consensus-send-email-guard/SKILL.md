---
name: consensus-send-email-guard
description: 针对AI系统的“基于用户画像（Persona）的预发送邮件管理机制”：该机制能够生成“批准（APPROVE）/阻止（BLOCK）/重写（REWRITE）”等决策结果，将这些决策记录写入董事会的账本（board ledger），并返回格式严格、可供机器解析的JSON数据。
version: 1.1.14
homepage: https://github.com/kaicianflone/consensus-send-email-guard
source: https://github.com/kaicianflone/consensus-send-email-guard
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
        package: consensus-send-email-guard
---
# consensus-send-email-guard

`consensus-send-email-guard` 是一个用于管理外部通信流程的工具，适用于生产环境。

## 功能概述

- 使用角色评估机制（persona panel）来审核邮件草稿；
- 根据用户的声誉（采用加权审批策略）来汇总投票结果；
- 禁止发送某些类别的邮件（如包含敏感数据、法律/医疗相关内容或不符合规定的保证声明）；
- 返回最终决策结果：`APPROVE | BLOCK | REWRITE`；
- 将决策结果写入到系统状态中。

## 重要性

电子邮件一旦发送，其影响巨大且不可撤销。该工具能够在产生外部副作用之前，及时发现并阻止不实承诺或违反政策的言论。

## 在生态系统中的位置

在技术架构中，它的位置如下：
`consensus-tools -> consensus-interact pattern -> persona_set -> send-email-guard`

该工具将原始生成的邮件内容转化为经过审核的、符合规定的发送行为。

## 管理与学习机制

- 采用严格的 JSON 合同来规范自动化流程；
- 实现幂等重试机制，以防止声誉数据被重复修改；
- 声誉值的更新会随着时间的推移逐渐调整评估者的影响力。

## 使用场景

- 面向客户的对外沟通邮件；
- 需要严格遵守法律或合作伙伴规定的敏感信息交流；
- 自动化处理营销活动内容的审核。

## 运行时环境与权限需求

- 运行时使用的二进制文件：`node`、`tsx`；
- 该工具的决策逻辑中不涉及网络调用；
- 该工具会读取以下配置文件：`CONSENSUS_STATE_FILE`、`CONSENSUS_STATE_ROOT`；
- 写入的文件位于配置好的共识状态路径下。

## 依赖关系与安全模型

- `consensus-guard-core` 是该工具执行过程中依赖的核心共识包；
- 所有版本都会在 `package.json` 中明确标注版本号，以确保可重复安装；
- 该工具不会请求系统的全局权限，也不会修改其他工具的状态。

## 安装方法

```bash
npm i consensus-send-email-guard
```

## 快速上手指南

```bash
node --import tsx run.js --input ./examples/email-input.json
```

## 与其他工具的集成

该工具通过共享的 `consensus-guard-core` 接口与以下工具进行集成：
- `readBoardPolicy`：读取董事会政策；
- `getLatestPersonaSet`/`getPersonaSet`：获取当前的角色集合；
- `writeArtifact`/`writeDecision`：写入决策结果；
- `idempotentDecisionLookup`：实现幂等的决策查询功能。

这些接口确保了不同工具之间的协调一致性。

## 调用方式

该工具提供了一个标准的调用接口：
`invoke(input, opts?) -> Promise<OutputJson | ErrorJson>`

`invoke()` 函数用于启动通信审核流程，并通过共享的 `consensus-guard-core` 接口与董事会操作协同执行决策评估。

## 外部代理模式（external_agent mode）

该工具支持两种运行模式：
- `mode="external_agent"`：调用者提供来自外部代理、人类用户或模型的投票数据，以便进行精确的投票汇总；
- `mode="persona"`：需要预先存在的 `persona_set_id`；此时工具不会自动生成角色集合。