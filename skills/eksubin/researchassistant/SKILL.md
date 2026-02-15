---
name: ResearchMonitor
description: 监控研究主题，以获取新的论文、会议和期刊信息。
---

# ResearchMonitor

此功能可帮助用户及时了解其所在研究领域的最新动态。

## 工作流程

1. **检查配置**：
   - 读取该目录下的 `research_config.json` 文件，以获取用户的研究主题和上次查看的日期。
   - 如果文件不存在或研究主题为空，请询问用户他们感兴趣的研究主题，并使用 `scripts/daily_briefing.py --add-topic "topic"` 命令将其保存下来。

2. **每日检查**：
   - 获取当前日期。
   - 与 `research_config.json` 文件中的 `last-checked` 日期进行比较。
   - 如果今天已经检查过相关内容，则除非用户另有要求，否则无需再次检查。

3. **执行搜索**：
   - 对于每个研究主题，使用 `search_web` 命令搜索以下信息：
     - “[主题] [当前月份/年份] 的新研究论文”
     - “[主题] [当前年份] 即将举行的会议”
     - “[主题] [当前月份/年份] 的新期刊文章”
     - 如有必要，还可以搜索 arXiv、IEEE Xplore、Google Scholar 或 X（Twitter）等专业平台。

4. **筛选与分析**：
   - 对于每个搜索到的结果，使用 `scripts/daily_briefing.py --check-seen "URL 或唯一标题"` 命令进行验证。
   - 如果返回 “true”，则表示该内容已被用户查看过，可以直接跳过。
   - 将搜索结果与昨天查看的内容进行比较（可以通过检查发布日期是否在最近 24-48 小时内来判断）。
   - **重要提示**：如果没有任何新的重要信息（没有新的研究论文或会议公告），则无需通知用户。

5. **生成报告**：
   - 如果发现新的内容，生成一份简短的 Markdown 报告，内容包括：
     - **标题**：新闻/论文的标题
     - **来源**：URL 或期刊名称
     **摘要**：简要说明该内容为何重要。
   - 将报告呈现给用户。
   - 使用 `scripts/daily_briefing.py --mark-seen "URL 或唯一标题"` 命令将相关内容标记为已查看。
   - 使用 `scripts/daily_briefing.py --update-date` 命令更新 `last-checked` 日期。

## 脚本

- `python scripts/daily_briefing.py --add-topic "主题"`：添加一个新的研究主题。
- `python scripts/daily_briefing.py --list-topics`：列出当前的所有研究主题。
- `python scripts/daily_briefing.py --update-date`：将上次查看的日期更新为当前时间。
- `python scripts/daily_briefing.py --check-seen "ID"`：检查某个内容 ID（URL 或标题）是否已被记录在系统中。
- `python scripts/daily_briefing.py --mark-seen "ID"`：将某个内容 ID 标记为已查看。