---
name: soulforge
description: "使用 Soulforge（feature-dev/bugfix/review-loop）运行高信号（high-signal）的自主编码循环，同时采用严格的工作树隔离（worktree isolation）、代码审查机制（review gates）以及有针对性的修复周期（scoped fix cycles）。"
metadata:
  {
    "openclaw":
      {
        "emoji": "🔥",
        "requires": { "bins": ["soulforge", "codex", "gh"], "env": [] },
      },
  }
---
# Soulforge（高效使用指南）

本文档**并非**完整的引擎参考手册，而是指导您如何使用Soulforge实现高质量自动化编码工作的操作指南。

## 核心运作模式

当您需要完成以下流程时，可以使用Soulforge：规划 → 实施 → 验证/测试 → 提交代码更改（PR） → 审查/修复问题，同时将人工干预降至最低：

- **`feature-dev`**：用于端到端的特性开发流程。
- **`bugfix`**：用于先诊断问题、再精确修复的流程。
- **`review-loop`**：用于优化现有的代码提交（PR），确保其质量达到标准。

## 最重要的规则

1. **切勿从仓库的主分支（main checkout）直接运行Soulforge命令。**  
   Soulforge现在会强制执行这一规则。
2. **始终将工作内容隔离在独立的工作目录（worktree）中。**  
   默认的工作目录路径为：`<repo>/worktrees/`。
3. **明确任务的范围。**  
   明确指定要处理的问题、验收标准以及禁止操作的事项。
4. **认真对待审查结果。**  
   对于属于当前任务范围内的问题，必须立即修复；对于超出范围的内容，应标记为“SEPARATE”（需单独处理）。
5. **仅使用`--callback-exec`选项进行回调处理。**  
   HTTP回调功能已被弃用。

## 建议使用的操作方式

### 工作目录（Workdir/Worktree）的安全性
- 如果省略`--workdir`参数，Soulforge会自动在`<repo>/worktrees/`目录下创建工作目录。
- 主分支（main checkout）不允许直接运行Soulforge命令（包括使用`bare+worktree`组合的情况）。
- 如果工作目录状态异常（例如包含未提交的修改），Soulforge会拒绝执行命令。
- 如果工作目录位于主分支之外，必须明确指定才能使用。

### 检查点（Checkpoint）机制
- 传统的“approve/reject”操作已被移除，现在使用`soulforge complete ...`命令来标记任务完成状态。
- 暂停任务的命令格式为`type: pause`。

### 回调（Callback）机制
- 必须使用`--callback-exec`选项来触发回调功能。
- 回调信息包括：
  - `{{run_id}}`（运行ID）
  - `{{step_id}}`（步骤ID）
  - `{{step_status}}`（步骤状态）
  - `{{status}}`（整体任务状态）
  - `{{callback_message}}`（步骤级别的反馈信息，推荐使用）
  - `{{prompt}}`（用于暂停操作时的提示信息，保持向后兼容性）

## 推荐的命令模式

### 特性开发（Feature Development）
```bash
soulforge run feature-dev "Implement <issue-url>.
Constraints: max 2 stories. DO NOT refactor unrelated modules." \
  --workdir /abs/path/to/repo/worktrees/feat-xyz \
  --callback-exec 'openclaw agent --session-key "agent:cpto:slack:channel:c0af7b05h28" --message "Soulforge {{run_id}} {{step_id}} {{step_status}}" --deliver'
```

### 问题修复（Bugfix）
```bash
soulforge run bugfix "Fix <issue-url> with failing test first; minimal patch only." \
  --workdir /abs/path/to/repo/worktrees/fix-xyz \
  --callback-exec 'openclaw agent --session-key "agent:cpto:slack:channel:c0af7b05h28" --message "Soulforge {{run_id}} {{step_id}} {{step_status}}" --deliver'
```

### 仅针对现有PR的优化（Review-only Optimization on Existing PR）
```bash
soulforge run review-loop "Review PR #123 and fix only in-scope findings." \
  --workdir /abs/path/to/repo/worktrees/pr-123 \
  --var pr_number=123 \
  --callback-exec 'openclaw agent --session-key "agent:cpto:slack:channel:c0af7b05h28" --message "Soulforge {{run_id}} {{step_id}} {{step_status}}" --deliver'
```

## 如何最大化自动化效率

### 1. 明确任务范围
- 提供以下信息：
  - 需要修复的问题或PR的URL
  - 明确列出属于当前任务范围内的内容
  - 明确列出不属于当前任务范围的内容
  - 制定明确的成功标准

### 2. 缩短迭代周期
- 如果PR在审查过程中反复出现相同的问题，应在工作目录中创建或更新`.soulforge-progress.md`文件，记录未解决的修复项。
- 仅针对剩余的问题重新运行`review-loop`流程。

### 3. 以操作员的角色处理审查流程
- 在审查环节：
  - 将属于当前任务范围内的问题立即修复。
  - 将无关的修改内容分离为单独的issue进行处理。
- 避免在审查过程中随意添加额外的功能。

### 4. 正视漫长的修复过程
- 对于复杂的代码重构，漫长的修复步骤是正常的。您的职责是确保代码质量，而不是干扰正在进行的自动化流程。

## 实用的问题分类策略
当代码审查返回问题时：
- 与原始问题直接相关的问题：立即修复。
- 与原始问题正确性无关的问题：通常也需要立即修复。
- 超出任务范围的问题：应标记为“SEPARATE”（需单独处理）。

## 应避免的做法
- 在同一分支下同时运行多个不同的工作流程。
- 在反复的审查和修复过程中允许任务范围不断扩大。
- 仅仅因为测试通过就合并代码更改。
- 将本文档视为通用的Soulforge使用指南，而非详细的操作手册。

## 操作员的简化工作流程
- 启动自动化流程。
- 等待审查结果。
- 严格按照任务范围进行问题分类和处理。
- 重复上述步骤，直到所有问题都得到解决。
- 合并修改后的代码到主分支。
- 构建项目并安装依赖包（使用npm）。
- 重启后台服务（如果本地运行环境需要更新）。

## 其他注意事项
- 如果迭代次数达到`max_loops`限制，应使用带有范围锁定文件的新的`review-loop`流程来继续处理问题。
- 对于耗时较长的项目，建议在团队频道中记录运行日志（包括运行ID、PR编号和状态信息）。