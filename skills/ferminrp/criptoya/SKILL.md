---
name: crypto-prices-criptoya
description: 使用 CriptoYa 功能，可以按交易所查询加密货币的报价，并以汇总的形式查看这些报价。当用户请求“BTC 对 ARS 的价格”、“USDT 的报价”、“ETH 对 USD 的价格”、“最佳交易所报价”、“比较不同交易所的价格”、“Belo/ripio/lemon/binance/bybit 上的价格”，或者询问提现手续费和网络费用时，可以使用此功能。
---
# CryptoPrices CriptoYa

查询CriptoYa的加密货币价格，包括按交易所划分的价格、综合价格以及提现手续费。

## API概述

- **基础URL**: `https://criptoya.com`
- **认证**: 无需认证
- **响应格式**: 验证通过的响应为JSON格式
- **操作说明**: 对于无效的货币对或参数，API可能会返回文本 `"Invalid pair"` 并返回HTTP状态码 `200`
- **时间戳**: 以Unix纪元表示的时间字段

## API端点

- `GET /api/{exchange}/{coin}/{fiat}/{volumen}`
- `GET /api/{coin}/{fiat}/{volumen}`
- `GET /api/fees`

示例：

```bash
curl -s "https://criptoya.com/api/BTC/ARS/0.1" | jq '.'
curl -s "https://criptoya.com/api/belo/BTC/ARS/0.1" | jq '.'
curl -s "https://criptoya.com/api/fees" | jq '.'
```

## 支持的参数

### `coin` (货币代码)

`BTC, ETH, USDT, USDC, DAI, UXD, USDP, WLD, BNB, SOL, XRP, ADA, AVAX, DOGE, TRX, LINK, DOT, MATIC, SHIB, LTC, BCH, EOS, XLM, FTM, AAVE, UNI, ALGO, BAT, PAXG, CAKE, AXS, SLP, MANA, SAND, CHZ`

### `fiat` (法定货币代码)

`ARS, BRL, CLP, COP, MXN, PEN, VES, BOB, UYU, DOP, PYG, USD, EUR`

### `exchange` (交易所名称)

`cryptomkt, letsbit, belo, bitsoalpha, bybit, ripio, lemoncash, fiwind, tiendacrypto, eluter, universalcoins, buenbit, binance, huobip2p, bitso, eldoradop2p, lemoncashp2p, kucoinp2p, decrypto, mexcp2p, pluscrypto, cocoscrypto, bitgetp2p, cryptomktpro, satoshitango, coinexp2p, paydecep2p, binancep2p, bingxp2p, ripioexchange, astropay, dolarapp, vibrant, wallbit, vitawallet, weexp2p, trubit, okexp2p, bybitp2p, saldo, p2pme, airtm`

### `volumen` (交易量)

使用小数点表示的数值：`0.1`, `1`, `250.5`

## 关键字段

- **按交易所划分的价格**:
  - `ask` (卖价), `totalAsk` (总卖价), `bid` (买价), `totalBid` (总买价), `time` (时间)
- **综合价格**:
  - 按交易所划分的对象，包含相同的字段 (`ask`, `totalAsk`, `bid`, `totalBid`, `time`)
- **手续费**:
  - 层嵌结构：`exchange -> coin -> red -> fee` (交易所 -> 货币 -> 网络 -> 手续费)

## 工作流程

1. 确定请求类型：
   - 查询综合价格
   - 查询按交易所划分的价格
   - 查询提现手续费
2. 验证必需的输入参数：
   - `coin`, `fiat`, `volumen`
   - 如适用，还需输入 `exchange`
3. 使用 `curl -s` 发送请求，并使用 `jq` 解析响应
4. 如果响应为 `"Invalid pair"` 或响应格式不是JSON，说明参数无效
5. 首先展示可操作的汇总信息：
   - 最优买价 (`bestBid`)
   - 最优卖价 (`bestAsk`)
   - 相关的价差 (`spread`)
6. 展示详细信息：
   - 按交易所划分的顶级交易所及其价格信息 (`time`)

## 错误处理

- **参数无效/不支持的货币对**:
  - 即使HTTP状态码为 `200`，也会检测到 `"Invalid pair"` 的错误，并明确提示请求的组合不受支持
- **网络问题/超时**:
  - 重试最多2次，并设置较短的等待时间
  - 如果失败，返回包含请求端点的明确错误信息
- **响应格式错误**:
  - 显示原始的JSON内容，并说明格式不一致的问题

## 结果展示

- 优先显示：
  - 最优买入价格 (`bestAsk`)
  - 最优卖出价格 (`bestBid`)
  - 按交易所划分的价差 (`spread`)
- 在对比结果中：
  - 以表格形式展示每个交易所的 `ask`, `bid`, `totalAsk`, `totalBid`, `time`
- 说明：
  - 仅提供数据信息，不提供财务建议

## 不在支持范围内的功能

此技能不应用于以下API端点：

- `/api/dolar`
- `/api/cer`
- `/api/uva`
- `/api/bancostodos`