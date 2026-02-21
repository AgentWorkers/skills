---
name: solo-community-outreach
description: 查找相关的 Reddit、HN 和 ProductHunt 论文，并根据发布检查表起草以用户价值为导向的社区回复。当用户请求“查找社区”、“起草推广内容”、“在 Reddit 上进行宣传”或“开展 ProductHunt 活动”时，请使用此流程。请勿将此内容用于社交媒体帖子（请使用 /content-gen）或视频脚本（请使用 /video-promo）。
license: MIT
metadata:
  author: fortunto2
  version: "1.1.0"
  openclaw:
    emoji: "💬"
allowed-tools: Read, Grep, Glob, Write, WebSearch, WebFetch, AskUserQuestion, mcp__solograph__web_search, mcp__solograph__kb_search, mcp__solograph__project_info
argument-hint: "<project-name or idea>"
---
# /社区拓展（Community Outreach）

在 Reddit、Hacker News 和 ProductHunt 等社区中寻找相关的讨论帖，然后撰写有针对性且以用户价值为核心的回复。切勿发送垃圾信息，而是要提供真正有帮助的答案，并自然地提及所涉及的产品。

## MCP 工具（如可用，请使用）

- `web_search(query, engines, include_raw_content)` — 在 Reddit（PullPush）、Hacker News 和其他网站上进行搜索
- `kb_search(query)` — 查找相关的方法论或信息
- `project_info(name)` — 获取项目详情

如果 MCP 工具不可用，请使用 Claude WebSearch 或 WebFetch 作为替代方案。

## SearXNG 引擎的使用说明

- `engines: "reddit"` — 使用 PullPush API 进行搜索，返回帖子的正文内容
- `site:news.ycombinator.com` — 通过 Google 搜索 Hacker News 的内容（原生引擎可能无法正常使用）
- `site:producthunt.com` — 在 ProductHunt 上进行搜索
- `site:indiehackers.com` — 在 Indie Hackers 社区中查找相关讨论

## 操作步骤

1. **解析项目信息**：从 `$ARGUMENTS` 中获取项目相关数据。
   - 阅读产品的需求文档（PRD）和用户手册（README），了解产品解决的问题、提供的解决方案以及核心功能。
   - 如果这些信息缺失，可以通过 `AskUserQuestion` 功能向用户询问。

2. **提取搜索关键词**：
   - 问题相关的关键词（用户抱怨的内容）
   - 解决方案相关的关键词（用户搜索的内容）
   - 产品所属的类别关键词
   - 竞争产品的名称（用于对比或分析）

3. **在相关社区中进行搜索**（并行执行搜索操作）：

   ### 3a. Reddit
   对于每一组关键词，使用 MCP 的 `web_search(query, engines="reddit")` 或 Claude WebSearch 进行搜索：
   - `"{问题} reddit"` — 搜索与问题相关的帖子
   - `"{解决方案类别} recommendations reddit"` — 搜索相关的产品推荐帖子
   - `"{竞争对手} alternative reddit"` — 搜索关于竞争对手的讨论帖子
   - `"{竞争对手} vs reddit"` — 搜索关于竞争对手与 Reddit 的对比帖子

   从搜索结果中提取以下信息：子版块名称（subreddit）、帖子标题、链接（URL）、发布日期和评论数量。筛选条件：帖子发布时间在 6 个月内且评论数量超过 5 条。

   ### 3b. Hacker News
   使用 `site:news.ycombinator.com` 进行搜索：
   - `"Show HN: {类似产品类别}"` — 查找类似产品的发布信息
   - `"Ask HN: {问题领域}"` — 查找与该问题相关的问题
   - `"{竞争对手 name} site:news.ycombinator.com"` — 查找关于竞争对手的讨论帖子

   从搜索结果中提取帖子标题、链接、点赞数和评论数量。

   ### 3c. ProductHunt
   使用 `site:producthunt.com` 进行搜索：
   - `"{产品类别} site:producthunt.com"` — 查找类似产品的发布信息
   - `"{竞争对手} site:producthunt.com"` — 查找竞争对手的产品页面

   从搜索结果中提取产品名称、发布日期和点赞数。

   ### 3d. 其他社区（可选）
   - `site:indiehackers.com "{问题}"` — 在 Indie Hackers 社区中查找相关讨论
   - `site:dev.to "{解决方案类别}"` — 在 Dev.to 社区中查找技术类产品的讨论

