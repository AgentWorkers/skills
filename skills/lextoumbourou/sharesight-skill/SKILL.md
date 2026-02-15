---
name: sharesight
version: 1.0.0
description: 通过 API 管理 Shareight 的投资组合、持仓以及自定义投资。
metadata: {"openclaw": {"category": "finance", "requires": {"env": ["SHARESIGHT_CLIENT_ID", "SHARESIGHT_CLIENT_SECRET"]}, "optional_env": ["SHARESIGHT_ALLOW_WRITES"]}}
---

# Sharesight Skill

用于管理Sharesight的投资组合、持仓、自定义投资、价格以及票息率。支持完整的CRUD（创建、读取、更新、删除）操作。

## 先决条件

请设置以下环境变量：
- `SHARESIGHT_CLIENT_ID`：您的Sharesight API客户端ID
- `SHARESIGHT_CLIENT_SECRET`：您的Sharesight API客户端密钥
- `SHARESIGHT_ALLOW_WRITES`：设置为`true`以启用创建、更新和删除操作（出于安全考虑，默认为禁用状态）

## 命令

### 认证

```bash
# Authenticate (required before first use)
sharesight auth login

# Check authentication status
sharesight auth status

# Clear saved token
sharesight auth clear
```

### 投资组合

```bash
# List all portfolios
sharesight portfolios list
sharesight portfolios list --consolidated

# Get portfolio details
sharesight portfolios get <portfolio_id>

# List holdings in a portfolio
sharesight portfolios holdings <portfolio_id>

# Get performance report
sharesight portfolios performance <portfolio_id>
sharesight portfolios performance <portfolio_id> --start-date 2024-01-01 --end-date 2024-12-31
sharesight portfolios performance <portfolio_id> --grouping market --include-sales

# Get performance chart data
sharesight portfolios chart <portfolio_id>
sharesight portfolios chart <portfolio_id> --benchmark SPY.NYSE
```

### 持仓

```bash
# List all holdings across portfolios
sharesight holdings list

# Get holding details
sharesight holdings get <holding_id>
sharesight holdings get <holding_id> --avg-price --cost-base
sharesight holdings get <holding_id> --values-over-time true

# Update holding DRP settings
sharesight holdings update <holding_id> --enable-drp true --drp-mode up
# drp-mode options: up, down, half, down_track

# Delete a holding
sharesight holdings delete <holding_id>
```

### 自定义投资

```bash
# List custom investments
sharesight investments list
sharesight investments list --portfolio-id <portfolio_id>

# Get custom investment details
sharesight investments get <investment_id>

# Create a custom investment
sharesight investments create --code TEST --name "Test Investment" --country AU --type ORDINARY
# type options: ORDINARY, TERM_DEPOSIT, FIXED_INTEREST, PROPERTY, ORDINARY_UNLISTED, OTHER

# Update a custom investment
sharesight investments update <investment_id> --name "New Name"

# Delete a custom investment
sharesight investments delete <investment_id>
```

### 价格（自定义投资价格）

```bash
# List prices for a custom investment
sharesight prices list <instrument_id>
sharesight prices list <instrument_id> --start-date 2024-01-01 --end-date 2024-12-31

# Create a price
sharesight prices create <instrument_id> --price 100.50 --date 2024-01-15

# Update a price
sharesight prices update <price_id> --price 101.00

# Delete a price
sharesight prices delete <price_id>
```

### 票息率（固定收益）

```bash
# List coupon rates for a fixed interest investment
sharesight coupon-rates list <instrument_id>
sharesight coupon-rates list <instrument_id> --start-date 2024-01-01

# Create a coupon rate
sharesight coupon-rates create <instrument_id> --rate 5.5 --date 2024-01-01

# Update a coupon rate
sharesight coupon-rates update <coupon_rate_id> --rate 5.75

# Delete a coupon rate
sharesight coupon-rates delete <coupon_rate_id>
```

### 参考数据

```bash
# List country codes
sharesight countries
sharesight countries --supported
```

## 输出格式

所有命令的输出均为JSON格式。例如，投资组合列表的响应格式如下：

```json
{
  "portfolios": [
    {
      "id": 12345,
      "name": "My Portfolio",
      "currency_code": "AUD",
      "country_code": "AU"
    }
  ]
}
```

## 日期格式

所有日期均使用`YYYY-MM-DD`格式（例如，`2024-01-15`）。

## 分组选项

性能报告支持以下分组方式：
- `country`：按国家分组
- `currency`：按货币分组
- `market`：按市场分组（默认）
- `portfolio`：按投资组合分组
- `sector_classification`：按行业分类分组
- `industry_classification`：按行业分类分组
- `investment_type`：按投资类型分组
- `ungrouped`：不进行分组

## 写入保护

出于安全考虑，写入操作（创建、更新、删除）默认是禁用的。要启用这些操作，请执行以下操作：

```bash
export SHARESIGHT_ALLOW_WRITES=true
```

如果不设置此选项，写入命令将会失败，并显示相应的错误信息：

```json
{"error": "Write operations are disabled by default. Set SHARESIGHT_ALLOW_WRITES=true to enable create, update, and delete operations.", "hint": "export SHARESIGHT_ALLOW_WRITES=true"}
```

## 常见工作流程

### 查看投资组合表现

```bash
# Get current year performance
sharesight portfolios performance 12345 --start-date 2024-01-01

# Compare against S&P 500
sharesight portfolios chart 12345 --benchmark SPY.NYSE
```

### 分析持仓情况

```bash
# List all holdings with cost information
sharesight holdings get 67890 --avg-price --cost-base
```

### 跟踪自定义投资

```bash
# Create a custom investment for tracking unlisted assets
sharesight investments create --code REALESTATE --name "Property Investment" --country AU --type PROPERTY

# Add price history for the investment
sharesight prices create 123456 --price 500000.00 --date 2024-01-01
sharesight prices create 123456 --price 520000.00 --date 2024-06-01
```

### 管理固定收益投资

```bash
# Create a term deposit
sharesight investments create --code TD001 --name "Term Deposit ANZ" --country AU --type TERM_DEPOSIT

# Set the coupon rate
sharesight coupon-rates create 123456 --rate 4.5 --date 2024-01-01

# Update rate when it changes
sharesight coupon-rates update 789 --rate 4.75
```

### 配置股息再投资

```bash
# Enable DRP and round up purchases
sharesight holdings update 67890 --enable-drp true --drp-mode up

# Disable DRP
sharesight holdings update 67890 --enable-drp false
```