---
name: external-sync-wizard
description: **专家指南：在 SpecWeave 与 GitHub Issues、JIRA 或 Azure DevOps 之间设置双向同步**  
本指南适用于配置外部工具集成、实现系统间的字段映射以及解决同步问题。内容涵盖 Webhook 的设置、身份验证机制以及冲突解决策略。
---

# 外部同步向导专家

我专注于配置 SpecWeave（您的本地数据源）与外部项目管理工具（如 GitHub Issues、Jira 和 Azure DevOps）之间的同步。

## 何时使用此技能

当您需要以下帮助时，请联系我：
- **设置 GitHub Issues 与 SpecWeave 增量的同步**
- **配置 Jira Epic 的集成**
- **Azure DevOps 工作项的同步**
- **选择同步方向**（双向、导出、导入、手动）
- **了解同步架构**和数据源原则
- **排查同步问题**或冲突
- **从外部工具迁移到 SpecWeave**

## 我的专业知识

### SpecWeave 的同步架构

**关键理解**：`.specweave/docs/specs/` 是 **永久的、本地的数据源**。外部工具（GitHub、Jira、ADO）是这个数据源的 **镜像**。

#### 正确的同步方向

```
✅ CORRECT Architecture:
.specweave/docs/specs/  ↔  GitHub Issues
.specweave/docs/specs/  ↔  Jira Epics
.specweave/docs/specs/  ↔  Azure DevOps Work Items

❌ WRONG (External-to-External):
GitHub PRs  ↔  Jira
GitHub Issues  ↔  Jira Epics
```

**中心是本地的**，而不是外部的！

### 同步方向选项

在设置同步时，用户可以从 4 个选项中选择：

| 选项 | 方向 | 描述 | 使用场景 |
|--------|-----------|-------------|----------|
| **双向** | 本地 ↔ 外部 | 双向同步更改 | 团队协作（推荐） |
| **仅导出** | 本地 → 外部 | 从本地推送到外部 | SpecWeave 是数据源 |
| **仅导入** | 外部 → 本地 | 从外部拉取到本地 | 导入现有项目 |
| **手动同步** | 按需 | 不自动同步，手动使用命令 | 测试、一次性同步 |

**默认推荐**：**双向**（对团队最有用）

---

## 交互式设置向导

### GitHub 同步设置

#### 第 1 步：身份验证

**问题**：“您是否希望将增量同步到 GitHub Issues？”

**如果回答“是”** → 继续进行身份验证设置：
- 安装 GitHub CLI：`brew install gh`（macOS）或等效命令
- 进行身份验证：`gh auth login`
- 选择仓库：`gh repo set-default`

**如果回答“否”** → 跳过 GitHub 同步设置

#### 第 2 步：同步方向

**重要提示**：提示必须显示“在本地增量和 GitHub 之间”，而不是“在 GitHub 和 Jira 之间”！

**问题**：
```
"What should be the sync behavior between local increments (.specweave/) and GitHub Issues?"
```

**选项**：

**1. 双向同步（推荐）**
```
Local increments ↔ GitHub Issues

Features:
- Changes sync both ways automatically (on task completion)
- Conflicts: You will be prompted to resolve when both sides change
- Scope: Active increments only (completed/abandoned not auto-synced)
- Example: Complete task in SpecWeave → GitHub issue updates with progress

Best for: Teams using both SpecWeave and GitHub for project tracking
```

**2. 仅导出（本地 → GitHub）**
```
Local increments → GitHub Issues

Features:
- SpecWeave is source of truth, GitHub is read-only mirror
- Changes push from local to GitHub only
- GitHub changes are ignored (must update locally)
- Example: Create increment in SpecWeave → GitHub issue created automatically

Best for: Solo developers who prefer SpecWeave but want GitHub visibility
```

**3. 仅导入（GitHub → 本地）**
```
GitHub Issues → Local increments

Features:
- GitHub is source of truth, local workspace mirrors it
- Changes pull from GitHub to local only
- Good for: Onboarding existing GitHub projects
- Example: Close GitHub issue → Local increment status updates

Best for: Migrating from GitHub-first workflow to SpecWeave
```

**4. 仅手动同步**
```
Use /sw-github:sync command when needed

Features:
- No automatic sync via hooks
- Full control over when sync happens
- Good for: Testing, one-off syncs, experimental increments

Best for: Advanced users who want explicit control
```

