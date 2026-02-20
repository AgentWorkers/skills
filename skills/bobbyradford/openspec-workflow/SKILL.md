---
name: openspec-workflow
description: "使用 OpenSpec CLI 和 Claude Code 进行自主的、基于规范的开发。您负责协调工作（起草相关文档、做出决策、提交 Pull Request），而 Claude Code 则可以访问实际的代码库并执行相应的任务。适用场景包括：  
1. 对使用 OpenSpec 的代码库进行任何修改；  
2. 创建或修改提案、设计文档、技术规范或任务分解方案；  
3. 提交需要相关规范文档的 Pull Request；  
4. 为使用 OpenSpec 的代码库设置自动归档的持续集成（CI）流程。  
整个开发流程涵盖以下环节：  
问题提出 → 生成 OpenSpec 规范文档 → Claude Code 进行代码审查 → Claude Code 完成代码实现 → 提交 Pull Request → 合并代码后自动归档。  
所需工具：openspec CLI、claude CLI（用于 Claude Code 的命令行工具）、gh CLI（GitHub 命令行工具）以及 git（版本控制工具）。"
---
# OpenSpec 工作流程

通过自动化的流程来推送基于规范的变更，并设置严格的审核质量检查点。

## 架构

**您是整个流程的协调者。** 您负责做出决策、起草规范文档、处理审核反馈，并决定哪些变更可以正式推送。Claude Code 是您的得力助手——它能够分析代码库、在真实的代码上下文中进行审核，并执行相应的任务。

| 角色 | 负责人 | 职责 |
|------|-----|------|
| **协调者** | 您（运行此技能的代理） | 调用 OpenSpec CLI、起草规范文档、审核变更、提交 Pull Request (PR) |
| **审核者** | Claude Code（或子代理） | 分析代码库、验证变更内容、提出审核意见 |
| **实施者** | Claude Code | 执行任务、修改代码、提交更改 |

**为何采用这种分工：** OpenSpec CLI 非常适合用于脚本编写和自动化操作，非常适合协调者使用；而 Claude Code 则能自动获取完整的代码库上下文，非常适合进行代码审核和实施工作。不过，当 AI 成为决策者时，这种交互式的流程可能会增加不必要的复杂性。**

## 何时使用此流程

**在以下情况下使用 OpenSpec：** 变更会影响产品的功能或行为时：
- 新功能的添加或现有功能的修改
- 会导致行为变化的代码重构
- 会造成问题的重大变更或系统迁移
- 任何会修改或创建新的技术规范的变更

**如果变更只是补充性的（例如示例代码、教程内容、文档更新等），可以直接提交 PR，无需使用 OpenSpec：**
- 修正拼写错误、更新 README 文件、调整注释
- 配置 CI/CD 工具（如 GitHub Actions、代码检查工具）
- 更新依赖关系

**关键问题：** “这个变更是否会影响产品的核心功能，还是仅仅是对现有功能的补充？”

## 先决条件

- 已安装 `openspec` CLI（`npm install -g @fission-ai/openspec`）
- 已安装 `claude` CLI
- 已通过 `gh` CLI 登录并具有仓库访问权限
- 仓库中已创建 `openspec/` 目录
- 工作目录为仓库的根目录或 Git 工作区

## 超时设置

当以子代理的身份运行此流程时，根据变更的复杂程度设置 `runTimeoutSeconds`：

| 变更类型 | 超时时间 | 原因 |
|-------------|---------|-----|
| 仅涉及文档的简单变更 | 300 秒（5 分钟） | 生成 1-2 个规范文档，可能无需审核，可快速实施 |
| 标准代码变更 | 900 秒（15 分钟） | 生成 4 个规范文档，Claude Code 进行审核并实施变更 |
| 复杂的变更（涉及多个文件） | 1200 秒（20 分钟） | 需要复杂的审核和大量的代码修改，可能需要重新审核 |

每次调用 Claude Code（无论是进行审核还是实施变更）大约需要 1-3 分钟。整个流程（包括 4 个规范文档的审核和实施）至少需要调用 Claude Code 5-8 次。

## 快速入门

```
1. openspec new change "<name>"
2. For each artifact: draft → review loop → write
3. Implement tasks
4. Commit, push, open PR with "OpenSpec change: <name>" in body
```

## 工作流程

### 第一步：创建变更

```bash
openspec new change "<kebab-case-name>"
openspec status --change "<name>"
```

### 第二步：处理规范文档

对于每个规范文档，按顺序执行以下操作（通常顺序为：提案 → 设计 → 规范文档 → 任务）：

```bash
openspec instructions <artifact-id> --change "<name>"
```

阅读规范文档的模板和依赖关系，然后起草文档内容。

**接下来需要决定：是否进行审核？**

- 如果规范文档非常简单（例如只需修改一行配置、进行简单的重命名等），则**跳过审核**，并记录原因：`跳过审核 — 简单变更：<原因>`。
- 如果规范文档涉及重要的设计决策、权衡或存在模糊之处，则**提交审核**。

使用仓库路径作为参数，创建子代理来执行审核任务，以便他们能够独立地分析代码库（例如阅读文件、查找代码中的问题等）。不要直接将规范文档复制给审核者，而是提供必要的工具让他们进行审核。详细流程和提示模板请参考 `references/review-loop.md`。

起草完规范文档后，确认审核进度：

```bash
openspec status --change "<name>"
```

继续处理下一个规范文档。

### 第三步：通过 Claude Code 实施变更

