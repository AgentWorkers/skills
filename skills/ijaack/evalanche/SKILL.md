---
name: evalanche
description: Avalanche的非托管代理钱包SDK，支持链上身份验证（ERC-8004）和支付功能（x402）。代理可以自行生成和管理密钥，无需人工干预。适用场景包括：启动自主代理钱包、发送AVAX代币、调用智能合约、验证代理身份、检查代理信誉、执行基于x402协议的支付请求、进行跨链转账（C↔X↔P）、委托质押、查询验证节点信息以及签署消息等。不适用场景：在去中心化交易所（DEX）中进行交易（请使用bankr）、桥接至非Avalanche区块链（请使用lifi-bridge）、管理ENS域名（请使用moltbook脚本）。网络支持：Avalanche的RPC协议。费用：每次交易需支付Gas费用。
metadata:
  {
    "openclaw":
      {
        "emoji": "🏔️",
        "homepage": "https://github.com/iJaack/evalanche",
        "source": "https://github.com/iJaack/evalanche",
        "requires": { "bins": ["node"] },
        "env":
          [
            {
              "name": "AGENT_PRIVATE_KEY",
              "description": "Hex-encoded private key (C-Chain only). Optional if using boot() or AGENT_MNEMONIC.",
              "required": false,
              "secret": true,
            },
            {
              "name": "AGENT_MNEMONIC",
              "description": "BIP-39 mnemonic phrase (required for multi-VM X/P-Chain). Optional if using boot() or AGENT_PRIVATE_KEY.",
              "required": false,
              "secret": true,
            },
            {
              "name": "AGENT_ID",
              "description": "ERC-8004 agent token ID for identity resolution.",
              "required": false,
            },
            {
              "name": "AGENT_KEYSTORE_DIR",
              "description": "Directory for encrypted keystore in boot() mode. Default: ~/.evalanche/keys",
              "required": false,
            },
            {
              "name": "AVALANCHE_NETWORK",
              "description": "Network: 'avalanche' (mainnet) or 'fuji' (testnet). Default: avalanche.",
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
# Evalanche — Avalanche的代理钱包

Evalanche是一个无头钱包SDK，支持ERC-8004身份验证和x402支付协议。它可以作为命令行工具（CLI）使用，也可以作为MCP（Multi-Chain Platform）服务器运行。

**来源：** https://github.com/iJaack/evalanche  
**许可证：** MIT  

## 安全模型  

### 密钥存储与加密  

`Evalanche.boot()`会自动管理密钥，并采用**加密存储**的方式：  
1. **首次运行时：** 通过`ethers.HDNodeWallet.createRandom()`生成BIP-39助记词（使用Node.js的`crypto.randomBytes`生成随机熵值）。  
2. **加密方式：** 使用ethers v6的keystore格式（**AES-128-CTR + scrypt KDF**）进行加密——与geth/MetaMask的密钥存储格式相同。  
3. **密码生成：** 通过`crypto.randomBytes(32)`生成一个32字节的随机熵值文件，并与keystore一起存储；加密密码就是从这个熵值文件中派生出来的。系统不使用用户设定的密码。  
4. **文件权限：** keystore文件（`agent.json`）和熵值文件（`.agent.json.entropy`）的权限设置为`chmod 0o600`（仅允许所有者读写）。  
5. **存储位置：** 默认存储在`~/.evalanche/keys/`目录下，可通过`AGENT_KEYSTORE_DIR`或`keystore.dir`选项进行配置。  

**这意味着：**  
- 私钥和助记词**永远不会以明文形式存储在磁盘上。  
- 如果攻击者同时获得了keystore和熵值文件，他们才能解密钱包。  
- 安全性依赖于操作系统级别的文件权限（0o600）和文件系统访问控制。  
- 为了更高安全性，可以将`~/.evalanche/keys/`目录挂载到加密的存储设备上，或者使用`AGENT_PRIVATE_KEY`环境变量来管理密钥（例如通过Vault、AWS KMS等工具）。  

### MCP服务器的访问控制  

- **标准模式（默认）：** 仅通过标准输入/输出（stdin/stdout）进行通信，不暴露于网络，适用于本地使用（如Claude Desktop、Cursor等工具）。  
- **HTTP模式（`--http`）：** 默认绑定到`localhost:3402`端口。**未经反向代理和身份验证的情况下，切勿将其暴露在公共网络中。** HTTP接口没有内置的身份验证机制，仅适用于本地或可信网络环境。在生产环境中，建议使用nginx/caddy等服务器，并结合TLS协议和API密钥认证。  

### 环境变量  

所有环境变量都是**可选的**。系统支持三种运行模式：  
1. **`boot()`模式**（无需环境变量）：代理程序自动生成并管理加密后的keystore。  
2. **手动提供密钥**（使用`AGENT_PRIVATE_KEY`或`AGENT_MNEMONIC`环境变量）。  
3. **指定keystore路径**（使用`AGENT_KEYSTORE_DIR`环境变量）。  

## 设置  

### 1. 安装  
```bash
npm install -g evalanche
```  

安装前，请确认包的源代码与GitHub仓库中的内容一致：  
```bash
npm info evalanche repository.url  # Should show github.com/iJaack/evalanche
```  

### 2. 启动（非托管模式——无需配置）  
```javascript
import { Evalanche } from 'evalanche';

// First run: generates wallet + encrypts to ~/.evalanche/keys/agent.json
// Every subsequent run: decrypts and loads existing wallet
const { agent, keystore } = await Evalanche.boot({
  network: 'avalanche',
  identity: { agentId: '1599' },
});

console.log(agent.address);        // 0x... (same every time)
console.log(keystore.isNew);       // true first time, false after
console.log(keystore.keystorePath); // ~/.evalanche/keys/agent.json
```  

### 2b. 使用现有密钥（可选）  
```bash
export AGENT_PRIVATE_KEY="0x..."       # For C-Chain only
export AGENT_MNEMONIC="word1 word2..." # For multi-VM (X/P/C chains)
export AGENT_ID="1599"                  # ERC-8004 agent ID
export AVALANCHE_NETWORK="avalanche"    # or "fuji" for testnet
```  

### 3. 作为MCP服务器运行（可选）  
```bash
# Stdio mode (recommended — no network exposure)
evalanche-mcp

# HTTP mode (localhost only — do NOT expose publicly without auth)
evalanche-mcp --http --port 3402
```  

## 可用的工具（MCP）  

当作为MCP服务器运行时，以下工具可供使用：  

### 钱包工具  
| 工具 | 功能 |  
|------|-------------|  
| `get_address` | 获取代理钱包地址 |  
| `get_balance` | 查看AVAX余额（C-Chain） |  
| `sign_message` | 签署任意消息 |  
| `send_avax` | 向指定地址发送AVAX |  
| `call_contract` | 调用合约方法 |  

### 身份验证（ERC-8004）  
| 工具 | 功能 |  
|------|-------------|  
| `resolve_identity` | 查找代理的链上身份及信誉信息 |  
| `resolve_agent` | 根据ID查询代理信息 |  

### 支付工具（x402）  
| 工具 | 功能 |  
|------|-------------|  
| `pay_and_fetch` | 发起基于x402协议的支付请求 |  

### 信誉管理工具  
| 工具 | 功能 |  
|------|-------------|  
| `submit_feedback` | 为其他代理提交链上信誉反馈 |  

### 网络工具  
| 工具 | 功能 |  
|------|-------------|  
| `get_network` | 获取当前网络配置 |  

## 程序化使用（不使用MCP）  

### 查看余额  
```bash
node -e "
const { Evalanche } = require('evalanche');
const agent = new Evalanche({ privateKey: process.env.AGENT_PRIVATE_KEY });
agent.provider.getBalance(agent.address).then(b => {
  const { formatEther } = require('ethers');
  console.log(formatEther(b) + ' AVAX');
});
"
```  

### 发送AVAX  
```bash
node -e "
const { Avalanche } = require('evalanche');
const agent = new Evalanche({ privateKey: process.env.AGENT_PRIVATE_KEY });
agent.send({ to: '0xRECIPIENT', value: '0.1' }).then(r => console.log('tx:', r.hash));
"
```  

### 跨链转账（需要助记词）  
```bash
node -e "
const { Evalanche } = require('evalanche');
const agent = new Evalanche({ mnemonic: process.env.AGENT_MNEMONIC, multiVM: true });
agent.transfer({ from: 'C', to: 'P', amount: '25' })
  .then(r => console.log('export:', r.exportTxId, 'import:', r.importTxId));
"
```  

## 关键概念  

### ERC-8004代理身份  
- Avalanche C-Chain上的链上代理身份注册系统：  
  - 代理ID包含tokenURI、所有者信息、信誉分数（0-100分）和信任等级。  
  - 信任等级分为：**高**（≥75）、**中等**（≥40）、**低**（<40）、**未知**（null）。  
  - 身份注册地址：`0x8004A169FB4a3325136EB29fA0ceB6D2e539a432`  
  - 信誉注册地址：`0x8004BAa17C55a88189AE136b182e5fdA19dE9b63`  

### x402支付协议  
- 支付请求必须遵循HTTP 402协议；系统会解析请求内容、签名后再尝试支付；  
- `maxPayment`参数用于防止超支。  
- 支付流程包括：请求 → 发送x402响应 → 支付 → 根据反馈重新尝试。  

### 多链环境（X-Chain、P-Chain）  
- 需要提供助记词才能生成X-Chain和P-Chain的密钥；  
- C-Chain使用EVM（以太坊虚拟机，基于ethers v6），X-Chain使用AVAX的UTXO模型，P-Chain使用PVM（staking机制）。  
- 跨链转账支持原子性的数据导入/导出操作。  

### 合约  
| 合约 | 地址 | 所在链 |  
|----------|---------|-------|  
| 身份注册合约 | `0x8004A169FB4a3325136EB29fA0ceB6D2e539a432` | AVAX C-Chain（43114） |  
| 信誉注册合约 | `0x8004BAa17C55a88189AE136b182e5fdA19dE9b63` | AVAX C-Chain（43114） |  

## 网络连接  
| 网络 | RPC接口 | 所在链ID |  
|---------|-----|----------|  
| Avalanche主网 | `https://api.avax.network/ext/bc/C/rpc` | 43114 |  
| Fuji测试网 | `https://api.avax-test.network/ext/bc/C/rpc` | 43113 |