---
name: fs-street
description: 从 Farnam Street 的 RSS 源中获取文章。当您想了解 Farnam Street 博客中关于决策、思维模型、学习或智慧方面的内容时，可以使用此功能。
---

# Farnam Street

该工具用于从 Farnam Street 博客中获取文章，内容涵盖思维模型、决策制定、领导力和学习等相关主题。

## 快速入门

```
# Basic queries
昨天的文章
今天的FS文章
2024-06-13的文章

# Search
有哪些可用的日期
```

## 查询类型

| 类型 | 示例 | 描述 |
|------|----------|-------------|
| 相对日期 | `昨天的文章` `今天的文章` `前天` | 昨天、今天、前天 |
| 绝对日期 | `2024-06-13 的文章` | 使用 YYYY-MM-DD 格式 |
| 日期范围 | `有哪些日期` `可用的日期` | 显示可用的日期范围 |
| 主题搜索 | `关于决策的文章` `思维模型` | 按关键词搜索 |

## 工作流程

```
- [ ] Step 1: Parse date from user request
- [ ] Step 2: Fetch RSS data
- [ ] Check content availability
- [ ] Format and display results
```

---

## 第一步：解析日期

| 用户输入 | 目标日期 | 计算方式 |
|------------|-------------|-------------|
| `昨天` | 昨天 | 当前日期 - 1 天 |
| `前天` | 前天 | 当前日期 - 2 天 |
| `今天` | 今天 | 当前日期 |
| `2024-06-13` | 2024-06-13 | 直接解析 |

**格式要求**：必须使用 `YYYY-MM-DD` 格式。

---

## 第二步：获取 RSS 数据

```bash
python skills/fs-street/scripts/fetch_blog.py --date YYYY-MM-DD
```

**可用命令**：

```bash
# Get specific date
python skills/fs-street/scripts/fetch_blog.py --date 2024-06-13

# Get date range
python skills/fs-street/scripts/fetch_blog.py --date-range

# Relative dates
python skills/fs-street/scripts/fetch_blog.py --relative yesterday
```

**安装要求**：`pip install feedparser requests`

---

## 第三步：检查内容

### 如果未找到内容

```markdown
Sorry, no article available for 2024-06-14

Available date range: 2023-04-19 ~ 2024-06-13

Suggestions:
- View 2024-06-13 article
- View 2024-06-12 article
```

### 仅限会员内容

部分文章会被标记为 `[FS Members]`——这些是付费内容，可能仅显示预览内容。

---

## 第四步：格式化结果

**示例输出**：

```markdown
# Farnam Street · 2024年6月13日

> Experts vs. Imitators: How to tell the difference between real expertise and imitation

## Content

If you want the highest quality information, you have to speak to the best people. The problem is many people claim to be experts, who really aren't.

**Key Insights**:
- Imitators can't answer questions at a deeper level
- Experts can tell you all the ways they've failed
- Imitators don't know the limits of their expertise

---
Source: Farnam Street
URL: https://fs.blog/experts-vs-imitators/
```

---

## 配置参数

| 参数 | 描述 | 默认值 |
|--------|-------------|---------|
| RSS_URL | RSS 数据源 URL | `https://fs.blog/feed/` |

无需使用 API 密钥。

---

## 故障排除

| 问题 | 解决方案 |
|------|---------|
| RSS 数据获取失败 | 检查网络连接 |
| 日期格式不正确 | 确保使用正确的 YYYY-MM-DD 格式 |
| 未找到内容 | 检查可用的日期范围 |
| 仅限会员内容 | 部分文章为付费内容 |

---

## 命令行接口参考

```bash
# Get specific date
python skills/fs-street/scripts/fetch_blog.py --date 2024-06-13

# Get date range
python skills/fs-street/scripts/fetch_blog.py --date-range

# Relative dates
python skills/fs-street/scripts/fetch_blog.py --relative yesterday
```