**不要直接手动实施变更。** 将任务委托给 Claude Code，因为它能够全面理解代码库的上下文，从而安全地执行变更。

```bash
# Get the task list for Claude Code's prompt
cat openspec/changes/<name>/tasks.md
```

在仓库（或 Git 工作区）中启动 Claude Code，使用 `--dangerously-skip-permissions` 参数：

```bash
exec pty:true workdir:<repo-path> background:true command:"claude --dangerously-skip-permissions -p 'Implement these tasks from openspec/changes/<name>/tasks.md. Read the tasks file, the proposal, design, and specs in that change directory for full context. Mark tasks complete as you go. Commit when done.

When completely finished, run: openclaw system event --text \"Done: implemented <name>\" --mode now'"
```

通过 `process action:logsessionId:<id>` 监控 Claude Code 的执行过程。Claude Code 会：
- 读取 OpenSpec 规范文档以获取上下文信息
- 执行每个指定的任务
- 完成任务后标记为 `[x]`
- 提交更改

对于简单的变更（例如纯文档编辑或一行代码的修改），可以直接手动实施，并记录原因：`直接实施 — 简单变更：<原因>`。

### 第四步：推送变更

**在提交之前**，确认变更的名称与实际对应的目录名称一致：

```bash
# Get the exact change directory name
CHANGE=$(ls openspec/changes/ | grep -v archive | head -1)
echo "Change name: $CHANGE"
```

在提交信息以及 Pull Request 的正文中，务必使用与目录名称完全匹配的名称：

```bash
git add -A
git commit -m "<type>(scope): <description> (#<issue>)

OpenSpec change: $CHANGE"
git push origin <branch>
gh pr create --repo <owner/repo> --base main --head <branch> \
  --title "<type>: <description>" \
  --body "Closes #<issue>

OpenSpec change: $CHANGE"
```

**重要提示：** Pull Request 正文中的 `OpenSpec change: <名称>` 必须与 `openspec/changes/` 目录下的实际文件名完全一致。GitHub 的自动归档功能会依据这个名称来定位变更文件。如果名称不一致，归档操作将会被忽略。在提交前，请务必使用 `ls openspec/changes/` 命令验证目录名称是否正确。**

### 第五步：处理 Pull Request 的审核评论

在打开 Pull Request 后，审核人员可能会留下评论。请及时查看并回复：

```bash
# Check for review comments
gh pr view <number> --repo <owner/repo> --json reviews,comments
gh api repos/<owner>/<repo>/pulls/<number>/comments
```

对于每条审核评论：
1. **评估评论的严重性**：它是否指出了真正的错误、遗漏的边缘情况或设计问题？
2. **如果评论内容重要**：在 Git 工作区中修复问题，然后提交更改，Pull Request 会自动更新。
   ```bash
   # Fix, then:
   git add -A && git commit -m "fix: address review — <what changed>"
   git push origin <branch>
   ```
3. **如果评论内容不重要**：直接在评论区回复并说明理由。
   ```bash
   gh api repos/<owner>/<repo>/pulls/<number>/comments/<comment-id>/replies \
     -f body="<your justification>"
   ```

遵循与规范文档审核相同的判断规则：接受合理的建议，对不合理的内容予以拒绝，并在适当的情况下部分采纳。不要盲目接受所有建议——最终决策权在您手中。

### 第六步：记录和报告流程

将整个流程的日志发布到 GitHub 问题中：

```bash
gh issue comment <number> --repo <owner/repo> --body '<workflow log>'
```

报告中应包含每个规范文档的起草内容、审核过程中的问题、修改记录、跳过审核的决策理由以及最终的实施细节。

**务必在报告中提供问题的链接和 Pull Request 的链接：**
- 问题链接：`https://github.com/<owner>/<repo>/issues/<number>`
- Pull Request 链接：`https://github.com/<owner>/<repo>/pull/<number>`

## 规范文档编写指南

### proposal.md
- 说明变更的**目的**（1-2 句），**具体变更内容**（使用项目符号列出），**新增或修改的功能**，以及**变更的影响**
- 列出所有会被修改或新增的技术规范文档

### design.md
- 说明变更的**背景信息**、**目标/非目标**、**决策过程（包括考虑过的替代方案）以及**可能的风险和权衡**
- 对于简单的文档修改（例如纯文本编辑或一行配置更改），可以跳过此步骤

### specs/\<capability\>/spec.md
- 使用差分格式编写文档：`## 新增的需求`、`## 修改的需求`、`## 删除的需求`
- 每个需求都需要包含 `### 需求：<名称>` 和至少一个 `#### 场景描述`
- 修改后的需求内容应包含完整的更新信息（而不仅仅是差异对比）
- 对于修改后的功能，应使用 `openspec/specs/` 目录中现有的规范名称

### tasks.md
- 使用编号和复选框来列出任务：`- [ ] 1.1 任务描述`
- 任务内容应简洁明了，能够在一次操作中完成
- 任务应按照依赖关系进行排序

## GitHub Action：自动归档

对于希望实现自动规范同步和归档的仓库，可以添加此工作流程。具体操作步骤请参考 `references/archive-action.md`。

该 GitHub Action 的功能包括：
1. 在 Pull Request 合并时触发
2. 从 Pull Request 正文中提取变更名称
3. 在新的分支上执行 `openspec archive --yes` 命令以生成归档文件
4. 创建一个新的 Pull Request，其中包含归档文件和同步后的规范文档
5. 删除原始的合并分支