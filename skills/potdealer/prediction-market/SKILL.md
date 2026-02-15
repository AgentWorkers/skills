# 花园温度预测市场（Garden Temp Market, GTM）技能

在 Base 平台上参与每日花园温度预测市场。

## 合同信息

**地址**: `0xA3F09E6792351e95d1fd9d966447504B5668daF6`  
**链**: Base（链 ID：8453）  
**RPC**: `https://mainnet.base.org`  

## 游戏规则

预测今日 18:00 UTC 的花园温度是高于还是低于昨日的温度：  
- **HIGHER**：预测今日的温度高于昨日  
- **LOWER**：预测今日的温度低于或等于昨日  

- 胜者将按比例获得 98% 的奖金池  
- 如果比赛结果平局，奖金池将顺延至下一天；单边预测失败的用户将获得退款  

## 查看市场状态  

### 获取完整市场信息  

```bash
cast call 0xA3F09E6792351e95d1fd9d966447504B5668daF6 \
  "getMarketState()(uint256,int256,uint256,uint256,uint256,bool,uint256,uint256)" \
  --rpc-url https://mainnet.base.org
```  

返回的信息顺序如下：  
1. `round`（uint256）：当前轮次编号  
2. `baseline`（int256）：昨日的温度（单位：°C，例如 1210 表示 12.10°C）  
3. `higherTotal`（uint256）：选择 “HIGHER” 方案的投注金额（单位：wei）  
4. `lowerTotal`（uint256）：选择 “LOWER” 方案的投注金额（单位：wei）  
5. `rollover`（uint256）：平局情况下的奖金池金额（单位：wei）  
6. `isBettingOpen`（bool）：当前是否可以下注  
7. `secondsUntilClose`（uint256）：距离投注截止的时间（秒）  
8. `secondsUntilSettle`（uint256）：距离结算的时间（秒）  

### 单个查询  

```bash
# Yesterday's baseline (divide by 100 for °C)
cast call 0xA3F09E6792351e95d1fd9d966447504B5668daF6 "yesterdayTemp()(int256)" --rpc-url https://mainnet.base.org

# Is betting open?
cast call 0xA3F09E6792351e95d1fd9d966447504B5668daF6 "bettingOpen()(bool)" --rpc-url https://mainnet.base.org

# Pool sizes (wei)
cast call 0xA3F09E6792351e95d1fd9d966447504B5668daF6 "higherPool()(uint256)" --rpc-url https://mainnet.base.org
cast call 0xA3F09E6792351e95d1fd9d966447504B5668daF6 "lowerPool()(uint256)" --rpc-url https://mainnet.base.org

# Check my bet (returns higherAmt, lowerAmt in wei)
cast call 0xA3F09E6792351e95d1fd9d966447504B5668daF6 "getMyBet(address)(uint256,uint256)" YOUR_ADDRESS --rpc-url https://mainnet.base.org

# Minimum bet (wei)
cast call 0xA3F09E6792351e95d1fd9d966447504B5668daF6 "minBet()(uint256)" --rpc-url https://mainnet.base.org
```  

## 下注操作  

### 函数选择器  

| 函数 | 选择器 |  
|---------|---------|  
| `betHigher()` | `0xb8b2e5f7` |  
| `betLower()` | `0x7a5ce755` |  

### 使用 Bankr Direct API 下注  

- **投注 0.01 ETH 选择 “HIGHER” 方案**：  
```json
{
  "to": "0xA3F09E6792351e95d1fd9d966447504B5668daF6",
  "data": "0xb8b2e5f7",
  "value": "10000000000000000",
  "chainId": 8453
}
```  
- **投注 0.01 ETH 选择 “LOWER” 方案**：  
```json
{
  "to": "0xA3F09E6792351e95d1fd9d966447504B5668daF6",
  "data": "0x7a5ce755",
  "value": "10000000000000000",
  "chainId": 8453
}
```  
- 通过 Bankr 提交投注：  
```
Submit this transaction:
{"to":"0xA3F09E6792351e95d1fd9d966447504B5668daF6","data":"0xb8b2e5f7","value":"10000000000000000","chainId":8453}
```  

### 使用 cast 工具下注  

```bash
# Bet HIGHER
cast send 0xA3F09E6792351e95d1fd9d966447504B5668daF6 "betHigher()" \
  --value 0.01ether --rpc-url https://mainnet.base.org --private-key $KEY

# Bet LOWER
cast send 0xA3F09E6792351e95d1fd9d966447504B5668daF6 "betLower()" \
  --value 0.01ether --rpc-url https://mainnet.base.org --private-key $KEY
```  

## 单位转换  

| ETH | Wei |  
|------|------|  
| 0.001 | 1000000000000000 |  
| 0.005 | 5000000000000000 |  
| 0.01 | 1000000000000000 |  
| 0.05 | 5000000000000000 |  
| 0.1 | 10000000000000000 |  

**最低投注金额**：0.001 ETH = 1000000000000000 wei  

## 时间安排  

| 时间（UTC） | 事件 |  
|---------|-------|  
| 结算后 | 开始下注 |  
| 12:00 | 关闭下注 |  
| 18:00 | 结算并支付奖金 |  

## 规则：  
- 每个地址每轮只能下一次注（选择 “HIGHER” 或 “LOWER”，不能同时选择两者）  
- 每个选项最多允许 200 位投注者  
- 如果平局，奖金池将顺延至下一天；  
- 单边预测失败的用户将获得退款  

## 示例代理策略  

```python
# Pseudocode for an agent betting strategy

# 1. Check if betting is open
is_open = call("bettingOpen()")
if not is_open:
    print("Betting closed, wait for next round")
    return

# 2. Get market state
state = call("getMarketState()")
baseline = state[1] / 100  # Convert to °C
higher_pool = state[2]
lower_pool = state[3]

# 3. Check weather forecast (external API)
forecast = get_weather_forecast()
expected_temp = forecast["temp_18utc"]

# 4. Decide bet
if expected_temp > baseline + 0.5:  # Confident it's warmer
    side = "HIGHER"
elif expected_temp < baseline - 0.5:  # Confident it's colder
    side = "LOWER"
else:
    print("Too close to call, skip this round")
    return

# 5. Consider odds (bet against crowd for better payout)
if side == "HIGHER" and higher_pool > lower_pool * 2:
    print("Pool is lopsided, might skip or bet small")

# 6. Place bet
amount = 0.01  # ETH
submit_bet(side, amount)
```  

## 需要监控的事件  

```solidity
event BetPlaced(uint256 indexed round, address indexed bettor, bool isHigher, uint256 amount, int256 baseline);
event RoundSettled(uint256 indexed round, int256 todayTemp, int256 yesterdayTemp, bool higherWon, bool wasTie, uint256 totalPot, uint256 houseFee);
event WinningsClaimed(uint256 indexed round, address indexed bettor, uint256 amount);
```  

## SensorNet 参考  

温度数据来自 Netclawd 的 SensorNet：  
- 合同地址：`0xf873D168e2cD9bAC70140eDD6Cae704Ed05AdEe0`  
- SensorNet 会将温度数据以消息形式发送至 Net Protocol  
-Keeper 负责读取数据并提交至结算系统  

## 相关链接：  
- Basescan：https://basescan.org/address/0xA3F09E6792351e95d1fd9d966447504B5668daF6  
- 源代码链接：https://github.com/Potdealer/prediction-market （如代码已公开）  

由 **potdealer** 与 **Ollie** 为 **Netclawd** 共同开发。