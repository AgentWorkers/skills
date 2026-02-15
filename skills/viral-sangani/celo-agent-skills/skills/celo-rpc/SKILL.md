---
name: celo-rpc
description: 通过 RPC（Remote Procedure Call）端点与 Celo 区块链进行交互。适用于读取账户余额、交易记录、区块信息，以及通过 viem 或 cast 工具与 Celo 进行交互的场景。
license: Apache-2.0
metadata:
  author: celo-org
  version: "1.0.0"
---

# Celo RPC交互

本技能涵盖了通过RPC端点与Celo区块链进行交互的方法。

## 使用场景

- 读取账户余额（CELO代币）
- 查询交易数据
- 获取区块信息
- 通过viem或cast与Celo进行交互

## 网络信息

| 网络 | 链路ID | RPC端点 |
|---------|----------|--------------|
| Celo主网 | 42220 | https://forno.celo.org |
| Celo Sepolia | 11142220 | https://forno.celo-sepolia.celo-testnet.org |

Forno是一个具有速率限制的服务，采用尽力而为（best-effort）的机制。在生产环境中，请使用专用的RPC提供商。

### 可选的RPC提供商

| 提供商 | 主网 | 测试网 |
|----------|---------|---------|
| Alchemy | https://celo-mainnet.g.alchemy.com/v2/{API_KEY} | https://celo-sepolia.g.alchemy.com/v2/{API_KEY} |
| Infura | https://celo-mainnet.infura.io/v3/{API_KEY} | https://celo-sepolia.infura.io/v3/{API_KEY} |
| Ankr | https://rpc.ankr.com/celo | https://rpc.ankr.com/celo_testnet |
| QuickNode | 通过控制台设置自定义端点 | 通过控制台设置自定义端点 |

## 区块浏览器

- **Celo主网：** https://celoscan.io
- **Celo Sepolia：** https://sepolia.celoscan.io

## 使用viem与Celo交互

### 安装

```bash
npm install viem
```

### 基本设置

```typescript
import { createPublicClient, http } from "viem";
import { celo, celoSepolia } from "viem/chains";

// Mainnet client
const publicClient = createPublicClient({
  chain: celo,
  transport: http("https://forno.celo.org"),
});

// Testnet client (Celo Sepolia)
const testnetClient = createPublicClient({
  chain: celoSepolia,
  transport: http("https://forno.celo-sepolia.celo-testnet.org"),
});
```

### 读取余额

```typescript
// Get CELO balance
const balance = await publicClient.getBalance({
  address: "0x...",
});
console.log("Balance:", balance, "wei");

// Get token balance (e.g., cUSD)
const cUSD = "0x765de816845861e75a25fca122bb6898b8b1282a";
const tokenBalance = await publicClient.readContract({
  address: cUSD,
  abi: [
    {
      name: "balanceOf",
      type: "function",
      stateMutability: "view",
      inputs: [{ name: "account", type: "address" }],
      outputs: [{ type: "uint256" }],
    },
  ],
  functionName: "balanceOf",
  args: ["0x..."],
});
```

### 获取区块数据

```typescript
// Get latest block number
const blockNumber = await publicClient.getBlockNumber();

// Get block by number
const block = await publicClient.getBlock({
  blockNumber: 12345678n,
});

// Get block by hash
const blockByHash = await publicClient.getBlock({
  blockHash: "0x...",
});
```

### 获取交易数据

```typescript
// Get transaction by hash
const tx = await publicClient.getTransaction({
  hash: "0x...",
});

// Get transaction receipt
const receipt = await publicClient.getTransactionReceipt({
  hash: "0x...",
});
```

## 使用cast（Foundry）

### 读取数据

```bash
# Get CELO balance
cast balance 0x... --rpc-url https://forno.celo.org

# Get block number
cast block-number --rpc-url https://forno.celo.org

# Get block details
cast block 12345678 --rpc-url https://forno.celo.org

# Get transaction
cast tx 0x... --rpc-url https://forno.celo.org

# Call view function
cast call 0x765de816845861e75a25fca122bb6898b8b1282a \
  "balanceOf(address)(uint256)" \
  0x... \
  --rpc-url https://forno.celo.org

# Get storage slot
cast storage 0x... 0 --rpc-url https://forno.celo.org
```

### 链路信息

```bash
# Get chain ID
cast chain-id --rpc-url https://forno.celo.org

# Get gas price
cast gas-price --rpc-url https://forno.celo.org
```

## 使用curl（原始RPC请求）

### 读取余额

```bash
curl -X POST https://forno.celo.org \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "eth_getBalance",
    "params": ["0x...", "latest"],
    "id": 1
  }'
```

### 获取区块编号

```bash
curl -X POST https://forno.celo.org \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "eth_blockNumber",
    "params": [],
    "id": 1
  }'
```

## 标准EVM RPC方法

所有标准的Ethereum JSON-RPC方法都得到支持：

| 方法 | 描述 |
|--------|-------------|
| eth_blockNumber | 返回当前区块编号 |
| eth_getBalance | 返回指定地址的余额 |
| eth_getTransactionByHash | 根据哈希值获取交易信息 |
| eth_getTransactionReceipt | 返回交易收据 |
| eth_call | 执行函数调用（不创建新交易） |
| eth_estimateGas | 估算交易所需的气体费用 |
| eth_gasPrice | 返回当前的气体价格 |
| eth_getBlockByNumber | 根据编号获取区块 |
| eth_getBlockByHash | 根据哈希值获取区块 |
| eth_getLogs | 根据条件过滤并获取日志信息 |
| eth_sendRawTransaction | 发送已签名的交易 |

## 额外资源

- [rpc-providers.md](references/rpc-providers.md) - 完整的RPC提供商列表