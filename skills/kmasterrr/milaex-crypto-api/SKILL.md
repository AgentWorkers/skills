---
name: milaex
description: 统一的加密货币市场数据API及脚本，支持交易所、市场、股票代码（tickers）、OHLCV（开高收低成交量）数据以及订单簿（orderbooks）的查询。
homepage: https://api.milaex.com/api-docs/index.html
metadata: {"clawdbot":{"emoji":"📈","requires":{"bins":["python3"],"env":["MILAEX_API_KEY"]}}}
---

# Milaex 技能（加密货币市场数据）

使用此技能可进行与加密货币数据相关的搜索，该技能能够通过 **Milaex 统一 REST API** 获取多个交易所的实时或标准化市场数据。

## 该技能为代理程序提供的功能：
- 可在单一位置查询交易所、市场/交易对、股票代码、开盘价/最高价/最低价/收盘价/成交量（OHLCV）数据以及订单簿信息。
- 所有交易所的请求和响应格式均保持一致。
- 输出的 JSON 数据格式统一，便于导入其他工具。
- 提供友好的错误信息（包含 HTTP 状态码和 Milaex 错误详细信息），并可选择性地打印速率限制相关头部信息。

## 服务详情（来自 milaex.com）：
- Milaex 是一个提供统一加密货币市场数据的 SaaS 服务，通过 REST API 支持多个交易所的数据访问。
- 支持的数据类型包括市场信息、股票代码、OHLCV 数据以及订单簿数据。
- 需要通过控制面板中的 API 密钥来访问这些数据。
- Milaex 仅提供数据服务（不涉及资金托管或交易执行功能）。
- 文档链接：https://api.milaex.com/api-docs/index.html

## 设置（获取 API 密钥）
1. 访问 https://milaex.com 并注册或登录。
2. 在 Milaex 控制面板中为市场数据 API 生成一个 API 密钥。

## 配置
**必需的环境变量：**
- `MILAEX_API_KEY`（以 `x-api-key` 的形式传递）

### 推荐做法（适用于 Clawdbot）：将密钥存储在 openclaw 配置文件中
这样 Clawdbot 在运行该技能时可以自动读取该环境变量。
编辑 `~/.clawdbot/openclaw.json` 文件：
```json
{
  "skills": {
    "entries": {
      "milaex": {
        "enabled": true,
        "env": {
          "MILAEX_API_KEY": "..."
        }
      }
    }
  }
}
```

### 手动使用（通过 shell 设置环境变量）
```bash
export MILAEX_API_KEY="..."
```

## 端点信息（来自公开版 OpenAPI v1）
以下脚本对应于 Milaex 的各个 API 端点：
- `GET /api/v1/exchange`  
- `GET /api/v1/exchange/markets?exchange=`  
- `GET /api/v1/exchange/ticker?exchange=&base_name=&quote_name=`  
- `GET /api/v1/exchange/tickers?exchange=&symbols=`  
- `GET /api/v1/exchange/ohlcv?exchange=&base_name=&quote_name=`  
- `GET /api/v1/exchange/orderbook?exchange=&base_name=&quote_name=`  
- `GET /api/v1/exchange/orderbook/complete?exchange=&base_name=&quote_name=`  

## 常见搜索问题与对应的 API 端点映射：
- 支持哪些交易所？ -> `GET /api/v1/exchange`  
- 交易所 X 支持哪些市场？ -> `GET /api/v1/exchange/markets?exchange=`  
- 交易所 X 上 BTC/USDT 的当前价格？ -> `GET /api/v1/exchange/ticker?exchange=&base_name=&quote_name=`  
- 交易所 X 上的多个股票代码？ -> `GET /api/v1/exchange/tickers?exchange=&symbols=`  
- 某交易对的蜡烛图数据？ -> `GET /api/v1/exchange/ohlcv?exchange=&base_name=&quote_name=`  
- 订单簿快照？ -> `GET /api/v1/exchange/orderbook?exchange=&base_name=&quote_name=`  

## 常用命令
所有命令都会将结果输出到 **stdout**；如果存在速率限制信息，则会输出到 **stderr**。

### 列出所有交易所
```bash
python3 skills/milaex/scripts/list_exchanges.py
# or
bash skills/milaex/bin/list_exchanges.sh
```

### 列出某个交易所的市场信息
```bash
python3 skills/milaex/scripts/list_markets.py --exchange binance
```

### 获取单个股票代码的信息
```bash
python3 skills/milaex/scripts/get_ticker.py --exchange binance --symbol BTC/USDT
```

### 获取股票代码信息（可选：按符号过滤）
```bash
python3 skills/milaex/scripts/get_tickers.py --exchange binance
python3 skills/milaex/scripts/get_tickers.py --exchange binance --symbols "BTC/USDT,ETH/USDT"
```

### 获取 OHLCV 数据
注意：Milaex v1 OpenAPI 使用 `exchange/base_name/quote_name` 的格式来表示 OHLCV 数据。虽然脚本支持 `--timeframe` 参数以兼容后续版本，但实际上不会发送该参数（以避免请求被拒绝）。
```bash
python3 skills/milaex/scripts/get_ohlcv.py --exchange binance --symbol BTC/USDT --limit 200
```

### 获取订单簿信息
```bash
python3 skills/milaex/scripts/get_orderbook.py --exchange binance --symbol BTC/USDT --limit 50
python3 skills/milaex/scripts/get_orderbook.py --exchange binance --symbol BTC/USDT --complete
```

## 常见使用场景：
- **对于交易员**：
  - 监控不同交易所的最佳买卖价差。
  - 构建跨交易所的套利分析工具。
  - 通过 OHLCV 数据检测市场波动情况。
  - 发送价格变动警报（例如：“价格在 Y 分钟内变动了 X%”）。

- **对于数据工程师/分析师**：
  - 从 Milaex 获取标准化的数据用于构建仪表盘。
  - 构建研究数据集（包括蜡烛图数据和订单簿快照）。
  - 运行定期的数据提取、转换和加载（ETL）任务，无需维护针对每个交易所的适配器。

- **对于产品和支持团队**：
  - 回答关于交易所、交易对及数据可用性的问题。
  - 使用真实数据验证价格和延迟方面的假设。

## 注意事项：
- 请确保请求频率符合 Milaex 的速率限制规定（如果您的订阅计划启用了速率限制功能，Milaex 会自动返回相应的头部信息）。
- 这些脚本需要 Python 3 和 `requests` 库来运行。
- 如有需要，请安装相关依赖库：
```bash
python3 -m pip install --user requests
```

## 测试（预期结果：未经授权的访问）
这是一个简单的测试，用于验证未经授权的访问行为。使用虚拟密钥进行测试时，部分系统会返回 **401** 错误，部分系统会返回带有“Api Key not found”信息的 **404** 错误。
```bash
MILAEX_API_KEY=dummy python3 skills/milaex/scripts/test_unauthorized.py
```