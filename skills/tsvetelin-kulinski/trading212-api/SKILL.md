---
name: trading212-api
description: '当用户请求“连接到Trading 212”、“认证Trading 212 API”、“下订单”、“买入股票”、“卖出股票”、“下达市价单”、“下达限价单”、“取消订单”、“查看我的余额”、“查看账户概要”、“获取持仓信息”、“查看投资组合”、“查看损益情况”、“查找股票代码”、“搜索交易工具”、“查看交易时间”、“查看股息信息”、“获取订单历史记录”、“导出交易数据”、“生成CSV报告”，或者需要关于Trading 212 API认证、订单下达、持仓监控、账户信息、工具查询或历史数据检索等方面的指导时，应使用此技能。'
license: MIT License
metadata:
  author: Trading 212
  version: 1.0.0
---

# Trading 212 API

> **注意：** Trading 212 API 目前处于 **测试** 阶段，仍在积极开发中。某些端点或功能可能会发生变化。

## 快速参考

### 环境

| 环境 | 基本 URL                             | 用途                                 |
| ----------- | ------------------------------------ | --------------------------------------- |
| 测试        | `https://demo.trading212.com/api/v0` | 不使用真实资金的模拟交易             |
| 实时        | `https://live.trading212.com/api/v0` | 使用真实资金的交易                         |

### 订单数量约定

- **正数数量 = 买入**（例如，`10` 表示买入 10 股）
- **负数数量 = 卖出**（例如，`-10` 表示卖出 10 股）

### 账户类型

仅支持 **Invest** 和 **Stocks ISA** 账户。

### 仪器标识符

Trading 212 使用自定义的 ticker 作为仪器的唯一标识符。在发起仪器请求之前，请务必查找对应的 Trading 212 ticker。

---

## 认证

使用 HTTP Basic Auth 进行认证，需要 API Key（用户名）和 API Secret（密码）。

### 先检查现有设置

在指导用户进行认证设置之前，请先确认凭据是否已经配置：

**规则说明：** 当至少有一组完整的凭据时，才认为配置完成：一组完整的凭据包括同一账户的 API Key 和 API Secret（例如 `T212_API_KEY` + `T212_API_SECRET`，或 `T212_API_KEY_INVEST` + `T212_API_SECRET_INVEST`，或 `T212_API_KEY_stockS_ISA` + `T212_API_SECRET_stockS_ISA`）。不需要所有四种账户特定的变量；只需 Invest 或 Stocks ISA 对应的凭据即可。检查是否存在至少一组可用的 key+secret 组合。

```bash
# Example: configured if any complete credential set exists
if [ -n "$T212_AUTH_HEADER" ] && [ -n "$T212_BASE_URL" ]; then
  echo "Configured (derived vars)"
elif [ -n "$T212_API_KEY" ] && [ -n "$T212_API_SECRET" ]; then
  echo "Configured (single account)"
elif [ -n "$T212_API_KEY_INVEST" ] && [ -n "$T212_API_SECRET_INVEST" ]; then
  echo "Configured (Invest); Stocks ISA also if T212_API_KEY_STOCKS_ISA and T212_API_SECRET_STOCKS_ISA are set"
elif [ -n "$T212_API_KEY_STOCKS_ISA" ] && [ -n "$T212_API_SECRET_STOCKS_ISA" ]; then
  echo "Configured (Stocks ISA); Invest also if T212_API_KEY_INVEST and T212_API_SECRET_INVEST are set"
else
  echo "No complete credential set found"
fi
```

如果存在任何一组完整的凭据，请跳过完整的设置流程，直接进行 API 调用；在发起请求时，请按照“发起请求”部分中的说明选择合适的凭据组合。不要让用户运行额外的代码或手动合并凭据。只有在没有完整凭据组合的情况下，才需要指导用户完成完整的设置流程。

> **重要提示：** 在进行任何 API 调用之前，务必询问用户希望使用哪种环境：**实时（LIVE）** 还是 **测试**（DEMO）。不要默认使用某个环境。

### API Key 是环境特定的

**API Key 与特定环境绑定，不能在不同环境之间共享。**

| API Key 的创建环境 | 可使用的环境            | 不能使用的环境    |
| ------------------ | --------------------- | --------------------- |
| 实时账户       | `live.trading212.com` | `demo.trading212.com` |
| 测试账户       | `demo.trading212.com` | `live.trading212.com` |

如果收到 401 错误，请确认：

1. 使用的 API Key 是否与目标环境匹配
2. API Key 是否在尝试访问的环境（实时或测试）中生成

### 获取凭据

1. **确定使用哪种环境** - 实时（LIVE）或测试（DEMO）
2. 打开 Trading 212 应用程序（移动端或网页版）
3. **切换到正确的账户** - 确保处于与目标环境匹配的实时或测试模式
4. 进入 **设置** > **API**
5. 生成新的 API Key 对
   - **API Key (ID)**（例如，`35839398ZFVKUxpHzPiVsxKdOtZdaDJSrvyPF`)
   - **API Secret**（例如，`7MOzYJlVJgxoPjdZJCEH3fO9ee7A0NzLylFFD4-3tlo`)
6. 如果同时使用两种环境，请分别为每种环境存储凭据

### 构建认证头部

将 API Key (ID) 和 Secret 用冒号连接起来，进行 Base64 编码，并在 Authorization 头部前加上 `Basic`。

