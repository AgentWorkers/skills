# Longbridge OpenAPI

Longbridge Securities OpenAPI SDK 支持香港和美国的股票交易、实时市场数据订阅以及账户管理功能。

## 介绍

Longbridge OpenAPI 是一个与 Longbridge Securities Open API 集成的 AI 技能包，允许您使用自然语言与 OpenClaw 进行交互，轻松完成股票市场查询、交易订单处理、账户管理等操作。

## 核心功能

### 📊 市场数据
- **实时市场订阅**：订阅香港股票、美国股票和 A 股的实时市场数据
- **股票报价查询**：获取实时价格、成交量、价格变动等数据
- **K线图数据**：支持分钟、日、周、月和年等多个时间周期
- **静态信息**：查询股票名称、交易所、货币、交易单位等基本信息

### 💰 交易功能
- **智能订单下达**：支持限价单、市价单、增强型限价单等多种订单类型
- **订单管理**：取消订单、修改订单
- **订单查询**：查看当天的订单、历史订单和交易记录
- **多市场支持**：涵盖香港股票、美国股票和 A 股

### 💼 账户管理
- **资金查询**：实时查看账户余额、可用资金和净资产
- **持仓管理**：查询当前持仓、成本价、市场价值等信息
- **多货币支持**：支持港元（HKD）、美元（USD）、人民币（CNY）等多种货币

## 支持的市场

| 市场 | 代码格式 | 示例 |
|--------|------------|----------|
| 🇭🇰 香港 | `XXX.HK` | `700.HK`（腾讯）、`9988.HK`（阿里巴巴） |
| 🇺🇸 美国股票 | `XXX.US` | `AAPL.US`（苹果）、`TSLA.US`（特斯拉） |
| 🇨🇳 A 股 | `XXX.SH/SZ` | `000001.SZ`（平安银行）、`600519.SH`（茅台） |

## 配置指南

### 1. 获取 API 凭据

