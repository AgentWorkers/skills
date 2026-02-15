---
name: ralph
description: 创建项目需求文档（PRDs），并使用 Claude Code 自动化 RALPH 构建流程。适用于启动新项目时，希望 Claude Code 能遵循基于结构化项目需求文档的开发流程，实现任务跟踪、测试以及 Git 提交的自动化操作。
---

# Ralph Skill - 基于产品需求文档（PRD）的驱动开发

使用产品需求文档（PRD）和 RALPH 构建循环（BUILD LOOP）自动化项目开发。

## 快速入门

```bash
# Create a PRD file
ralph init --name "My Project" --language python

# Start Claude Code with the PRD
ralph build

# Check progress
ralph status

# Clean up when done
ralph cleanup
```

## Ralph 的功能

1. **初始化 PRD** - 创建结构化的项目需求文档
2. **启动 Claude Code** - 使用 `--dangerously-skip-permissions` 标志
3. **管理 RALPH 循环** - 跟踪任务优先级、完成情况以及测试进度
4. **处理提交** - 自动提交带有任务 ID 的更改（例如：“SEC-001：添加 .gitignore 文件”）
5. **监控进度** - 随着任务的完成更新 PRD
6. **运行测试** - 在继续进行下一步之前验证每个任务是否正常工作

## RALPH 构建循环

Ralph 会自动执行以下 8 个步骤的工作流程：

```
1. START      → Create .gitignore + .env.example (security first!)
2. LOOP       → Pick highest priority incomplete task
3. READ       → Check if file exists, read existing code
4. BUILD      → Implement task per acceptance_criteria
5. TEST       → Run test command, verify it works
6. COMMIT     → git add + commit with task ID
7. MARK       → Update task status to "complete"
8. REPEAT     → Go to step 2 until all tasks done
9. DONE       → Run full test suite
```

## 监控

Ralph 会在后台自动监控 Claude Code 的构建过程：

```bash
# Monitor a running build
ralph monitor --session <session_id> --dir <project_dir>

# With custom check interval (default 30s)
ralph monitor --session <session_id> --dir <project_dir> --interval 60
```

**监控功能包括：**
- 每 30 秒检查一次会话状态（可配置）
- 报告文件变更情况（哪些文件被创建或修改）
- 显示最近的活动记录
- 如果会话意外停止会发出警报
- 最长监控时间为 1 小时（默认设置）

**输出示例：**
```
📊 BUILD STATUS CHECK
⏱️  Session: fast-slug...
🟢 RUNNING
📝 Recent files (5):
   - package.json
   - src/App.jsx
   - Dockerfile
   - ...and 2 more
💬 Recent activity: CORE-001: Implementing chess logic...
```

监控器会持续运行并定期报告状态，因此您无需手动检查！

## 命令

### `ralph init`
初始化一个新的基于 PRD 的项目。

```bash
ralph init --name "Project Name" --language python
ralph init --name "Web App" --language javascript --github
```

选项：
- `--name`（必选）- 项目名称
- `--language`（可选）- 编程语言（python、javascript、go、rust 等）
- `--github`（可选）- 初始化时创建 GitHub 仓库
- `--path`（可选）- 项目目录（默认为当前目录）

创建的文件：
- `PRD.json` - 项目需求文档
- `.gitignore` - 安全基线配置文件
- `.env.example` - 环境配置文件
- `ralph.config.json` - Ralph 配置文件

### `ralph build`
使用 PRD 启动 Claude Code 并开始 RALPH 构建循环。

```bash
ralph build                          # Use PRD.json in current dir
ralph build --prd custom-prd.json   # Use custom PRD
ralph build --auto-commit           # Auto-commit after each task
```

选项：
- `--prd`（可选）- PRD 文件的路径
- `--auto-commit`（可选）- 每个任务完成后自动提交
- `--section`（可选）- 从特定部分开始执行（如 00_security、01_setup 等）

### `ralph status`
显示当前的项目状态和任务进度。

```bash
ralph status
```

