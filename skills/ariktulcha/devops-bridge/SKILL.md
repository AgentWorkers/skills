---
name: devops-bridge
description: >
  **统一开发操作平台**  
  该平台能够将 GitHub、持续集成/持续部署（CI/CD，如 GitHub Actions）、Slack、Discord 以及问题跟踪工具（如 Linear、Jira、GitHub Issues）连接起来，形成跨工具的自动化工作流程。它具备以下功能：  
  - 向 Slack 发送包含详细测试失败信息的 CI 失败通知；  
  - 跟踪 Pull Request（PR）的审核流程，并在需要时发送提醒；  
  - 生成每日开发团队会议摘要；  
  - 在 PR 合并时同步问题状态；  
  - 检测存在问题的测试用例；  
  - 监控仓库的健康状况。  
  **应用场景：**  
  - PR 审核提醒；  
  - CI 构建警报；  
  - 了解仓库中的最新动态；  
  - 查找失败的构建任务；  
  - 确认谁需要审核；  
  - 开发团队会议总结；  
  - 部署通知；  
  - 仓库监控；  
  - 将 GitHub 与 Slack 连接起来；  
  - 将 PR 与 Jira/Linear 票据关联；  
  - 代码审查跟踪；  
  - 合并冲突警报；  
  - 以及其他需要整合开发工具的场景。  
  **注意事项：**  
  - 如果用户同时提及 GitHub 和 Slack（或任意两个开发工具），该平台会自动将它们连接起来。
metadata:
  openclaw:
    emoji: "🔧"
---
# DevOps Bridge

这是连接您开发工具之间的缺失环节。该工具将 GitHub、CI/CD、Slack/Discord 和问题跟踪器整合到统一的工作流程中，让您无需在多个浏览器标签页之间来回切换。

## 为何需要这个工具

开发者已经分别使用不同的工具来管理 GitHub、Slack 等平台，但至今还没有一个工具能够自动完成以下操作：当 CI 测试失败时，将其与相关的 PR 关联起来，通知相应的 Slack 频道，并更新问题跟踪器中的状态。DevOps Bridge 就是这个桥梁。

## 核心功能

### 1. 智能通知

将 GitHub 上的复杂事件转化为易于理解、信息丰富的通知。例如，当构建失败时，通知内容会包含具体的失败原因（如：“某个测试用例失败了”）：

```
🔴 CI Failed — PR #142 "Add OAuth flow" by @alice
  └─ Test: auth.test.ts:47 — Expected 200, got 401
  └─ Last passing commit: abc1234 (2 hours ago)  
  └─ Linked issue: LINEAR-389 "Implement SSO"
  └─ Action: Reply "fix" to see the failing test, "logs" for full output
```

发送通知时，请务必：
- 包括 PR 的标题和作者，而不仅仅是编号
- 提供具体的失败测试用例的链接，而不仅仅是简单的“CI 失败”
- 提及最后一次成功的提交信息，以便快速定位问题
- 如果存在相关的问题或工单，会进行交叉引用
- 建议下一步应采取的具体操作

### 2. PR 审查管理

跨多个工具跟踪 Pull Request 的生命周期：

**审查提醒**：
- 每日扫描待审的 PR，并标记出需要审查的 PR
- 根据延迟时间进行分级提醒：24 小时后发送温和的提醒，48 小时后发送更强烈的提醒，72 小时后发送紧急提醒
- 通过 Slack/Discord 的私信或频道向指定的审阅者发送提醒
- 通知格式如下：
  ```
  👀 Review needed:
  • PR #142 "Add OAuth flow" — waiting 3 days (assigned: @bob)
  • PR #156 "Fix pagination" — waiting 1 day (assigned: @carol)
  ```

**审查状态同步**：
- 当 PR 在 GitHub 上被批准时，会在团队频道中发布通知
- 当需要修改代码时，直接通知作者
- 当所有测试通过并得到批准后，提示：“可以合并了——需要我帮忙合并吗？”

### 3. 智能的 CI/CD 分析

提供比简单的“通过/失败”更详细的分析：
- **失败原因汇总**：如果多个 PR 在同一个测试用例上失败，将其视为系统性问题，而不是单独发送通知
- **测试稳定性检测**：如果某个测试用例在不同 PR 中反复失败，会标记出来：“该测试用例本周已在多个 PR 中失败 3 次——可能是不稳定”
- **构建耗时分析**：“这次构建耗时 45 分钟，而通常只需要 20 分钟——可能存在问题”
- **自动重试建议**：对于已知不稳定的测试用例，建议或触发自动重试

### 4. 问题跟踪器同步

