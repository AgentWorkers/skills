---
name: web3-investor
description: >
  专为自主代理设计的、符合AI使用习惯的Web3投资基础设施。适用于以下场景：  
  (1) 发现和分析DeFi/NFT投资机会；  
  (2) 通过本地密钥库（keystore）的REST API执行安全交易（该API具备预览-审批-执行的状态机功能）；  
  (3) 利用仪表板管理投资组合并接收到期提醒。  
  该系统支持Base链和以太坊链，具备可配置的安全机制，包括白名单保护、交易限额以及执行前的强制模拟功能。
---
# Web3投资者技能

> **用途**：使AI代理能够安全地发现、分析并执行DeFi投资。

> **核心理念**：基于数据的决策。没有实时数据发现，就无法提供通用建议。

---

## ⚠️ 重要规则（必须遵守）

### 规则1：优先进行数据发现
**当用户请求投资建议时：**
```
❌ WRONG: Give generic advice immediately (e.g., "I recommend Aave")
✅ CORRECT: 
   1. Collect investment preferences (chain, token, risk tolerance)
   2. Run discovery to get real-time data
   3. Analyze data
   4. Provide data-backed recommendations
```

### 规则2：用户的LLM负责做出决策
- 该技能仅提供**原始数据**。
- 投资分析和建议由用户的LLM/代理负责。
- 该技能不对投资结果负责。

### 规则3：风险告知
- 年化收益率（APY）数据来自第三方API，可能存在延迟或不准确的情况。
- 投资决策由用户自行承担风险。
- 始终要自行进行充分研究（DYOR）。

### 规则4：在交易前验证执行能力
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

### 规则5：首先检查支付能力（v0.5.0新增）
**在询问用户交易详情之前，务必检查执行准备情况：**
```
❌ WRONG: Ask "How much do you want to invest?" without checking payment capability
✅ CORRECT:
   1. Run: python3 scripts/trading/preflight.py check --network <chain>
   2. Inform user of available payment methods
   3. Then ask for transaction details
```

**飞行前检查输出：**
```json
{
  "recommended": "eip681_payment_link",
  "methods": [
    {"method": "keystore_signer", "status": "unavailable"},
    {"method": "eip681_payment_link", "status": "available"}
  ],
  "message": "⚠️ No local signer. Use EIP-681 payment link."
}
```

**支付方式流程：**
| 推荐方式 | 操作 |
|-------------------|--------|
| `keystore_signer` | 使用`preview → approve → execute`流程 |
| `eip681_payment_link` | 使用`eip681_payment.py`生成EIP-681链接 |

---

## 🎯 代理快速入门

### 第1步：收集投资偏好（必填）
在运行数据发现功能之前，询问用户以下信息：

| 偏好设置 | 关键参数 | 选项 | 重要性说明 |
|------------|-----|---------|----------------|
| **链** | `chain` | ethereum, base, arbitrum, optimism | 决定搜索哪个区块链 |
| **资本代币** | `capital_token` | USDC, USDT, ETH, WBTC等 | 用户想要投资的代币 |
| **奖励偏好** | `reward_preference` | 单一代币/多种代币/任意 | 单一代币奖励还是多种代币奖励 |
| **是否接受临时损失** | `accept_il` | true/false/任意 | 是否能接受临时损失 |
| **基础资产类型** | `underlying_preference` | rwa/onchain/mixed/任意 | 实际资产还是链上资产 |

### 第2步：运行数据发现
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
#### 选项A：Keystore签名者（生产环境）
```bash
# Preview → Approve → Execute
python3 scripts/trading/trade_executor.py preview \
  --type deposit --protocol aave --asset USDC --amount 1000 --network base

python3 scripts/trading/trade_executor.py approve --preview-id <uuid>

python3 scripts/trading/trade_executor.py execute --approval-id <uuid>
```

#### 选项B：EIP-681支付链接（移动端）
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
| 模块 | 用途 | 详情 |
|--------|---------|---------|
| **数据发现** | 搜索DeFi收益机会 | 详见[references/discovery.md] |
| **投资配置** | 收集和筛选用户偏好 | 详见[references/investment-profile.md] |
| **交易执行器** | 交易执行REST API | 详见[references/trade-executor.md] |
| **投资组合索引器** | 查询链上余额 | 详见[references/portfolio-indexer.md] |