4. **制定拓展策略**：
   在撰写回复之前，先确定以下内容：
   - 最值得参与的 5 个帖子（相关性最高且活跃度最高的）
   - 不同社区的交流风格：Reddit（轻松、自我调侃），Hacker News（技术性较强、数据驱动），ProductHunt（热情洋溢、注重产品展示）
   **以用户价值为核心**：在提及产品之前，首先明确我们能提供哪些实际帮助
   **重要原则**：禁止虚假宣传或使用虚假账号，必须明确说明自己是产品的开发者

5. **为前 5 个帖子撰写回复**：

   对于每个帖子，使用以下格式编写回复内容：
   ```markdown
   ### Thread: {title}
   **URL:** {url}
   **Subreddit/Community:** {community}
   **Why relevant:** {1 sentence}

   **Draft response:**
   {2-4 paragraph response that:
   - Directly addresses the question/problem
   - Provides genuine value (tips, experience, data)
   - Mentions the product naturally (last paragraph)
   - Includes "disclaimer: I'm the developer" for transparency
   }
   ```

6. **生成 ProductHunt 的产品发布相关 checklist**：
   ```markdown
   ## ProductHunt Launch Checklist

   ### Pre-Launch (1 week before)
   - [ ] Hunter identified (or self-hunting)
   - [ ] Tagline ready (< 60 chars): "{tagline}"
   - [ ] Description ready (< 260 chars)
   - [ ] 5+ screenshots/GIF prepared
   - [ ] Maker comment drafted (story + problem + solution)
   - [ ] Launch day scheduled (Tuesday-Thursday, 00:01 PST)

   ### Launch Day
   - [ ] Post live and verified
   - [ ] Maker comment posted immediately
   - [ ] Share in relevant communities (not vote-begging)
   - [ ] Respond to all comments within 1 hour
   - [ ] Share progress on Twitter/LinkedIn

   ### Post-Launch
   - [ ] Thank supporters
   - [ ] Collect feedback from comments
   - [ ] Update product based on feedback
   ```

7. **将拓展计划写入 `docs/outreach-plan.md` 文件中**：
   ```markdown
   # Community Outreach Plan: {Project Name}

   **Generated:** {YYYY-MM-DD}
   **Product:** {one-line description}
   **ICP:** {target persona}

   ## Target Communities

   | Community | Relevant Threads Found | Priority |
   |-----------|----------------------|----------|
   | r/{subreddit} | N | high/medium/low |
   | Hacker News | N | high/medium/low |
   | ProductHunt | N | high/medium/low |

   ## Top Threads to Engage

   {5 thread drafts from step 5}

   ## ProductHunt Launch Checklist

   {checklist from step 6}

   ## Search Keywords Used
   - {keyword1}: N results
   - {keyword2}: N results

   ---
   *Generated by /community-outreach. Review all drafts before posting.*
   ```

8. **输出总结**：记录找到的社区、值得参与的帖子以及 ProductHunt 的准备情况。

## 重要规则

1. **以用户价值为核心，产品信息为辅助**：所有回复都必须真正帮助到用户
2. **务必说明身份**：必须明确表示“我是该产品的开发者”
3. **禁止操纵投票**：切勿请求用户点赞
4. **禁止虚假行为**：严禁伪装成用户参与讨论
5. **遵守社区规则**：在发布内容前请先查看相关社区的规则
6. **质量优先**：5 条高质量回复比 50 条泛泛而空的回复更有价值

## 常见问题及解决方法

### SearXNG 无法使用
**原因**：SSH 隧道未启用或服务器故障。
**解决方法**：在 solopreneur 脚本中运行 `make search-tunnel` 命令。如果问题仍然存在，可以切换到 Claude WebSearch。

### 未找到相关帖子
**原因**：产品所属的市场领域过于细分或关键词使用不当。
**解决方法**：扩大搜索范围，尝试使用竞争对手的名称、问题描述或相关类别的关键词。

### 回复内容过于宣传化
**原因**：产品提及过于突出或缺乏实质性的帮助内容。
**解决方法**：重新撰写回复，确保 80% 的内容是帮助用户的实际建议，只有 20% 是关于产品的信息。同时务必明确说明自己是产品的开发者。