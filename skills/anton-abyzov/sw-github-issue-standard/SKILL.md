---
name: github-issue-standard
description: SpecWeave 创建的所有 GitHub 问题的强制性格式标准：这些问题需要具备可验证的验收标准以及完整的元数据。在创建 GitHub 问题、格式化问题内容或确保问题结构的一致性时，请遵循此标准。该标准适用于用户故事（user stories）、大型项目（epics）、功能需求（features）以及开发过程中的小步骤（incidents）。
---

# GitHub 问题标准格式（通用格式）

**紧急（CRITICAL）**：这是 SpecWeave 创建的所有 GitHub 问题的**强制**格式，适用于以下类型：
- 用户故事（单独的 us-*.md 文件）
- 特性（Epics/Features，即 FS-* 文件夹）
- 增量版本（Increments，即 0001-* 文件夹）
- 规范文档（Specs，即 spec-*.md 文件）

## 问题标题格式（强制要求）

### ✅ 允许的标题格式仅限于以下几种

```
[FS-XXX][US-YYY] User Story Title    ← STANDARD (User Stories)
[FS-XXX] Feature Title               ← Rare (Feature-level only)
```

**示例**：
- ✅ `[FS-059][US-003] 钩子优化（P0）`
- ✅ `[FS-054][US-001] 修复重新打开时的同步问题（P0）`
- ✅ `[FS-048] 智能分页功能`

### ❌ 禁用的标题格式（绝对禁止使用）

```
[BUG] Title                          ← WRONG! Bug is a LABEL, not title prefix
[HOTFIX] Title                       ← WRONG! Hotfix is a LABEL
[FEATURE] Title                      ← WRONG! Feature is a LABEL
[DOCS] Title                         ← WRONG! Docs is a LABEL
[Increment XXXX] Title               ← DEPRECATED! Old format
```

**为什么？** 像 `[BUG]` 这样的基于类型的标题前缀会破坏问题的可追溯性：
- 无法链接到相应的特性文档（FS-XXX）
- 无法链接到用户故事（US-YYY）
- 违反 SpecWeave 的数据流规则：`增量版本 → 实时文档 → GitHub`

**应如何处理？**
1. 将工作内容链接到实时文档中的相应特性（FS-XXX）。
2. 在该特性下创建用户故事（US-YYY）。
3. 使用 GitHub 的**标签**进行分类：`bug`（错误）、`enhancement`（增强）、`hotfix`（紧急修复）。

### 验证规则

GitHub 客户端（`github-client-v2.ts`）会执行以下验证：
- 拒绝以 `[BUG]`、`[HOTFIX]`、`[FEATURE]` 等开头的标题。
- 拒绝过时的 `[Increment XXXX]` 格式。
- 仅允许 `[FS-XXX][US-YYY]` 或 `[FS-XXX]` 格式的标题。

---

## 标准格式要求

每个 GitHub 问题必须包含以下内容：

1. **可验证的验收标准**：
   - 使用 GitHub 任务复选框格式：`- [x]` 或 `- [ ]`
   - 包括验收标准的 ID、描述、优先级和是否可测试的标志。
   - 示例：`- [x] **AC-US4-01**：描述（P1，可测试）`

2. **可验证的任务**：
   - 使用 GitHub URL 链接到增量版本的任务文档（不要使用相对路径）。
   - 使用 GitHub 任务复选框格式。
   - 示例：`- [x] [T-008: 标题](https://github.com/owner/repo/tree/develop/.specweave/increments/0031/tasks.md#t-008-title)`

3. **有效的 GitHub 链接**（版本 5.0.0 及以上）：
   - 特性链接：`https://github.com/owner/repo/tree/develop/.specweave/docs/internal/specs/{project}/FS-031`
   - 用户故事链接：`https://github.com/owner/repo/tree/develop/.specweave/docs/internal/specs/{project}/FS-031/us-004-*.md`
   - 任务链接：`https://github.com/owner/repo/tree/develop/.specweave/increments/0031/tasks.md#task-anchor`
   - 增量版本链接：`https://github.com/owner/repo/tree/develop/.specweave/increments/0031`

   **注意**：特性 ID 是从增量版本号（如 0031）派生而来的（例如，0031 → FS-031）。

4. **提取的优先级**：
   - 从验收标准中提取优先级（优先级越高越优先：P1 > P2 > P3）
   - 仅显示存在优先级的情况（不要显示“undefined”）。
   - 示例：`**优先级**：P1`

5. **禁止使用的项目字段**：
   - 不要包含 `**Project**：...`——GitHub 问题中不需要这个字段。
   - 项目名称由仓库上下文自动确定。

### 禁止使用的格式：
- 禁止使用相对路径（如 `../../{project}/FS-031`）
- 禁止使用未定义的值（如 `**Priority**: undefined`）
- 禁止在元数据中设置项目字段
- 禁止使用纯文本列表项作为验收标准或任务列表项（必须使用复选框）

## 实现细节

### UserStoryContentBuilder（参考实现）

