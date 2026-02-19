---
name: openclaw-workspace-governance-installer
description: 将 OpenClaw 转变为一个更安全、更易于使用的工作空间系统，提供引导式的设置、升级和审计功能。
author: Adam Chan
user-invocable: true
metadata: {"openclaw":{"emoji":"🚀","homepage":"https://github.com/Adamchanadam/OpenClaw-WORKSPACE-GOVERNANCE","requires":{"bins":["openclaw"]}}}
---# OpenClaw 工作区治理安装程序

本安装程序专为希望 OpenClaw 在使用初期及后续使用过程中都能保持稳定性的用户设计。

## 用户为何需要安装此程序
许多用户都会遇到以下问题：
1. 代理程序修改文件的频率过高。
2. 新会话中仍然会出现相同的错误。
3. 升级操作难以验证，也难以向团队成员解释其必要性。

本安装程序可帮助您建立更安全、更可重复的工作流程。

## 您将获得的好处
1. 固定的治理生命周期：`计划（PLAN）→ 阅读（READ）→ 修改（CHANGE）→ 质量控制（QC）→ 持久化（PERSIST）`。
2. 统一的设置入口点：`gov_setup`（支持 `install`、`upgrade`、`check` 命令）。
3. 提供持续的维护工具：`gov_migrate`、`gov_audit`、`gov_apply <NN>`。
4. 通过运行报告和索引更新来追踪操作痕迹。

## 3 分钟快速入门步骤
1. 安装：
   - `openclaw plugins install @adamchanadam/openclaw-workspace-governance@latest`
2. 启用：
   - `openclaw plugins enable openclaw-workspace-governance`
3. 验证：
   - `openclaw plugins list`
   - `openclaw skills list --eligible`
4. 在 OpenClaw 聊天窗口中执行：
   - `/gov_setup install`
   - `/gov_audit`

## 如果命令行工具不稳定，可以使用以下替代方法：
   - `/skill gov_setup install`
   - `/skill gov_setup check`
   - `/skill gov_migrate`
   - `/skill gov_audit`

您也可以用自然语言请求帮助：
   `请以只读模式运行 `gov_setup`，并返回工作区的根目录信息、安装状态以及升级建议。`

## 了解更多信息
如需了解用户价值、官方基线差异及使用场景指南，请参阅：
1. `README.md`
2. `README.en.md`
3. `WORKSPACE_GOVERNANCE_README.md`
4. `VALUE_POSITIONING_AND_FACTORY_GAP.md`