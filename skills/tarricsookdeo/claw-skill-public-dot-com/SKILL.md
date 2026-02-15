---
id: public-dot-com
name: public.com
description: 您可以使用 Public.com API 来操作您的 Public.com 经纪账户。该 API 允许您查看投资组合、获取股票报价、执行交易以及接收账户更新信息。如需创建 Public.com 账户，请访问 public.com/signup。
env: ['PUBLIC_COM_SECRET', 'PUBLIC_COM_ACCOUNT_ID']
license: Apache-2.0
metadata:
  author: PublicDotCom
  source: https://github.com/PublicDotCom/claw-skill-public-dot-com
  category: "Finance"
  tags: ["investing", "stocks", "crypto", "options", "public", "finance"]
  version: "1.0"
---

# Public.com 账户管理器  
> **免责声明：** 本文档仅用于说明和信息提供目的，不构成投资建议或推荐。  

> 我们建议在尽可能独立的实例中运行此功能。如果可能的话，也请在新创建的 Public.com 账户上测试其集成效果。  

此功能允许用户与其 Public.com 经纪账户进行交互。  

## 先决条件  
- **Python 3.8+** 和 **pip** — 必需在您的 OpenClaw 环境中安装。  
- **Public.com 账户** — 请访问 https://public.com/signup 创建一个账户。  
- **Public.com API 密钥** — 请访问 https://public.com/settings/v2/api 获取 API 密钥。  

需要 `publicdotcom-py` SDK。该 SDK 会在首次运行时自动安装，或者您可以手动安装：  
```bash
pip install publicdotcom-py
```  

## 配置  
此功能使用两个环境变量：`PUBLIC_COM_SECRET`（必填）和 `PUBLIC_COM_ACCOUNT_ID`（可选）。它们的获取顺序如下：  
1. **安全文件**：`~/.openclaw/workspace/.secrets/public_com_secret.txt`（或 `public_com_account.txt`）  
2. **环境变量**：`PUBLIC_COM_SECRET` / `PUBLIC_COM_ACCOUNT_ID`  

通过 `openclaw config set` 设置值会自动写入安全文件中。  

### API 密钥（必填）  
如果未设置 `PUBLIC_COM_SECRET`：  
- 告知用户：“我需要您的 Public.com API 密钥。您可以在 https://public.com/settings/v2/api 的开发者设置中找到它。”  
- 获取密钥后，保存为：`openclaw config set skills.publicdotcom.PUBLIC_COM_SECRET [VALUE]`  

### 默认账户 ID（可选）  
如果用户希望为所有请求设置默认账户：  
- 保存为：`openclaw config set skills.publicdotcom.PUBLIC_COM_ACCOUNT_ID [VALUE]`  
- 这样就不需要在每个命令中指定 `--account-id` 了。  

## 可用命令  

### 获取账户信息  
当用户请求“获取我的账户”、“列出账户”或“显示我的 Public.com 账户”时：  
1. 执行 `python3 scripts/get_accounts.py`  
2. 将账户 ID 和类型返回给用户。  

### 获取投资组合信息  
当用户请求“获取我的投资组合”、“显示我的持仓”或“我的账户里有什么”时：  
1. 如果设置了 `PUBLIC_COM_ACCOUNT_ID`，执行 `python3 scripts/get_portfolio.py`（无需参数）。  
2. 如果未设置且不知道用户的账户 ID，先运行 `get_accounts.py` 获取账户 ID。  
3. 执行 `python3 scripts/get_portfolio.py --account-id [ACCOUNT_ID]`  
4. 将投资组合概要（股票、可用资金、持仓情况）返回给用户。  

### 获取订单信息  
当用户请求“获取我的订单”、“显示我的订单”、“查看活跃订单”或“查看待处理订单”时：  
1. 如果设置了 `PUBLIC_COM_ACCOUNT_ID`，执行 `python3 scripts/get_orders.py`（无需参数）。  
2. 如果未设置且不知道用户的账户 ID，先运行 `get_accounts.py` 获取账户 ID。  
3. 执行 `python3 scripts/get_orders.py --account-id [ACCOUNT_ID]`  
4. 将活跃订单的详细信息（股票代码、方向、类型、状态、数量、价格）返回给用户。  

