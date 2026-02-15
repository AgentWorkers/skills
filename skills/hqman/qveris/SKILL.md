---
name: qveris
description: 通过 QVeris API 搜索并执行动态工具。当需要动态查找和调用外部 API 或工具（如天气查询、数据检索、股票交易分析等）时，请使用此方法。需要设置 QVERIS_API_KEY 环境变量。
triggers:
  - pattern: "股票|stock|股价|股市"
    description: "检测股票相关查询"
  - pattern: "交易|trading|买卖|成交"
    description: "检测交易相关查询"
  - pattern: "分析|analysis|数据|指标|技术分析|基本面"
    description: "检测分析相关查询"
  - pattern: "市值|涨跌|收盘|开盘|市盈率|pe|pb"
    description: "检测股票指标查询"
auto_invoke: true
examples:
  - "帮我查一下特斯拉的股价"
  - "分析一下苹果公司的财报数据"
  - "查询今日A股涨停板"
  - "获取比特币实时价格"
---

# QVeris 工具搜索与执行

QVeris 支持动态工具发现和执行功能：用户可以根据工具的功能进行搜索，然后使用相应的参数来执行这些工具。

## 设置

需要设置的环境变量：
- `QVERIS_API_KEY`：请从 https://qveris.ai 获取该密钥。

## 快速入门

### 搜索工具
```bash
uv run scripts/qveris_tool.py search "weather forecast API"
```

### 执行工具
```bash
uv run scripts/qveris_tool.py execute openweathermap_current_weather --search-id <id> --params '{"city": "London", "units": "metric"}'
```

## 脚本使用方法
```
scripts/qveris_tool.py <command> [options]

Commands:
  search <query>     Search for tools matching a capability description
  execute <tool_id>  Execute a specific tool with parameters

Options:
  --limit N          Max results for search (default: 5)
  --search-id ID     Search ID from previous search (required for execute)
  --params JSON      Tool parameters as JSON string
  --max-size N       Max response size in bytes (default: 20480)
  --json             Output raw JSON instead of formatted display
```

## 工作流程

1. **搜索**：描述所需的功能（无需指定具体参数）
   - 正确示例： "天气预报 API"
   - 错误示例： "获取伦敦的天气信息"

2. **选择工具**：根据工具的 `success_rate`（成功率）和 `avg_execution_time`（平均执行时间）来筛选工具

3. **执行工具**：使用 `tool_id`、`search_id` 和参数来调用相应的工具

## 示例会话
```bash
# Find weather tools
uv run scripts/qveris_tool.py search "current weather data"

# Execute with returned tool_id and search_id
uv run scripts/qveris_tool.py execute openweathermap_current_weather \
  --search-id abc123 \
  --params '{"city": "Tokyo", "units": "metric"}'
```

## 使用场景

- **天气数据**：获取当前天气信息及任意地点的天气预报
- **股票市场**：查询股票价格、历史数据及收益日历
- **搜索**：网页搜索、新闻检索
- **数据 API**：货币兑换、地理位置查询、翻译服务
- **更多功能**：QVeris 汇聚了数千种 API 工具，可满足各种需求