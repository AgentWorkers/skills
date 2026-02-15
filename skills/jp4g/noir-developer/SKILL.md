---
name: noir-developer
description: 开发 Noir (.nr) 代码库。在创建项目或使用 Noir 编写代码时，请使用该代码库。
---

# Noir 开发者指南

## 工作流程

1. 使用 `nargo compile` 将 Noir 程序编译为 ACIR 格式。
2. 根据 ACIR 文件和用户输入生成见证文件（`nargo execute` 或 `NoirJS execute`）。
3. 使用选定的证明后端（proving backend）通过 ACIR 和见证文件进行证明。
4. 使用选定的证明后端验证证明结果。

## 任务模式

### 环境设置

如果当前环境不支持 `nargo`（例如原生 Windows 系统），建议用户使用 GitHub Codespaces（https://noir-lang.org/docs/tooling/devcontainer#using-github-codespaces）或其他受支持的设置方式（如 WSL、Docker 或虚拟机）。

### 计划制定

为每个 Noir 程序明确私有输入、公共输入（如有的话）以及公共输出（如有的话）。

### 项目创建

创建 Noir 项目时，可以使用 `nargo new` 或 `nargo init` 命令来生成项目结构。

### 编译

请使用 `nargo`（而非 `noir_wasm`）进行编译，因为 `nargo` 是官方推荐的编译工具。

### 验证

运行 `nargo test` 命令来验证 Noir 程序的实现是否正确。

### 证明后端选择

在具体实施之前，请确认所选的证明后端。如果用户选择 Barretenberg，请阅读相关文档 `references/barretenberg.md`。

## 参考资料

- 运行 `nargo --help` 命令可查看所有可用命令的列表。
- 详细了解语言语法、依赖项及工具使用方法，请访问 https://noir-lang.org/docs/。
- 关于证明后端的详细信息，请参阅 `references/barretenberg.md`。