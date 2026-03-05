---
name: web3-investor
description: >
  专为自主代理设计的、符合AI使用习惯的Web3投资基础设施。适用于以下场景：  
  (1) 发现并分析DeFi/NFT投资机会；  
  (2) 通过本地密钥库（keystore）的REST API执行安全交易（该API具备预览-审批-执行的状态机功能）；  
  (3) 利用仪表盘管理投资组合并接收到期提醒。  
  该系统支持Base链和Ethereum链，具备可配置的安全机制，包括白名单保护、交易限额设置，以及执行前的强制模拟功能。
---
# Web3 Investor Skill v0.3.0

## **用途**：  
使AI代理能够安全地发现、分析并执行DeFi投资。

## **核心理念**：  
数据驱动的决策。没有实时数据发现，就无法提供通用建议。

---

## 🧠 设计理念：以代理为核心  
该技能专为**智能代理（Agents）**设计，而非人类用户或固定程序。

### 核心原则  
| 传统设计 | 本技能的设计 |
|-------------------|---------------------|
| 为人类设计 → 精致的用户界面、友好的提示 | 为代理设计 → 清晰的文档、可读的代码 |
| 为程序设计 → 严格的API契约 | 为代理设计 → 明确的设计意图、可修改性 |
| 目标：**开箱即用** | 目标：**易于理解、可适应** |

### 对代理能力的假设  
使用此技能的代理应具备：  
- **大语言模型（LLM）能力**：能够阅读和理解文档  
- **编程能力**：能够修改代码和配置  
- **适应能力**：能够根据实际环境调整行为  

### 后果  
1. **文档即接口**：代理通过阅读SKILL.md、SETUP.md、SIGNER_API_SPEC.md来了解使用方法。  
2. **可配置的端点**：所有端点和参数均可通过`config/config.json`进行修改。  
3. **可修改的代码**：代理可以根据实际的签名者服务API调整`trade_executor.py`。  
4. **参考而非强制**：SIGNER_API_SPEC.md是一个参考规范，并非强制性标准。  

## ⚠️ 重要规则（必须遵守）  

### 规则1：优先发现  
**当用户请求投资建议时：**  
```
❌ WRONG: Give generic advice immediately (e.g., "I recommend Aave")
✅ CORRECT: 
   1. Collect investment preferences (chain, token, risk tolerance)
   2. Run discovery to get real-time data
   3. Analyze data
   4. Provide data-backed recommendations
```  

### 规则2：用户的LLM做出决策  
- 该技能仅提供**原始数据**。  
- 投资分析和建议由用户的LLM/代理负责。  
- 该技能不对投资结果负责。  

### 规则3：风险提示  
- 年化收益率（APY）数据来自第三方API，可能存在延迟或不准确的情况。  
- 投资决策由用户自行承担风险。  
- 请务必自行研究（DYOR）。  

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
在运行发现功能之前，询问用户：  
| 偏好设置 | 关键参数 | 选项 | 重要性 |
|------------|-----|---------|----------------|  
| **区块链** | `chain` | `ethereum`、`base`、`arbitrum`、`optimism` | 决定搜索哪个区块链 |
| **资本代币** | `capital_token` | `USDC`、`USDT`、`ETH`、`WBTC`等 | 用户想要投资的代币 |
| **奖励偏好** | `reward_preference` | `single` / `multi` / `any` | 单一代币奖励还是多种代币（例如CRV+CVX） |
| **是否接受IL** | `accept_il` | `true` / `false` / `any` | 是否接受LP产品的临时损失 |
| **基础资产类型** | `underlying_preference` | `rwa` / `onchain` / `mixed` / `any` | 实际资产还是纯链上协议 |

### 第2步：运行发现功能  
```bash
# Basic search
python3 scripts/discovery/find_opportunities.py \
  --chain ethereum \
  --min-apy 5 \
  --limit 20

# With LLM-ready output for analysis
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

# Get filtered opportunities
filtered = profile.filter_opportunities(opportunities)
```  

### 第4步：执行交易（选择支付方式）  
**⚠️ 重要**：根据您的环境选择合适的支付方式。  

