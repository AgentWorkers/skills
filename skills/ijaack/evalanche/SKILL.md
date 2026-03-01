---
name: evalanche
description: >
  **多EVM代理钱包SDK**  
  该SDK支持链上身份验证（ERC-8004标准）、支付功能（x402协议）、跨链桥接（Li.Fi技术）以及目标链上的Gas费用支付（Gas.zip模块）。兼容21种以上的EVM区块链，包括Ethereum、Base、Arbitrum、Optimism、Polygon、BSC、Avalanche等。代理节点可自行生成和管理密钥，无需人工干预。  
  **适用场景：**  
  - 在任意EVM区块链上启动自主代理钱包  
  - 发送代币  
  - 调用智能合约  
  - 验证代理节点的身份  
  - 检查代理节点的信誉  
  - 使用x402协议进行支付操作  
  - 实现跨链代币桥接（Li.Fi）  
  - 在目标链上支付Gas费用（Gas.zip模块）  
  - 进行跨链转账（Avalanche ↔ X ↔ Polygon）  
  - 委派质押任务  
  - 查询验证节点的状态  
  - 签署消息  
  **不适用场景：**  
  - 在去中心化交易所（DEX）上进行交易（建议使用bankr工具）  
  - 管理ENS（建议使用moltbook脚本）  
  **网络架构：**  
  支持通过Routescan进行EVM链间的RPC通信，并提供公共回退机制。  
  **费用计算：**  
  所有操作均按每次交易产生的Gas费用计费。
metadata:
  {
    "openclaw":
      {
        "emoji": "⛓️",
        "homepage": "https://github.com/iJaack/evalanche",
        "source": "https://github.com/iJaack/evalanche",
        "requires": { "bins": ["node"] },
        "env":
          [
            {
              "name": "AGENT_PRIVATE_KEY",
              "description": "Hex-encoded private key (EVM). Optional if using boot() or AGENT_MNEMONIC.",
              "required": false,
              "secret": true,
            },
            {
              "name": "AGENT_MNEMONIC",
              "description": "BIP-39 mnemonic phrase (required for Avalanche multi-VM X/P-Chain). Optional if using boot() or AGENT_PRIVATE_KEY.",
              "required": false,
              "secret": true,
            },
            {
              "name": "AGENT_ID",
              "description": "ERC-8004 agent token ID for identity resolution (Avalanche C-Chain only).",
              "required": false,
            },
            {
              "name": "AGENT_KEYSTORE_DIR",
              "description": "Directory for encrypted keystore in boot() mode. Default: ~/.evalanche/keys",
              "required": false,
            },
            {
              "name": "AVALANCHE_NETWORK",
              "description": "EVM chain alias: 'ethereum', 'base', 'arbitrum', 'optimism', 'polygon', 'bsc', 'avalanche', 'fuji', etc. Default: avalanche.",
              "required": false,
            },
            {
              "name": "EVM_CHAIN",
              "description": "Alias for AVALANCHE_NETWORK. EVM chain to connect to.",
              "required": false,
            },
          ],
        "configPaths": ["~/.evalanche/keys/agent.json"],
        "install":
          [
            {
              "id": "node",
              "kind": "node",
              "package": "evalanche",
              "bins": ["evalanche-mcp"],
              "label": "Install evalanche (npm)",
            },
          ],
      },
  }
---
# Evalanche — 多EVM代理钱包

这是一个无头钱包SDK，支持ERC-8004身份验证、x402支付协议、Li.Fi跨链桥接功能以及Gas.zip跨链燃料支付。可在21个以上的EVM区块链上使用，既可作为命令行工具（CLI），也可作为MCP（Multi-Chain Protocol）服务器使用。

**来源：** https://github.com/iJaack/evalanche  
**许可证：** MIT  

## 支持的区块链  
Ethereum、Base、Arbitrum、Optimism、Polygon、BSC、Avalanche、Fantom、Gnosis、zkSync Era、Linea、Scroll、Blast、Mantle、Celo、Moonbeam、Cronos、Berachain，以及测试网（Fuji、Sepolia、Base Sepolia）。  

优先使用Routescan RPC进行通信；在Routescan不可用时，会使用公共的备用RPC接口。  

## 安全模型  

### 密钥存储与加密  
`Evalanche.boot()`会自动管理密钥，并采用**加密存储**机制：  
1. **首次运行时：** 通过`ethers.HDNodeWallet.createRandom()`生成BIP-39助记词。  
2. **加密方式：** AES-128-CTR加密算法，结合scrypt KDF（兼容geth的密钥存储格式）。  
3. **密码生成：** 使用`crypto.randomBytes(32)`生成32字节的随机熵值作为密码。  
4. **文件权限设置：** 设置为`chmod 0o600`（仅所有者可读写）。  
5. **密钥存储路径：** 默认为`~/.evalanche/keys/`。  

### MCP服务器访问控制  
- **标准模式（默认）：** 仅通过标准输入/输出（stdin/stdout）进行通信，不暴露网络接口。  
- **HTTP模式（`--http`）：** 运行在`localhost:3402`，未经授权不得公开访问。  

### OpenClaw外部秘钥（优先使用）  
在可用情况下，优先使用OpenClaw提供的秘钥；其次使用环境变量中的秘钥，最后使用加密后的密钥文件。  

## 设置步骤  

