---
name: mfapi
description: 通过免费的 MFapi.in REST API，可以查询印度共同基金的净资产价值（NAV）、基金方案信息以及历史数据。
homepage: https://www.mfapi.in
metadata:
  {
    "openclaw":
      { "emoji": "₹", "requires": { "bins": ["jq", "curl"] } },
  }
---
# MFapi 技能

使用免费的 [MFapi.in](https://www.mfapi.in) API 查询印度共同基金的数据——包括净资产价值（NAV）历史记录、基金方案信息等。

## 设置

无需进行身份验证或提供 API 密钥。该 API 完全免费且开放使用。

请确保已安装 `curl` 和 `jq` 工具：

```bash
# Debian/Ubuntu
sudo apt install -y curl jq

# macOS
brew install curl jq
```

## 什么是 ISIN 代码？

ISIN（国际证券识别码）是一个由 12 个字符组成的字母数字代码，用于在全球范围内唯一标识一种证券（例如 `INF200K01UT4`）。印度共同基金方案通常具有两个 ISIN 代码：

- **isinGrowth**：用于标识基金的成长型投资选项；
- **isinDivReinvestment**：用于标识基金的股息再投资选项（可能为 `null`）。

ISIN 代码会印在合并账户报表（CAS）、经纪/证券托管平台上以及 AMFI（印度共同基金管理局）的网站上。这些代码是稳定的标识符——与基金名称不同，它们不会因基金管理公司的品牌变更而改变。

## 基本 URL

```
https://api.mfapi.in
```

数据每天更新 6 次（时间分别为印度标准时间（IST）的上午 10:05、下午 2:05、下午 6:05、晚上 9:05、凌晨 3:09 和上午 5:05）。

## 使用方法

### 按名称搜索基金方案

```bash
curl -s "https://api.mfapi.in/mf/search?q=HDFC" | jq '.[] | {schemeCode, schemeName}'
```

### 列出所有基金方案（分页显示）

```bash
curl -s "https://api.mfapi.in/mf?limit=100&offset=0" | jq '.[] | {schemeCode, schemeName}'
```

### 获取某个基金的最新净资产价值

```bash
curl -s "https://api.mfapi.in/mf/125497/latest" | jq '{scheme: .meta.scheme_name, nav: .data[0].nav, date: .data[0].date}'
```

### 获取某个基金的净资产价值历史记录

```bash
curl -s "https://api.mfapi.in/mf/125497" | jq '{scheme: .meta.scheme_name, records: (.data | length)}'
```

### 获取指定日期范围内的净资产价值历史记录

```bash
curl -s "https://api.mfapi.in/mf/125497?startDate=2023-01-01&endDate=2023-12-31" | jq '.data'
```

### 获取所有基金的最新净资产价值

```bash
curl -s "https://api.mfapi.in/mf/latest" | jq '.[:5]'
```

## 响应格式

### 最新净资产价值（`/mf/{scheme_code}/latest`）

```json
{
  "meta": {
    "fund_house": "HDFC Mutual Fund",
    "scheme_type": "Open Ended Schemes",
    "scheme_category": "Equity Scheme - Large Cap Fund",
    "scheme_code": 125497,
    "scheme_name": "HDFC Top 100 Fund - Direct Plan - Growth",
    "isin_growth": "INF179K01BB2",
    "isin_div_reinvestment": null
  },
  "data": [
    {
      "date": "26-10-2024",
      "nav": "892.45600"
    }
  ],
  "status": "SUCCESS"
}
```

### 搜索（`/mf/search?q=...`）

```json
[
  {
    "schemeCode": 125497,
    "schemeName": "HDFC Top 100 Fund - Direct Plan - Growth"
  }
]
```

### 基金方案列表（`/mf`）

```json
[
  {
    "schemeCode": 125497,
    "schemeName": "HDFC Top 100 Fund - Direct Plan - Growth",
    "isinGrowth": "INF179K01BB2",
    "isinDivReinvestment": "INF179K01BC0"
  }
]
```

## 端点参考

| 方法 | 端点 | 描述 | 参数 |
|--------|----------|-------------|------------|
| GET | `/mf/search` | 按名称搜索基金方案 | `q`（必填） |
| GET | `/mf` | 列出所有基金方案（分页显示） | `limit`（1–1000），`offset`（默认值 0） |
| GET | `/mf/{scheme_code}` | 获取某个基金的净资产价值历史记录 | `startDate`，`endDate`（ISO 8601 格式） |
| GET | `/mf/{scheme_code}/latest` | 获取某个基金的最新净资产价值 | — |
| GET | `/mf/latest` | 获取所有基金的最新净资产价值 | — |

## 通过 ISIN 获取最新净资产价值（Python 示例）

该 API 不支持直接通过 ISIN 进行查询。`scripts/get_nav.py` 脚本会使用本地缓存的基金方案列表将 ISIN 转换为对应的基金代码，然后获取该基金的最新净资产价值。

### 工作原理

1. **缓存**：将所有基金方案的列表（约 37,000 个方案）下载到 `/tmp/mfapi-schemes.json` 文件中。如果缓存缺失或超过 24 小时，系统会自动刷新缓存。
2. **查找**：在缓存中搜索 `isinGrowth` 和 `isinDivReinvestment` 字段。如果没有找到匹配项，则刷新缓存并重新尝试查询。
3. **获取数据**：使用转换后的基金代码调用 `/mf/{scheme_code}/latest` 端点来获取数据。

### 使用示例

```bash
# Single ISIN
python3 scripts/get_nav.py INF200K01UT4

# Multiple ISINs
python3 scripts/get_nav.py INF200K01UT4 INF846K01DP8
```

### 示例输出

```json
{
  "isin": "INF200K01UT4",
  "scheme_code": 119800,
  "scheme_name": "SBI Liquid Fund - DIRECT PLAN -Growth",
  "fund_house": "SBI Mutual Fund",
  "category": "Debt Scheme - Liquid Fund",
  "nav": "4277.67540",
  "date": "18-02-2026"
}
```

当传递多个 ISIN 代码时，输出结果将以 JSON 数组的形式返回。

## 注意事项

- 响应中的日期格式为 `DD-MM-YYYY`；查询参数使用 ISO 8601 格式（`YYYY-MM-DD`）；
- 净资产价值（NAV）以小数点后 5 位的精度显示为字符串；
- 基金代码可以通过搜索或列表端点获取，也可以从 AMFI 的网站上查询；
- `/mf` 端点返回所有约 37,000 个基金方案的信息；Python 脚本会将这些信息缓存在 `/tmp/mfapi-schemes.json` 文件中，以避免重复进行大量数据请求；
- 如果缓存未找到相应信息或超过 24 小时，系统会自动刷新缓存；
- 虽然 API 没有明确设置请求速率限制，但建议合理使用该服务。

## 示例用法

```bash
# Find all SBI mutual fund schemes
curl -s "https://api.mfapi.in/mf/search?q=SBI" | jq '.[].schemeName'

# Get today's NAV for a known scheme
curl -s "https://api.mfapi.in/mf/119551/latest" | jq '.data[0]'

# Compare NAVs across a year
curl -s "https://api.mfapi.in/mf/125497?startDate=2025-01-01&endDate=2025-12-31" \
  | jq '[.data[0], .data[-1]] | {latest: .[0], oldest: .[1]}'

# Get fund house and category for a scheme
curl -s "https://api.mfapi.in/mf/125497/latest" | jq '.meta | {fund_house, scheme_category}'

# List first 10 Direct Plan Growth schemes matching "Axis"
curl -s "https://api.mfapi.in/mf/search?q=Axis" \
  | jq '[.[] | select(.schemeName | test("Direct.*Growth"))] | .[:10]'

# Get latest NAV by ISIN
python3 scripts/get_nav.py INF200K01UT4
```