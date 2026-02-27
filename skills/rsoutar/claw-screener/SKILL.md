---
name: claw-screener
description: >
  **股票筛选器：结合威廉姆斯%R超卖信号与沃伦·巴菲特式的基本面分析**  
  该工具支持美国（标准普尔500指数）和泰国（SET指数）市场。  
  **功能特点：**  
  1. **威廉姆斯%R超卖信号**：利用威廉姆斯%R指标来判断股票是否处于超卖状态，从而识别潜在的买入机会。  
  2. **沃伦·巴菲特式基本面分析**：结合巴菲特的投资理念，对股票的基本面数据进行深入分析，以评估其长期投资价值。  
  3. **多市场支持**：同时覆盖美国和泰国的主要市场。  
  **使用说明：**  
  1. 输入目标股票代码或股票名称，系统将自动显示符合筛选条件的股票列表。  
  2. 根据%R超卖信号和基本面分析结果，您可以进一步筛选出最具投资潜力的股票。  
  3. 提供实时数据更新和图表展示，帮助您做出更明智的投资决策。
homepage: https://github.com/rsoutar/claw-screener
metadata:
  clawdbot:
    emoji: "📊"
    requires:
      env: []
      files:
        - ~/.claw-screener-watchlist.json
        - sec_cache.db
        - price_cache.db
      runtime: bun >=1.3.1
      config_paths: ~/.claw-screener-watchlist.json
---
# Claw-Screener

这是一个股票筛选工具，它结合了技术分析（Williams %R指标的超卖信号）和沃伦·巴菲特式的基本面分析（使用美国证券交易委员会（SEC）的数据）。支持美国（标准普尔500指数）和泰国（SET）市场。

## 何时使用此工具

当你需要以下情况时，可以使用此工具：
- 找到基本面强劲但被过度抛售的股票
- 使用巴菲特的10个评估公式筛选优质股票
- 使用Carlson过滤器筛选具有长期增长潜力的股票
- 分析个股以做出投资决策
- 以文本、JSON或Telegram格式获取每日股票筛选结果

## 工具功能

### 1. 综合筛选
找到技术上被过度抛售（Williams %R < -80）且基本面强劲（巴菲特评分 >= 阈值）的股票。

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
仅使用Williams %R指标进行快速超卖筛选。不需要SEC数据。适用于美国和泰国市场。

**命令：**
```
bun run src/technicalOnly.ts [options]
```

**选项：**
| 标志 | 描述 | 默认值 |
|------|-------------|---------|
| `--market` | 市场：`us` 或 `bk` | `us` |
| `--threshold` | Williams %R阈值 | `-80` |
| `--top-n` | 显示的结果数量 | `20` |
| `--format` | 输出格式：`text`、`json`、`telegram` | `text` |

**示例：**
```
bun run src/technicalOnly.ts
bun run src/technicalOnly.ts --threshold -70 --top-n 50
bun run src/technicalOnly.ts --market bk
```

### 3. 分析个股
使用巴菲特的10个评估公式对单只股票进行深入分析。

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

### 4. 长期增长筛选器
使用Carlson风格的过滤器筛选具有长期增长潜力的股票：
- 收入和净利润的同比增长趋势
- 净资产回报率（ROIC）阈值（默认 >15%）
- 过去3年的股票回购情况
- 操作利润率阈值（默认 >20%）
- 包括当前收益率与5年平均收益率以及简单的10年现金流折现（DCF）分析

**命令：**
```
bun run src/compoundingMachine.ts [options]
```

**选项：**
| 标志 | 描述 | 默认值 |
|------|-------------|---------|
| `--market` | 市场范围：`us` 或 `bk` | `us` |
| `--tickers` | 用逗号分隔的股票代码（覆盖市场范围） | - |
| `--max-tickers` | 显示的通过筛选的股票数量 | `25` |
| `--concurrency` | 并行处理任务的数量 | `4` |
| `--format` | 输出格式：`text` 或 `json` | `text` |
| `--db-path` | SQLite缓存路径 | `sec_cache.db` |
| `--ttl-days` | 缓存有效期（天数） | `7` |
| `--min-roic` | ROIC阈值（%） | `15` |
| `--min-op-margin` | 操作利润率阈值（%） | `20` |
| `--min-buyback` | 过去3年股票回购比例（%） | `2` |
| `--show-rejected` | 是否在输出中包含失败股票及其原因 | `off` |

**示例：**
```
bun run src/compoundingMachine.ts
bun run src/compoundingMachine.ts --tickers AAPL,MSFT,NVDA --top-n 10
bun run src/compoundingMachine.ts --format json --max-tickers 100
bun run src/compoundingMachine.ts --tickers PLTR --show-rejected
```

**运行/缓存说明：**
- 首次对整个美国市场进行完整筛选可能需要20-30分钟以上。
- 这是正常的：每个股票代码都需要多次向Yahoo Finance请求基本面数据和报价，并进行重试以应对速率限制。
- 由于使用了SQLite缓存（`sec_cache.db`，缓存有效期为7天），后续运行速度会快很多。
- 如需快速测试，可以缩小筛选范围（例如使用`--max-tickers 50`或指定股票代码`--tickers`）。

