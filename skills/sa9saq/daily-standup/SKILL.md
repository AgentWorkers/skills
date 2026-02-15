---
description: 根据 Git 活动、待办事项（TODOs）以及项目状态生成每日站会报告。
---

# 每日站会（Daily Standup）

根据 Git 活动和项目状态自动生成站会报告。

## 指令

1. **收集 Git 活动**：
   ```bash
   # Yesterday's commits
   git log --since="yesterday 00:00" --until="today 00:00" --oneline --all --author="$(git config user.name)"

   # Today's commits
   git log --since="today 00:00" --oneline --all --author="$(git config user.name)"

   # Stats (24h)
   git log --since="24 hours ago" --shortstat --author="$(git config user.name)"

   # Files changed
   git log --since="24 hours ago" --name-only --pretty=format:"" | sort -u | grep .
   ```

2. **检查项目状态**：待办事项（TODO）文件、已打开的分支、未处理的 Pull Request（PR）

3. **生成报告**：
   ```
   ## 📋 Standup — 2025-02-08

   ### ✅ Done (Yesterday)
   - feat: Add user auth endpoint (abc1234)
   - fix: Resolve login timeout (#42)

   ### 🔨 In Progress
   - Working on payment integration (branch: feature/payments)
   - 3 files changed today

   ### 🚧 Blockers
   - Waiting on API key from vendor

   ### 📊 Stats (24h)
   - Commits: 5 | Files: 12 | +340/-89 lines
   ```

4. **多仓库管理**：
   ```bash
   for dir in ~/projects/*/; do
     [ -d "$dir/.git" ] || continue
     commits=$(git -C "$dir" log --since="24 hours ago" --oneline --author="$(git config user.name)" 2>/dev/null)
     [ -n "$commits" ] && echo "### $(basename $dir)" && echo "$commits"
   done
   ```

## 特殊情况处理

- **没有提交（No commits）**：报告“无活动”；询问团队成员是否在离线状态下完成了工作。
- **多个作者（Multiple authors）**：根据 `git config user.name` 进行过滤；如果该字段未设置，则进行特殊标记。
- **分离的 HEAD 分支或裸仓库（Detached HEAD / bare repos）**：优雅地跳过这些仓库的统计。
- **周末站会（Weekend standups）**：将统计时间范围调整为“自周五 00:00 起”。

## 需求

- 必须有 Git 仓库（支持任何类型的项目）。
- 不需要使用 API 密钥或依赖第三方服务。