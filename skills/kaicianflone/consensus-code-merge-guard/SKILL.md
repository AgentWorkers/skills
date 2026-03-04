---
name: consensus-code-merge-guard
description: 基于用户偏好的合并管理机制，用于辅助人工智能驱动的工程开发。该机制会评估拉取请求（PR）的风险（包括测试结果、安全提示、可靠性指标等），并给出“合并（MERGE）”、“拒绝（BLOCK）”或“修改（REVISE”）的决策建议；同时还会记录与董事会相关的审计信息。
version: 1.1.14
homepage: https://github.com/kaicianflone/consensus-code-merge-guard
source: https://github.com/kaicianflone/consensus-code-merge-guard
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
        package: consensus-code-merge-guard
---
# consensus-code-merge-guard

`consensus-code-merge-guard` 将代码合并的审批过程转变为一个受管控、可审计的决策流程。

## 功能概述

- 接收 Pull Request（PR）或代码变更的摘要信息
- 执行基于用户角色的加权投票机制
- 强制执行某些硬性约束（例如测试、安全相关检查）
- 将审批结果映射到工程决策状态（`MERGE`、`BLOCK`、`REVISE`）
- 将决策结果及相关的用户角色信息写入到管理系统的状态数据库中

## 重要性

仅通过持续集成（CI）的流程并不能保证合并代码的质量；共识评审机制有助于防止潜在问题被悄悄地引入生产环境。

## 生态系统中的角色

该工具与其他管理工具使用相同的共识框架，从而实现跨领域的统一管理，并提供可比较的评估指标。

## 适用场景

- 自主或半自动化的代码合并流程
- 需要遵循特定政策的高风险代码仓库
- 需要保留代码变更历史记录的重复性发布流程

## 运行时环境、权限要求及网络交互

- 运行时依赖的程序：`node`、`tsx`
- 该工具的决策过程中不涉及任何网络调用
- 文件系统操作：将决策结果及用户角色信息写入到配置好的状态存储路径中

## 依赖关系管理

- `consensus-guard-core` 是该工具执行过程中使用的核心共识组件
- 所有依赖版本都通过 `package.json` 明确指定，以确保可重复的安装
- 该工具不会请求系统级别的权限，也不会修改其他工具的功能

## 安装（通过注册表）

```bash
npm i consensus-code-merge-guard
```

## 快速上手指南

```bash
node --import tsx run.js --input ./examples/input.json
```

## 与其他工具的集成

该工具与其他系统通过以下接口进行交互：
- `readBoardPolicy`：读取管理系统的政策配置
- `getLatestPersonaSet`/`getPersonaSet`：获取当前的用户角色信息
- `writeArtifact`/`writeDecision`：写入决策结果及用户角色信息
- 提供幂等的决策查询功能

这些接口确保了不同管理工具之间的操作标准化。

## 调用方式

该工具提供统一的调用接口：
- `invoke(input, opts?) -> Promise<OutputJson | ErrorJson>`

`invoke()` 函数用于启动决策流程，并通过共享的 `consensus-guard-core` 接口与管理系统进行交互，执行明确的策略评估。

## 外部代理模式

该工具支持两种运行模式：
- `mode="external_agent"`：调用者提供来自外部代理（如人工审核系统、模型等）的投票结果，以便进行统一的统计分析
- `mode="persona"`：需要预先存在的 `persona_set_id`；此时工具不会自动生成用户角色信息