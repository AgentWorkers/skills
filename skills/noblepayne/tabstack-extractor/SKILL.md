---
name: tabstack-extractor
description: 使用 Tabstack API 从网站中提取结构化数据。适用于抓取职位列表、新闻文章、产品页面或任何具有结构化格式的网页内容。该工具支持基于 JSON 模式的数据提取，并能将提取到的数据转换为格式规范的 Markdown 文本。使用前需设置 `TABSTACK_API_KEY` 环境变量。
---

# Tabstack 提取器

## 概述

该技能允许使用 Tabstack API 从网站中提取结构化数据。它非常适合用于网页抓取任务，特别是在需要从招聘网站、新闻网站、产品页面或任何结构化内容中提取一致且基于模式的数据时。

## 快速入门

### 1. （如需要）安装 Babashka
```bash
# Option A: From GitHub (recommended for sharing)
curl -s https://raw.githubusercontent.com/babashka/babashka/master/install | bash

# Option B: From Nix
nix-shell -p babashka

# Option C: From Homebrew
brew install borkdude/brew/babashka
```

### 2. 设置 API 密钥

**选项 A：环境变量（推荐）**
```bash
export TABSTACK_API_KEY="your_api_key_here"
```

**选项 B：配置文件**
```bash
mkdir -p ~/.config/tabstack
echo '{:api-key "your_api_key_here"}' > ~/.config/tabstack/config.edn
```

