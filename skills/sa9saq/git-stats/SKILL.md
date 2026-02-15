---
description: 分析 Git 仓库的统计数据——包括贡献者排名、提交频率、文件变更情况以及活动模式。
---

# Git 统计

用于分析 Git 仓库的统计数据并生成可视化报告。

**适用场景**：审查项目活动、贡献者排名或识别代码热点区域。

## 前提条件**

- 需要一个 Git 仓库。
- 不需要 API 密钥。

## 操作步骤**

1. **验证仓库是否为 Git 仓库**：执行 `git rev-parse --is-inside-work-tree`；如果不是 Git 仓库，则立即退出程序。

2. **运行分析命令**：

   ```bash
   # Project overview
   echo "First commit: $(git log --reverse --format='%ai' | head -1)"
   echo "Latest commit: $(git log -1 --format='%ai')"
   echo "Total commits: $(git rev-list --count HEAD)"
   echo "Contributors: $(git shortlog -sn --all | wc -l)"
   echo "Branches: $(git branch -a | wc -l)"
   echo "Tags: $(git tag | wc -l)"

   # Top contributors
   git shortlog -sn --all | head -15

   # Commits per day
   git log --format='%ai' | cut -d' ' -f1 | sort | uniq -c | sort -rn | head -20

   # Commits by day of week
   git log --format='%ad' --date=format:'%A' | sort | uniq -c | sort -rn

   # Commits by hour
   git log --format='%ad' --date=format:'%H' | sort | uniq -c | sort -n

   # Most changed files (hotspots)
   git log --pretty=format: --name-only | sort | uniq -c | sort -rn | head -20

   # Lines added/removed per contributor
   git log --format='%aN' --numstat | awk '...'  # complex awk parsing
   ```

3. **输出格式**：
   ```
   ## 📊 Git Repository Stats
   **Repo:** <name> | **Period:** <first> → <last> | **Age:** X months

   ### 👥 Top Contributors
   | # | Author | Commits | % |
   |---|--------|---------|---|
   | 1 | Alice  | 342     | 45% |
   | 2 | Bob    | 210     | 28% |

   ### 📅 Activity Patterns
   - Busiest day: Wednesday (avg 4.2 commits)
   - Busiest hour: 14:00-15:00
   - Longest streak: 23 consecutive days

   ### 🔥 Hotspot Files (most changed)
   | File | Changes | Last Modified |
   |------|---------|--------------|
   | src/main.ts | 89 | 2025-01-10 |

   ### 📈 Monthly Trend
   | Month | Commits |
   |-------|---------|
   | 2025-01 | ████████ 42 |
   | 2024-12 | ██████ 31 |
   ```

4. **自定义日期范围**：支持使用 `--since` 和 `--until` 标志来过滤分析结果。

## 特殊情况处理**

- **空仓库**：报告“未找到任何提交记录”。
- **仅有一个贡献者**：跳过排名功能，重点关注代码活动模式。
- **仓库规模非常大（超过 10 万条提交记录）**：默认使用 `--since="1 year ago"` 来限制分析范围，并在报告中注明这一限制。
- **HEAD 指针指向的分支被分离（即该分支不再与其他分支关联）**：使用 `--all` 标志来包含所有分支。

## 故障排除**

- **作者重复**（同一人使用不同电子邮件地址）：建议使用 `.mailmap` 文件来消除重复记录。
- **在大型仓库上分析速度较慢**：可以添加 `--no-merges` 标志，并适当缩小日期范围以加快分析速度。