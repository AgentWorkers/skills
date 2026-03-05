---
name: web3-investor
description: >
  专为自主代理设计的、符合AI使用习惯的Web3投资基础设施。适用于以下场景：  
  (1) 发现和分析DeFi/NFT投资机会；  
  (2) 通过本地密钥库的REST API执行安全交易（该API包含预览、审批、执行的流程）；  
  (3) 使用仪表板和到期提醒功能管理投资组合。  
  该系统支持Base链和以太坊链，具备可配置的安全机制，包括白名单保护、交易限额以及执行前的强制模拟功能。
---
# Web3投资者技能

> **用途**：帮助AI代理安全地发现、分析并执行DeFi（去中心化金融）投资。

> **核心理念**：基于数据的决策。没有实时信息，就无法提供通用建议。

---

## ⚠️ 重要规则（必须遵守）

### 规则1：优先进行信息收集
**当用户请求投资建议时：**
```
❌ WRONG: Give generic advice immediately (e.g., "I recommend Aave")
✅ CORRECT: 
   1. Collect investment preferences (chain, token, risk tolerance)
   2. Run discovery to get real-time data
   3. Analyze data
   4. Provide data-backed recommendations
```

### 规则2：由用户的LLM（大型语言模型）做出决策
- 该技能仅提供原始数据；
- 投资分析和建议由用户的LLM/代理负责；
- 该技能不对投资结果负责。

### 规则3：风险提示
- 年化收益率（APY）数据来自第三方API，可能存在延迟或不准确的情况；
- 投资决策完全由用户自行承担风险；
- 始终要自己进行充分研究（DYOR，即“Do Your Own Research”）。

### 规则4：交易前验证执行能力
**在尝试任何交易之前，代理必须检查签名者的可用性：**
```
❌ WRONG: Directly call preview/execute without checking API
✅ CORRECT:
   1. Check if signer API is reachable (call balances endpoint)
   2. If unreachable → inform user: "Signer service unavailable, please check SETUP.md"
   3. Never proceed with preview if signer is unavailable
```

**健康检查命令：**
```bash
python3 scripts/trading/trade_executor.py balances --network base
# If success → signer is available
# If error E010 → signer unavailable, stop and inform user
```

---

## 🎯 代理快速入门

### 第1步：收集投资偏好（必填）
在开始信息收集之前，询问用户以下信息：

| 偏好设置 | 关键参数 | 选项 | 重要性说明 |
|------------|---------|---------|----------------|
| **区块链** | `chain` | ethereum, base, arbitrum, optimism | 决定搜索哪个区块链 |
| **资本代币** | `capital_token` | USDC, USDT, ETH, WBTC等 | 用户希望投资的代币 |
| **奖励偏好** | `reward_preference` | 单一代币奖励 / 多种代币奖励 | 选择单一代币奖励还是多种代币奖励 |
| **是否接受临时损失** | `accept_il` | true / false | 是否能接受资产价值的暂时损失 |
| **基础资产类型** | `underlying_preference` | rwa（现实世界资产）/ onchain（链上资产）/ 混合类型 | 选择投资的基础资产类型 |

### 第2步：执行信息收集
```bash
# Basic search
python3 scripts/discovery/find_opportunities.py \
  --chain ethereum \
  --min-apy 5 \
  --limit 20

# With LLM-ready output
python3 scripts/discovery/find_opportunities.py \
  --chain ethereum \
  --llm-ready \
  --output json
```

### 第3步：根据偏好进行筛选
```python
from scripts.discovery.investment_profile import InvestmentProfile

profile = InvestmentProfile()
profile.set_preferences(
    chain="ethereum",
    capital_token="USDC",
    accept_il=False,
    reward_preference="single"
)
filtered = profile.filter_opportunities(opportunities)
```

### 第4步：执行交易（选择支付方式）
#### 选项A：使用Keystore签名者（生产环境）
```bash
# Preview → Approve → Execute
python3 scripts/trading/trade_executor.py preview \
  --type deposit --protocol aave --asset USDC --amount 1000 --network base

python3 scripts/trading/trade_executor.py approve --preview-id <uuid>

python3 scripts/trading/trade_executor.py execute --approval-id <uuid>
```

