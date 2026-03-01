---
name: consensus-publish-guard
description: 基于用户角色的权限管理机制，用于控制内容的发布（包括博客文章、社交媒体帖子和公告）。通过严格的访问控制、加权共识机制、内容重写功能以及内置的审计工具，有效防止不安全的公开内容被发布。
homepage: https://github.com/kaicianflone/consensus-publish-guard
source: https://github.com/kaicianflone/consensus-publish-guard
metadata:
  {"openclaw": {"requires": {"bins": ["node", "tsx"]}}}
---
# consensus-publish-guard

`consensus-publish-guard` 负责在内容发布前对其进行审核，确保其符合公开发布的标准。

## 功能概述

- 通过多人共识机制审查内容草稿；
- 识别可能涉及政策、法律或敏感风险的内容；
- 决定内容是“批准”（APPROVE）、“阻止”（BLOCK）还是“重写”（REWRITE）；
- 对可修改的内容生成相应的修复补丁（rewrite patch）；
- 将最终决策及人员信息更新保存到相应的管理平台（board artifacts）中。

## 重要性

公开发布的内容直接影响品牌形象、法律合规性以及用户信任度。通过多人共识机制进行审核，能够比单一流程更有效地确保内容的安全性。

## 生态系统中的角色

该工具依赖于 `consensus-persona-generator` 生成的人员信息（personas），并使用 `consensus-guard-core` 提供的确定性逻辑进行处理；所有相关数据均通过 `consensus-tools` 管理平台进行存储和管理。

## 适用场景

- 适用于需要人工智能辅助的内容审核流程（如社交媒体、媒体发布等）；
- 产品发布前的文本检查；
- 需要严格遵循政策规定的沟通内容。

## 运行时环境、权限要求及网络行为

- 运行时使用的编程语言：`node`、`tsx`；
- 在审核过程中不涉及网络调用；
- 如果需要生成人员信息（personas），且相关后端使用了外部大型语言模型（LLM），则可能需要进行外部 API 调用；
- 默认情况下不需要特殊权限；但如果使用外部 LLM 生成人员信息，则可能需要提供相应的 API 密钥（例如 `OPENAI_API_KEY`）；
- 数据存储在配置好的管理平台文件系统中。

## 依赖关系管理

- `consensus-guard-core` 和 `consensus-persona-generator` 均为第三方提供的共识处理模块；
- 它们的版本信息通过 `package.json` 文件进行版本控制，以确保可重复安装；
- 该工具本身不会请求系统的全局权限，也不会修改其他工具的功能。

## 快速入门

```bash
node --import tsx run.js --input ./examples/input.json
```

## 与其他工具的集成

该工具与 `consensus-interact` 合规性检查框架紧密集成（通过共享的 `consensus-guard-core` 封装层实现）：
- 提供 `readBoardPolicy`、`getLatestPersonaSet`、`writeArtifact`、`writeDecision` 等接口；
- 支持幂等性的决策查询功能。

## 调用方式

该工具提供了一个标准的接口：
- `invoke(input, opts?) -> Promise<OutputJson | ErrorJson>`

调用该接口会启动审核流程，包括人员信息评估以及与 `consensus-interact` 框架的交互操作。

## 外部代理模式（external_agent mode）

该工具支持两种运行模式：
- `mode="persona"`（默认模式）：自动加载/生成人员信息并执行内部投票；
- `mode="external_agent"`：由外部代理提供投票结果（`external_votes[]`），工具负责进行数据汇总、政策检查及最终决策的写入。