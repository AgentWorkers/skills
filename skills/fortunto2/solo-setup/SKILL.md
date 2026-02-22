---
name: solo-setup
description: 根据用户的需求（如“设置工作流程”、“配置TDD”、“搭建开发工作流程”），可以自动从现有的 PRD（Project Requirements Document）和 CLAUDE.md 文件中生成项目工作流程配置文件（docs/workflow.md），而无需用户进行任何额外输入或确认。此功能适用于常规的项目配置场景，但不适用于创始人账户的初始化（请使用 /init 命令）或项目的基础搭建（请使用 /scaffold 命令）。
license: MIT
metadata:
  author: fortunto2
  version: "2.1.1"
  openclaw:
    emoji: "⚙️"
allowed-tools: Read, Grep, Bash, Glob, Write, Edit, AskUserQuestion, mcp__solograph__project_info, mcp__solograph__codegraph_query, mcp__solograph__kb_search
argument-hint: "[project-name]"
---
# /setup

本脚本会根据现有的 `PRD.md` 和 `CLAUDE.md` 文件自动生成项目的工作流程配置文件。整个过程无需用户交互，所有所需信息均从项目数据中提取（这些数据在执行 `/scaffold` 命令后就已经生成）。

## 使用场景

在 `/scaffold` 命令创建项目之后、执行 `/plan` 命令之前使用本脚本。该脚本会生成 `docs/workflow.md` 文件，以确保 `/plan` 和 `build` 命令能够正常运行。

## MCP 工具（如可用，请使用）

- `project_info(name)`：获取项目详细信息及所使用的开发技术栈。
- `kb_search(query)`：搜索开发规范、项目配置文件（manifest）以及相关模板。
- `codegraph_query(query)`：在代码图中检查项目依赖关系。

如果 MCP 工具不可用，系统将仅读取本地文件。

## 执行步骤

1. **确定项目根目录：**
   - 如果提供了 `$ARGUMENTS` 参数，将在当前目录或 `~/.solo-factory/defaults.yaml` 中指定的 `projects_dir` 中查找名为该参数的项目。
   - 如果未提供参数，使用当前的工作目录。
   - 确认目录存在，并且其中包含 `CLAUDE.md` 文件。
   - 如果找不到 `CLAUDE.md`，系统会通过 `AskUserQuestion` 提示用户确认。

2. **检查项目是否已初始化：**
   - 如果 `docs/workflow.md` 文件已经存在，系统会发出警告并询问用户是否需要重新生成该文件。

3. **读取项目数据**（所有数据会同时被读取）：
   - `CLAUDE.md`：包含技术栈、项目架构、可执行的命令以及开发规范。
   - `docs/prd.md`：包含项目问题、用户信息、解决方案、功能列表、性能指标和定价信息。
   - `package.json` 或 `pyproject.toml`：记录项目的依赖版本。
   - `Makefile`：列出可用的命令。
   - 代码格式检查配置文件（如 `.eslintrc*`, `eslint.config.*`, `.swiftlint.yml`, `ruff.toml`, `detekt.yml`）。

4. **读取项目相关的补充信息**（可选，有助于提高文档质量）：
   - 从 `CLAUDE.md` 中获取技术栈名称（通常位于 “Stack:” 标签下或技术文档部分）。
   - 如果 MCP 的 `kb_search` 功能可用，可以搜索相关的技术栈模板和开发规范文件。
   - 如果 `kb_search` 不可用，可以在 `.solo/` 目录或插件模板目录中查找 `stacks/<stack>.yaml` 和 `dev-principles.md` 文件。
   - 如果这些文件都不存在，系统会仅使用 `CLAUDE.md` 和项目配置文件中的信息。

5. **根据项目配置文件确定开发语言：**
   - `package.json`：表示项目使用 TypeScript。
   - `pyproject.toml`：表示项目使用 Python。
   - `*.xcodeproj` 或 `Package.swift`：表示项目使用 Swift。
   - `build.gradle.kts`：表示项目使用 Kotlin。

6. **（如有需要）创建文档目录：**
   ```bash
   mkdir -p docs
   ```

7. **生成 `docs/workflow.md` 文件：**
   根据开发规范（可以从 MCP 或内置默认设置中获取）生成工作流程文档。
   ```markdown
   # Workflow — {ProjectName}

   ## TDD Policy
   **Moderate** — Tests encouraged but not blocking. Write tests for:
   - Business logic and validation
   - API route handlers
   - Complex algorithms
   Tests optional for: UI components, one-off scripts, prototypes.

   ## Test Framework
   {from package manifest devDeps: vitest/jest/pytest/xctest}

   ## Commit Strategy
   **Conventional Commits**
   Format: `<type>(<scope>): <description>`
   Types: feat, fix, refactor, test, docs, chore, perf, style

   ## Verification Checkpoints
   **After each phase completion:**
   1. Run tests — all pass
   2. Run linter — no errors
   3. Run build — successful (if applicable)
   4. Manual smoke test

   ## Branch Strategy
   - `main` — production-ready
   - `feat/<track-id>` — feature branches
   - `fix/<description>` — hotfixes
   ```

8. **更新 `CLAUDE.md` 文件：**
   如果 `CLAUDE.md` 中没有工作流程相关的内容，系统会将其添加到 “Key Documents” 部分。

9. **显示项目概要并提示下一步操作：**
   ```
   Setup complete for {ProjectName}!

   Created:
     docs/workflow.md — TDD moderate, conventional commits

   Next: /plan "Your first feature"
   ```

## 常见问题

### 问题：找不到 `CLAUDE.md`
**原因：** 项目尚未通过 `/scaffold` 命令进行初始化，或者当前目录不是项目根目录。
**解决方法：** 先执行 `/scaffold` 命令，确保当前目录是包含 `CLAUDE.md` 的项目根目录。

### 问题：`docs/workflow.md` 文件已经存在
**原因：** 项目之前已经配置过工作流程。
**解决方法：** 系统会发出警告并询问用户是否需要重新生成 `docs/workflow.md` 文件；用户可以选择保留现有文件或覆盖它。

### 问题：检测到的测试框架不正确
**原因：** `devDependencies` 中包含了多个测试框架。
**解决方法：** 系统会自动选择第一个检测到的测试框架；如果需要，用户可以手动修改 `docs/workflow.md` 文件以指定正确的测试框架。