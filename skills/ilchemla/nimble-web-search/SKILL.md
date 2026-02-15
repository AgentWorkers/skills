---
name: nimble-web-search
description: >
  Real-time web intelligence powered by Nimble Search API. Perform intelligent web searches with 8 specialized focus modes (general, coding, news, academic, shopping, social, geo, location).
  This skill provides real-time search results when you need to search the web, find current information, discover URLs, research topics, or gather up-to-date data.
  Use when: searching for information, finding recent news, looking up academic papers, searching for coding examples, finding shopping results, discovering social media posts, researching topics, or getting latest real-time data.
license: MIT
metadata:
  version: "0.1.0"
  author: Nimbleway
  repository: https://github.com/Nimbleway/agent-skills
---

# Nimble Web Search

使用Nimble Search API实现实时网络情报检索，支持多种专注模式，并具备基于人工智能的结果合成功能。

## 先决条件

**需要Nimble API密钥** - 请在https://www.nimbleway.com/获取您的密钥。

### 配置

使用您的平台方法设置`NIMBLE_API_KEY`环境变量：

**Claude Code:**
```json
// ~/.claude/settings.json
{
  "env": {
    "NIMBLE_API_KEY": "your-api-key-here"
  }
}
```

**VS Code/GitHub Copilot:**
- 将密钥添加到仓库的`.github/skills/`目录中
- 或使用GitHub Actions的秘密配置来设置Copilot环境变量

**Shell/Terminal:**
```bash
export NIMBLE_API_KEY="your-api-key-here"
```

**任何平台:**
无论您使用何种平台，系统都会检查`NIMBLE_API_KEY`环境变量的存在。

### API密钥验证

**重要提示：** 在发送任何搜索请求之前，请确保API密钥已正确配置：

```bash
# Check if API key is set
if [ -z "$NIMBLE_API_KEY" ]; then
  echo "❌ Error: NIMBLE_API_KEY not configured"
  echo ""
  echo "Get your API key: https://www.nimbleway.com/"
  echo ""
  echo "Configure using your platform's method:"
  echo "- Claude Code: Add to ~/.claude/settings.json"
  echo "- GitHub Copilot: Use GitHub Actions secrets"
  echo "- Shell: export NIMBLE_API_KEY=\"your-key\""
  echo ""
  echo "Do NOT fall back to other search tools - guide the user to configure first."
  exit 1
fi
```

## 概述

Nimble Search提供实时网络情报服务，支持8种专为不同类型查询优化的专注模式。它能够通过人工智能生成答案、深度内容提取、URL发现以及按域名和日期进行智能过滤来即时获取网络数据。

**重要提示：** 使用此功能时，**务必在请求中明确指定**以下参数：

- `deep_search`：**默认值为`false`，可加快5-10倍的响应速度**
  - **使用`false`（快速模式 - 1-3秒）：**适用于95%的用例（如URL发现、研究、比较、答案生成）
  - **使用`true`（深度模式 - 5-15秒）：**仅在需要提取完整页面内容以进行存档或详细分析时使用

- `focus`：**默认值为`"general"`，适用于广泛搜索**
  - 可更改为特定模式（`coding`、`news`、`academic`、`shopping`、`social`、`geo`、`location`）以获得更精准的结果

- `max_results`：**默认值为10**，以平衡搜索速度和覆盖范围

**性能提示：** 显式设置`deep_search: false`时，系统会使用快速模式，响应时间约为1-3秒。如果设置`deep_search: true`，响应时间约为5-15秒。

### 快速入门

使用包装脚本可获得最简单的使用体验：

```bash
# ALWAYS specify deep_search explicitly
./scripts/search.sh '{
  "query": "React hooks",
  "deep_search": false
}'
```

该脚本会自动处理身份验证、跟踪请求头和输出格式化。

### 各模式的适用场景

**使用`deep_search: false`（快速模式 - 1-3秒） - 适用于95%的用例：**
- ✅ 查找URL和资源
- ✅ 研究和主题探索
- ✅ 生成答案和摘要
- ✅ 产品比较
- ✅ 新闻监控
- ✅ 任何不需要完整文章内容的情况

