---
name: kuvera
description: "Kuvera投资组合与市场数据命令行接口（CLI）：用于从Kuvera系统中查询共同基金数据、黄金价格、美元/印度卢比汇率、基金类别的收益情况以及用户的投资组合信息。当用户询问自己的投资情况、共同基金信息、黄金价格、市场概况或Kuvera投资组合时，可以使用该工具。"
homepage: https://kuvera.in
metadata:
  {
    "openclaw":
      {
        "emoji": "📊",
        "requires": { "bins": ["kuvera-cli"] },
      },
  }
---
# Kuvera 产品组合与市场数据命令行工具（Kuvera Portfolio & Market Data CLI）

该工具可用于从 Kuvera 平台获取印度市场数据、共同基金信息、黄金价格以及投资组合详情。

## 使用场景

✅ 当您需要查询以下信息时，请使用此工具：
- 黄金价格
- 市场行情
- 热门共同基金
- 美元兑印度卢比的汇率
- 共同基金各类别的收益率
- 关于特定共同基金（如 XYZ）的详细信息
- 查看您的 Kuvera 投资组合
- 了解您的投资表现
- 查看最近的交易记录
- 显示您正在进行的定期投资（SIP）计划
- 计算您的损益（P&L）及投资回报

## 命令列表

### 市场概览（包含黄金价格、美元汇率及共同基金类别）

```bash
kuvera-cli market
```

### 黄金价格

```bash
kuvera-cli gold
```

### 美元兑印度卢比汇率

```bash
kuvera-cli usd
```

### 共同基金类别收益率

```bash
kuvera-cli categories
```

### 共同基金详情（按代码查询）

```bash
# Example: look up a specific fund
kuvera-cli fund LFAG-GR
```

### 热门共同基金

```bash
# Top bought funds
kuvera-cli top bought

# Top sold funds
kuvera-cli top sold

# Most watched funds
kuvera-cli top watched
```

### 用户信息（需要登录）

```bash
kuvera-cli user
```

### 带有损益的投资组合（需要登录）

```bash
kuvera-cli portfolio
```

### 最近的交易记录（需要登录）

```bash
# Show last 20 transactions (default)
kuvera-cli transactions

# Show last N transactions
kuvera-cli transactions 10
```

### 正在进行的定期投资计划（需要登录）

```bash
kuvera-cli sips
```

## 注意事项

**此工具仅支持读取数据，严禁执行以下操作：**
- 买卖、赎回或更换任何共同基金
- 下达任何交易指令或修改交易记录
- 更改用户设置或投资组合配置
- 调用任何会修改数据的 Kuvera API 接口

该命令行工具在代码层面严格限制了这些操作——所有非 GET 请求（登录请求除外）均会被阻止。

## 其他说明：
- 所有市场数据相关的命令无需登录即可使用。
- `kuvera-cli user`、`portfolio`、`transactions` 和 `sips` 命令均需通过 `kuvera-cli login <email> <password>` 进行登录。
- 该工具仅支持数据查询，不支持任何买入、卖出或交易操作。