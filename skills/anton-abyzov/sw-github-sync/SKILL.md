---
name: github-sync
description: SpecWeave 规范与 GitHub 项目之间的双向同步（默认支持推送和拉取操作）。当需要了解 GitHub 集成设置、排查同步问题或配置同步选项时，请参考本文档。如需实际执行同步操作，请使用 `/sw-github:sync-spec` 命令。
---

# GitHub同步 - 双向规范 ↔ 项目同步

**目的**：实现SpecWeave规范与GitHub项目的无缝同步，以便团队成员能够清晰地了解项目进展并进行项目管理。

**默认行为**：**双向同步**（推送与拉取）——任一系统中的更改都会被自动同步。

**⚠️ 重要提示**：本文档仅提供关于GitHub同步的说明和指导。实际进行同步操作时，用户应直接使用`/sw-github:sync-spec`命令。该功能不应在用户调用该命令时自动激活。

## 何时激活该功能

✅ **在以下情况下激活**：
- 用户询问：“如何设置GitHub同步？”
- 用户询问：“需要哪些GitHub凭据？”
- 用户询问：“GitHub集成是如何工作的？”
- 用户需要帮助配置GitHub集成

❌ **在以下情况下不要激活**：
- 用户已经调用了`/sw-github:sync-spec`命令（该命令会自动处理同步）
- 命令正在运行中（避免重复调用）
- 任务完成钩子正在执行同步操作（属于自动流程）

**集成方式**：通过`/sw-github:sync-spec`命令实现同步。

---

## 正确的架构

**关键点**：SpecWeave将**规范（Specs）**同步到GitHub，而不是代码的增量更新！

---


**为什么选择同步规范而非代码增量？**
- ✅ **规范是永久性的文档**（用于记录功能相关的信息）
- ❌ **代码增量只是临时性的快照**（完成开发后可以删除）
- ✅ **GitHub应反映的是永久性的工作成果**，而非临时的开发阶段


---

## GitHub同步的工作原理

### 1. 从规范同步到GitHub项目（导出）

**触发条件**：规范创建或更新时

**操作步骤**：
1. 创建一个GitHub项目，内容如下：
   - 标题：`[SPEC-001] 核心框架与架构`
   - 描述：规范的概述及进度
   - 列表：待办事项（Backlog）、进行中（In Progress）、已完成（Done）
   - 将项目链接到相应的仓库

2. 将项目ID存储在规范的元数据中：
   ```yaml
   # .specweave/docs/internal/specs/spec-001.md (frontmatter)
   ---
   externalLinks:
     github:
       projectId: 123
       projectUrl: https://github.com/users/anton-abyzov/projects/123
       syncedAt: 2025-11-11T10:00:00Z
   ---
   ```

3. 为每个用户故事创建GitHub问题（Issue）：
   - 标题：`[US-001] 作为开发者，我希望通过NPM安装SpecWeave`
   - 问题描述中包含验收标准（以复选框的形式）
   - 添加标签：`user-story`、`spec:spec-001`、`priority:P1`
   - 将问题链接到相应的项目

**示例GitHub项目**：
```markdown
# [SPEC-001] Core Framework & Architecture

**Status**: In Progress (75% complete)
**Priority**: P0 (Critical)
**Feature Area**: Foundation & Plugin System

## Overview

The core framework and architecture spec covers SpecWeave's foundational capabilities:
- TypeScript-based CLI framework
- Plugin system architecture
- Cross-platform compatibility

## Progress

- ✅ US-001: NPM installation (Complete)
- ✅ US-002: Plugin system (Complete)
- ⏳ US-003: Context optimization (In Progress)
- ⏳ US-004: Intelligent agents (In Progress)

**Overall**: 2/4 user stories complete (50%)

---

🤖 Auto-synced by SpecWeave GitHub Plugin
```

### 2. 用户故事进度更新（从规范同步到GitHub）

**触发条件**：每个任务完成后（通过任务完成后的钩子）

