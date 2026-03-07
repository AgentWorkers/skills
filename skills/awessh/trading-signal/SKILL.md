---
name: trading-signal
description: 订阅并获取链上的“智能资金”交易信号。监控这些“智能资金”地址的交易活动，包括买入/卖出信号、触发价格、当前价格、最大收益以及退出价格。当用户寻找投资机会时，可以利用这些信号作为参考——它们可以为潜在的交易提供有价值的信息。
metadata:
  author: binance-web3-team
  version: "1.0"
---
# 交易信号技能

## 概述

该技能可获取链上的“智能资金”交易信号，帮助用户追踪专业投资者的交易行为：

- 获取智能资金的买入/卖出信号
- 将信号触发价格与当前价格进行比较
- 分析信号的最大收益和退出比例
- 获取代币标签（例如：Pumpfun、DEX Paid）

## API 端点

### 获取智能资金信号

**方法**：POST

**URL**： 
```
https://web3.binance.com/bapi/defi/v1/public/wallet-direct/buw/wallet/web/signal/smart-money
```

**请求头**：
```
Content-Type: application/json
Accept-Encoding: identity
```

**请求体**：
```json
{
    "smartSignalType": "",
    "page": 1,
    "pageSize": 100,
    "chainId": "CT_501"
}
```

**请求参数**：

| 参数 | 类型 | 是否必填 | 说明 |
|-------|------|----------|-------------|
| smartSignalType | string | 否 | 信号类型过滤器，空字符串表示获取所有类型 |
| page | number | 是 | 页码，从 1 开始 |
| pageSize | number | 是 | 每页显示的条目数，最多 100 条 |
| chainId | string | 是 | 链ID：BSC 为 `56`，Solana 为 `CT_501` |

**示例请求**：
```bash
curl --location 'https://web3.binance.com/bapi/defi/v1/public/wallet-direct/buw/wallet/web/signal/smart-money' \
--header 'Content-Type: application/json' \
--header 'Accept-Encoding: identity' \
--data '{"smartSignalType":"","page":1,"pageSize":100,"chainId":"CT_501"}'
```

**响应示例**：
```json
{
    "code": "000000",
    "message": null,
    "messageDetail": null,
    "data": [
        {
            "signalId": 22179,
            "ticker": "symbol of the token",
            "chainId": "CT_501",
            "contractAddress": "NV...pump",
            "logoUrl": "/images/web3-data/public/token/logos/825C62EC6BE6.png",
            "chainLogoUrl": "https://bin.bnbstatic.com/image/admin_mgs_image_upload/20250303/42065e0a-3808-400e-b589-61c2dbfc0eac.png",
            "tokenDecimals": 6,
            "isAlpha": false,
            "launchPlatform": "Pumpfun",
            "mark": null,
            "isExclusiveLaunchpad": false,
            "alphaPoint": null,
            "tokenTag": {
                "Social Events": [
                    {"tagName": "DEX Paid", "languageKey": "wmp-label-update-dexscreener-social"}
                ],
                "Launch Platform": [
                    {"tagName": "Pumpfun", "languageKey": "wmp-label-title-pumpfun"}
                ],
                "Sensitive Events": [
                    {"tagName": "Smart Money Add Holdings", "languageKey": "wmp-label-title-smart-money-add-position"}
                ]
            },
            "smartSignalType": "SMART_MONEY",
            "smartMoneyCount": 5,
            "direction": "buy",
            "timeFrame": 883000,
            "signalTriggerTime": 1771903462000,
            "totalTokenValue": "3436.694044670495772073",
            "alertPrice": "0.024505932131088482",
            "alertMarketCap": "24505118.720436560690909782",
            "currentPrice": "0.025196",
            "currentMarketCap": "25135683.751234890220129783671668745",
            "highestPrice": "0.027244000000000000",
            "highestPriceTime": 1771927760000,
            "exitRate": 78,
            "status": "timeout",
            "maxGain": "5.4034",
            "signalCount": 23
        }
    ],
    "success": true
}
```

**响应字段**：

### 基本信息
| 字段 | 类型 | 说明 |
|-------|------|-------------|
| signalId | number | 唯一的信号 ID |
| ticker | string | 代币符号/名称 |
| chainId | string | 链ID |
| contractAddress | string | 代币合约地址 |
| logoUrl | string | 代币图标 URL 路径 |
| chainLogoUrl | string | 链图标 URL |
| tokenDecimals | number | 代币的小数位数 |