保持问题跟踪器（如 Linear、Jira、GitHub Issues）与实际开发活动的同步：
- 当 PR 引用了某个问题时（例如：“修复了问题 #123”），会自动更新问题的状态
- 当 PR 被合并时，会将相关问题标记为“已完成”或“正在审查中”
- 当 PR 关联的问题导致 CI 失败时，会在问题跟踪器中添加注释说明失败原因
- 识别出“孤立”的 PR（即没有关联问题的 PR）：“PR #167 没有引用任何问题——是否应该关闭它？”

### 5. 日度开发总结

根据需要或通过定时任务生成团队级别的开发总结：

```
🧑‍💻 Dev Standup — [Date]

Merged yesterday:
  • PR #140 "Refactor auth module" by @alice → LINEAR-385 closed
  • PR #143 "Update deps" by @bob

In review:
  • PR #142 "Add OAuth flow" by @alice — 2 approvals, CI passing ✅
  • PR #156 "Fix pagination" by @carol — changes requested by @bob

Blocked:
  • PR #158 "Migrate DB" by @dave — CI failing (migration timeout)
  • Issue LINEAR-402 — no assignee, due tomorrow

CI Health: 87% pass rate (down from 94% last week)
  └─ Flaky: auth.test.ts (failed 4/10 runs)
```

## 配置要求

### 必需工具
- `gh` CLI（GitHub 命令行工具）——用于查询仓库活动、PR 状态等
- 至少配置一个消息传递渠道（Slack、Discord、Telegram）

### 可选工具
- Linear CLI 或 API——用于管理 Linear 的问题跟踪
- Jira API——用于与 Jira 集成
- GitHub Issues——与 `gh` 的集成非常简单

### 设置流程

首次使用时，需要交互式地配置以下参数：
1. **监控哪些仓库？** 可以选择具体仓库，或使用“我具有推送权限的所有仓库”
2. **将通知发送到哪里？** 可以选择 Slack、Discord、Telegram 或同时发送到多个渠道
3. **提醒的频率如何？** 可以选择温和（72 小时一次）、中等（48 小时一次）或频繁（24 小时一次）
4. **是否包含 CI 详细信息？** 有些用户需要完整的日志，有些用户只需要知道结果（通过/失败）
5. **团队成员信息**：将 GitHub 用户名映射到 Slack/Discord 的昵称，以便在通知中提及

配置信息会保存在工作区内存中，以便后续使用。

### 定时任务设置

提供以下默认的定时任务方案（用户可自行调整）：

```json
[
  {
    "name": "Morning dev digest",
    "schedule": "0 9 * * 1-5",
    "prompt": "Generate dev standup summary for my repos"
  },
  {
    "name": "PR review reminder",  
    "schedule": "0 14 * * 1-5",
    "prompt": "Check for PRs waiting for review and send reminders"
  },
  {
    "name": "End of day CI report",
    "schedule": "0 17 * * 1-5",
    "prompt": "Summarize today's CI/CD activity and flag any issues"
  }
]
```

## 命令参考

用户可以使用自然语言来触发特定操作：

| 用户指令 | 功能 |
|-----------|--------|
| “我的仓库里发生了什么？” | 查看所有监控仓库的完整活动总结 |
| “有哪些构建失败了？” | 检查 CI 的状态，并显示失败的具体原因 |
| “谁需要审阅？” | 列出待审的 PR，包括延迟时间和负责人 |
| “生成每日开发总结” | 生成每日开发总结 |
| “通知 #dev-team 关于 PR 142” | 发送关于特定 PR 的格式化通知 |
| “将 PR 142 与 LINEAR-389 关联起来” | 在 PR 和相关问题之间建立关联 |
| “为仓库 X 配置 CI 警报” | 为指定仓库配置监控设置 |
| “合并 PR 142” | 如果所有测试通过并得到批准，则执行合并；否则发出警告 |

## 特殊情况处理

- **单仓库项目**：如果监控的是单仓库项目，建议按目录或团队分组通知
- **分支仓库**：如果 PR 来自分支仓库，请明确标注
- **草稿 PR**：除非用户要求，否则不发送审阅提醒
- **长时间未处理的 PR**：如果 PR 开放超过 7 天且没有活动，建议关闭或重新提交
- **GitHub API 的使用限制**：GitHub API 有使用频率限制，请批量请求并缓存结果
- **未配置消息传递渠道**：如果未配置 Slack/Discord/Telegram，会将通知内容输出到当前的对话窗口
- **多个 GitHub 组织**：如果用户管理多个 GitHub 组织的仓库，请分别处理，但需明确标注

## 集成方式

该工具与其他已安装的工具配合使用效果最佳：
- 当检测到相关操作时，可以将其与 `github skill` 集成，将原始的 GitHub 操作委托给 DevOps Bridge 处理
- 与 `slack skill` 集成时，由 DevOps Bridge 负责消息的发送
- 与 `daily-briefing-hub` 集成时，可以将开发活动数据添加到每日简报的“开发活动”部分