### 获取交易历史记录  
当用户请求“获取我的交易历史”、“显示我的交易记录”、“交易历史”或查看过去的账户活动时：  
**可选参数：**  
- `--type`：按交易类型过滤（TRADE、MONEY_MOVEMENT、POSITION_ADJUSTMENT）  
- `--limit`：限制返回的交易数量  

**示例：**  
获取所有交易历史记录：  
```bash
python3 scripts/get_history.py
```  
仅获取交易记录：  
```bash
python3 scripts/get_history.py --type TRADE
```  
仅获取资金变动记录（存款、取款、股息、费用）：  
```bash
python3 scripts/get_history.py --type MONEY_MOVEMENT
```  
获取最近 10 笔交易：  
```bash
python3 scripts/get_history.py --limit 10
```  
使用明确的账户 ID：  
```bash
python3 scripts/get_history.py --account-id YOUR_ACCOUNT_ID
```  

**工作流程：**  
1. 如果未设置 `PUBLIC_COM_ACCOUNT_ID` 且不知道用户的账户 ID，先运行 `get_accounts.py` 获取账户 ID。  
2. 执行：`python3 scripts/get_history.py [OPTIONS]`  
3. 按类型（交易、资金变动、持仓调整）分组显示交易历史记录。  
4. 包括股票代码、数量、净金额、费用和时间戳等详细信息。  

**交易类型：**  
- **TRADE**：股票、期权和加密货币的买卖交易  
- **MONEY_MOVEMENT**：存款、取款、股息、费用和现金调整  
- **POSITION_ADJUSTMENT**：股票分割、合并和其他持仓变动  

### 获取报价  
当用户请求“获取报价”、“查看价格”或查询股票/加密货币价格时：  
**格式：** `SYMBOL` 或 `SYMBOL:TYPE`（类型默认为 EQUITY）  

**示例：**  
获取单只股票的报价（使用默认账户）：  
```bash
python3 scripts/get_quotes.py AAPL
```  
获取多只股票的报价：  
```bash
python3 scripts/get_quotes.py AAPL GOOGL MSFT
```  
获取多种类型的报价：  
```bash
python3 scripts/get_quotes.py AAPL:EQUITY BTC:CRYPTO
```  
获取期权报价：  
```bash
python3 scripts/get_quotes.py AAPL260320C00280000:OPTION
```  
使用明确的账户 ID：  
```bash
python3 scripts/get_quotes.py AAPL --account-id YOUR_ACCOUNT_ID
```  

**工作流程：**  
1. 如果未设置 `PUBLIC_COM_ACCOUNT_ID` 且不知道用户的账户 ID，先运行 `get_accounts.py` 获取账户 ID。  
2. 解析用户的请求（股票代码和类型）。  
3. 执行：`python3 scripts/get_quotes.py [SYMBOLS...] [--account-id ACCOUNT_ID]`  
4. 将报价信息（最新价格、买入价、卖出价、成交量等）返回给用户。  

### 获取可交易工具信息  
当用户请求“列出可交易的工具”、“查看可交易的股票”或查看可交易的工具时：  
**可选参数：**  
- `--type`：可交易的工具类型（EQUITY、OPTION、CRYPTO）。默认为 EQUITY。  
- `--trading`：交易状态过滤（BUY_AND_SELL、BUY_ONLY、SELL_ONLY、NOT_TRADABLE）  
- `--search`：按股票代码或名称搜索  
- `--limit`：限制结果数量  

**示例：**  
列出所有股票：  
```bash
python3 scripts/get_instruments.py
```  
列出股票和加密货币：  
```bash
python3 scripts/get_instruments.py --type EQUITY CRYPTO
```  
仅列出可交易的工具：  
```bash
python3 scripts/get_instruments.py --type EQUITY --trading BUY_AND_SELL
```  
搜索特定工具：  
```bash
python3 scripts/get_instruments.py --search AAPL
```  
限制结果数量：  
```bash
python3 scripts/get_instruments.py --limit 50
```  