---

## 🔍 数据来源

### 主要数据来源
| 来源 | 类型 | 使用场景 |
|--------|------|----------|
| **MCP (AntAlpha)** | 实时收益数据 | DeFi机会的主要来源 |
| **DefiLlama** | 协议的总价值（TVL）/收益数据 | 备用数据源及交叉验证 |
| **Dune** | 链上分析工具 | 提供自定义查询和高级分析功能 |

### Dune与MCP的集成
Dune通过MCP（Model Context Protocol）提供强大的链上分析功能。可以使用Dune进行：
- 自定义链上数据查询 |
- 协议特定分析 |
- 历史趋势分析 |
- 大额钱包追踪

**配置文件（`config/config.json`）：**
```json
{
  "discovery": {
    "data_sources": ["mcp", "dune", "defillama"],
    "dune": {
      "mcp_endpoint": "https://api.dune.com/mcp/v1",
      "auth": {
        "header": { "name": "x-dune-api-key", "env_var": "DUNE_API_KEY" },
        "query_param": { "name": "api_key", "env_var": "DUNE_API_KEY" }
      }
    }
  }
}
```

**环境设置：**
```bash
# Required for Dune integration
export DUNE_API_KEY="your_dune_api_key"
```

**身份验证方式**：
1. **头部认证**（推荐）：`x-dune-api-key: <DUNE_API_KEY>`
2. **查询参数**：`?api_key=<DUNE_API_KEY>`

**使用示例：**
```bash
# Query Dune for protocol analytics
curl -H "x-dune-api-key: $DUNE_API_KEY" \
  "https://api.dune.com/mcp/v1/query/<query_id>/results"
```

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
    "max_trade_usd": 10000,
    "max_slippage_percent": 3.0,
    "whitelist_enabled": false,
    "whitelist_tokens": ["USDC", "USDT", "DAI", "WETH", "ETH", "stETH", "rETH"],
    "whitelist_protocols": ["uniswap", "aave", "compound", "lido", "0x"],
    "double_confirm": {
      "enabled": true,
      "large_trade_threshold_usd": 5000
    }
  }
}
```

#### 白名单配置
| 参数 | 默认值 | 说明 |
|-----------|---------|-------------|
| `whitelist_enabled` | `false` | 是否启用交易执行中的白名单过滤 |
| `whitelist_tokens` | [...] | 允许交易的代币 |
| `whitelist_protocols` | [...] | 允许交互的协议 |

**注意**：当`whitelist_enabled`设置为`false`（默认值）时，交易执行将跳过白名单检查，允许更广泛的协议/代币访问。设置为`true`可强制执行严格的白名单验证。

### 白名单设置
```bash
python3 scripts/trading/whitelist.py \
  --add 0x87870Bca3F3fD6335C3F4ce8392D69350B4fA4E2 \
  --name "Aave V3 Pool" \
  --limit 10000
```

---

## 📝 技能使用提示（生成交易时必须包含）
在使用此技能生成交易时，请包含以下提示内容：
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
请从工作区根目录运行脚本：
```bash
cd /home/admin/.openclaw/workspace
python3 skills/web3-investor/scripts/discovery/find_opportunities.py ...
```

### 未找到投资机会
- 检查链名拼写是否正确。
- 尝试降低`--min-apy`阈值。
- 确保`--max-apy`设置不会过于严格。

### 速率限制
- DefiLlama的速率限制相对宽松，但偶尔仍可能遇到限制。
- 如果批量处理请求，请在请求之间添加延迟。

---

## 🤝 贡献方式
欢迎捐赠支持：
- **网络**：Base Chain
- **地址**：`0x1F3A9A450428BbF161C4C33f10bd7AA1b2599a3e`

---

**维护者**：Web3投资者技能团队  
**注册地址**：https://clawhub.com/skills/web3-investor  
**许可证**：MIT许可证