**可视化辅助**（包含在提示中）：
```
✅ CORRECT Architecture:
Local (.specweave/) ↔ GitHub Issues

❌ WRONG:
GitHub ↔ Jira
```

#### 第 3 步：自动创建问题

**问题**：“当规划增量时，SpecWeave 是否应自动创建 GitHub 问题？**

**选项**：

**1. 是，自动创建（推荐）**
```
Every /sw:increment creates a GitHub issue automatically

Benefits:
- Immediate team visibility
- Bidirectional sync works from day 1
- Zero manual work
- Links: spec.md, plan.md, tasks.md included in issue

Best for: Teams that want automatic GitHub integration
```

**2. 否，手动创建**
```
Use /sw-github:create-issue manually when needed

Benefits:
- Create issues only for important increments
- More control over what goes to GitHub
- Good for: Experimental/internal increments

Best for: Solo developers or selective GitHub usage
```

---

### Jira 同步设置

#### 第 1 步：身份验证

**问题**：“您是否希望将增量同步到 Jira Epics？**

**如果回答“是”** → 继续进行身份验证设置：
- Jira 域名：`your-company.atlassian.net`
- API 令牌：从 Jira 设置中生成
- 电子邮件：您的 Jira 账户电子邮件
- 项目键：`PROJ`（例如，`AUTH`、`PAY`、`INFRA`）

**如果回答“否”** → 跳过 Jira 同步设置

#### 第 2 步：同步方向

**问题**：
```
"What should be the sync behavior between local increments (.specweave/) and Jira Epics?"
```

**选项**：

**1. 双向同步（推荐）**
```
Local increments ↔ Jira Epics

Features:
- Changes sync both ways automatically (on task completion)
- Conflicts: You will be prompted to resolve when both sides change
- Scope: Active increments only
- Example: Complete task in SpecWeave → Jira epic status updates

Best for: Teams using both SpecWeave and Jira for project management
```

**2. 仅导出（本地 → Jira）**
```
Local increments → Jira Epics

Features:
- SpecWeave is source of truth, Jira is read-only mirror
- Changes push from local to Jira only
- Jira changes are ignored (must update locally)
- Example: Create increment in SpecWeave → Jira epic created automatically

Best for: Developers who prefer SpecWeave but need Jira reporting
```

**3. 仅导入（Jira → 本地）**
```
Jira Epics → Local increments

Features:
- Jira is source of truth, local workspace mirrors it
- Changes pull from Jira to local only
- Good for: Onboarding existing Jira projects
- Example: Update Jira epic → Local increment syncs

Best for: Migrating from Jira-first workflow to SpecWeave
```

**4. 仅手动同步**
```
Use /sw-jira:sync command when needed

Features:
- No automatic sync via hooks
- Full control over when sync happens

Best for: Advanced users or testing scenarios
```

---

### Azure DevOps 同步设置

#### 第 1 步：身份验证

**问题**：“您是否希望将增量同步到 Azure DevOps 工作项？**

**如果回答“是”** → 继续进行身份验证设置：
- 组织 URL：`https://dev.azure.com/your-org`
- 个人访问令牌（PAT）：从 ADO 设置中生成
- 项目名称：`MyProject`
- 区域路径：（可选）用于多团队组织

**如果回答“否”** → 跳过 ADO 同步设置

#### 第 2 步：同步方向

**问题**：
```
"What should be the sync behavior between local increments (.specweave/) and Azure DevOps work items?"
```

**选项**：

**1. 双向同步（推荐）**
```
Local increments ↔ ADO Work Items

Features:
- Changes sync both ways automatically (on task completion)
- Conflicts: You will be prompted to resolve when both sides change
- Scope: Active increments only
- Example: Complete task in SpecWeave → ADO work item updates

Best for: Enterprise teams using Azure DevOps
```

**2. 仅导出（本地 → ADO）**
```
Local increments → ADO Work Items

Features:
- SpecWeave is source of truth, ADO is read-only mirror
- Changes push from local to ADO only
- ADO changes are ignored (must update locally)
- Example: Create increment in SpecWeave → ADO work item created automatically

Best for: Developers who prefer SpecWeave with ADO visibility
```