**可选：** 可以预先计算头部信息：

```bash
export T212_AUTH_HEADER="Basic $(echo -n "$T212_API_KEY:$T212_API_SECRET" | base64)"
```

否则，代理会在发起请求时根据 `T212_API_KEY` 和 `T212_API_SECRET` 自动构建头部信息。

**手动设置（占位符示例）：**

```bash
# Format: T212_AUTH_HEADER = "Basic " + base64(API_KEY_ID:API_SECRET)
export T212_AUTH_HEADER="Basic $(echo -n "<YOUR_API_KEY_ID>:<YOUR_API_SECRET>" | base64)"

# Example with sample credentials:
export T212_AUTH_HEADER="Basic $(echo -n "35839398ZFVKUxpHzPiVsxKdOtZdaDJSrvyPF:7MOzYJlVJgxoPjdZJCEH3fO9ee7A0NzLylFFD4-3tlo" | base64)"
```

### 发起请求

在发起 API 调用时，根据实际情况选择合适的凭据组合：

- **如果 `T212_AUTH_HEADER` 和 `T212_BASE_URL` 已设置**：直接使用它们。
- **如果 `T212_API_KEY` 和 `T212_API_SECRET` 已设置**：使用这对凭据（适用于单个账户）。将头部信息设置为 `Basic $(echo -n "$T212_API_KEY:$T212_API_SECRET" | base64)`，并将基本 URL 设置为 `https://${T212_ENV:-live}.trading212.com`。不要让用户自行计算或合并凭据。
- **如果同时设置了两种账户特定的凭据对**（`T212_API_KEY_INVEST`/`T212_API_SECRET_INVEST` 和 `T212_API_KEY_stockS_ISA`/`T212_API_SECRET_stockS_ISA`）：用户必须明确指定目标账户（Invest 或 Stocks ISA）。如果用户请求的是所有账户的信息，请分别对 Invest 和 Stocks ISA 发起请求，并汇总结果。如果从上下文中无法判断使用哪个账户，请在发起请求前确认（例如：“我应该使用哪个账户——Invest 还是 Stocks ISA？”）。根据选择的凭据和基本 URL 构建头部信息：`https://${T212_ENV:-live}.trading212.com`。
- **如果只设置了 Invest 对**（`T212_API_KEY_INVEST` 和 `T212_API_SECRET_INVEST`）：使用这对凭据。
- **如果只设置了 Stocks ISA 对**（`T212_API_KEY_stockS_ISA` 和 `T212_API_SECRET_stockS_ISA`）：使用这对凭据。如果用户询问关于 Invest 的信息，说明只配置了 Invest 账户；如果询问关于 Stocks ISA 的信息，说明只配置了 Stocks ISA 账户。

当 `T212_AUTH_HEADER` 已设置时，请在 Authorization 头部中使用它的值：

```bash
# When T212_AUTH_HEADER and T212_BASE_URL are set:
curl -H "Authorization: $T212_AUTH_HEADER" \
  "${T212_BASE_URL}/api/v0/equity/account/summary"
```

当只设置了基本凭据时，可以使用 curl 中的内联格式：

```bash
# When only T212_API_KEY, T212_API_SECRET, T212_ENV are set:
curl -H "Authorization: Basic $(echo -n "$T212_API_KEY:$T212_API_SECRET" | base64)" \
  "https://${T212_ENV:-live}.trading212.com/api/v0/equity/account/summary"
```

> **警告：** `T212_AUTH_HEADER` 必须包含 `Basic` 前缀的完整头部信息。
>
> ```bash
> # WRONG - raw base64 without "Basic " prefix
> curl -H "Authorization: <base64-only>" ...  # This will NOT work!
>
> # CORRECT - use T212_AUTH_HEADER (contains "Basic <base64>")
> curl -H "Authorization: $T212_AUTH_HEADER" ...  # This works
> ```

### 环境变量

**单个账户 vs 所有账户：** API Key 仅适用于 **单个账户**。一组凭据（`T212_API_KEY` + `T212_API_SECRET`）对应一个账户（Invest 或 Stocks ISA）。如果要使用 **所有账户**（Invest 和 Stocks ISA），用户必须设置 **两组** 凭据：`T212_API_KEY_INVEST` / `T212_API_SECRET_INVEST` 和 `T212_API_KEY_stockS_ISA` / `T212_API_SECRET_stockS_ISA`。当设置了两组凭据时，用户必须明确指定目标账户；如果从上下文中无法判断，应在发起请求前确认（Invest 或 Stocks ISA）。

**单个账户的设置：** 为了与插件 README 保持一致，请设置这些凭据：

```bash
export T212_API_KEY="your-api-key"       # API Key (ID) from Trading 212
export T212_API_SECRET="your-api-secret"
export T212_ENV="demo"                   # or "live" (defaults to "live" if unset)
```

**特定账户的设置（Invest 和/或 Stocks ISA）：** 只需要设置实际使用的那组凭据。一组完整的凭据（同一账户的 Key + Secret）即可。例如，仅针对 Invest 账户：

```bash
export T212_API_KEY_INVEST="your-invest-api-key"
export T212_API_SECRET_INVEST="your-invest-api-secret"
export T212_ENV="demo"                   # or "live"
```

如果需要同时使用两个账户的凭据，请设置两组：

