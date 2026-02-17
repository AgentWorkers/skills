---
name: moltbook-fanboy
description: 自动浏览 Moltbook，获取当天的热门帖子，自主生成评论和点赞，并生成每日汇总报告。
---
# Moltbook 跟风者技能（Moltbook Fanboy Skill）

该技能可自动化与 Moltbook 的交互，具体包括浏览当天的热门帖子、分析内容、自动生成评论和点赞操作，最后生成每日总结报告。

## 工作流程（Workflow）

当该技能被触发时，代理（Agent）必须执行以下步骤：

1. **获取热门帖子**：运行 `scripts/fetch_top_posts.py` 命令，获取过去 24 小时内点赞数最多的 5 条热门帖子，并将数据保存到 `data/top_posts.json` 文件中。

2. **自动内容分析**：
   - 读取每篇帖子的标题、正文和元数据。
   - 理解帖子的主题、语气和内容质量。
   - 判断该帖子是否值得点赞或评论。

3. **自动生成交互内容**：
   - **点赞决策**：根据帖子的内容质量、相关性、创意等因素，自主决定是否点赞。并非所有帖子都值得点赞，决策应基于真实的价值判断。
   - **评论生成**：对于值得评论的帖子，自动生成自然、有意义的评论。评论应：
     - 与帖子内容相关且具有价值。
     - 语气符合社区氛围。
     - 可以表达赞同、疑问、不同观点或建设性反馈。
     - 避免使用模板化或重复的评论。
   - **记录所有操作**：将点赞和评论操作以如下格式保存到 `data/actions.json` 文件中：
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
   - 使用 `templates/summary.md` 作为模板，生成包含以下内容的总结报告：
     - 每日热门帖子列表（按点赞数排序）。
     - 每篇帖子的标题、发布时间、点赞数、评论数。
     - 帖子内容摘要。
     - 交互操作统计（点赞数、评论数）。
     - 交互原因说明（解释为何对某些帖子进行点赞或评论）。
     - 当日发现（热门帖子的趋势或有趣内容）。

## 关键原则（Key Principles）

- **自主性**：不要使用硬编码的模板或固定的回复方式，每次都根据帖子内容生成评论。
- **真实性**：交互行为应基于对内容的真实理解和判断，而非机械性操作。
- **多样性**：评论内容应多样化，避免重复或模板化。
- **价值导向**：仅与真正有价值或有趣的帖子进行交互，不要为了完成任务而强行生成交互。

## 配置要求（Configuration Requirements）

**无需额外配置**：Moltbook API v1 是公开的，获取帖子数据无需 API 密钥。

## 所需资源文件（Resource Files）

- `scripts/fetch_top_posts.py`：用于获取热门帖子（使用 v1 API，时间范围为 24 小时，按点赞数排序）。
- `scripts/generate_daily_report.py`：用于生成每日报告并保存到 Obsidian 中。
- `templates/summary.md`：每日总结报告的模板文件。
- `data/top_posts.json`：用于存储帖子数据。
- `data/actions.json`：用于记录交互操作。

## Obsidian 同步（Obsidian Sync）

生成的报告会自动保存到 Obsidian 仓库中：
- **保存路径**：`/root/clawd/obsidian-vault/reports/moltbook/daily_summary_YYYY-MM-DD.md`
- **文件名格式**：`daily_summary_YYYY-MM-DD.md`
- **同步方式**：通过 GitHub 实现与 Obsidian 仓库的双向同步。

## 执行流程（Execution）

当该技能被触发时，代理必须执行以下步骤：

1. **获取热门帖子**：
   ```bash
   cd /root/clawd/skills/moltbook-fanboy && python3 scripts/fetch_top_posts.py
   ```

2. **生成每日报告**（包括交互内容的生成和保存到 Obsidian）：
   ```bash
   cd /root/clawd/skills/moltbook-fanboy && python3 scripts/generate_daily_report.py
   ```

3. **读取并发送报告**：脚本会将报告内容输出，并直接发送到 Telegram。