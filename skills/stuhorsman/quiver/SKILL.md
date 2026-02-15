---
name: quiver
description: 从 Quiver Quantitative 获取替代性金融数据（包括国会交易、游说活动、政府合同以及内幕交易信息）。利用这些数据来追踪政治人物的股票交易行为或非传统市场信号。
---

# Quiver Quantitative 技能

您可以使用 Quiver Quantitative 提供的替代数据集来追踪非传统市场信号。

## 先决条件

- **API 令牌：** 您需要一个 Quiver Quantitative 的 API 令牌。
- **环境配置：** 在您的环境变量中设置 `QUIVER_API_KEY`，或参考 `TOOLS.md` 文件中的配置。

## 使用方法

此技能通过 Python 脚本获取数据，并以 JSON 格式返回结果。

### 国会交易
追踪美国参议员和众议员的股票交易记录。

```bash
# Recent trades by all members
skills/quiver/scripts/query_quiver.py congress

# Specific Ticker
skills/quiver/scripts/query_quiver.py congress --ticker NVDA

# Specific Politician
skills/quiver/scripts/query_quiver.py congress --politician "Nancy Pelosi"
```

### 企业游说
追踪企业的游说支出情况。

```bash
skills/quiver/scripts/query_quiver.py lobbying AAPL
```

### 政府合同
追踪授予企业的政府合同信息。

```bash
skills/quiver/scripts/query_quiver.py contracts LMT
```

### 内幕交易
追踪企业的内幕交易行为。

```bash
skills/quiver/scripts/query_quiver.py insiders TSLA
```

## 输出结果

所有命令都会输出一个 JSON 数组形式的记录。您可以将该输出结果传递给 `jq` 工具进行过滤或格式化处理。

```bash
# Get Pelosi's recent NVDA trades
skills/quiver/scripts/query_quiver.py congress --politician "Nancy Pelosi" | jq '.[] | select(.Ticker == "NVDA")'
```