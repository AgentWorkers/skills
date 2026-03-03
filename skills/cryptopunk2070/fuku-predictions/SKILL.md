---
name: fuku-predictions
description: 通过对话来交易 Kalshi 预测市场，该功能基于 Fuku 体育模型的预测结果。当用户询问 Kalshi 市场情况、需要带有分析结果的体育预测、想要进行交易或退出现有交易，或者希望自动扫描市场机会时，均可使用该服务。该系统支持 CBB（大学篮球）、NBA（美国职业篮球联赛）、NHL（国家冰球联盟）和足球赛事，并提供个性化的交易建议。用户可以使用自然语言表达自己的偏好（例如：“我希望 CBB 比赛中的主场球队能获得 7 分以上”），系统会据此生成用户的交易档案，扫描市场并展示具有优势、预期收益和推荐的交易机会。Kalshi 的 API 密钥会存储在本地设备上，绝不会被传输到外部。
---
# Fuku Predictions — 一种基于对话的Kalshi交易技能

通过对话来参与交易预测市场。该智能代理会了解您的兴趣和偏好，生成个性化的交易档案，然后在Kalshi市场中寻找符合您投资风格的投资机会。

## 三种模式

### 1. 个人资料构建（交互式）
用户描述自己的投资偏好 → 代理生成交易档案 → 保存以供后续使用。

### 2. 对话式市场扫描
代理根据用户档案扫描市场 → 提供符合偏好的投资机会 → 用户确认是否进行交易。

### 3. 自动交易
代理在设定的风险范围内自动扫描并执行交易。

---

## 设置

### 所需依赖项
```bash
pip install httpx cryptography python-dotenv
```

### Kalshi API密钥
在技能目录下创建`.env`文件：
```env
KALSHI_API_KEY_ID=your_key_id
KALSHI_PRIVATE_KEY="-----BEGIN RSA PRIVATE KEY-----
...
-----END RSA PRIVATE KEY-----"
```
获取凭证：https://kalshi.com/profile/api

---

## 定义投资偏好

用户可以使用自然语言表达自己的投资需求：

**情境相关：**“我希望看到CBB比赛中主场球队获得7分以上的比赛” · “在大胜之后，显示那些可能表现不佳的比赛” · “寻找那些上一次弱队以15分以上分差落败的‘复仇之战’”

**球员实力对比：**“最佳球员与对手之间的FPR（预测胜率）差距超过50%的比赛” · “明星球员受伤时的比赛”

**统计数据：**“仅选择防守排名前30的球队参与的比赛” · “比赛节奏差异（快队 vs 慢队）” · “赔率差小于3分的比赛”

**风险与投注金额：**“对最有信心的投注选择投注5美元” · “每天最多进行8笔交易” · “采用Quarter-Kelly投注策略”

---

## 代理工具

### 个人资料管理
```bash
# Process user preference input
python3 scripts/agent_interface.py --input "I want home dogs getting 7+ points in CBB"

# Scan using a profile
python3 scripts/agent_interface.py --scan --profile default

# List profiles
python3 scripts/agent_interface.py --input "list my profiles"
```

### 市场浏览器
```bash
# Tonight's markets with predictions and edges
python3 scripts/browse.py

# Filter by sport or game
python3 scripts/browse.py --sport cbb
python3 scripts/browse.py --game "Duke" --date 2026-03-03

# Change bet display amount (default $5)
python3 scripts/browse.py --bet 10
```

### 直接访问Kalshi市场
```bash
python3 scripts/kalshi_client.py balance
python3 scripts/kalshi_client.py positions
python3 scripts/kalshi_client.py markets --series KXNBASPREAD
```

---

## 向用户展示市场信息

**必须包含的信息：**市场名称、价格（美元）、模型预测结果、投资优势、预期收益以及交易建议。

**请使用美元进行金额表述，系统会自动转换为相应的投注合约数量。** 例如：用户说“在波士顿队身上投注5美元”，系统会内部转换为相应的合约数量。

**每种市场类型的显示方式：**
- **主线**：投注金额最接近50美分的合约（市场共识）
- **🔒 更安全**：投资优势最高（置信度较高，预期收益适中）
- **🎰 风险更高**：投注金额接近模型预测结果的合约（模型预测概率约50%，预期收益较高，但需要至少3%的投资优势）

**投资优势图标：** 🔥 ≥20% · ✅ ≥10% · 📊 ≥5% · ➖ <5%

**示例：**
```
🏀 Boston @ Milwaukee — 7:30 PM
📊 Our model: BOS -8.4 | Total 224.1

• BOS -2.5 at 50¢ → 70% model (+20% edge 🔥) — $5 pays $10
  ↳ 🔒 Safer: BOS -1.5 at 57¢ → 82% model (+25% edge) — $5 pays $8
  ↳ 🎰 Riskier: BOS -8.5 at 31¢ → 50% model (+19% edge) — $5 pays $16
• Over 215.5 at 52¢ → 79% model (+27% edge 🔥) — $5 pays $9

💰 Balance: $49.95
Want me to put money on any of these?
```

### 美元与合约数量的换算
例如：“在波士顿队身上投注5美元，当前赔率为-8.5”，则计算如下：
投注金额（5美元）÷ 赔率（-8.5）= 16份合约
每份合约的成本 = 5美元 ÷ -8.5 = 0.31美元
如果预测正确，总收益 = 16份合约 × 0.31美元 = 4.96美元
如果预测错误，总损失 = 16份合约 × -0.31美元 = 4.96美元