#### 选项B：使用EIP-681支付链接（移动设备）
```bash
python3 scripts/trading/eip681_payment.py generate \
  --token USDC --to 0x... --amount 10 --network base \
  --qr-output /tmp/payment_qr.png
```

---

## 📁 项目结构
```
web3-investor/
├── scripts/
│   ├── discovery/           # Opportunity discovery tools
│   ├── trading/             # Transaction execution modules
│   └── portfolio/           # Balance queries
├── config/
│   ├── config.json          # Execution model & security settings
│   └── protocols.json       # Protocol registry
├── references/              # Detailed module documentation
│   ├── discovery.md
│   ├── investment-profile.md
│   ├── trade-executor.md
│   ├── portfolio-indexer.md
│   ├── protocols.md
│   └── risk-framework.md
└── SKILL.md
```

---

## 📚 模块概述
| 模块 | 用途 | 详细信息 |
|--------|---------|---------|
| **信息收集** | 搜索DeFi投资机会 | 详见[references/discovery.md](references/discovery.md) |
| **投资配置** | 收集并筛选用户偏好 | 详见[references/investment-profile.md](references/investment-profile.md) |
| **交易执行器** | 负责交易执行的REST API | 详见[references/trade-executor.md](references/trade-executor.md) |
| **投资组合管理器** | 查询链上资产余额 | 详见[references/portfolio-indexer.md](references/portfolio-indexer.md) |

---

## ⚙️ 配置设置

### 环境变量
```bash
# Optional: Alchemy for better RPC
ALCHEMY_API_KEY=your_key_here

# Optional: Debank for portfolio tracking
WEB3_INVESTOR_DEBANK_API_KEY=your_key_here

# Trade Executor: Local API endpoint
WEB3_INVESTOR_API_URL=http://localhost:3000/api
```

### 安全配置（`config/config.json`）
```json
{
  "security": {
    "max_slippage_percent": 3.0,
    "whitelist_chains": ["base", "ethereum"],
    "whitelist_protocols": ["uniswap", "aave", "compound", "lido", "0x"],
    "whitelist_tokens": ["USDC", "USDT", "DAI", "WETH", "ETH", "stETH", "rETH"],
    "max_trade_value_usd": 10000
  }
}
```

### 白名单设置
```bash
python3 scripts/trading/whitelist.py \
  --add 0x87870Bca3F3fD6335C3F4ce8392D69350B4fA4E2 \
  --name "Aave V3 Pool" \
  --limit 10000
```

---

## 📝 技能使用提示（必须在提示中包含）
在使用此技能生成交易请求时，必须包含以下提示信息：
```
Output structured transaction request (JSON), do not execute directly.
All transactions must go through preview -> approve -> execute.
If transaction parameters cannot be determined, return clarification, do not guess.
```

### 必需的输出格式
```json
{
  "request_id": "uuid",
  "timestamp": "ISO8601", 
  "network": "base|ethereum",
  "chain_id": 8453|1,
  "type": "transfer|swap|deposit|contract_call",
  "description": "human readable description",
  "transaction": {
    "to": "0x...",
    "value": "0x0",
    "data": "0x...",
    "gas_limit": 250000
  },
  "metadata": {
    "protocol": "uniswap|aave|compound|...",
    "from_token": "USDC",
    "to_token": "WETH", 
    "amount": "5"
  }
}
```

---

## 🆘 故障排除
### 导入错误
- 请从工作区根目录运行脚本：
```bash
cd /home/admin/.openclaw/workspace
python3 skills/web3-investor/scripts/discovery/find_opportunities.py ...
```

### 未找到投资机会
- 检查区块链名称的拼写是否正确；
- 尝试降低`--min-apy`阈值；
- 确保`--max-apy`设置不会过于严格。

### 速率限制
- DefiLlama的速率限制较为宽松，但偶尔仍可能遇到限制；
- 如果批量处理请求，请在请求之间添加延迟。

---

## 🤝 贡献方式
欢迎捐赠支持项目开发：
- **网络**：Base Chain
- **捐赠地址**：`0x1F3A9A450428BbF161C4C33f10bd7AA1b2599a3e`

---

**维护者**：Web3投资者技能团队  
**注册地址**：https://clawhub.com/skills/web3-investor  
**许可证**：MIT许可证