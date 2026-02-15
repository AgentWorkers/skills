---
name: openspec
description: 使用 OpenSpec CLI 进行基于规范的开发。适用于构建新功能、进行代码迁移、重构或任何结构化的开发工作。该工具管理从提案到规范、设计、任务再到实现的整个开发流程。支持自定义开发模式（如测试驱动开发（TDD）、快速开发等）。会在涉及功能规划、规范编写、变更管理的请求中自动触发相应的流程，或者在用户执行 `/opsx` 命令时启动相关流程。
---

# OpenSpec — 基于规范的开发（Spec-Driven Development）

OpenSpec 将人工智能辅助的开发过程转化为可追踪的变更，通过生成各种文档（提案、规范、设计文档和任务列表）来指导开发实施。

## 设置（Setup）

```bash
# Install globally
npm install -g @fission-ai/openspec@latest

# Initialize in a project
cd /path/to/project
openspec init --tools claude

# Update after CLI upgrade
openspec update
```

## 核心工作流程（Core Workflow）

每个变更都遵循以下步骤：**新建 → 规划 → 应用 → 验证 → 归档**

### 1. 启动变更（Start a Change）

```bash
# Create change folder with default schema
openspec new change <name>

# With specific schema
openspec new change <name> --schema tdd-driven
```

### 2. 规划（Create Artifacts）

使用 CLI 的 `instructions` 命令来获取每个文档的创建指南：

```bash
# Get instructions for next artifact
openspec instructions --change <name> --json

# Check progress
openspec status --change <name> --json
```

**文档创建顺序（基于规范的流程）：**
1. `proposal.md` — 变更的背景、目的和范围
2. `specs/` — 需求与测试场景（Given/When/Then）
3. `design.md` — 技术实现方案和架构设计
4. `tasks.md` — 实现任务清单（包含复选框）

### 3. 实施（Implement）

阅读 `tasks.md`，完成其中的各项任务，并将已完成的任务标记为 `[x]`。

### 4. 验证（Verify）

```bash
openspec validate --change <name> --json
```

验证变更的完整性、正确性和逻辑一致性。

### 5. 归档（Archive）

将修改后的文档合并到主目录 `openspec/specs/` 中，并将变更状态标记为已归档。

## 作为 AI 代理的使用方法（Agent Workflow）

当用户请求使用 OpenSpec 进行构建、迁移或重构代码时，代理会执行以下操作：

1. **检查项目状态：**
   ```bash
   openspec list --json           # Active changes
   openspec list --specs --json   # Current specs
   openspec schemas --json        # Available schemas
   ```

2. **创建变更：**
   ```bash
   openspec new change <name> [--schema <schema>]
   ```

3. **针对每个文档**，获取创建指南并生成相应的文件：
   ```bash
   openspec instructions <artifact> --change <name> --json
   openspec status --change <name> --json
   ```
   然后将生成的文档保存到 `openspec/changes/<名称>/` 目录下。

4. **执行 `tasks.md` 中列出的任务。**

5. **验证并归档：**
   ```bash
   openspec validate <name> --json
   openspec archive <name> --yes
   ```

## CLI 快速参考（CLI Quick Reference）

| 命令 | 功能 |
|---------|---------|
| `openspec list [--specs] [--json]` | 列出所有变更或规范 |
| `openspec show <名称> [--json]` | 显示指定变更或规范的详细信息 |
| `openspec status --change <名称> [--json]` | 查看变更的完成状态 |
| `openspec instructions [文档名称] --change <名称> [--json]` | 获取创建该文档的详细指南 |
| `openspec validate [名称] [--all] [--json]` | 验证所有变更或规范的有效性 |
| `openspec archive <名称> [--yes]` | 将已完成的任务归档 |
| `openspec schemas [--json]` | 列出所有可用的文档模板 |
| `openspec templates [--json]` | 显示文档模板的路径 |
| `openspec config` | 查看或修改配置设置 |

在使用 CLI 时，请务必加上 `--json` 参数以支持程序化或自动化操作。

## 自定义文档模板（Custom Schemas）

文档模板用于定义文档的创建顺序。可以根据不同的工作流程创建自定义模板：

```bash
# Fork built-in schema
openspec schema fork spec-driven my-workflow

# Create from scratch
openspec schema init my-workflow

# Validate
openspec schema validate my-workflow
```

自定义模板文件保存在 `openspec/schemas/<名称>/schema.yaml` 中，模板文件则保存在 `templates/` 目录下。

有关模板结构的详细信息，请参阅 [references/schemas.md](references/schemas.md)。

## 项目结构（Project Structure）

```
project/
├── openspec/
│   ├── config.yaml          # Project config (default schema, context, rules)
│   ├── specs/               # Source of truth — current system behavior
│   ├── changes/             # Active changes (one folder each)
│   │   └── <change-name>/
│   │       ├── .openspec.yaml
│   │       ├── proposal.md
│   │       ├── specs/       # Delta specs (what's changing)
│   │       ├── design.md
│   │       └── tasks.md
│   └── schemas/             # Custom schemas
└── .claude/skills/          # Auto-generated Claude integration
```

## 规范格式（Spec Format）

规范文件使用 RFC 2119 中的定义关键字（SHALL/MUST/SHOULD/MAY），并结合 Given/When/Then 测试场景来描述需求。

## 变更文档（Delta Specs）

变更不会直接重写原始规范，而是生成描述具体修改内容的文档（如新增内容、修改内容或删除内容），这些文档会在归档时合并到主规范中。

## 配置文件（Config）

`openspec/config.yaml` 文件用于设置项目的默认配置：

```yaml
schema: spec-driven      # or tdd-driven, rapid, custom
context: |
  Tech stack: TypeScript, React, Node.js
  Testing: Jest
rules:
  proposal:
    - Include rollback plan
  specs:
    - Use Given/When/Then format
```