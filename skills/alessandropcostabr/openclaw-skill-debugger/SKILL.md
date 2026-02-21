---
name: openclaw-skill-debugger
description: Identifica e resolve problemas comuns em AgentSkills do OpenClaw, incluindo: (1) Falhas de instalação via ClawHub, (2) Inconsistências de configuração (ex: paths absolutos), (3) Dependências ausentes ou mal documentadas, e (4) Erros de execução de scripts ou integração com APIs. Fornece um guia passo a passo para depurar e validar skills, garantindo sua correta operação em ambientes de quarentena ou produção. Use esta skill quando uma AgentSkill não se comporta como esperado ou você precisa auditar seu código.
---

# OpenClaw 技能调试器

## 概述

该工具旨在帮助调试和分析 OpenClaw 中的 `AgentSkills` 相关问题。它提供了相应的工具和结构化的工作流程，以帮助识别导致安装失败、执行错误、依赖关系问题以及其他可能影响技能正常运行的不一致性的根本原因。

## 使用流程

在调试技能时，请按照以下步骤操作：

1. **理解问题**：首先收集关于错误的尽可能多的信息，包括错误消息、日志、问题复现步骤以及技能的预期行为。
2. **初步检查**：使用快速检查脚本并参考相关文档，以识别常见的问题。
    * **绝对路径/硬编码路径**：运行 `scripts/check-hardcoded-paths.sh <技能路径>`，以查找可能导致移植问题的路径。
    * **依赖关系**：查阅 `references/common-skill-issues.md` 并运行 `scripts/verify-dependencies.sh <技能路径>`（如果已实现），确认所有先决条件都已满足且文档记录正确。
    * **辅助脚本缺失**：检查目标技能的 `SKILL.md` 中引用的所有辅助脚本是否存在于 `scripts/` 目录中。
3. **详细分析**：如果初步检查未能解决问题，请参考 `references/debug-workflow.md` 进行更深入的分析，包括审查技能的源代码、OpenClaw 的日志以及在隔离环境中进行测试。
4. **修复与验证**：实施必要的修复措施，并对技能进行彻底测试，以确保问题已得到解决。

## 脚本

### `scripts/check-hardcoded-paths.sh`

该脚本接收一个技能的路径，然后扫描其文件中是否存在使用绝对路径或硬编码路径（例如 `/home/usuario/`、`/var/`、`/etc/`）的情况。
* **用法**：`bash scripts/check-hardcoded-paths.sh <要调试的技能路径>`

### `scripts/verify-dependencies.sh`（待实现）

**（此脚本尚未实现）** 该脚本将检查目标技能的 `SKILL.md` 中列出的依赖关系是否已在环境中安装。

## 参考文档

### `references/common-skill-issues.md`

该文档详细介绍了在 OpenClaw 技能开发和执行过程中常见的问题，例如：
- 脚本中使用的绝对路径。
- 未存在的辅助脚本。
- 依赖关系的声明不正确或缺失。
- 使用 `npx` 进行安装时的风险和注意事项（远程代码执行）。
- 与遥测系统集成的问题（例如，如 Issue #18794 中讨论的 OTLP 日志发送失败问题）。

### `references/debug-workflow.md`

该文档提供了从问题复现到定位根本原因并实施修复的完整调试工作流程，包括以下步骤：
- 隔离问题。
- 查看系统和技能的日志。
- 使用隔离环境。
- 代码审查技术。