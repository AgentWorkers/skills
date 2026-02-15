# Kraken Crypto Skill

使用 `kraken_cli.py` 包装器来查询您的 Kraken 账户信息。

## 设置

导出您的 Kraken API 凭据。

```bash
export KRAKEN_API_KEY="your_api_key"
export KRAKEN_API_SECRET="your_api_secret"
```

您还可以在技能目录下创建一个 `.env` 文件来存储这些凭据。

## 1. 主要命令

使用以下命令查询您的投资组合信息。这些命令会自动计算各项数据的总和：

| 命令 | 描述 |
|---------|-------------|
| summary | 显示投资组合概览及各项资产的总价值 |
| net-worth | 计算您的净资产 |
| performance | 显示投资回报与存款金额的对比情况 |
| holdings | 显示资产明细（以美元计价） |
| staking | 显示您的质押位置及奖励情况 |

### 示例输出（summary 命令的输出）

```
TOTAL NET WORTH
  Main Wallet (Equity):    $544.95
  Earn Wallet (Bonded):    $81.89
  TOTAL:                   $626.84

AUTO EARN (Flexible) in Main Wallet
  BTC   : $493.92 (rewards: $0.03)
  ETH   : $50.66 (rewards: $0.11)

BONDED STAKING in Earn Wallet
  SOL   : $66.73 (rewards: $0.89)
  DOT   : $15.16 (rewards: $0.55)

  Total Staking Rewards:   $1.71
```

该包装器会区分“自动收益”（Auto Earn）和“绑定质押”（Bonded Staking）类型，以避免数据重复计算。

## 2. 原始 API 命令

这些命令通过 `kraken_api.py` 来获取更详细的数据。适用于需要获取主要命令未涵盖的信息：

### 公开市场数据

| 命令 | 描述 | 使用场景 |
|---------|-------------|----------|
| ticker --pair XXBTZUSD | 获取 XXBTZUSD 的当前价格及 24 小时交易数据 | 价格查询 |
| ohlc --pair XXBTZUSD | 获取 XXBTZUSD 的历史交易数据（K线图） | 图表数据查询 |
| depth --pair XXBTZUSD | 获取 XXBTZUSD 的订单簿信息 | 流动性分析 |
| recent-trades --pair XXBTZUSD | 获取 XXBTZUSD 的实时交易记录 | 市场活动查询 |
| assets | 获取所有资产名称及其相关信息 | 资产信息查询 |
| pairs | 获取可交易的货币对列表 | 货币对信息查询 |
| status | 获取交易所状态 | 连接状态检查 |
| time | 获取服务器时间 | API 运行状态检查 |

### 私有账户数据

| 命令 | 描述 | 使用场景 |
|---------|-------------|----------|
| balance | 获取资产原始数量 | 资产明细 |
| balance-ex | 获取包含预留资金的账户余额 | 杠杆分析 |
| portfolio | 获取以美元计价的交易余额 | 股权数据查询 |
| open-orders | 获取未成交订单 | 订单管理 |
| closed-orders | 获取已成交订单 | 订单历史记录 |
| trades | 获取交易执行历史 | 交易分析 |
| ledger | 获取所有交易记录 | 交易追踪 |
| ledger --asset ZUSD | 按资产类型筛选交易记录 | 资产历史记录 |
| volume | 获取过去 30 天的交易量 | 手续费等级信息 |

### 私有收益数据

| 命令 | 描述 | 使用场景 |
| earn-positions | 获取质押分配详情 | 抽象数据查询 |
| earn-strategies | 获取可用的收益计划 | 收益策略查询 |
| earn-status | 查看待处理的质押操作 | 抽象数据查询 |
| earn-dealloc-status --refid ID | 查看待解除的质押操作 | 抽象数据查询 |

### 资金管理相关命令

| 命令 | 描述 | 使用场景 |
|---------|-------------|----------|
| deposits-methods | 获取可用的存款方式 | 存款选项查询 |
| deposits-address --asset BTC | 获取 BTC 现金账户地址 | 接收加密货币 |

## 3. 重要注意事项

### 数据重复计算警告

请勿将 `balance`（账户余额）与 `earn-positions`（质押收益）相加：

Kraken 提供两种质押方式：
- **自动收益**：相关资产保留在主钱包中，计入投资组合的净资产。
- **绑定质押**：相关资产会被转移到收益钱包中，不计入投资组合的净资产。

`summary` 命令会正确处理这种差异。如果您手动使用原始 API 命令，请遵循以下逻辑：
- 正确的计算方法是：总资产 = 投资组合净资产 + 仅限绑定质押的收益。
- 错误的计算方法是：总资产 = 投资组合净资产 + 所有质押收益的总额。

### API 响应说明

- `ohlc` 命令的返回结果会以 `pair` 为键存储在列表中。
- `depth` 命令的买卖报价信息会嵌套在 `pair` 键下。
- `recent-trades` 命令的返回结果是一个包含价格、成交量、时间、交易方向、交易类型等信息的列表。
- `earn-strategies` 命令使用 `items` 键来获取收益相关信息（例如年利率 `apr_estimate`）。

## 4. 使用示例

| 用户请求 | 机器人操作 |
|--------------|------------|
| 我的投资组合是什么？ | 执行 `summary` 命令 |
| 我的净资产是多少？ | 执行 `net-worth` 命令 |
| 我的投资表现如何？ | 执行 `performance` 命令 |
| 显示我的资产持有情况 | 执行 `holdings` 命令 |
| 显示我的质押情况 | 执行 `staking` 命令 |
| BTC 的价格是多少？ | 执行 `ticker --pair XXBTZUSD` 命令 |
| 显示我的未成交订单 | 执行 `open-orders` 命令 |
| 显示我的交易历史 | 执行 `trades` 命令 |
| 获取我的 BTC 存款地址 | 执行 `deposits-address --asset BTC` 命令 |

## 5. 所需的 API 密钥权限

| 功能 | 所需权限 |
|---------|------------|
| 账户余额和投资组合信息 | 查询资金信息 |
| 订单、交易及交易记录 | 查询资金信息 |
| 抽象收益数据 | 访问收益相关数据 |
| 存款信息 | 查询资金信息 |
| 市场数据 | 无特殊权限要求 |