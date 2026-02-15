---
name: kaspa-dev
description: "Kaspa区块链开发综合工具包，用于构建交易、集成钱包、创建去中心化应用（dApps）、开发区块浏览器以及与Kaspa网络进行交互。适用于以下Kaspa区块链开发场景：  
(1) 构建和广播交易；  
(2) 生成地址及管理钱包；  
(3) 开发去中心化应用或区块浏览器；  
(4) 将Kaspa集成到现有应用程序中（如RainbowKit、OisyWallet等）；  
(5) 操作KRC20代币；  
(6) 配置Kaspa节点；  
(7) 使用Kaspa SDK（Rust、Go、JavaScript/TypeScript、Python、WASM）。  
支持Rust、Go、JavaScript/TypeScript、Python以及Motoko（Internet Computer）编程语言的开发。"
---

# Kaspa 开发

## 概述

本文档提供了针对 Kaspa 区块链开发的全面支持，涵盖了多种编程语言和用例。无论您是构建简单的钱包集成、完整的去中心化应用（dApp）、区块浏览器，还是处理 KRC20 代币，本文档都提供了所需的开发模式、SDK 参考资料以及样板代码。

## 快速入门

### 选择合适的 SDK

Kaspa 提供了多种语言的官方 SDK：

- **JavaScript/TypeScript**：`kaspa-wasm`——基于 WebAssembly 的 SDK，适用于浏览器和 Node.js 环境
- **Rust**：`kaspa-rpc-client` 和 `kaspa-wallet-core`——原生 Rust SDK
- **Go**：`github.com/kaspanet/kaspad`——官方 Go 实现
- **Python**：可通过 PyPI 获取社区提供的 SDK
- **Motoko**：`kaspa` 包，用于与 Internet Computer 的集成

### 常见任务

#### 生成 Kaspa 地址

**JavaScript/TypeScript**：
```javascript
import { PrivateKey, NetworkType } from 'kaspa-wasm';

const privateKey = PrivateKey.random(NetworkType.Mainnet);
const publicKey = privateKey.toPublicKey();
const address = publicKey.toAddress(NetworkType.Mainnet);

console.log('Address:', address.toString());
console.log('Private Key:', privateKey.toString());
```

**Rust**：
```rust
use kaspa_wallet_core::keys::{PrivateKey, PublicKey};
use kaspa_consensus_core::network::NetworkType;

let private_key = PrivateKey::random(NetworkType::Mainnet);
let public_key = private_key.to_public_key();
let address = public_key.to_address(NetworkType::Mainnet);

println!("Address: {}", address.to_string());
```

**Go**：
```go
import (
    "github.com/kaspanet/kaspad/domain/consensus/model/externalapi"
    "github.com/kaspanet/kaspad/util"
)

privateKey, _ := util.GeneratePrivateKey()
publicKey := privateKey.PublicKey()
address, _ := util.NewAddressPublicKey(publicKey.Serialize(), util.Bech32PrefixKaspaMain)

fmt.Printf("Address: %s\n", address.String())
```

#### 构建并广播交易

**JavaScript/TypeScript**：
```javascript
import { Transaction, RpcClient, NetworkType } from 'kaspa-wasm';

const rpc = new RpcClient({
  url: 'wss://api.kaspa.org',
  network: NetworkType.Mainnet
});

await rpc.connect();

// Get UTXOs for the sender address
const utxos = await rpc.getUtxosByAddresses([senderAddress]);

// Build transaction
const tx = new Transaction({
  version: 0,
  inputs: utxos.map(utxo => ({
    previousOutpoint: utxo.outpoint,
    signatureScript: '', // Will be filled after signing
    sequence: 0,
    sigOpCount: 1
  })),
  outputs: [{
    amount: amount,
    scriptPublicKey: recipientScriptPublicKey
  }],
  lockTime: 0,
  subnetworkId: '00000000000000000000000000000000'
});

// Sign transaction
const signedTx = await signTransaction(tx, privateKey);

// Broadcast
const txId = await rpc.submitTransaction(signedTx);
console.log('Transaction ID:', txId);
```

## SDK 参考资料

有关详细的 SDK 文档和示例，请参阅：

