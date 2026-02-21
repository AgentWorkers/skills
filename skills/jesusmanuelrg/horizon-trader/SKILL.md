---
name: horizon-trader
version: 0.4.16
description: "v0.4.16 - 交易预测市场（Polymarket、Kalshi）：支持管理持仓、订单、进行风险管理；提供Kelly投资策略计算工具、钱包分析功能；包含蒙特卡洛模拟、套利分析、定量分析工具；支持AFML（自动市场建模与标签生成）、分数阶微分算法、HRP（高分辨率处理）以及去噪技术；支持多策略协同执行；包含阿尔法策略研究功能；具备分层访问控制机制以及市场探索功能。"
emoji: "\U0001F4C8"
metadata:
  openclaw:
    requires:
      env:
        - HORIZON_API_KEY
    primaryEnv: HORIZON_API_KEY
    install:
      - id: pip
        kind: uv
        formula: horizon-sdk
        label: "Horizon SDK (pip install horizon-sdk)"
    homepage: https://docs.openclaw.ai/tools/clawhub
---
# Horizon Trader

您是一个由 Horizon SDK 支持的预测市场交易助手。

## 何时使用此功能

当用户询问以下内容时，请使用此功能：
- 查看他们的 **持仓**、**盈亏** 或 **投资组合状态**
- 在预测市场上 **提交** 或 **取消** 订单
- 在 Polymarket 或 Kalshi 上 **查找** 或 **搜索** 市场或事件
- 计算 **Kelly 最优** 持仓规模
- 管理 **风险** 控制（止损、止盈等）
- 查看 **行情** 价格或市场数据
- 在 Polymarket 上查询 **钱包** 活动、交易、持仓或个人资料
- 分析某个市场的 **交易流量** 或 **主要持有者**
- 对投资组合风险进行 **蒙特卡洛模拟**
- 执行 **跨交易所套利**
- 与 **预测市场交易** 相关的任何操作

## 使用方法

通过 CLI 脚本运行命令。所有输出均为 JSON 格式。

```bash
python3 {baseDir}/scripts/horizon.py <command> [args...]
```

## 可用命令

### 投资组合与状态
```bash
# Engine status: PnL, open orders, positions, kill switch, uptime
python3 {baseDir}/scripts/horizon.py status

# List all open positions
python3 {baseDir}/scripts/horizon.py positions

# List open orders (optionally for a specific market)
python3 {baseDir}/scripts/horizon.py orders [market_id]

# List recent fills
python3 {baseDir}/scripts/horizon.py fills
```

### 交易
```bash
# Submit a limit order: quote <market_id> <side> <price> <size> [market_side]
# side: buy or sell, price: 0-1 (probability), market_side: yes or no (default: yes)
python3 {baseDir}/scripts/horizon.py quote <market_id> buy 0.55 10
python3 {baseDir}/scripts/horizon.py quote <market_id> sell 0.40 5 no

# Cancel a single order
python3 {baseDir}/scripts/horizon.py cancel <order_id>

# Cancel all orders
python3 {baseDir}/scripts/horizon.py cancel-all

# Cancel all orders for a specific market
python3 {baseDir}/scripts/horizon.py cancel-market <market_id>
```

### 市场搜索
```bash
# Search for markets on an exchange
python3 {baseDir}/scripts/horizon.py discover <exchange> [query] [limit] [market_type] [category]
# market_type: "all" (default), "binary", or "multi"
# category: tag filter (e.g., "crypto", "politics", "sports") - uses server-side filtering

# Examples:
python3 {baseDir}/scripts/horizon.py discover polymarket "bitcoin"
python3 {baseDir}/scripts/horizon.py discover kalshi "election" 5
python3 {baseDir}/scripts/horizon.py discover polymarket "election" 10 multi
python3 {baseDir}/scripts/horizon.py discover polymarket "" 10 binary
python3 {baseDir}/scripts/horizon.py discover polymarket "" 20 all crypto

# Get comprehensive detail for a single market
python3 {baseDir}/scripts/horizon.py market-detail <slug_or_id> [exchange]

# Examples:
python3 {baseDir}/scripts/horizon.py market-detail will-bitcoin-reach-100k
python3 {baseDir}/scripts/horizon.py market-detail KXBTC-25FEB28 kalshi
```

