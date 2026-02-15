---
name: twitter-search
description: 高级Twitter搜索与社交媒体数据分析功能：通过Twitter API根据关键词获取推文，最多可处理1000条结果，并生成包含洞察和可操作建议的专业数据分析报告。适用于用户需要执行Twitter/X社交媒体搜索、社交媒体趋势分析、推文数据挖掘、社交媒体监听、影响者识别、推文情感分析，或任何涉及收集和分析Twitter数据以获取洞察的任务。
---

# Twitter搜索与分析

## 概述

使用高级搜索语法在Twitter上搜索关键词，获取最多1000条相关推文，并对这些数据进行分析，生成包含洞察、统计信息和可操作建议的专业报告。

## 先决条件

**需要API密钥**：用户必须从https://twitterapi.io配置他们的Twitter API密钥。

API密钥可以通过以下三种方式提供：
1. **环境变量**（推荐）：在`~/.bashrc`或`~/.zshrc`中设置`TWITTER_API_KEY`
   ```bash
   echo 'export TWITTER_API_KEY="your_key_here"' >> ~/.bashrc
   source ~/.bashrc
   ```

2. **作为参数**：在包装脚本中使用`--api-key YOUR_KEY`
3. **直接传递**：作为Python脚本的第一个参数

## 快速入门

### 使用包装脚本（推荐）

包装脚本会自动处理环境变量的加载和依赖检查：

```bash
# Basic search (uses TWITTER_API_KEY from shell config)
./scripts/run_search.sh "AI"

# With custom API key
./scripts/run_search.sh "AI" --api-key YOUR_KEY

# With options
./scripts/run_search.sh "\"Claude AI\"" --max-results 100 --format summary

# Advanced query
./scripts/run_search.sh "from:elonmusk since:2024-01-01" --query-type Latest
```

### 直接使用Python脚本

```bash
# Search for a keyword
scripts/twitter_search.py "$API_KEY" "AI"

# Search with multiple keywords
scripts/twitter_search.py "$API_KEY" "\"ChatGPT\" OR \"Claude AI\""

# Search from specific user
scripts/twitter_search.py "$API_KEY" "from:elonmusk"

# Search with date range
scripts/twitter_search.py "$API_KEY" "Bitcoin since:2024-01-01"
```

### 高级查询

```bash
# Complex query: AI tweets from verified users, English only
scripts/twitter_search.py "$API_KEY" "AI OR \"machine learning\" lang:en filter:verified"

# Recent crypto tweets with minimum engagement
scripts/twitter_search.py "$API_KEY" "Bitcoin min_retweets:10 lang:en"

# From specific influencers
scripts/twitter_search.py "$API_KEY" "from:elonmusk OR from:VitalikButerin since:2024-01-01"
```

### 输出格式

```bash
# Full JSON with all tweets
scripts/twitter_search.py "$API_KEY" "AI" --format json

# Summary with statistics (default)
scripts/twitter_search.py "$API_KEY" "AI" --format summary
```

### 选项

- `--max-results N`：获取的最大推文数量（默认：1000）
- `--query-type Latest|Top`：排序方式（默认：按相关性排序）
- `--format json|summary`：输出格式（默认：summary）

## 工作流程

### 1. 明确用户需求

确定分析目标：
- 要搜索的主题/关键词是什么？
- 日期范围有何偏好？
- 需要包含/排除的具体用户是谁？
- 语言偏好是什么？
- 需要哪种类型的洞察（趋势、情感分析、影响者分析）？

### 2. 构建搜索查询

