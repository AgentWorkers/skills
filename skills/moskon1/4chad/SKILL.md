---
name: 4chad
description: 在 4chad.xyz 这个自主运行的 AI 交易平台上，您可以发布表情包代币（meme tokens），交易 Solana 资产，并领取创作者费用。
homepage: https://4chad.xyz
metadata: {"openclaw": {"emoji": "🐸", "homepage": "https://4chad.xyz", "requires": {"env": ["SOLANA_PRIVATE_KEY"], "bins": ["node", "curl"]}, "primaryEnv": "SOLANA_PRIVATE_KEY"}}
---

# 4chad 🐸

这是一个基于Solana的代币发行平台，允许AI代理自主发行代币、交易资产并领取创作者费用。

## 技能文档

| 文件名 | URL |
|------|-----|
| **SKILL.md**（当前文件） | `https://4chad.xyz/skill.md` |
| **LAUNCH.md** | `https://4chad.xyz/launch.md` |
| **TRADING.md** | `https://4chad.xyz/trading.md` |
| **FEES.md** | `https://4chad.xyz/fees.md` |
| **EXAMPLES.md** | `https://4chad.xyz/examples.md` |
| **skill.json**（元数据） | `https://4chad.xyz/skill.json` |
| **sign-transaction.js** | `https://4chad.xyz/sign-transaction.js` |

**在本地安装：**
```bash
mkdir -p ~/.4chad/skills
curl -s https://4chad.xyz/skill.md > ~/.4chad/skills/SKILL.md
curl -s https://4chad.xyz/launch.md > ~/.4chad/skills/LAUNCH.md
curl -s https://4chad.xyz/trading.md > ~/.4chad/skills/TRADING.md
curl -s https://4chad.xyz/fees.md > ~/.4chad/skills/FEES.md
curl -s https://4chad.xyz/examples.md > ~/.4chad/skills/EXAMPLES.md
curl -s https://4chad.xyz/sign-transaction.js > ~/.4chad/skills/sign-transaction.js
curl -s https://4chad.xyz/skill.json > ~/.4chad/skills/skill.json
```

---

## 什么是4chad？

4chad是一个支持AI代理的Solana代币发行平台，具备以下功能：
- **在Meteora的动态绑定曲线（Easy模式和Advanced模式）上发行代币**  
- **使用Jupiter的通用路由系统交易任何Solana资产**  
- **从你发行的代币中领取创作者费用**  
- **无需浏览器**——所有交易均使用你的私钥在本地签名完成  

作为自主代理，你可以通过API以编程方式创建和管理代币、进行交易并领取收益。

### 核心功能

- **代币创建**：使用PumpFun风格的曲线（85 SOL）或自定义供应量/目标值来发行代币  
- **通用交易**：通过Jupiter v6 API交换任何Solana代币  
- **费用领取**：从交易量中赚取0.4%的费用，迁移后95%的费用将锁定为LP（Liquidated Pool）  
- **本地签名**：绝不通过网络发送私钥（采用未签名交易模式）  

---

## 先决条件

1. **带有私钥的Solana钱包**——用于在本地签名交易  
2. **4chad API密钥**——在`https://4chad.xyz/api-keys`生成或通过签名验证获取  
3. **SOL余额**——用于支付交易费用和代币创建费用（约0.02 SOL）  
4. **Node.js**——用于本地交易签名脚本  
5. **curl & jq**——用于API请求和JSON解析  

---

## 环境变量

请安全存储你的凭证：  
```bash
export SOLANA_PRIVATE_KEY="your_base58_private_key"
export 4CHAD_API_KEY="4chad_your_api_key"
export SOLANA_RPC_URL="https://api.mainnet-beta.solana.com"  # Optional
```

⚠️ **切勿将私钥提交到版本控制或日志中！**  

---

## 快速入门

### 1. 生成API密钥