**工作流程：**  
1. 解析用户的请求（类型、交易状态、搜索词）。  
2. 执行：`python3 scripts/get_instruments.py [OPTIONS]`  
3. 将可交易的工具及其交易状态返回给用户。  

### 获取工具详细信息  
当用户请求“获取工具详细信息”、“显示 AAPL 的详细信息”或查看特定工具的详细信息时：  
**必填参数：**  
- `--symbol`：股票代码（例如：AAPL、BTC）  

**可选参数：**  
- `--type`：工具类型（EQUITY、OPTION、CRYPTO）。默认为 EQUITY。  

**示例：**  
获取股票工具的详细信息：  
```bash
python3 scripts/get_instrument.py --symbol AAPL
```  
获取加密货币工具的详细信息：  
```bash
python3 scripts/get_instrument.py --symbol BTC --type CRYPTO
```  

**工作流程：**  
1. 解析用户的请求（股票代码和可选类型）。  
2. 执行：`python3 scripts/get_instrument.py --symbol [SYMBOL] [--type TYPE]`  
3. 将工具的详细信息（交易状态、是否可分割交易、期权交易等）返回给用户。  

### 获取期权到期日  
**此功能可以列出任何股票的所有可用期权到期日。**  
当用户请求“获取期权到期日”、“列出到期日”、“显示到期日”或想知道某只股票的期权到期日时：  
1. 执行 `python3 scripts/get_option_expirations.py [SYMBOL]`  
2. 将可用到期日返回给用户。  

**常见用户指令：**  
- “获取 AAPL 的期权到期日”  
- “Google 的期权到期日是什么？”  
- “TSLA 的期权何时到期？”  
- “显示 SPY 期权的到期日”  
- “列出 MSFT 的可用到期日”  
- “能获取 Apple 的期权到期日吗？”  
- “NVDA 的期权到期日有哪些？”  

**必填参数：**  
- `symbol`：标的股票代码（例如：AAPL、GOOGL、TSLA、SPY）。  
**示例：**  
```bash
python3 scripts/get_option_expirations.py AAPL
python3 scripts/get_option_expirations.py GOOGL
python3 scripts/get_option_expirations.py TSLA
python3 scripts/get_option_expirations.py SPY
```  

**常见公司名称与股票代码的对应关系：**  
- Apple = AAPL  
- Google/Alphabet = GOOGL  
- Tesla = TSLA  
- Microsoft = MSFT  
- Amazon = AMZN  
- Nvidia = NVDA  
- Meta/Facebook = META  

**工作流程：**  
1. 从用户请求中提取股票代码。将公司名称转换为股票代码。  
2. 执行：`python3 scripts/get_option_expirations.py [SYMBOL]`  
3. 将可用到期日返回给用户。  
4. 如果用户想查看期权链，可以使用 `get_option_chain.py`。  

### 获取期权希腊值  
当用户请求“获取期权希腊值”（Delta、Gamma、Theta、Vega）或分析期权时：  
**必填参数：**  
- 一个或多个 OSI 期权代码（例如：AAPL260116C00270000）  

**OSI 期权代码格式：**  
```
AAPL260116C00270000
^^^^------^--------
|   |     |  Strike price ($270.00)
|   |     Call (C) or Put (P)
|   Expiration (Jan 16, 2026 = 260116)
Underlying symbol
```  
**示例：**  
获取单个期权的希腊值：  
```bash
python3 scripts/get_option_greeks.py AAPL260116C00270000
```  
获取多个期权（例如，相同执行价的看涨和看跌期权）：  
```bash
python3 scripts/get_option_greeks.py AAPL260116C00270000 AAPL260116P00270000
```  

**工作流程：**  
1. 如果用户提供了到期日、执行价和看涨/看跌期权类型，帮助用户构建 OSI 期权代码。  
2. 执行：`python3 scripts/get_option_greeks.py [OSI_SYMBOLS...]`  
3. 将希腊值（Delta、Gamma、Theta、Vega、Rho、IV）及其解释返回给用户。  

### 获取期权链  
当用户请求“获取期权链”、“获取 AAPL 的期权链”或查看可用期权时：  
**必填参数：**  
- `symbol`：标的股票代码（例如：AAPL）  
**可选参数：**  
- `--expiration`：到期日（YYYY-MM-DD）。如果未提供，使用最近的到期日。  
- `--list-expirations`：列出所有可用到期日。  