**3. 仅导入（ADO → 本地）**
```
ADO Work Items → Local increments

Features:
- ADO is source of truth, local workspace mirrors it
- Changes pull from ADO to local only
- Good for: Onboarding existing ADO projects
- Example: Update ADO work item → Local increment syncs

Best for: Migrating from ADO-first workflow to SpecWeave
```

**4. 仅手动同步**
```
Use /sw-ado:sync command when needed

Features:
- No automatic sync via hooks
- Full control over when sync happens

Best for: Advanced users or selective sync scenarios
```

---

## 实施注意事项

### 生成增量规划向导时

1. ✅ 检查 `config.plugins.enabled` 数组
2. ✅ 仅询问已启用的插件（GitHub/Jira/ADO）
3. ✅ 对于每个已启用的插件，询问：“本地 ↔ [提供者]” 的同步方向
4. ❌ 绝不要询问外部到外部的同步（例如，“GitHub ↔ Jira”）

### 配置存储

**密钥**（`.env` - 被 git 忽略）：
```bash
# GitHub
GITHUB_TOKEN=ghp_xxx

# Jira
JIRA_API_TOKEN=xxx
JIRA_EMAIL=user@example.com

# Azure DevOps
ADO_PAT=xxx
```

**配置**（`.specweave/config.json` - 提交到 git）：
```json
{
  "plugins": {
    "enabled": ["github", "jira", "ado"]
  },
  "sync": {
    "github": {
      "enabled": true,
      "direction": "bidirectional",
      "autoCreateIssue": true,
      "repo": "owner/repo"
    },
    "jira": {
      "enabled": true,
      "direction": "bidirectional",
      "domain": "company.atlassian.net",
      "projectKey": "PROJ"
    },
    "ado": {
      "enabled": true,
      "direction": "export-only",
      "organization": "your-org",
      "project": "MyProject"
    }
  }
}
```

---

## 同步工作流程

### 双向同步（自动）

**触发器**：任务完成钩子（`post-task-completion.sh`）

**流程**：
1. 用户在 SpecWeave 完成任务 → `tasks.md` 更新
2. 钩子检测到变化 → 读取增量元数据
3. 如果启用了 GitHub → 更新 GitHub 问题的进度
4. 如果启用了 Jira → 更新 Jira Epic 的状态
5. 如果启用了 ADO → 更新 ADO 工作项

**冲突解决**：
- 如果本地和外部都发生了变化 → 提示用户解决
- 显示差异：本地变化与外部变化
- 用户选择：保留本地更改、保留外部更改或合并

### 仅导出同步

**触发器**：任务完成钩子

**流程**：
1. 用户在 SpecWeave 完成任务
2. 钩子将更改推送到外部工具
3. 外部工具的更改被忽略（单向流程）

**使用场景**：SpecWeave 是权威数据源，外部工具是只读镜像

### 仅导入同步

**触发器**：手动运行 `/specweave-[tool]:sync` 命令

**流程**：
1. 用户运行同步命令
2. 从外部工具获取更改
3. 用外部数据更新本地增量
4. 本地更改不会被推送（单向流程）

**使用场景**：从外部工具导入现有项目

### 手动同步

**触发器**：明确运行的命令

**流程**：
1. 用户运行 `/sw-github:sync [increment-id]`
2. 选择方向：拉取、推送或双向
3. 执行同步操作
4. 向用户报告结果

**使用场景**：测试、一次性同步、高级控制

---

## 常见问题

### 问：如果同时启用了 GitHub 和 Jira 会怎样？

**答**：SpecWeave 会独立地将数据同步到两者：
```
.specweave/docs/specs/ ↔ GitHub Issues
.specweave/docs/specs/ ↔ Jira Epics
```

GitHub 和 Jira 之间不会相互同步。SpecWeave 是中心。

### 问：之后可以更改同步方向吗？

**答**：可以！编辑 `.specweave/config.json`：
```json
{
  "sync": {
    "github": {
      "direction": "export-only"  // Change from bidirectional
    }
  }
}
```

### 问：如果我手动删除了 GitHub 问题怎么办？

**答**：取决于同步方向：
- **双向**：SpecWeave 的增量会被标记为已删除（软删除）
- **仅导出**：下次同步时 GitHub 问题会重新创建
- **仅导入**：本地增量会被删除
- **手动**：在手动同步之前没有影响