**文件**：`plugins/specweave-github/lib/user-story-content-builder.ts`

这是**黄金标准**实现方式。所有其他构建工具都必须遵循这一模式。

**关键特性**：
```typescript
// 1. Accept GitHub repo parameter
async buildIssueBody(githubRepo?: string): Promise<string>

// 2. Auto-detect repo from git remote
private async detectGitHubRepo(): Promise<string | null>

// 3. Extract priority from ACs
private extractPriorityFromACs(criteria: AcceptanceCriterion[]): string | null

// 4. Generate GitHub URLs (not relative) - v5.0.0+: No _features folder
const featureUrl = `https://github.com/${repo}/tree/develop/.specweave/docs/internal/specs/${project}/${featureId}`;

// 5. Convert task links to GitHub URLs
if (repo && taskLink.startsWith('../../')) {
  const relativePath = taskLink.replace(/^\.\.\/\.\.\//, '.specweave/');
  taskLink = `https://github.com/${repo}/tree/develop/${relativePath}`;
}
```

### 模板

```markdown
**Feature**: [FS-031](https://github.com/owner/repo/tree/develop/.specweave/docs/internal/specs/{project}/FS-031)
**Status**: complete
**Priority**: P1

---

## User Story

**As a** user
**I want** feature
**So that** benefit

📄 View full story: [`us-004-name.md`](https://github.com/owner/repo/tree/develop/.specweave/docs/internal/specs/{project}/FS-031/us-004-name.md)

---

## Acceptance Criteria

Progress: 4/6 criteria met (67%)

- [x] **AC-US4-01**: Description (P1, testable)
- [x] **AC-US4-02**: Description (P1, testable)
- [ ] **AC-US4-03**: Description (P2, testable)
- [ ] **AC-US4-04**: Description (P2, testable)

---

## Implementation Tasks

Progress: 3/6 tasks complete (50%)

**Increment**: [0031-name](https://github.com/owner/repo/tree/develop/.specweave/increments/0031-name)

- [x] [T-008: Title](https://github.com/owner/repo/tree/develop/.specweave/increments/0031/tasks.md#t-008-title)
- [x] [T-009: Title](https://github.com/owner/repo/tree/develop/.specweave/increments/0031/tasks.md#t-009-title)
- [ ] [T-010: Title](https://github.com/owner/repo/tree/develop/.specweave/increments/0031/tasks.md#t-010-title)

---

🤖 Auto-synced by SpecWeave
```

## 实现机制

所有 GitHub 问题的内容都是由以下构建工具生成的：

1. **UserStoryIssueBuilder**（`plugins/specweave-github/lib/user-story-issue-builder.ts`）：
   - 从 `us-*.md` 文件创建问题。
   - 生成 `[FS-XXX][US-YYY]` 格式的标题。
   - 从验收标准中提取信息并转换为复选框。
   - 使用 GitHub 的绝对路径。

2. **GitHubFeatureSync**（`plugins/specweave-github/lib/github-feature-sync.ts`）：
   - 将特性同步为 GitHub 的里程碑。
   - 通过 UserStoryIssueBuilder 将用户故事同步为 GitHub 问题。
   - 实现统一的层级结构：特性 → 里程碑 → 用户问题。

### 命令

所有 GitHub 同步命令都遵循统一的层级结构：
- `/sw-github:sync`：通过特性/用户故事层级同步增量版本。
- `/sw-github:create-issue`：使用标准格式创建问题。
- `/sw-github:update-user-story`：更新用户问题。

## 验证检查清单

在创建或更新 GitHub 问题时，请确保：
- 特性链接是可点击的 GitHub URL（不要使用相对路径）。
- 用户故事链接是可点击的 GitHub URL。
- 所有任务链接都是可点击的 GitHub URL。
- 验收标准可以被选中/取消选中（GitHub 界面中的复选框功能正常工作）。
- 任务可以被选中/取消选中（GitHub 界面中的复选框功能正常工作）。
- 优先级显示实际值（P1/P2/P3），或者不显示优先级。
- 不要出现“Project: undefined”字段。
- 进度百分比显示正确。
- 增量版本链接是可点击的 GitHub URL。

## 好处：
- ✅ **链接有效**：不再使用错误的相对路径。
- ✅ **可验证**：验收标准和任务可以在 GitHub 界面中直接进行勾选/取消勾选。
- ✅ **元数据清晰**：没有未定义的值干扰问题信息。
- ✅ **格式统一**：所有类型的问题都采用相同的格式。
- ✅ **可追溯**：可以直接链接到仓库中的源文件。

## 使用建议

**始终使用！** 这是 SpecWeave 创建的所有 GitHub 问题的唯一允许的格式。
没有例外，也没有捷径。所有问题都必须遵循这一标准。

## 相关文件：
- **用户故事构建工具**：`plugins/specweave-github/lib/user-story-issue-builder.ts`
- **特性同步工具**：`plugins/specweave-github/lib/github-feature-sync.ts`
- **示例问题**：`https://github.com/anton-abyzov/specweave/issues/501`