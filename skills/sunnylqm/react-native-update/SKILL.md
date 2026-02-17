---
name: react-native-update
description: 这是一个用于 React Native 更新/推送（Update/Pushy）的统一集成技能，适用于 OpenClaw 和 Claude 代码工作流程。该技能可用于安装配置、连接 appKey/update.json 文件、处理 iOS/Android 原生代码的修改、制定更新策略（checkStrategy/updateStrategy）、排查 expo-updates 引发的冲突，以及在混合代理（mixed agent）的 CLI 环境中解决热更新（hot update）相关的问题。
---
# React Native 更新集成

## 概述
使用此技能将项目从“未集成状态”提升为“在发布版本中支持热更新”状态。优先选择易于复制的步骤、最小的可行变更，并设置明确的验证检查点。

## 工作流程
1. 确定应用程序类型（React Native CLI 还是 Expo）以及目标平台。
2. 根据 `references/integration-playbook.md` 中的说明执行依赖项的安装步骤。
3. 配置必要的原生组件（如 Bundle URL 和 MainApplication 的集成点）。
4. 添加 `Pushy` 客户端和 `UpdateProvider` 以实现基本的热更新功能。
5. 运行 `scripts/integration_doctor.sh <app-root>` 命令以检查是否存在常见的问题。
6. 提供一个简短的行动列表：已完成的任务、缺失的步骤以及下一步需要验证的内容。

## 平台适配
- 如果用户使用的是 OpenClaw：提供以 OpenClaw 为主导的指导说明和文件/工作区规范。
- 如果用户使用的是 Claude Code：提供以 Claude Code 为主导的命令风格和工作流程说明。
- 如果平台未知：首先提供通用的步骤，然后再补充 OpenClaw/Claude Code 的具体说明。
- 技术步骤保持一致，仅调整命令规范和呈现方式。

## 注意事项
- 尽量减少用户代码的修改，并确保修改内容与项目当前风格相匹配。
- 不要承诺在调试模式下热更新功能能够正常工作；重点应放在发布版本的验证上。
- 对于使用 Expo 的项目，要提醒用户注意 `expo-updates` 可能导致的冲突。
- 保持应用程序的现有架构；根据当前项目风格对相关代码进行适当的调整。
- 如果原生文件的差异较大（例如使用单仓库管理或混合原生开发方式），应提供针对性的修复指导，而不是进行全面的重写。

## 提供的输出内容
- 最小的集成差异（具体涉及的文件和代码片段）。
- 验证检查清单（包括构建、更新检查、下载以及版本切换等步骤）。
- 常见问题的故障排除提示。
- 根据需求提供的示例场景（包括类组件集成和自定义白名单的部署方法）。

## 参考资源
- 在执行操作前，请阅读 `references/integration-playbook.md`。
- 使用 `scripts/integration_doctor.sh` 命令对项目进行快速诊断。