显示内容：
- 已完成的任务 / 总任务数
- 当前正在处理的部分
- 下一个需要执行的任务
- 最近的提交记录
- 测试结果

### `ralph update`
在手动修改后更新 PRD 中的任务状态。

```bash
ralph update --task SEC-001 --status complete
ralph update --task SEC-001 --comment "Security baseline added"
```

### `ralph test`
运行项目的测试套件（根据编程语言选择相应的测试命令）。

```bash
ralph test                    # Run all tests
ralph test --task SEC-001     # Test specific task
```

### `ralph commit`
使用任务 ID 自动创建提交记录。

```bash
ralph commit --task SEC-001 --message "Add .gitignore"
```

### `ralph cleanup`
项目完成后进行清理。

```bash
ralph cleanup                 # Archive PRD and config
ralph cleanup --full         # Remove entire project
```

## PRD 结构

Ralph 使用以下结构创建 PRD 文档：

```json
{
  "pn": "Project Name",
  "pd": "Project description",
  "sp": "Starter prompt for Claude Code",
  "gh": true,
  "ts": {
    "language": "Python",
    "framework": "Flask"
  },
  "p": {
    "00_security": {
      "n": "Security",
      "t": [
        {
          "id": "SEC-001",
          "ti": "Create .gitignore",
          "d": "Add .gitignore with secrets and dependencies",
          "f": ".gitignore",
          "pr": "high",
          "st": "pending",
          "ac": "[x] .gitignore created, [x] .env.example created"
        }
      ]
    },
    "01_setup": {...},
    "02_core": {...},
    "03_api": {...},
    "04_test": {...}
  }
}
```

字段说明：
- `id` - 任务标识符（例如：SEC-001）
- `ti` - 任务标题
- `d` - 任务描述
- `f` - 涉及的文件
- `pr` - 任务优先级（高、中、低）
- `st` - 任务状态（待处理、进行中、已完成、受阻）
- `ac` - 接受标准（以清单形式呈现）

## 配置

Ralph 将配置信息存储在 `ralph.config.json` 文件中：

```json
{
  "project_name": "My Project",
  "language": "python",
  "prd_path": "PRD.json",
  "test_command": "pytest",
  "auto_commit": false,
  "claude_code_flags": ["--dangerously-skip-permissions"],
  "git_user": "name",
  "git_email": "email@example.com"
}
```

## 任务优先级顺序

Ralph 的执行顺序始终如下：
1. **00_security** - `.gitignore` 文件、`.env.example` 文件的配置、秘密管理
2. **01_setup** - Git 仓库的设置、GitHub 配置、持续集成/持续交付（CI/CD）设置、依赖项管理
3. **02_core** - 应用程序的核心逻辑和功能开发
4. **03_api** - API 端点开发与集成
5. **04_test** - 全面测试套件的执行

## 使用示例

```bash
# 1. Initialize new Python project
ralph init --name "Todo API" --language python

# 2. Edit PRD.json with your specific tasks
# (Ralph adds defaults; customize as needed)

# 3. Start Claude Code with RALPH loop
ralph build --auto-commit

# 4. Monitor progress
ralph status

# 5. When done, review and clean up
ralph cleanup
```

## 高级功能

### 自定义测试命令

Ralph 可根据编程语言自动识别测试命令：

```
Python  → pytest
Node.js → npm test
Go      → go test ./...
Rust    → cargo test
```

您可以在 `ralph.config.json` 中进行自定义配置：

```json
{
  "test_command": "python -m pytest --cov"
}
```

### GitHub 集成

Ralph 可以帮助创建 GitHub 仓库并设置持续集成/持续交付（CI/CD）流程：

```bash
ralph init --name "Project" --github
```

创建的文件/配置包括：
- 远程 GitHub 仓库
- 用于 CI/CD 的 `.github/workflows/test.yml` 文件
- 主分支的权限保护规则

### 任务依赖关系

Ralph 会确保依赖其他任务的步骤只有在相关任务完成之后才会开始执行（例如：CORE-005 依赖于 CORE-001 和 CORE-002 的完成）。

## 如何启动构建过程

