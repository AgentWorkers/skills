---
name: solo-research
description: >
  **深度市场研究**：包括竞争对手分析、用户痛点识别、SEO/ASO关键词的筛选、域名可用性检查，以及市场规模的估算（TAM/SAM/SOM）。  
  适用场景：当用户提出“研究这个想法”、“寻找竞争对手”、“分析市场情况”、“检查域名是否可用”、“评估市场规模”或“分析市场机会”等需求时。  
  **注意**：此功能不适用于对创意进行评分（请使用 `/validate` 功能），也不适用于对现有网页进行SEO审计（请使用 `/seo-audit` 功能）。
license: MIT
metadata:
  author: fortunto2
  version: "1.7.1"
  openclaw:
    emoji: "🔍"
allowed-tools: Read, Grep, Bash, Glob, Write, Edit, WebSearch, WebFetch, AskUserQuestion, mcp__solograph__kb_search, mcp__solograph__web_search, mcp__solograph__session_search, mcp__solograph__project_info, mcp__solograph__codegraph_query, mcp__solograph__codegraph_explain, mcp__solograph__project_code_search, mcp__playwright__browser_navigate, mcp__playwright__browser_snapshot, mcp__playwright__browser_close
argument-hint: "[idea name or description]"
---
# /research

在生成产品需求文档（PRD）之前，需要进行深入的研究。研究结果将以结构化的`research.md`文件形式呈现，其中包含竞争分析、用户痛点、SEO/ASO关键词、域名选择建议以及市场规模等信息。

## MCP工具（如果可用）

如果MCP工具可用，建议优先使用它们，而非命令行界面（CLI）：
- `kb_search(query, n_results)` — 在知识库中搜索相关文档
- `web_search(query, engines, include_raw_content)` — 使用指定搜索引擎进行网页搜索
- `session_search(query, project)` — 查找之前是否有过类似的研究
- `project_info(name)` — 查看项目详情和技术栈
- `codegraph_explain(project)` — 查看项目的架构概览（技术栈、使用模式、依赖库）
- `codegraph_query(query)` — 使用Cypher查询代码图谱（查找共享库和依赖关系）
- `project_code_search(query, project)` — 对项目源代码进行语义搜索

MCP的`web_search`支持自定义搜索引擎，例如：`engines="reddit"`、`engines="youtube"`等。

如果MCP工具不可用，应主要使用WebSearch/WebFetch。如果MCP的`web_search`工具可用，使用它可以获得更好的搜索结果。

### Reddit搜索的最佳实践

- Reddit搜索时最多使用3个关键词 — 关键词越多，搜索结果越少
- 例如：`"product hunt outreach launch"` 是合适的搜索词；`"product hunt scraper maker profiles linkedin outreach launch strategy"` 则不太合适
- `include_raw_content=true` 在Reddit上很少有效 — 请使用以下备用方法

### Reddit内容获取的备用方法

当搜索到相关的Reddit帖子时，需要使用以下方法来获取其完整内容：

**方法1：MCP Playwright**（推荐用于获取完整帖子内容）
- 使用 `browser_navigate("https://old.reddit.com/r/...")` — 这个链接可以绕过CAPTCHA
- `www.reddit.com` 会显示CAPTCHA（需要验证用户身份），请始终使用 `old.reddit.com`
- 该方法可以获取包含完整帖子和评论的结构化YAML数据
- 例如：`old.reddit.com/r/indiehackers/comments/abc123/post_title/`

**方法2：PullPush API**（用于搜索和发现）
- 端点：`https://api.pullpush.io/reddit/submission/search`
- 参数：`q`、`subreddit`、`author`、`score`（例如：`>10,<100`）、`since`/`until`（时间戳）、`size`（最大100条结果）
- 请求限制：每分钟15次（软限制），每分钟30次（硬限制），每小时1000次。请求之间需间隔4秒。
- 返回包含完整帖子内容（`selftext`）、作者信息、评分和创建时间的JSON数据
- 评论搜索：`/reddit/comment/search`（参数相同）

**方法3：Reddit的.json端点**（经常被屏蔽）
- 在任何Reddit链接后添加`.json`后缀：`reddit.com/r/sub/comments/id.json`
- 该方法返回包含完整帖子和评论的原始JSON数据
- 但由于经常被屏蔽（403/429错误），请仅作为备用方法使用