**操作步骤**：
1. **更新GitHub问题**：
   - 更新验收标准对应的复选框状态
   - 用`[x]`标记已完成的验收标准
   - 更新问题描述
   - 更新问题标签（如`in-progress`、`testing`、`ready-for-review`）

2. **更新GitHub项目**：
   - 将问题卡片在列表中移动（待办事项 → 进行中 → 已完成）
   - 更新项目进度百分比
   - 发布进度评论

**示例问题更新**：
```markdown
**User Story**: US-001

As a developer, I want to install SpecWeave via NPM so that I can use it in my projects

## Acceptance Criteria

- [x] AC-001-01: `npm install -g specweave` works
- [x] AC-001-02: `specweave init` creates `.specweave/` structure
- [ ] AC-001-03: Version command shows current version (In Progress)

---

**Progress**: 2/3 ACs complete (67%)

🤖 Auto-updated by SpecWeave (2025-11-11)
```

### 3. 规范完成（关闭项目）

**触发条件**：所有用户故事都已完成

**操作步骤**：
1. 关闭所有相关的GitHub问题
2. 将GitHub项目归档
3. 发布最终评论：
   ```markdown
   ✅ **Spec Completed**

   **Final Stats**:
   - 35 user stories completed (100%)
   - 4 increments implemented (0001, 0002, 0004, 0005)
   - Duration: 6 weeks

   **Deliverables**:
   - Core framework architecture
   - Plugin system
   - Cross-platform CLI

   Spec complete. Project archived.

   ---
   🤖 Auto-closed by SpecWeave
   ```

### 4. 从GitHub项目同步到规范（导入）

**使用场景**：将现有的GitHub项目导入到SpecWeave规范中

**命令**：`/sw-github:import-project <项目编号>`

**操作步骤**：
1. 通过GitHub GraphQL API获取项目信息
2. 构建规范结构：
   - 将项目标题解析为规范标题
   - 将项目描述解析为规范概述
   - 将问题映射到用户故事
   - 将标签映射到相应的优先级
3. 生成包含用户故事和验收标准的spec.md文件
4. 将项目链接到规范的元数据中

---

## 配置

在`.specweave/config.json`文件中配置GitHub同步设置：

```json
{
  "plugins": {
    "enabled": ["specweave-github"],
    "settings": {
      "specweave-github": {
        "repo": "owner/repo",
        "autoSyncSpecs": true,
        "syncDirection": "two-way",
        "defaultLabels": ["specweave", "spec"],
        "syncFrequency": "on-change"
      }
    }
  }
}
```

---

## GitHub CLI要求

使用此功能需要安装并登录GitHub CLI（`gh`）：

```bash
# Install GitHub CLI
brew install gh              # macOS
sudo apt install gh          # Ubuntu
choco install gh             # Windows

# Authenticate
gh auth login

# Verify
gh auth status
```

---

## 手动同步操作

### 将规范同步到GitHub

```bash
/sw-github:sync-spec spec-001
```

**操作步骤**：
- 为spec-001创建或更新相应的GitHub项目。

### 同步所有规范

```bash
/sw-github:sync-spec --all
```

**操作步骤**：
- 将所有规范同步到GitHub项目中。

### 导入GitHub项目

```bash
/sw-github:import-project 123
```

**操作步骤**：
- 将GitHub项目#123导入到SpecWeave规范中。

### 检查同步状态

**操作步骤**：
- 查看同步状态（项目编号、上次同步时间、进度百分比）


---

## 工作流程集成

### 完全自动化的流程

```bash
# 1. Create spec (PM agent)
User: "Create spec for user authentication"
PM: Creates .specweave/docs/internal/specs/spec-005-user-auth.md

# 2. Auto-sync to GitHub (hook)
→ GitHub Project created automatically
→ Issues created for each user story

# 3. Implement increments
/sw:increment "Add login flow"
→ Increment 0010 created (implements US-001, US-002)

# 4. Work on tasks
/sw:do
→ Task completed
→ Hook fires
→ Spec updated (AC marked complete)
→ GitHub Project updated automatically

# 5. Complete spec
→ All user stories done
→ GitHub Project archived automatically
```

