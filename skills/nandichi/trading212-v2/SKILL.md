---
name: trading212
description: 该工具用于分析 Trading212 的投资组合，每日生成包含盈亏情况的总结以及表现最佳的/最差的资产列表；根据可配置的规则提出交易建议，并能够执行交易指令。此外，它还支持查看股息信息、订单历史记录、设置价格预警的功能，以及进行投资组合配置分析并提供建议（包括重新平衡投资组合的方案）。适用于用户需要了解投资组合状况、每日表现、交易操作情况或请求投资组合概览的场景。
metadata: {"openclaw":{"requires":{"bins":["python3"],"env":["TRADING212_API_KEY","TRADING212_API_SECRET"]},"primaryEnv":"TRADING212_API_KEY"}}
---
# Trading212 技能

该技能连接到 Trading212 API，提供投资组合分析、交易建议和订单执行功能。

**重要提示**：默认情况下，所有操作都在 **模拟交易**（paper-trading）环境中进行。只有当您确定用户希望使用真实资金进行交易时，才需要将 `TRADING212_DEMO` 设置为 `false`。

## 先决条件

请从技能的脚本目录中安装所需的依赖项：

```bash
pip install -r {baseDir}/requirements.txt
```

## 可用模式

### 1. summary -- 日度投资组合概览

```bash
python3 {baseDir}/scripts/trading212_skill.py --mode summary
```

返回结构化的 JSON 数据，包含以下内容：
- 投资组合总价值、现金余额、每日变动（欧元金额及百分比）
- 每个持仓的详细信息（数量、平均价格、当前价格、未实现的盈亏）
- 表现最佳的持仓和表现最差的持仓
- 重要事件（当天执行的订单、收到的股息）
- 多期业绩（1周、1个月、3个月、1年）

当用户询问“我的投资组合今天表现如何？”、“给我一个总结”或“我的投资组合发生了什么变化？”时，可以使用此模式。

以易于理解的英文形式呈现 JSON 输出结果。突出显示每日变动情况，列出表现最佳的持仓和表现最差的持仓，并说明重要事件。

### 2. propose -- 交易建议

```bash
python3 {baseDir}/scripts/trading212_skill.py --mode propose
python3 {baseDir}/scripts/trading212_skill.py --mode propose --risk low
python3 {baseDir}/scripts/trading212_skill.py --mode propose --risk high
```

返回一系列建议的交易操作（买入、卖出、减少持仓或持有持仓），同时提供相应的数量和理由。具体规则配置在 `config/rules.yaml` 文件中。

**活跃规则**：
- **减少持仓**：建议减少当天价格大幅下跌且权重较大的持仓
- **获利了结**：建议卖出未实现高收益的小持仓
- **定期定额投资买入**：在有足够现金时，建议买入定期定额投资列表中的股票
- **止损**：当价格跌至低于平均买入价时，建议卖出持仓
- **最大持仓比例限制**：当某个持仓的权重超过投资组合总权重上限时，建议减少该持仓
- **成本平均法**：当价格远低于平均买入价时，建议增加持仓
- **现金储备**：当现金余额低于投资组合的最低比例时，发出警告

当用户询问“我应该怎么做？”、“有什么交易建议吗？”或“我应该买入还是卖出什么？”时，可以使用此模式。

在执行任何交易建议之前，务必先征得用户的确认。切勿自动执行交易。

### 3. execute_trade -- 下单

```bash
python3 {baseDir}/scripts/trading212_skill.py --mode execute_trade --params '{"symbol":"AAPL_US_EQ","side":"buy","quantity":5,"order_type":"market"}'
```

参数（JSON 格式）：
- `symbol`（必填）：Trading212 的股票代码，例如 "AAPL_US_EQ"
- `side`（必填）："buy" 或 "sell"
- `quantity`（必填）：股票数量（正数）
- `order_type`："market"（默认）或 "limit"
- `limit_price`：当 `order_type` 为 "limit" 时必填

