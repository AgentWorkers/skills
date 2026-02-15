# 代理新闻监控器（Agent News Monitor）

该工具会监控 Hacker News、Reddit 和 arXiv 上与 AI 代理相关的开发动态，并每日生成新闻摘要及热门话题警报。

## 功能简介

及时了解 AI 代理的最新进展非常重要，但这一过程往往耗时较多。本工具能够自动化地收集相关的新闻、论文和讨论内容。

## 命令选项

### 每日摘要（Daily Digest）
```bash
./monitor.sh digest
```
生成过去 24 小时的新闻摘要（以 Markdown 格式输出）。

### 当前热门话题（Trending Now）
```bash
./monitor.sh trending
```
显示所有来源中当前最热门的话题。

### 搜索（Search）
```bash
./monitor.sh search "memory systems"
```
根据指定主题搜索最近发布的文章。

### 关注主题（Watch Topics）
```bash
./monitor.sh watch "autonomous agents,tool use,memory"
```
设置需要在未来摘要中重点展示的主题。

## 数据来源

- **Hacker News**：匹配 AI 代理关键词的热门/新文章
- **Reddit**：r/LocalLLaMA、r/MachineLearning、r/artificial 等板块
- **arXiv**：cs.AI、cs.CL、cs.LG 等分类下的论文

## 集成到 HEARTBEAT.md 中

可将本工具的功能集成到 HEARTBEAT.md 文件中：
```markdown
## Morning News Check
- Run: ./skills/agent-news/monitor.sh digest --quiet
- If interesting items: Send summary to Serene
- Log: Update memory/news-state.json
```

## 输出格式

支持 Markdown（默认格式）和 JSON（`--json` 参数）格式的输出。