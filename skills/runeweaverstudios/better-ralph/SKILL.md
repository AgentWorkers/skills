---
name: better-ralph
description: "执行一次“Better Ralph”迭代：采用基于产品需求文档（PRD）的自动化编码流程。具体步骤如下：  
1. 读取 `prd.json` 文件；  
2. 选择下一个需要实现的功能或任务；  
3. 实现该功能或任务；  
4. 运行相关检查；  
5. 提交代码更改；  
6. 标记该功能或任务为“已完成”；  
7. 记录实施进度。  

整个过程仅使用标准的 OpenClaw 工具（如 `read`、`write`、`exec`、`git`）。  
触发条件包括：  
- 执行 `run better ralph` 命令；  
- 开始新的 “Better Ralph” 迭代；  
- 选择下一个需要处理的功能或任务；  
- 进入 “Ralph 循环”（持续执行编码和检查流程）。"
user-invocable: true
---

# Better Ralph – 单次迭代（OpenClaw）

执行 **一次** Better Ralph 工作流程：选择下一个 PRD 任务，实现它，运行质量检查，提交代码，更新 PRD 文件，并记录进度。仅使用标准工具（`read_file`、`write_file`、`edit`、`exec`、`git`），无需外部运行器或 Aether-Claw。

---

## 使用场景

- 用户请求：“运行 Better Ralph”、“执行一次 Better Ralph 迭代”、“选择下一个 PRD 任务”、“继续处理 PRD 中的任务”。
- 项目的工作空间根目录下存在一个 `prd.json` 文件（具体格式见下文）。

---

## 单次迭代工作流程

按以下步骤依次操作，**仅** 使用标准的文件处理工具（`read_file`、`exec`、`git`）：

### 1. 读取当前状态

- **读取** `prd.json` 文件（位于工作空间根目录）并解析其内容。
- 如果存在 `progress.txt` 文件，也请读取它。如果文件开头（直到下一个 `##` 标签或文件末尾）有 `## Codebase Patterns` 部分，将其作为实现代码时的参考；否则忽略该部分。

### 2. 选择下一个任务

- 从 `prd.json.userStories` 中找到所有 `passes` 为 `false` 的任务。
- 按优先级升序排序（数字越小，优先级越高）。
- 选择 **第一个** 未完成的任务。
- 如果所有任务的 `passes` 都为 `true`，则回复：“所有 PRD 任务都已完成，无需继续处理。” 并结束流程。

### 3. 确认当前 Git 分支

- 查看当前 Git 分支（例如使用 `git branch --show-current` 命令）。
- 如果 `prd.json` 中指定了 `branchName` 且与当前分支不同，切换到该分支（例如 `git checkout -b <branchName>`）。

### 4. 实现任务

- 选择的任务包含以下信息：`id`、`title`、`description`、`acceptanceCriteria`、`priority`、`passes`。
- 根据 `acceptanceCriteria` 中的要求编写或修改代码。
- **仅** 处理当前任务，不要开始下一个任务。

### 5. 运行质量检查

- 运行项目的质量检查命令（例如 `npm test`、`npm run lint`、`npm run typecheck` 等）。
- 如果有任何检查失败，请 **不要** 提交代码。告知用户具体是哪个检查失败，并停止当前流程。对于失败的任务，不要更新 `prd.json` 或 `progress.txt`。

### 6. 提交代码（仅当检查通过时）

- 将所有更改添加到暂存区（例如 `git add -A`）。
- 提交代码时，提交信息应为：`feat: [任务 ID] - [任务标题]`  
  例如：`feat: US-002 - 在任务卡片上显示优先级`。

### 7. 在 `prd.json` 中标记任务完成

- 重新读取 `prd.json` 文件（以防文件有更新）。
- 找到刚刚完成的任务，并将其 `passes` 属性设置为 `true`。
- 将更新后的 `prd.json` 文件写回原位置（保持文件结构和其他字段不变，仅修改 `passes` 属性）。

### 8. 记录进度到 `progress.txt`

- 在 `progress.txt` 文件中添加新的进度记录（不要覆盖原有内容），格式如下：

```
## [Current date/time] - [Story ID]
- What was implemented (1–2 sentences)
- Files changed (list paths)
- **Learnings for future iterations:**
  - Patterns or gotchas (e.g. "this codebase uses X for Y", "remember to update Z when changing W")
---
```

- 如果 `progress.txt` 文件不存在，先创建一个文件，第一行写 `# Better Ralph Progress`，然后再添加上述进度记录。

### 9. 向用户报告

- 告知用户已完成的任务（包括 ID 和标题），以及已更新的 PRD 文件和进度情况。
- 如果仍有任务的 `passes` 为 `false`，则提示用户：“请再次运行流程以处理下一个任务”；如果所有任务都已完成，则说明：“所有 PRD 任务均已完成。”

---

## prd.json 文件格式

如果用户需要 **创建**一个新的 `prd.json` 文件（文件尚不存在），请按照以下格式编写：

```json
{
  "project": "ProjectName",
  "branchName": "ralph/feature-kebab-case",
  "description": "Short feature description",
  "userStories": [
    {
      "id": "US-001",
      "title": "Short title",
      "description": "As a [role], I want [thing] so that [benefit].",
      "acceptanceCriteria": [
        "Verifiable criterion 1",
        "Verifiable criterion 2",
        "Typecheck passes"
      ],
      "priority": 1,
      "passes": false,
      "notes": ""
    }
  ]
}
```

- **priority**：数字越小，优先级越高。任务按依赖关系排序（例如，先处理基础功能相关的任务）。
- **passes**：初始值为 `false`；只有在任务实现并提交后才能设置为 `true`。
- **acceptanceCriteria**：每个检查项都必须可验证（例如：“类型检查通过”、“测试通过”）。

---

## Codebase Patterns（progress.txt）

可选地在 `progress.txt` 文件的开头添加一个 **Codebase Patterns** 部分，以便后续迭代或下次运行时参考：

```
# Better Ralph Progress

## Codebase Patterns
- Use X for Y in this codebase
- Always run Z after changing W
- Tests require PORT=3000

---
```

在每次迭代开始时，请阅读 `progress.txt` 中的这一部分。如果发现可复用的代码模式，请将其添加到这里（只需修改文件开头部分，其他内容保持不变）。不要将特定于任务的详细信息放入 `Codebase Patterns` 中。

---

## 规则

- **每次迭代只处理一个任务**，不要同时处理多个任务。
- **未通过质量检查的代码不得提交**。
- 如果未提交代码（例如检查失败），请不要将任务标记为完成。
- **仅在进度更新时追加记录到 `progress.txt`，切勿替换整个文件**（除非是首次创建文件）。
- 更改内容应 **最小化**，且仅针对当前任务的验收标准进行。

---

## 检查清单（单次迭代）

- [ ] 已读取 `prd.json`、`progress.txt`（以及 `Codebase Patterns` 文件，如果有的话）
- [ ] 选择了下一个 `passes` 为 `false`、优先级最低的任务
- [ ] 当前 Git 分支与 `prd.json` 中指定的 `branchName` 一致
- [ ] 任务已实现且所有验收标准均满足
- [ ] 质量检查通过（测试/代码检查/类型检查）
- [ ] 使用 `feat: [任务 ID] - [任务标题]` 作为提交信息
- [ ] 已将任务的 `passes` 属性设置为 `true` 在 `prd.json` 中
- [ ] 已将进度记录添加到 `progress.txt` 文件中