系统会自动进行交易前的验证：
- 买入订单：检查是否有足够的现金
- 卖出订单：检查是否持有足够的股票

**关键安全规则**：
1. 未经用户明确确认，切勿执行任何交易。
2. 在执行交易前，务必向用户明确显示将要执行的交易内容（股票代码、交易方向、数量和订单类型），并询问“是否要执行此订单？”
3. 如果 `TRADING212_DEMO` 为 `true`（默认值），需提醒用户这是在模拟交易环境中进行操作。
4. 如果 `TRADING212_DEMO` 为 `false`，需明确告知用户这是使用真实资金进行的交易。

### 4. dividends -- 股息信息

```bash
python3 {baseDir}/scripts/trading212_skill.py --mode dividends
```

返回结构化的 JSON 数据，包含以下内容：
- 收到的总股息（历史累计及过去12个月的股息）
- 每只股票的股息明细（包括总金额、最后一次支付日期和预估年收益率）
- 股息发放日历（每只股票的最近一次股息支付日期）

当用户询问“我收到了多少股息？”、“我的股息情况如何？”或“我的上次股息是什么时候发放的？”时，可以使用此模式。

### 5. history -- 订单历史

```bash
python3 {baseDir}/scripts/trading212_skill.py --mode history
python3 {baseDir}/scripts/trading212_skill.py --mode history --params '{"ticker":"AAPL_US_EQ","days":30}'
```

返回结构化的 JSON 数据，包含以下内容：
- 历史订单的总数
- 每只股票及整个投资组合的已实现盈亏
- 完整的订单列表（包含订单日期、价格和数量）

可选参数（JSON 格式）：
- `ticker`：按特定股票代码过滤订单
- `days`：仅显示过去 N 天内的订单

当用户询问“显示我的订单历史”或“我实现了多少利润？”或“我上个月交易了什么？”时，可以使用此模式。

### 6. watchlist -- 价格监控

```bash
python3 {baseDir}/scripts/trading212_skill.py --mode watchlist
```

读取 `config/watchlist.yaml` 文件，并检查每个股票的价格警报。返回以下信息：
- 监控列表中的股票及其当前价格（如果持有该股票）
- 触发的价格警报（价格高于或低于预设阈值）

在 `config/watchlist.yaml` 文件中配置监控列表：
```yaml
watchlist:
  - ticker: "NVDA_US_EQ"
    alert_below: 100.0
    alert_above: 150.0
```

当用户询问“查看我的监控列表”或“有什么价格警报？”或“我关注的股票表现如何？”时，可以使用此模式。

### 7. allocation -- 投资组合配置分析

```bash
python3 {baseDir}/scripts/trading212_skill.py --mode allocation
python3 {baseDir}/scripts/trading212_skill.py --mode allocation --rebalance
```

返回结构化的 JSON 数据，包含以下内容：
- 每个持仓的当前权重与目标配置的对比情况
- 每个持仓与目标配置的偏差
- 未达到目标配置的股票代码（在目标配置中但实际未持有的股票）
- 现金分配与目标配置的对比情况

使用 `--rebalance` 标志时，还会生成买入/卖出建议，以帮助用户调整投资组合配置。

在 `config/allocation.yaml` 文件中配置目标配置：
```yaml
target_allocation:
  "VWCE.UK": 40.0
  "IWDA.UK": 30.0
  _cash: 5.0
```

当用户询问“我的投资组合配置情况如何？”或“我的投资组合是否平衡？”或“我应该如何重新平衡投资组合？”时，可以使用此模式。

## 输出格式

所有模式都会以结构化的 JSON 格式将结果输出到标准输出（stdout）。解析这些数据后，以易于理解的英文形式向用户呈现结果。

## 额外资源

有关完整的输出格式和 API 详细信息，请参阅 [reference.md](reference.md)。