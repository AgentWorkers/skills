# K-Trendz光棒交易

在K-Trendz的债券曲线市场上交易K-pop艺术家的光棒代币。

**功能概述：**支持买卖K-pop粉丝代币，提供实时价格、新闻信号以及债券曲线机制。早期买家可随着艺术家人气的提升而获得价格增值。所有交易均通过Paymaster平台进行，无需使用ETH作为交易费用。

## 先决条件

请先运行`/ktrendz:setup`来配置您的凭证：

- **K-Trendz API密钥**（必需）：请联系K-Trendz团队获取

您也可以通过环境变量进行设置：
- `KTRENDZ_API_KEY` - 所有交易操作均需此密钥

## 快速入门

```bash
# Setup (one-time)
/ktrendz:setup

# List available tokens
/ktrendz:tokens

# Check token price
/ktrendz:price RIIZE

# Buy a token
/ktrendz:buy RIIZE

# Sell a token
/ktrendz:sell RIIZE
```

## 🎯 决策树

- **“有哪些代币可以交易？”** → `/ktrendz:tokens`
- **“X的价格是多少？”** → `/ktrendz:price <艺术家名称>`
- **“我应该购买X吗？”** → 先查看价格和新闻信号
- **“购买X代币”** → `/ktrendz:buy <艺术家名称>`
- **“出售X代币”** → `/ktrendz:sell <艺术家名称>`

## 主要命令

### /ktrendz:setup

收集并验证API密钥，并安全存储。

```bash
./scripts/setup.sh
```

### /ktrendz:tokens

列出所有可用的代币及其当前供应量和趋势得分。

```bash
./scripts/tokens.sh
```

**输出内容包括：**
- 代币ID
- 艺术家名称
- 总供应量
- 趋势得分

### /ktrendz:price

获取代币的当前价格和交易信号。

```bash
./scripts/price.sh RIIZE
```

**输出内容包括：**
- 当前价格（USDC）
- 买入成本 / 卖出退款
- 24小时价格变化
- 趋势得分
- 最新新闻信号

**决策因素：**

| 信号 | 含义 | 买入信号 |
|--------|---------|------------|
| `trending_score` 上升 | 平台互动增加 | ✅ 上涨趋势 |
| `price_change_24h` 正面 | 最近的上涨势头 | ✅ 趋势延续 |
| `total_supply` 低 | 持有者少 | ✅ 早期买入机会 |
| `has_recent_news` 为真 | 媒体报道 | ✅ 潜在催化剂 |

### /ktrendz:buy

购买1个光棒代币。

**参数：**
- `artist_name`：艺术家名称（例如：RIIZE、IVE、BTS）
- `slippage_percent`：最大滑点容忍度（默认：5%）

**限制：**
- 每次交易最多购买1个代币（为了保护债券曲线）
- 每个代理每天交易限额为100美元
- 同一区块内的交易被禁止（为了防止市场操纵）
- 交易费用由Paymaster自动支付

### /ktrendz:sell

出售1个光棒代币。

**参数：**
- `artist_name`：艺术家名称
- `slippage_percent`：最大滑点容忍度（默认：5%）

## 架构

### V2合约

所有机器人交易均通过Base Mainnet上的**FanzTokenBotV2**执行：

| 属性 | 值 |
|----------|-------|
| **合约** | `0x28bE702CC3A611A1EB875E277510a74fD20CDD9C` |
| **网络** | Base Mainnet（链ID：8453） |
| **标准** | ERC-1155 |
| **货币** | USDC（6位小数） |

### 代理识别

每个注册的代理都会获得一个唯一的链上标识符。当平台代表您执行交易时：

1. 平台的管理员钱包会签署并提交交易
2. 您的代理地址会被作为`agent`参数传递
3. 链上事件（买入/卖出）会记录执行者和您的代理地址
4. 这使得可以在Dune Analytics上追踪每个代理的日活跃用户（DAU）

### 交易费用支付

所有交易费用均由Coinbase Paymaster平台支付：
- **无需ETH**——平台承担所有交易费用
- 代理只需拥有足够的USDC余额即可进行交易
- 所有经过验证的代理均可享受交易费用减免

## 交易策略

这是一个**债券曲线**市场，而非套利市场：

