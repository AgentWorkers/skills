---
name: binance-signal-engine
description: 使用 Binance 的公共 API 进行多时间框架的加密货币技术分析，提供评分交易信号、结构化的交易计划以及仓位管理功能。适用于用户提出以下需求时：分析 BTC 的走势、获取 ETH/USDT 的交易信号、进行加密货币分析、为 SOL 制定交易策略、扫描加密货币对、查看 BTC 的趋势、进行多时间框架分析、生成交易信号、判断 ETH 的市场趋势、分析 BTC/USDT 的技术形态、判断买入 BTC 的时机，或计算加密货币交易的仓位大小。
version: 1.0.2
homepage: https://github.com/eplt/binance-signal-engine
metadata:
  openclaw:
    emoji: "📊"
    requires:
      bins:
        - python3
    install:
      - kind: uv
        package: ccxt pandas numpy ta
        label: "Install Python dependencies (ccxt, pandas, numpy, ta)"
    files:
      - "scripts/*"

---
# Binance Signal Engine

这是一个用于加密货币市场的多时间框架技术分析信号生成器。它将三个时间框架的数据合并成一个加权得分，并输出一个包含头寸大小的结构性交易计划。

## 使用场景

当用户需要以下功能时，可以使用此工具：
- 对任何在Binance上市的加密货币对进行技术分析
- 获取市场趋势（牛市/熊市/中性）或交易信号
- 生成交易的入场价、止损价和获利了结价
- 检查市场趋势（1天）、市场动能（4小时）和入场时机（15分钟）
- 根据账户风险参数调整头寸大小
- 一次性扫描多个交易品种
- 为某个交易品种生成可用于回测的数据记录

## 工作原理

该工具会对三个独立的时间框架进行评分，并将结果合并：

**1天时间框架 — 市场趋势**
- 使用EMA（9/21/50周期）和ADX指标以及方向性指标（DI+/DI−）来判断市场整体趋势是牛市、熊市还是中性。这一判断作为后续分析的基准，动能和交易信号都会基于此趋势进行解读。

**4小时时间框架 — 市场动能**
- 通过MACD线与信号线的交叉、直方图的方向以及随机振荡器的交叉来分析市场动能。随机振荡器的信号会根据市场趋势的不同而赋予不同的权重（例如，在牛市中，从超卖区间发出的买入信号比在熊市中的信号更具参考价值）。

**15分钟时间框架 — 入场时机**
- 通过RSI指标判断市场是否处于超卖/超买状态、布林带重新进入信号、成交量相对于20日均线的变化，以及20根K线内的RSI背离情况来确定当前的入场时机。

每个时间框架的得分都会被赋予可配置的权重，最终综合得分会映射到一个五级趋势判断体系中：**强烈牛市 → 牛市 → 中性 → 熊市 → 强烈熊市**，并据此给出相应的交易建议（买入、观察多头、等待、观察空头、卖出/做空）。

当各项条件满足时，交易规划器会生成一个完整的交易计划，包括滚动使用的支撑/阻力位、基于平均真实范围（ATR）的止损设置以及可配置的风险回报目标。头寸大小的调整会考虑账户余额、风险百分比、交易所的最低交易单位限制以及最小名义金额限制。

## 使用方法

```bash
# Single pair — human-readable summary
python3 {baseDir}/scripts/binance_signal_engine.py BTC/USDT

# Multiple pairs
python3 {baseDir}/scripts/binance_signal_engine.py BTC/USDT ETH/USDT SOL/USDT

# JSON output for programmatic consumption
python3 {baseDir}/scripts/binance_signal_engine.py BTC/USDT --output json

# Futures mode with custom risk parameters
python3 {baseDir}/scripts/binance_signal_engine.py BTC/USDT \
  --market futures --leverage 3 --balance 5000 --risk 2

# Use a JSON config file to override all indicator/scoring parameters
python3 {baseDir}/scripts/binance_signal_engine.py ETH/USDT --config my_config.json

# Debug mode for verbose logging
python3 {baseDir}/scripts/binance_signal_engine.py BTC/USDT --debug
```

### 命令行参数（CLI Flags）