```bash
export T212_API_KEY_INVEST="your-invest-api-key"
export T212_API_SECRET_INVEST="your-invest-api-secret"
export T212_API_KEY_STOCKS_ISA="your-stocks-isa-api-key"
export T212_API_SECRET_STOCKS_ISA="your-stocks-isa-api-secret"
export T212_ENV="demo"                   # or "live" (applies to both)
```

**可选 – 预计算（适用于脚本或用户偏好）：** 用户可以从基本变量中设置认证头部和基本 URL，但通常不需要这样做；如果这些变量未设置，您（代理）必须根据基本变量构建头部和基本 URL。

```bash
# Build auth header and base URL from T212_API_KEY, T212_API_SECRET, T212_ENV
export T212_AUTH_HEADER="Basic $(echo -n "$T212_API_KEY:$T212_API_SECRET" | base64)"
export T212_BASE_URL="https://${T212_ENV:-live}.trading212.com"
```

**替代方案（手动设置）：** 如果不希望将凭据存储在环境变量中，可以直接设置相关的变量。**注意：API Key 仅适用于其对应的环境。**

```bash
# For DEMO (paper trading)
export T212_AUTH_HEADER="Basic $(echo -n "<DEMO_API_KEY_ID>:<DEMO_API_SECRET>" | base64)"
export T212_BASE_URL="https://demo.trading212.com"

# For LIVE (real money) - generate separate credentials in LIVE account
# export T212_AUTH_HEADER="Basic $(echo -n "<LIVE_API_KEY_ID>:<LIVE_API_SECRET>" | base64)"
# export T212_BASE_URL="https://live.trading212.com"
```

**提示：** 如果同时使用两种环境，请使用不同的变量名：

```bash
# Demo credentials
export T212_DEMO_AUTH_HEADER="Basic $(echo -n "<DEMO_KEY_ID>:<DEMO_SECRET>" | base64)"

# Live credentials
export T212_LIVE_AUTH_HEADER="Basic $(echo -n "<LIVE_KEY_ID>:<LIVE_SECRET>" | base64)"
```

### 常见认证错误

| 错误代码 | 原因                | 解决方案                                                                                      |
| ---- | -------------------- | --------------------------------------------------------------------------------------------- |
| 401  | 凭据无效              | 检查 API Key/Secret 是否正确，确保没有多余的空白字符              |
| 401  | 环境不匹配            | **实时 API Key 不能用于测试环境，反之亦然** - 确保 Key 与目标环境匹配 |
| 403  | 权限不足              | 检查 Trading 212 设置中的 API 权限              |
| 408  | 请求超时              | 重试请求                                                                                     |
| 429  | 超过速率限制            | 等待 `x-ratelimit-reset` 时间戳                        |

---

## 账户

### 获取账户概要

`GET /api/v0/equity/account/summary`（请求频率：1 次/5 秒）

```bash
curl -H "Authorization: $T212_AUTH_HEADER" \
  "$T212_BASE_URL/api/v0/equity/account/summary"
```

**响应格式：**

```json
{
  "id": 12345678,
  "currency": "GBP",
  "totalValue": 15250.75,
  "cash": {
    "availableToTrade": 2500.5,
    "reservedForOrders": 150.0,
    "inPies": 500.0
  },
  "investments": {
    "currentValue": 12100.25,
    "totalCost": 10500.0,
    "realizedProfitLoss": 850.5,
    "unrealizedProfitLoss": 1600.25
  }
}
```

### 账户字段

| 字段                              | 类型    | 描述                             |
| ---------------------------------- | ------- | --------------------------------------- |
| `id`                               | 整数 | 主要交易账户编号                          |
| `currency`                         | 字符串  | 主要账户货币（ISO 4217 标准）                   |
| `totalValue`                       | 数字    | 账户总价值（以主要货币计）                   |
| `cash.availableToTrade`            | 数字    | 可用于交易的现金                         |
| `cash.reservedForOrders`           | 数字    | 为待处理订单预留的现金                     |
| `cash.inPies`                      | 数字    | 未投资的现金（以 pies 为单位）                   |
| `investments.currentValue`         | 数字    | 所有投资的当前价值                      |
| `investments.totalCost`            | 数字    | 当前投资的成本基础                      |
| `investments.realizedProfitLoss`   | 数字    | 实现的利润和损失                      |
| `investments.unrealizedProfitLoss` | 数字    | 如果现在出售可能实现的利润和损失                |

---

## 订单

### 订单类型

| 类型      | 端点                           | 可用性 | 描述                          |
| --------- | ---------------------------------- | ------------ | ------------------------------------ |
| 市场订单    | `/api/v0/equity/orders/market`     | 测试 + 实时 | 立即以最佳价格执行                     |
| 限价订单    | `/api/v0/equity/orders/limit`      | 测试 + 实时 | 以限价或更优价格执行                     |
| 止损订单    | `/api/v0/equity/orders/stop`       | 测试 + 实时 | 当达到止损价格时执行                     |
| 止损限价订单 | `/api/v0/equity/orders/stop_limit` | 测试 + 实时 | 当达到止损限价时执行                     |

### 订单状态

