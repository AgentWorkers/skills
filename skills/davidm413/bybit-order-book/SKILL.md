---
name: bybit-orderbook-backtester
description: >
  Download, process, and backtest ByBit derivatives historical order book data. Use this skill when
  the user wants to: (1) download historical order book snapshots from ByBit's derivatives history-data
  page using Selenium automation, (2) process/unzip ob500 JSONL files and filter to depth 50, (3) run
  any of 10 order-book-based trading strategies (Order Book Imbalance, Breakout, False Breakout,
  Scalping, Momentum, Reversal, Spoofing Detection, Optimal Execution, Market Making, Latency
  Arbitrage) against the data, or (4) generate full backtest performance reports with PnL, Sharpe
  ratio, win rate, max drawdown, and strategy comparison. Triggers on: "bybit order book", "order book
  backtest", "download bybit data", "ob500", "order book imbalance", "spoofing detection strategy",
  "market making backtest", "crypto order book", "depth of book backtest", "bybit historical data".
---

# ByBit 订单簿回测工具

整个流程包括：下载 → 处理 → 回测 → 生成报告。

## 依赖项

```bash
pip install undetected-chromedriver selenium pandas numpy pyarrow --break-system-packages
```

使用 Selenium 时，必须安装 Chrome/Chromium 浏览器。

## 工作流程

该流程分为三个阶段。请按顺序执行这些阶段；如果数据已经准备好，可以直接跳到后续阶段。

### 第一阶段：下载订单簿数据

提示用户输入：
- **交易品种**（默认：BTCUSDT）
- **时间范围**（默认：过去30天）

运行 `scripts/download_orderbook.py`：

```bash
python scripts/download_orderbook.py \
  --symbol BTCUSDT \
  --start 2024-06-01 --end 2024-06-30 \
  --output ./data/raw
```

主要操作：
- 从 `https://www.bybit.com/derivatives/en/history-data` 下载数据
- 自动将数据分割成每7天一个的数据段（ByBit 的规定）
- 使用 `undetected-chromedriver` 来绕过 Cloudflare 的限制
- 输出结果为 ZIP 文件，文件保存在 `./data/raw/` 目录下，文件名为 `{date}_{symbol}_ob500.data.zip`
- 有关数据格式的详细信息，请参阅 `references/bybit_data_format.md`

**如果 Selenium 失败**（可能是由于 Cloudflare 的限制或 ByBit 界面发生变化）：请用户手动从 ByBit 网站下载数据，并将 ZIP 文件放入 `./data/raw/` 目录中。

### 第二阶段：处理数据并筛选到前50层报价

运行 `scripts/process_orderbook.py`：

```bash
python scripts/process_orderbook.py \
  --input ./data/raw \
  --output ./data/processed \
  --depth 50 \
  --sample-interval 1s
```

主要功能：
- 从 ZIP 文件中读取 JSONL 格式的数据（每行代表一个包含50层报价的快照）
- 筛选出前50个买/卖报价
- 计算相关指标：中间价、价差、成交量不平衡、微价格
- 可选地对数据进行处理（例如，将时间间隔调整为 `1秒`、`5秒` 或 `1分钟`——这有助于加快回测速度）
- 输出结果为 Parquet 格式的文件，保存在 `./data/processed/` 目录下

**不进行数据降采样的情况下**：每天大约有86,000个快照，每个品种的 Parquet 文件大小约为300MB。
**进行1秒时间间隔的降采样后**：每天大约有86,000个快照，每个品种的 Parquet 文件大小约为5MB，更适合回测使用。

### 第三阶段：回测策略

运行 `scripts/backtest.py`：

```bash
# Run all 10 strategies
python scripts/backtest.py \
  --input ./data/processed/BTCUSDT_ob50.parquet \
  --output ./reports

# Run specific strategies
python scripts/backtest.py \
  --input ./data/processed/BTCUSDT_ob50.parquet \
  --strategies imbalance,breakout,market_making \
  --output ./reports

# Quick test with limited rows
python scripts/backtest.py \
  --input ./data/processed/BTCUSDT_ob50.parquet \
  --max-rows 100000 \
  --output ./reports
```

策略相关的关键参数包括：`imbalance`、`breakout`、`false_breakout`、`scalping`、`momentum`、`reversal`、`spoofing`、`optimal_execution`、`market_making`、`latency_arb`

输出结果保存在 `./reports/` 目录下：
- `{SYMBOL}_backtest_report.json`：包含完整的回测结果及资产曲线图
- `{SYMBOL}_backtest_report.md`：包含对比表格和详细指标

每种策略的回测指标包括：总交易次数、盈利/亏损交易数量、胜率、累计盈亏（PnL）、夏普比率（Sharpe ratio）、最大回撤（绝对值和百分比）、平均每次交易的盈亏、平均持仓时间、盈利因子、最佳/最差交易记录以及资产曲线图。

有关策略的具体逻辑和可调参数，请参阅 `references/strategies.md`。

## 自定义设置

要修改策略参数，请编辑 `scripts/backtest.py` 中相应策略类的 `__init__` 方法。每个策略的 `self.params` 字典中包含了所有可调整的参数。

**添加新策略的方法**：
1. 在 `scripts/backtest.py` 中继承 `Strategy` 类
2. 实现 `on_snapshot(self, row, idx, df)` 方法，用于定义入场/出场逻辑
3. 将新策略添加到 `STRATEGY_MAP` 字典中

## 常见问题解决方法**

- **Selenium 无法加载 ByBit 页面**：ByBit 使用了 Cloudflare 的安全策略。请确保 `undetected-chromedriver` 是最新版本；如果需要，可以尝试使用 `--no-headless` 参数进行可视化调试；如果问题仍然存在，可以手动下载数据。
- **处理数据时内存不足**：可以使用 `--sample-interval 1s` 或更大的时间间隔来减少内存消耗；或者一次只处理一天的数据。
- **没有生成交易记录**：可能是策略的阈值设置过于严格。请参考 `references/strategies.md` 中的建议，适当放宽阈值或调整回测时间范围。