---
name: exchange-rates
description: 从 XE.com 获取任意货币对之间的实时汇率。当用户询问货币兑换、汇率或货币之间的金额转换时可以使用此功能（例如：“USD 转换为 INR”、“100 EUR 等于多少 GBP”、“美元的汇率是多少”）。
---

# 汇率（XE.com）

通过无头浏览器（headless browser）从 XE.com 获取实时中间市场汇率。

## 使用方法

```bash
node ~/clawd/skills/exchange-rates/scripts/xe-rate.mjs <FROM> <TO> [AMOUNT]
```

**示例：**
```bash
node ~/clawd/skills/exchange-rates/scripts/xe-rate.mjs USD INR        # 1 USD → INR
node ~/clawd/skills/exchange-rates/scripts/xe-rate.mjs EUR USD 500    # 500 EUR → USD
node ~/clawd/skills/exchange-rates/scripts/xe-rate.mjs THB INR 1000   # 1000 THB → INR
```

**输出格式：** JSON 格式，包含以下字段：
- `amount`（金额）
- `from`（来源货币）
- `to`（目标货币）
- `rate`（汇率）
- `converted`（转换后的金额）
- `source`（数据来源）
- `timestamp`（获取时间）

## 响应格式要求：

- 突出显示转换后的金额。
- 显示单位汇率（例如：1 FROM = X TO）。
- 明确标注数据来源为 XE.com 提供的中间市场汇率。
- 对于金额大于 1 的情况，同时显示单位汇率和总转换金额。

## 注意事项：

- 该脚本使用 Playwright 和 Browserless（CDP）技术从 XE.com 抓取数据。
- 如果 XE.com 无法正常访问，脚本会自动切换到 exchangerate-api.com 作为备用数据源。
- 货币代码遵循标准的 3 位 ISO 4217 标准（如 USD、INR、EUR、GBP、THB、JPY 等）。
- 提供的汇率为中间市场汇率（而非买卖价差）。
- 每次查询大约需要 4-5 秒（包含浏览器加载时间）。