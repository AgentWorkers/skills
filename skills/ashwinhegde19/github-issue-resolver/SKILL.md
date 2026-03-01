---
name: github-issue-resolver
description: >
  **具有安全防护机制的自主GitHub问题解决代理**  
  适用于用户希望发现、分析并修复GitHub仓库中的未解决问题时使用。该代理会在收到诸如“修复GitHub问题”、“解决仓库中的问题”或“处理GitHub漏洞”等请求时触发，或者在用户提供GitHub仓库URL并请求问题解决时启动。它支持从问题发现到提交Pull Request（PR）的完整工作流程，并通过安全防护机制防止范围蔓延（scope creep）、未经授权的访问以及危险操作的发生。
---
# GitHub 问题解决器

这是一个自主运行的代理程序，用于发现、分析和修复 GitHub 上的未解决问题——并配备了五层安全防护机制。

## ⚠️ 安全防护机制 — 请先阅读

**所有操作都必须经过安全防护机制的审核。** 在执行任何操作之前，系统会执行以下步骤：
1. 加载 `guardrails.json` 配置文件。
2. 验证操作的范围（仓库、分支、路径）。
3. 检查操作类型（自动执行、通知用户或需要用户批准）。
4. 验证所执行的命令是否在允许执行的命令列表中。
5. 将操作记录到审计日志中。

有关安全防护机制的详细信息，请参阅 [references/guardrails-guide.md](references/guardrails-guide.md)。

### 核心规则（不可更改）
- **严禁修改受保护的分支**（如 `main`、`master`、`production` 分支）。
- **严禁修改 `.env` 文件、敏感配置文件（如 secrets）、持续集成（CI）配置文件或凭据**。
- **严禁强制推送代码**。
- **未经明确批准，严禁修改依赖库文件**。
- **一次只处理一个问题**——完成当前问题后再开始处理新问题。
- **所有危险操作（如编写代码、提交更改、推送代码或创建 Pull Request）都需要用户批准**。
- **所有操作都会被记录到 `audit/` 目录中**。

---

## 工作流程

### 第一阶段 — 问题发现

**触发条件：** 用户提供 GitHub 仓库的地址（格式为 `owner/repo`）。

**操作步骤：**
1. **使用安全防护机制验证仓库**：
   ```bash
   python3 scripts/guardrails.py repo <owner> <repo>
   ```
   如果发现违规行为，立即通知用户并停止当前操作。

2. **使用推荐引擎获取问题信息、对问题进行评分，并以可视化的方式呈现给用户**：
   ```bash
   python3 scripts/recommend.py <owner> <repo>
   ```
   该引擎会自动获取所有未解决的问题，过滤掉 Pull Request，根据问题的严重性、影响程度、解决难度和更新频率对问题进行评分，并以统一的格式呈现给用户。
   **请务必使用 `recommend.py` 脚本**——切勿手动格式化问题信息。该脚本能确保每次展示的效果一致。
   （如需获取原始的 JSON 数据以供进一步处理，可参考：```bash
   python3 scripts/recommend.py <owner> <repo> --json
   ```）

**⏹️ 停止。等待用户选择问题。**

---

### 第二阶段 — 问题修复

**触发条件：** 用户选择了某个问题。

**操作步骤：**
1. **锁定所选问题**（每次只能处理一个问题）：
   ```bash
   python3 scripts/guardrails.py issue_lock <owner> <repo> <issue_number>
   ```

2. **阅读问题的完整讨论记录（包括所有评论）**。

3. **克隆仓库**（操作类型：`notify`）：
   ```bash
   python3 scripts/sandbox.py run git clone https://github.com/<owner>/<repo>.git /tmp/openclaw-work/<repo>
   ```

4. **创建一个用于修复问题的临时分支**（操作类型：`auto`）：
   ```bash
   python3 scripts/sandbox.py run git checkout -b fix-issue-<number>
   ```

5. **浏览代码库**——阅读相关文件。
   对于每个文件，执行以下操作：
   ```bash
   python3 scripts/guardrails.py path <file_path>
   ```