| 状态             | 描述                             |
| ------------------ | --------------------------------------- |
| `LOCAL`            | 订单在本地创建，尚未发送                     |
| `UNCONFIRMED`      | 已发送至交易所，等待确认                     |
| `CONFIRMED`        | 交易所已确认                         |
| `NEW`              | 正在等待执行                         |
| `CANCELLING`       | 取消请求正在进行中                     |
| `CANCELLED`        | 取消请求成功                         |
| `PARTIALLY_FILLED`     | 部分成交                         |
| `FILLED`           | 完全成交                         |
| `REJECTED`         | 被交易所拒绝                         |
| `REPLACING`        | 修改订单正在进行中                     |
| `REPLACED`         | 订单已成功修改                         |

### 订单有效期

| 有效期              | 描述                                |
| ------------------ | ------------------------------------------ |
| `DAY`              | 在交易所时间午夜过期                         |
| `GOOD_TILL_CANCEL` | 有效直至取消                         |

### 订单策略

| 有效性              | 描述                                |
| ------------------ | ------------------------------------------ |
| `QUANTITY` | 按股票数量排序（API 支持）                   |
| `VALUE`    | 按货币价值排序（API 不支持）                   |

### 订单来源

| 来源        | 描述         | ------------------- |
| ------------ | ------------------- |
| `API`        | 通过此 API 发起                         |
| `IOS`        | iOS 应用                         |
| `ANDROID`    | Android 应用                         |
| `WEB`        | Web 平台                         |
| `SYSTEM`     | 系统自动生成                         |
| `AUTOINVEST` | 自动投资功能                         |

### 发起市场订单

`POST /api/v0/equity/orders/market`（请求频率：50 次/分钟）

**请求字段：**

| 字段           | 类型    | 是否必填 | 描述                                                                                                            |
| --------------- | ------- | -------- | -------------------------------------- |
| `ticker`        | 字符串      | 是         | 仪器 ticker（例如，`AAPL_US_EQ`）                         |
| `quantity`      | 数字      | 是         | 正数表示买入，负数表示卖出                     |
| `extendedHours` | 布尔值    | 是否允许在盘前（4:00-9:30 ET）和盘后（16:00-20:00 ET）时段执行 | 默认值：`false` |

**响应：**

```json
{
  "id": 123456789,
  "type": "MARKET",
  "ticker": "AAPL_US_EQ",
  "instrument": {
    "ticker": "AAPL_US_EQ",
    "name": "Apple Inc",
    "isin": "US0378331005",
    "currency": "USD"
  },
  "quantity": 5,
  "filledQuantity": 0,
  "status": "NEW",
  "side": "BUY",
  "strategy": "QUANTITY",
  "initiatedFrom": "API",
  "extendedHours": false,
  "createdAt": "2024-01-15T10:30:00Z"
}
```

### 发起限价订单

`POST /api/v0/equity/orders/limit`（请求频率：1 次/2 秒）

**请求字段：**

| 字段          | 类型   | 是否必填 | 描述                             |
| -------------- | ------ | -------- | --------------------------------------- |
| `ticker`       | 字符串      | 是         | 仪器 ticker                         |
| `quantity`     | 数字      | 是         | 正数表示买入，负数表示卖出                     |
| `limitPrice`   | 数字      | 最高价；负数表示最低价                     |
| `timeValidity` | 字符串      | 是否必填 | `DAY`（默认）或 `GOOD_TILL_CANCEL`                   |

### 发起止损订单

`POST /api/v0/equity/orders/stop`（请求频率：1 次/2 秒）

**请求字段：**

| 字段          | 类型   | 是否必填 | 描述                             |
| -------------- | ------ | -------- | --------------------------------------- |
| `ticker`       | 字符串      | 是         | 仪器 ticker                         |
| `quantity`     | 数字      | 是         | 正数表示买入，负数表示卖出                     |
| `stopPrice`    | 数字      | 触发止损的价格                     |
| `timeValidity` | 字符串      | 是否必填 | `DAY`（默认）或 `GOOD_TILL_CANCEL`                   |

### 发起止损限价订单

`POST /api/v0/equity/orders/stop_limit`（请求频率：1 次/2 秒）

**请求字段：**

| 字段          | 类型   | 是否必填 | 描述                             |
| -------------- | ------ | -------- | --------------------------------------- |
| `ticker`       | 字符串      | 是         | 仪器 ticker                         |
| `quantity`     | 数字      | 是         | 正数表示买入，负数表示卖出                     |
| `stopPrice`    | 数字      | 触发止损的价格                     |
| `limitPrice`   | 数字      | 最高价；限价订单的成交价格                     |
| `timeValidity` | 字符串      | 是否必填 | `DAY`（默认）或 `GOOD_TILL_CANCEL`                   |

### 获取待处理订单

`GET /api/v0/equity/orders`（请求频率：1 次/5 秒）

**返回值：** 包含状态为 NEW、PARTIALLY_FILLED 等的 Order 对象数组。

### 根据 ID 获取订单

`GET /api/v0/equity/orders/{id}`（请求频率：1 次/1 秒）

**请求频率：** 1 次/1 秒

### 取消订单

`DELETE /api/v0/equity/orders/{id}`（请求频率：50 次/分钟）

**返回值：** 如果取消请求成功，返回 200 OK。订单可能已经成交。

### 常见订单错误