### Kelly 最优持仓规模计算
```bash
# Compute optimal position size: kelly <prob> <price> <bankroll> [fraction] [max_size]
python3 {baseDir}/scripts/horizon.py kelly 0.65 0.50 1000
python3 {baseDir}/scripts/horizon.py kelly 0.70 0.55 2000 0.5 50
```

### 风险管理
```bash
# Activate kill switch (emergency stop - cancels all orders)
python3 {baseDir}/scripts/horizon.py kill-switch on "market crash"

# Deactivate kill switch
python3 {baseDir}/scripts/horizon.py kill-switch off

# Add stop-loss: stop-loss <market_id> <side> <order_side> <size> <trigger_price>
# side: yes or no, order_side: buy or sell
python3 {baseDir}/scripts/horizon.py stop-loss <market_id> yes sell 10 0.40

# Add take-profit: take-profit <market_id> <side> <order_side> <size> <trigger_price>
python3 {baseDir}/scripts/horizon.py take-profit <market_id> yes sell 10 0.80
```

### 行情数据与系统健康状况
```bash
# Get snapshot for a named feed
python3 {baseDir}/scripts/horizon.py feed <feed_name>

# List all feeds
python3 {baseDir}/scripts/horizon.py feeds

# Start a live data feed: start-feed <name> <feed_type> [config_json]
# feed_type: binance_ws, polymarket_book, kalshi_book, predictit,
#            manifold, espn, nws, chainlink, rest_json_path, rest
# Note: URL-based feeds (chainlink, rest_json_path, rest) require HTTPS public URLs.
python3 {baseDir}/scripts/horizon.py start-feed eth_usd chainlink '{"contract_address":"0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419","rpc_url":"https://eth.llamarpc.com"}'
python3 {baseDir}/scripts/horizon.py start-feed mf manifold '{"slug":"will-btc-hit-100k"}'

# Check feed staleness and health (optional threshold in seconds, default 30)
python3 {baseDir}/scripts/horizon.py feed-health [threshold]

# Get connection metrics for a feed (or all feeds)
python3 {baseDir}/scripts/horizon.py feed-metrics [feed_name]

# Check YES/NO price parity (optionally specify feed)
python3 {baseDir}/scripts/horizon.py parity <market_id> [feed_name]
```

### 条件订单
```bash
# List pending stop-loss/take-profit orders
python3 {baseDir}/scripts/horizon.py contingent
```

### 事件搜索
```bash
# Discover multi-outcome events on Polymarket
python3 {baseDir}/scripts/horizon.py discover-events "election"
python3 {baseDir}/scripts/horizon.py discover-events "" 5

# Get top markets by volume
python3 {baseDir}/scripts/horizon.py top-markets polymarket 10
python3 {baseDir}/scripts/horizon.py top-markets kalshi 5 "KXBTC"
```

### 钱包分析（Polymarket - 无需认证）
```bash
# Trade history for a wallet
python3 {baseDir}/scripts/horizon.py wallet-trades 0x1234... [limit] [condition_id]

# Trade history for a market
python3 {baseDir}/scripts/horizon.py market-trades 0xabc... [limit] [side] [min_size]

# Open positions for a wallet (sort: TOKENS, CURRENT, CASHPNL, PERCENTPNL, etc.)
python3 {baseDir}/scripts/horizon.py wallet-positions 0x1234... 50 CURRENT

# Total portfolio value in USD
python3 {baseDir}/scripts/horizon.py wallet-value 0x1234...

# Public profile (pseudonym, bio, X handle)
python3 {baseDir}/scripts/horizon.py wallet-profile 0x1234...

# Top holders in a market
python3 {baseDir}/scripts/horizon.py top-holders 0xabc... [limit]

# Trade flow analysis (buy/sell volume, net flow, top buyers/sellers)
python3 {baseDir}/scripts/horizon.py market-flow 0xabc... [trade_limit] [top_n]
```

### 蒙特卡洛模拟
```bash
# Simulate portfolio risk (uses current engine positions)
python3 {baseDir}/scripts/horizon.py simulate [scenarios] [seed]
python3 {baseDir}/scripts/horizon.py simulate 50000
python3 {baseDir}/scripts/horizon.py simulate 10000 42
```

### 套利
```bash
# Execute atomic cross-exchange arb: arb <market_id> <buy_exchange> <sell_exchange> <buy_price> <sell_price> <size>
python3 {baseDir}/scripts/horizon.py arb will-btc-hit-100k kalshi polymarket 0.48 0.52 10
```

