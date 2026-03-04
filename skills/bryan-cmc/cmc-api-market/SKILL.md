---
name: cmc-api-market
description: >
  **CoinMarketCap市场全范围API参考**  
  本文档涵盖了CoinMarketCap（CMC）提供的市场全范围API接口，包括全球市场指标、恐惧/贪婪指数、热门话题以及图表数据。  
  **使用场景：**  
  - 当用户提及“市场API”时  
  - 当用户询问恐惧/贪婪指数相关内容时  
  - 当用户需要全球市场指标或BTC市场份额数据时  
  - 当用户需要K线图或市场情绪分析数据时  
  **API概述：**  
  这些API接口提供了对整个加密货币市场的全面访问，帮助开发者或分析师获取实时的市场数据和分析工具。  
  **常用接口示例：**  
  - **全球市场指标API**：用于获取各类加密货币的全球市场数据（价格、成交量、市值等）  
  - **恐惧/贪婪指数API**：用于分析市场参与者的情绪（恐惧/贪婪程度）  
  - **趋势话题API**：用于获取当前加密货币市场的热门讨论话题  
  - **图表API**：用于生成各种加密货币的K线图  
  **示例用法：**  
  ```bash
  curl https://api.cmc.com/v1/market/globalmetrics?symbol=BTC
  ```  
  （用于获取比特币的全球市场指标）  
  **触发词：**  
  - `market API`  
  - `fear_greed API`  
  - `global_metrics API`  
  - `CMC charts API`  
  - `/cmc-api-market`  
  **注意：**  
  - 请确保在使用这些API时遵循CMC的官方文档和使用规范。  
  - 部分API可能需要API密钥才能访问高级功能。  
  **更多信息：**  
  请访问CoinMarketCap的官方文档以获取更多关于这些API的详细信息：[https://docs.cmc.com/](https://docs.cmc.com/)
homepage: https://github.com/coinmarketcap/skills-for-ai-agents-by-CoinMarketCap
source: https://github.com/coinmarketcap/skills-for-ai-agents-by-CoinMarketCap
user-invocable: true
allowed-tools:
  - Bash
  - Read
---
# CoinMarketCap市场API技能

本技能涵盖了包括全球指标、情绪指标、市场指数、社区活动、新闻内容、图表数据以及实用功能端点在内的全方位加密货币市场数据。

## 认证

所有请求都需要`X-CMC_PRO_API_KEY`请求头。

```bash
curl -X GET "https://pro-api.coinmarketcap.com/v1/global-metrics/quotes/latest" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

您可以在以下链接获取API密钥：https://pro.coinmarketcap.com/login

## 基础URL

```
https://pro-api.coinmarketcap.com
```

## 常见用例

请参阅[use-cases.md](references/use-cases.md)，以获取关于使用哪个端点的指导：

1. 获取当前市场情绪（恐惧与贪婪指数）
2. 获取加密货币总市值
3. 获取比特币的市场占比
4. 跟踪市值历史变化
5. 跟踪恐惧与贪婪指数的历史变化
6. 获取CMC100指数表现
7. 比较CMC100与CMC20指数
8. 获取用于图表的OHLCV蜡烛图数据
9. 获取简单的价格时间序列数据
10. 获取社区中热门的代币
11. 获取热门的讨论话题
12. 获取最新的加密货币新闻
13. 转换货币金额
14. 检查API的使用情况和限制
15. 获取法定货币的ID

## API概述

### 全球指标

| 端点 | 描述 | 参考文档 |
|----------|-------------|-----------|
| GET /v1/global-metrics/quotes/historical | 历史全球市场指标 | [global-metrics.md](references/global-metrics.md) |
| GET /v1/global-metrics/quotes/latest | 最新总市值、比特币市场占比 | [global-metrics.md](references/global-metrics.md) |

### 恐惧与贪婪指数

| 端点 | 描述 | 参考文档 |
|----------|-------------|-----------|
| GET /v3/fear-and-greed/historical | 历史上的恐惧/贪婪指数值 | [fear-greed.md](references/fear-greed.md) |
| GET /v3/fear-and-greed/latest | 当前市场情绪得分 | [fear-greed.md](references/fear-greed.md) |

### 市场指数

| 端点 | 描述 | 参考文档 |
|----------|-------------|-----------|
| GET /v3/index/cmc100-historical | CMC100指数历史数据 | [indices.md](references/indices.md) |
| GET /v3/index/cmc100-latest | CMC100当前指数值 | [indices.md](references/indices.md) |
| GET /v3/index/cmc20-historical | CMC20指数历史数据 | [indices.md](references/indices.md) |
| GET /v3/index/cmc20-latest | CMC20当前指数值 | [indices.md](references/indices.md) |

### 社区

| 端点 | 描述 | 参考文档 |
|----------|-------------|-----------|
| GET /v1/community/trending/token | 根据社区活跃度排序的热门代币 | [community.md](references/community.md) |
| GET /v1/community/trending/topic | 热门讨论话题 | [community.md](references/community.md) |

### 内容

| 端点 | 描述 | 参考文档 |
|----------|-------------|-----------|
| GET /v1/content/latest | 最新新闻和Alexandria文章 | [content.md](references/content.md) |
| GET /v1/content/posts/comments | 特定帖子的评论 | [content.md](references/content.md) |
| GET /v1/content/posts/latest | 最新社区帖子 | [content.md](references/content.md) |
| GET /v1/content/posts/top | 最受欢迎的社区帖子 | [content.md](references/content.md) |

### K线图

| 端点 | 描述 | 参考文档 |
|----------|-------------|-----------|
| GET /v1/k-line/candles | OHLCV蜡烛图数据 | [kline.md](references/kline.md) |
| GET /v1/k-line/points | 价格/市值的时间序列数据 | [kline.md](references/kline.md) |

### 工具

| 端点 | 描述 | 参考文档 |
|----------|-------------|-----------|
| GET /v1/fiat/map | 将法定货币映射到CMC ID | [tools.md](references/tools.md) |
| GET /v1/key/info | API密钥使用情况和计划详情 | [tools.md](references/tools.md) |
| GET /v2/tools/price-conversion | 货币转换 | [tools.md](references/tools.md) |

## 常见工作流程

### 获取市场情绪概览

1. 获取恐惧/贪婪指数：`/v3/fear-and-greed/latest`
2. 获取全球指标：`/v1/global-metrics/quotes/latest`
3. 结合这些数据进行分析以了解市场情绪

### 跟踪市场指数表现

1. 获取当前CMC100指数值：`/v3/index/cmc100-latest`
2. 获取历史数据：`/v3/index/cmc100-historical`
3. 随时间跟踪指数表现

### 监控社区活动

1. 查看热门代币：`/v1/community/trending/token`
2. 查看热门讨论话题：`/v1/community/trending/topic`
3. 阅读最新帖子：`/v1/content/posts/top`

### 构建价格图表

1. 获取OHLCV蜡烛图数据：`/v1/k-line/candles`
2. 使用间隔参数设置时间范围（1小时、4小时、1天）
3. 使用返回的数据绘制蜡烛图

### 货币转换

1. 获取法定货币ID：`/v1/fiat/map`
2. 进行货币转换：`/v2/tools/price-conversion`

## 错误处理

| 状态码 | 含义 | 处理方式 |
|-------------|---------|--------|
| 400 | 请求错误 | 检查参数值和格式 |
| 401 | 未授权 | 确认API密钥有效 |
| 403 | 禁止访问 | 该端点不在您的使用计划范围内 |
| 429 | 请求频率限制 | 等待一段时间后重试 |
| 500 | 服务器错误 | 延迟后重试 |

### 错误响应格式

```json
{
  "status": {
    "error_code": 400,
    "error_message": "Invalid value for 'id'"
  }
}
```

### 请求频率限制头信息

请查看以下响应头以监控API使用情况：

1. `X-CMC_PRO_API_KEY_CREDITS_USED` - 已使用的信用额度
2. `X-CMC_PRO_API_KEY_CREDITS_REMAINING` - 剩余信用额度
3. `X-CMC_PRO_API_KEY_RATE_LIMIT` - 每分钟的请求限制

## 响应格式

所有端点返回的JSON数据均遵循以下结构：

```json
{
  "status": {
    "timestamp": "2024-01-15T10:30:00.000Z",
    "error_code": 0,
    "error_message": null,
    "credit_count": 1
  },
  "data": { }
}
```

## 提示

1. 在大量使用API之前，使用`/v1/key/info`端点查看您的使用计划限制。
2. 全球指标数据每隔几分钟更新一次，可以适当缓存。
3. 恐惧与贪婪指数每天更新一次，无需频繁请求。
4. K线图数据支持多种时间间隔，适用于不同的图表时间段。
5. 社区热门数据会在一天内定期更新。