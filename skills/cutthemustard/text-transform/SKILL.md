---
name: text-transform
description: 文本转换、正则表达式处理、差异对比、格式转换以及 JSON 数据操作。
version: 1.0.1
metadata:
  openclaw:
    emoji: "📝"
    homepage: https://text.agentutil.net
    always: false
---
# 文本转换（Text Transformation）

支持正则表达式操作、行级差异比较（line-level diffs）、文本转换（如生成URL短链接、调整大小写、统计字符/单词数量、截断文本）、Markdown与HTML之间的转换，以及JSON数据的处理。

## 数据处理（Data Handling）

该功能会将文本发送到外部API进行结构化处理。**在发送任何非用户自动生成的文本之前，必须先征得用户的同意。** 仅允许对代理生成的内容（例如：自定义格式化输出、转换用户创建的标记语言内容、统计用户撰写的草稿中的单词数量）使用此功能；除非用户另有明确要求。未经用户明确指示，严禁发送用户的文档、私人消息或文件内容。

该服务采用无状态（stateless）文本处理方式：处理后的数据不会被存储、记录或保留，仅生成即时响应。

## 接口端点（Endpoints）

### 文本转换（Text Transform）

```bash
curl -X POST https://text.agentutil.net/v1/transform \
  -H "Content-Type: application/json" \
  -d '{"input": "Hello World", "operations": ["slugify", "word_count", "lowercase"]}'
```

支持的操作包括：生成URL短链接（slugify）、截断文本（truncate）、统计单词数量（word_count）、统计字符数量（char_count）、统计行数（line_count）、将文本转换为大写/小写（uppercase/lowercase）、转换文本为标题格式（title_case）、反转文本顺序（reverse）、去除文本两端的空白字符（trim）。

### 正则表达式（Regex）

```bash
curl -X POST https://text.agentutil.net/v1/regex \
  -H "Content-Type: application/json" \
  -d '{"input": "order 123 and 456", "pattern": "\\d+", "operation": "match_all", "flags": "g"}'
```

支持的操作包括：匹配（match）、全局匹配（match_all）、替换（replace）和测试正则表达式（test）。

### 差异比较（Diff）

```bash
curl -X POST https://text.agentutil.net/v1/diff \
  -H "Content-Type: application/json" \
  -d '{"a": "line one\nold line", "b": "line one\nnew line"}'
```

### 格式转换（Format Conversion）

```bash
curl -X POST https://text.agentutil.net/v1/convert \
  -H "Content-Type: application/json" \
  -d '{"input": "# Hello", "from": "markdown", "to": "html"}'
```

### JSON操作（JSON Operations）

```bash
curl -X POST https://text.agentutil.net/v1/json \
  -H "Content-Type: application/json" \
  -d '{"input": "{\"key\": \"value\"}", "operation": "format"}'
```

支持的操作包括：解析JSON数据（parse）、格式化JSON（format）、验证JSON数据（validate）、压缩JSON数据（minify），以及通过`path`参数查询JSON数据。

## 响应格式（Response Format）

```json
{
  "results": {"word_count": 2, "slugify": "hello-world", "lowercase": "hello world"},
  "request_id": "abc-123",
  "service": "https://text.agentutil.net"
}
```

## 价格（Pricing）

- 免费 tier：每天10次查询，无需身份验证。
- 付费 tier：每次查询费用为0.001美元，通过x402协议支付（使用Base币种的USDC）。

## 隐私政策（Privacy）

采用无状态文本处理方式，不会存储或保留任何数据。免费 tier无需身份验证；付费 tier仅使用IP地址进行速率限制。