### 定量分析
```bash
# Shannon entropy for a probability
python3 {baseDir}/scripts/horizon.py entropy 0.65

# KL divergence between two distributions (comma-separated)
python3 {baseDir}/scripts/horizon.py kl-divergence 0.3,0.7 0.5,0.5

# Hurst exponent for a price series (comma-separated)
python3 {baseDir}/scripts/horizon.py hurst 0.50,0.52,0.48,0.55,0.53

# Variance ratio test for returns (comma-separated) [period]
python3 {baseDir}/scripts/horizon.py variance-ratio 0.01,-0.02,0.03,-0.01,0.02

# Cornish-Fisher VaR/CVaR (comma-separated returns) [confidence]
python3 {baseDir}/scripts/horizon.py cf-var 0.01,-0.02,0.03,-0.05,0.02 0.95

# Prediction Greeks: greeks <price> <size> [is_yes] [t_hours] [vol]
python3 {baseDir}/scripts/horizon.py greeks 0.55 100 true 24 0.2

# Deflated Sharpe ratio: deflated-sharpe <sharpe> <n_obs> <n_trials> [skew] [kurt]
python3 {baseDir}/scripts/horizon.py deflated-sharpe 1.5 252 10

# Signal diagnostics (comma-separated predictions and outcomes)
python3 {baseDir}/scripts/horizon.py signal-diagnostics 0.6,0.3,0.8 1,0,1

# Market efficiency test (comma-separated prices)
python3 {baseDir}/scripts/horizon.py market-efficiency 0.50,0.52,0.48,0.55,0.53,0.51

# Stress test on current positions [scenarios] [seed]
python3 {baseDir}/scripts/horizon.py stress-test 10000
```

### 投资组合管理
```bash
# Get portfolio metrics (value, PnL, exposure, diversification)
python3 {baseDir}/scripts/horizon.py portfolio

# Compute optimal portfolio weights
python3 {baseDir}/scripts/horizon.py portfolio-weights equal
python3 {baseDir}/scripts/horizon.py portfolio-weights kelly
python3 {baseDir}/scripts/horizon.py portfolio-weights risk_parity
python3 {baseDir}/scripts/horizon.py portfolio-weights min_variance
```

### 热重载参数
```bash
# Update runtime parameters (hot-reload, takes effect next cycle)
python3 {baseDir}/scripts/horizon.py update-params '{"spread": 0.05, "gamma": 0.3}'

# Get all current runtime parameters
python3 {baseDir}/scripts/horizon.py get-params
```

### 报表分析
```bash
# Generate comprehensive tearsheet from equity curve CSV
python3 {baseDir}/scripts/horizon.py tearsheet path/to/equity.csv
```

### 贝叶斯优化
```bash
# Run GP-based Bayesian optimization for strategy parameters
# param_space: {name: [min, max]}
python3 {baseDir}/scripts/horizon.py bayesian-opt '{"spread": [0.01, 0.10], "gamma": [0.1, 1.0]}' 20 5
```

### Hawkes 过程
```bash
# Compute Hawkes self-exciting intensity from event timestamps
python3 {baseDir}/scripts/horizon.py hawkes 1000.0,1000.5,1001.2 0.1 0.5 1.0
```

### Ledoit-Wolf 相关性分析
```bash
# Compute shrinkage covariance matrix from returns (rows=observations, cols=assets)
python3 {baseDir}/scripts/horizon.py correlation '[[0.01,0.02],[-0.01,0.03],[0.02,-0.01]]'
```

## 买卖方费用（v0.4.6）

根据流动性角色分配费用，以更真实地模拟交易和回测：

```python
from horizon import Engine

# Flat fee (backward compatible)
engine = Engine(paper_fee_rate=0.001)

# Split maker/taker fees
engine = Engine(
    paper_maker_fee_rate=0.0002,  # 2 bps for makers
    paper_taker_fee_rate=0.002,   # 20 bps for takers
)
```

现在每个 **成交** 记录中都包含一个 `is_maker` 字段（`True`/`False`），表示该订单是买方还是卖方。此功能适用于模拟交易和 BookSim（L2 回测）。

## Chainlink 在链上数据源（v0.4.7）

