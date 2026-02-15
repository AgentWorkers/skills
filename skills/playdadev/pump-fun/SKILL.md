---
name: pump-fun
description: 使用 PumpPortal API 在 Pump.fun 上购买、出售和发行代币。
homepage: https://pump.fun
user-invocable: true
metadata: {"moltbot":{"requires":{"env":["SOLANA_PRIVATE_KEY"]},"primaryEnv":"SOLANA_PRIVATE_KEY"}}
---

# Pump.fun 交易技能

该技能允许通过 PumpPortal API 在 Pump.fun 平台上进行交易和发行代币。

## 命令

### 购买代币
通过指定代币的发行地址和数量，在 Pump.fun 上购买代币。

**用法：** `/pump-buy <发行地址> <数量 SOL> [滑点]`

**示例：**
- `/pump-buy 7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU 0.1` - 购买价值 0.1 SOL 的代币
- `/pump-buy 7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU 0.5 15` - 以 15% 的滑点购买代币

### 卖出代币
通过指定代币的发行地址和数量，在 Pump.fun 上出售代币。

**用法：** `/pump-sell <发行地址> <数量|百分比> [滑点]`

**示例：**
- `/pump-sell 7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU 1000000` - 出售 1,000,000 个代币
- `/pump-sell 7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU 100%` - 出售所有代币
- `/pump-sell 7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU 50% 10` - 以 10% 的滑点出售 50% 的代币

### 发行代币
在 Pump.fun 上创建并发行新的代币。

**用法：** `/pump-launch <名称> <符号> <描述> [开发者购买数量 SOL]`

**示例：**
- `/pump-launch "My Token" MTK "一种革命性的代币" 1` - 以 1 SOL 的开发者购买数量发行代币
- `/pump-launch "Cool Coin" COOL "有史以来最酷的代币"` - 使用默认的开发者购买数量发行代币

## 配置

### 必需的环境变量
- `SOLANA_PRIVATE_KEY` - 你的 Solana 钱包私钥（base58 编码）

### 可选的环境变量
- `SOLANA_RPC_URL` - 自定义 RPC 端点（默认为公共主网）
- `PUMP_PRIORITY_FEE` - 优先级费用（单位：SOL，默认值为 0.0005）
- `PUMP_DEFAULT_SLIPPAGE` - 默认滑点百分比（默认值为 10）

## 设置

1. 安装依赖项：
   ```bash
   cd {baseDir}
   npm install
   ```

2. 设置环境变量：
   ```bash
   export SOLANA_PRIVATE_KEY="your-base58-private-key"
   ```

3. （可选）配置自定义 RPC：
   ```bash
   export SOLANA_RPC_URL="https://your-rpc-endpoint.com"
   ```

## 安全提示

- 切勿共享你的私钥
- 使用专用的交易钱包，并控制资金规模
- 从少量交易开始进行测试
- 该技能使用本地交易 API 以确保最高安全性（交易在本地签名）

## 费用

- PumpPortal 对每笔交易收取 0.5% 的费用
- 遵循标准的 Solana 网络费用规则
- 优先级费用可以自定义

## 支持的池

该技能会自动选择最佳的交易池，但支持以下类型：
- `pump` - Pump.fun 的债券曲线池
- `raydium` - Raydium 的自动做市商（AMM）池
- `pump-amm` - Pump.fun 的自动做市商池
- `auto` - 自动选择交易池（默认值）