### 1. 安装  
```bash
npm install -g evalanche
```  

### 2. 在任意区块链上启动钱包  
```javascript
import { Evalanche } from 'evalanche';

// Base
const { agent } = await Evalanche.boot({ network: 'base' });

// Ethereum
const { agent: eth } = await Evalanche.boot({ network: 'ethereum' });

// Arbitrum
const { agent: arb } = await Avalanche.boot({ network: 'arbitrum' });

// Avalanche (with identity)
const { agent: avax } = await Evalanche.boot({
  network: 'avalanche',
  identity: { agentId: '1599' },
});
```  

### 3. 作为MCP服务器运行  
```bash
AVALANCHE_NETWORK=base evalanche-mcp
```  

## 可用工具（MCP）  

### 钱包功能  
| 工具 | 功能描述 |  
|------|-------------|  
| `get_address` | 获取代理钱包地址 |  
| `get_balance` | 查看原生代币余额 |  
| `sign_message` | 签署任意消息 |  
| `send_avax` | 发送原生代币 |  
| `call_contract` | 调用合约方法 |  

### 身份验证（ERC-8004）  
| 工具 | 功能描述 |  
|------|-------------|  
| `resolve_identity` | 查证代理身份及信誉评分 |  
| `resolve_agent` | 根据ID查找代理节点 |  

### 支付功能（x402）  
| 工具 | 功能描述 |  
|------|-------------|  
| `pay_and_fetch` | 发起基于x402协议的支付请求 |  

### 信誉管理  
| 工具 | 功能描述 |  
|------|-------------|  
| `submit_feedback` | 提交链上信誉反馈 |  

### 网络与区块链管理  
| 工具 | 功能描述 |  
|------|-------------|  
| `get_network` | 获取当前网络配置 |  
| `get_supported_chains` | 列出所有支持的区块链 |  
| `get_chain_info` | 查看特定区块链的详细信息 |  
| `switch_network` | 切换到其他EVM区块链 |  

### 跨链桥接功能  
| 工具 | 功能描述 |  
|------|-------------|  
| `get_bridge_quote` | 获取跨链桥接报价（Li.Fi） |  
| `get_bridge_routes` | 查看所有桥接路由选项 |  
| `bridge_tokens` | 在不同区块链之间转移代币 |  
| `fund_destination_gas` | 通过Gas.zip为交易提供燃料（跨链费用） |  

## 程序化使用示例  

### 在Base区块链上查看余额  
```bash
node -e "
const { Evalanche } = require('evalanche');
const agent = new Evalanche({ privateKey: process.env.AGENT_PRIVATE_KEY, network: 'base' });
agent.provider.getBalance(agent.address).then(b => {
  const { formatEther } = require('ethers');
  console.log(formatEther(b) + ' ETH');
});
"
```  

### 在Ethereum到Arbitrum之间转移代币  
```bash
node -e "
const { Evalanche } = require('evalanche');
const agent = new Evalanche({ privateKey: process.env.AGENT_PRIVATE_KEY, network: 'ethereum' });
agent.bridgeTokens({
  fromChainId: 1, toChainId: 42161,
  fromToken: '0x0000000000000000000000000000000000000000',
  toToken: '0x0000000000000000000000000000000000000000',
  fromAmount: '0.1', fromAddress: agent.address,
}).then(r => console.log('tx:', r.txHash));
"
```  

### 在Avalanche区块链上进行跨链转账（需要助记词）  
```bash
node -e "
const { Evalanche } = require('evalanche');
const agent = new Evalanche({ mnemonic: process.env.AGENT_MNEMONIC, multiVM: true });
agent.transfer({ from: 'C', to: 'P', amount: '25' })
  .then(r => console.log('export:', r.exportTxId, 'import:', r.importTxId));
"
```  

## 关键概念  

### ERC-8004代理身份（仅适用于Avalanche）  
- 在Avalanche的C-Chain上实现的链上代理身份注册系统：  
  - 代理ID包含代币URI、所有者信息及信誉评分（0-100分）。  
  - 信任等级分为：**高**（≥75分）、**中等**（≥40分）、**低**（<40分）。  

### Li.Fi跨链桥接  
- 支持跨多个主要桥接服务（如Across、Stargate、Hop等）的跨链转账；  
- 支持所有区块链上的原生代币及ERC-20代币；  
- 使用Li.Fi的REST API进行跨链操作（无需额外SDK）。  

### Gas.zip  
- 一种低成本的跨链燃料支付方式；  
- 可通过指定地址向任意目标区块链支付跨链费用。  

### x402支付协议  
- 需要通过HTTP发送402请求；  
- 支付前需解析请求参数并签名；  
- `maxPayment`功能可防止超支。  

### 多虚拟机架构（Avalanche X-Chain、P-Chain）  
- 使用助记词进行登录，并指定网络类型（`'avalanche'`或`'fuji'`）；  
- C-Chain基于EVM（ethers v6），X-Chain基于AVM（UTXO），P-Chain基于PVM（staking）。  

## 合约  
| 合约 | 地址 | 所在区块链 |  
|----------|---------|-------|  
| Identity Registry | `0x8004A169FB4a3325136EB29fA0ceB6D2e539a432` | AVAX C-Chain（43114） |  
| Reputation Registry | `0x8004BAa17C55a88189AE136b182e5fdA19dE9b63` | AVAX C-Chain（43114） |