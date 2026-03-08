---
name: evalanche
description: >
  **多EVM代理钱包SDK**  
  该SDK支持链上身份验证（ERC-8004标准）、支付功能（x402协议）、跨链桥接（Li.Fi技术）以及目标链上的Gas费用支付（Gas.zip模块）。兼容21种以上的EVM区块链，包括Ethereum、Base、Arbitrum、Optimism、Polygon、BSC、Avalanche等。代理节点可自行生成和管理密钥，无需人工干预。  
  **适用场景：**  
  - 在任何EVM区块链上启动自主代理钱包  
  - 发送代币  
  - 调用智能合约  
  - 验证代理节点的身份  
  - 检查代理节点的信誉  
  - 使用x402协议进行支付操作  
  - 实现跨链代币桥接（Li.Fi技术）  
  - 在目标区块链上支付Gas费用（Gas.zip模块）  
  - 进行跨链转账（Avalanche ↔ X ↔ Polygon）  
  - 委派节点权益  
  - 查询验证节点信息  
  - 创建子网  
  - 使用BLS密钥添加新的验证节点  
  - 查询节点详细信息  
  **不适用场景：**  
  - 管理ENS（建议使用moltbook脚本）。  
  **网络架构：**  
  该SDK基于EVM的RPC通信机制，通过Routescan进行网络连接，并提供公共备用方案（public fallbacks）。  
  **费用模型：**  
  所有操作均按交易次数收取Gas费用。
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

这是一个无头钱包SDK，支持ERC-8004身份验证、x402支付协议、Li.Fi跨链桥接功能以及Gas.zip跨链燃料支付服务。该钱包兼容21个以上的EVM区块链，并可作为命令行工具（CLI）或MCP服务器使用。

**来源：** https://github.com/iJaack/evalanche  
**许可证：** MIT  

## 支持的区块链  
Ethereum、Base、Arbitrum、Optimism、Polygon、BSC、Avalanche、Fantom、Gnosis、zkSync Era、Linea、Scroll、Blast、Mantle、Celo、Moonbeam、Cronos，以及相应的测试网络（Fuji、Sepolia、Base Sepolia）。  

在可用情况下，优先使用Routescan RPC接口；若Routescan不可用，则使用公共的备用RPC接口。  

## 安全模型  

### 密钥存储与加密  
`Evalanche.boot()`会自动管理密钥，并采用**加密存储**机制：  
1. **首次运行时：** 通过`ethers.HDNodeWallet.createRandom()`生成BIP-39助记词。  
2. **加密方式：** AES-128-CTR加密算法，结合scrypt KDF（兼容geth的密钥存储格式）。  
3. **密码生成：** 使用`crypto.randomBytes(32)`生成32字节的随机熵值作为密码。  
4. **文件权限设置：** `chmod 0o600`（仅允许所有者读写）。  
5. **密钥存储位置：** 默认为`~/.evalanche/keys/`。  

### MCP服务器访问控制  
- **标准模式（默认）：** 仅通过标准输入/输出（stdin/stdout）进行交互，不暴露网络接口。  
- **HTTP模式（`--http`）：** 运行在`localhost:3402`端口；未经授权不得公开访问。  

### OpenClaw外部密钥（优先使用）  
在可以使用OpenClaw的情况下，优先使用其提供的密钥；其次使用环境变量中的密钥，最后使用加密后的密钥存储文件。  

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

### 3. 以MCP服务器模式运行  
```bash
AVALANCHE_NETWORK=base evalanche-mcp
```  

## 可用的工具（MCP）  

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
| `resolve_agent` | 根据ID查询代理信息 |  

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

### Arena DEX（Avalanche）  
| 工具 | 功能描述 |  
|------|-------------|  
| `arena_buy` | 通过绑定曲线购买Arena社区代币（需支付$ARENA） |  
| `arena_sell` | 以$ARENA价格出售Arena社区代币 |  
| `arena_token_info` | 根据地址查询代币信息（包括费用和曲线参数） |  
| `arena_buy_cost` | 计算购买所需费用（仅读） |  

### 跨链桥接功能  
| 工具 | 功能描述 |  
|------|-------------|  
| `get_bridge_quote` | 获取跨链桥接报价（Li.Fi） |  
| `get_bridge_routes` | 查看所有可用的桥接路径 |  
| `bridge_tokens` | 在不同区块链之间转移代币 |  
| `fund_destination_gas` | 通过Gas.zip为跨链交易提供燃料 |  

### 平台命令行工具（需安装`platform-cli`）  
**安装命令：** `go install github.com/ava-labs/platform-cli@latest`  
| 工具 | 功能描述 |  
|------|-------------|  
| `platform_cli_available` | 检查是否已安装platform-cli |  
| `subnet_create` | 创建新的Avalanche子网 |  
| `subnet_convert_l1` | 将子网转换为L1区块链 |  
| `subnet_transfer_ownership` | 转移子网所有权 |  
| `add-validator` | 将验证者添加到主网络 |  
| `l1_register_validator` | 注册新的L1验证者 |  
| `l1_add_balance` | 为L1验证者添加余额 |  
| `l1_disable-validator` | 禁用L1验证者 |  
| `node_info` | 从运行中的节点获取NodeID和BLS密钥 |  
| `pchain_send` | 在P-Chain上发送AVAX代币 |  

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

### 在Avalanche上进行跨链转移（需使用助记词）  
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
  - 代理ID包含代币URI、所有者信息、信誉评分（0-100分）和信任等级（**高**≥75、**中**≥40、**低**<40）。  
- **信任等级**用于衡量代理的可靠性。  

### Li.Fi跨链桥接  
- 支持跨所有主要区块链（如Across、Stargate、Hop等）的桥接服务；  
- 支持所有区块链的原生代币和ERC-20代币；  
- 无需依赖第三方SDK，直接使用Li.Fi的REST API进行桥接操作。  

### Gas.zip  
- 提供低成本的跨链燃料服务；  
- 可通过指定地址向任意目标区块链发送燃料（Gas）。  

### x402支付协议  
- 需要通过HTTP发送402请求；  
- 支持支付请求的解析和重试机制；  
- `maxPayment`功能可防止超支。  

### 多虚拟机环境支持（Avalanche的X-Chain、P-Chain）  
- 使用BIP-39助记词进行身份验证；  
- 需指定网络类型（`network: 'avalanche'`或`'fuji'`）。  
- C-Chain使用EVM（ethers v6），X-Chain使用AVM（UTXO），P-Chain使用PVM（staking）。  

## 合约管理  
| 合约 | 地址 | 所在区块链 |  
|----------|---------|-------|  
| Identity Registry | `0x8004A169FB4a3325136EB29fA0ceB6D2e539a432` | AVAX C-Chain（43114） |  
| Reputation Registry | `0x8004BAa17C55a88189AE136b182e5fdA19dE9b63` | AVAX C-Chain（43114） |