**示例：**  
列出所有可用到期日：  
```bash
python3 scripts/get_option_chain.py AAPL --list-expirations
```  
获取最近到期日的期权链：  
```bash
python3 scripts/get_option_chain.py AAPL
```  
获取特定到期日的期权链：  
```bash
python3 scripts/get_option_chain.py AAPL --expiration 2026-03-20
```  

**工作流程：**  
1. 如果用户未指定到期日，先使用 `--list-expirations` 显示可用到期日。  
2. 执行：`python3 scripts/get_option_chain.py [SYMBOL] [--expiration DATE]`  
3. 返回看涨和看跌期权的执行价、买入价/卖出价、成交量和未平仓量。  

### 设置默认账户  
当用户请求“设置我的默认账户”或“将账户 X 设置为默认账户”时：  
1. 保存设置：`openclaw config set skills.publicdotcom.PUBLIC_COM_ACCOUNT_ID [ACCOUNT_ID]`  
2. 确认用户未来将使用此账户作为默认账户。  

### 预订单计算  
当用户请求“估算订单成本”、“预订单”、“购买成本是多少”或想在下单前查看预估成本和账户影响时：  
**必填参数：**  
- `--symbol`：股票代码（例如：AAPL、BTC 或期权代码如 NVDA260213P00177500）  
- `--type`：EQUITY、OPTION 或 CRYPTO  
- `--side`：BUY 或 SELL  
- `--order-type`：LIMIT、MARKET、STOP 或 STOP_LIMIT  
- `--quantity` 或 `--amount`：股票数量/合约数量或名义金额  

**条件参数：**  
- `--limit-price`：LIMIT 和 STOP_LIMIT 订单必需  
- `--stop-price`：STOP 和 STOP_LIMIT 订单必需  
- `--session`：CORE（默认）或 EXTENDED（适用于股票订单）  
- `--open-close`：OPEN（用于开新仓）或 CLOSE（用于平仓）（适用于期权订单）  
- `--time-in-force`：DAY（默认）或 GTC（Good Till Cancelled）  

**示例：**  
预订单：买入 AAPL 的股票（限价）：  
```bash
python3 scripts/preflight.py --symbol AAPL --type EQUITY --side BUY --order-type LIMIT --quantity 10 --limit-price 227.50
```  
预订单：卖出 AAPL（市价）：  
```bash
python3 scripts/preflight.py --symbol AAPL --type EQUITY --side SELL --order-type MARKET --quantity 10
```  
预订单：买入加密货币（按金额）：  
```bash
python3 scripts/preflight.py --symbol BTC --type CRYPTO --side BUY --order-type MARKET --amount 100
```  
预订单：买入期权合约（开新仓）：  
```bash
python3 scripts/preflight.py --symbol NVDA260213P00177500 --type OPTION --side BUY --order-type LIMIT --quantity 1 --limit-price 4.00 --open-close OPEN
```  
预订单：卖出期权合约（平仓）：  
```bash
python3 scripts/preflight.py --symbol NVDA260213P00177500 --type OPTION --side SELL --order-type LIMIT --quantity 1 --limit-price 5.00 --open-close CLOSE
```  

**工作流程：**  
1. 从用户处收集订单参数（股票代码、类型、方向、订单类型、数量/金额）。  
2. 执行：`python3 scripts/preflight.py [OPTIONS]`  
3. 将预估成本、购买影响和费用返回给用户。  
4. 如果用户同意，使用 `place_order.py` 脚本执行订单。  

### 下单  
当用户请求“买入”、“卖出”或“下单”时：  
**必填参数：**  
- `--symbol`：股票代码（例如：AAPL、BTC）  
- `--type`：EQUITY、OPTION 或 CRYPTO  
- `--side`：BUY 或 SELL  
- `--order-type`：LIMIT、MARKET、STOP 或 STOP_LIMIT  
- `--quantity` 或 `--amount`：股票数量或名义金额  