### 问：如何导入现有的 GitHub 项目？

**答**：
1. 设置同步方向：**仅导入**
2. 运行：`/sw-github:import-all`
3. SpecWeave 会从 GitHub 问题创建增量
4. 根据需要审查和调整
5. 准备好后再切换到 **双向** 同步

### 问：可以仅同步特定的增量吗？

**答**：可以！使用手动同步：
```bash
/sw-github:sync 0042-auth-feature  # Sync specific increment
```

自动同步仅影响 **活跃的** 增量（未完成/已放弃的增量）。

---

## 故障排除

### 问题：运行 `/sw:increment` 后没有创建 GitHub 问题

**诊断**：
1. 检查 GitHub CLI：`gh auth status`
2. 检查配置：`.specweave/config.json` → `sync.github.autoCreateIssue: true`
3. 检查元数据：`.specweave/increments/####/metadata.json` 是否包含 `github` 部分

**解决方法**：
```bash
# Manual creation
/sw-github:create-issue 0042-auth-feature
```

### 问题：Jira Epic 未更新

**诊断**：
1. 检查 `.env` 中的 Jira 凭据
2. 检查 `config.json` 中的 Jira 域名和项目键
3. 检查同步方向（必须是双向或仅导出）
4. 检查钩子日志：`.specweave/logs/sync-*.log`

**解决方法**：
```bash
# Manual sync
/sw-jira:sync 0042-auth-feature --force
```

### 问题：双向同步时发生冲突

**诊断**：
- 本地和外部都修改了相同的字段（例如，状态）

**解决选项**：
1. **保留本地**：保留本地更改
2. **保留外部**：保留外部更改
3. **合并**：应用两种更改（手动解决）

**示例**：
```
⚠️  Conflict detected for increment 0042-auth-feature

Field: status
Local value: in-progress
GitHub value: completed

Choose resolution:
1. Keep local (in-progress)
2. Keep external (completed)
3. Merge manually

Your choice:
```

---

## 最佳实践

### 1. 从双向同步开始

大多数团队受益于双向同步：
- 开发者在 SpecWeave 中更新
- 项目经理/利益相关者在 GitHub/Jira 中跟踪进度
- 变更会自动同步

### 2. 对于独立项目使用仅导出同步

如果您独自工作且只需要在 GitHub 上查看进度：
- 设置方向为仅导出
- SpecWeave 是您的数据源
- GitHub 是只读镜像

### 3. 对于导入项目使用仅导入同步

在从 GitHub/Jira 迁移到 SpecWeave 时：
1. 先使用仅导入同步
2. 将所有现有工作导入 SpecWeave
3. 审查并整理数据
4. 确认无误后切换到双向同步

### 4. 在测试时使用手动同步

在测试或实验时：
- 禁用自动同步
- 使用手动命令
- 在启用自动同步之前验证行为

### 5. 坚持一个数据源

**黄金规则**：切勿同时手动编辑 SpecWeave 和外部工具中的相同字段。

**示例**：
- ❌ 错误做法：在 SpecWeave 和 GitHub 中手动更新任务状态
- ✅ 正确做法：在 SpecWeave 中更新，然后让同步结果传播到 GitHub

---

## 相关命令

### GitHub
- `/sw-github:sync [increment-id]` - 手动同步
- `/sw-github:create-issue [increment-id]` - 创建问题
- `/sw-github:close-issue [increment-id]` - 关闭问题
- `/sw-github:import-all` - 导入所有 GitHub 问题
- `/sw-github:status [increment-id]` - 检查同步状态

### Jira
- `/sw-jira:sync [increment-id]` - 手动同步
- `/sw-jira:create-epic [increment-id]` - 创建 Epic
- `/sw-jira:import-all` - 导入所有 Jira Epic
- `/sw-jira:status [increment-id]` - 检查同步状态

### Azure DevOps
- `/sw-ado:sync [increment-id]` - 手动同步
- `/sw-ado:create-workitem [increment-id]` - 创建工作项
- `/sw-ado:import-all` - 导入所有 ADO 工作项
- `/sw-ado:status [increment-id]` - 检查同步状态

---

**记住**：SpecWeave 是您的本地数据源。外部工具只是镜像。同步的目的是保持这些镜像的更新，而不是管理双重数据源。