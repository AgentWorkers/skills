---
name: claw-screener
description: 这款股票筛选工具结合了威廉姆斯百分比R（Williams %R）指标的“超卖”信号与沃伦·巴菲特式的基本面分析方法。支持美国（标准普尔500指数，S&P 500）和泰国（SET）市场的数据。
homepage: https://github.com/rsoutar/claw-screener
metadata:
  clawdbot:
    emoji: "📊"
    requires:
      env: []
      files:
        - ~/.claw-screener-watchlist.json
---
# Claw-Screener

这是一个股票筛选工具，它结合了技术分析（Williams %R指标的超卖信号）和沃伦·巴菲特式的基本面分析方法，并使用美国证券交易委员会（SEC）的数据。支持美国（S&P 500指数）和泰国（SET指数）市场。

## 何时使用此工具

当您需要以下情况时，可以使用此工具：
- 找到基本面强劲但被市场过度抛售的股票
- 使用巴菲特的10个评估标准来筛选优质股票
- 分析个别股票以做出投资决策
- 以文本、JSON或Telegram格式获取每日股票筛选结果

## 工具功能

### 1. 综合筛选
寻找同时满足技术超卖条件（Williams %R < -80）和基本面强劲条件（巴菲特评分 >= 阈值）的股票。

**命令：**
```
bun run src/screening.ts [options]
```

**选项：**
| 标志 | 描述 | 默认值 |
|------|-------------|---------|
| `--market` | 市场：`us` 或 `bk` | `us` |
| `--min-score` | 最低巴菲特评分（0-10） | `5` |
| `--top-n` | 显示的结果数量 | `10` |
| `--format` | 输出格式：`text`、`json`、`telegram` | `text` |

**示例：**
```
bun run src/screening.ts
bun run src/screening.ts --market us --min-score 7 --top-n 5
bun run src/screening.ts --market bk
bun run src/screening.ts --format json
bun run src/screening.ts --format telegram
```

### 2. 仅技术分析
仅使用Williams %R指标进行快速超卖筛选。无需SEC数据。适用于美国和泰国市场。

**命令：**
```
bun run src/technicalOnly.ts [options]
```

**选项：**
| 标志 | 描述 | 默认值 |
|------|-------------|---------|
| `--market` | 市场：`us` 或 `bk` | `us` |
| `--threshold` | Williams %R的阈值 | `-80` |
| `--top-n` | 显示的结果数量 | `20` |
| `--format` | 输出格式：`text`、`json`、`telegram` | `text` |

**示例：**
```
bun run src/technicalOnly.ts
bun run src/technicalOnly.ts --threshold -70 --top-n 50
bun run src/technicalOnly.ts --market bk
```

### 3. 单股分析
使用巴菲特的10个评估标准对单只股票进行深入分析。

**命令：**
```
bun run src/analyze.ts <ticker> [options]
```

**选项：**
| 标志 | 描述 | 默认值 |
|------|-------------|---------|
| `--format` | 输出格式：`text`、`json`、`telegram` | `text` |

**示例：**
```
bun run src/analyze.ts AAPL
bun run src/analyze.ts MSFT --format telegram
bun run src/analyze.ts GOOGL --format json
bun run src/analyze.ts PTT.BK
```

### 4. 关注列表管理
跟踪您感兴趣的股票，并在它们被市场过度抛售或过度买入时接收警报。

**命令：**
```
bun run src/watchList.ts <command> [options]
```

**其他命令：**
| 命令 | 描述 |
|---------|-------------|
| `add <ticker>` | 将股票添加到关注列表 |
| `remove <ticker>` | 从关注列表中删除股票 |
| `list` | 显示所有关注的股票 |

**选项：**
| 标志 | 描述 | 默认值 |
|------|-------------|---------|
| `--market us\|th` | 市场：`us`（美国）或 `th`（泰国） | `us` |
| `--notes '...'` | 股票的备注 | - |
| `--alert-threshold` | 发送警报的Williams %R阈值 | - |

**示例：**
```
bun run src/watchList.ts add AAPL
bun run src/watchList.ts add AAPL --market us --notes 'Big tech'
bun run src/watchList.ts add PTT.BK --market th
bun run src/watchList.ts remove AAPL
bun run src/watchList.ts list
bun run src/watchList.ts list --market us
```

**NPM脚本：**
```
npm run watchlist:add <ticker> [options]
npm run watchlist:remove <ticker>
npm run watchlist:list
```

**数据存储：**
关注列表保存在`~/.claw-screener-watchlist.json`文件中。

## 巴菲特的10个评估标准

该工具根据沃伦·巴菲特的标准对股票进行基本面分析：

| 序号 | 评估标准 | 目标 | 描述 |
|---|---------|--------|-------------|
| 1 | 现金比率 | > 总债务 | 现金覆盖所有债务 |
| 2 | 负债与股本比率 | < 0.5 | 低杠杆率 |
| 3 | 股东权益回报率 | > 15% | 资本使用效率 |
| 4 | 流动比率 | > 1.5 | 短期流动性 |
| 5 | 操作利润率 | > 12% | 运营效率 |
| 6 | 资产周转率 | > 0.5 | 资产利用效率 |
| 7 | 利息保障倍数 | > 3倍 | 支付利息的能力 |
| 8 | 盈利稳定性 | 正值 | 盈利能力稳定 |
| 9 | 自由现金流 | > 0 | 产生现金的能力 |
| 10 | 资本配置 | 股东权益回报率（ROE）> 15% | 管理效率 |

**评分规则：** 每个满足标准的评估标准得1分。最高分为10分。

## 技术指标：Williams %R（威廉姆斯百分比范围）

- 范围：-100到0
- 超卖：< -80（潜在买入信号）
- 过度买入：> -20（潜在卖出信号）

## 综合评分公式

综合评分 = （技术评分 × 0.3）+ （基本面评分 × 0.7）

- 技术评分：(Williams %R + 100) / 100
- 基本面评分：(巴菲特评分 / 10) × 100

## 数据来源

- **美国股票**：使用SEC的EDGAR数据库获取基本面数据，Yahoo Finance获取股价数据
- **泰国股票**：仅使用Yahoo Finance的数据（无SEC数据）

## 安装方法**
```bash
bun install
```

## NPM脚本**
```bash
npm run dev              # Run screening (alias for bun run src/screening.ts)
npm run screening        # Run combined screening
npm run technical        # Run technical-only scan
npm run analyze          # Analyze a stock (requires ticker argument)
npm run watchlist:add    # Add stock to watchlist
npm run watchlist:remove # Remove stock from watchlist
npm run watchlist:list   # List watched stocks
```

## 输出格式示例

### 文本格式（默认）
```
📊 Combined Quality Screening (US (S&P 500))
Technical: Oversold signals (Williams %R < -80)
Fundamental: Warren Buffett's 10 formulas on SEC data
Minimum Buffett Score: 5/10

Results:
  Total Scanned: 503
  Oversold Found: 42
  Quality Stocks: 8 (Buffett ≥5/10)

Top 10 Opportunities:

1. AAPL   — Combined: 85.2% | Buffett: 8/10 | WR: -82.3
2. MSFT   — Combined: 79.1% | Buffett: 7/10 | WR: -85.1
```

### Telegram格式
```
📊 Combined Quality Screening (US (S&P 500))
Scanned: 503 stocks
Oversold: 42
Quality (Buffett ≥5/10): 8

🌟 Top 10 Quality Opportunities:

1. **AAPL** — Combined: 85% | Buffett: 8/10 | WR: -82.3
2. **MSFT** — Combined: 79% | Buffett: 7/10 | WR: -85.1
```