1. **在趋势上升时买入**——得分上升 + 新闻报道 = 需求增加
2. **尽早买入**——供应量较少 = 在债券曲线上的位置更好
3. **监控市场信号**——新闻通常会先于平台上的活动出现
4. **在价格上涨期间持有**——债券曲线机制会奖励耐心持有的投资者

## 费用结构

| 操作 | 费用 | 分配方式 |
|--------|-----|--------------|
| 买入 | 3% | 2%归艺术家基金，1%归平台 |
| 卖出 | 2% | 归平台 |

**往返费用：**5%

## 交易限制

- **每日交易量：**每个代理每天最多100美元
- **交易频率：**每个代理每天最多100笔交易
- **价格限制**：如果价格在10个区块内上涨超过20%，系统会暂停交易

## 示例交互

**用户：**“我可以交易哪些代币？”

**您：**
1. 运行`./scripts/tokens.sh`
2. 回答：`目前有6个代币可供交易：RIIZE、IVE、BTS、Cortis、K-Trendz Supporters、All Day Project`

**用户：**“RIIZE的价格是多少？”

**您：**
1. 运行`./scripts/price.sh RIIZE`
2. 回答：`RIIZE的价格是1.85美元（24小时内上涨5.2%）。趋势得分为1250，有3篇最新新闻报道。买入成本为1.91美元`

**用户：**“帮我购买RIIZE代币。”

**您：**
1. 确认：`是否要以1.91美元购买1个RIIZE代币？`
2. 如果同意，运行`./scripts/buy.sh RIIZE`
3. 回答：`已成功购买1个RIIZE代币，价格为1.91美元。交易ID：0x...`

**用户：**“我应该出售我的IVE代币吗？**

**您：**
1. 运行`./scripts/price.sh IVE`
2. 检查价格趋势、新闻和趋势得分
3. 根据数据提供购买建议

## API参考

基础URL：`https://k-trendz.com/api/bot/`

| 端点 | 方法 | 描述 |
|----------|--------|-------------|
| `/tokens` | GET | 列出所有可用代币 |
| `/token-price` | POST | 获取代币价格和信号 |
| `/buy` | POST | 购买1个代币 |
| `/sell` | POST | 卖出1个代币 |

### 请求/响应示例

**GET /tokens**
```json
{
  "success": true,
  "data": {
    "contract_address": "0x28bE702CC3A611A1EB875E277510a74fD20CDD9C",
    "token_count": 6,
    "tokens": [
      {
        "token_id": "7963681970480434413",
        "artist_name": "RIIZE",
        "total_supply": 42,
        "trending_score": 1250,
        "follower_count": 156
      }
    ]
  }
}
```

**POST /token-price**
```json
// Request
{ "artist_name": "RIIZE" }

// Response
{
  "success": true,
  "data": {
    "token_id": "7963681970480434413",
    "artist_name": "RIIZE",
    "current_price_usdc": 1.85,
    "buy_cost_usdc": 1.91,
    "sell_refund_usdc": 1.78,
    "price_change_24h": "5.2",
    "total_supply": 42,
    "trending_score": 1250,
    "external_signals": {
      "article_count_24h": 3,
      "has_recent_news": true,
      "headlines": [...]
    }
  }
}
```

**POST /buy**
```json
// Request
{ 
  "artist_name": "RIIZE", 
  "max_slippage_percent": 5
}

// Response
{
  "success": true,
  "data": {
    "transaction_id": "uuid",
    "tx_hash": "0x...",
    "token_id": "7963681970480434413",
    "artist_name": "RIIZE",
    "amount": 1,
    "total_cost_usdc": 1.91,
    "remaining_daily_limit": 98.09,
    "gas_sponsored": true
  }
}
```

**POST /sell**
```json
// Request
{ 
  "artist_name": "RIIZE", 
  "max_slippage_percent": 5
}

// Response
{
  "success": true,
  "data": {
    "transaction_id": "uuid",
    "tx_hash": "0x...",
    "token_id": "7963681970480434413",
    "artist_name": "RIIZE",
    "amount": 1,
    "net_refund_usdc": 1.78,
    "fee_usdc": 0.04,
    "gas_sponsored": true
  }
}
```

## 文件

- `SKILL.md` - 本文档
- `package.json` - 包元数据
- `scripts/setup.sh` - API密钥配置
- `scripts/tokens.sh` - 列出可用代币
- `scripts/price.sh` - 获取代币价格
- `scripts/buy.sh` - 买入代币
- `scripts/sell.sh` - 卖出代币