#### 选项A：Keystore签名者（生产环境）  
需要运行本地的签名服务。最适合具有专用签名基础设施的自动化代理。  
```bash
# Step 4a: Preview transaction
python3 scripts/trading/trade_executor.py preview \
  --type deposit \
  --protocol aave \
  --asset USDC \
  --amount 1000 \
  --network base

# Step 4b: Approve (returns approval_id)
python3 scripts/trading/trade_executor.py approve \
  --preview-id <uuid-from-preview>

# Step 4c: Execute (broadcasts signed tx)
python3 scripts/trading/trade_executor.py execute \
  --approval-id <uuid-from-approve>
```  

#### 选项B：EIP-681支付链接（推荐用于移动设备）  
生成兼容MetaMask的支付链接或二维码。最适合移动用户，无需设置本地签名器即可快速完成投资。  
```bash
# Generate payment link for RWA investment
python3 scripts/trading/eip681_payment.py generate \
  --token USDC \
  --to 0x1F3A9A450428BbF161C4C33f10bd7AA1b2599a3e \
  --amount 10 \
  --network base \
  --qr-output /tmp/payment_qr.png
```  
**输出内容包括：**  
- MetaMask深度链接（移动用户点击打开应用）  
- QR码PNG文件（桌面用户用手机扫描）  
- 原始交易详情（供手动验证）  
**支持的代币**：USDC、USDT、WETH（Base和Ethereum主网）。  

#### 选项C：WalletConnect（计划中）  
将在未来版本中推出。将支持复杂的DeFi交互和持久的钱包连接。  

---

## 📁 项目结构  
```
web3-investor/
├── scripts/
│   ├── discovery/
│   │   ├── find_opportunities.py   # Main discovery tool
│   │   ├── investment_profile.py   # Preference collection & filtering
│   │   ├── unified_search.py       # Multi-source search
│   │   └── dune_mcp.py            # Dune Analytics adapter
│   ├── trading/
│   │   ├── trade_executor.py      # REST API adapter for local keystore signer
│   │   ├── eip681_payment.py      # EIP-681 payment link & QR code generator
│   │   ├── safe_vault.py          # [Debug Tool] Calldata generation & balance check
│   │   ├── whitelist.py           # Address whitelist management
│   │   └── simulate_tx.py         # [Debug Tool] Transaction simulation
│   └── portfolio/
│       └── indexer.py             # On-chain balance queries
├── config/
│   ├── config.json                # Execution model & security settings
│   └── protocols.json             # Protocol registry (12 protocols)
├── references/
│   ├── protocols.md               # Protocol documentation
│   └── risk-framework.md          # Risk assessment guide
└── SKILL.md                       # This file
```  

### 模块使用指南  
| 模块 | 用途 | 生产环境/调试环境 |
|--------|---------|------------------|  
| `trade_executor.py` | 主执行模块，连接签名服务 | ✅ 生产环境 |
| `eip681_payment.py` | 生成MetaMask支付链接和二维码 | ✅ 生产环境 |
| `safe_vault.py` | 生成Calldata、检查余额（不涉及签名） | 🔧 调试环境 |
| `simulate_tx.py` | 交易模拟（不涉及签名） | 🔧 调试环境 |

---

## 🔍 模块1：机会发现  
### 功能：  
在多个来源中搜索DeFi投资机会，并提供实时数据。  

### 主要特性（v0.2.2）  
- **风险提示**：每个投资机会都包含结构化的风险数据：  
  - `reward_type`：`none` | `single` | `multi`  
  - `has_il_risk`：`true` | `false`（是否涉及临时损失）  
  - `underlying_type`：`rwa` | `onchain` | `mixed` | `unknown`  
- **可执行地址**：准备好执行的合约地址  
- **适合LLM处理的输出**：结构化JSON格式，便于AI分析  

### 数据来源（优先顺序）  
1. **DefiLlama API**（主要来源）——免费，无需API密钥  
2. **Dune MCP**（可选）——如配置则提供深度分析  
3. **协议注册表**（备用）——已知协议的静态元数据  

### 使用示例  
```bash
# Search Ethereum opportunities with min 5% APY
python3 scripts/discovery/find_opportunities.py \
  --chain ethereum \
  --min-apy 5 \
  --limit 20

# Search stablecoin products only
python3 scripts/discovery/find_opportunities.py \
  --chain ethereum \
  --min-apy 3 \
  --max-apy 25 \
  --limit 50

# Output for LLM analysis
python3 scripts/discovery/find_opportunities.py \
  --chain ethereum \
  --llm-ready \
  --output json
```  

