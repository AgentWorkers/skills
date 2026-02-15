---
name: pr-review-loop
description: **具有 Greptile 功能的自动化 PR 审核流程**  
当代理创建一个 Pull Request（PR）时，可以使用此流程来自动处理代码审核反馈：读取 Greptile 提供的审核意见、修复问题、推送修复后的代码、重新触发审核流程，并在审核得分达到 4/5 分以上时自动合并代码。该流程可通过以下命令触发：`pr review {url}` 或 `review my PR`；同时，当 Greptile 的审核 Webhook 或轮询机制发送反馈时，流程也会自动启动。
---

# PR 审查循环

**自动流程**：Greptile 审查 PR → 代理根据反馈进行修复 → 推送代码 → 重新触发审查流程 → 重复此过程，直到评分达到 4/5 或达到最大轮次。

## 快速入门

当通过 PR 的 URL 或审查数据触发该流程时：

```bash
# Run the review loop
bash scripts/pr-review-loop.sh <owner/repo> <pr-number>
```

或者也可以手动执行这些步骤——详见下方说明。

## 工作流程

### 1. 获取审查信息

```bash
# Get latest Greptile review
gh api "/repos/{owner}/{repo}/pulls/{pr}/reviews" \
  --jq '[.[] | select(.user.login == "greptile-apps[bot]")] | last'

# Get inline comments
gh api "/repos/{owner}/{repo}/pulls/{pr}/comments" \
  --jq '[.[] | select(.user.login == "greptile-apps[bot]")]'
```

### 2. 解析评分

在审查内容中查找评分信息。Greptile 通常会显示类似 `Score: X/5` 或 `Confidence: X/5` 的评分。提取该评分：
- **评分 ≥ 4/5** → 自动合并代码
- **评分 < 4/5** → 修复问题
- **未找到评分** → 如果有评论，则认为代码需要修复；否则直接合并代码

### 3. 自动合并（评分 ≥ 4）

```bash
gh pr merge <number> --merge --delete-branch --repo <owner/repo>
```

### 4. 修复问题（评分 < 4）

对于 Greptile 提出的每一条评论：
1. 阅读相关文件和行号
2. 理解反馈内容
3. 应用相应的修复措施
4. 将修改内容提交到代码仓库

提交代码时，需要附上详细的说明，列出所有修复的内容：
```
Address Greptile review feedback (round N)

- Fix X in path/to/file.ts
- Fix Y in path/to/other.ts
- Improve Z per reviewer suggestion
```

**推送代码并重新触发审查流程**：
```bash
git push
gh pr comment <number> --repo <owner/repo> --body "@greptileai review"
```

### 5. 跟踪流程状态

在工作区维护 `review-state.json` 文件：
```json
{
  "owner/repo#123": {
    "rounds": 2,
    "maxRounds": 5,
    "lastScore": 3,
    "sameScoreCount": 1
  }
}
```

**每轮审查结束后更新状态**：
- **审查轮次 ≥ 5** → 无论如何都应合并代码，并通知项目负责人（Master）
- **连续两轮评分相同** → 无论如何都应合并代码，并通知项目负责人

### 6. 升级处理

- **涉及架构决策**（评论中提到架构、设计模式或可能破坏现有功能的变更） → 通过 Telegram 通知项目负责人，不要自动修复代码
- **达到最大审查轮次** → 合并代码并向项目负责人提交总结报告
- **反馈内容不明确** → 询问项目负责人的意见

## 命令接口

代理应响应以下命令：
- `pr review <url>` — 启动针对指定 PR 的审查流程
- `pr review <owner/repo#number>` — 根据提交者或仓库编号启动审查流程
- `pr status` — 显示当前正在进行的审查流程及其状态

## 参考资料

请参阅 `references/greptile-patterns.md`，了解常见的 Greptile 评审反馈模式和修复策略。