---
name: parallel-extract
description: "**通过Parallel API提取URL内容**：该功能可以从网页、文章、PDF文件以及JavaScript代码较多的网站中提取干净的Markdown格式内容。适用于需要使用大型语言模型（LLM）处理特定URL数据的场景。"
homepage: https://parallel.ai
---

# 并行提取（Parallel Extract）

从URL中提取干净、适合大型语言模型（LLM）使用的内容。支持处理网页、文章、PDF文件以及需要渲染的JavaScript含量较高的网站。

## 使用场景

当用户提出以下请求时，可使用此功能：
- “阅读这个URL”
- “从...中提取内容”
- “从[URL]获取内容”
- “这篇文章讲了什么？”
- 阅读PDF文件、JavaScript含量较高的页面或需要付费才能访问的内容
- 从杂乱无章的网页中提取清晰的Markdown格式内容

**使用“搜索”功能来发现目标内容，再使用“提取”功能来读取所需信息。**

## 快速入门

```bash
parallel-cli extract "https://example.com/article" --json
```

## 命令行接口（CLI）参考

### 基本用法

```bash
parallel-cli extract "<url>" [options]
```

### 常用参数

| 参数 | 说明 |
|------|-------------|
| `--url "<url>"` | 需要提取内容的URL（最多可输入10个URL） |
| `--objective "<focus>"` | 指定提取的具体内容范围 |
| `--json` | 以JSON格式输出结果 |
| `--excerpts` / `--no-excerpts` | 是否包含相关摘录（默认为包含） |
| `--full-content` / `--no-full-content` | 是否包含完整页面内容 |
| `--excerpts-max-chars N` | 每条摘录的最大字符数 |
| `--excerpts-max-total-chars N` | 所有摘录的最大总字符数 |
| `--full-max-chars N` | 完整页面内容的最大字符数 |
| `-o <file>` | 将输出结果保存到指定文件 |

### 示例

**基本提取：**
```bash
parallel-cli extract "https://example.com/article" --json
```

**针对性提取：**
```bash
parallel-cli extract "https://example.com/pricing" \
  --objective "pricing tiers and features" \
  --json
```

**提取PDF文件的完整内容：**
```bash
parallel-cli extract "https://example.com/whitepaper.pdf" \
  --full-content \
  --json
```

**处理多个URL：**
```bash
parallel-cli extract \
  --url "https://example.com/page1" \
  --url "https://example.com/page2" \
  --json
```

## 默认工作流程

1. 使用带有目标关键词的查询进行“搜索”；
2. 查看标题、URL和发布日期，选择最合适的来源；
3. 提取所需的特定页面内容（前N个URL）；
4. 使用提取到的摘录或内容进行回答。

## 最佳提示方式

### 提供明确的目标

在请求提取内容时，应提供以下信息：
- 你需要查找的具体信息是什么？
- 你为什么需要这些信息（这有助于精确定位提取内容）。

**示例：** `--objective "查找安装步骤和系统要求"`

**错误示例：** `--objective "阅读页面内容"`

## 输出格式

返回结构化的JSON格式数据，包含以下字段：
- `url`：来源URL
- `title`：页面标题
- `excerpts[]`：相关文本摘录（如果启用）
- `full_content`：完整页面内容（如果启用）
- `publish_date`：页面的发布日期

## 输出处理

在将提取的内容呈现给用户时，请注意以下几点：
- 保持内容原样，避免不必要的改写；
- 彻底提取所有列表项；
- 去除无关内容（如导航菜单、页脚、广告、“点击这里”链接等）；
- 保留所有事实、名称、数字、日期和引文；
- 显示URL和发布日期以确保信息的透明度。

## 缺乏上下文怎么办？

对于较长的对话，可以先保存提取结果，然后使用`sessions_spawn`功能启动子代理来继续处理：

```bash
parallel-cli extract "<url>" --json -o /tmp/extract-<topic>.json
```

之后，可以通过````json
{
  "tool": "sessions_spawn",
  "task": "Read /tmp/extract-<topic>.json and summarize the key content.",
  "label": "extract-summary"
}
````启动子代理来继续执行后续任务。

## 错误处理

| 错误代码 | 含义 |
|-----------|---------|
| 0 | 操作成功 |
| 1 | 发生意外错误（网络问题或解析错误） |
| 2 | 参数无效 |
| 3 | API调用失败（非2xx状态码） |

## 先决条件

1. 在[parallel.ai](https://parallel.ai)获取API密钥；
2. 安装相应的命令行工具。

```bash
curl -fsSL https://parallel.ai/install.sh | bash
export PARALLEL_API_KEY=your-key
```

## 参考资料

- [API文档](https://docs.parallel.ai)
- [提取API参考](https://docs.parallel.ai/api-reference/extract)