### 标签信息
| 字段 | 类型 | 说明 |
|-------|------|-------------|
| isAlpha | boolean | 是否为 Alpha 代币 |
| launchPlatform | string | 发布平台（例如：Pumpfun） |
| isExclusiveLaunchpad | boolean | 是否为独家发布平台 |
| alphaPoint | number | Alpha 分数（可为空） |
| tokenTag | object | 代币标签类别 |

### 信号数据
| 字段 | 类型 | 说明 |
|-------|------|-------------|
| smartSignalType | string | 信号类型，例如：`SMART_MONEY` |
| smartMoneyCount | number | 参与交易的智能资金地址数量 |
| direction | string | 交易方向：`buy` / `sell` |
| timeFrame | number | 时间范围（毫秒） |
| signalTriggerTime | number | 信号触发时间（毫秒） |
| signalCount | number | 总信号数量 |

### 价格数据
| 字段 | 类型 | 说明 |
| totalTokenValue | string | 总交易金额（美元） |
| alertPrice | string | 信号触发时的价格 |
| alertMarketCap | string | 信号触发时的市值 |
| currentPrice | string | 当前价格 |
| currentMarketCap | string | 当前市值 |
| highestPrice | string | 信号触发后的最高价格 |
| highestPriceTime | number | 最高价格的时间戳（毫秒） |

### 性能数据
| 字段 | 类型 | 说明 |
| exitRate | number | 退出比例（%） |
| status | string | 信号状态：`active`/`timeout`/`completed` |
| maxGain | string | 最大收益（%） |

## 代币标签类型

### 社交事件
| 标签 | 说明 |
|-----|-------------|
| DEX Paid | 通过 DEX 支付的推广活动 |

### 发布平台
| 标签 | 说明 |
|-----|-------------|
| Pumpfun | Pump.fun 平台 |
| Moonshot | Moonshot 平台 |

### 敏感事件
| 标签 | 说明 |
|-----|-------------|
| Smart Money Add Holdings | 智能资金增加持有量 |
| Smart Money Reduce Holdings | 智能资金减少持有量 |
| Whale Buy | 鲸鱼投资者买入 |
| Whale Sell | 鲸鱼投资者卖出 |

## 支持的链

| 链名称 | chainId |
|------------|---------|
| BSC | 56 |
| Solana | CT_501 |

## 信号状态

| 状态 | 说明 |
|--------|-------------|
| active | 信号仍然有效 |
| timeout | 超过观察期限 |
| completed | 任务完成，达到目标或止损条件 |

## 使用场景

1. **追踪智能资金**：监控专业投资者的交易行为 |
2. **发现机会**：在智能资金买入时获取早期信号 |
3. **风险预警**：在智能资金开始卖出时接收警报 |
4. **性能分析**：分析历史信号的表现和最大收益 |
5. **策略验证**：通过退出比例（exitRate）和最大收益（maxGain）评估信号质量 |

## 示例请求

### 在 Solana 上获取智能资金信号
```bash
curl --location 'https://web3.binance.com/bapi/defi/v1/public/wallet-direct/buw/wallet/web/signal/smart-money' \
--header 'Content-Type: application/json' \
--header 'Accept-Encoding: identity' \
--data '{"smartSignalType":"","page":1,"pageSize":50,"chainId":"CT_501"}'
```

### 在 BSC 上获取信号
```bash
curl --location 'https://web3.binance.com/bapi/defi/v1/public/wallet-direct/buw/wallet/web/signal/smart-money' \
--header 'Content-Type: application/json' \
--header 'Accept-Encoding: identity' \
--data '{"smartSignalType":"","page":1,"pageSize":50,"chainId":"56"}'
```

## 注意事项

1. 代币图标 URL 需要完整的域名前缀：`https://bin.bnbstatic.com` + 图标 URL 路径 |
2. 链图标 URL（chainLogoUrl）已经是完整的 URL |
3. 所有时间戳均以毫秒为单位 |
4. maxGain 以百分比字符串形式表示 |
5. 信号可能会超时（status=timeout），请关注有效的信号 |
6. 智能资金地址数量（smartMoneyCount）越多，信号可靠性可能越高 |
7. exitRate 表示智能资金的退出状态，较高的 exitRate 可能表示信号已失效