---

## 💰 模块2：投资概况与筛选  
### 功能：  
收集结构化的偏好设置并进行机会筛选。  

### 使用原因：  
- 确保不同代理之间的问题流程一致  
- 提供类型安全的偏好存储  
- 根据多个标准进行一次性筛选  

### 代码示例  
```python
from scripts.discovery.investment_profile import InvestmentProfile

# Create profile
profile = InvestmentProfile()

# Method 1: Direct assignment
profile.chain = "ethereum"
profile.capital_token = "USDC"
profile.accept_il = False
profile.reward_preference = "single"
profile.min_apy = 5
profile.max_apy = 30

# Method 2: Batch setup
profile.set_preferences(
    chain="ethereum",
    capital_token="USDC",
    accept_il=False,
    reward_preference="single",
    underlying_preference="onchain",
    min_apy=5,
    max_apy=30
)

# Filter opportunities
filtered = profile.filter_opportunities(opportunities)

# Get human-readable explanation
print(profile.explain_filtering(len(opportunities), len(filtered)))
```  

### 用于构建用户界面的问题示例  
```python
questions = InvestmentProfile.get_questions()

# Returns structured dict:
{
  "required": [...],      # Must ask: chain, capital_token
  "preference": [...],    # Should ask: reward_preference, accept_il, etc.
  "constraints": [...]    # Optional: min_apy, max_apy, min_tvl
}
```  

---

## 🔐 模块3：交易执行器（REST API适配器）  
### 功能：  
通过REST API生成可执行的交易请求，发送到本地keystore签名者。**该模块不存储私钥**——所有交易均需明确批准。  

### 执行模型  
| 属性 | 值 |  
|----------|-------|  
| **钱包类型** | 本地keystore签名者 |  
| **支持的区块链** | `base`、`ethereum` |  
| **入口点** | REST API |  
| **状态机** | `preview` → `approve` → `execute` |  

### 安全限制（必须遵守）  
- ❌ **不能跳过`approve`步骤**——每个交易都需要手动确认  
- ✅ **执行前必须进行模拟**——使用`eth_call`进行验证  
- ⚠️ **必须返回风险警告**——余额不足、权限不足、路由无效  
- 🔒 **默认权限设置**：  
  - 白名单中的区块链/协议/代币  
  - 交易金额限制  
  - 最大滑点限制  

### 统一的交易请求格式  
所有交易请求均遵循以下格式：  
```json
{
  "request_id": "uuid",
  "timestamp": "ISO8601",
  "network": "base",
  "chain_id": 8453,
  "type": "transfer|swap|deposit|contract_call",
  "description": "human readable",
  "transaction": {
    "to": "0x...",
    "value": "0x0",
    "data": "0x...",
    "gas_limit": 250000
  },
  "metadata": {
    "protocol": "uniswap|0x|aave|...",
    "from_token": "USDC",
    "to_token": "WETH",
    "amount": "5"
  }
}
```  

### API端点  
| 操作 | 方法 | 端点 | 描述 |  
|-----------|--------|----------|-------------|  
| 查询余额 | GET | `/api/wallet/balances` | 查询钱包代币余额 |  
| 预览交易 | POST | `/api/trades/preview` 或 `/api/uniswap/preview-swap` 或 `/api/zerox/preview-swap` | 生成交易预览 |  
| 批准交易 | POST | `/api/trades/approve` | 确认交易以执行 |  
| 执行交易 | POST | `/api/trades/execute` | 广播已签名的交易 |  
| 查询状态 | GET | `/api/transactions/{tx_hash}` | 查询交易状态 |  
| 查询权限 | GET | `/api/allowances` | 查询代币权限 |  
| 取消预览 | POST | `/api/allowances/revoke-preview` | 取消交易预览 |  