| 错误代码 | 原因                   | 解决方案                            |
| ------------------------------ | ----------------------- | ----------------------------------- |
| `InsufficientFreeForStocksBuy` | 可用于购买的现金不足         | 检查 `cash.availableToTrade`                   |
| `SellingEquityNotOwned` | 出售的数量超过了持有的数量         | 检查 `quantityAvailableForTrading`                   |
| `MarketClosed`                 | 交易时间之外                         | 检查交易所的交易时间表                     |

---

## 持仓

### 获取所有持仓

`GET /api/v0/equity/positions`（请求频率：1 次/1 秒）

**查询参数：**

| 参数          | 类型   | 是否必填 | 描述                                      |
| -------------- | ------ | -------- | ---------------------------------------------- |
| `ticker`       | 字符串      | 不必填写 | 按特定 ticker 过滤（例如，`AAPL_US_EQ`）               |

**响应格式：**

```bash
# All positions
curl -H "Authorization: $T212_AUTH_HEADER" \
  "$T212_BASE_URL/api/v0/equity/positions"

# Filter by ticker
curl -H "Authorization: $T212_AUTH_HEADER" \
  "$T212_BASE_URL/api/v0/equity/positions?ticker=AAPL_US_EQ"
```

### 持仓字段

| 字段                               | 类型     | 描述                             |
| ----------------------------------- | -------- | ----------------------------------- |
| `quantity`                          | 数字      | 持有的总股数                         |
| `quantityAvailableForTrading`       | 数字      | 可用于交易的股数                         |
| `quantityInPies`                    | 数字      | 分配给 pies 的股数                         |
| `currentPrice`                      | 数字      | 当前价格（以货币计）                     |
| `averagePricePaid`                  | 数字      | 每股的平均成本                         |
| `createdAt`                         | 字符串      | 持仓创建日期                         |
| `walletImpact(currency`             | 字符串      | 账户货币                         |
| `walletImpact.totalCost`            | 数字      | 账户货币中的总成本                     |
| `walletImpact.currentValue`         | 数字      | 账户货币中的当前价值                     |
| `walletImpact.unrealizedProfitLoss` | 数字      | 账户货币中的未实现利润和损失                 |
| `walletImpact.fxImpact`             | 数字      | 货币汇率对价值的影响                     |

### 持仓数量示例

| 持仓情况            | 可用于交易的股数 | 分配给 pies 的股数         |
| ------------------- | -------- | --------------------------- | -------------- |
| 全部直接持有       | 10       | 10                              | 0                              |
| 部分在 pies 中       | 10       | 7                              | 3                              |
| 全部在 pies 中       | 10       | 0                              | 10                              |

**重要提示：** 在下达卖出订单之前，务必检查 `quantityAvailableForTrading` 的值。

---

## 仪器

### 查找仪器 ticker 的工作流程

当用户通过通用名称（如 “SAP”、“Apple”、“AAPL”）查找仪器时，**必须** 在下达任何订单、持仓或历史数据查询之前，先查找对应的 Trading 212 ticker。**切勿手动构造 ticker 格式**。

> **优先使用缓存：** 在调用 API 之前，务必检查 `/tmp/t212_instruments.json`。仪器端点的请求频率限制为 50 秒，每次请求返回的数据量约为 5MB。只有在缓存缺失或缓存时间超过 1 小时时，才需要调用 API。

**通用搜索：** 在三个相关字段（ticker、name 或 shortName）中匹配用户的搜索词。使用一个变量（例如 `SEARCH_TERM`），对每个字段执行 `test($q; "i")`，以便高效匹配 “TSLA”、“Tesla”、“TL0” 等名称。对于区域过滤（如 “美国股票”、“欧洲 SAP”），可以使用 ISIN 前缀（前两个字符）来表示国家代码，或在 grep 后添加 `currencyCode`。

> **重要提示：** **切勿自动选择仪器。** 如果存在多个选项，必须询问用户的偏好。

```bash
# SEARCH_TERM = user query (e.g. TSLA, Tesla, AAPL, SAP)
SEARCH_TERM="TSLA"
CACHE_FILE="/tmp/t212_instruments.json"
if [ -f "$CACHE_FILE" ] && [ $(($(date +%s) - $(stat -f %m "$CACHE_FILE" 2>/dev/null || stat -c %Y "$CACHE_FILE"))) -lt 3600 ]; then
  # Search ticker, name, or shortName fields
  jq --arg q "$SEARCH_TERM" '[.[] | select((.ticker // "" | test($q; "i")) or (.name // "" | test($q; "i")) or (.shortName // "" | test($q; "i")))]' "$CACHE_FILE"
else
  curl -s -H "Authorization: $T212_AUTH_HEADER" \
    "$T212_BASE_URL/api/v0/equity/metadata/instruments" > "$CACHE_FILE"
fi
```

### 获取所有仪器信息

`GET /api/v0/equity/metadata/instruments`（请求频率：1 次/50 秒）

**响应格式：**

```bash
curl -H "Authorization: $T212_AUTH_HEADER" \
  "$T212_BASE_URL/api/v0/equity/metadata/instruments"
```

### 仪器字段