**使用`deep_search: true`（深度模式 - 5-15秒） - 仅在需要时使用：**
- 📄 存档完整文章内容
- 📄 提取完整文档
- 📄 构建文本数据集
- 📄 处理完整页面内容以进行分析

**决策规则：** 如果不确定如何选择，建议使用`deep_search: false`。如有需要，可以随时重新运行并设置为`true`。

## 核心功能

### 专注模式

根据查询类型选择合适的专注模式：

1. **general** - 适用于广泛的网络搜索
2. **coding** - 实时访问技术文档、代码示例和编程资源
3. **news** - 实时新闻文章、时事新闻
4. **academic** - 研究论文、学术文章和学术资源
5. **shopping** - 实时产品搜索、电子商务结果和价格比较
6. **social** - 实时社交媒体帖子、讨论和热门社区内容
7. **geo** - 基于位置的搜索和地理信息
8. **location** - 本地商家搜索和特定地点的查询

### 搜索功能

**LLM答案生成**
- 从搜索结果中生成人工智能生成的答案
- 由Claude提供高质量摘要
- 包含来源URL的引用
- 适用于：研究问题、主题概述和比较分析

**URL发现**
- 为查询提取1-20个最相关的URL
- 适用于构建阅读列表和参考资料库
- 返回带有标题和描述的URL
- 适用于：资源收集、链接构建和研究准备

**深度内容提取**
- **默认（推荐）：** `deep_search=false` - 响应最快，返回标题、描述和URL
- **可选：** `deep_search=true` - 提取完整页面内容
- **注意：** 大多数用例使用`deep_search=false`（默认设置）即可满足需求
- 当`deep_search=true`时，支持的输出格式包括：markdown、plain_text、simplified_html
- 仅在需要详细内容分析、存档或全面提取文本时启用深度搜索

**域名过滤**
- 包含特定域名（例如：github.com、stackoverflow.com）
- 排除不需要的域名
- 结合多个域名进行定向搜索
- 适用于：针对性研究、品牌监控和竞争分析

**时间过滤**
- **推荐：** 使用`time_range`进行实时时效性过滤（小时、天、周、月、年）
- **替代方案：** 使用`start_date`/`end_date`进行精确日期范围过滤（YYYY-MM-DD）
- **注意：** `time_range`和日期过滤器是互斥的
- 适用于：实时新闻监控、最新发展和时间分析

## 使用示例