6. **向用户解释修复方案**：
   ```
   ## Proposed Fix
   - Problem: [root cause]
   - Solution: [what changes]
   - Files: [list of files and what changes in each]
   - Estimated diff size: [lines]
   ```

**⏹️ 停止。等待用户批准修复方案后再进行下一步操作。**

7. **实施修复**（操作类型：`approve`）：
   - 应用修复代码。
   - 检查代码差异的大小：`python3 scripts/guardrails.py diff <line_count>`
   - 记录操作日志：`python3 scripts/audit.py log_action write_code success`

---

### 第三阶段 — 测试

**修复完成后：**
1. **查找并运行相关测试**（操作类型：`notify`）：
   ```bash
   python3 scripts/sandbox.py run npm test   # or pytest, cargo test, etc.
   ```

2. **如果测试失败且 `autoRollbackOnTestFail` 选项被设置为 `true`：**
   - 恢复所有更改。
   - 通知用户。
   - 提出替代的修复方案。

3. **如果项目中没有测试用例**，则需要编写针对此次修复的简单测试用例。

4. **将测试结果报告给用户**。

---

### 第四阶段 — 创建 Pull Request 以供审核（必须获得用户批准）

**⚠️ 严禁自动创建 Pull Request。请务必先征得用户同意。**

**切勿在聊天中直接发送完整的代码差异内容。** 对于非简单的项目，应将修复后的分支推送到 GitHub，让用户在那里进行审核。在 GitHub 上，用户可以查看代码的高亮显示、逐文件的导航功能以及内联评论。

1. **提交更改**（操作类型：`approve`）：
   ```bash
   python3 scripts/sandbox.py run git add .
   python3 scripts/sandbox.py run git commit -m "Fix #<number>: <title>"
   ```

2. **以简洁的方式展示更改摘要**（不要显示原始的代码差异内容）：
   ```
   ## Changes
   - **src/models.py** — Added field validation (title length, enum checks)
   - **app.py** — Added validation to POST endpoint, 400 error responses
   - **tests/test_app.py** — 22 new tests covering validation rules
   - 4 files changed, ~100 lines of source + ~150 lines of tests
   - All tests passing ✅
   ```

3. **明确询问用户：**“准备好推送代码并创建 Pull Request 吗？”

4. **只有在用户同意后**（操作类型：`approve`），才能继续下一步操作：
   ```bash
   python3 scripts/sandbox.py run git push -u origin fix-issue-<number>
   python3 scripts/sandbox.py run gh pr create --draft --title "..." --body "..."
   ```
   注意：所有 Pull Request 都会默认创建为“草稿”状态。PR 正文中应包含所有更改的详细说明、测试结果以及问题的链接（用于关闭原问题：#N）。
5. **分享 Pull Request 的链接**，让用户在 GitHub 上进行审核。

6. **解锁问题**：
   ```bash
   python3 scripts/guardrails.py issue_unlock
   ```

---

## 脚本参考

| 脚本 | 功能 | 是否需要阅读脚本说明 |
|--------|---------|---------------------|
| `scripts/recommend.py` | 主要入口脚本——用于获取问题信息、评分和展示问题 | ✅ |
| `scripts/fetch_issues.py` | 用于获取问题的原始数据（供 `recommend.py` 内部使用） | ✅ |
| `scripts/analyze_issue.py` | 对单个问题进行深入分析 | ✅ |
| `scripts/create_pr.py` | 用于创建 Pull Request 的辅助脚本 | ✅ |
| `scripts/guardrails.py` | 安全防护机制的执行引擎 | ✅ |
| `scripts/sandbox.py` | 用于安全地执行命令的辅助脚本 | ✅ |
| `scripts/audit.py` | 用于记录操作日志的脚本 | ✅ |

## 参考资料

- [references/quick-reference.md](references/quick-reference.md) — GitHub API 参考、评分标准及测试命令说明
- [references/guardrails-guide.md](references/guardrails-guide.md) — 安全防护机制的完整文档及自定义设置指南