| 字段               | 类型     | 描述                                 |
| ------------------- | -------- | ------------------------------------------- |
| `ticker`            | 字符串      | 仪器的唯一标识符                         |
| `name`              | 字符串      | 仪器的完整名称                         |
| `shortName`         | 字符串      | 简称（例如，AAPL）                         |
| `isin`              | 字符串      | 国际证券代码                         |
| `currencyCode`      | 字符串      | 交易货币（ISO 4217 标准）                     |
| `type`              | 字符串      | 仪器类型                         |
| `maxOpenQuantity`   | 数字      | 允许的最大持仓数量                     |
| `extendedHours`     | 布尔值    | 是否支持盘前（4:00-9:30 ET）和盘后（16:00-20:00 ET）交易         |
| `workingScheduleId` | 整数      | 交易所时间表的引用                         |
| `addedOn`           | 字符串      | 仪器添加到平台的日期                         |

### 仪器类型

| 类型             | 描述                           |
| ---------------- | ---------------------- |
| `STOCK`          | 普通股票                         |
| `ETF`            | 交易型开放式指数基金                     |
| `CRYPTOCURRENCY` | 加密货币                         |
| `CRYPTO`         | 加密资产                         |
| `FOREX`          | 外汇                         |
| `FUTURES`        | 期货合约                         |
| `INDEX`          | 指数                         |
| `WARRANT`        | 期权                         |
| `CVR`            | 条件价值权利                         |
| `CORPACT`        | 公司行动                         |

### ticker 格式

`{SYMBOL}_{EXCHANGE}_{TYPE}` - 例如：
- `AAPL_US_EQ` - 美国交易所的 Apple
- `VUSA_LSE_EQ` | 伦敦交易所的 Vanguard S&P 500
- `BTC_crypto` | Bitcoin                         |

### 获取交易所元数据

`GET /api/v0/equity/metadata/exchanges`（请求频率：1 次/30 秒）

**响应格式：**

```json
[
  {
    "id": 123,
    "name": "NASDAQ",
    "workingSchedules": [
      {
        "id": 456,
        "timeEvents": [
          { "type": "PRE_MARKET_OPEN", "date": "2024-01-15T09:00:00Z" },
          { "type": "OPEN", "date": "2024-01-15T14:30:00Z" },
          { "type": "CLOSE", "date": "2024-01-15T21:00:00Z" },
          { "type": "AFTER_HOURS_CLOSE", "date": "2024-01-15T01:00:00Z" }
        ]
      }
    ]
  }
]
```

### 时间事件类型

| 类型                | 描述                                 |
| ------------------- | -------------------------- |
| `PRE_MARKET_OPEN`   | 盘前交易开始                         |
| `OPEN`              | 正常交易开始                         |
| `BREAK_START`       | 交易休息开始                         |
| `BREAK_END`         | 交易休息结束                         |
| `CLOSE`             | 正常交易结束                         |
| `AFTER_HOURS_OPEN`  | 盘后交易开始                         |
| `AFTER_HOURS_CLOSE` | 盘后交易结束                         |
| `OVERNIGHT_OPEN`    | 隔夜交易开始                         |

---

## 历史数据

所有历史数据端点都支持基于游标的分页功能，使用 `nextPagePath` 进行分页。

### 分页参数

| 参数          | 类型          | 默认值 | 最大值 | 描述                                         |
| -------------- | ------------- | ------- | --------------------------------------------------------- |
| `limit`   | 整数       | 20      | 每页显示的项数                         |
| `cursor`  | 字符串/数字 | -       | 分页游标（用于 `nextPagePath`）                         |
| `ticker`  | 字符串      | -       | 根据 ticker 过滤请求                         |
| `time`    | 字符串      | -       | 分页时间（用于 `nextPagePath` 中的交易时间过滤）                         |

### 分页示例

```bash
#!/bin/bash
# Fetch all historical orders with pagination

NEXT_PATH="/api/v0/equity/history/orders?limit=50"

while [ -n "$NEXT_PATH" ]; do
  echo "Fetching: $NEXT_PATH"

  RESPONSE=$(curl -s -H "Authorization: $T212_AUTH_HEADER" \
    "$T212_BASE_URL$NEXT_PATH")

  # Process items (e.g., save to file)
  echo "$RESPONSE" | jq '.items[]' >> orders.json

  # Get next page path (null if no more pages)
  NEXT_PATH=$(echo "$RESPONSE" | jq -r '.nextPagePath // empty')

  # Wait 1 second between requests (50 req/min limit)
  if [ -n "$NEXT_PATH" ]; then
    sleep 1
  fi
done

echo "Done fetching all orders"
```

### 历史订单

`GET /api/v0/equity/history/orders`（请求频率：50 次/分钟）

**响应格式：**

```json
{
  "items": [
    {
      "order": {
        "id": 123456789,
        "type": "MARKET",
        "ticker": "AAPL_US_EQ",
        "instrument": {
          "ticker": "AAPL_US_EQ",
          "name": "Apple Inc",
          "isin": "US0378331005",
          "currency": "USD"
        },
        "quantity": 5,
        "filledQuantity": 5,
        "status": "FILLED",
        "side": "BUY",
        "createdAt": "2024-01-15T10:30:00Z"
      },
      "fill": {
        "id": 987654321,
        "type": "TRADE",
        "quantity": 5,
        "price": 185.5,
        "filledAt": "2024-01-15T10:30:05Z",
        "tradingMethod": "TOTV",
        "walletImpact": {
          "currency": "GBP",
          "fxRate": 0.79,
          "netValue": 732.72,
          "realisedProfitLoss": 0,
          "taxes": [
            { "name": "STAMP_DUTY", "quantity": 3.66, "currency": "GBP" }
          ]
        }
      }
    }
  ],
  "nextPagePath": "/api/v0/equity/history/orders?limit=50&cursor=1705326600000"
}
```

