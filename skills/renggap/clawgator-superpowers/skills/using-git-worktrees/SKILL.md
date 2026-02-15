---
name: using-git-worktrees
description: **使用场景：**  
在开始需要与当前工作区隔离的新功能开发时，或在执行实施计划之前，可以使用该工具。该工具能够创建隔离的 Git 工作目录，并通过智能的目录选择机制确保数据的安全性。
---

# 使用 Git Worktrees

## 概述

Git Worktrees 创建了独立的工作空间，这些工作空间共享同一个仓库，从而可以在不切换分支的情况下同时进行多分支的开发。

**核心原则：** 系统化的目录选择 + 安全性验证 = 可靠的隔离。

**启动时声明：** “我将使用 ‘using-git-worktrees’ 技能来设置一个独立的工作空间。”

## 目录选择流程

请按照以下优先级顺序进行操作：

### 1. 检查现有目录

```bash
# Check in priority order
ls -d .worktrees 2>/dev/null     # Preferred (hidden)
ls -d worktrees 2>/dev/null      # Alternative
```

**如果找到现有目录：** 使用该目录。如果两个目录都存在，则优先使用 `.worktrees/` 目录。

### 2. 检查 CLAUDE.md 文件

```bash
grep -i "worktree.*director" CLAUDE.md 2>/dev/null
```

**如果 CLAUDE.md 文件中指定了优先目录：** 无需询问，直接使用该目录。

### 3. 询问用户

如果不存在任何目录且 CLAUDE.md 文件中也未指定优先目录：

```
No worktree directory found. Where should I create worktrees?

1. .worktrees/ (project-local, hidden)
2. ~/.config/superpowers/worktrees/<project-name>/ (global location)

Which would you prefer?
```

## 安全性验证

### 对于项目本地目录（`.worktrees` 或 `worktrees`）

在创建 Worktree 之前，**必须验证该目录是否被 Git 忽略**：

```bash
# Check if directory is ignored (respects local, global, and system gitignore)
git check-ignore -q .worktrees 2>/dev/null || git check-ignore -q worktrees 2>/dev/null
```

**如果目录没有被忽略：**

根据 Jesse 的规则：“立即修复问题”：
1. 在 `.gitignore` 文件中添加相应的忽略规则。
2. 提交更改。
3. 继续创建 Worktree。

**为什么这很重要？** 这可以防止意外地将 Worktree 的内容提交到仓库中。

### 对于全局目录（`~/.config/superpowers/worktrees`）

由于该目录完全位于项目外部，因此不需要进行 `.gitignore` 的验证。

## 创建步骤

### 1. 检测项目名称

```bash
project=$(basename "$(git rev-parse --show-toplevel)")
```

### 2. 创建 Worktree

```bash
# Determine full path
case $LOCATION in
  .worktrees|worktrees)
    path="$LOCATION/$BRANCH_NAME"
    ;;
  ~/.config/superpowers/worktrees/*)
    path="~/.config/superpowers/worktrees/$project/$BRANCH_NAME"
    ;;
esac

# Create worktree with new branch
git worktree add "$path" -b "$BRANCH_NAME"
cd "$path"
```

### 3. 运行项目设置

系统会自动检测并运行相应的项目设置脚本：

```bash
# Node.js
if [ -f package.json ]; then npm install; fi

# Rust
if [ -f Cargo.toml ]; then cargo build; fi

# Python
if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
if [ -f pyproject.toml ]; then poetry install; fi

# Go
if [ -f go.mod ]; then go mod download; fi
```

### 4. 验证初始状态

运行测试以确保 Worktree 的初始状态是干净的：

```bash
# Examples - use project-appropriate command
npm test
cargo test
pytest
go test ./...
```

**如果测试失败：** 报告失败情况，并询问是否继续或需要进一步调查。

**如果测试通过：** 报告工作空间已准备好使用。

### 5. 报告 Worktree 的位置

```
Worktree ready at <full-path>
Tests passing (<N> tests, 0 failures)
Ready to implement <feature-name>
```

## 快速参考

| 情况 | 应采取的操作 |
|-----------|--------|
| `.worktrees/` 目录存在 | 使用该目录（并验证它是否被 Git 忽略） |
| `worktrees/` 目录存在 | 使用该目录（并验证它是否被 Git 忽略） |
| 两个目录都存在 | 优先使用 `.worktrees/` 目录 |
| 两个目录都不存在 | 查看 CLAUDE.md 文件 → 询问用户 |
| 目录未被 Git 忽略 | 将该目录添加到 `.gitignore` 文件中并提交更改 |
| 基线测试失败 | 报告失败情况并询问用户是否继续 |
| 项目中没有 `package.json` 或 `Cargo.toml` 文件 | 跳过依赖项的安装步骤 |

## 常见错误

### 跳过忽略规则验证

- **问题：** Worktree 的内容会被跟踪到仓库中，导致 `git status` 显示混乱。
- **解决方法：** 在创建项目本地 Worktree 之前，务必使用 `git check-ignore` 命令验证目录是否被忽略。

### 误判目录位置

- **问题：** 这会导致不一致性，违反项目规范。
- **解决方法：** 严格按照优先级顺序选择目录：优先使用现有目录 > 查看 CLAUDE.md 文件 > 询问用户。

### 在测试失败的情况下继续操作

- **问题：** 无法区分新出现的错误和已存在的问题。
- **解决方法：** 报告测试失败情况，并获得明确的继续操作许可。

### 硬编码设置命令

- **问题：** 这可能会导致在使用不同工具的项目中出现问题。
- **解决方法：** 从项目文件（如 `package.json` 等）中自动检测设置命令。

## 示例工作流程

```
You: I'm using the using-git-worktrees skill to set up an isolated workspace.

[Check .worktrees/ - exists]
[Verify ignored - git check-ignore confirms .worktrees/ is ignored]
[Create worktree: git worktree add .worktrees/auth -b feature/auth]
[Run npm install]
[Run npm test - 47 passing]

Worktree ready at /Users/jesse/myproject/.worktrees/auth
Tests passing (47 tests, 0 failures)
Ready to implement auth feature
```

## 需避免的行为

**绝对禁止：**
- 在未验证目录是否被忽略的情况下创建 Worktree（尤其是项目本地目录）。
- 跳过基线测试的验证。
- 在测试失败的情况下继续操作。
- 在目录位置不明确的情况下擅自选择目录。
- 跳过对 CLAUDE.md 文件的检查。

**必须始终遵循：**
- 严格按照目录选择的优先级顺序操作：优先使用现有目录 > 查看 CLAUDE.md 文件 > 询问用户。
- 确保项目本地目录被 Git 忽略。
- 自动检测并运行项目设置脚本。
- 验证初始测试状态是否干净。

## 集成方式

**被调用场景：**
- **头脑风暴**（第 4 阶段）——在设计方案获得批准后必须执行。
- **子代理驱动的开发流程**——在执行任何任务之前必须执行。
- **执行计划**——在执行任何任务之前必须执行。
- 任何需要独立工作空间的技能。

**配合使用的技能：**
- **完成开发分支**——工作完成后必须执行清理操作。