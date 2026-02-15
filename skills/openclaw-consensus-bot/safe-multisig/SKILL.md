---
name: safe-multisig-skill
description: 使用 Safe{Core} SDK（协议套件 v6 / API 套件 v4）来提议、确认并执行安全的多重签名交易。该 SDK 需要 TypeScript 严格类型检查的支持。当代理需要操作一个 Safe 智能账户时，可以使用以下功能：  
(1) 创建或预测一个新的 Safe 账户；  
(2) 获取 Safe 账户的所有者信息、交易阈值以及随机数（nonce）；  
(3) 列出待处理的多重签名交易；  
(4) 构建并提议交易；  
(5) 添加交易确认；  
(6) 在链上执行交易；  
(7) 解决跨多个区块链（如 Base、Ethereum、Optimism、Arbitrum、Polygon 等）的 Safe 随机数或签名相关问题。
---

# 安全的多重签名（Safe Multisig）功能

这些TypeScript-strict脚本用于通过以下方式与安全的多重签名（Safe multisig）账户进行交互：
- **安全交易服务（Safe Transaction Service）**：读取账户状态、提议交易（propose transactions）、提交确认（submit confirmations）
- **Safe{Core} SDK**：创建多重签名账户（create Safes）、创建交易（create transactions）、计算哈希值（compute hashes）、签名（sign）、执行交易（execute transactions）

所有脚本均使用`ethers v6`，验证输入数据（地址、交易哈希值），并输出JSON格式的结果。

## 快速入门

```bash
cd <this-skill>
./scripts/bootstrap.sh

# sanity check network + service
./scripts/safe_about.sh --chain base
```

## 核心脚本

| 脚本          | 描述                                      |
|----------------|-----------------------------------------|
| `create-safe.ts`    | 预测账户地址；可选地部署新的多重签名账户                |
| `safe-info.ts`    | 获取多重签名账户的信息（所有者、阈值、随机数（nonce）             |
| `list-pending.ts`    | 列出待处理的多重签名交易                         |
| `safe_txs_list.ts`    | 列出所有已排队或已执行的多重签名交易                   |
| `propose-tx.ts`    | 创建并提议一个新的多重签名交易请求                   |
| `approve-tx.ts`    | 为交易哈希添加离线确认（off-chain confirmation）         |
| `execute-tx.ts`    | 在链上执行已确认的交易                         |

所有脚本的使用方法：`npx tsx scripts/<脚本名称>.ts --help`

## 常见操作

### 1) 创建新的多重签名账户

```bash
npx tsx scripts/create-safe.ts \
  --chain base \
  --owners 0xOwner1,0xOwner2,0xOwner3 \
  --threshold 2
```

在运行脚本时，添加`--deploy`和`SAFE_SIGNER_PRIVATE_KEY`参数以部署新的账户。

### 2) 获取多重签名账户信息

```bash
npx tsx scripts/safe-info.ts --chain base --safe 0xYourSafe
```

### 3) 列出待处理的多重签名交易

```bash
npx tsx scripts/list-pending.ts --chain base --safe 0xYourSafe
```

### 4) 提议新的交易

请参考`references/tx_request.schema.json`和`references/examples.md`来生成交易请求的JSON格式。

```bash
export SAFE_SIGNER_PRIVATE_KEY="..."

npx tsx scripts/propose-tx.ts \
  --chain base \
  --rpc-url "$BASE_RPC_URL" \
  --tx-file ./references/example.tx.json
```

### 5) 确认（批准）提议的交易

```bash
export SAFE_SIGNER_PRIVATE_KEY="..."

npx tsx scripts/approve-tx.ts \
  --chain base \
  --safe 0xYourSafe \
  --safe-tx-hash 0x...
```

### 6) 在链上执行已确认的交易

```bash
export SAFE_SIGNER_PRIVATE_KEY="..."

npx tsx scripts/execute-tx.ts \
  --chain base \
  --rpc-url "$BASE_RPC_URL" \
  --safe 0xYourSafe \
  --safe-tx-hash 0x...
```

## 配置参数

所有脚本支持以下配置选项：
- `--chain <链名>`（推荐）：例如 `base`、`base-sepolia`、`mainnet`、`arbitrum`、`optimism`
- `--tx-service-url <交易服务URL>`：自定义交易服务URL
- `--rpc-url <RPC端点>`：RPC服务端点（或通过环境变量`RPC_URL`设置）
- `--api-key <API密钥>`：安全交易服务的API密钥（或通过环境变量`SAFE_TX_SERVICE_API_KEY`设置）

## 安全注意事项

- **切勿将私钥粘贴到聊天框中**。请使用环境变量或文件来存储私钥。
- 尽量使用权限较低的角色进行签名操作，并设置合理的交易花费限制。
- 在签名之前，务必验证多重签名账户的地址、链名（chainId）、RPC端点以及随机数（nonce）。

## 参考资料

- `references/examples.md`：示例交易请求及操作流程
- `references/tx_request.schema.json`：交易请求的JSON格式规范
- `references/tx_service_slugs.md`：各链的名称及相关说明