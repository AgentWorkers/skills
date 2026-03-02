---
name: polymarket-mert-sniper
displayName: Mert Sniper
description: 在 Polymarket 上，存在接近到期的“定罪交易”（conviction trading）策略。当市场概率严重失衡时，这种交易策略可能会带来较高的收益。你可以按主题筛选交易机会，设定投注上限，并且只在截止日期临近时交易那些具有较高潜力的股票（即那些价格波动较大的股票）。
metadata: {"clawdbot":{"emoji":"🎯","requires":{"env":["SIMMER_API_KEY"],"pip":["simmer-sdk"]},"cron":null,"autostart":false,"automaton":{"managed":true,"entrypoint":"mert_sniper.py"},"tunables":[{"env":"SIMMER_MERT_MAX_BET_USD","type":"number","default":50,"range":[1,200],"step":5,"label":"Max bet per trade"},{"env":"SIMMER_MERT_EXPIRY_MINUTES","type":"number","default":30,"range":[5,120],"step":5,"label":"Order expiry (minutes)"},{"env":"SIMMER_MERT_MIN_SPLIT","type":"number","default":0.10,"range":[0.01,0.50],"step":0.01,"label":"Minimum probability split"},{"env":"SIMMER_MERT_MAX_TRADES_PER_RUN","type":"number","default":5,"range":[1,20],"step":1,"label":"Max trades per run"},{"env":"SIMMER_MERT_SIZING_PCT","type":"number","default":0.10,"range":[0.01,1.0],"step":0.01,"label":"Position sizing percentage"}]}}
authors:
  - Simmer (@simmer_markets)
attribution: "Strategy inspired by @mert — https://x.com/mert/status/2020216613279060433"
version: "1.0.7"
difficulty: advanced
published: true
---
# Mert Sniper

这是一个用于在Polymarket上进行交易策略执行的脚本，专注于在合约即将到期时进行交易（尤其是当赔率严重失衡时）。该策略由[@mert](https://x.com/mert/status/2020216613279060433)设计，提供了详细的实现细节。

**策略要点：**
- 根据主题筛选市场；
- 限制每次交易的投注金额；
- 仅在市场即将到期时进行交易；
- 仅选择赔率严重失衡（例如60/40或更高）的市场进行交易。

**注意：**  
- 该脚本仅适用于Polymarket平台，并且所有交易均使用真实的USDC进行。  
- 使用`--live`参数可进行实时交易，否则为模拟交易。

**适用场景：**
- 当用户希望交易那些即将到期的合约时；
- 希望根据特定主题（如SOLANA或加密货币市场）进行筛选；
- 希望限制每次交易的投注金额（例如不超过10美元）；
- 希望仅在赔率严重失衡时进行交易；
- 希望运行自动化的交易策略。

**设置流程：**
1. **获取Simmer API密钥**：  
   - 从simmer.markets/dashboard的SDK选项卡中获取API密钥，并将其存储在环境变量`SIMMER_API_KEY`中。
2. **获取钱包私钥**（用于实时交易）：  
   - 这是用户在Polymarket平台上使用的钱包私钥（用于存储USDC）。  
   - 将其存储在环境变量`WALLET_PRIVATE_KEY`中。SDK会使用该密钥在客户端自动签署交易订单，无需手动操作。
3. **配置策略参数**：  
   - **市场筛选**：指定需要扫描的市场（默认为所有市场）；  
   - **最大投注额**：每次交易的最大金额（默认为10美元）；  
   - **到期时间窗口**：设置市场在多少分钟内到期（默认为2分钟）；  
   - **最小赔率差**：只有当赔率达到或超过此值时才进行交易（默认为60/40）；  
   - **每次扫描的最大交易次数**：每次扫描周期内允许的最大交易次数（默认为5次）；  
   - **智能投注比例**：每次交易占余额的百分比（默认为0.05%）。

**配置文件示例（config.json）：**
```json
{
  "SIMMER_MERT_FILTER": "solana",
  "SIMMER_MERT_MAX_BET": 10.00,
  "SIMMER_MERT_EXPIRY_MINS": 2,
  "SIMMER_MERT_MIN_SPLIT": 0.60,
  "SIMMER_MERT_MAX_TRADES": 5,
  "SIMMER_MERT_SIZING_PCT": 0.05
}
```

**常用命令：**
（此处省略了具体的命令示例，因为它们通常与API调用相关。）

**API参考：**
- 基础URL：`https://api.simmer.markets`
- 认证方式：`Authorization: Bearer $SIMMER_API_KEY`
- 财产信息：`GET /api/sdk/portfolio`
- 交易头寸：`GET /api/sdk/positions`

**运行脚本：**
（此处省略了脚本的运行命令，因为它们通常依赖于特定的命令行参数或工具。）

**工作原理：**
- 脚本会定期从Simmer API获取活跃市场列表（可根据需要通过标签或关键词进行筛选）；
- 筛选出在指定时间内到期的市场；
- 检查市场的价格赔率差，仅当赔率差达到或超过最小阈值时才进行交易；
- 确定交易方向（选择赔率较高的那一方）；
- 实施交易（投注金额不超过最大限额）；
- 提供已扫描、筛选和已交易市场的汇总信息。

**示例输出：**
（此处省略了示例输出，因为具体的输出格式可能因市场数据和策略设置而异。）

**故障排除：**
- **“未找到市场”**：检查筛选条件；如果没有筛选条件，可以尝试直接运行脚本。
- **“没有在指定时间内到期的市场”**：增加到期时间窗口（例如`--expiry 10`）；或者增加扫描频率（例如使用cron任务每分钟扫描一次）。
- **“赔率差太小”**：降低最小赔率阈值（例如`--set min_split=0.55`）；这样虽然交易频率会增加，但投注金额可能会减少。
- **对于15分钟周期的市场，到期时间为17小时”**：Polymarket的`endDate`指的是整个平台的日终时间，而非单个市场的实际收盘时间。对于15分钟的加密货币市场，实际收盘时间需要根据具体情况确定。可以调整到期时间窗口（例如`--expiry 1080`），或者使用赔率筛选条件来寻找交易机会。
- **“外部钱包需要预签名订单”**：确保`WALLET_PRIVATE_KEY`已正确设置；SDK会自动处理订单签署。
- **“余额显示为0美元，但我有USDC在Polygon上”**：Polymarket使用的是`USDC.e`（一种桥接后的USDC形式，合约地址为`0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174`）。如果最近将USDC桥接到了Polygon，可能需要将`USDC.e`转换为原生USDC后再尝试交易。
- **“API密钥无效”**：从simmer.markets/dashboard的SDK选项卡中重新获取API密钥。

请注意，这些说明基于提供的SKILL.md文件内容。在实际使用中，可能需要根据具体需求和环境进行调整。