### 返回格式  
#### `preview`响应  
```json
{
  "preview_id": "uuid",
  "simulation_ok": true|false,
  "risk": {
    "balance_sufficient": true|false,
    "allowance_sufficient": true|false,
    "route_valid": true|false,
    "warnings": ["..."]
  },
  "next_step": "approve" | "clarification"
}
```  
#### `approve`响应  
```json
{
  "approval_id": "uuid",
  "preview_id": "...",
  "approved_at": "ISO8601",
  "expires_at": "ISO8601"
}
```  
#### `execute`响应  
```json
{
  "tx_hash": "0x...",
  "explorer_url": "https://basescan.org/tx/0x...",
  "executed_at": "ISO8601",
  "network": "base"
}
```  
#### 错误格式  
```json
{
  "code": "E001-E999",
  "message": "human readable",
  "diagnostics": "technical details"
}
```  
### 使用示例  
```bash
# Step 1: Preview a swap
python3 scripts/trading/trade_executor.py preview \
  --type swap \
  --from-token USDC \
  --to-token WETH \
  --amount 5 \
  --network base

# Step 2: Approve the preview
python3 scripts/trading/trade_executor.py approve \
  --preview-id <uuid-from-step-1>

# Step 3: Execute the approved transaction
python3 scripts/trading/trade_executor.py execute \
  --approval-id <uuid-from-step-2>

# Check balances
python3 scripts/trading/trade_executor.py balances \
  --network base

# Check transaction status
python3 scripts/trading/trade_executor.py status \
  --tx-hash 0x...
```  

---

## 📊 模块4：投资组合索引器  
### 功能：  
查询指定地址的链上余额。  

### 支持的区块链  
- Ethereum主网  
- Base  
- Arbitrum（部分支持）  

### 使用方法  
```bash
# Query portfolio
python3 scripts/portfolio/indexer.py \
  --address 0x... \
  --chain ethereum \
  --output json
```  

---

## ⚙️ 配置  
### 环境变量  
```bash
# Required for discovery (free tier works)
# No API key needed for DefiLlama

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
  },
  "execution_model": {
    "wallet_type": "local_keystore_signer",
    "supported_chains": ["base", "ethereum"],
    "entry_point": "rest_api",
    "state_machine": ["preview", "approve", "execute"]
  }
}
```  

### 白名单设置  
```bash
# Add trusted address
python3 scripts/trading/whitelist.py \
  --add 0x87870Bca3F3fD6335C3F4ce8392D69350B4fA4E2 \
  --name "Aave V3 Pool" \
  --limit 10000
```  

---

## 📚 参考文档  
| 文件 | 用途 |  
|------|---------|  
| [CHANGELOG.md] | 版本历史 |  
| [references/protocols.md] | 已知协议的元数据 |  
| [references/risk-framework.md] | 风险评估方法论 |  
| [TODO.md] | 已知问题和开发计划 |  

---

## 🆘 故障排除  
### 导入错误  
如果出现`ModuleNotFoundError`，请确保从工作区根目录运行脚本：  
```bash
cd /home/admin/.openclaw/workspace
python3 skills/web3-investor/scripts/discovery/find_opportunities.py ...
```  

### 未找到投资机会  
- 检查区块链名称的拼写（某些情况下区分大小写）  
- 尝试降低`--min-apy`阈值  
- 确保`--max-apy`设置不过于严格  

### 速率限制  
- DefiLlama的速率限制较为宽松，但偶尔仍可能受限  
- 如果批量处理，请在请求之间添加延迟  

---

## 📦 版本历史  
| 版本 | 发布日期 | 主要变更 |  
|---------|------|-------------|  
| 0.3.0 | 2026-03-05 | 添加REST API适配器、支持本地keystore签名者、改进状态机、统一交易格式 |  
| 0.2.2 | 2026-03-04 | 重写SKILL.md文档、引入强制发现规则、支持python3命令 |  
| 0.2.1 | 2026-03-04 | 引入投资偏好系统、增强风险提示功能 |  
| 0.2.0 | 2026-03-04 | 重新设计风险提示机制、优化可执行地址、升级Safe Vault v2 |  
| 0.1.0 | 2026-03-03 | 初始版本发布 |  

---

## 📝 技能使用提示模板  
在使用此技能生成交易请求时，请在提示中包含以下模板：  
```
Output structured transaction request (JSON), do not execute directly.
All transactions must go through preview -> approve -> execute.
If transaction parameters cannot be determined, return clarification, do not guess.
```  

### 必须遵循的输出格式  
所有交易请求必须遵循统一的格式：  
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

## 🤝 贡献方式  
欢迎捐赠：  
- **网络**：Base Chain  
- **地址**：`0x1F3A9A450428BbF161C4C33f10bd7AA1b2599a3e`  

**维护者**：Web3 Investor Skill团队  
**注册地址**：https://clawhub.com/skills/web3-investor  
**许可证**：MIT