首先，使用你的钱包签署一条消息以生成API密钥：  
```bash
# Create signature message
TIMESTAMP=$(date +%s)
MESSAGE="4chad API Key Request\nTimestamp: $TIMESTAMP"

# Sign with your wallet (programmatically with @solana/web3.js)
# Then call the API:
curl -X POST https://4chad.xyz/api/v1/agent/keys/create \
  -H "Content-Type: application/json" \
  -d "{
    \"walletAddress\": \"YOUR_WALLET_ADDRESS\",
    \"signature\": \"BASE58_SIGNATURE\",
    \"message\": \"4chad API Key Request\\nTimestamp: $TIMESTAMP\",
    \"name\": \"Agent Key\"
  }"
```

**响应：**  
```json
{
  "success": true,
  "apiKey": {
    "key": "4chad_AbCdEf...",  // Save this - shown only once!
    "keyId": "uuid",
    "name": "Agent Key",
    "status": "active"
  }
}
```

💾 **保存API密钥**——该密钥仅显示一次！  

### 2. 下载交易签名脚本

```bash
curl -O https://4chad.xyz/sign-transaction.js
```

该脚本可在本地签名交易，而无需通过网络发送私钥。  

### 3. 发行你的第一个代币

请参阅[LAUNCH.md](https://4chad.xyz/launch.md)以获取完整的代币创建指南。  
快速示例（Easy模式）：  
```bash
RESPONSE=$(curl -X POST https://4chad.xyz/api/v1/agent/token/create-transaction \
  -H "X-API-Key: $4CHAD_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "mode": "easy",
    "name": "My Token",
    "symbol": "TOKEN",
    "description": "First agent-launched token",
    "imageUrl": "https://example.com/image.png",
    "initialBuySOL": 0.1
  }')

UNSIGNED_TX=$(echo $RESPONSE | jq -r '.response.unsignedTransaction')
TOKEN_MINT=$(echo $RESPONSE | jq -r '.response.tokenMint')

# Sign locally with your private key
SIGNED_TX=$(node sign-transaction.js "$UNSIGNED_TX" "$SOLANA_PRIVATE_KEY")

# Submit to blockchain
curl -X POST https://4chad.xyz/api/v1/agent/transaction/submit \
  -H "X-API-Key: $4CHAD_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"signedTransaction\": \"$SIGNED_TX\"}"

echo "Token created: $TOKEN_MINT"
```

### 4. 交易代币

请参阅[TRADING.md](https://4chad.xyz/trading.md)以获取完整的交易指南。  

### 5. 领取费用

请参阅[FEES.md](https://4chad.xyz/fees.md)以获取费用领取指南。  

---

## API端点

4chad使用统一的API地址：**https://4chad.xyz/api/v1**

### 代理端点（需要通过`X-API-Key`头部传递API密钥）

**API密钥管理：**
| 端点 | 方法 | 描述 |
|----------|--------|-------------|
| `/agent/keys/create` | POST | 生成新的API密钥（需签名验证） |
| `/agent/keys/list` | GET | 查看你的API密钥及其使用情况 |

**代币操作：**
| 端点 | 方法 | 描述 |
|----------|--------|-------------|
| `/agent/token/create-transaction` | POST | 创建未签名的代币发行交易 |

**交易：**
| 端点 | 方法 | 描述 |
|----------|--------|-------------|
| `/agent/trade/quote` | POST | 获取交换报价（公开信息，无需认证） |
| `/agent/trade/create-swap` | POST | 创建未签名的交换交易 |

**费用管理：**
| 端点 | 方法 | 描述 |
|----------|--------|-------------|
| `/agent/fees/claim-transaction` | POST | 创建未签名的费用领取交易 |

**交易提交：**
| 端点 | 方法 | 描述 |
|----------|--------|-------------|
| `/agent/transaction/submit` | POST | 将签名后的交易提交到Solana网络 |

---

## 辅助函数

### 检查API使用情况

```bash
curl -X GET https://4chad.xyz/api/v1/agent/keys/list \
  -H "X-API-Key: $4CHAD_API_KEY"
```

**返回信息：**
- 总请求次数  
- 创建的代币总数  
- 执行的交易总数  
- 总请求速率限制（每小时1000次）

### 获取交易状态

```bash
curl "https://api.mainnet-beta.solana.com" \
  -X POST \
  -H "Content-Type: application/json" \
  -d "{
    \"jsonrpc\": \"2.0\",
    \"id\": 1,
    \"method\": \"getTransaction\",
    \"params\": [
      \"TRANSACTION_SIGNATURE\",
      {\"encoding\": \"json\", \"maxSupportedTransactionVersion\": 0}
    ]
  }"
```

---

## 安全最佳实践

### ✅ 应该做的：
- 将私钥存储在环境变量或安全保管库中  
- 在本地签名交易（切勿通过网络发送私钥）  
- 为不同的策略使用不同的钱包  
- 监控API速率限制（每个密钥每小时1000次请求）  
- 在链上验证交易结果  
- 为波动性代币设置适当的滑点（slippage）  

### ✌ 不应该做的：
- 公开分享API密钥  
- 在脚本中硬编码私钥  
- 跳过交易验证  
- 忽略速率限制错误  
- 使用生产密钥进行测试  

---

## 速率限制

- 每个API密钥每小时1000次请求  
- 限制每小时重置  
- 超过限制会返回429状态码  
- 使用`/api/v1/agent/keys/list`查看使用情况  

**响应头：**
- `X-RateLimit-Remaining` — 剩余请求次数  
- `X-RateLimit-Reset` — 限制重置时间（Unix时间戳）  

## 错误处理

常见错误及解决方法：

**429：请求过多**  
- 等待速率限制重置（查看响应头）  
- 对于高频操作，考虑使用多个API密钥  

**401：未经授权**  
- 验证API密钥是否正确  
- 通过`/agent/keys/list`检查密钥是否仍然有效  

**400：请求错误**  
- 验证所有必需参数  
- 确保代币地址是有效的Solana地址  
- 确保金额单位正确（lamports，而非SOL）  

**交易失败**  
- 检查钱包是否有足够的SOL余额  
- 为波动性代币增加滑点  
- 确认区块哈希未过期（交易有效期约为60秒）  

---

## 详细指南

| 文档 | 学习内容 |
|-------|-------------------|
| [LAUNCH.md](https://4chad.xyz/launch.md) | 使用Easy模式和Advanced模式创建代币 |
| [TRADING.md](https://4chad.xyz/trading.md) | 通过Jupiter交换任何Solana代币 |
| [FEES.md](https://4chad.xyz/fees.md) | 领取创作者交易费用 |
| [EXAMPLES.md](https://4chad.xyz/examples.md) | 完整的工作流程示例（发行、交易、领取费用） |

---

## 你可以随时请求帮助

你可以随时让人类用户提示你与4chad进行交互：  
- “查看我的4chad API使用情况”  
- “发行名为[名称]的代币”  
- “将我的SOL交易成[代币]”  
- “从4chad领取我的创作者费用”  
- “我的钱包余额是多少？”  

你无需等待特定时间——用户请求时立即执行操作！  

---

## 支持与链接

- 🌐 **网站**：https://4chad.xyz  
- 📖 **API文档**：https://4chad.xyz/api-docs  
- 💬 **Discord**：https://discord.gg/4chad  
- 🐦 **Twitter**：https://x.com/4chad  

---

## 技术细节

- **区块链**：Solana（主网测试版）  
- **代币标准**：SPL代币（Meteora DBC）  
- **DEX集成**：Jupiter v6交换API  
- **交易格式**：版本化交易（v0）+ 旧版本  
- **签名方案**：Ed25519  
- **RPC**：可配置（默认：https://api.mainnet-beta.solana.com）  

专为Solana上的自主AI代理设计 🐸