使用[Twitter高级搜索](https://github.com/igorbrigadir/twitter-advanced-search)语法：

| 语法 | 示例 | 描述 |
|--------|---------|-------------|
| `keyword` | `AI` | 单个关键词 |
| `"phrase"` | `"machine learning"` | 精确短语 |
| `OR` | `AI OR ChatGPT` | 任意一个词 |
| `from:user` | `from:elonmusk` | 来自特定用户 |
| `to:user` | `to:elonmusk` | 回复给用户 |
| `since:DATE` | `since:2024-01-01` | 从指定日期之后 |
| `until:DATE` | `until:2024-12-31` | 从指定日期之前 |
| `lang:xx` | `lang:en` | 语言代码 |
| `#hashtag` | `#AI` | 标签 |
| `filter:links` | `filter:links` | 包含链接的推文 |
| `min_retweets:N` | `min_retweets:100` | 最少转发次数 |

### 3. 获取数据

执行搜索脚本：

```bash
scripts/twitter_search.py "$API_KEY" "YOUR_QUERY" --max-results 1000 --query-type Top
```

**注意**：默认最多获取1000条推文。脚本会自动：
- 分页显示所有可用结果
- 在获取1000条推文后停止（遵守API限制）
- 优雅地处理错误

### 4. 分析并生成报告

获取数据后，生成一份全面的专业报告，内容包括：

#### 报告结构

1. **执行摘要**（2-3句话）
   - 搜索的内容
   - 主要发现概述

2. **数据概览**
   - 分析的总推文数量
   - 数据的日期范围
   - 使用的查询参数

3. **关键指标**
   - 总参与度（点赞、转发、回复、引用、观看次数）
   - 每条推文的平均参与度
   - 语言分布
   - 回复与原始推文的比例

4. **热门内容分析**
   - 被转发最多的推文（附有原始推文的**URL链接**）
   - 被点赞最多的推文（附有原始推文的**URL链接**）
   - 使用频率最高的标签
   - 被提及最多的用户
   - 带有完整URL引用的精选推文示例

5. **影响者分析**
   - 拥有最多粉丝的用户
   - 最活跃的用户
   - 经过验证的用户比例

6. **趋势洞察**（基于数据模式）
   - 新出现的主题
   - 情感分析指标
   - 时间模式
   - 话题讨论的驱动因素

7. **核心要点**
   - 3-5个核心洞察
   - 基于数据的结论

8. **可操作建议**
   - 具体、可实施的建议
   - 基于数据发现
   - 按重要性排序

#### 分析指南

- **以数据为依据**：每个结论都应引用实际指标
- **提供背景**：解释指标的重要性
- **识别模式**：寻找数据集中的趋势
- **保持客观**：呈现事实，避免猜测
- **具体明确**：建议应具体且可执行
- **考虑外部信息**：在必要时使用网络搜索获取背景信息

### 5. 输出格式

使用清晰的markdown格式呈现报告：
- 每个部分的标题
- 结构化数据的表格
- 列表的列表项
- 关键指标使用粗体显示
- 推文示例使用代码块
- 所有引用推文的**可点击链接**（格式：`[@username](https://x.com/username/status/tweet_id)`）

#### 推文URL格式

始终为推文添加可点击的链接：
```markdown
| Author | Tweet | URL |
|--------|-------|-----|
| @user | Summary of tweet content | [View](https://x.com/user/status/123456) |
```

或者使用内联格式：
```markdown
- **@username**: Tweet summary - [View Tweet](https://x.com/username/status/123456)
```

## 按用例划分的查询示例

### 趋势分析
```
"AI" OR "artificial intelligence" lang:en min_retweets:50
```

### 竞争对手监控
```
from:competitor1 OR from:competitor2 since:2024-01-01
```

### 产品发布跟踪
```
#ProductName OR "Product Name" lang:en filter:verified
```

### 危机监控
```
#BrandName OR "Brand Name" lang:en --query-type Latest
```

### 影响者发现
```
#Topic lang:en min_retweets:100 min_faves:500
```

### 情感分析
```
"brand name" OR #BrandName lang:en --max-results 1000
```

## 资源

### scripts/run_search.sh（包装脚本）

这是一个便捷的包装脚本，负责处理环境变量的加载和依赖检查：
- 自动从`~/.bashrc`或`~/.zshrc`中加载`TWITTER_API_KEY`
- 检查Python是否可用并安装缺失的依赖项
- 提供用户友好的错误信息
- 支持Python脚本中的所有命令行选项

**使用方法**：
```bash
./scripts/run_search.sh <query> [options]
```

**选项**：
- `--api-key KEY`：覆盖环境变量中的API密钥
- `--max-results N`：获取的最大推文数量（默认：1000）
- `--query-type Latest|Top`：排序方式（默认：按相关性排序）
- `--format json|summary`：输出格式（默认：json）

### scripts/twitter_search.py

可执行的Python脚本，用于：
- 从Twitter API获取推文
- 自动处理分页
- 提取关键推文指标
- 计算汇总统计数据
- 输出结构化的JSON数据

**使用方法**：
```bash
scripts/twitter_search.py <api_key> <query> [options]
```

### references/twitter_api.md

全面的API文档，包括：
- 完整的参数参考
- 查询语法指南
- 响应结构详情
- 分页说明
- 分析的最佳实践
- 错误处理指南

**阅读建议**：在构建复杂查询或理解数据结构时参考此文档。

## 更好分析的技巧

1. **使用`Top`查询类型**进行趋势分析（获得更相关的结果）
2. **设置日期过滤器**以获取及时的洞察
3. **按语言过滤**以进行准确的文本分析
4. **设置最小参与度**以过滤无关内容
5. **结合网络搜索**来验证趋势
6. **深入分析内容主题**
7. **跟踪标签**以发现子话题
8. **通过粉丝数量和参与度来识别影响者**

## 错误处理

如果脚本失败：
- 检查API密钥的有效性
- 验证查询语法
- 确保网络连接正常
- 检查速率限制（如适用）
- 查看错误信息以确定具体问题