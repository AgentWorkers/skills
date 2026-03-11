---
name: mock-trading-agent
description: 使用算法策略（如SMA交叉信号、均值回归）来模拟加密货币交易，而无需实际投入资金。适用于用户希望开始模拟交易、测试交易机器人或监控模拟投资组合的场景。
---
# 模拟交易代理技能

该技能提供了一个功能齐全的模拟（纸面）交易环境，允许 OpenClaw 通过获取实时市场数据、评估交易策略并更新虚拟投资组合来模拟算法交易。

## 组件

- **`assets/portfolio.json`**：一个包含 10,000 美元的虚拟银行账户模板。
- **`scripts/mock_bot.py`**：一个 Python 脚本，用于执行交易机器人的一个“交易周期”（包括获取数据、评估策略、执行模拟交易以及更新投资组合文件）。

## 设置与使用方法

当用户请求开始模拟交易会话时：

1. **初始化投资组合**：
   将模板投资组合复制到用户的工作目录中。
   ```bash
   cp {baseDir}/assets/portfolio.json ./my_portfolio.json
   ```

2. **运行交易周期**：
   运行该脚本。该脚本会执行一个完整的交易周期（包括获取数据、评估策略、执行交易以及保存结果）。
   ```bash
   uv run {baseDir}/scripts/mock_bot.py --portfolio ./my_portfolio.json --asset bitcoin
   ```

3. **自动化（Heartbeat/Cron）**：
   要让机器人持续运行，可以将步骤 2 中的命令添加到用户的 `HEARTBEAT.md` 文件中，或者通过 Cron 任务设置为每 5-10 分钟运行一次。

4. **报告**：
   读取 `./my_portfolio.json` 文件以获取用户的当前盈亏（PnL）、现金余额和交易历史记录。

## 修改策略
当前脚本默认使用 **SMA Crossover** 策略。如果用户需要不同的交易逻辑，可以本地编辑 Python 脚本，将其替换为均值回归（Mean Reversion）、动量突破（Momentum Breakout）或相对强弱指数（RSI）策略。