**条件参数：**  
- `--limit-price`：LIMIT 和 STOP_LIMIT 订单必需  
- `--stop-price`：STOP 和 STOP_LIMIT 订单必需  
- `--session`：CORE（默认）或 EXTENDED（适用于股票订单）  
- `--open-close`：OPEN（用于开新仓）或 CLOSE（用于平仓）（适用于期权订单）  
- `--time-in-force`：DAY（默认）或 GTC（Good Till Cancelled）  

**示例：**  
以限价 $227.50 买入 10 股 AAPL：  
```bash
python3 scripts/place_order.py --symbol AAPL --type EQUITY --side BUY --order-type LIMIT --quantity 10 --limit-price 227.50
```  
以市价卖出 $500 的 AAPL：  
```bash
python3 scripts/place_order.py --symbol AAPL --type EQUITY --side SELL --order-type MARKET --amount 500
```  
以扩展时段买入加密货币：  
```bash
python3 scripts/place_order.py --symbol BTC --type CRYPTO --side BUY --order-type MARKET --amount 100
```  
使用 GTC（Good Till Cancelled）订单买入加密货币：  
```bash
python3 scripts/place_order.py --symbol AAPL --type EQUITY --side BUY --order-type LIMIT --quantity 10 --limit-price 220.00 --time-in-force GTC
```  

**工作流程：**  
1. 从用户处收集所有所需信息（股票代码、方向、订单类型、数量/金额）。  
2. 在执行前与用户确认订单详情。  
3. 执行：`python3 scripts/place_order.py [OPTIONS]`  
4. 将订单 ID 和确认信息返回给用户。  
5. 提醒用户订单是异步处理的——他们可以稍后查看订单状态。  

### 取消订单  
当用户请求“取消订单”或取消特定订单时：  
**必填参数：**  
- `--order-id`：要取消的订单 ID  

**示例：**  
```bash
python3 scripts/cancel_order.py --order-id 345d3e58-5ba3-401a-ac89-1b756332cc94
```  
**使用明确的账户 ID：**  
```bash
python3 scripts/cancel_order.py --order-id 345d3e58-5ba3-401a-ac89-1b756332cc94 --account-id YOUR_ACCOUNT_ID
```  

**工作流程：**  
1. 如果用户未提供订单 ID，先运行 `get_orders.py` 显示其活跃订单。  
2. 与用户确认要取消的订单。  
3. 执行：`python3 scripts/cancel_order.py --order-id [ORDER_ID]`  
4. 告知用户取消操作是异步的——他们需要查看订单状态以确认取消结果。  

### 期权策略指导  
当用户询问期权策略、如何自动化策略、在特定情况下使用哪种策略或需要帮助构建多腿期权交易时：  
1. 阅读位于同一目录下的 `options-automation-library.md` 文件，其中包含详细的策略说明。  
2. 该库包含 35 种以上的期权策略，按类别分类：  
   - **单腿策略**：长期看涨、长期看跌、保护性看涨、现金担保看跌  
   - **垂直价差**：牛市看涨、熊市看涨、牛市看跌、熊市看跌  
   - **日历和对角价差**：长期日历价差、对角价差  
   - **跨式和勒式**：长期/短期跨式、长期/短期勒式  
   - **复杂价差**：铁秃鹫、铁蝴蝶、碎翼蝴蝶、圣诞树  
   - **合成头寸**：合成长期/短期、合成保护性看涨、转换/反转  
   - **收益策略**：轮盘式、穷人保护性看涨、比率价差  
   - **高级/量化策略**：箱式价差、风险反转、对冲铁蝶式、波动率套利、日历价差  
   - **事件驱动策略**：收益波动率挤压、盘前波动率扩张、盘后波动率波动  
3. 每个策略都包含：描述、使用场景及示例、策略失效条件、API 工作流程步骤以及使用 Public.com SDK 的代码示例。  
4. 在编写代码示例时，使用库中的辅助工具（Setup、Market Data、Preflight、Multi-leg order helpers）。  
5. 推荐策略时，务必提供“该策略的失效条件”，以便用户了解风险。  
6. 对于可执行的交易，将库中的代码模式映射到此技能中的实际脚本（例如：`get_option_chain.py`、`get_option_expirations.py`、`preflight.py`、`place_order.py`）。