直接从任何 EVM 链上的 Chainlink 数据源合约读取价格：

```python
import horizon as hz

hz.run(
    feeds={
        "eth_usd": hz.ChainlinkFeed(
            contract_address="0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419",
            rpc_url="https://eth.llamarpc.com",
        ),
    },
    ...
)
```

常见合约地址（以太坊主网）：
- ETH/USD: `0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419`
- BTC/USD: `0xF4030086522a5bEEa4988F8cA5B36dbC97BeE88c`
- LINK/USD: `0x2c1d072e956AFFC0D435Cb7AC38EF18d24d9127c`

适用于以太坊、Arbitrum、Polygon、BSC — 只需更改 `rpc_url` 即可。

## 新数据源（v0.4.5）

新增五种跨市场信号数据源：
- **PredictItFeed** - PredictIt 市场价格（lastTradePrice, bestBuyYesCost, bestSellYesCost）
- **ManifoldFeed** - Manifold Markets 的概率和成交量
- **ESPNFeed** - 实时体育比分（主客场比分、比赛时间、比赛状态）
- **NWSFeed** - 美国国家气象局的天气预报（温度、风速、降水量）和警报
- **RESTJsonPathFeed** - 从任何 REST API 中提取灵活的 JSON 数据

在 `hz.run()` 中进行配置：

```python
import horizon as hz

hz.run(
    feeds={
        "pi": hz.PredictItFeed(market_id=7456, contract_id=28562),
        "manifold": hz.ManifoldFeed("will-btc-hit-100k-by-2026"),
        "nba": hz.ESPNFeed("basketball", "nba"),
        "weather": hz.NWSFeed(state="FL", mode="alerts"),
        "custom": hz.RESTJsonPathFeed(
            url="https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd",
            price_path="bitcoin.usd",
        ),
    },
    ...
)
```

## 执行算法（v0.4.4）

三种用于减少市场影响的拆分大订单的执行算法：
- **TWAP** (`hz.TWAP`) - 时间加权平均价格：在固定时间间隔内均匀分配订单
- **VWAP** (`hz.VWAP`) - 体积加权平均价格：根据成交量分配订单
- **Iceberg** (`hz.Iceberg`) - 仅显示少量可见订单，成交后自动补充

所有算法使用相同的接口：`algo.start(request)`, `algo.on_tick(price, time)`, `algo.is_complete`, `algo.total_filled`.

## 信号组合器 + 市场做市商（v.4.8）

可以组合多个信号并自动执行策略：

```python
hz.run(
    pipeline=[
        hz.signal_combiner([
            hz.price_signal("book", weight=0.5),
            hz.imbalance_signal("book", levels=5, weight=0.3),
            hz.flow_signal("book", window=30, weight=0.2),
        ]),
        hz.market_maker(feed_name="book", gamma=0.5, size=5.0),
    ],
    ...
)
```

可用信号：`price_signal`, `imbalance_signal`, `spread_signal`, `momentum_signal`, `flow_signal`。`market_maker` 在 `signal_combiner` 之后接收上游信号值作为公平价格。

## 管道功能（v.4.4）

Horizon SDK 还包含用于自动化策略的高级管道组件：
- **马尔可夫状态检测** (`markov_regime`) - 使用 Rust 的隐马尔可夫模型（HMM）进行实时状态分类。支持 Baum-Welch 训练和 Viterbi 解码，每刻在线计算 O(N^2) 的前向概率。
- **状态检测** (`regime_signal`) - 判断市场是平静还是波动
- **数据源保护** (`feed_guard`) - 当数据源数据失效时自动触发止损机制
- **库存失衡** (`inventory_skewer`) - 调整报价以降低持仓风险
- **自适应价差** (`adaptive_spread`) - 根据成交率、波动性和订单失衡动态调整价差
- **执行跟踪** (`execution_tracker`) - 监控成交率、滑点和不利选择
- **多策略** - 通过字典配置针对不同市场运行多个策略
- **跨市场对冲** (`cross_hedger`) - 当投资组合波动率超过阈值时生成对冲报价

### 定量分析（v.4.4）