**用户消息引导：**
- 如果用户运行全市场筛选，应明确提示首次运行可能需要20-30分钟。
- 建议在等待期间尝试快速测试：
  - `bun run src/compoundingMachine.ts --max-tickers 50`
  - `bun run src/compoundingMachine.ts --tickers AAPL,MSFT,NVDA`

### 5. 关注列表管理
跟踪你感兴趣的股票，并在它们被过度抛售或过度买入时接收警报。

**命令：**
```
bun run src/watchList.ts <command> [options]
```

**命令：**
| 命令 | 描述 |
|---------|-------------|
| `add <ticker>` | 将股票添加到关注列表 |
| `remove <ticker>` | 从关注列表中移除股票 |
| `list` | 显示所有关注的股票 |

**选项：**
| 标志 | 描述 | 默认值 |
|------|-------------|---------|
| `--market us\|th` | 市场：`us`（美国）或 `th`（泰国） | `us` |
| `--notes '...'` | 股票的备注 | - |
| `--alert-threshold` | 用于警报的Williams %R阈值 | - |

**示例：**
```
bun run src/watchList.ts add AAPL
bun run src/watchList.ts add AAPL --market us --notes 'Big tech'
bun run src/watchList.ts add PTT.BK --market th
bun run src/watchList.ts remove AAPL
bun run src/watchList.ts list
bun run src/watchList.ts list --market us
```

**存储：** 关注列表保存在`~/.claw-screener-watchlist.json`文件中

## 巴菲特的10个评估公式

该工具根据沃伦·巴菲特的标准对股票进行基本面分析：

| 编号 | 公式 | 目标 | 描述 |
|---|---------|--------|-------------|
| 1 | 现金测试 | 现金余额 > 总债务 | 现金覆盖所有债务 |
| 2 | 负债与股权比率 | < 0.5 | 低杠杆率 |
| 3 | 股东回报率 | > 15% | 资本使用效率 |
| 4 | 流动比率 | > 1.5 | 短期流动性 |
| 5 | 操作利润率 | > 12% | 运营效率 |
| 6 | 资产周转率 | > 0.5 | 资产利用效率 |
| 7 | 利息保障倍数 | > 3倍 | 偿付利息的能力 |
| 8 | 盈利稳定性 | 正值 | 盈利能力稳定 |
| 9 | 自由现金流 | > 0 | 现金生成能力 |
| 10 | 资本配置 | 净资产回报率（ROE）> 15% | 管理效率 |

**评分规则：** 每个满足条件的公式得1分。最高分为10分。

## 技术指标

**Williams %R（Williams百分比范围）**

- 范围：-100到0
- 超卖：< -80（潜在买入信号）
- 过买：> -20（潜在卖出信号）

## 综合评分公式

综合评分 = （技术评分 × 0.3）+ （基本面评分 × 0.7）

- 技术评分：(Williams %R + 100) / 100
- 基本面评分：(巴菲特评分 / 10) × 100

## 数据来源

- **美国股票**：使用SEC EDGAR数据获取基本面信息，使用Yahoo Finance获取价格数据
- **泰国股票**：仅使用Yahoo Finance数据（无SEC数据）

## 安装

### 运行环境要求

- **Bun**（版本 >=1.3.1）：执行TypeScript脚本所需的运行环境
- 不需要Node.js，因为Bun提供了所有必要的运行时功能

### 安装Bun

如果尚未安装Bun，请运行以下命令：
```bash
# macOS/Linux
curl -fsSL https://bun.sh/install | bash

# Windows (PowerShell)
iwr https://bun.sh/install -outfile "install.ps1"; ./install.ps1
```

### 安装依赖项

```bash
bun install
```

## 文件管理

此工具创建并管理以下文件：

| 文件 | 位置 | 用途 | 缓存有效期 |
|------|----------|---------|-----|
| 关注列表 | `~/.claw-screener-watchlist.json` | 用户的股票关注列表 | 永久保存 |
| SEC缓存 | `sec_cache.db` | SEC EDGAR财务数据的缓存 | 7天（默认） |
| 价格缓存 | `price_cache.db` | 股票价格数据的缓存 | 1天（默认） |

### 缓存管理

- 缓存文件在首次运行时自动生成
- 使用`--ttl-days`选项调整缓存有效期
- 可以删除缓存文件以强制重新获取数据
- 缓存显著提升后续运行的性能

### 注意事项
- 首次对整个美国市场进行完整筛选可能需要20-30分钟以上
- 由于缓存机制，后续运行速度会快很多
- 如需快速测试，可以使用`--max-tickers 50`或指定股票代码`--tickers`

## Bun脚本

```bash
bun run dev              # Run screening (alias for bun run src/screening.ts)
bun run screening        # Run combined screening
bun run technical        # Run technical-only scan
bun run analyze          # Analyze a stock (requires ticker argument)
bun run compounder       # Run Compounding Machine screener
bun run watchlist:add    # Add stock to watchlist
bun run watchlist:remove # Remove stock from watchlist
bun run watchlist:list   # List watched stocks
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