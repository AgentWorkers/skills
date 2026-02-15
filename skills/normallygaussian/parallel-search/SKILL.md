---
name: parallel-search
description: "通过 Parallel API 实现的 AI 驱动的网络搜索功能。该搜索返回经过排序的结果，并包含针对大型语言模型（LLM）进行优化的摘录内容。适用于最新研究、事实核查以及特定领域的搜索需求。"
homepage: https://parallel.ai
---

# 并行搜索

专为AI代理设计的高精度网络搜索工具。返回经过优化的排名结果，其中包含适合大型语言模型（LLM）使用的摘录内容。

## 使用场景

当用户提出以下请求时，可触发此技能：
- “在网络上搜索”  
- “查找信息”  
- “查询[主题]的最新资料”  
- “核实事实（需要引用来源）”  
- 针对特定领域的搜索（例如：“在GitHub上搜索...”）

## 快速入门

```bash
parallel-cli search "your query" --json --max-results 5
```

## 命令行接口（CLI）参考

### 基本用法

```bash
parallel-cli search "<objective>" [options]
```

### 常用参数

| 参数 | 说明 |
|------|-------------|
| `-q, --query "<关键词>"` | 添加关键词过滤条件（建议使用3-8个关键词） |
| `--max-results N` | 结果数量（1-20个，默认值：10） |
| `--json` | 以JSON格式输出结果 |
| `--after-date YYYY-MM-DD` | 仅显示指定日期之后的内容 |
| `--include-domains domain.com` | 仅限于特定域名（最多10个域名） |
| `--exclude-domains domain.com` | 排除特定域名（最多10个域名） |
| `--excerpt-max-chars-total N` | 限制摘录内容的总字符数（默认值：8000） |

### 示例

**基本搜索：**
```bash
parallel-cli search "When was the United Nations founded?" --json --max-results 5
```

**使用关键词过滤条件：**
```bash
parallel-cli search "Latest developments in quantum computing" \
  -q "quantum" -q "computing" -q "2026" \
  --json --max-results 10
```

**针对特定域名的搜索：**
```bash
parallel-cli search "React hooks best practices" \
  --include-domains react.dev --include-domains github.com \
  --json --max-results 5
```

**仅显示最新新闻：**
```bash
parallel-cli search "AI regulation news" \
  --after-date 2026-01-01 \
  --json --max-results 10
```

## 最佳提示方式

### 编写提示语的技巧

1. 用1-3句话描述实际任务背景（为什么需要这些信息）。
2. 明确对结果新鲜度的要求（例如：“优先显示2026年以后的内容”或“最新文档”）。
3. 指定首选信息来源（如“官方文档”或“新闻网站”）。

### 关键词查询

请使用3-8个关键词进行查询，包括：
- 具体术语、版本号、错误信息等。
- 相关的常用同义词。
- 如果适用，可包含日期信息（如“2026年”、“2026年1月”）。

## 结果格式

返回结构化的JSON数据，包含以下内容：
- `search_id` — 唯一标识符
- `results[]` — 结果数组：
  - `url` — 网页链接
  - `title` — 页面标题
  - `excerpts[]` — 相关文本摘录
  - `publish_date` — 文章发布日期

## 结果展示方式

在向用户展示结果时：
- 尽量使用**官方/主要来源**的信息。
- **仅**引用或改写相关的摘录内容。
- 显示**链接和发布日期**以增加透明度。
- 如果存在不同结果，请同时展示并说明差异。

## 情况复杂时如何处理？

对于较长的对话过程，可以先保存搜索结果，然后使用`sessions_spawn`函数启动一个子代理来继续处理后续任务：

```bash
parallel-cli search "<query>" --json -o /tmp/search-<topic>.json
```

之后，可以创建一个新的子代理来执行后续操作：

```json
{
  "tool": "sessions_spawn",
  "task": "Read /tmp/search-<topic>.json and synthesize a summary with sources.",
  "label": "search-summary"
}
```

## 错误处理

| 错误代码 | 含义 |
|-----------|---------|
| 0 | 操作成功 |
| 1 | 发生意外错误（网络问题或数据解析错误） |
| 2 | 参数格式不正确 |
| 3 | API调用失败（非2xx状态码） |

## 先决条件

1. 从[parallel.ai](https://parallel.ai)获取API密钥。
2. 安装相应的命令行工具。

```bash
curl -fsSL https://parallel.ai/install.sh | bash
export PARALLEL_API_KEY=your-key
```

## 参考资料

- [API文档](https://docs.parallel.ai)
- [搜索API参考](https://docs.parallel.ai/api-reference/search)