```bash
# Initialize a new project
ralph init --name "My Project" --language python

# Edit PRD.json with your specific tasks

# Start Claude Code (WITHOUT --dangerously-skip-permissions)
cd ~/Desktop/my-project
claude exec "Follow the RALPH BUILD LOOP. Here's the PRD: $(cat PRD.json)"

# Approve the security prompt when Claude Code asks
# Then let it work through each task
```

**重要提示：** 不要使用 `--dangerously-skip-permissions` 标志——这可能会导致 Claude Code 出现错误。请在需要时正常请求权限。

## 权限与安全原则

**我（Clawd）负责在构建过程中授予权限。** 您已经表示对大多数操作持宽容态度，只要这些操作：
- 不会破坏系统运行
- 不会让您面临安全风险
- 不会损坏您的文件

**您的原则：**
> “我非常重视安全性。我希望在保证良好用户体验的同时，也能确保系统的安全性。虽然我不希望安全性影响到用户体验，但对于一些基本的安全措施（如 `.gitignore` 文件和 `.env` 文件的配置），我是坚决不会妥协的。”

**翻译说明：** 在优化用户体验的同时，务必坚守安全底线：
- ✅ 必须配置 `.gitignore` 文件（仓库中不应包含敏感信息）
- ✅ 必须创建 `.env` 文件（敏感信息不能被提交）
- ✅ 对于安全相关的常规操作，无需额外请求权限
- ✅ 用户体验和操作流程同样重要（确保构建过程顺畅快速）

**我会自动批准以下安全操作：**
- ✅ 安装/运行 npm 包管理工具
- ✅ 在项目目录中创建/编辑文件
- ✅ 运行构建/测试命令（如 `npm build`、`cargo test` 等）
- ✅ 使用 Docker 进行相关操作（如 `docker build`、`docker compose up` 等）
- ✅ 执行 Git 操作（如 `git init`、`git add`、`git commit`、`git push`）
- ✅ 使用标准的开发工具和操作流程
- ✅ 正确配置 `.gitignore` 和 `.env.example` 文件

**我会请求或拒绝以下操作：**
- ❌ 删除重要目录的命令
- ❌ 修改系统级设置的操作
- ❌ 运行未经审核的第三方脚本
- ❌ 访问或暴露敏感数据/凭证的操作
- ❌ 行为可疑的网络操作
- ❌ 忽略 `.gitignore` 或 `.env` 文件中的安全配置（这些是绝对不允许的）

**在构建过程中：** 当 Claude Code 请求权限时，如果操作是安全的，我会自动处理。您可以专注于整体项目进度，而我负责处理具体的操作细节，并确保所有基本安全措施得到落实。

## 随附资源

- **scripts/init_prd.py** - 用于创建新的 PRD 文档
- **scripts/run_ralph_loop.py** - 用于执行 RALPH 工作流程
- **scripts/monitor_build.py** - 用于监控 Claude Code 的构建过程并报告进度
- **references/prd_templates.md** - 各编程语言对应的 PRD 模板文件
- **assets/prd_schema.json** - PRD 文档的 JSON 结构规范

## 常见问题

**Claude Code 无法启动**
- 确保已安装 `claude` 命令行工具
- 检查您的版本是否支持 `--dangerously-skip-permissions` 选项

**任务无法提交**
- 确保已执行 `git init` 命令
- 检查 `git config user.email` 的配置是否正确

**测试失败**
- Ralph 会暂停并报告失败原因，您需要查看测试结果并修复问题后，再使用 `ralph build --section 04_test` 继续构建

## 使用建议

1. **优先处理安全性相关任务** - Ralph 会首先执行 `.gitignore` 和 `.env.example` 的配置
2. **仔细阅读 PRD 文档** - 优秀的 PRD 文档是项目成功的基础
3. **频繁进行测试** - Ralph 会在每个任务完成后自动执行测试
4. **编写清晰的提交信息** - 任务 ID 有助于记录操作历史
5. **定期审查 PRD 文档** - 随着项目进展，及时更新接受标准（acceptance criteria）