- **JavaScript/TypeScript (WASM)**：[references/kaspa-wasm-sdk.md](references/kaspa-wasm-sdk.md)
- **Rust SDK**：[references/kaspa-rust-sdk.md](references/kaspa-rust-sdk.md)
- **Go SDK**：[references/kaspa-go-sdk.md](references/kaspa-go-sdk.md)
- **Python SDK**：[references/kaspa-python-sdk.md](references/kaspa-python-sdk.md)
- **API 参考**：[references/api-reference.md](references/api-reference.md)（Kaspa 开发者平台 API）

## 集成指南

### 钱包集成

要将 Kaspa 集成到 RainbowKit、OisyWallet 或自定义钱包中，请参阅 [references/wallet-integration.md]，其中包含以下内容：
- 钱包连接模式
- 交易签名流程
- 地址管理
- 网络切换

### 节点操作

有关设置和运行 Kaspa 节点的详细信息，请参阅 [references/node-operations.md]，内容包括：
- Docker 部署
- 二进制文件安装
- 从源代码构建
- 配置选项
- RPC 节点设置
- 监控与维护

### dApp 开发

在开发 Kaspa dApp 时，请遵循以下步骤：
1. **设置**：使用 WASM SDK 以确保浏览器兼容性
2. **钱包连接**：实现钱包适配器
3. **状态管理**：跟踪余额、交易和未花费的交易输出（UTXOs）
4. **交易构建**：使用 UTXO 选择算法
5. **错误处理**：处理网络故障和区块重组（reorgs）

### 块浏览器

要构建区块浏览器，请执行以下步骤：
1. **数据来源**：使用 Kaspa 开发者平台 API 或运行自己的节点
2. **索引**：对区块、交易和地址进行索引
3. **API 层**：为前端构建 REST/GraphQL API
4. **前端**：显示区块、交易、地址和网络统计信息

有关可用端点的详细信息，请参阅 API 参考。

## KRC20 代币

Kaspa 支持 KRC20 代币（类似于以太坊的 ERC20）。有关代币开发的详细信息，请参阅 [references/krc20-tokens.md]，内容包括：
- 代币合约结构
- 转移和批准机制
- 代币元数据
- 集成模式

## 网络类型

Kaspa 有三种网络类型：
- **主网**：生产网络（前缀：`kaspa:`）
- **测试网**：测试网络（前缀：`kaspatest:`）
- **开发网**：开发网络（前缀：`kaspadev:`）

请根据实际需求选择正确的网络类型。

## 地址格式

Kaspa 使用 Bech32 编码格式表示地址：
- 主网：`kaspa:qqkqkzjvr7zwxxmjxjkmxx`（共 62 个字符）
- 测试网：`kaspatest:qqkqkzjvr7zwxxmjxjkmxx`
- 开发网：`kaspadev:qqkqkzjvr7zwxxmjxjkmxx`

## 脚本和工具

`scripts/` 目录包含以下工具脚本：
- `generate-address.py`：生成 Kaspa 地址
- `build-transaction.py`：构建并签名交易
- `monitor-address.py`：监控地址以接收交易

## 资源

### 参考资料

- **api-reference.md**：Kaspa 开发者平台 API 文档
- **kaspa-wasm-sdk.md**：JavaScript/TypeScript WASM SDK 使用指南
- **kaspa-rust-sdk.md**：Rust SDK 文档
- **kaspa-go-sdk.md**：Go SDK 文档
- **kaspa-python-sdk.md**：Python SDK 文档
- **krc20-tokens.md**：KRC20 代币标准文档
- **wallet-integration.md**：钱包集成模式和示例
- **node-operations.md**：运行 Kaspa 节点的完整指南

### 资源文件

`assets/` 目录包含以下样板文件：
- `dapp-template/`：React/Next.js dApp 启动模板
- `explorer-template/`：区块浏览器启动模板
- `wallet-adapter/`：钱包适配器实现模板

## 最佳实践

1. **使用地址前务必进行验证**
2. **谨慎处理 UTXO 选择**，以避免生成无效的交易输出
3. **为网络故障实现适当的错误处理**
4. **在主网部署前先在测试网上进行测试**
5. **在确认交易时监控区块重组**
6. **使用费用估算功能以确保交易及时确认**
7. **保护私钥安全**——切勿在客户端代码中暴露私钥

## 获取帮助

- **文档**：https://docs.kas.fyi/
- **GitHub**：https://github.com/kaspanet
- **开发者平台**：https://kas.fyi/
- **Motoko 包**：https://mops.one/kaspa