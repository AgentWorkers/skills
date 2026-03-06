---
name: weather-plus
description: >
  获取当前天气、多日天气预报、穿衣指数以及体感温度。无需使用 API 密钥。适用于以下场景：  
  (1) 查看当前天气；  
  (2) 查看多日天气预报；  
  (3) 获取穿衣建议；  
  (4) 查看体感温度和舒适度指数。  
  支持全球任何城市。  
  使用 SkillPay.me 付费，费用为每次调用 0.001 美元。
---
# Weather Plus

提供天气信息、天气预报、穿衣建议以及体感温度。无需使用API密钥。每次调用费用为0.001 USDT。

## 命令

| 命令 | 脚本 | 描述 |
|:---|:---|:---|
| **weather** | `scripts/weather.py` | 当前天气及体感温度 |
| **forecast** | `scripts/forecast.py` | 多日天气预报（最长7天） |
| **clothing** | `scripts/clothing.py` | 穿衣建议及推荐 |
| **billing** | `scripts/billing.py` | SkillPay费用结算/余额查询/支付 |

## 工作流程

```
1. Billing:   python3 scripts/billing.py --charge --user-id <id>
2. Weather:   python3 scripts/weather.py --city "Beijing"
3. Forecast:  python3 scripts/forecast.py --city "Shanghai" --days 5
4. Clothing:  python3 scripts/clothing.py --city "Chengdu"
```

## 示例

```bash
# Current weather
python3 scripts/weather.py --city "New York"
python3 scripts/weather.py --city "成都"

# Multi-day forecast
python3 scripts/forecast.py --city "Tokyo" --days 7

# Clothing index
python3 scripts/clothing.py --city "Beijing"
python3 scripts/clothing.py --city "London"
```

## 配置

| 环境变量 | 是否必需 | 描述 |
|:---|:---|:---|
| `SKILLPAY_API_KEY` | 是 | SkillPay.me的API密钥 |

## 参考资料

有关穿衣建议的详细方法，请参阅`references/clothing-index.md`。