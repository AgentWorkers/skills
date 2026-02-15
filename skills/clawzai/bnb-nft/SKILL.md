---
name: bnb-nft
description: 在 BNB 链上进行的 NFT 操作包括：获取 NFT 元数据、检查所有权、按所有者列出 NFT、转移 ERC-721 代币以及获取收藏集信息。这些功能可用于 BSC 上的所有与 NFT 相关的任务。
---

# BNB Chain NFT 功能

在 BNB Chain（BSC）上支持 ERC-721 标准的 NFT 操作。

## 准备工作

需要安装 Node.js 和 ethers.js：

```bash
cd ~/.openclaw/workspace/skills/bnb-nft && npm install ethers --silent
```

## 配置

对于写入操作（转账、批准等），需要设置私钥：

```bash
export BNB_PRIVATE_KEY="0x..."
```

或者使用 `--key` 参数来传递私钥。

## 使用方法

所有操作均通过 `nft.js` 脚本执行：

### 获取集合信息

```bash
node nft.js collection <contract_address>
```

返回集合的名称、符号以及总发行量（如果可用）。

### 获取 NFT 元数据

```bash
node nft.js metadata <contract_address> <token_id>
```

返回 NFT 的所有者、TokenURI 以及获取到的元数据（如果元数据通过 HTTP 提供）。

### 检查 NFT 所有者

```bash
node nft.js owner <contract_address> <token_id>
```

### 列出某个地址拥有的 NFT

```bash
node nft.js owned <contract_address> <wallet_address> [--limit 100]
```

扫描指定地址拥有的 NFT ID；可以使用 `--limit` 参数来限制扫描范围。

### 获取钱包中的 NFT 数量

```bash
node nft.js balance <contract_address> <wallet_address>
```

返回钱包中拥有的 NFT 数量。

### 转移 NFT

```bash
node nft.js transfer <contract_address> <to_address> <token_id> [--key <private_key>]
```

### 批准 NFT 的转移

```bash
node nft.js approve <contract_address> <spender_address> <token_id> [--key <private_key>]
```

### 为所有 NFT 设置默认批准状态

```bash
node nft.js approve-all <contract_address> <operator_address> <true|false> [--key <private_key>]
```

### 检查是否已获得批准

```bash
node nft.js is-approved <contract_address> <token_id> <spender_address>
```

## 常见的 BSC 主网 NFT 集合

| 集合名称 | 地址            |
|------------|-------------------|
| Pancake Squad | `0x0a8901b0E25DEb55A87524f0cC164E9644020EBA` |
| Pancake Bunnies | `0xDf7952B35f24aCF7fC0487D01c8d5690a60DBa07` |
| BakerySwap | `0x5d0915E32b1fb1144f27B87C9f65AC3f661C9e6D` |

## 安全提示

- **切勿将私钥提交到 Git 仓库**  
- 在进行任何操作前，请务必验证合约地址的合法性。  
- 先在测试网（testnet）上测试转账操作。  
- 在将 NFT 上架到市场之前，请先检查其批准状态。