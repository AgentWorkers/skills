---
name: paper-trading
description: 运行一个结构化的模拟交易循环，该循环支持基于 SQLite 的事件记录、持仓跟踪以及盈亏（PnL）分析功能。适用于开立/平仓模拟交易、记录论文相关笔记、检查投资组合状态或生成每周绩效总结等场景。
metadata:
  {
    "openclaw":
      {
        "emoji": "📓",
        "requires": { "bins": ["node"] },
      },
  }
---
# 模拟交易

基于 SQLite 的模拟交易系统，支持不可变的事件日志记录。

**资产标识：**
- `symbol` 是执行交易/快照命令所必需的。
- `mint` 是执行 `snapshot` 和 `open` 操作所必需的（格式：`--mint <address>`）。
- 如果多个头寸共享相同的 `symbol`，在执行 `close` 或 `set-levels` 操作时需要指定 `--mint` 参数，以确保操作针对正确的头寸。
- 对于在去中心化交易所（DEX）上的 ETH/BTC 资产，应使用相应的代币合约地址（如 `WETH`、`WBTC` 或 `cbBTC`）作为 `mint` 参数。

## 使用场景**

当用户希望执行以下操作时，可以使用此功能：
- 在投入实际资金之前测试交易策略；
- 随时间跟踪交易记录（包括入场、出场、止损、止盈等操作）；
- 计算已实现和未实现的利润（PnL）；
- 记录交易思路并定期进行回顾。

## 数据库**

默认数据库路径：
```bash
~/.openclaw/paper-trading.db
```

可以通过 `--db <path>` 参数自定义数据库路径。

## 命令说明**

使用以下脚本执行相应操作：
```bash
node --experimental-strip-types {baseDir}/scripts/paper_trading.ts --help
```

**环境注意事项：**
- SQLite 不需要额外的 npm 依赖，系统使用内置的 `node:sqlite` 模块。
- 在当前版本的 Node.js 中，使用 SQLite 可能会触发 `ExperimentalWarning` 警告，这是正常现象。

### 1) 初始化账户
```bash
node --experimental-strip-types {baseDir}/scripts/paper_trading.ts init \
  --account main \
  --name "Main Paper Account" \
  --base-currency USD \
  --starting-balance 10000
```

### 2) 记录市场快照（用于计算未实现的利润）
```bash
node --experimental-strip-types {baseDir}/scripts/paper_trading.ts snapshot \
  --symbol BTC \
  --mint 6p6xgHyF7AeE6TZk8x9mNQd2r2hH7r4mYJ8t6x6hYfSR \
  --price 62000 \
  --source dexscreener
```

### 3) 开立头寸
```bash
node --experimental-strip-types {baseDir}/scripts/paper_trading.ts open \
  --account main \
  --symbol BTC \
  --mint 6p6xgHyF7AeE6TZk8x9mNQd2r2hH7r4mYJ8t6x6hYfSR \
  --side LONG \
  --qty 0.1 \
  --price 62000 \
  --fee 4 \
  --stop-price 60500 \
  --take-price 65000 \
  --max-risk-pct 1.5 \
  --note "Breakout + volume confirmation"
```

### 4) 更新止损/止盈设置
```bash
node --experimental-strip-types {baseDir}/scripts/paper_trading.ts set-levels \
  --account main \
  --symbol BTC \
  --mint 6p6xgHyF7AeE6TZk8x9mNQd2r2hH7r4mYJ8t6x6hYfSR \
  --side LONG \
  --stop-price 61200 \
  --take-price 66000 \
  --note "Move stop to reduce downside"
```

### 5) 平仓头寸
```bash
node --experimental-strip-types {baseDir}/scripts/paper_trading.ts close \
  --account main \
  --symbol BTC \
  --mint 6p6xgHyF7AeE6TZk8x9mNQd2r2hH7r4mYJ8t6x6hYfSR \
  --side LONG \
  --qty 0.05 \
  --price 63500 \
  --fee 3 \
  --note "Partial take profit"
```

### 6) 记录交易笔记
```bash
node --experimental-strip-types {baseDir}/scripts/paper_trading.ts note \
  --account main \
  --symbol BTC \
  --side LONG \
  --note "Invalidation if daily close < 61k" \
  --tags thesis risk macro
```

### 7) 查看投资组合状态
```bash
node --experimental-strip-types {baseDir}/scripts/paper_trading.ts status --account main
node --experimental-strip-types {baseDir}/scripts/paper_trading.ts status --account main --format json --pretty
```

### 8) 进行每周回顾
```bash
node --experimental-strip-types {baseDir}/scripts/paper_trading.ts review --account main
node --experimental-strip-types {baseDir}/scripts/paper_trading.ts review --account main --format json --pretty
```

## 工作流程：
1. 对持有未平仓头寸的资产，始终使用 `--mint` 和 `--source dexscreener` 参数来更新快照。
2. 只有在设置了明确的止损和风险上限的情况下才执行交易（使用 `--max-risk-pct` 参数）。
3. 将所有交易变化记录为事件，切勿修改旧事件记录。
4. 每次交易后运行 `status` 命令，每周末进行一次交易回顾。

## 其他说明：
- SQLite 中的事件记录为只读（只能追加数据，不能修改）。
- 利润（PnL）是通过重新执行所有交易事件来计算的。
- `status` 命令会根据每个 `symbol` 和 `mint` 的组合使用最新的快照来计算未实现的利润。

## 验证方法**

运行完整的模拟交易测试套件：
```bash
node --test {baseDir}/tests/paper_trading.test.mjs
```