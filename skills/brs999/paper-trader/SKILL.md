---
name: paper-trading
description: 运行一个结构化的模拟交易循环，该循环支持基于 SQLite 的事件记录、头寸跟踪以及盈亏（PnL）分析功能。适用于开立/关闭模拟交易、记录论文相关笔记、检查投资组合状态或生成每周绩效总结等场景。
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

基于 SQLite 的模拟交易系统，具有不可更改的事件日志功能。

**资产标识：**
- `symbol` 是执行交易或生成快照命令所必需的。
- `mint` 是可选参数（`--mint <address>`），用于针对特定代币地址进行追踪。
- 如果多个头寸共享相同的 `symbol`，在执行 `close` 或 `set-levels` 操作时，请务必指定 `--mint` 以确保操作针对正确的头寸。

## 使用场景**

当用户需要以下功能时，可以使用此模拟交易系统：
- 在实际投入资金之前测试交易策略；
- 随时间追踪交易记录（包括入场、出场、止损、止盈等操作）；
- 计算已实现和未实现的损益（PnL）；
- 记录交易笔记并进行定期回顾。

## 数据库**

默认数据库路径：
```bash
~/.openclaw/paper-trading.db
```

可以通过 `--db <path>` 参数进行自定义。

## 命令**

使用以下脚本执行相应操作：
```bash
node --experimental-strip-types {baseDir}/scripts/paper_trading.ts --help
```

**环境注意事项：**
- SQLite 不需要依赖 npm（使用内置的 `node:sqlite` 模块）；
- 在当前版本的 Node.js 中，使用 SQLite 可能会触发 `ExperimentalWarning`，这是正常现象。

### 1) 初始化账户
```bash
node --experimental-strip-types {baseDir}/scripts/paper_trading.ts init \
  --account main \
  --name "Main Paper Account" \
  --base-currency USD \
  --starting-balance 10000
```

### 2) 生成市场快照（用于计算未实现的损益）
```bash
node --experimental-strip-types {baseDir}/scripts/paper_trading.ts snapshot \
  --symbol BTC \
  --mint 6p6xgHyF7AeE6TZk8x9mNQd2r2hH7r4mYJ8t6x6hYfSR \
  --price 62000 \
  --source manual
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
1. 对持有未平仓头寸的资产持续更新快照。
2. 仅在执行交易时设置明确的止损和风险上限（使用 `--max-risk-pct` 参数）。
3. 将所有交易变化记录为事件，切勿修改历史事件。
4. 每次交易后运行 `status` 命令，每周末进行一次全面回顾。

## 其他说明：
- SQLite 中的事件记录为只读（仅允许追加数据）。
- 损益（PnL）是通过重新执行所有交易事件来计算的。
- `status` 命令会根据每个 `symbol` 和 `mint` 的组合使用最新的快照来计算未实现的损益。

## 验证**

运行完整的模拟交易测试套件：
```bash
node --test {baseDir}/tests/paper_trading.test.mjs
```