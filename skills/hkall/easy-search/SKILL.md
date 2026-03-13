---
name: "easy-search"
description: "**使用多个搜索引擎进行简单的网络搜索，无需API密钥。** 支持 Google、Bing、DuckDuckGo、Baidu、Sogou、360、Brave、Yandex 等搜索引擎。具备时间过滤、交互式模式、片段提取以及网络诊断功能。"
---
# 简易搜索技能

这是一个强大的网络搜索工具，无需使用API密钥。它通过直接的HTTP请求和`duckduckgo_search`库来获取可靠的结果。

## 特点

- **无需API密钥**：使用公开的搜索接口
- **支持9个搜索引擎**：Google、Bing、DuckDuckGo、Baidu、Sogou、360、Brave、Yandex、Startpage
- **自动选择搜索引擎**：自动选择最佳可用引擎
- **提取结果片段**：获取结果预览，而不仅仅是标题
- **时间过滤**：按天/周/月/年进行过滤
- **交互式模式**：支持实时切换搜索引擎的连续搜索
- **网络诊断**：内置网络连接检查及代理提示功能
- **支持代理**：尊重`ALL_PROXY`和`HTTPS_PROXY`环境变量
- **结果缓存**：重复搜索时更快
- **智能故障转移**：在出现故障时自动切换到备用引擎

## 系统要求

- Python 3.6及以上版本
- 可选：安装`pip install duckduckgo-search requests`以获得更好的搜索效果

## 命令

### 基本搜索

```bash
# Simple search (positional argument)
python3 {baseDir}/scripts/search.py Python tutorial

# With flag
python3 {baseDir}/scripts/search.py --query "your search terms"

# Specify engine
python3 {baseDir}/scripts/search.py "AI news" --engine bing

# More results
python3 {baseDir}/scripts/search.py "React hooks" --results 10

# JSON output (default)
python3 {baseDir}/scripts/search.py "Vue.js" --format json

# Markdown output
python3 {baseDir}/scripts/search.py "machine learning" --format md

# Simple output (quick reading)
python3 {baseDir}/scripts/search.py "Docker" --format simple

# CSV output
python3 {baseDir}/scripts/search.py "Kubernetes" --format csv
```

### 时间过滤

```bash
# News from last 24 hours
python3 {baseDir}/scripts/search.py "AI news" --time day

# Results from last week
python3 {baseDir}/scripts/search.py "React 19" --time week

# Results from last month
python3 {baseDir}/scripts/search.py "Python 3.13" --time month

# Results from last year
python3 {baseDir}/scripts/search.py "best laptops 2024" --time year
```

### 交互式模式

```bash
# Start interactive mode
python3 {baseDir}/scripts/search.py --interactive

# In interactive mode:
# [auto]> Python tutorial          # Search with auto engine
# [auto]> :engine duckduckgo       # Change engine
# [duckduckgo]> React hooks        # Search with new engine
# [duckduckgo]> :format simple     # Change output format
# [duckduckgo]> :check             # Check engine health
# [duckduckgo]> :quit              # Exit
```

### 网络诊断

```bash
# Run network diagnostics
python3 {baseDir}/scripts/search.py --diagnose

# Check which engines are available
python3 {baseDir}/scripts/search.py --check-engines
```

### 引擎管理

```bash
# Clear cache
python3 {baseDir}/scripts/search.py --clear-cache

# Disable auto-fallback (stay on specified engine)
python3 {baseDir}/scripts/search.py "query" --engine google --no-fallback
```

## 支持的搜索引擎

| 引擎 | 适用场景 | 备注 |
|--------|----------|-------|
| `auto` | 通用搜索 | 自动选择最佳可用引擎 |
| `startpage` | 遵守隐私政策，全球适用 | 以隐私保护为核心，HTML解析可靠 |
| `duckduckgo` | 遵守隐私政策，全球适用 | 如果已安装该库，则优先使用该引擎 |
| `bing` | 全球搜索 | 可靠性高，结果片段质量不错 |
| `google` | 搜索效果最佳 | 在某些地区可能需要使用代理 |
| `baidu` | 中文内容搜索 | 具有强大的反爬虫机制 |
| `sogou` | 中文内容搜索 | Baidu的优质替代方案 |
| `so360` | 中文内容搜索 | 另一个中文搜索选项 |
| `brave` | 重视隐私保护 | 指数持续增长 |
| `yandex` | 俄罗斯/全球适用 | 在某些地区可用 |

## 输出格式

- **JSON**  
- **Markdown**  
- **简单文本**  

## 示例

```bash
# Quick search for documentation
python3 {baseDir}/scripts/search.py "Python requests library docs"

# Search Chinese content with Sogou
python3 {baseDir}/scripts/search.py "人工智能最新进展" --engine sogou

# Get recent news in markdown format
python3 {baseDir}/scripts/search.py "OpenAI news" --time day --format md

# Use interactive mode for multiple searches
python3 {baseDir}/scripts/search.py -i

# Search with time filter
python3 {baseDir}/scripts/search.py "React 19 features" --time month --results 10
```

## 代理配置

设置环境变量以支持代理：

```bash
# Set proxy
export ALL_PROXY="http://127.0.0.1:7890"
export HTTPS_PROXY="http://127.0.0.1:7890"

# Then run search
python3 {baseDir}/scripts/search.py "your query"
```

## 常见问题及解决方法

| 问题 | 解决方案 |
|---------|----------|
| 没有结果 | 使用`--engine`参数尝试其他搜索引擎 |
| 连接超时 | 检查代理设置或使用`--timeout 60`参数 |
| 被限制搜索频率 | 在搜索之间等待一段时间或切换搜索引擎 |
| DuckDuckGo搜索速度慢 | 安装`duckduckgo-search`库 |
| 无法提取结果片段 | 部分搜索引擎对结果片段的提取有限 |
| Google无法访问 | 使用代理或切换到Bing/DuckDuckGo |
| 所有引擎均无法使用 | 运行`--diagnose`命令检查网络连接 |

## 获取最佳搜索结果的小贴士

1. **使用`auto`引擎**：让工具自动选择最佳搜索引擎
2. **安装依赖库**：安装`pip install duckduckgo-search requests`以提高搜索可靠性
3. **使用时间过滤**：对于新闻或最新话题，使用`--time day`或`--time week`参数
4. **尝试中文搜索引擎**：使用`sogou`或`so360`搜索中文内容
5. **交互式模式**：适合进行多次相关搜索
6. **利用缓存**：重复搜索时速度更快（结果缓存1小时）
7. **运行诊断工具**：使用`--diagnose`命令排查网络问题

## 版本历史

- **v1.1.0**：新增Startpage引擎并优化了URL中的HTML实体解码
- **v1.0.1**：添加网络诊断功能，改进了代理提示信息，优化了错误提示
- **v1.0.0**：新增4个搜索引擎（Sogou、360、Brave、Yandex），支持时间过滤和交互式模式，改进了结果片段提取功能
- **v4.0.0**：集成`duckduckgo_search`库，实现自动引擎选择
- **v1.0.0**：初始版本，包含基本搜索功能