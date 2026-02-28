---
name: consensus-send-email-guard
description: 针对AI系统的“基于角色权重”的预发送邮件管理机制：该机制能够生成“批准/阻止/重写”等决策结果，将这些决策记录写入董事会的账本中，逐步更新相关角色的声誉，并返回格式严格、可供机器解析的JSON数据。
homepage: https://github.com/kaicianflone/consensus-send-email-guard
source: https://github.com/kaicianflone/consensus-send-email-guard
metadata:
  {"openclaw": {"requires": {"bins": ["node", "tsx"], "env": ["OPENAI_API_KEY"]}}}
---
# consensus-send-email-guard

`consensus-send-email-guard` 是一个用于管理外部通信流程的守护机制（outbound communication guardrail），适用于生产环境。

## 功能概述

- 使用角色评估模型（persona panel）对邮件草稿进行审核；
- 根据用户的声誉（reputation）对投票结果进行加权汇总；
- 遵循严格的规则来阻止某些类型的邮件发送（例如：敏感数据、法律/医疗相关的信息、不可接受的承诺等）；
- 返回最终决策结果：`APPROVE`（批准）、`BLOCK`（阻止）或 `REWRITE`（重写邮件内容）；
- 将决策结果以及更新后的 `persona_set` 数据写入系统状态。

## 重要性

电子邮件一旦发送，其影响巨大且不可撤销。该机制能够在引发外部问题之前，及时发现并阻止不真实或违反政策的言论。

## 在生态系统中的位置

在技术架构中，它的位置如下：
`consensus-tools -> consensus-interact pattern -> persona_set -> send-email-guard`

它将原始生成的邮件内容转化为经过审核、符合规定的发送行为。

## 管理与学习机制

- 采用严格的 JSON 合同来规范自动化流程；
- 实现幂等重试机制，以避免重复修改用户声誉数据；
- 声誉值的更新会随着时间的推移逐渐调整评估模型的权重。

## 使用场景

- 面向客户的对外沟通；
- 涉及合作伙伴或法律敏感信息的通信；
- 自动化营销活动的质量审核。

## 运行时环境、凭证及网络行为

- 运行时使用的二进制文件：`node`、`tsx`；
- 在决策过程中不涉及网络调用；
- 如果需要生成用户角色信息，且相关后端使用了外部大型语言模型（LLM），则该后端可能会执行外部 API 调用；
- 凭证要求：在基于 LLM 的场景中，可能需要 `OPENAI_API_KEY`（或类似的服务密钥）来生成用户角色信息；如果提供了 `persona_set_id`，则无需 LLM 凭证即可运行该机制；
- 数据存储：将结果写入配置好的系统状态路径下的文件系统中。

## 依赖关系管理

- `consensus-guard-core` 和 `consensus-persona-generator` 是属于同一方的核心组件；
- 版本信息通过 `package.json` 的 semver 标签进行固定，以确保可重复的安装；
- 该机制不会请求系统的全局权限，也不会修改其他组件的状态。

## 快速入门

```bash
node --import tsx run.js --input ./examples/email-input.json
```

## 与其他组件的集成

该机制通过以下接口与 `consensus-interact` 模块进行集成：
- `readBoardPolicy`：读取系统策略；
- `getLatestPersonaSet`/`getPersonaSet`：获取最新的用户角色信息；
- `writeArtifact`/`writeDecision`：写入决策结果和更新后的角色信息；
- 提供幂等的决策查询功能。

这些接口确保了不同组件之间的操作能够标准化。

## 调用方式

该机制提供了一个标准的调用接口：
`invoke(input, opts?) -> Promise<OutputJson | ErrorJson>`

`invoke()` 函数用于启动整个处理流程，包括角色评估以及与 `consensus-interact` 模块的交互操作。

## 外部代理模式（external_agent mode）

该机制支持两种运行模式：
- `mode="persona"`（默认模式）：自动加载/生成用户角色信息并执行内部投票；
- `mode="external_agent"`：调用者提供来自外部代理的投票结果（`external_votes[]`），机制会直接进行投票汇总、政策检查并生成最终决策，无需依赖外部角色生成服务。