访问 [Longbridge Open Platform](https://open.longportapp.com/) 注册账户并创建应用程序，以获取以下信息：
- **应用密钥**：App Key
- **应用秘钥**：App Secret
- **访问令牌**：Access Token

### 2. 配置环境变量

在使用此技能之前，必须设置以下环境变量：

```bash
export LONGBRIDGE_APP_KEY="your_app_key_here"
export LONGBRIDGE_APP_SECRET="your_app_secret_here"
export LONGBRIDGE_ACCESS_TOKEN="your_access_token_here"
```

**持久化配置**（推荐）：

将配置添加到 `~/.bashrc` 或 `~/.zshrc` 文件中：

```bash
# Longbridge OpenAPI Configuration
export LONGBRIDGE_APP_KEY="your_app_key_here"
export LONGBRIDGE_APP_SECRET="your_app_secret_here"
export LONGBRIDGE_ACCESS_TOKEN="your_access_token_here"
```

然后执行 `source ~/.bashrc` 或 `source ~/.zshrc` 以应用配置。

## 使用示例

### 示例 1：查询股票市场数据

**用户输入：**
```
Query the latest stock prices of Tencent and Alibaba
```

**OpenClaw 操作：**
- 调用 `get_realtime_quote` 工具
- 参数：`symbols=['700.HK', '9988.HK']`

**响应：**
```
Tencent Holdings (700.HK)
Latest: 320.40 HKD | Change: +2.40 (+0.75%)
Open: 318.00 | High: 322.80 | Low: 317.60
Volume: 1,234,567 shares | Turnover: 395M HKD

Alibaba-SW (9988.HK)
Latest: 78.50 HKD | Change: -1.20 (-1.51%)
Open: 79.20 | High: 80.00 | Low: 78.00
Volume: 2,345,678 shares | Turnover: 184M HKD
```

### 示例 2：获取 K线图数据

**用户输入：**
```
Get the last 7 days of daily candlestick data for Apple stock
```

**OpenClaw 操作：**
- 调用 `get_candlesticks` 工具
- 参数：`symbol='AAPL.US', period='day', count=7`

**响应：**
返回包含开盘价、最高价、最低价、收盘价、成交量等数据的 7 条 K 线图

### 示例 3：提交买入订单

**用户输入：**
```
Buy 100 shares of Tencent at 320 HKD
```

**OpenClaw 操作：**
- 首先与用户确认订单详情
- 调用 `submit_order` 工具
- 参数：
  ```python
  symbol='700.HK'
  order_type='LO'  # Limit order
  side='Buy'
  quantity=100
  price=320.0
  time_in_force='Day'
  ```

**响应：**
```
✅ Order submitted successfully
Order ID: 123456789
Stock: Tencent Holdings (700.HK)
Side: Buy
Quantity: 100 shares
Price: 320.00 HKD
Type: Limit Order (Day)
```

### 示例 4：查询账户信息

**用户输入：**
```
What is my account balance?
```

**OpenClaw 操作：**
- 调用 `get_account_balance` 工具

**响应：**
```
💰 Account Fund Status

HKD Account
Cash: 50,000.00 HKD
Buying Power: 100,000.00 HKD
Net Assets: 150,000.00 HKD

USD Account
Cash: 10,000.00 USD
Buying Power: 20,000.00 USD
Net Assets: 30,000.00 USD
```

### 示例 5：查看持仓情况

**用户输入：**
```
What stocks do I hold?
```

**OpenClaw 操作：**
- 调用 `get_stock_positions` 工具

**响应：**
```
📊 Current Positions

1. Tencent Holdings (700.HK)
   Quantity: 500 shares | Available: 500 shares
   Cost: 300.00 HKD | Current: 320.40 HKD
   Market Value: 160,200.00 HKD | P&L: +10,200.00 (+6.80%)

2. Apple (AAPL.US)
   Quantity: 100 shares | Available: 100 shares
   Cost: 150.00 USD | Current: 175.50 USD
   Market Value: 17,550.00 USD | P&L: +2,550.00 (+17.00%)
```

## API 工具列表

### 市场数据工具
| 工具名称 | 描述 |
|-----------|-------------|
| `quote_subscribe` | 订阅实时市场数据（报价/深度/经纪商/交易） |
| `get_realtime_quote` | 获取实时股票报价 |
| `get_static_info` | 获取股票静态信息 |
| `get_candlesticks` | 获取历史 K 线图数据 |

### 交易工具
| 工具名称 | 描述 |
|-----------|-------------|
| `submit_order` | 提交交易订单 |
| `cancel_order` | 取消订单 |
| `get_today_orders` | 获取当天的订单列表 |
| `get_history_orders` | 获取历史订单 |

### 账户工具
| 工具名称 | 描述 |
|-----------|-------------|
| `get_account_balance` | 查询账户资金余额 |
| `get_stock_positions` | 查询持仓列表 |

## 订单类型说明

| 类型代码 | 订单类型 | 描述 |
|-----------|------------|-------------|
| `LO` | 限价单 | 在指定价格或更优价格执行 |
| `MO` | 市价单 | 立即以当前市场价格执行 |
| `ELO` | 增强型限价单 | 仅适用于香港股票，可在多个价格水平匹配 |
| `ALO` | 拍卖限价单 | 在拍卖期间使用 |

## 订单生效时间

| 代码 | 有效时间 | 描述 |
|------|---------------|-------------|
| `Day` | 当日订单 | 仅在当前交易日内有效 |
| `GTC` | 有效直至取消 | 有效直至成交或手动取消 |
| `GTD` | 有效直至指定日期 | 有效直至指定日期 |

## 安全注意事项

### ⚠️ 风险提示
1. **投资风险**：股票交易涉及市场风险，用户需自行承担投资决策责任
2. **仅用于学习**：此技能仅用于技术学习和研究，不构成投资建议
3. **谨慎使用**：未经充分测试，请勿在生产环境中直接使用

### 🔒 安全建议
1. **保护密钥**：妥善保管 API 密钥，切勿泄露给他人或上传到代码仓库
2. **使用演示账户测试**：建议先使用 Longbridge 的演示账户进行测试
3. **订单确认**：所有交易操作在执行前应手动确认
4. **权限控制**：为 API 密钥设置必要的最小权限
5. **定期轮换**：定期轮换 API 密钥以提高安全性

## 技术架构

```
┌──────────────────┐
│    OpenClaw      │  ← User natural language interaction
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Longbridge Skill │  ← Skill layer (tool invocation)
│   (skill.py)     │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Longbridge SDK   │  ← Python SDK (FFI)
│   (longbridge)   │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Longbridge API   │  ← REST API / WebSocket
│ (HTTP/WebSocket) │
└──────────────────┘
```

## 依赖项

- **Python**：>= 3.7
- **longbridge**：>= 0.2.77

安装此技能时，依赖项将自动安装。

## 常见问题

### Q1：如何获取 API 密钥？
访问 [Longbridge Open Platform](https://open.longportapp.com/)，注册账户，然后在“应用程序管理”中创建应用程序以获取密钥。

### Q2：支持演示账户吗？
是的，Longbridge 提供演示账户供测试使用。您可以在开放平台上切换到模拟环境。

### Q3：如果订单提交失败怎么办？
请检查：
- 环境变量配置是否正确？
- API 密钥是否有效？
- 账户余额是否足够？
- 是否在交易时间内？
- 订单参数（价格、数量等）是否有效？

### Q4：支持哪些市场？
目前支持香港、美国和 A 股市场的股票、ETF、权证和期权交易。

### Q5：如何查看 API 调用日志？
SDK 会内部输出日志。您可以配置 Python 的日志模块来查看详细的调用信息。

## 更新日志

### v1.0.0 (2026-02-02)
- ✨ 初始发布
- ✅ 支持实时市场查询和订阅
- ✅ 支持订单提交、取消和修改
- ✅ 支持账户资金和持仓查询
- ✅ 支持历史 K 线图数据检索
- ✅ 完全覆盖香港、美国和 A 股市场

## 参考资料

- 📖 [Longbridge OpenAPI 官方文档](https://open.longbridge.com/docs)
- 🐍 [Python SDK 文档](https://longbridge.readthedocs.io/en/latest/)
- 💻 [GitHub 源代码仓库](https://github.com/longportapp/openapi)
- 📦 [PyPI 包](https://pypi.org/project/longbridge/)
- 🌐 [Open Platform 主页](https://open.longportapp.com/)

## 许可证

MIT 许可证

## 作者

genkin

## 支持

如有任何问题或建议，请通过以下方式联系我们：
- 在 GitHub 上提交问题
- 访问 Longbridge 开发者社区
- 查阅官方文档

---

**免责声明**：此技能仅用于学习和技术研究，不构成投资建议。用户应充分了解股票投资的风险，并自行承担投资决策责任。