**方法4：PRAW**（Reddit官方API，用于实时搜索和用户信息）
- [praw-dev/praw](https://github.com/praw-dev/praw) — Python Reddit API封装库
- 支持OAuth2认证和速率限制，支持同步和异步操作
- 适用于：实时搜索子版块内容、用户信息、评论获取等
- 使用方法：`pip install praw` 或 `uv add praw`

## 搜索策略：混合使用MCP和WebSearch

建议结合使用多种搜索工具。每种工具都有其优势：

| 步骤 | 最适合的工具 | 原因 |
|------|-------------|-----|
| **竞争对手信息** | WebSearch + `site:producthunt.com` + `site:g2.com` | 广泛的搜索范围 + Product Hunt平台上的信息 + B2B评论 |
| **Reddit上的用户痛点** | MCP的`web_search`（使用`engines: reddit`） + MCP Playwright（用于获取完整帖子内容） | 使用PullPush API获取帖子内容 |
| **YouTube评论** | MCP的`web_search`（使用`engines: youtube`） | 视频评论（观看量可反映需求） |
| **市场规模** | WebSearch | 从多个来源汇总数据 |
| **SEO/ASO分析** | WebSearch | 更广泛的覆盖范围和趋势数据 |
| **页面内容抓取** | WebFetch或MCP的`web_search`（使用`include_raw_content`） | 可抓取最多5000个字符的页面内容 |
| **Hacker News** | WebSearch `site:news.ycombinator.com` | 获取Hacker News上的讨论和观点 |
| **融资/公司信息** | WebSearch `site:crunchbase.com` | 获取公司的融资信息和团队规模 |
| **收入验证** | WebFetch `trustmrr.com/startup/<slug>` | 通过Stripe验证的收入数据、增长百分比、技术栈和流量 |

## 搜索流程

1. **从 `$ARGUMENTS` 中解析研究主题**。如果参数为空，询问用户具体想研究什么。
2. **判断产品类型** — 根据描述判断：
   - 如“app”、“mobile”、“iPhone”、“Android”等关键词 → 移动应用
   - 如“website”、“SaaS”、“dashboard”、“web app”等关键词 → Web应用
   - 如“CLI”、“terminal”、“command line”等关键词 → 命令行工具
   - 如“API”、“backend”、“service”等关键词 → 后端服务
   - 如“extension”、“plugin”、“browser”等关键词 → 插件或浏览器扩展
   - 如果不明确，默认为Web应用
   - 只有在确实难以判断时才通过`AskUserQuestion`询问用户（例如，“构建一个待办事项应用”可能是Web应用或移动应用）
   - 根据产品类型确定需要进行的分析内容（如移动应用的ASO分析、Web应用的SEO分析等）
3. **搜索知识库和之前的研究成果**：
   - 如果MCP的`kb_search`可用：`kb_search(query="<idea keywords>", n_results=5)`
   - 如果MCP的`session_search`可用：`session_search(query="<idea keywords:")` — 查看之前是否有过相关研究
   - 如果没有，就在`.md`文件中搜索相关关键词
   - 检查是否存在`research.md`或`prd.md`文件
4. **查看现有的项目组合**（如果MCP的codegraph工具可用）：
   - `codegraph_explain(project="<similar project:")` — 查看项目组合中相关项目的架构
   - `project_code_search(query="<relevant pattern>", project="<sibling:")` — 查找可重用的代码、模式和技术栈
   - `codegraph_query("MATCH (p:Project)-[:DEPENDS_ON]->(pkg:Package) WHERE pkg.name CONTAINS '<relevant tech>' RETURN p.name, pkg.name)` — 查找使用类似技术的项目
   - 有助于评估项目的可行性、可重用的代码、技术栈选择和开发时间
   - 如果没有MCP工具，跳过此步骤
5. **竞争分析** — 主要使用WebSearch，必要时结合MCP的`web_search`：
   - `"<idea> competitors alternatives 2026"` — 广泛搜索竞争对手
   - `"<idea> app review pricing"` — 查找产品价格信息
   - 使用WebFetch或MCP的`include_raw_content`功能抓取竞争对手的详细价格信息
   - 使用MCP的`engines: reddit`或WebSearch：`"<idea> vs"` — 查看用户评价
   - `site:producthunt.com <idea>` 或 `site:g2.com <idea>` — 查看Product Hunt平台上的评价
   - `site:crunchbase.com <competitor>` — 查看公司的融资信息和团队规模
   - `site:trustmrr.com <idea>` 或使用WebFetch `trustmrr.com/startup/<slug>` — 查看Stripe验证的收入数据、增长百分比、技术栈和流量
   - 提取每个竞争对手的信息：名称、网址、价格、主要功能、弱点以及通过TrustMRR验证的收入数据
6. **用户痛点** — 使用MCP的`web_search`或WebSearch + YouTube：
   - 使用MCP的`engines: reddit`或WebSearch：`"<problem>"` — 在Reddit上搜索相关讨论（最多使用3个关键词）
   - 如果找到相关帖子但无法直接查看内容，使用MCP Playwright：`browser_navigate("https://old.reddit.com/r/...")` — 绕过CAPTCHA
   - 使用MCP的`engines: youtube`或WebSearch：`"<problem> review"` — 查看视频评论
   - `site:news.ycombinator.com <problem>` — 查看Hacker News上的观点
   - 使用WebSearch：`"<problem> frustrating OR annoying"` — 进行更广泛的搜索
   - 整理出前5个用户痛点，并附上引用来源
7. **SEO/ASO分析**（根据步骤2确定的 product 类型进行）：
   - **对于Web应用**：
     - `"<competitor> SEO keywords ranking"` — 竞争对手的关键词
     - `"<problem domain> search volume trends 2026"` — 查看需求趋势
   - 使用WebFetch或MCP的`include_raw_content`功能抓取竞争对手页面的元标签
   - 结果包括关键词、搜索意图和竞争情况
   - **对于移动应用**：
     - `"<category> App Store top apps keywords 2026"` — 查看应用商店的热门关键词
     - `site:reddit.com <competitor app> review` — 查看用户评价
   - 结果包括ASO关键词、竞争对手评分和常见用户反馈
8. **域名和公司注册**：
   - 生成7-10个候选域名（结合描述性和易于记忆的名称）
   - 使用三重验证方法（whois、dig、RDAP）检查域名是否可用
   - 检查域名是否与商标或公司名称冲突
   - 详细信息请参考`references/domain-check.md`文件

9. **市场规模**（TAM/SAM/SOM） — 主要使用WebSearch：
   - `WebSearch`：`"<market> market size 2025 2026 report"` — 汇总市场规模数据
   - `WebSearch`：`"<market> growth rate CAGR billion"` — 查看增长率预测
   - 根据这些数据推算TAM（总市场容量）、SAM（服务市场容量）和SOM（可服务市场容量）
10. **编写`research.md`文件** — 将结果写入当前项目目录下的`docs/research.md`文件。如果需要，先创建该目录。
11. **输出总结**：
    - 主要研究结果（3-5点）
    - 建议是否继续进行该项目，以及原因
    - 生成的研究文件的位置
    - 下一步建议：`/validate <idea>`

## `research.md`文件格式

详细格式请参考`references/research-template.md`文件。

## 注意事项

- 项目目录名请使用驼峰式命名法（kebab-case）
- 如果`research.md`文件已经存在，在覆盖之前请先询问用户是否需要重新生成
- 如果搜索任务可以并行执行，请同时进行

## 常见问题及解决方法

### MCP的`web_search`不可用
**原因**：MCP服务器未运行或配置错误。
**解决方法**：主要使用WebSearch/WebFetch。如果需要使用特定搜索引擎（如Reddit、GitHub、YouTube），请安装并配置[SearXNG](https://github.com/fortunto2/searxng-docker-tavily-adapter)（私有、自托管、免费）。

### 域名验证结果错误
**原因**：`.app`或`.dev`等扩展名可能导致显示未注册域名的创建日期。
**解决方法**：使用三重验证方法（whois、dig、RDAP）来获取准确的域名信息。

### `research.md`文件已存在
**原因**：之前已经针对该主题进行过研究。
**解决方法**：在覆盖文件之前先询问用户是否需要重新生成研究内容。

## 建议的搜索技巧

### 深入分析Reddit内容

- 使用MCP的`web_search`或WebSearch进行搜索（Reddit搜索时最多使用3个关键词），并获取帖子链接
- 使用MCP Playwright访问`old.reddit.com`以获取完整的帖子和评论内容（绕过CAPTCHA）
- 提取引用内容时，请注明来源（用户ID、子版块名称和日期）

### Product Hunt平台的搜索技巧

- 访问`producthunt.com/visit-streaks`查看排行榜数据
- 使用`producthunt.com/@username`查看作者的个人资料和社交链接
- 注意：PH API v2已于2023年2月停止使用，建议使用其他方法抓取数据

### TrustMRR的收入验证

- 使用`trustmrr.com/startup/<slug>`获取Stripe验证的收入数据
- 无需认证，返回包含结构化数据的JSON
- 数据字段包括：收入、累计收入、过去30天的数据、活跃订阅用户数、技术栈和流量
- 适用于验证竞争对手的收入信息、市场规模和技术栈

### GitHub上的资源搜索

- 使用MCP的`engines: github`时可能返回空结果，建议主要使用WebSearch
- 使用`github.com/topics/<keyword>`浏览相关主题页面

### 遇到内容被屏蔽时的备用方法

如果使用WebFetch时页面返回403错误或CAPTCHA：
- 对于Reddit，使用MCP Playwright访问`old.reddit.com`（始终有效且无CAPTCHA）
- 对于其他网站，使用PullPush API `api.pullpush.io`获取结构化JSON数据
- 对于Product Hunt等网站，使用MCP的`browser_navigate`功能（大多数网站无需CAPTCHA）

---

请注意，上述代码块中的````
1. MCP Playwright (old.reddit.com)     ← BEST: bypasses CAPTCHA, full post + comments
2. PullPush API (api.pullpush.io)      ← search by query/subreddit/author/score/date
3. MCP web_search include_raw_content   ← sometimes works, often truncated
4. WebFetch / WebSearch snippets        ← last resort, partial data only
````和````
MCP Playwright (best) → PullPush API (Reddit) → WebFetch → WebSearch snippets → MCP web_search include_raw_content
````是占位符，实际代码需要根据实际情况填写。