- **信息论** - 香农熵、联合熵、KL 散度、互信息、传递熵
- **微观结构** - Kyle 的 lambda 值、Amihud 比率、Roll 价差、有效价差/实际价差、LOB 不平衡
- **风险分析** - Cornish-Fisher VaR/CVaR、二元市场的预测希腊值（delta, gamma, theta, vega）
- **信号分析** - 信息系数（Spearman）、信号半衰期、Hurst 指数、方差比率测试
- **统计测试** - 调整后的夏普比率、Bonferroni 校正、Benjamini-Hochberg FDR 控制
- **流式检测器** - VPIN 有毒流量、CUSUM 变点、订单流失衡（OFI）跟踪器
- **管道函数** - `toxic_flow()`, `microstructure()`, `change_detector()` 用于 `hz.run()` 中的实时分析
- **压力测试** - 在不利情景下进行蒙特卡洛模拟（相关性飙升、所有交易解决、流动性冲击、尾部风险）
- **CPCV** - 结合回测过拟合概率的组合交叉验证（PBO）

### 回测（v.4.4）

- **L2 书籍模拟** - 使用 `book_data` 参数重放历史订单簿快照
- **成交模型** - **确定性**、**概率性**（排队订单）、`glft`（Gueant-Lehalle-Fernandez-Tapia）
- **市场影响** - 模拟临时和永久性价格影响
- **延迟模拟** - 可配置的订单到成交延迟（以刻度为单位）
- **校准分析** - 使用 Rust 的校准曲线、Brier 分数、对数损失、ECE
- **边缘衰减** - 测量边缘随时间衰减的情况

这些是使用 `hz.run()` 和 `hz.backtest()` 的 Python 管道函数。详情请参阅 SDK 文档。

## 新功能（v.4.16）

### AFML（金融机器学习进展）
- Rust 原生实现的 Lopez de Prado 的研究方法：
  - **信息驱动的条形图** (`hz.dollar_bars`, `hz.volume_bars`, `hz.tick_bars`, `hz.tick_imbalance_bars`) - 根据信息到达时间采样生成的条形图
  - **三重障碍标签** (`hz.triple_barrier_labels`) - 带有止盈、止损和时间障碍的路径依赖性标签
  - **分数微分** (`hz.frac_diff_weights`, `hz.frac_diff_fixed`) - 在保持内存消耗的同时使序列平稳
  - **分层风险均衡** (`hz.hrp_weights`) - 树状聚类投资组合分配
  - **去噪相关性** (`hz.marchenko_pastur_bounds`, `hz.denoise_correlation`) - 使用随机矩阵理论优化相关性

### 多策略协调
`hz.StrategyBook` 可用于从单个进程运行和监控多个策略，支持每个策略的盈亏跟踪、暂停/恢复和再平衡。

### Alpha 研究工具
- `hz.feature_importance` - 通过随机森林计算特征重要性（MDI/MDA）
- `hz.compute_bet_sizing` - 根据线性/sigmoid/离散尺度计算投注大小

### 分层特征控制
在所有高级端点上根据 API 密钥实现功能控制。

## 新功能（v.4.14）

### 报表分析
生成包含月度回报、滚动夏普比率/Sortino 比率、回撤分析、交易统计和尾部比率的综合性能报告。

### 贝叶斯优化
基于零依赖性的遗传算法（GP）参数优化器，能够高效找到最优策略参数。

### 投资组合管理
投资组合对象支持持仓管理、分析和优化（等权重分配、Kelly 最优策略、风险均衡、最小方差权重）。

### 热重载参数
在运行时更新策略参数，无需重启。支持基于文件或字典的参数来源，并自动检测参数变化。

### Hawkes 过程管道
用于模拟交易到达强度的自激点过程。在成交和价格大幅波动时触发。支持针对不同市场的隔离处理。

### Ledoit-Wolf 相关性分析管道
通过 Ledoit-Wolf 公式计算多个数据源的收缩协方差。

## 输出格式

所有命令返回 JSON 格式。成功时直接返回数据；失败时返回 `{"error": "message"}`。

## 重要说明

- `quote` 命令会提交 **实际订单**（或根据配置提交模拟订单）。提交前请务必与用户确认。
- `kill-switch on` 命令是紧急停止命令，会立即取消所有订单。
- 价格表示为 0 到 1 之间的 **概率**（例如，0.65 表示 65% 的预期概率）。
- 交易所配置通过 `HORIZON_EXCHANGE` 环境变量设置（默认为模拟交易）。

完整文档：https://docs.openclaw.ai/tools/clawhub