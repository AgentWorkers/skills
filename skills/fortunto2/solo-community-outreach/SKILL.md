---
name: solo-community-outreach
description: 查找相关的 Reddit、HN（Hacker News）和 ProductHunt 论文，并根据发布检查清单（launch checklist）起草以用户价值为中心的社区回复。适用于用户提出“寻找社区资源”、“起草宣传材料”、“在 Reddit 上进行推广”或“开展 ProductHunt 活动”等需求时。请勿将这些内容用于社交媒体帖子（请使用 /content-gen），也不得用于视频脚本（请使用 /video-promo）。
license: MIT
metadata:
  author: fortunto2
  version: "1.1.1"
  openclaw:
    emoji: "💬"
allowed-tools: Read, Grep, Glob, Write, WebSearch, WebFetch, AskUserQuestion, mcp__solograph__web_search, mcp__solograph__kb_search, mcp__solograph__project_info
argument-hint: "<project-name or idea>"
---
# /community-outreach

在 Reddit、Hacker News 和 ProductHunt 等社区中寻找相关的讨论帖，并起草有针对性、以用户需求为导向的回复。请注意，不要发送垃圾信息，而是提供真正有帮助的答案，并自然地提及产品。

## MCP 工具（如可用，请使用）

- `web_search(query, engines, include_raw_content)` — 在 Reddit、Hacker News 和其他网站上进行搜索
- `kb_search(query)` — 查找相关的方法或技巧
- `project_info(name)` — 获取项目详情

如果 MCP 工具不可用，请使用 WebSearch 或 WebFetch 作为替代方案。

## 步骤

1. **从 `$ARGUMENTS` 中解析项目信息**：
   - 阅读产品的需求文档（PRD/README）以了解问题、解决方案、关键特性等信息。
   - 如果这些信息缺失，可以通过 AskUserQuestion 功能进行询问。

2. **提取搜索关键词**：
   - 问题相关的关键词（用户抱怨的内容）
   - 解决方案相关的关键词（用户搜索的内容）
   - 产品所属的类别关键词
   - 竞争产品的名称（用于对比或讨论相关话题）

3. **在各个社区中进行搜索**（同时运行多个搜索任务）：

   ### 3a. Reddit
   对于每一组关键词，使用 MCP 的 `web_search(query)` 或 WebSearch 进行搜索：
   - `"{问题} reddit"` — 关于该问题的讨论帖
   - `"{解决方案类别} recommendations reddit"` — 关于该解决方案的推荐请求
   - `"{竞争产品} alternative reddit"` — 关于该竞争产品的讨论帖
   - `"{竞争产品} vs reddit"` — 关于该竞争产品的对比帖

   从搜索结果中提取：子版块名称（subreddit）、帖子标题、URL、发布日期和评论数量。
   筛选条件：帖子创建时间在 6 个月内且评论数量超过 5 条（表示帖子仍然活跃）。

   ### 3b. Hacker News
   在 `site:news.ycombinator.com` 上进行搜索：
   - `"Show HN: {类似产品类别}"` — 查找类似产品的发布信息
   - `"Ask HN: {问题领域}"` — 查找与该问题相关的问题
   - `"{竞争产品名称} site:news.ycombinator.com"` — 查找关于该竞争产品的讨论

   从搜索结果中提取：帖子标题、URL、获得的点赞数和评论数量。

   ### 3c. ProductHunt
   在 `site:producthunt.com` 上进行搜索：
   - `"{产品类别} site:producthunt.com"` — 查找类似产品的发布信息
   - `"{竞争产品} site:producthunt.com"` — 查找关于该竞争产品的信息

   从搜索结果中提取：产品名称、发布日期和点赞数。

   ### 3d. 其他社区（可选）
   - `site:indiehackers.com "{问题}"` — Indie Hackers 社区
   - `site:dev.to "{解决方案类别}"` — Dev.to 社区（如果产品具有技术特性）

4. **制定外展策略**：
   在起草回复之前，先确定以下内容：
   - **最值得参与的 5 个帖子**（相关性最高且活跃度最高的帖子）
   - **针对不同社区的沟通方式**：Reddit（轻松、自嘲的风格），Hacker News（技术性强的风格），ProductHunt（热情洋溢的风格）
   **以用户需求为导向的回复内容**：在提及产品之前，先提供真正有帮助的信息
   **重要原则**：禁止虚假宣传，禁止使用虚假账号，必须明确说明自己是产品的开发者

5. **为前 5 个帖子起草回复内容**：

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

6. **生成 ProductHunt 的产品发布信息列表**：

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

7. **将外展计划编写到 `docs/outreach-plan.md` 文件中**：

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

8. **输出总结**：找到的社区、最值得参与的 3 个帖子以及 ProductHunt 的准备情况。

## 重要规则

1. **以用户需求为导向，产品信息为辅助** — 每条回复都必须真正帮助到用户
2. **必须明确说明**： “我是该产品的开发者” 或 “免责声明：这是我开发的”
3. **禁止操纵投票** — 绝不要请求点赞
4. **禁止虚假宣传** — 绝不要伪装成用户
5. **遵守社区规则** — 发帖前请查看相关子版块的规则
6. **质量优先，数量其次** — 5 条高质量回复比 50 条泛泛而空的回复更有价值

## 常见问题

### MCP 的 web_search 工具无法使用
**原因**：MCP 的 web_search 工具未配置或无法使用。
**解决方法**：将 WebSearch 或 WebFetch 作为主要搜索工具。为了获得更好的搜索效果（尤其是针对 Reddit 和 Hacker News），可以安装并配置 [SearXNG](https://github.com/fortunto2/searxng-docker-tavily-adapter)（私有、自托管、免费工具），并配置 solograph MCP。

### 未找到相关帖子
**原因**：产品所属的细分市场太小或使用的关键词不准确。
**解决方法**：扩大搜索范围，尝试使用竞争产品的名称、问题描述或相关类别的关键词。

### 回复内容过于宣传化
**原因**：产品信息在回复中过于突出或缺乏实质性的帮助内容。
**解决方法**：重新撰写回复，确保 80% 的内容是帮助用户的实际建议，只有 20% 是关于产品的信息。同时，必须明确说明自己是产品的开发者。