以下示例均使用`./scripts/search.sh`包装脚本。如需直接使用API，请参阅[API集成](#api-integration)部分。

### 基本搜索

使用快速模式进行快速搜索（务必明确指定`deep_search`）：

```bash
./scripts/search.sh '{
  "query": "React Server Components tutorial",
  "deep_search": false
}'
```

对于技术内容，指定`coding`专注模式（仍然使用快速模式）：

```bash
./scripts/search.sh '{
  "query": "React Server Components tutorial",
  "focus": "coding",
  "deep_search": false
}'
```

### 基于AI的摘要研究

从多个来源获取综合见解（快速模式非常适合答案生成）：

```bash
./scripts/search.sh '{
  "query": "impact of AI on software development 2026",
  "deep_search": false,
  "include_answer": true
}'
```

### 域名特定搜索

针对特定权威来源进行搜索（快速模式）：

```bash
./scripts/search.sh '{
  "query": "async await patterns",
  "focus": "coding",
  "deep_search": false,
  "include_domains": ["github.com", "stackoverflow.com", "dev.to"],
  "max_results": 8
}'
```

### 实时新闻监控

实时跟踪当前事件和突发新闻（快速模式）：

```bash
./scripts/search.sh '{
  "query": "latest developments in quantum computing",
  "focus": "news",
  "deep_search": false,
  "time_range": "week",
  "max_results": 15,
  "include_answer": true
}'
```

### 学术研究 - 快速模式（推荐）

使用快速模式查找和合成学术内容：

```bash
./scripts/search.sh '{
  "query": "machine learning interpretability methods",
  "focus": "academic",
  "deep_search": false,
  "max_results": 20,
  "include_answer": true
}'
```

**何时使用深度模式：** 仅在需要提取完整论文内容以进行存档时使用`deep_search: true`：

```bash
./scripts/search.sh '{
  "query": "machine learning interpretability methods",
  "focus": "academic",
  "deep_search": true,
  "max_results": 5,
  "output_format": "markdown"
}'
```
**注意：** 深度模式的响应速度较慢（约5-15倍）。仅在必要时使用。

### 实时购物研究

比较产品和当前价格（快速模式）：

```bash
./scripts/search.sh '{
  "query": "best mechanical keyboards for programming",
  "focus": "shopping",
  "deep_search": false,
  "max_results": 10,
  "include_answer": true
}'
```

## 并行搜索策略

### 何时使用并行搜索

在以下情况下可以并行运行多个实时搜索：
- **比较不同视角**：在同一主题下使用不同的专注模式进行搜索
- **多方面研究**：同时调查一个主题的多个方面
- **竞争分析**：同时搜索多个域名或竞争对手
- **实时监控**：同时跟踪多个主题或关键词
- **交叉验证**：实时验证不同来源的信息

### 实现方法

**方法1：后台进程（推荐）**

使用包装脚本同时运行多个搜索：

```bash
# Start multiple searches in parallel
./scripts/search.sh '{"query": "React", "focus": "coding"}' > react_coding.json &
./scripts/search.sh '{"query": "React", "focus": "news"}' > react_news.json &
./scripts/search.sh '{"query": "React", "focus": "academic"}' > react_academic.json &

# Wait for all to complete
wait

# Combine results
jq -s '.' react_*.json > combined_results.json
```

**方法2：使用xargs进行控制并行性**

通过限制请求速率来处理多个查询：

```bash
# Create queries file
cat > queries.txt <<EOF
{"query": "AI frameworks", "focus": "coding"}
{"query": "AI regulation", "focus": "news"}
{"query": "AI research", "focus": "academic"}
EOF

# Run with max 3 parallel processes
cat queries.txt | xargs -n1 -P3 -I{} ./scripts/search.sh '{}'
```

**方法3：比较不同专注模式下的搜索结果**

在同一主题下使用不同的专注模式进行搜索：

```bash
QUERY="artificial intelligence trends"

for focus in "general" "coding" "news" "academic"; do
  (
    ./scripts/search.sh "{\"query\": \"$QUERY\", \"focus\": \"$focus\"}" \
      > "${focus}_results.json"
  ) &
done

wait
echo "All searches complete!"
```

### 并行执行的最佳实践

1. **限制请求速率**：将并行请求数量限制在3-5个，以避免超出API的承受能力
   - 使用`xargs -P3`设置最大并发请求数
   - 在增加并行性之前，请检查您的API层级限制

2. **错误处理**：优雅地捕获和处理错误
   ```bash
   ./scripts/search.sh '{"query": "test"}' || echo "Search failed" >> errors.log
   ```

3. **结果聚合**：所有搜索完成后合并结果
   ```bash
   # Wait for all searches
   wait

   # Merge JSON results
   jq -s 'map(.results) | flatten' result*.json > combined.json
   ```

4. **进度跟踪**：监控搜索完成状态
   ```bash
   echo "Running 5 parallel searches..."

   for i in {1..5}; do
     ./scripts/search.sh "{\"query\": \"query$i\"}" > "result$i.json" &
   done

   wait
   echo "All searches complete!"
   ```

### 示例：多视角研究

```bash
#!/bin/bash
# Research a topic across multiple focus modes simultaneously

QUERY="artificial intelligence code generation"
OUTPUT_DIR="./search_results"
mkdir -p "$OUTPUT_DIR"

# Run searches in parallel across different focus modes
for focus in "general" "coding" "news" "academic"; do
  (
    ./scripts/search.sh "{
      \"query\": \"$QUERY\",
      \"focus\": \"$focus\",
      \"max_results\": 10
    }" > "$OUTPUT_DIR/${focus}_results.json"
  ) &
done

# Wait for all searches to complete
wait

# Aggregate and analyze results
jq -s '{
  general: .[0].results,
  coding: .[1].results,
  news: .[2].results,
  academic: .[3].results
}' "$OUTPUT_DIR"/*.json > "$OUTPUT_DIR/combined_analysis.json"

echo "✓ Multi-perspective search complete"
```

### 性能考虑

- **最佳并行度**：3-5个并发请求可以平衡搜索速度和API限制
- **内存使用**：每个并行请求会占用内存；请注意处理大量结果集
- **网络带宽**：并行请求可能会占用较慢连接的网络带宽
- **API费用**：并行请求越多，API配额消耗越快

### 何时不使用并行搜索

- 单个、明确的查询，且只需要一个答案
- 需要每个搜索结果来指导后续操作的顺序研究
- API配额有限或费用较高
- 结果需要在下一次搜索前进行处理
- 仅需要简单URL集合，不需要多角度分析

## API集成

**注意：** 对于大多数用例，建议使用[使用示例](#usage-patterns)中提供的`./scripts/search.sh`包装脚本。以下原始API示例适用于需要直接API访问或自定义集成的高级用户。

### 必需配置

**在发送任何API请求之前，请务必验证API密钥已正确配置：**

```bash
# Validate API key is set
if [ -z "$NIMBLE_API_KEY" ]; then
  echo "❌ Nimble API key not configured."
  echo "Get your key at https://www.nimbleway.com/"
  echo ""
  echo "Set NIMBLE_API_KEY environment variable using your platform's method."
  exit 1
fi
```

该功能需要`NIMBLE_API_KEY`环境变量。具体平台设置说明请参阅[先决条件](#prerequisites)。

请在https://www.nimbleway.com/获取您的API密钥。

### API端点

```
POST https://nimble-retriever.webit.live/search
```

### 请求格式

```json
{
  "query": "search query string",  // REQUIRED
  "focus": "general",  // OPTIONAL: default "general" | coding|news|academic|shopping|social|geo|location
  "max_results": 10,  // OPTIONAL: default 10 (range: 1-100)
  "include_answer": false,  // OPTIONAL: default false
  "deep_search": false,  // OPTIONAL: default false (RECOMMENDED: keep false for speed)
  "output_format": "markdown",  // OPTIONAL: default "markdown" | plain_text|simplified_html
  "include_domains": ["domain1.com"],  // OPTIONAL: default [] (no filter)
  "exclude_domains": ["domain3.com"],  // OPTIONAL: default [] (no filter)
  "time_range": "week",  // OPTIONAL: hour|day|week|month|year
  "start_date": "2026-01-01",  // OPTIONAL: Use time_range OR start_date/end_date (not both)
  "end_date": "2026-12-31"  // OPTIONAL
}
```

**默认参数：**
- `focus`：`"general"` - 如需特定结果，请更改为相应模式
- `deep_search`：`false` - 除非需要完整页面内容，否则保持默认值
- `max_results`：`10` - 平衡搜索速度和覆盖范围

### 响应格式

```json
{
  "results": [
    {
      "url": "https://example.com/page",
      "title": "Page Title",
      "description": "Page description",
      "content": "Full page content (if deep_search=true)",
      "published_date": "2026-01-15"
    }
  ],
  "include_answer": "AI-generated summary (if include_answer=true)",
  "urls": ["url1", "url2", "url3"],
  "total_results": 10
}
```

## 最佳实践

### 专注模式选择

- **使用`coding`进行：**
  - 编程问题
  - 技术文档
  - 代码示例和教程
  - API参考
  - 框架指南

- **使用`news`进行：**
  - 实时时事新闻
  - 突发新闻
  - 最新公告
  - 热门话题
  - 敏感时间的信息

- **使用`academic`进行：**
  - 研究论文
  - 学术文章
  - 科学研究
  - 学术期刊
  - 引用和参考文献

- **使用`shopping`进行：**
  - 产品搜索
  - 价格比较
  - 电子商务研究
  - 产品评论
  - 购物指南

- **使用`social`进行：**
  - 实时社交媒体监控
  - 实时社区讨论
  - 用户生成的内容
  - 热门标签和话题
  - 实时公众情绪

- **使用`geo`进行：**
  - 地理信息
  - 区域数据
  - 地图和位置
  - 特定地区的查询

- **使用`location`进行：**
  - 本地商家搜索
  - 特定地点的信息
  - 附近服务
  - 地区推荐

### 结果数量限制

- **快速搜索**：5-10个结果，以获得快速概览
- **全面研究**：15-20个结果，以获得更详细的信息
- **答案生成**：10-15个结果，以获得平衡的结果
- **URL收集**：20个结果，以获得完整的资源列表

### 何时使用LLM答案

✅ **在以下情况下使用LLM答案：**
  - 需要对某个主题进行综合概述
  - 比较多个来源或方法
  - 总结最新发展
  - 回答具体问题
  - 创建研究摘要

❌ **在以下情况下跳过LLM答案：**
  - 仅需要URL列表
  - 构建参考资料库
  - 对速度要求较高
  - 需要手动分析来源
  - 需要原始来源文本

### 内容提取

**默认（推荐）：`deep_search=false`**

默认设置适用于95%的用例：
- ✅ 响应速度最快
- ✅ 返回标题、描述和URL
- ✅ 与`include_answer=true`配合使用效果最佳
- ✅ 适用于研究、比较和URL发现

**仅在需要时使用`deep_search=true`：**
- 提取完整页面内容
- 存档完整文章
- 处理全文以进行分析
- 构建全面的数据集

**性能影响：**
- `deep_search=false`：约1-3秒
- `deep_search=true`：约5-15秒（明显较慢）

## 错误处理

### 常见问题

**身份验证失败**
- 确保`NIMBLE_API_KEY`设置正确
- 检查API密钥在nimbleway.com上是否有效
- 确保密钥具有搜索API访问权限

**请求速率限制**
- 减少`max_results`的数量
- 在请求之间添加延迟
- 检查您的计划限制
- 考虑升级API层级

**无结果**
- 尝试不同的专注模式
- 扩展搜索范围
- 移除域名过滤器
- 调整日期过滤器

**超时错误**
- 减少`max_results`的数量
- 关闭深度内容提取
- 简化查询
- 稍后重试

## 性能技巧

1. **使用默认设置**：保持`deep_search=false`（默认设置）以获得更快的响应速度
2. **从简单开始**：从`{"query": "..."`开始
3. **选择正确的专注模式**：合适的专注模式可以显著提高搜索相关性（默认设置为“general”）
4. **优化结果数量**：默认的10个结果可以平衡搜索速度和覆盖范围
5. **域名过滤**：预先过滤来源以获得更快、更相关的结果
6. **避免深度搜索**：仅在确实需要完整内容时启用`deep_search=true`
7. **批量查询**：将相关搜索分组以减少API调用次数
8. **缓存结果**：在适当的情况下将结果存储在本地

## 集成示例

请查看`examples/`目录中的详细集成示例：
- `basic-search.md` - 简单搜索实现
- `deep-research.md` - 多步骤研究工作流程
- `competitive-analysis.md` - 域名特定研究示例

请查看`references/`目录中的详细文档：
- `focus-modes.md` - 完整的专注模式指南
- `search-strategies.md` - 高级搜索技巧
- `api-reference.md` - 完整的API文档

## 脚本

### search.sh - 主要搜索包装脚本

推荐的使用Nimble Search API的方法：

```bash
./scripts/search.sh '{"query": "your search", "focus": "coding"}'
```

**特点：**
- 使用`$NIMBLE_API_KEY`进行自动身份验证
- 检测平台类型（claude-code、github-copilot、vscode、cli）
- 为分析目的跟踪请求头
- JSON格式验证和错误处理
- 使用`jq`进行输出格式化

**使用方法：**
```bash
# Basic search
./scripts/search.sh '{"query": "React hooks"}'

# With all options
./scripts/search.sh '{
  "query": "AI frameworks",
  "focus": "coding",
  "max_results": 15,
  "include_answer": true,
  "include_domains": ["github.com"]
}'
```

### validate-query.sh - API配置测试

测试您的API配置和连接性：

```bash
./scripts/validate-query.sh "test query" general
```

该脚本会验证：
- API密钥是否已配置
- 端点是否可访问
- 响应格式是否正确
- 是否支持专注模式