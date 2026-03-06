---
name: google-search-serper
description: 由 Serper.dev API 支持的 Google 搜索功能——提供 9 种搜索类型：网页、新闻、图片、视频、地点、购物、学术文献、专利以及自动完成搜索。搜索结果会包含知识图谱（Knowledge Graph）、答案框（Answer Box）、用户常见问题（People Also Ask）和相关搜索建议（Related Searches）。当用户需要使用 Google 进行搜索时，无论是查找当前信息、浏览网页、搜索新闻、查看图片、研究学术论文、查找本地地点，还是当 Brave Search 的搜索结果不够全面时，都可以使用该功能；当然，如果用户明确希望获得 Google 的搜索结果，也可以使用此服务。
---
# Google搜索技能

该技能基于Serper.dev的API实现，可替代Brave Search，提供更丰富的搜索结果，包括知识图谱（Knowledge Graph）、答案框（Answer Box）、用户也问（People Also Ask）以及多种专门的搜索类型。

## 使用场景
适用于所有Google搜索请求。系统会自动识别用户的搜索意图：
- 默认 → `search`
- “关于X的新闻” / “最新的X” → `news`
- “X的图片” → `images`
- “X的视频” / “如何做X的视频” → `videos`
- “X附近的餐厅” / “我附近的X” → `places`
- “X的价格是多少” / “购买X” → `shopping`（⚠️ 需要2个信用点数）
- “关于X的论文” / “关于X的研究” → `scholar`
- “X的专利” → `patents`
- “关于X的建议” → `suggest`

## 使用方法

```bash
SCRIPT_DIR="~/.openclaw/workspace/skills/google-search/scripts"

# Web search (default)
npx tsx $SCRIPT_DIR/google-search.ts search "query" [--num 10] [--time day|week|month|year] [--country us] [--lang en]

# Specialized
npx tsx $SCRIPT_DIR/google-search.ts news "query" [--num 10]
npx tsx $SCRIPT_DIR/google-search.ts images "query"
npx tsx $SCRIPT_DIR/google-search.ts videos "query"
npx tsx $SCRIPT_DIR/google-search.ts places "query"
npx tsx $SCRIPT_DIR/google-search.ts shopping "query"
npx tsx $SCRIPT_DIR/google-search.ts scholar "query" [--year 2023]
npx tsx $SCRIPT_DIR/google-search.ts patents "query"
npx tsx $SCRIPT_DIR/google-search.ts suggest "query"
npx tsx $SCRIPT_DIR/google-search.ts credits
```

在命令前添加`--json`选项可获取原始的JSON格式输出。

## 设置要求
需要从Serper.dev获取免费的API密钥：
1. 访问https://serper.dev注册（包含2500次免费搜索次数）
2. 从控制面板复制您的API密钥
3. 将密钥添加到环境变量中：`export SERPER_API_KEY=your_key_here`

如果未设置API密钥，请提醒用户前往serper.dev注册——注册是免费的，只需30秒。

## 工作流程
1. 运行相应的搜索命令
2. 解析返回的格式化结果
3. 如需获取更详细的信息，可对符合条件的链接使用`web_fetch`函数
4. 每个响应中都会显示剩余的信用点数，请注意使用情况
5. 购物功能需要2个信用点数——仅当用户明确请求价格或购物信息时使用

## 时间筛选选项
`--time`支持以下时间单位：`hour`（小时）、`day`（天）、`week`（周）、`month`（月）、`year`（年），或简写形式`h`、`d`、`w`、`m`、`y`

## 注意事项
- 免费 tier 的请求速率限制为每秒5次
- 除购物功能外，所有搜索操作均消耗1个信用点数
- 搜索结果包含丰富的信息：知识图谱、答案框、用户也问以及相关搜索结果