---
name: hyperliquid
description: 交易和监控 Hyperliquid 永续期货。可以查看账户余额、持仓情况（包括盈亏），下达/取消交易订单，以及执行市场交易。当用户咨询 Hyperliquid 的交易相关事宜、投资组合状态、加密货币持仓情况，或希望进行 Hyperliquid 交易时，可使用该功能。
---

# Hyperliquid 交易技能

适用于 Hyperliquid 永续期货交易所的完整交易和投资组合管理功能。

## 先决条件

只需安装一次依赖项：

```bash
cd skills/hyperliquid/scripts && npm install
```

## 认证

**仅用于读取操作（余额、持仓、价格）：**
- 设置 `HYPERLIQUID_ADDRESS` 环境变量
- 不需要私钥

**用于交易操作：**
- 设置 `HYPERLIQUID_PRIVATE_KEY` 环境变量
- 地址会从私钥自动生成

**测试网：**
- 设置 `HYPERLIQUID_TESTNET=1` 以使用测试网

## 核心操作

### 投资组合监控

**检查余额：**
```bash
HYPERLIQUID_ADDRESS=0x... node scripts/hyperliquid.mjs balance
```

**查看持仓及盈亏情况：**
```bash
HYPERLIQUID_ADDRESS=0x... node scripts/hyperliquid.mjs positions
```

**查看未成交订单：**
```bash
HYPERLIQUID_ADDRESS=0x... node scripts/hyperliquid.mjs orders
```

**查看交易历史：**
```bash
HYPERLIQUID_ADDRESS=0x... node scripts/hyperliquid.mjs fills
```

**查询某种币的价格：**
```bash
node scripts/hyperliquid.mjs price BTC
```

### 交易操作

所有交易命令都需要 `HYPERLIQUID_PRIVATE_KEY`。

**下达限价单：**
```bash
# Buy 0.1 BTC at $45,000
HYPERLIQUID_PRIVATE_KEY=0x... node scripts/hyperliquid.mjs buy BTC 0.1 45000

# Sell 1 ETH at $3,000
HYPERLIQUID_PRIVATE_KEY=0x... node scripts/hyperliquid.mjs sell ETH 1 3000
```

**市价单（带有 5% 的滑点保护）：**
```bash
# Market buy 0.5 BTC
HYPERLIQUID_PRIVATE_KEY=0x... node scripts/hyperliquid.mjs market-buy BTC 0.5

# Market sell 2 ETH
HYPERLIQUID_PRIVATE_KEY=0x... node scripts/hyperliquid.mjs market-sell ETH 2
```

**取消订单：**
```bash
# Cancel specific order
HYPERLIQUID_PRIVATE_KEY=0x... node scripts/hyperliquid.mjs cancel BTC 12345

# Cancel all orders
HYPERLIQUID_PRIVATE_KEY=0x... node scripts/hyperliquid.mjs cancel-all

# Cancel all orders for specific coin
HYPERLIQUID_PRIVATE_KEY=0x... node scripts/hyperliquid.mjs cancel-all BTC
```

## 输出格式

所有命令的输出均为 JSON 格式。需要解析后以适合聊天的方式显示：

**对于余额/投资组合：**
- 显示总资产、可用余额
- 列出持仓信息（数量、入场价格、未实现盈亏）
- 总结未成交订单

**对于交易执行：**
- 在执行前确认订单详情
- 执行后报告订单 ID 和状态
- 如果立即成交，显示成交价格

## 安全指南

**在执行交易前：**
1. 与用户确认交易参数（币种、数量、方向、价格）
2. 显示当前价格和持仓情况
3. 计算预估成本/收益

**持仓规模控制：**
- 如果交易金额超过账户资产的 20%，则发出警告
- 根据账户余额建议合适的交易规模

**价格检查：**
- 对于限价单，将限价与当前市场价格进行比较
- 如果限价与市场价格相差超过 5%，则发出警告（可能是输入错误）

## 错误处理

**常见错误：**
- “需要地址” → 请设置 `HYPERLIQUID_ADDRESS` 或 `HYPERLIQUID_PRIVATE_KEY`
- “需要私钥” → 交易操作需要 `HYPERLIQUID_PRIVATE_KEY`
- “未知币种” → 使用 `meta` 命令检查可交易的币种
- HTTP 错误 → 检查网络连接和 API 状态

**发生错误时：**
- 向用户显示错误信息
- 建议解决方法（设置环境变量、检查币种名称、验证余额）
- 不要自动重试交易

## 工作流程示例

**“我的 Hyperliquid 投资组合情况如何？”**
1. 运行 `balance` 命令获取总资产
2. 运行 `positions` 命令获取持仓信息
3. 格式化输出：总资产、持仓情况及未实现盈亏

**“在 Hyperliquid 上购买 0.5 BTC”**
1. 运行 `price BTC` 命令获取当前价格
2. 运行 `balance` 命令确认资金充足
3. 与用户确认：“以当前价格购买 0.5 BTC？当前价格：$X。预估成本：$Y”
4. 执行 `market-buy BTC 0.5` 命令
5. 报告订单结果

**“Hyperliquid 上的 BTC 当前价格是多少？”**
1. 运行 `price BTC` 命令
2. 格式化输出：“Hyperliquid 上的 BTC 价格为 $X”

**“关闭我的 ETH 持仓”**
1. 运行 `positions` 命令获取当前 ETH 持仓数量
2. 如果是多头持仓 → 以市价卖出；如果是空头持仓 → 以市价买入
3. 根据持仓数量执行交易
4. 报告交易结果

## 高级功能

**列出所有可交易的币种：**
```bash
node scripts/hyperliquid.mjs meta
```

**查询其他地址：**
```bash
# Check someone else's positions (read-only, public data)
node scripts/hyperliquid.mjs positions 0x1234...
```

## 注意事项

- 所有数量单位均为基础货币（BTC、ETH 等）
- 价格以美元（USD）显示
- 市价单使用带有 5% 滑点保护的限价单
- Hyperliquid 支持的是永久期货交易，而非现货交易
- 请参阅 `references/api.md` 以获取完整的 API 文档