### 填单类型

| 类型                        | 描述                                 |
| --------------------------- | ------------------------- |
| `TRADE`                     | 正常交易执行                         |
| `STOCK_SPLIT`               | 股票拆分调整                         |
| `STOCK_DISTRIBUTION`        | 股票分配                         |
| `FOP`                       | 免费分配                         |
| `FOP_CORRECTION`            | FOP 更正                         |
| `CUSTOM_stock_DISTRIBUTION` | 自定义股票分配                         |
| `EQUITY_RIGHTS`             | 股权分配                         |

### 交易方式

| 类型        | 描述                                 |
| --------------------------- | ------------------------- |
| `TOTV`         | 在交易场所交易                         |
| `OTC`         | 场外交易                         |

### 税务类型（walletImpact.taxes）

| 类型                | 描述                                 |
| ------------------------- | -------------------------- |
| `COMMISSION_TURNOVER`     | 交易佣金                         |
| `CURRENCY_CONVERSION_FEE` | 货币兑换费                         |
| `FINRA_FEE`               | FINRA 交易活动费                         |
| `FRENCH_TRANSACTION_TAX` | 法国交易税                         |
| `PTM_LEVY`                | 收购税                         |
| `STAMP_DUTY`              | 英国印花税                         |
| `STAMP_DUTY_RESERVE_TAX` | 英国 SDRT                         |
| `TRANSACTION_FEE`         | 一般交易费                         |

### 历史股息

`GET /api/v0/equity/history/dividends`（请求频率：50 次/分钟）

**响应格式：**

```json
{
  "items": [
    {
      "ticker": "AAPL_US_EQ",
      "instrument": {
        "ticker": "AAPL_US_EQ",
        "name": "Apple Inc",
        "isin": "US0378331005",
        "currency": "USD"
      },
      "type": "ORDINARY",
      "amount": 12.5,
      "amountInEuro": 14.7,
      "currency": "GBP",
      "tickerCurrency": "USD",
      "grossAmountPerShare": 0.24,
      "quantity": 65.5,
      "paidOn": "2024-02-15T00:00:00Z",
      "reference": "DIV-123456"
    }
  ],
  "nextPagePath": null
}
```

### 股息类型

| 类型                          | 描述                                 |
| ----------------------------- | -------------------------- |
| `ORDINARY`                    | 常规股息                         |
| `BONUS`                       | 红利股息                         |
| `INTEREST`                    | 利息支付                         |
| `DIVIDEND`                    | 股息分配                         |
| `CAPITAL_GAINS`               | 资本收益分配                         |
| `RETURN_OF_CAPITAL`           | 资本返还                         |
| `PROPERTY_INCOME`             | 财产收入                         |
| `DEMERGER`                    | 合并分配                         |
| `QUALIFIED_INVESTMENT-entity` | 合并分配                         |

> **注：** 对于 1042-S 报告，还存在许多特定的美国税务类型。

### 账户交易

`GET /api/v0/equity/history/transactions`（请求频率：50 次/分钟）

**分页说明：**

- **首次请求：** 仅使用 `limit` 参数（无需使用 cursor 或 timestamp）。
- **后续请求：** 使用上一次请求返回的 `nextPagePath`，其中包含 cursor 和 timestamp。
- **时间过滤：** 无法按时间过滤交易记录——只能通过分页来浏览历史数据。

```bash
# First request - use only limit
curl -H "Authorization: $T212_AUTH_HEADER" \
  "$T212_BASE_URL/api/v0/equity/history/transactions?limit=50"
```

**响应格式：**

```json
{
  "items": [
    {
      "type": "DEPOSIT",
      "amount": 1000.0,
      "currency": "GBP",
      "dateTime": "2024-01-10T14:30:00Z",
      "reference": "TXN-123456"
    }
  ],
  "nextPagePath": null
}
```

### 交易类型

| 类型       | 描述                                 |
| ---------- | ---------------------------- |
| `DEPOSIT`      | 向账户存入资金                         |
| `WITHDRAW`      | 从账户提取资金                         |
| `FEE`      | 收取的费用                         |
| `TRANSFER`      | 内部转账                         |

### CSV 报告

**请求报告：** `POST /api/v0/equity/history/exports`（请求频率：1 次/30 秒）

**响应格式：**

```json
{
  "reportId": 12345
}
```

**查询报告状态：**

`GET /api/v0/equity/history/exports`（请求频率：1 次/分钟）

**响应格式：**

```bash
curl -H "Authorization: $T212_AUTH_HEADER" \
  "$T212_BASE_URL/api/v0/equity/history/exports"
```

**下载报告：**

```bash
# Get the download link from the response
DOWNLOAD_URL=$(curl -s -H "Authorization: $T212_AUTH_HEADER" \
  "$T212_BASE_URL/api/v0/equity/history/exports" | jq -r '.[0].downloadLink')

# Download the CSV file
curl -o trading212_report.csv "$DOWNLOAD_URL"
```

### 报告状态

| 状态       | 描述                               |
| ------------ | --------------------------------- |
| `Queued`     | 接收到报告请求                         |
| `Processing` | 正在生成报告                         |
| `Running`    | 报告正在生成                         |
| `Finished`   | 报告生成完成 - 提供下载链接                         |
| `Cancelled`   | 报告请求被取消                         |
| `Failed`     | 生成报告失败                         |

