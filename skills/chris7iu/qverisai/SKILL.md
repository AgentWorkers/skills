---
name: qverisai
description: 通过 QVeris API 搜索并执行动态工具。当需要动态查找和调用外部 API/工具时，请使用此方法——涵盖天气、搜索、股票、金融、经济、地理定位、AIGC、新闻、社交媒体、健康数据等众多领域。需要设置 `QVERIS_API_KEY` 环境变量。
env:
  - QVERIS_API_KEY
requirements:
  env_vars:
    - QVERIS_API_KEY
credentials:
  primary: QVERIS_API_KEY
  scope: read-only
  endpoint: https://qveris.ai/api/v1
auto_invoke: true
source: https://qveris.ai
examples:
  - "Show me current weather in Tokyo"
  - "Search for latest tech news"
  - "Check Tesla stock price"
  - "Analyze Apple's financial data"
  - "What is the US GDP growth rate"
  - "Generate an image of a sunset over mountains"
  - "Get trending topics on Twitter"
  - "Find clinical trials for diabetes treatment"
---

# QVeris 工具搜索与执行

QVeris 提供动态的工具发现和执行功能——可以根据工具的功能进行搜索，然后使用相应的参数来执行这些工具。

## 设置

需要设置的环境变量：
- `QVERIS_API_KEY`：请从 https://qveris.ai 获取该密钥。

无需额外的依赖项——仅使用 Node.js 内置的 `fetch` 函数。

## 安全性

- **凭证**：仅访问 `QVERIS_API_KEY`，不会读取其他环境变量或敏感信息。
- **网络**：API 密钥仅通过 HTTPS 发送到 `https://qveris.ai/api/v1`，不会访问其他端点。
- **存储**：该密钥不会被记录、缓存或写入磁盘。
- **建议**：使用具有时效限制且可撤销的 API 密钥，并在 https://qveris.ai 上监控其使用情况。

## 快速入门

### 搜索工具
```bash
node scripts/qveris_tool.mjs search "weather forecast API"
```

### 执行工具
```bash
node scripts/qveris_tool.mjs execute openweathermap_current_weather --search-id <id> --params '{"city": "London", "units": "metric"}'
```

## 脚本使用方法
```
node scripts/qveris_tool.mjs <command> [options]

Commands:
  search <query>     Search for tools matching a capability description
  execute <tool_id>  Execute a specific tool with parameters

Options:
  --limit N          Max results for search (default: 10)
  --search-id ID     Search ID from previous search (required for execute)
  --params JSON      Tool parameters as JSON string
  --max-size N       Max response size in bytes (default: 20480)
  --timeout N        Request timeout in seconds (default: 30 for search, 60 for execute)
  --json             Output raw JSON instead of formatted display
```

## 工作流程

1. **搜索**：描述所需的功能（无需指定具体参数）
   - 正确示例：`weather forecast API`
   - 错误示例：`get weather for London`

2. **选择工具**：根据 `success_rate`（成功率）和 `avg_execution_time`（平均执行时间）来筛选工具。

3. **执行工具**：使用 `tool_id`、`search_id` 和 `parameters` 来调用相应的工具。

## 示例会话
```bash
# Find weather tools
node scripts/qveris_tool.mjs search "current weather data"

# Execute with returned tool_id and search_id
node scripts/qveris_tool.mjs execute openweathermap_current_weather \
  --search-id abc123 \
  --params '{"city": "Tokyo", "units": "metric"}'
```

## 使用场景

- **天气**：获取当前天气信息及任意地点的天气预报
- **搜索**：网络搜索、信息检索
- **股票与金融**：查询股票价格、历史数据、财报信息
- **经济**：GDP、通货膨胀率、经济指标
- **地理定位**：IP 地址查询、地理编码、反向地理编码
- **人工智能与生成内容（AIGC）**：图像生成、文本转语音、AI 内容创作
- **新闻**：新闻标题、文章搜索、热门话题
- **社交媒体**：热门话题、帖子分析、用户互动数据
- **健康数据**：临床试验、药品信息、健康统计数据
- **更多**：QVeris 支持数千种 API 工具