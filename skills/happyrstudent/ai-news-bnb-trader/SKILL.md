---
name: ai-news-bnb-trader
description: TypeScript（基于Node.js 20+）开发的AI驱动的BNB策略交易机器人，专为BSC（Binance Smart Chain）设计。适用于需要事件/新闻情感分析信号、严格风险控制功能，以及自动化WBNB（Binance Coin）与稳定币之间兑换的用户。该机器人具备试运行安全机制、紧急模式、状态监控以及交易批准/撤销工具。
---
# AI新闻驱动的BNB交易机器人

该机器人使用新闻情感分析及风险控制机制来运行基于事件的BSC（Binance Smart Chain）交易策略。

## 安全性优先

- 默认设置为 `DRY_RUN=true`（即仅执行交易逻辑，不生成日志）。
- 绝不在日志中打印私钥或种子短语。
- 仅允许交易以下资产：`WBNB`、`USDT`、`BUSD` 和 `USDC`。
- 进入恐慌模式时会立即停止所有交易操作。

## 命令

```bash
npm run start -- start
npm run start -- status
npm run start -- panic
npm run start -- revoke-approvals
npm run key:encrypt -- --out ./secrets/key.json
```

## 新闻获取方式

- 每 `NEWS POLL_SECONDS` 秒通过 `NEWS_API_URL` 调用REST接口获取新闻数据。
- 可选地，也可以通过 `NEWS_WS_URL` 使用WebSocket实时获取新闻数据。
- 两种方式都会根据 `news.id` 去重处理数据，并在请求失败时采用指数级重试策略。

## 信号模型

- **RuleSignalModel**（默认）：基于关键词规则进行交易决策，同时提供详细的决策理由。
- **OpenAISignalModel**（可选）：在设置了 `OPENAI_API_KEY` 时启用；该模型结合OpenAI API进行智能分析，若API请求失败则回退至规则判断。

## 交易策略

- 当 `sentiment * impact >= BUY_THRESHOLD` 且 `confidence >= MIN_CONF` 时，买入WBNB并转换为稳定币。
- 当 `sentiment * impact <= -SELL_THRESHOLD` 且 `confidence >= MIN_CONF` 时，卖出WBNB并转换为稳定币。
- 在执行任何交易前，必须满足所有设定的风险控制条件。

## 风险控制措施

- 设置订单的最大名义金额、最大持仓比例以及每日交易限额。
- 实施每日最大亏损限制（基于市场价值MTM计算）。
- 设置基于平均买入价的止盈（TP）和止损（SL）目标。
- 交易之间有冷却时间间隔。
- 限制交易过程中的滑点幅度。
- 如果连续多次请求失败，系统将自动进入安全模式（SAFE_MODE）。

## 其他注意事项

- 如果提供了私有RPC接口（`PRIVATE_RPC_URL`），请优先使用该接口进行通信。
- 在生产环境中，需要验证相关代币/去中心化交易所（DEX）的地址，并加强市场有效性（MEV）保护机制。