---

## 下单前的验证

### 买入前 - 检查可用资金

```bash
#!/bin/bash
# Validate funds before placing a buy order

TICKER="AAPL_US_EQ"
QUANTITY=10
ESTIMATED_PRICE=185.00
ESTIMATED_COST=$(echo "$QUANTITY * $ESTIMATED_PRICE" | bc)

# Get available funds
AVAILABLE=$(curl -s -H "Authorization: $T212_AUTH_HEADER" \
  "$T212_BASE_URL/api/v0/equity/account/summary" | jq '.cash.availableToTrade')

echo "Estimated cost: $ESTIMATED_COST"
echo "Available funds: $AVAILABLE"

if (( $(echo "$ESTIMATED_COST > $AVAILABLE" | bc -l) )); then
  echo "ERROR: Insufficient funds"
  exit 1
fi

echo "OK: Funds available, proceeding with order"
```

### 卖出前 - 检查可用股票数量

```bash
#!/bin/bash
# Validate position before placing a sell order

TICKER="AAPL_US_EQ"
SELL_QUANTITY=5

# Get position for the ticker
POSITION=$(curl -s -H "Authorization: $T212_AUTH_HEADER" \
  "$T212_BASE_URL/api/v0/equity/positions?ticker=$TICKER")

AVAILABLE_QTY=$(echo "$POSITION" | jq '.[0].quantityAvailableForTrading // 0')

echo "Sell quantity: $SELL_QUANTITY"
echo "Available to sell: $AVAILABLE_QTY"

if (( $(echo "$SELL_QUANTITY > $AVAILABLE_QTY" | bc -l) )); then
  echo "ERROR: Insufficient shares (some may be in pies)"
  exit 1
fi

echo "OK: Shares available, proceeding with order"
```

---

## 速率限制处理

### 理解速率限制

速率限制是针对 **每个账户** 的，而不是针对每个 API Key 或 IP 地址。如果多个应用程序使用同一个 Trading 212 账户，它们将共享相同的速率限制配额。

### 响应头部信息

每个 API 响应都包含速率限制相关的头部信息：

| 头部字段          | 描述                                 |
| ----------------------- | -------------------------------- |
| `x-ratelimit-limit`     | 指定时间内的总请求次数                     |
| `x-ratelimit-period`    | 时间周期（以秒为单位）                         |
| `x-ratelimit-remaining` | 剩余的请求次数                         |
| `x-ratelimit-reset`     | 速率限制重置的时间戳                         |
| `x-ratelimit-used`      | 已经发出的请求次数                         |

### 避免批量请求以避免触发速率限制

**不要一次性发送大量请求。** 即使某个端点允许每分钟发送 50 次请求，一次性发送所有请求也可能触发速率限制并影响性能。** 请均匀分配请求频率，例如每 1.2 秒发送一次请求，确保始终在限制范围内。

**错误做法（批量发送请求）：**

```bash
# DON'T DO THIS - sends all requests at once
for ticker in AAPL_US_EQ MSFT_US_EQ GOOGL_US_EQ; do
  curl -H "Authorization: $T212_AUTH_HEADER" \
    "$T212_BASE_URL/api/v0/equity/positions?ticker=$ticker" &
done
wait
```

**正确做法（均匀发送请求）：**

```bash
# DO THIS - space requests evenly
for ticker in AAPL_US_EQ MSFT_US_EQ GOOGL_US_EQ; do
  curl -H "Authorization: $T212_AUTH_HEADER" \
    "$T212_BASE_URL/api/v0/equity/positions?ticker=$ticker"
  sleep 1.2  # 1.2 second between requests for 50 req/m limit
done
```

### 缓存策略

对于不经常变化的数据，可以在本地缓存以减少 API 请求次数：

```bash
#!/bin/bash
# Cache instruments list (changes rarely)

CACHE_FILE="/tmp/t212_instruments.json"
CACHE_MAX_AGE=3600  # 1 hour

if [ -f "$CACHE_FILE" ]; then
  CACHE_AGE=$(($(date +%s) - $(stat -f %m "$CACHE_FILE")))
  if [ "$CACHE_AGE" -lt "$CACHE_MAX_AGE" ]; then
    cat "$CACHE_FILE"
    exit 0
  fi
fi

# Cache expired or doesn't exist - fetch fresh data
curl -s -H "Authorization: $T212_AUTH_HEADER" \
  "$T212_BASE_URL/api/v0/equity/metadata/instruments" > "$CACHE_FILE"

cat "$CACHE_FILE"
```

---

## 安全指南

1. **先在测试环境中测试** - 在进行实际交易之前，务必验证工作流程。
2. **下单前进行验证** - 买入前检查可用资金（`cash.availableToTrade`），卖出前检查可交易的股票数量（`quantityAvailableForTrading`）。
3. **确认具有破坏性的操作** - 下单和取消操作是不可逆的。
4. **API 不具备幂等性** - 重复请求可能会导致重复订单。
5. **切勿记录凭据** - 使用环境变量来存储凭据。
6. **遵守速率限制** - 均匀分配请求，避免批量发送。
7. **每个 ticker 和每个账户最多 50 个待处理订单**。
8. **缓存元数据** - 仪器和交易所的信息很少会发生变化。