---
description: 使用真实的CoinGecko数据回测加密交易策略（如RSI、DCA、MACD、网格交易等）。
---

# 加密货币模拟器

使用真实市场数据回测和模拟加密货币交易策略。

## 快速入门

```bash
cd {skill_dir}
npm install && npm run build

# Backtest a strategy
node dist/cli.js backtest --coin bitcoin --strategy rsi_swing --days 90

# Compare all strategies
node dist/cli.js compare --coin ethereum --days 180

# Optimize parameters
node dist/cli.js optimize --coin bitcoin --strategy rsi_swing

# Start REST API
node dist/cli.js serve --port 3002
```

## 交易策略

| 策略 | 适用市场 | 逻辑 |
|----------|----------|-------|
| RSI摆动交易 | 波动较大的市场 | 当RSI指标低于30时买入，高于70时卖出 |
| 定投策略 (DCA) | 长期投资 | 按固定间隔进行买入 |
| 移动平均线交叉策略 | 趋势市场 | 在移动平均线交叉时买入/卖出 |
| 网格交易策略 | 波动市场 | 在预设的价格区间内下达订单 |
| 持有策略 (HODL) | 牛市 | 买入后长期持有 |
| 布林带交易策略 | 均值回归 | 在布林带突破时进行交易 |
| MACD交易策略 | 动量交易 | 当MACD信号线交叉时进行交易 |
| 均值回归策略 | 波动市场 | 在价格低于平均值时买入，在价格高于平均值时卖出 |

**支持的加密货币**: BTC、ETH、SOL、DOGE、ADA、DOT、AVAX、LINK、MATIC、XRP

## API接口

| 方法 | 路径 | 说明 |
|--------|------|-------------|
| `GET` | `/api/prices/:coinId` | 获取当前及历史价格 |
| `POST` | `/api/backtest` | 运行回测 |
| `GET` | `/api/compare/:coinId` | 比较所有策略的表现 |
| `POST` | `/api/optimize` | 优化交易策略的参数 |

## 注意事项

- **CoinGecko的请求限制**: 免费账户的请求频率约为每分钟10-30次。使用SQLite缓存可避免不必要的重复请求 |
- **数据不足**: 短时间范围内的数据可能不足以生成有效的交易信号（例如，50日均线需要至少50天的数据）
- **滑点**: 回测结果基于理想交易环境，实际交易中可能存在滑点现象，导致结果有所不同 |

## ⚠️ 免责声明

本工具仅用于教育或信息交流目的，不构成任何财务建议。过去的表现并不代表未来的结果。

## 配置参数

| 参数 | 默认值 | 说明 |
|----------|---------|-------------|
| `PORT` | 3002 | API服务器端口 |
| `CACHE_DIR` | `./data` | SQLite缓存目录 |

## 系统要求

- Node.js 18及以上版本 |
- 需要互联网连接以访问CoinGecko API |
- 免费账户无需API密钥 |