---
name: solo-setup
description: 根据用户需求，可以自动从现有的 PRD（Project Requirements Document）和 CLAUDE.md 文件中生成项目工作流程配置（docs/workflow.md），而无需用户额外提问。此功能适用于以下场景：用户请求“设置工作流程”、“配置测试驱动开发（TDD）”或“搭建开发工作流程”，以及在执行 `/plan` 命令之前先运行 `/scaffold` 命令的情况。请注意：此功能不适用于创始人账户的初始化设置（使用 `/init` 命令），也不适用于项目的基础架构搭建（使用 `/scaffold` 命令）。
license: MIT
metadata:
  author: fortunto2
  version: "2.1.0"
  openclaw:
    emoji: "⚙️"
allowed-tools: Read, Grep, Bash, Glob, Write, Edit, AskUserQuestion, mcp__solograph__project_info, mcp__solograph__codegraph_query, mcp__solograph__kb_search
argument-hint: "[project-name]"
---
# /setup

该脚本会从现有的 `PRD` 文件和 `CLAUDE.md` 文件自动生成项目的工作流程配置。整个过程无需任何交互式输入——所有所需信息都从项目数据中提取，这些数据在执行 `/scaffold` 命令后就已经生成了。

## 使用场景

在 `/scaffold` 命令创建项目之后、执行 `/plan` 命令之前使用该脚本。该脚本会生成 `docs/workflow.md` 文件，以确保 `/plan` 和 `build` 命令能够正常运行。

## MCP 工具（如有可用）

- `project_info(name)`：获取项目详细信息及所使用的开发技术栈。
- `kb_search(query)`：搜索开发原则、项目规范以及相关模板。
- `codegraph_query(query)`：在代码图中检查项目依赖关系。

如果 MCP 工具不可用，则仅使用本地文件来生成工作流程配置。

## 执行步骤

1. **确定项目根目录：**
   - 如果提供了 `$ARGUMENTS` 参数，使用 `~/startups/active/<name>` 作为项目根目录。
   - 否则，使用当前的工作目录。
   - 确认该目录存在，并且包含 `CLAUDE.md` 文件。
   - 如果找不到 `CLAUDE.md`，则通过 `AskUserQuestion` 提问用户是否需要重新生成配置文件。

2. **检查配置文件是否已存在：**
   - 如果 `docs/workflow.md` 文件已经存在，系统会发出警告，并询问用户是否需要重新生成。

3. **读取项目数据**（同时读取所有相关文件）：
   - `CLAUDE.md`：包含技术栈、项目架构、可使用的命令以及开发规范。
   - `docs/prd.md`：包含项目问题、用户信息、解决方案、功能列表、性能指标和定价信息。
   - `package.json` 或 `pyproject.toml`：包含项目的依赖版本信息。
   - `Makefile`：包含可执行的命令。
   - 代码风格检查工具的配置文件（如 `.eslintrc*`, `eslint.config.*`, `.swiftlint.yml`, `ruff.toml`, `detekt.yml`）。

4. **读取与项目生态系统相关的内容**（可选，可提升文档质量）：
   - 从 `CLAUDE.md` 中获取技术栈名称（通常位于 “Stack:” 标签下或技术部分）。
   - 如果 MCP 提供了 `kb_search` 功能，可以搜索相关的技术栈模板和开发原则。
   - 如果没有这些资源，可以查找位于 `solopreneur` 根目录下的 `1-methodology/stacks/<stack>.yaml` 和 `1-methodology/dev-principles.md` 文件。
   - 如果这些文件也不存在，则完全依赖 `CLAUDE.md` 和项目配置文件中的信息。

5. **根据项目配置文件确定开发语言：**
   - `package.json`：表示项目使用 TypeScript。
   - `pyproject.toml`：表示项目使用 Python。
   - `*.xcodeproj` 或 `Package.swift`：表示项目使用 Swift。
   - `build.gradle.kts`：表示项目使用 Kotlin。

6. **（如需要）创建文档目录：**
   ```bash
   mkdir -p docs
   ```

7. **生成 `docs/workflow.md` 文件：**
   根据项目中的开发原则（来自 MCP 提供的信息或内置的默认值）来生成工作流程文档。
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

8. **更新 `CLAUDE.md` 文件**：
   如果 `CLAUDE.md` 中没有工作流程相关的信息，会在其中添加相应的引用。

9. **显示配置摘要并提示下一步操作：**
   ```
   Setup complete for {ProjectName}!

   Created:
     docs/workflow.md — TDD moderate, conventional commits

   Next: /plan "Your first feature"
   ```

## 常见问题

### 问题：找不到 `CLAUDE.md` 文件
**原因：** 项目尚未通过 `/scaffold` 命令进行初始化，或者当前目录不是项目根目录。
**解决方法：** 先运行 `/scaffold` 命令，确保当前目录是包含 `CLAUDE.md` 的项目根目录。

### 问题：`docs/workflow.md` 文件已经存在
**原因：** 之前已经生成过工作流程配置文件。
**解决方法：** 系统会发出警告，并询问用户是否需要重新生成。除非用户明确选择覆盖现有文件，否则会保留原有文件。

### 问题：检测到的测试框架不正确
**原因：** `devDependencies` 中包含多个测试框架。
**解决方法：** 系统会自动选择第一个检测到的测试框架；如果需要，可以手动修改 `docs/workflow.md` 文件以指定正确的测试框架。