| 参数 | 默认值 | 说明 |
|------|-------|---------|
| `symbols` | | （必填）一个或多个交易对，例如 `BTC/USDT` 或 `ETH/USDT` |
| `--market` | `-m` | `spot` | 市场类型：现货（spot）或期货（futures） |
| `--exchange` | `-e` | `binance` | 交易所ID（兼容ccxt） |
| `--balance` | `-b` | `10000` | 账户余额（单位：美元） |
| `--risk` | `-r` | `1.0` | 每笔交易的风险百分比 |
| `--leverage` | `-l` | `1.0` | 杠杆倍数（仅限期货） |
| `--config` | `-c` | `None` | 配置文件路径，用于覆盖所有参数 |
| `--output` | `-o` | `summary` | 输出格式：文本（summary）或JSON（机器可读） |
| `--debug` | | `off` | 启用调试日志记录 |

## 输出结构

JSON输出包含四个部分：
- **signal**：综合得分、各时间框架的详细评分（趋势/动能/入场时机）、市场趋势判断、交易建议以及解释评分决策的文字说明。
- **trade_plan**：交易方向（多头/空头）、入场类型（市价/限价）、入场价、止损价、获利了结价、支撑位、阻力位、有效风险回报比、是否可交易以及交易计划状态（准备中/等待中/被拒绝/无效）。
- **position_size**：头寸单位、名义金额、风险预算、实际风险金额、潜在收益金额、头寸占账户余额的比例，以及头寸是否受到名义金额限制。
- **backtest_row**：包含时间戳、交易品种、15分钟收盘价、总得分、市场趋势判断、是否可交易、有效风险回报比以及头寸大小的键值记录。适用于追加到CSV或DataFrame中用于历史分析。

## 配置

所有参数都可以通过`--config`参数传入的JSON文件进行配置。主要配置项包括：
- EMA周期（快速：9，慢速：21，趋势：50）
- MACD参数（12/26/9）
- ADX周期和趋势判断阈值（14, 25.0）
- RSI周期和超卖/超买阈值（14, 35/65）
- 随机振荡器窗口、平滑处理方式和阈值（14, 3, 20/80）
- 布林带窗口和标准差（20, 2.0）
- ATR周期和止损倍数（14, 1.5）
- 成交量移动平均周期和成交量异常阈值（20, 1.5倍）
- 支撑/阻力位的回溯窗口和缓冲倍数
- 各时间框架的评分权重（共15个权重）
- 弱信号/强信号的评分阈值（10/30）
- 风险回报比、最低可接受的风险回报比、滑点缓冲值
- 账户余额、风险百分比、最大名义金额限制、杠杆倍数

默认配置适用于在Binance上进行波段交易或日内交易的情况。

## 依赖项

需要Python 3.8及以上版本，并安装以下库：```bash
pip install ccxt pandas numpy ta
```

该工具不使用API密钥，仅使用Binance提供的公开OHLCV数据端点。

## 限制条件：
- 信号仅作为分析工具使用，不构成财务建议。请自行判断并管理风险。
- Binance对API请求有速率限制（每分钟约1200次请求）。该工具会在请求之间加入内置延迟。
- 最新的（仍开放的）K线数据会被自动排除，以避免预测偏差。
- 空头交易信号和头寸大小调整仅在期货模式下可用。
- 回测数据仅为历史数据快照，并非完整的回测引擎。

## 外部数据端点

| 端点 | 发送的数据 | 用途 |
|----------|-----------|---------|
| `https://api.binance.com`（通过ccxt） | 交易品种名称、时间框架、K线数据 | 获取公开的OHLCV价格数据 |

该工具不会调用任何需要认证的API，也不会下达交易指令，也不会将任何数据传输到外部。

## 安全与隐私：
- **无需API密钥**：仅使用公开的市场数据端点。
- **数据安全**：所有指标计算和评分都在本地Python环境中完成。
- **无数据写入**：所有数据仅输出到标准输出（stdout），不会写入交易所系统。
- **无后台进程**：工具运行完成后立即退出。

## 模型调用说明

当用户的请求符合描述中的触发条件时，该工具可能会被自动调用。这是OpenClaw的标准行为。如果希望仅通过`/binance-signal-engine`命令手动调用该工具，可以在文档的开头设置`disable-model-invocation: true`。

## 信任声明

通过安装此工具，您同意以下事项：
- `ccxt`库会通过HTTPS向Binance的公开REST API请求K线数据。
- 所有分析操作都在您的本地机器上完成，无需输入任何凭据。
- 仅当您同意向`api.binance.com`发送公开市场数据请求时，才建议安装此工具。