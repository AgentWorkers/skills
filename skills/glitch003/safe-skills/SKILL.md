# SafeSkills – 为AI代理提供安全的秘密管理服务

SafeSkills 是一款安全的秘密管理工具。它用于存储秘密信息（例如钱包私钥），并利用这些秘密执行相应的操作，确保**您（作为代理）永远不会看到原始的秘密值**。该工具支持的首个功能是EVM钱包管理：您可以创建钱包、转移代币、发送交易、查询余额等。

**重要提示：****切勿尝试访问或请求原始的秘密值。所有操作均通过API在服务器端完成。**

## 配置

- **基础API地址：** 如果设置了`SAFESKILLS_API_URL`环境变量，请使用该地址；否则默认为`https://safeskill-production.up.railway.app`。
- **前端地址：** 如果设置了`SAFESKILLS_FRONTEND_URL`环境变量，请使用该地址；否则默认为`https://safeskill-production.up.railway.app`。

所有API请求都需要一个Bearer令牌（即创建钱包时返回的API密钥）。

```
Authorization: Bearer <API_KEY>
```

## 工作流程

### 1. 创建钱包

创建一个EVM钱包的秘密信息，并保存返回的API密钥以供后续请求使用。将钱包的声明URL（claim URL）分享给用户，以便他们能够管理钱包的相关设置。

```bash
curl -X POST "${SAFESKILLS_API_URL:-https://safeskill-production.up.railway.app}/api/secrets" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "EVM_WALLET",
    "memo": "My agent wallet",
    "chainId": 11155111
  }'
```

响应内容包括：
- `apiKey`：请妥善保管此密钥，将其用作后续请求的Bearer令牌。
- `claimUrl`：分享给用户，以便他们查看和管理钱包的设置。
- `address`：创建的钱包的智能合约地址。

创建完成后，告知用户：“这是您的钱包声明URL：<claimUrl>。您可以使用它来管理支出策略和监控钱包状态。”

### 2. 获取秘密信息

检索与当前API密钥关联的秘密元数据。

```bash
curl -X GET "${SAFESKILLS_API_URL:-https://safeskill-production.up.railway.app}/api/secrets/info" \
  -H "Authorization: Bearer <API_KEY>"
```

### 3. 获取钱包地址

```bash
curl -X GET "${SAFESKILLS_API_URL:-https://safeskill-production.up.railway.app}/api/skills/evm-wallet/address" \
  -H "Authorization: Bearer <API_KEY>"
```

### 4. 查询余额

查询钱包中的原生代币余额，以及可选的ERC-20代币余额（只需将代币合约地址作为逗号分隔的查询参数传递）。

```bash
# Native balance only
curl -X GET "${SAFESKILLS_API_URL:-https://safeskill-production.up.railway.app}/api/skills/evm-wallet/balance" \
  -H "Authorization: Bearer <API_KEY>"

# With ERC-20 tokens
curl -X GET "${SAFESKILLS_API_URL:-https://safeskill-production.up.railway.app}/api/skills/evm-wallet/balance?tokens=0xTokenAddr1,0xTokenAddr2" \
  -H "Authorization: Bearer <API_KEY>"
```

### 5. 转移ETH或代币

将原生ETH或ERC-20代币转移到指定地址。

```bash
# Transfer native ETH
curl -X POST "${SAFESKILLS_API_URL:-https://safeskill-production.up.railway.app}/api/skills/evm-wallet/transfer" \
  -H "Authorization: Bearer <API_KEY>" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "0xRecipientAddress",
    "amount": "0.01"
  }'

# Transfer ERC-20 token
curl -X POST "${SAFESKILLS_API_URL:-https://safeskill-production.up.railway.app}/api/skills/evm-wallet/transfer" \
  -H "Authorization: Bearer <API_KEY>" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "0xRecipientAddress",
    "amount": "100",
    "token": "0xTokenContractAddress"
  }'
```

### 6. 发送任意交易

发送带有自定义调用数据的交易。此功能适用于与智能合约进行交互。

```bash
curl -X POST "${SAFESKILLS_API_URL:-https://safeskill-production.up.railway.app}/api/skills/evm-wallet/send-transaction" \
  -H "Authorization: Bearer <API_KEY>" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "0xContractAddress",
    "data": "0xCalldata",
    "value": "0"
  }'
```

## 重要注意事项

- **切勿尝试访问原始的秘密值。** SafeSkills的核心优势就在于所有秘密信息都存储在服务器端。
- 请务必保存创建钱包时返回的API密钥，因为这是验证后续请求的唯一依据。
- 创建钱包后，务必将钱包的声明URL分享给用户。
- 默认的链ID为`11155111`（Ethereum Sepolia测试网）。根据需要可进行调整。
- 如果转账或交易失败，请检查钱包是否有足够的余额，并确认用户已通过声明URL批准了所有必要的操作。