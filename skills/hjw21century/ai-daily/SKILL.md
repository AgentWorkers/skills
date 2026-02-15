---
name: ai-daily
description: 从 smol.ai 的 RSS 源中获取 AI 相关的新闻。当用户询问 AI 新闻或每日科技动态时可以使用该功能。
---

# AI每日新闻

从smol.ai的RSS源获取AI行业新闻。

## 快速入门

```
# Basic queries
昨天AI资讯
今天的AI新闻
2026-01-13的资讯
```

## 查询类型

| 类型 | 示例 | 描述 |
|------|----------|-------------|
| 相对日期 | `昨天AI资讯` `今天的新闻` `前天` | 昨天、今天、前天 |
| 绝对日期 | `2026-01-13的新闻` | 使用YYYY-MM-DD格式 |
| 日期范围 | `有哪些日期的新闻` | 显示可用的日期 |

## 工作流程

```
- [ ] Step 1: Parse date from user request
- [ ] Step 2: Fetch RSS data
- [ ] Step 3: Check content availability
- [ ] Step 4: Format and display results
```

---

## 第一步：解析日期

| 用户输入 | 目标日期 | 计算方式 |
|------------|-------------|-------------|
| `昨天` | 昨天 | 当前日期 - 1天 |
| `前天` | 前天 | 当前日期 - 2天 |
| `今天` | 今天 | 当前日期 |
| `2026-01-13` | 2026-01-13 | 直接解析 |

**格式要求**：始终使用`YYYY-MM-DD`格式。

---

## 第二步：获取RSS数据

```bash
python skills/ai-daily/scripts/fetch_news.py --date YYYY-MM-DD
```

**可用命令**：

```bash
# Get specific date
python skills/ai-daily/scripts/fetch_news.py --date 2026-01-13

# Get date range
python skills/ai-daily/scripts/fetch_news.py --date-range

# Relative dates
python skills/ai-daily/scripts/fetch_news.py --relative yesterday
```

**安装依赖**：`pip install feedparser requests`

---

## 第三步：检查内容

### 如果未找到数据

```markdown
Sorry, no news available for 2026-01-14

Available date range: 2026-01-10 ~ 2026-01-13

Suggestions:
- View 2026-01-13 news
- View 2026-01-12 news
```

---

## 第四步：格式化结果

**示例输出**：

```markdown
# AI Daily · 2026年1月13日

> not much happened today

## Content

[News content from smol.ai RSS...]

---
Source: smol.ai
```

---

## 配置参数

| 参数 | 描述 | 默认值 |
|---------|-------------|---------|
| RSS_URL | RSS源URL | `https://news.smol.ai/rss.xml` |

无需使用API密钥。

---

## 故障排除

| 问题 | 解决方案 |
|-------|----------|
| RSS数据获取失败 | 检查网络连接 |
| 日期格式错误 | 使用YYYY-MM-DD格式 |
| 未找到内容 | 检查指定的日期范围是否有效 |

---

## 参考资料

- [输出格式](references/output-format.md) - Markdown输出格式模板
- [HTML主题](references/html-themes.md) - 网页主题规范