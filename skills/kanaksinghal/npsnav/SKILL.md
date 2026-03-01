---
name: npsnav
description: 通过免费的 npsnav.in REST API，您可以查询印度国家养老金系统（National Pension System, NPS）的基金净资产价值（NAV）数据、计划详情、收益情况以及历史记录。
homepage: https://npsnav.in
metadata:
  {
    "openclaw":
      { "emoji": "🏦", "requires": { "bins": ["jq", "curl"] } },
  }
---
# NPS NAV 技能

使用免费的 [npsnav.in](https://npsnav.in) API，可以查询印度国家养老金系统（NPS）基金的数据，包括净资产价值（NAV）、计划信息、收益情况以及历史数据。

## 设置

无需认证或 API 密钥。该 API 非商业用途完全免费。

请确保已安装 `curl` 和 `jq` 工具。

## 什么是 NPS 计划代码？

NPS 计划代码的格式为 `SM` 后跟 6 位数字（例如 `SM001001`）。每个代码唯一标识一个由养老金基金管理机构（PFM）管理的 NPS 基金。计划代码可以通过 Schemes API 或 [NPS 基金完整列表](https://npsnav.in/nps-funds-list) 获取。

## 基本 URL

```
https://npsnav.in/api
```

## 使用方法

### 获取某个计划的最新净资产价值（纯文本）

最简单的 API 端点，仅返回净资产价值（NAV）的数值，非常适合用于电子表格或快速查询。

```bash
curl -s "https://npsnav.in/api/SM001001"
# → 46.7686
```

### 列出所有计划代码

```bash
curl -s "https://npsnav.in/api/schemes" | jq '.data[] | {code: .[0], name: .[1]}'
```

### 获取所有基金的最新净资产价值（详细信息）

```bash
curl -s "https://npsnav.in/api/latest" | jq '.data[:5]'
```

### 获取所有基金的最新净资产价值（简化信息）

```bash
curl -s "https://npsnav.in/api/latest-min" | jq '.data[:5]'
```

### 获取包含收益的详细基金数据

```bash
curl -s "https://npsnav.in/api/detailed/SM001001" | jq '.'
```

### 获取历史净资产价值数据

```bash
curl -s "https://npsnav.in/api/historical/SM001001" | jq '.data[:5]'
```

## 更多示例

```bash
# Get NAV for SBI Pension Fund (Central Govt)
curl -s "https://npsnav.in/api/SM001001"

# List all NPS scheme names
curl -s "https://npsnav.in/api/schemes" | jq '.data[] | .[1]'

# Get detailed data with returns for a scheme
curl -s "https://npsnav.in/api/detailed/SM001001" | jq '{name: .["Scheme Name"], nav: .NAV, "1Y": .["1Y"], "3Y": .["3Y"]}'

# Get latest NAV and date for all funds
curl -s "https://npsnav.in/api/latest" | jq '.data[] | {code: .["Scheme Code"], name: .["Scheme Name"], nav: .NAV}'

# Get historical NAV for a scheme
curl -s "https://npsnav.in/api/historical/SM001001" | jq '[.data[0], .data[-1]] | {latest: .[0], oldest: .[1]}'

# Find a scheme by name (filter from schemes list)
curl -s "https://npsnav.in/api/schemes" | jq '.data[] | select(.[1] | test("HDFC")) | {code: .[0], name: .[1]}'
```

## API 端点参考

| 方法                | 端点                          | 描述                                      | 响应类型     |
|------------------|-----------------------------|-----------------------------------------|-----------|
| GET                | `/api/schemes`                | 列出所有计划代码和名称                        | JSON        |
| GET                | `/api/{scheme_code}`            | 某个计划的最新净资产价值                     | 纯文本       |
| GET                | `/api/latest`                | 所有基金的最新净资产价值（详细信息）                | JSON        |
| GET                | `/api/latest-min`                | 所有基金的最新净资产价值（简化信息）                | JSON        |
| GET                | `/api/detailed/{scheme_code}`          | 包含收益的基金详细数据                        | JSON        |
| GET                | `/api/historical/{scheme_code}`        | 某个计划的历史净资产价值数据                    | JSON        |

## 注意事项

- 计划代码的格式为 `SM` + 6 位数字（例如 `SM001001`）
- 响应中的日期采用 `DD-MM-YYYY` 格式
- 简单 API (`/api/{scheme_code}`) 返回纯文本，而非 JSON 格式
- `/api/schemes` 端点返回大约 151 个 NPS 计划的代码
- 无需 API 密钥或使用频率限制，非商业用途可无限使用
- 数据来源于 Protean eGov Technologies 和 NPS Trust