---

## 交易流程
```python
from kalshi_client import KalshiClient
c = KalshiClient()

# Buy
c.place_order(ticker="KXNBA...", side="yes", action="buy",
              count=16, order_type="limit", yes_price=31)

# Sell to exit
c.place_order(ticker="KXNBA...", side="yes", action="sell",
              count=16, order_type="limit", yes_price=current_bid)
```

---

## 投资优势的计算方法

**概率转换采用正态分布（不使用scipy库）：**
- 使用`math.erfc`函数计算累积分布函数（CDF）
- 根据不同运动项目的特性调整标准差（σ）：CBB比赛赔率为12.0，NBA为11.0，NHL为1.5，足球为1.2

**球员属性的影响：**球员属性对赔率的影响为预测值的30%（最低为2.0%）

---

## Kalshi市场结构

- **系列赛**（如NBA、CBB、NHL、足球）：使用`KXNBASPREAD`、`KXNBATOTAL`、`KXNBAGAME`等标识
- **单场比赛**：使用`KXNBASPREAD-26MAR02BOSMIL`等标识
- **具体合约**：例如`KXNBASPREAD-26MAR02BOSMIL-BOS7`表示“波士顿队胜出超过7.5分吗？”

**价格格式：**结果以“YES/NO”表示，赔率以美分（1-99）表示。例如“YES”表示赔率为31%，意味着如果预测正确，投注1份合约的预期收益为31%（即1美元）。

### 支持的运动项目
| 运动项目 | 赔率差 | 总投注金额 | 模型预测 | 球员属性 |
|--------|--------|---------|---------|--------|
| NBA    | `KXNBASPREAD` | `KXNBATOTAL` | `KXNBAGAME` | — |
| CBB    | `KXNCAAMBSPREAD` | `KXNCAAMBTOTAL` | `KXNCAABGAME` | — |
| NHL    | `KXNHLSPREAD` | `KXNHLTOTAL` | `KXNHLGAME` | 进球数/得分/助攻 |
| 足球    | 根据联赛不同（EPL/La Liga/Serie A/Bundesliga/Ligue 1/UCL/MLS） | 每个联赛独立计算 | 总进球数 |

---

## 自动交易配置

`config/config.json`文件中的配置选项：
```json
{
  "strategy": "model_follower",
  "sports": ["nba", "cbb"],
  "min_edge_pct": 3.0,
  "max_daily_loss_pct": 10,
  "max_daily_bets": 15,
  "sizing": "quarter_kelly",
  "mode": "approve"
}
```

**运行模式：**`dry_run`（仅记录日志）· `approve`（需要用户确认）· `auto`（自动交易）

---

## 安全措施

- 每日最大损失限制（默认为10%）
- 单笔交易的最大持仓比例限制（默认为5%）
- 强制停止交易功能：在技能目录中找到`KILL_SWITCH`并触发
- 所有交易记录都会保存到`trades.json`文件中
- API密钥严格保管，不得离开设备

---

## Kalshi API认证

使用RSA-PSS签名机制。客户端会自动处理认证过程。

**签名注意事项：**投资组合相关的API端点在请求路径中不包含查询参数；而市场数据相关的API端点则需要包含查询参数。详情请参考`kalshi_client.py`文件中的 `_SIGN_PATH_ONLY` 配置。

## Fuku Prediction API（公开接口）

**基础地址：**`https://cbb-predictions-api-nzpk.onrender.com`

| API端点 | 提供的数据 |
|----------|------|
| `/api/public/cbb/predictions?date=YYYY-MM-DD` | CBB比赛预测结果 |
| `/api/public/nba/predictions?date=YYYY-MM-DD` | NBA比赛预测结果 |
| `/api/public/nhl/predictions?date=YYYY-MM-DD` | NHL比赛预测结果 |
| `/api/public/soccer/predictions?date=YYYY-MM-DD` | 足球比赛预测结果 |
| `/api/public/cbb/rankings?limit=N` | 球队FPR排名 |
| `/api/public/cbb/players?team=X&limit=N` | 球员FPR数据 |

---

## 相关文件

| 文件名 | 用途 |
|--------|---------|
| `scripts/browse.py` | 主要文件——包含市场数据、投资优势及预期收益信息 |
| `scripts/agent_interface.py` | 负责构建用户交易档案并进行市场扫描 |
| `scripts/profile_engine.py` | 根据用户档案生成投资机会的评分系统 |
| `scripts/profile_builder.py` | 将自然语言输入转换为可解析的JSON格式的档案 |
| `scripts/autopilot.py` | 自动化市场扫描和交易执行流程 |
| `scripts/kalshi_client.py` | 用于与Kalshi API进行交互的客户端代码（包括认证和订单处理） |
| `scripts/scanner.py` | 全面扫描所有合约的投资机会 |
| `scripts/executor.py` | 负责交易执行及风险管理 |
| `scripts/portfolio.py` | 跟踪持仓情况并计算盈亏 |
| `scripts/setup.py` | 交互式设置向导 |
| `config/config.json` | 存储交易策略和风险设置 |
| `config/profiles/*.json` | 用户的交易档案 |
| `references/strategies.md` | 交易策略说明 |
| `references/kalshi-markets.md` | Kalshi市场的相关说明 |