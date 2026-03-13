---
name: consensus-publish-guard
description: 基于用户身份（Persona）的治理机制，用于控制内容的发布方式（包括博客、社交媒体和公告等）。通过严格的访问控制、加权共识机制、内容重写功能以及内置的审计工具，有效防止不安全的公开声明或不当行为的出现。
version: 1.1.15
homepage: https://github.com/kaicianflone/consensus-publish-guard
source: https://github.com/kaicianflone/consensus-publish-guard
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
        package: consensus-publish-guard
---
# consensus-publish-guard

`consensus-publish-guard` 负责在内容发布前对其进行审核，确保其符合公开发布的标准。

## 功能概述

- 通过多人共识机制审查内容草稿；
- 识别与政策、法律或高风险相关的问题；
- 决定内容是“批准”（APPROVE）、“阻止”（BLOCK）还是“重写”（REWRITE）；
- 在问题可解决的情况下生成重写后的代码补丁；
- 将决策结果保存到共识系统的状态数据库中。

## 重要性

公开发布的内容直接关系到品牌形象、法律合规性以及用户信任。通过多人共识机制进行审核，能够比单一流程更有效地确保内容的安全性。

## 在生态系统中的角色

该组件利用 `consensus-guard-core` 提供的确定性逻辑，以及通过共识系统收集的输入数据，来执行审核流程。

## 适用场景

- 适用于需要人工审核的 AI 辅助社交/媒体内容生成流程；
- 产品发布前的文本检查；
- 需要严格遵循政策规定的沟通材料。

## 运行时环境与权限要求

- 运行时使用的工具：`node`、`tsx`；
- 在审核过程中不涉及任何网络调用；
- 该组件会读取以下配置文件：`CONSENSUS_STATE_FILE`、`CONSENSUS_STATE_ROOT`；
- 审核结果会写入配置好的共识状态路径下的文件系统中。

## 依赖关系管理

- `consensus-guard-core` 是该组件执行审核功能所依赖的核心组件；
- 该组件的版本信息通过 `package.json` 中的 semver 标签进行固定，以确保可重复的安装；
- 该组件不会请求额外的系统权限，也不会修改其他组件的状态。

## 安装要求

当前，该组件的安装依赖于 `consensus-guard-core` 的本地副本。

```bash
# from repos/ directory
# repos/
#   consensus-guard-core/
#   consensus-publish-guard/
```

接下来，请在该仓库中安装所需的依赖项：

```bash
npm i
```

## 全局安装（通过包管理器）

```bash
npm i consensus-publish-guard
```

## 快速上手指南

```bash
node --import tsx run.js --input ./examples/input.json
```

## 与其他组件的集成

该组件与共识系统（consensus-interact）通过共享的 `consensus-guard-core` 接口进行集成，支持以下操作：
- `readBoardPolicy`：读取董事会的政策配置；
- `getLatestPersonaSet` / `getPersonaSet`：获取当前使用的角色集；
- `writeArtifact` / `writeDecision`：保存审核结果或更新决策内容；
- 提供幂等的决策查询功能。

这样的设计有助于确保所有组件之间的协同工作更加标准化。

## 调用方式

该组件提供了一个标准的接口：
- `invoke(input, opts?) -> Promise<OutputJson | ErrorJson>`：该接口用于启动审核流程，并通过共享的 `consensus-guard-core` 接口执行决策逻辑。

## 外部代理模式

该组件支持两种运行模式：
- `mode="external_agent"`：由外部代理（如人工审核者或模型）提供审核结果；
- `mode="persona"`：需要预先指定的 `persona_set_id`；此时组件不会自行生成角色集。