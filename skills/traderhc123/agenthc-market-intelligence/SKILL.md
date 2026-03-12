---
name: agenthc-market-intelligence
description: AI代理的市场数据API：涵盖股票、固定收益产品、加密货币以及宏观经济数据。同时支持比特币Lightning网络的微支付功能。
homepage: https://api.traderhc.com/docs
metadata:
  clawdbot:
    emoji: "📊"
    requires:
      env: ["AGENTHC_API_KEY"]
      bins: ["curl", "jq", "python3"]
    primaryEnv: "AGENTHC_API_KEY"
license: UNLICENSED
---
# 股票市场情报

这是一个专为AI代理和开发者设计的市场数据API，涵盖股票、固定收益、加密货币以及宏观经济数据。支持通过Webhook和Discord发送实时警报，并支持比特币Lightning网络进行微支付。由@traderhc开发。

## 设置

### 对于AI代理

```bash
export AGENTHC_API_KEY=$(curl -s -X POST "https://api.traderhc.com/api/v1/register" \
  -H "Content-Type: application/json" \
  -d '{"name": "MyAgent"}' | jq -r '.api_key')
```

完全免费，无需进行客户尽职调查（KYC），也无需信用卡。可以查询任何免费提供的API端点：

```bash
curl -s "https://api.traderhc.com/api/v1/data/overview" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### 交互式设置

```bash
bash scripts/setup.sh
```

### 非交互式设置（持续集成/脚本）

```bash
export AGENTHC_API_KEY=$(bash scripts/setup.sh --auto)
```

## 提供的服务

| 级别 | 支持的数据范围 | 费用 |
|------|------------------|------|
| **免费** | 市场概览、教育性内容 | $0 |
| **高级版** | 股票、固定收益、宏观经济、加密货币、波动率数据 | 约$50/月 |
| **机构版** | 全平台访问权限及高级分析功能 | 约$500/月 |

请访问[api.traderhc.com/docs](https://api.traderhc.com/docs)查看完整的API端点目录。

## 代理优化格式

使用`format=agent`可获取可操作的实时市场信号：

```bash
curl -s "https://api.traderhc.com/api/v1/data/overview?format=agent" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.signals'
```

## 简洁格式

使用`format=compact`可减少数据传输量：

```bash
curl -s "https://api.traderhc.com/api/v1/data/overview?format=compact" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.'
```

## 批量查询（高级版及以上）

可以在一个请求中查询多个API端点：

```bash
curl -s -X POST "https://api.traderhc.com/api/v1/data/batch" \
  -H "X-API-Key: $AGENTHC_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"endpoints": ["overview", "fixed_income", "macro"]}' | jq '.'
```

## 警报功能

可以通过Webhook或Discord订阅实时市场警报：

```bash
# List available alert types
curl -s "https://api.traderhc.com/api/v1/alerts" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.alerts'

# Subscribe via webhook
curl -s -X POST "https://api.traderhc.com/api/v1/alerts/subscribe" \
  -H "X-API-Key: $AGENTHC_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"type": "market_events", "callback_url": "https://your-agent.com/webhook"}' | jq '.'
```

## Lightning支付（L402）

如需无需注册即可进行支付，请按照以下步骤操作：

1. 请求一个高级版API端点（无需身份验证）
2. 收到包含Lightning支付信息的402响应
3. 通过任意Lightning钱包支付该费用
4. 重新发送请求时添加`Authorization: L402 <macaroon>:<preimage>`参数

## 价格政策

| 级别 | 数据传输频率 | 费用 |
|------|------------------|------|
| 免费 | 每分钟10次，每天100次 | $0 |
| 高级版 | 每分钟60次，每天5,000次 | 约$50/月（50,000 Satoshis） |
| 机构版 | 每分钟120次，每天50,000次 | 约$500/月（500,000 Satoshis） |

所有费用均通过比特币Lightning网络支付，支持即时结算，无需进行客户尽职调查（KYC）。

## 免责声明

所有数据和分析内容仅用于教育和信息提供目的，不构成任何财务建议。我们并非注册投资顾问。请始终自行进行充分研究。