**获取 API 密钥：** 在 [Tabstack 控制台](https://console.tabstack.ai/signup) 注册

### 3. 测试连接
```bash
bb scripts/tabstack.clj test
```

### 4. 提取 Markdown（简单示例）
```bash
bb scripts/tabstack.clj markdown "https://example.com"
```

### 5. 提取 JSON（简单示例）
```bash
# Start with simple schema (fast, reliable)
bb scripts/tabstack.clj json "https://example.com" references/simple_article.json

# Try more complex schemas (may be slower)
bb scripts/tabstack.clj json "https://news.site" references/news_schema.json
```

### 6. 高级功能
```bash
# Extract with retry logic (3 retries, 1s delay)
bb scripts/tabstack.clj json-retry "https://example.com" references/simple_article.json

# Extract with caching (24-hour cache)
bb scripts/tabstack.clj json-cache "https://example.com" references/simple_article.json

# Batch extract from URLs file
echo "https://example.com" > urls.txt
echo "https://example.org" >> urls.txt
bb scripts/tabstack.clj batch urls.txt references/simple_article.json
```

## 核心功能

### 1. Markdown 提取
从任何网页中提取干净、易读的 Markdown 格式的内容。适用于内容分析、摘要生成或归档。

**使用场景：** 当您需要获取网页的文本内容而不需要 HTML 格式时。

**示例用法：**
- 提取文章内容以进行摘要生成
- 归档网页内容
- 分析博客文章内容

### 2. JSON 模式提取
使用 JSON 模式提取结构化数据。您可以精确定义所需的数据，并以一致的格式获取。

**使用场景：** 在抓取招聘信息、产品页面或新闻文章等结构化数据时。

**示例用法：**
- 从 BuiltIn/LinkedIn 网站抓取招聘信息
- 从电子商务网站提取产品详情
- 收集带有统一元数据的新文章

### 3. 模式模板
为常见的抓取任务提供了预先构建的模式模板。请查看 `references/` 目录以获取模板。

**可用模板：**
- 招聘信息模式（参见 `references/job_schema.json`）
- 新闻文章模式
- 产品页面模式
- 联系信息模式

## 工作流程：抓取招聘信息示例

按照以下步骤抓取招聘信息：

1. **确定目标网站** - BuiltIn、LinkedIn 或公司职业页面
2. **选择或创建模式** - 使用 `references/job_schema.json` 或自定义模式
3. **测试提取** - 运行单个页面以验证模式是否正确
4. **扩展抓取范围** - 处理多个 URL
5. **存储结果** - 保存到数据库或文件中

**示例招聘信息模式：**
```json
{
  "type": "object",
  "properties": {
    "title": {"type": "string"},
    "company": {"type": "string"},
    "location": {"type": "string"},
    "description": {"type": "string"},
    "salary": {"type": "string"},
    "apply_url": {"type": "string"},
    "posted_date": {"type": "string"},
    "requirements": {"type": "array", "items": {"type": "string"}}
  }
}
```

## 与其他技能的集成

### 与 Web 搜索结合使用
1. 使用 `web_search` 找到相关 URL
2. 使用 Tabstack 从这些 URL 中提取结构化数据
3. 将结果存储在 Datalevin 中（后续技能）

### 与浏览器自动化结合使用
1. 使用 `browser` 工具导航复杂网站
2. 提取页面 URL
3. 使用 Tabstack 进行结构化数据提取

## 错误处理

常见问题及解决方法：

1. **身份验证失败** - 检查 `TABSTACK_API_KEY` 环境变量
2. **无效 URL** - 确保 URL 可访问且正确
3. **模式不匹配** - 调整模式以匹配页面结构
4. **速率限制** - 在请求之间添加延迟

## 资源

### 脚本/
- `tabstack.clj` - Babashka 中的主要 API 包装器（推荐，具有重试逻辑、缓存和批量处理功能）
- `tabstack_curl.sh` - Bash/curl 替代方案（简单，无依赖项）
- `tabstack_api.py` - Python API 包装器（需要 `requests` 模块）

### 参考资料/
- `job_schema.json` - 招聘信息模式模板
- `api_reference.md` - Tabstack API 文档

## 最佳实践

1. **从小处开始** - 在扩展之前先测试单个页面
2. **遵守 robots.txt** - 查看网站的抓取政策
3. **添加延迟** - 避免对目标网站造成负担
4. **验证模式** - 在示例页面上测试模式
5. **优雅地处理错误** - 为失败的请求实现重试逻辑

## 教学重点：如何创建模式

该技能旨在教授代理如何有效使用 Tabstack API。关键在于学习如何为不同网站创建合适的 JSON 模式。

### 学习路径
1. **从简单开始** - 使用 `references/simple_article.json`（4 个基本字段）
2. **广泛测试** - 在多种页面类型上测试模式
3. **迭代优化** - 根据页面实际内容添加字段
4. **优化** - 删除不必要的字段以提高速度

详细说明和示例请参阅 [模式创建指南](references/schema_guide.md)。

### 常见错误及避免方法
- **模式过于复杂** - 从 2-3 个字段开始，而不是 20 个
- **缺少字段** - 不要要求页面上不存在的字段
- **不进行测试** - 先在 example.com 上测试，然后再针对目标网站进行测试
- **忽略超时设置** - 复杂的模式可能需要更长的时间（建议设置 45 秒的超时）

## Babashka 的优势

使用 Babashka 进行此技能开发具有以下优势：

1. **单一二进制文件** - 易于共享和安装（支持 GitHub 发布、Brew 和 Nix）
2. **快速启动** - 无需 JVM 加热时间，启动时间约 50 毫秒
3. **内置 HTTP 客户端** - 无需外部依赖项
4. **Clojure 语法** - 对您来说较为熟悉且表达能力强
5. **内置重试逻辑和缓存** - 自动实现
6. **批量处理** - 可同时处理多个 URL

## 用户示例请求

**触发此技能的命令示例：**
- “从 Docker 职业页面抓取招聘信息”
- “从这篇文章中提取主要内容”
- “从这个电子商务页面提取产品数据”
- “从这个网站获取所有新闻文章”
- “从这个公司页面提取联系信息”
- “从这 20 个 URL 批量提取招聘信息”
- “获取该页面的缓存结果（避免重复调用 API）”