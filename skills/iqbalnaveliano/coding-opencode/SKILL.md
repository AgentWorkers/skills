---
name: coding-opencode
description: 允许使用通过“Oh My OpenCode”定制的OpenCode编码代理，来执行复杂的代码开发任务、代码库探索、调试以及多模型编排等工作。当您需要自主且先进的AI编码辅助时，可以运用这一技能，尤其是在希望利用“Oh My OpenCode”中的Sisyphus、Hephaestus、Oracle、Librarian或Explorer等代理功能，以及LSP/AST工具时。
---

# 技能：coding-opencode

该技能旨在充分利用您通过“Oh My OpenCode”自定义后的 OpenCode 安装。它提供了对复杂的多代理编排系统、集成开发工具以及自动化工作流程的支持，帮助您完成编码任务。

## 何时使用此技能

在以下情况下使用 `coding-opencode`：
- 需要 AI 助力来编写或修改代码。
- 需要对代码库进行深入探索。
- 需要调试或重构代码。
- 需要使用特定的代理（如前端 UI/UX 工程师代理或 Oracle 代理）。
- 计划执行需要多个步骤及代理间协作的开发任务。
- 希望启用 “ultrawork” 或 “ulw” 模式，以实现自动化、持续的任务执行。

## “Oh My OpenCode” 的主要功能

“Oh My OpenCode” 为您的 OpenCode 增加了多种代理和高级功能：
- **Sisyphus（主代理）**：负责协调其他代理的工作，确保任务顺利完成。
- **Hephaestus（自主深度工作代理）**：专注于目标导向的自动化执行任务。
- **Oracle（设计与调试代理）**：专门用于辅助设计和调试过程。
- **Librarian（文档与代码库探索代理）**：用于查找文档和浏览代码库。
- **Explore（快速代码库搜索代理）**：提供高效的代码库搜索功能。
- **LSP & AST 工具**：全面支持 Language Server Protocol (LSP) 和 Abstract Syntax Tree (AST)，以实现更精确、安全的重构。
- **多模型编排**：支持使用多种不同的 AI 模型，每种模型都针对特定任务进行了优化。
- **`ultrawork` / `ulw` 关键字**：在命令中添加 `ultrawork` 或 `ulw` 即可激活完整的自动化工作流程，从而利用 “Oh My OpenCode” 的所有代理和功能。

## 使用方法

要使用此技能，您可以通过 `exec` 工具调用 OpenCode 命令，并提供必要的指令和参数。若要启用 “Oh My OpenCode”的全套编排功能，请确保在命令提示符或参数中包含 `ultrawork` 或 `ulw`。

**常见用法示例：**

```bash
# Untuk memulai sesi OpenCode dengan mode ultrawork
opencode --agent build --ultrawork "Buatkan sebuah fungsi Python untuk menghitung deret Fibonacci"

# Untuk meminta agen Librarian mencari informasi tentang suatu API
opencode --agent build "ulw: Cari dokumentasi untuk API 'requests' Python dan berikan contoh penggunaan dasar."

# Untuk refactoring kode
opencode --agent build "ulw: Refactor file 'src/main.js' agar menggunakan async/await."
```

**注意：** 上面的 `opencode` 命令仅作为示例。由于 OpenCode 是通过 WSL 安装并通过 PowerShell 运行的，因此每个 OpenCode 命令都需要以 `wsl` 开头。示例：`wsl opencode ...`

**默认工作目录**：所有编码操作或文件操作默认以 `C:\Users\Administrator\Documents\Jagonyakomputer` 作为工作目录，除非另有指定。

**Docker 集成**：如果任务涉及容器化或隔离的开发环境，这些代理具备通过 PowerShell 操作 Docker 容器的能力。

## 配置

“Oh My OpenCode” 具有很高的可定制性。配置信息位于以下位置：
- `.opencode/oh-my-opencode.json`（针对项目）
- `~/.config/opencode/oh-my-opencode.json`（针对用户）

您可以在这些配置文件中更改代理的运行模型、工作温度、命令提示符设置以及权限等。

如果您需要特定配置或解决相关问题，请参考 “Oh My OpenCode”的官方文档或相应的配置文件。