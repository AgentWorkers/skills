---
name: consensus-support-reply-guard
description: 基于角色权重的共识机制，实现风险意识强的支持响应管理。能够识别法律/敏感/保密性问题，执行严格的策略检查，并生成可供审计的决策记录，以支持面向客户的自动化流程。
version: 1.1.14
homepage: https://github.com/kaicianflone/consensus-support-reply-guard
source: https://github.com/kaicianflone/consensus-support-reply-guard
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
        package: consensus-support-reply-guard
        bins:
          - node
          - tsx
---
# consensus-support-reply-guard

`consensus-support-reply-guard` 是一个用于保护支持工作流程的客户信任机制（customer-trust guard）。

## 功能概述

- 在发送支持回复之前对回复内容进行评估
- 检测可能存在的高风险行为或违规模式
- 当发现政策违规时，阻止或重写回复内容
- 根据最终决策结果更新相关人员的声誉
- 将决策历史记录保存在董事会的文档中

## 重要性

支持回复的频率很高，且对品牌形象至关重要。该机制能够有效防止因过度自信而导致的法律或个人隐私（PII）相关错误。

## 在生态系统中的角色

该机制通过与共识董事会的状态（consensus board state）协同工作，利用明确的投票输入和确定的决策规则来确保流程的规范性。

## 适用场景

- 自动化工单分类与回复处理
- 一级/二级人工智能（L1/L2 AI）的回复审核流程
- 受监管或企业级的支持渠道

## 运行时环境、所需权限及网络行为

- 运行时使用的二进制文件：`node`、`tsx`
- 该机制的决策过程中不涉及任何网络调用
- 文件系统写入操作：将决策结果保存在配置好的董事会状态路径下的文档中

## 依赖关系

- `consensus-guard-core` 是执行该机制时所依赖的核心组件
- 所有版本信息均通过 `package.json` 中的 semver 标签进行固定，以确保可重复的安装
- 该机制不会请求系统的全局权限，也不会修改其他组件

## 快速入门

```bash
node --import tsx run.js --input ./examples/input.json
```

## 与其他组件的集成

该机制通过共享的 `consensus-guard-core` 接口与共识系统进行交互：
- `readBoardPolicy`：读取董事会政策信息
- `getLatestPersonaSet` / `getPersonaSet`：获取相关人员的信息
- `writeArtifact` / `writeDecision`：写入决策记录
- 提供幂等的决策查询功能

这些接口确保了不同组件之间的操作标准化。

## 调用方式

该机制提供了一个标准的调用接口：
- `invoke(input, opts?) -> Promise<OutputJson | ErrorJson>`

`invoke()` 函数用于启动决策流程，并通过共享的 `consensus-guard-core` 接口与董事会操作协同执行决策评估。

## 外部代理模式（external_agent mode）

该机制支持两种调用模式：
- `mode="external_agent"`：调用者提供来自外部代理、人类操作员或模型的投票数据，以便进行统一的决策处理
- `mode="persona"`：需要预先存在的 `persona_set_id`；该机制不会自行生成人员信息