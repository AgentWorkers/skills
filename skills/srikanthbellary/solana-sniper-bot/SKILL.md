---
name: solana-sniper-bot
description: 这是一个自主运行的Solana代币狙击和交易机器人。它能够监控Raydium/Jupiter平台上新发行的代币，利用大型语言模型（LLM）进行分析以评估代币的潜在风险，自动购买有潜力的新代币，并管理交易策略的退出机制。用户可以使用该机器人来狙击Solana代币的发行机会、交易加密货币（memecoins）、监控新的Solana交易对（currency pairs），或者构建自己的Solana交易机器人。该机器人支持基于Cron任务的自动监控功能，具备设置获利止损点（take-profit/stop-loss）以及管理投资组合（portfolio tracking）的能力。
metadata: {"openclaw": {"requires": {"env": ["SOLANA_PRIVATE_KEY", "LLM_API_KEY"]}, "primaryEnv": "LLM_API_KEY", "homepage": "https://github.com/srikanthbellary"}}
---

# Solana Sniper Bot

这是一个用于Solana网络的自动化代币交易机器人。它通过监控Raydium和Jupiter平台上的新流动性池，利用大语言模型（LLM）来检测潜在的“rugpull”（欺诈性代币发行）行为，并通过Jupiter聚合器执行买入/卖出交易。

## 先决条件

- **Solana钱包**：需要持有SOL代币作为交易手续费以及交易资金（建议使用USDC或SOL）
- **Anthropic API密钥**：用于代币评估（每次评估费用约为0.001美元）
- **Helius或QuickNode RPC服务**：免费 tier可用，但推荐使用付费服务以获得更快的处理速度

## 设置

### 1. 安装依赖项

```bash
python3 {baseDir}/scripts/setup.sh
```

或者手动安装：

```bash
pip install solana solders httpx aiohttp python-dotenv
```

### 2. 配置

创建`.env`文件：

```
SOLANA_PRIVATE_KEY=<base58-private-key>
LLM_API_KEY=<anthropic-api-key>
RPC_URL=https://api.mainnet-beta.solana.com
HELIUS_API_KEY=<optional-for-faster-monitoring>
BUY_AMOUNT_SOL=0.1
TAKE_PROFIT=2.0
STOP_LOSS=0.5
```

### 3. 部署

```bash
cp {baseDir}/scripts/sniper.py /opt/sniper/
python3 /opt/sniper/sniper.py
```

## 工作原理

1. **池监控**：实时监控Raydium的自动市场机制（AMM）平台，以发现新的流动性池创建事件。
2. **代币分析**：针对每个新创建的流动性池，查询代币的元数据：
   - 发行代币的权限（如果权限已被撤销，则视为安全风险）
   - 代币的锁定状态（如果权限已被撤销，则视为安全风险）
   - 流动性提供者（LP）的锁定比例
   - 前十大持有者的持股比例
   - 合同的验证状态
3. **LLM风险评估**：将代币数据发送给Claude Haiku大语言模型，以评估其是否存在“rugpull”风险。
4. **自动买入**：如果风险评分低于预设阈值，通过Jupiter聚合器以最优价格买入代币。
5. **头寸管理**：设置盈利和止损触发条件，以管理交易头寸。
6. **自动卖出**：当达到预设的盈利目标（TP）或止损点（SL）时，通过Jupiter平台卖出代币。

## 风险评分

每个代币的风险评分范围为0-100分（分数越低，风险越低）：

| 评估因素 | 权重 | 风险提示 |
|--------|--------|----------|
| 发行代币的权限 | 25% | 权限未被撤销 |
| 代币的锁定状态 | 20% | 权限未被撤销 |
| 流动性提供者的锁定比例 | 20% | 锁定比例低于80% |
| 前十大持有者 | 15% | 持有比例超过50% |
| 合同创建时间 | 10% | 合同创建时间小于1小时 |
| LLM评估结果 | 10% | 评估结果为负面 |

默认的买入阈值：风险评分低于40分。

## 交易参数

这些参数可以在`.env`文件中配置：
- `BUY_AMOUNT_SOL`：每次交易的买入金额（默认：0.1 SOL）
- `TAKE_PROFIT`：盈利退出倍数（默认：2.0，表示100%的收益）
- `STOP_LOSS`：止损退出倍数（默认：0.5，表示50%的损失）
- `MAX_POSITIONS`：同时持有的最大交易数量（默认：5）
- `MIN_LIQUIDITY`：最低池流动性（以美元计，默认：5000美元）
- `SLIPPAGE_BPS`：滑点容忍度（以百万分之一计，默认：500）

## ⚠️ 安全注意事项

- **使用专用钱包**，并且只投入你能承受损失的资金。
- **memecoin（低质量代币）的交易风险极高**——大多数新发行的memecoin最终价值会归零。
- **切勿使用你的主钱包私钥**。
- **从少量资金开始交易（每次交易0.01-0.1 SOL）**。
- **持续监控交易情况**——本系统并非“一次设置即可长期使用”的工具。
- **注意RPC服务的使用限制**：免费的Solana RPC服务可能无法及时处理快速的交易请求。建议使用Helius或QuickNode等付费服务。

## 参考资料

- 有关Jupiter聚合器API的详细信息，请参阅`references/jupiter-api.md`。
- 有关流动性池监控的详细信息，请参阅`references/raydium-pools.md`。