---
name: amazon-orders
description: 通过一个非官方的 Python API 和 CLI 下载并查询您的亚马逊订单历史记录。
homepage: https://github.com/alexdlaird/amazon-orders
metadata: {"clawdbot":{"emoji":"📦","requires":{"bins":["python3","pip3"],"env":["AMAZON_USERNAME", "AMAZON_PASSWORD", "AMAZON_OTP_SECRET_KEY"]}}}
---

# amazon-orders 技能

使用非官方的 `amazon-orders` Python 包和命令行界面（CLI）来查询您的 Amazon.com 订单历史记录。

> 注意：`amazon-orders` 通过抓取/解析 Amazon 的消费者网站来获取数据，因此如果 Amazon 更改了页面结构，该工具可能会失效。目前仅支持英文版的 Amazon.com 网站。

## 设置

### 安装/升级
```bash
python3 -m pip install --upgrade amazon-orders
```
（安装详情和版本固定指南请参见项目的 README 文件。）

### 认证方式

`amazon-orders` 可以从以下来源获取认证信息（优先级从高到低）：环境变量、传递给 `AmazonSession` 的参数，或本地配置文件。

环境变量：
```bash
export AMAZON_USERNAME="you@example.com"
export AMAZON_PASSWORD="your-password"
# Optional: for accounts with OTP/TOTP enabled
export AMAZON_OTP_SECRET_KEY="BASE32_TOTP_SECRET"
```
（关于 OTP 密钥的使用方法，请参考项目的文档。）

## 使用方法

您可以将 `amazon-orders` 作为 **Python 库** 使用，也可以通过 **命令行** 来调用它。

### Python：基本用法
```python
from amazonorders.session import AmazonSession
from amazonorders.orders import AmazonOrders

amazon_session = AmazonSession("<AMAZON_EMAIL>", "<AMAZON_PASSWORD>")
amazon_session.login()

amazon_orders = AmazonOrders(amazon_session)

# Orders from a specific year
orders = amazon_orders.get_order_history(year=2023)

# Or use a time filter for recent orders
orders = amazon_orders.get_order_history(time_filter="last30")     # Last 30 days
orders = amazon_orders.get_order_history(time_filter="months-3")   # Past 3 months

for order in orders:
    print(f"{order.order_number} - {order.grand_total}")
```


#### 完整信息（获取速度较慢，包含更多字段）
某些订单字段仅在您请求完整信息时才会显示；如需更详细的订单数据，请使用以下参数：
- Python：`full_details=True`
- CLI：在 `history` 命令后添加 `--full-details`

### CLI：常用命令
```bash
# Authenticate (interactive / uses env vars if set)
amazon-orders login

# Order history
amazon-orders history --year 2023
amazon-orders history --last-30-days
amazon-orders history --last-3-months
```


### 提示

- 如果您的账户启用了多因素认证（MFA），建议在自动化脚本中设置 `AMAZON_OTP_SECRET_KEY`。
- 在自动化过程中，请将认证信息存储在安全的地方，避免泄露到 shell 历史记录中：可以使用环境变量或密钥管理工具（如 1Password、Vault、GitHub Actions 的 secrets 等）。

## 示例

### 将年度订单历史记录导出为 JSON 格式
```bash
amazon-orders history --year 2023 --full-details > orders_2023.json
```

### 快速查看订单总额（需要使用 jq 工具）
```bash
amazon-orders history --last-30-days --full-details   | jq -r '.[] | [.order_number, .grand_total] | @tsv'
```

## 注意事项

- 这是一个基于抓取技术的非官方工具，并非官方提供的 Amazon API。
- 官方文档请访问 [Read the Docs](https://docs.amazon.com/) 以获取高级用法和 API 的详细信息（如订单、交易等）。