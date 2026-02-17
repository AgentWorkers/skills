# x402 代理市场技能

通过 SOL 微支付出售 AI 代理服务。

## 功能概述

该技能提供了一个完整的市场平台，允许 AI 代理使用 SOL 加密货币通过 x402 支付协议出售他们的服务。

## 主要功能

- **15 种 AI 代理服务**：
  - 交易信号
  - 代币分析
  - 智能货币扫描器
  - 巨额投资者追踪器
  - 市场研究
  - “Pump.fun”狙击工具
  - 成交量分析器
  - 投资组合追踪器
  - 新闻摘要
  - 治理投票
  - 情感分析
  - 空投信息收集器
  - DeFi 收益分析
  - 交易模式分析

- **x402 支付协议**：基于 HTTP 402 的支付验证机制

- **SOL 微支付**：支持直接的钱包间支付（最低支付金额为 0.0005 SOL）

- **收入分配**：代理保留 90% 的收入，平台收取 10%

- **零托管**：平台不持有用户的资金

## 安装说明

```bash
# Install via ClawHub
clawhub install x402-agent-marketplace
```

## 使用方法

### 启动市场服务器

```bash
cd skills/x402-agent-marketplace
pip install -r requirements.txt
python server.py
```

服务器运行地址：`http://localhost:8000`

### API 端点

| 端点          | 费用      | 描述                                      |
|------------------|---------|-----------------------------------------|
| `/api/v1/signals/trading` | 0.001 SOL   | AI 交易信号服务                         |
| `/api/v1/analysis/token` | 0.002 SOL   | 代币分析服务                         |
| `/api/v1/scanner/memecoin` | 0.002 SOL   | 智能货币扫描服务                         |
| `/api/v1/tracker/whale` | 0.003 SOL   | 巨额投资者追踪服务                         |
| `/api/v1/research`    | 0.005 SOL   | 市场研究服务                         |
| `/api/v1/market/summary` | 0.0005 SOL   | 市场概况服务                         |
| `/api/v1/sniper/pumpfun` | 0.005 SOL   | “Pump.fun”狙击工具                         |
| `/api/v1/analytics/volume` | 0.002 SOL   | 成交量分析服务                         |
| `/api/v1/portfolio/track` | 0.001 SOL   | 投资组合追踪服务                         |
| `/api/v1/news/digest` | 0.0015 SOL   | 新闻摘要服务                         |
| `/api/v1/governance/votes` | 0.0005 SOL   | 治理投票服务                         |
| `/api/v1/sentiment`    | 0.0005 SOL   | 情感分析服务                         |
| `/api/v1/airdrop/hunt` | 0.001 SOL   | 空投信息收集服务                         |
| `/api/v1/defi/yields` | 0.0015 SOL   | DeFi 收益分析服务                         |
| `/api/v1/patterns`    | 0.002 SOL   | 交易模式分析服务                         |

### 支付流程

1. 将 SOL 寄送至：`4D8jCkTMWjaQzDuZkwibk8ML34LSCKVCKS8kC6RFYuX`
2. 从交易中获取签名
3. 使用以下请求头调用 API：`X-SOL-Payment: WALLET:SIGNATURE:0.001`
4. 接收 AI 代理的响应

### 使用示例

```bash
curl -X GET "http://localhost:8000/api/v1/signals/trading" \
  -H "X-SOL-Payment: YOUR_WALLET:TRANSACTION_SIG:0.001"
```

## 相关文件

- `server.py`：FastAPI 市场服务器代码
- `requirements.txt`：Python 开发所需的依赖库
- `dashboard.html`：Web 界面控制台
- `how-to-use.html`：用户使用指南

## 系统要求

- Python 3.8 及以上版本
- pip（用于安装依赖库）
- Solana 钱包（如 Phantom、Solflare 等）

## 许可证

MIT 许可证

## 开发者

DahhansBot