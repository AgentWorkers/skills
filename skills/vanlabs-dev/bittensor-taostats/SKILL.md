# TaoStats 技能

**用途**：与 TaoStats API 进行交互，以获取 Bittensor 区块链的数据——包括子网、验证器、矿工、质押情况、排放量等信息。

**API 文档**：https://docs.taostats.io/  
**基础 URL**：`https://api.taostats.io`  
**速率限制**：每分钟 5 次调用（免费 tier）

---

## 设置

### 1. 设置 API 密钥
从 [taostats.io](https://taostats.io) 获取免费的 API 密钥，并将其设置为环境变量：
```bash
export TAOSTATS_API_KEY="tao-xxxxx:yyyyy"
```

### 2. 辅助函数
```bash
source ~/.openclaw/workspace/skills/taostats/taostats.sh
```

---

## 完整的端点参考

### dTAO 池端点

#### `GET /api/dtao/pool/latest/v1?netuid={N}`
**关键**：此端点包含了所有用于交易决策的信息。

**关键字段**：
- `price` - 当前的 alpha 价格（以 TAO 为单位）
- `root_prop` - 来自根节点的 TAO 注入比例（对入场决策至关重要）
- `fear_and_greed_index` / `fear_and_greed_sentiment` - 市场情绪
- `seven_day_prices` - 历史价格数组（42 个数据点）
- `price_change_1_hour`, `price_change_1_day`, `price_change_1_week`, `price_change_1_month`
- `market_cap`, `liquidity`, `total_tao`, `total_alpha`
- `tao_volume_24_hr`, `alpha_volume_24_hr`, `buys_24_hr`, `sells_24_hr`
- `highest_price_24_hr`, `lowest_price_24_hr`

**示例**：
```bash
curl -s "https://api.taostats.io/api/dtao/pool/latest/v1?netuid=33" \
  -H "Authorization: $TAOSTATS_API_KEY" | jq '.data[0].root_prop'
# Returns: "0.2104087259347016725" (21% - GOOD entry)
```

#### `GET /api/dtao/pool/history/v1?netuid={N}&limit={L>`
用于回测的历史池快照。

#### `GET /api/dtao/validator/yield/latest/v1?netuid={N}`
多个时间段的验证器年化收益率（APY）。

**关键字段**：
- `seven_day_apy` - 主要的质押决策指标
- `one_day_apy`, `one_hour_apy`, `thirty_day_apy`
- `seven_day_epoch_participation` - 验证器的可靠性
- `name`, `hotkey.ss58`, `stake`, `take`

**示例**：
```bash
curl -s "https://api.taostats.io/api/dtao/validator/yield/latest/v1?netuid=33" \
  -H "Authorization: $TAOSTATS_API_KEY" | \
  jq -r '.data | sort_by(-.seven_day_apy) | .[0] | 
  "\(.name // .hotkey.ss58): \(.seven_day_apy * 100)% APY"'
```

#### `GET /api/dtao/stake_balance/latest/v1?coldkey={COLDKEY>`
所有子网中的质押位置信息。

**关键字段**：
- `netuid`, `hotkey.ss58`, `hotkey_name`
- `balance_as_tao` - 以 RAO 为单位（需除以 1e9）
- `price`, `price_change_1_day`
- `root_prop` - 每个位置的根节点比例

### 子网端点

#### `GET /api/subnet/latest/v1` 或 `?netuid={N>`
完整的子网参数和经济信息。

**关键字段**：
- `netuid`, `emission`, `projected_emission`
- `net_flow_1_day`, `net_flow_7_days`, `net_flow_30_days` - 资本流动情况
- `recycled_24_hours`, `recycled_lifetime` - 注册经济信息
- `tao_flow`, `excess_tao` - dTAO 机制相关数据
- `immune_owner_uids_limit`, `immunity_period` - 风险评估
- `max_validators`, `active_validators`
- `difficulty`, `adjustment_alpha` - 矿工经济信息

#### `GET /api/subnet/registration/v1?netuid={N}`
子网注册详情。

**关键字段**：
- `owner.ss58` - 子网所有者
- `registration_cost` - 当前的注册费用
- `timestamp` - 注册时间

### 验证器端点

#### `GET /api/validator/latest/v1?netuid={N}`
当前验证器的状态。

**关键字段**：
- `apr`, `apr_7_day_average`, `apr_30_day_average`
- `nominator_return_per_k` - 每 1000 TAO 的提名者收益
- `nominators`, `nominators_24_hr_change` - 资本流入/流出
- `stake`, `stake_24_hr_change`, `validator_stake`, `system_stake`
- `take` - 手续费率
- `name`, `coldkey.ss58`, `hotkey.ss58`
- `permits` - 子网权限

#### `GET /api/validator/history/v1?netuid={N}&hotkey={H}&limit={L}`
验证器的历史性能数据。

**关键字段**：
- 所有 APR 指标（按天显示）
- `nominators_24_hr_change` - 资本流动情况
- `dominance`, `subnet_dominance` - 市场份额

### 交易端点

#### `GET /api/delegation/v1?nominator={COLDKEY}&action={all|stake|unstake}&limit={L}`
完整的交易历史记录（质押、解质押、转账）。

**关键字段**：
- `action` ("add" = 质押, "remove" = 解质押)
- `amount`, `rate` (价格), `tao_amount`, `alpha_amount`
- `fee`, `slippage`
- `block_number`, `timestamp`
- `hotkey.ss58`, `coldkey.ss58`

#### `GET /api/transfer/v1?from={COLDKEY}&limit={L}`
TAO 转账历史记录（非质押相关）。

**关键字段**：
- `from.ss58`, `to.ss58`, `amount`, `fee`
- `block_number`, `timestamp`

### 元图端点

#### `GET /api/metagraph/latest/v1?netuid={N}&limit={L>`
每个节点的完整子网状态。

**关键字段**：
- `uid`, `hotkey.ss58`, `coldkey.ss58`
- `rank`, `trust`, `consensus`, `incentive`, `dividends`, `emission`
- `alpha_stake`, `root_stake`, `total_alpha_stake`
- `daily_mining_alpha`, `daily_validating_alpha`, `daily_reward`
- `validator_permit`, `is_immunity_period`, `in_danger`
- `daily_burned_alpha`, `daily_owner_alpha`

#### `GET /api/neuron/latest/v1?netuid={N}&limit={L>`
简化的节点视图，包含剪枝风险信息。

**关键字段**：
- `uid`, `name`, `hotkey.ss58`, `coldkey.ss58`
- `pruning_score`, `in_danger`, `is_immune`
- `miner_rank`, `validator_rank`

---

## 快速参考

### 获取子网池数据
```bash
taostats_pool 33
# Returns: price, root_prop, fear_and_greed_index, 7-day price history, volume
```

### 获取验证器年化收益率
```bash
taostats_validator_yield 33
# Returns: All validators with 1h/1d/7d/30d APYs
```

### 获取质押余额
```bash
taostats_stake_balance "YOUR_COLDKEY_HERE"
# Returns: All positions with root_prop per subnet
```

### 获取交易历史
```bash
taostats_delegation_history "YOUR_COLDKEY_HERE"
# Returns: All stake/unstake transactions with slippage
```

### 获取子网参数
```bash
taostats_subnet_info 33
# Returns: Emissions, net flows, registration cost, immunity params
```

### 获取元图信息
```bash
taostats_metagraph 33
# Returns: All neurons with stakes, ranks, emissions
```

---

## 常见操作模式

### 检查入场质量（root_prop < 0.30）
```bash
NETUID=33
ROOT_PROP=$(curl -s "https://api.taostats.io/api/dtao/pool/latest/v1?netuid=$NETUID" \
  -H "Authorization: $TAOSTATS_API_KEY" | jq -r '.data[0].root_prop')

if (( $(echo "$ROOT_PROP < 0.30" | bc -l) )); then
  echo "SN$NETUID: GOOD entry (root_prop: $ROOT_PROP)"
else
  echo "SN$NETUID: AVOID (root_prop: $ROOT_PROP - artificial price)"
fi
```

### 为子网寻找最佳验证器
```bash
NETUID=33
curl -s "https://api.taostats.io/api/dtao/validator/yield/latest/v1?netuid=$NETUID" \
  -H "Authorization: $TAOSTATS_API_KEY" | \
  jq -r '.data | sort_by(-.seven_day_apy) | .[0] | 
  "\(.name // .hotkey.ss58) | APY: \(.seven_day_apy * 100)% | Commission: \(.take * 100)%"'
```

### 检查每个位置的 root_prop 情况
```bash
COLDKEY="YOUR_COLDKEY_HERE"
curl -s "https://api.taostats.io/api/dtao/stake_balance/latest/v1?coldkey=$COLDKEY" \
  -H "Authorization: $TAOSTATS_API_KEY" | \
  jq -r '.data[] | 
  "SN\(.netuid): \((.balance_as_tao | tonumber) / 1000000000) TAO | root_prop: \(.root_prop)"'
```

### 寻找高 APY 机会（仅限 S 级别）
```bash
for NETUID in 33 64 51 13 3 1 100; do
  MAX_APY=$(curl -s "https://api.taostats.io/api/dtao/validator/yield/latest/v1?netuid=$NETUID" \
    -H "Authorization: $TAOSTATS_API_KEY" | jq -r '.data | max_by(.seven_day_apy) | .seven_day_apy')
  echo "$NETUID|$MAX_APY"
  sleep 0.3
done | sort -t'|' -k2 -rn | while IFS='|' read netuid apy; do
  printf "SN%-3s: %6.1f%%\n" "$netuid" "$(echo "$apy * 100" | bc -l)"
done
```

### 监控资本流动（net_flow 表示市场趋势）
```bash
curl -s "https://api.taostats.io/api/subnet/latest/v1" \
  -H "Authorization: $TAOSTATS_API_KEY" | \
  jq -r '.data[] | select(.netuid != 0) | 
  "SN\(.netuid): net_flow_7d=\(.net_flow_7_days) | emission=\(.emission)"' | \
  sort -t'=' -k2 -rn | head -10
```

---

## Python 工具

### `taostats_client.py`
一个具有自动重试逻辑的强大 API 客户端。

```python
from taostats_client import TaostatsAPI

api = TaostatsAPI("your-api-key")

# Single call with retry
result = api.get_json("dtao/pool/latest/v1?netuid=33")

# Paginated (handles all pages automatically)
all_data = api.get_paginated("dtao/stake_balance/latest/v1?coldkey=XYZ")

# Balance history
history = api.get_balance_history(coldkey, start_timestamp, end_timestamp)
```

### `balance_history.py`
跟踪随时间变化的每日投资组合情况。

```bash
# View last 30 days
python3 skills/taostats/balance_history.py --days 30

# Export to CSV
python3 skills/taostats/balance_history.py --days 90 --export
```

**输出**：
```
📊 Portfolio History (30 records):
--------------------------------------------------------------------------------
Date         Free τ    Staked τ    Total τ    Daily Δ
--------------------------------------------------------------------------------
2026-01-07   0.0234    1.9567    1.9801            
2026-01-08   0.0256    1.9789    2.0045   +0.0244
...
Overall Change: +0.5399 τ (+27.27%)
```

---

## Bash 脚本（taostats.sh）

### 核心交易功能

#### `taostats_pool <netuid>`
获取包含 root_prop 和市场情绪的完整池数据。
- **返回值**：价格、root_prop、fear_and_greed_index、七天价格、交易量
- **用途**：入场验证、情绪分析、价格历史

#### `taostats_pool_history <netuid> [limit]`
获取历史池快照。
- **返回值**：池状态的时间序列数据
- **用途**：回测、趋势分析

#### `taostats-validator_yield <netuid>`
获取所有验证器的年化收益率。
- **返回值**：1小时/1天/7天/30天的年化收益率、参与率
- **用途**：验证器选择

#### `taostats_stake_balance <coldkey>`
获取每个子网的质押余额及 root_prop。
- **返回值**：每个位置的余额、价格、root_prop
- **用途**：投资组合监控、风险评估

#### `taostats_delegation_history <coldkey> [limit]`
获取包含滑点的交易历史记录。
- **返回值**：质押量、解质押量、手续费、滑点
- **用途**：性能跟踪、税务记录

### 子网分析功能

#### `taostats_subnet_info [netuid]`
子网参数和经济信息。
- **返回值**：排放量、资本流动、注册费用
- **用途**：基本面分析

#### `taostats_subnet_registration <netuid>`
子网所有权和注册详情。
- **返回值**：所有者、注册费用、注册时间
- **用途**：尽职调查

### 验证器分析功能

#### `taostats.validator_info <netuid>`
当前验证器的状态。
- **返回值**：年化收益率、提名者收益、质押变化
- **用途**：深入研究验证器

#### `taostats-validator_history <netuid> <hotkey> [limit]`
验证器的历史性能数据。
- **返回值**：每日年化收益率趋势
- **用途**：验证器可靠性评估

### 元图功能

#### `taostats_metagraph <netuid>`
完整的子网状态。
- **返回值**：所有节点的质押量、排放量、排名
- **用途**：生态系统分析

#### `taostats_neurons <netuid>`
简化的节点视图。
- **返回值**：剪枝分数、免疫状态
- **用途**：风险监控

---

## 速率限制处理

**免费 tier**：每分钟 5 次调用

**最佳实践**：
1. 缓存池数据（变化较慢）
2. 在每次调用之间添加 `sleep 0.3` 的延迟（每分钟 20 次调用是安全的）
3. 尽可能批量处理请求
4. 监控 429 错误代码

**示例速率限制循环**：
```bash
for NETUID in {1..50}; do
  taostats_pool $NETUID | jq -r '.data[0] | "SN\(.netuid): root_prop=\(.root_prop)"'
  sleep 0.3
done
```

---

## 错误处理

| 代码 | 原因 | 解决方案 |
|------|-------|-----|
| 401 | API 密钥无效 | 检查 `.taostats` 格式，确保没有 "Bearer" 前缀 |
| 404 | 钱包未索引 | 等待 1-2 小时，新钱包会添加到索引中 |
| 429 | 速率限制 | 在调用之间添加延迟 |
| 空结果 | 子网不存在 | 先检查子网是否存在 |

---

## 交易决策的关键字段

### 入场验证
- `root_prop` < 0.30 = 良好（价格自然）
- `root_prop` > 0.70 = 不良（价格被人为抬高）

### 市场趋势信号
- `net_flow_7_days` > 0 = 资本流入
- `nominators_24_hr_change` > 0 = 验证器质押量增加

### 风险指标
- `in_danger` = 是 → 存在剪枝风险
- `is_immunity_period` = 是 → 受到保护，不会被移除
- `pruning_score` 越低越安全

### 市场情绪
- `fear_and_greed_index` < 30 = 恐惧（潜在买入信号）
- `fear_and_greed_index` > 70 = 贪婪（潜在等待信号）

---

## 已知问题

### `balance_as_tao` 字段错误
**问题**：返回的值以 rao（原始单位）表示，而非 TAO。

**解决方法**：始终除以 1,000,000,000
```bash
balance_tao=$(echo "$balance_as_tao / 1000000000" | bc -l)
```

**受影响的端点**：
- `/api/dtao/stake_balance/latest/v1`

---

## 集成示例

### 入场扫描器（root_prop + APY + 流量）
```bash
#!/bin/bash
source ~/.openclaw/workspace/skills/taostats/taostats.sh

echo "=== High-Quality Entry Opportunities ==="
for NETUID in 33 64 51 13 3 1 100 117 12 120; do
  POOL=$(taostats_pool $NETUID)
  ROOT_PROP=$(echo "$POOL" | jq -r '.data[0].root_prop')
  PRICE=$(echo "$POOL" | jq -r '.data[0].price')
  FEAR_GREED=$(echo "$POOL" | jq -r '.data[0].fear_and_greed_sentiment')
  
  MAX_APY=$(taostats_validator_yield $NETUID | jq -r '.data | max_by(.seven_day_apy) | .seven_day_apy')
  
  if (( $(echo "$ROOT_PROP < 0.30" | bc -l) )); then
    printf "SN%-3s | root_prop: %.2f | APY: %5.1f%% | Sentiment: %s\n" \
      "$NETUID" "$ROOT_PROP" "$(echo "$MAX_APY * 100" | bc -l)" "$FEAR_GREED"
  fi
  sleep 0.3
done
```

### 投资组合风险监控
```bash
#!/bin/bash
source ~/.openclaw/workspace/skills/taostats/taostats.sh

COLDKEY="YOUR_COLDKEY"
echo "=== Portfolio Risk Assessment ==="

taostats_stake_balance $COLDKEY | jq -r '.data[] | 
  "\(.netuid)|\(.balance_as_tao)|\(.root_prop)"' | while IFS='|' read netuid balance root_prop; do
  BALANCE_TAO=$(echo "$balance / 1000000000" | bc -l)
  if (( $(echo "$root_prop > 0.50" | bc -l) )); then
    printf "⚠️ SN%-3s: %6.3f TAO | HIGH root_prop: %.2f - Consider exit\n" "$netuid" "$BALANCE_TAO" "$root_prop"
  else
    printf "✅ SN%-3s: %6.3f TAO | OK root_prop: %.2f\n" "$netuid" "$BALANCE_TAO" "$root_prop"
  fi
done
```

---

## Python 封装层

```python
import requests
import os

class TaoStatsAPI:
    def __init__(self):
        self.base_url = "https://api.taostats.io"
        self.api_key = os.getenv("TAOSTATS_API_KEY")
        
    def _get(self, endpoint):
        headers = {"Authorization": self.api_key, "accept": "application/json"}
        r = requests.get(f"{self.base_url}{endpoint}", headers=headers)
        return r.json()
    
    def pool(self, netuid):
        """Get pool data with root_prop and fear & greed"""
        return self._get(f"/api/dtao/pool/latest/v1?netuid={netuid}")
    
    def validator_yield(self, netuid):
        """Get all validators with APYs"""
        return self._get(f"/api/dtao/validator/yield/latest/v1?netuid={netuid}")
    
    def stake_balance(self, coldkey):
        """Get all positions with root_prop per subnet"""
        return self._get(f"/api/dtao/stake_balance/latest/v1?coldkey={coldkey}")
    
    def subnet_info(self, netuid=None):
        """Get subnet parameters and net flows"""
        if netuid:
            return self._get(f"/api/subnet/latest/v1?netuid={netuid}")
        return self._get("/api/subnet/latest/v1")

# Usage
api = TaoStatsAPI()
pool = api.pool(33)
print(f"SN33 root_prop: {pool['data'][0]['root_prop']}")
```

---

## 技能维护

**最后更新**：2026-02-06  
**作者**：vanlabs-dev  
**依赖库**：`curl`, `jq`, `bc`

**更新日志**：
- 2026-02-06：全面重构 - 在池端点中发现了 root_prop、fear_and_greed、7 天历史数据
- 2026-02-06：添加了所有经过测试的可用端点
- 2026-02-06：使用 root_prop 添加了入场验证模式
- 2026-02-03：初始版本

**待办事项**：
- [ ] 为池数据添加缓存层
- [ ] 实现带有指数退避机制的重试逻辑
- [ ] 创建实时监控仪表板
- [ ] 为投资组合位置添加 root_prop 警报