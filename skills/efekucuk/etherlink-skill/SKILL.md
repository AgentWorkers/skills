---
name: etherlink
description: **Etherlink区块链交互**：  
Etherlink是一个基于Tezos平台的、与EVM（以太坊虚拟机）兼容的二层（L2）区块链解决方案。它支持通过MCP（Multi-Chain Protocol）服务器连接到Tezos的主网（mainnet）和测试网（shadownet）。用户可以利用Etherlink进行余额查询、交易处理、智能合约的部署以及代币的操作。
tags: [blockchain, evm, tezos, l2, web3, etherlink, mcp]
version: 1.0.0
---

# Etherlink 技能

**与 [Etherlink](https://etherlink.com) 交互**  
Etherlink 是一个基于 Tezos 构建的、兼容 EVM 的二层网络（L2）平台。

## 快速入门

### 1. 配置 MCP 服务器  
在您的 Claude/MCP 配置文件中添加以下内容：  
```json
{
  "mcpServers": {
    "etherlink": {
      "command": "bun",
      "args": ["run", "/path/to/etherlink-mcp-server/src/index.ts"],
      "env": {
        "EVM_PRIVATE_KEY": "your-private-key-here"
      }
    }
  }
}
```

### 2. 选择网络  
您可以使用网络名称或链 ID 来连接网络：  
- **主网 (Mainnet)**：`etherlink` 或 `42793`  
- **测试网 (Testnet)**：`etherlink-shadownet` 或 `127823`  

## 网络信息  
| 网络 | 链 ID | RPC 接口 | 探索器 (Explorer) |  
|---------|----------|------------------|------------------|  
| Etherlink 主网 | 42793 | https://node.mainnet.etherlink.com | https://explorer.etherlink.com |  
| Etherlink 测试网 | 127823 | https://node.shadownet.etherlink.com | https://shadownet.explorer.etherlink.com |  

**原生货币**：XTZ（18 位小数）  

## 常用操作  

### 检查余额  
```
Get balance for 0x... on etherlink
```  

### 发送交易  
```
Send 0.1 XTZ to 0x... on etherlink
```  

### 读取合约信息  
```
Call balanceOf on contract 0x... for address 0x... on etherlink
```  

### 获取区块信息  
```
Get latest block on etherlink
```  

## Etherlink 的特殊说明  

### 主要区别：  
1. **原生货币**：使用 XTZ（Tezos 的原生货币），而非 ETH。  
2. **未支持 EIP-1559**：目前尚未实现费用市场机制，因此仍使用传统的Gas定价方式。  
3. **区块哈希计算方式**：与以太坊不同，无法仅通过区块头验证区块哈希。  
4. **请求速率限制**：公共 RPC 请求的速率被限制为每分钟 1000 次。  

### 支持的 RPC 接口  
- ✅ `eth_blockNumber`、`eth_chainId`、`eth_getBalance`  
- ✅ `eth_call`、`eth_estimateGas`、`eth_gasPrice`  
- ✅ `eth_sendRawTransaction`、`eth_getLogs`  
- ✅ `debug_traceTransaction`  
- ❌ `eth.subscribe`（仅限实验用途）  
- ❌ `eth_newFilter` 等过滤接口  

### Tezos L1 桥接  
Etherlink 提供了与 Tezos L1 的桥梁功能，支持存款和取款操作。使用这些功能需要 Tezos 相关的工具。详情请参阅 [Etherlink 文档](https://docs.etherlink.com/building-on-etherlink/bridging)。  

## 测试网 faucet  
您可以在 [此处](https://shadownet.faucet.etherlink.com) 获取测试网 XTZ。  

## 常见问题解决方法：  
- **“不支持的网络”**：请使用正确的网络名称（`etherlink` 或 `etherlink-shadownet`）或链 ID。  
- **请求速率限制**：公共 RPC 请求的速率限制为每分钟 1000 次。如需在生产环境中使用，请自行运行节点。  
- **交易失败**：由于不支持 EIP-1559，请不要设置 `maxFeePerGas` 或 `maxPriorityFeePerGas` 参数。  

## 相关资源：  
- [Etherlink 文档](https://docs.etherlink.com/)  
- [区块浏览器](https://explorer.etherlink.com)  
- [Shadownet 探索器](https://shadownet.explorer.etherlink.com)  
- [测试网 faucet](https://shadownet.faucet.etherlink.com)