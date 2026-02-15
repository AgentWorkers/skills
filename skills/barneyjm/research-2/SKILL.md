---
name: research
description: "您可以在终端中直接获取关于任何主题的由 AI 合成的研究结果，并附带引用信息。该工具支持结构化的 JSON 输出格式，适用于数据管道（pipelines）的处理。当您需要基于网络数据进行全面的研究，而无需编写代码时，可以使用该工具。"
---

# 研究技能

能够对任何主题进行全面的调研，支持自动收集信息、分析数据，并自动生成带有引用的调研结果。

## 先决条件

**需要 Tavily API 密钥** - 请在 [https://tavily.com](https://tavily.com) 获取您的密钥。

将密钥添加到 `~/.claude/settings.json` 文件中：
```json
{
  "env": {
    "TAVILY_API_KEY": "tvly-your-api-key-here"
  }
}
```

## 快速入门

> **提示**：调研过程通常需要 30 至 120 秒。按 **Ctrl+B** 可以在后台运行调研任务。

### 使用脚本

```bash
./scripts/research.sh '<json>' [output_file]
```

**示例：**
```bash
# Basic research
./scripts/research.sh '{"input": "quantum computing trends"}'

# With pro model for comprehensive analysis
./scripts/research.sh '{"input": "AI agents comparison", "model": "pro"}'

# Save to file
./scripts/research.sh '{"input": "market analysis for EVs", "model": "pro"}' ./ev-report.md

# With custom citation format
./scripts/research.sh '{"input": "climate change impacts", "model": "mini", "citation_format": "apa"}'

# With structured output schema
./scripts/research.sh '{"input": "fintech startups 2025", "model": "pro", "output_schema": {"properties": {"summary": {"type": "string"}, "companies": {"type": "array", "items": {"type": "string"}}}, "required": ["summary"]}}'
```

### 基础调研

```bash
curl --request POST \
  --url https://api.tavily.com/research \
  --header "Authorization: Bearer $TAVILY_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
    "input": "Latest developments in quantum computing",
    "model": "mini",
    "stream": false,
    "citation_format": "numbered"
  }'
```

> **注意**：为便于管理令牌，系统禁用了数据流功能。调研任务会等待完成后再返回格式化的 JSON 数据。

### 使用自定义数据结构

```bash
curl --request POST \
  --url https://api.tavily.com/research \
  --header "Authorization: Bearer $TAVILY_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
    "input": "Electric vehicle market analysis",
    "model": "pro",
    "stream": false,
    "citation_format": "numbered",
    "output_schema": {
      "properties": {
        "market_overview": {
          "type": "string",
          "description": "2-3 sentence overview of the market"
        },
        "key_players": {
          "type": "array",
          "description": "Major companies in this market",
          "items": {
            "type": "object",
            "properties": {
              "name": {"type": "string", "description": "Company name"},
              "market_share": {"type": "string", "description": "Approximate market share"}
            },
            "required": ["name"]
          }
        }
      },
      "required": ["market_overview", "key_players"]
    }
  }'
```

## API 参考

### 端点

```
POST https://api.tavily.com/research
```

### 请求头

| 头部字段 | 值         |
|---------|------------|
| `Authorization` | `Bearer <TAVILY_API_KEY>` |
| `Content-Type` | `application/json` |

### 请求体

| 字段        | 类型        | 默认值      | 说明                |
|------------|------------|----------------|-------------------|
| `input`      | string      | 必填        | 研究主题或问题            |
| `model`      | string      | `"mini"`     | 可选模型：`mini`, `pro`, `auto`     |
| `stream`      | boolean     | `false`     | 禁用数据流功能（用于令牌管理）     |
| `output_schema` | object     | null       | 输出数据的 JSON 结构         |
| `citation_format` | string      | `"numbered"` | 引用格式：`numbered`, `mla`, `apa`, `chicago` |

### 响应格式（JSON）

当 `stream` 参数设置为 `false` 时，响应将以纯 JSON 格式返回：

```json
{
  "content": "# Research Results\n\n...",
  "sources": [{"url": "https://...", "title": "Source Title"}],
  "response_time": 45.2
}
```

## 模型选择

**经验法则**：
- 如果只是询问“X 的功能是什么？”，建议使用 `mini` 模型。
- 如果需要对比“X 与 Y 与 Z”，或寻找“最佳方法”，建议使用 `pro` 模型。
- 如果问题较为复杂，系统会自动选择合适的模型 (`auto` 模型)。

| 模型        | 使用场景            | 处理速度（秒）         |
|------------|------------------|----------------------|
| `mini`      | 单一主题的针对性调研     | 约 30 秒              |
| `pro`      | 全面的多角度分析     | 约 60–120 秒             |
| `auto`      | 系统根据复杂度自动选择模型 | 变化较大              |

## 数据结构的使用

使用数据结构可以使输出更加结构化且易于理解。每个字段都必须包含 `type` 和 `description` 两个属性。

```json
{
  "properties": {
    "summary": {
      "type": "string",
      "description": "2-3 sentence executive summary"
    },
    "key_points": {
      "type": "array",
      "description": "Main takeaways",
      "items": {"type": "string"}
    }
  },
  "required": ["summary", "key_points"]
}
```

## 示例

### 市场调研

```bash
curl --request POST \
  --url https://api.tavily.com/research \
  --header "Authorization: Bearer $TAVILY_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
    "input": "Fintech startup landscape 2025",
    "model": "pro",
    "stream": false,
    "citation_format": "numbered",
    "output_schema": {
      "properties": {
        "market_overview": {"type": "string", "description": "Executive summary of fintech market"},
        "top_startups": {
          "type": "array",
          "description": "Notable fintech startups",
          "items": {
            "type": "object",
            "properties": {
              "name": {"type": "string", "description": "Startup name"},
              "focus": {"type": "string", "description": "Primary business focus"},
              "funding": {"type": "string", "description": "Total funding raised"}
            },
            "required": ["name", "focus"]
          }
        },
        "trends": {"type": "array", "description": "Key market trends", "items": {"type": "string"}}
      },
      "required": ["market_overview", "top_startups"]
    }
  }'
```

### 技术对比

```bash
curl --request POST \
  --url https://api.tavily.com/research \
  --header "Authorization: Bearer $TAVILY_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
    "input": "LangGraph vs CrewAI for multi-agent systems",
    "model": "pro",
    "stream": false,
    "citation_format": "mla"
  }'
```

### 快速概览

```bash
curl --request POST \
  --url https://api.tavily.com/research \
  --header "Authorization: Bearer $TAVILY_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
    "input": "What is retrieval augmented generation?",
    "model": "mini",
    "stream": false
  }'
```