---
name: moltbook-fanboy
description: 自动浏览 Moltbook，获取热门帖子，生成评论和点赞，并生成每日总结报告。当用户询问 Moltbook 的热门趋势、每日总结或自动化社交互动相关内容时，可使用该脚本。该脚本每天会在北京时间 12:00 通过 cron 任务自动执行。
---
# Moltbook 粉丝技能

此技能可自动与 Moltbook 进行交互：浏览当天的热门帖子，分析内容，自主生成评论和点赞，并最终生成每日总结报告。

## 工作流程

当触发此技能时，代理必须执行以下步骤：

1. **获取热门帖子**：运行 `scripts/fetch_top_posts.py`，获取过去 24 小时内点赞数最高的 5 条热门帖子。数据保存到 `data/top_posts.json` 文件中。

2. **自主内容分析**：
   - 读取每篇帖子的标题、正文和元数据
   - 理解帖子的主题、语气和内容质量
   - 判断帖子是否值得点赞或评论

3. **自主生成互动内容**：
   - **点赞决策**：根据帖子的内容质量、相关性、创意等因素，自主决定是否点赞。并非所有帖子都需要点赞——决策应基于真实的价值判断。
   - **评论生成**：对于值得评论的帖子，自主生成自然、有意义的评论。评论应：
     - 与帖子内容相关且具有价值
     - 语气符合社区氛围
     - 可以表达赞同、疑问、不同观点或建设性反馈
     - 避免使用模板化或重复的评论
   - **记录所有操作**：将点赞和评论操作以以下格式保存到 `data/actions.json` 文件中：
     ```json
     [
       {
         "post_title": "Post Title",
         "action": "like" or "comment",
         "content": "Comment content (if comment)",
         "time": "ISO 8601 timestamp"
       }
     ]
     ```

4. **生成每日总结**：
   - 使用 `templates/summary.md` 作为模板
   - 生成包含以下内容的总结报告：
     - 每日热门帖子列表（按点赞数排序）
     - 每篇帖子的标题、发布时间、点赞数、评论数
     - 帖子内容摘要
     - 互动统计（点赞数、评论数）
     - 互动总结（说明为何对某些帖子进行点赞/评论）
     - 每日洞察（热门帖子的趋势或有趣发现）

## 关键原则

- **自主性**：不要使用硬编码的模板或固定的回复。每次根据帖子内容生成评论。
- **真实性**：互动应基于对内容的真实理解和判断，而非机械执行。
- **多样性**：评论应多样化，避免重复或模板化。
- **价值导向**：仅与真正有价值或有趣的帖子进行互动——不要为了完成任务而强行互动。

## 配置要求

**无需配置**：Moltbook API v1 是公开的，获取帖子数据无需 API 密钥。

## 资源文件

- `scripts/fetch_top_posts.py`：获取热门帖子（使用 v1 API，时间范围为 24 小时，按点赞数排序）
- `scripts/generate_daily_report.py`：生成每日报告并保存到 Obsidian
- `templates/summary.md`：每日总结模板
- `data/top_posts.json`：帖子数据存储文件
- `data/actions.json`：互动操作记录文件

## Obsidian 同步

生成的报告会自动保存到 Obsidian 仓库：
- **保存路径**：`/root/clawd/obsidian-vault/reports/moltbook/YYYY-MM-DD.md`
- **文件名格式**：`YYYY-MM-DD.md`
- **同步方式**：通过 GitHub 实现与 Obsidian 仓库的双向同步

## 执行流程

当触发此技能时，代理必须执行以下步骤：

1. **获取热门帖子**：
   ```bash
   cd /root/clawd/skills/moltbook-fanboy && python3 scripts/fetch_top_posts.py
   ```

2. **生成每日报告**（包括互动内容的生成和保存到 Obsidian）：
   ```bash
   cd /root/clawd/skills/moltbook-fanboy && python3 scripts/generate_daily_report.py
   ```

3. **读取并发送**：脚本将报告内容输出后，直接发送到 Telegram。