### 团队协作

**对于开发者**：
- 在本地使用SpecWeave规范进行开发
- GitHub项目会自动更新，确保团队成员随时掌握最新信息
- 无需手动管理项目

**对于项目经理**：
- 通过GitHub项目查看所有规范
- 在GitHub项目中跟踪项目进度
- 通过问题评论与开发者沟通

**对于利益相关者**：
- 通过熟悉的GitHub界面查看项目进度
- 无需了解SpecWeave的具体结构
- 清晰地了解功能开发的现状


## 冲突解决

**如果项目与规范之间存在差异怎么办？**

规范始终是信息的来源。GitHub项目只是为了提供透明度的镜像。

**同步冲突**（较为罕见）：
1. 规范的状态与项目状态不一致
2. 对项目/问题内容或标题进行了手动修改

**解决方法**：
- 运行`/sw-github:sync-spec spec-001 --force`命令，用规范中的信息覆盖项目中的数据
- 或者手动更新规范的元数据以匹配项目状态


## 隐私与安全

**同步的内容包括**：
- ✅ 规范的标题、概述、进度
- ✅ 用户故事及验收标准
- ✅ 用户故事的完成状态
- ❌ 代码差异或文件内容（不会被同步）
- ❌ 内部笔记或敏感数据

**安全措施**：
- 使用环境中的GitHub令牌（`GITHUB_TOKEN`或`GH_TOKEN`）
- 遵守仓库的读写权限设置
- 不会向第三方发送任何数据


## 好处

**对于SpecWeave用户**：
- 无需手动管理GitHub项目
- 自动同步团队信息
- 规范文档是信息的唯一来源
- 可在IDE之外直接使用GitHub集成功能

**对于团队**：
- 可在GitHub项目中跟踪SpecWeave的工作进展
- 如常使用里程碑、标签和分配者
- 通过问题评论与开发者沟通
- 实时查看项目进度

**对于组织**：
- 跨仓库统一项目跟踪
- 使用熟悉的GitHub工作流程
- 所有同步操作都有时间戳记录
- 支持与GitHub Actions和Webhooks的集成


## 故障排除

**项目未创建？**
- 检查GitHub CLI的登录状态：`gh auth status`
- 确认仓库的写权限
- 检查`.specweave/config.json`配置文件

**同步失败？**
- 检查网络连接是否正常
- 确认项目是否存在（未被删除）
- 检查GitHub的API调用频率限制：`gh api rate_limit`

**进度更新失败？**
- 检查配置文件中的`autoSyncSpecs`设置是否为`true`
- 查看日志文件`.specweave/logs/hooks-debug.log`
- 手动执行同步操作：`/sw-github:sync-spec spec-001`

---

## 高级用法

### 自定义项目模板

创建`.specweave/github/project-template.md`文件：

```markdown
# [{{spec.id.toUpperCase()}}] {{spec.title}}

{{spec.overview}}

## SpecWeave Details

- **Spec**: [spec.md]({{spec.url}})
- **Priority**: {{spec.priority}}
- **Feature Area**: {{spec.featureArea}}

## User Stories

{{spec.userStories.map(us => `- ${us.id}: ${us.title}`).join('\n')}}
```

### 选择性同步

**操作步骤**：
- 仅同步特定的规范


### 多仓库同步

**操作步骤**：
- 对于包含多个GitHub仓库的单个项目库，执行相应的同步操作


---

**相关功能**

- **github-issue-tracker**：通过问题评论来跟踪具体任务（已弃用，建议使用规范同步）
- **github-manager agent**：用于自动化GitHub操作的AI代理
- **命令**：`/sw-github:sync-spec`、`/sw-github:import-project`、`/sw-github:status`

---

**版本**：2.0.0（基于规范的架构）
**插件**：`specweave-github`
**最后更新时间**：2025-11-11