---
name: web-search
description: 使用 DuckDuckGo 的 Instant Answer API 进行网络搜索（无需 API 密钥）。当您需要在网上查找信息、定义、计算结果、转换数据或快速获取事实时，可以使用此功能。此外，当用户输入“搜索”、“查找”、“查找信息”、“什么是...”、“如何...”或“在 Google 上搜索某内容”等指令时，该功能也能提供即时响应。该技能无需外部 API 凭据即可提供答案、定义、摘要及相关主题内容。
---

# 网页搜索

使用 DuckDuckGo 的 Instant Answer API 进行免费网页搜索，无需 API 密钥。

## 快速入门

```bash
# Basic search
cd /home/hxx/clawd/tools && ./web-search.sh "your query"

# Examples
./web-search.sh "what is artificial intelligence"
./web-search.sh "python programming"
./web-search.sh "define recursion"
./web-search.sh "2+2"
```

## 命令行选项

### 核心选项
- `-h, --help` - 显示带有使用示例的帮助信息
- `--format <format>` - 输出格式：`text`、`markdown`、`plain`（默认：`text`）
  - `text`：带颜色的终端输出（默认）
  - `markdown`：纯 markdown 格式（不含 ANSI 颜色）
  - `plain`：不含颜色的纯文本
- `--no-color` - 禁用彩色输出（与 `--format plain` 功能相同）
- `--max-related <N>` - 控制显示的相关主题数量（默认：5 个）
- `--quiet` - 最小化输出模式（仅显示结果，无标题/页脚）

### 将结果输出到文件
使用 shell 重定向将结果保存到文件：

```bash
# Save to file
./web-search.sh "query" > output.txt

# With markdown format
./web-search.sh --format markdown "query" > results.md

# With no colors for logs
./web-search.sh --no-color "query" > search.log
```

## 工具返回的内容

该工具提供多种结果类型：
- **答案**：针对计算、转换、天气等问题提供的直接答案
- **摘要**：带有来源和链接的维基百科风格摘要
- **定义**：单词/术语的定义
- **相关主题**：其他相关结果（可配置，默认显示 5 个）

## 最佳使用建议
1. **具体说明**：越具体的查询，得到的即时答案越准确
2. **尝试多种表达方式**：如果未找到结果，请重新表述查询
3. **用于获取事实**：定义、计算、快速查询等功能效果最佳
4. **查看链接**：工具始终会提供 DuckDuckGo 的完整搜索链接
5. **选择合适的输出格式**：
   - 终端输出：`--format text`（带颜色，默认）
   - 文档：`--format markdown` > file.md`
   - 日志/管道输出：`--format plain` 或 `--no-color`

## 限制
- 不提供完整的网页搜索结果（仅提供即时答案）
- 根据 DuckDuckGo 的数据，某些查询可能返回有限的结果
- 部分摘要中存在字符编码问题（已知限制）
- 需要互联网连接才能查询 DuckDuckGo API
- 并非所有类型的查询都能得到即时答案（例如，复杂的数学计算如 `sqrt(144)`）
- 并非所有术语的定义都能被提供
- 最新新闻可能不会显示（DuckDuckGo 侧重于长期有效的内容）

## 使用示例

### 基本搜索
```bash
# Simple query
./web-search.sh "open source AI models"

# Wikipedia-style query
./web-search.sh "what is recursion"
```

### Markdown 格式
```bash
# Clean markdown output
./web-search.sh --format markdown "python programming"

# Save to markdown file
./web-search.sh --format markdown "AI research" > research.md
```

### 纯文本/无颜色
```bash
# For logs or piping
./web-search.sh --format plain "search query"

# Disable colors explicitly
./web-search.sh --no-color "search query"
```

### 控制显示的相关主题数量
```bash
# Show fewer related topics
./web-search.sh --max-related 3 "machine learning"

# Show more related topics
./web-search.sh --max-related 10 "open source"
```

### 最小化输出模式
```bash
# Minimal output (just results)
./web-search.sh --quiet "what is 42 + 7"
```

### 综合使用多个选项
```bash
# Markdown, no color, saved to file
./web-search.sh --format markdown --no-color "topic" > results.md

# Quiet with custom related count
./web-search.sh --quiet --max-related 2 "definition"
```

## 测试情况
已测试并通过验证的功能包括：
- ✅ 计算：`2+2`、`10% of 500`
- ✅ 转换：`100 miles to km`
- ✅ 维基百科查询：`what is artificial intelligence`
- ✅ 编程：`what is python`、`how to install docker`
- ✅ 人物信息：`who is Elon Musk`
- ✅ 科学事实：`speed of light`
- ✅ 天气查询：`weather in Tokyo`
- ✅ 特殊情况：空查询、包含特殊字符的查询（无结果）
- ✅ 输出格式：text、markdown、plain
- ✅ 可使用的选项：`--help`、`--format`、`--no-color`、`--max-related`、`--quiet`

详细测试结果请参阅 [test-outputs.md](test-outputs.md)。

## 故障排除
- **“未找到直接结果”**：尝试重新表述查询或使用 DuckDuckGo 的完整搜索链接。
- **网络错误**：请检查网络连接。该工具需要网络访问。
- **字符编码问题**：部分摘要可能显示乱码。这是基本解析过程中的已知问题（建议安装 `jq` 以获得更好的结果）。
- **“未找到 jq”警告**：即使不安装 `jq`，工具也能正常工作（使用基本文本提取方式），但安装 `jq` 可以提高 JSON 解析效果：
```bash
# Ubuntu/Debian
sudo apt-get install jq

# macOS
brew install jq

# Via package managers
npm install -g jq
```

## 输出格式

### 文本格式（默认）
- **蓝色**：标题和搜索信息
- **绿色**：结果标记和内容
- **黄色**：来源、链接和警告信息
- **红色**：错误信息

使用 `--format plain` 或 `--no-color` 可禁用颜色显示。

### Markdown 格式
- 使用以下格式编写文档：
  - `##` 用于创建章节标题
  - `**bold` 用于强调文本
  - `-` 用于创建项目符号列表
  - `*italics*` 用于表示元数据
  - `[links]()` 用于生成链接

### 纯文本格式
不含 ANSI 颜色代码或 markdown 格式，适用于日志和管道传输。

## 所需软件
- `curl` 或 `wget`（用于发送 HTTP 请求）
- 可选：`jq`（用于更高效的 JSON 解析）