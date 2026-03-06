---
name: QELT Blockchain
description: 通过 JSON-RPC 查询和交互 QELT 区块链（链 ID 770）。适用于查询区块、交易、钱包余额、智能合约调用、gas 估算、事件日志、nonce 以及提交原始交易等场景。支持 QELT 主网（770）和测试网（771）。
read_when:
  - Querying QELT blocks or transactions
  - Checking wallet balances on QELT
  - Estimating gas for a QELT transaction
  - Fetching event logs from QELT contracts
  - Submitting a pre-signed raw transaction to QELT
  - Looking up nonce or contract code on QELT
homepage: https://docs.qelt.ai
metadata: {"clawdbot":{"emoji":"⛓️","requires":{"bins":["curl"]}}}
allowed-tools: Bash(qelt-blockchain:*)
---
# QELT区块链技能

QELT是一个企业级区块链平台，基于Hyperledger Besu 25.12.0构建，兼容EVM（以太坊虚拟机），采用QBFT（Quorum-Based Fault Tolerance）共识机制。每个区块的确认时间仅为5秒，且不存在基础交易费用（约0.002美元/笔交易）。

**主网：** 链ID `770` · RPC接口：`https://mainnet.qelt.ai`  
**测试网：** 链ID `771` · RPC接口：`https://testnet.qelt.ai`  
**存档（历史数据+交易追踪）：** `https://archivem.qelt.ai`

## 安全注意事项

- **严禁** 请求、存储、打印或传输私钥或助记词。  
- 所有写入操作仅接受**预签名过的原始交易数据**（以`0x`开头的十六进制字符串）。  
- 如需查询历史数据或交易追踪信息，请使用`https://archivem.qelt.ai`。  
- 在提交交易前，请确认当前使用的是主网还是测试网。  
- **切勿** 自定义区块编号、哈希值或账户余额——请始终获取实时数据。

## 终端节点

| 功能 | URL            |
|------|-------------------|
| 主网RPC接口 | `https://mainnet.qelt.ai`     |
| 主网存档/交易追踪 | `https://archivem.qelt.ai`     |
| 测试网RPC接口 | `https://testnet.qelt.ai`     |
| 测试网存档 | `https://archive.qelt.ai`     |
| 区块浏览器 | `https://qeltscan.ai`       |
| 索引器API | `https://mnindexer.qelt.ai`     |

## JSON-RPC调用

所有API调用均遵循标准的Ethereum JSON-RPC 2.0协议，采用`POST`请求方式。

### 获取最新区块编号  
```bash
curl -fsSL -X POST https://mainnet.qelt.ai \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}'
```  
解析`result`（十六进制字符串）后，使用`printf '%d\n' <hex>`输出结果。

### 获取区块信息  
```bash
# By number (hex): block 1000 = 0x3e8
curl -fsSL -X POST https://mainnet.qelt.ai \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_getBlockByNumber","params":["0x3e8",true],"id":1}'

# By hash
curl -fsSL -X POST https://mainnet.qelt.ai \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_getBlockByHash","params":["0xHASH",true],"id":1}'
```  

### 获取账户余额  
```bash
curl -fsSL -X POST https://mainnet.qelt.ai \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_getBalance","params":["0xADDRESS","latest"],"id":1}'
```  
将`result`（以wei为单位，十六进制表示）除以`10^18`以获得QELT的实际余额。

### 获取交易详情  
```bash
curl -fsSL -X POST https://mainnet.qelt.ai \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_getTransactionByHash","params":["0xTX_HASH"],"id":1}'
```  

### 获取交易收据  
```bash
curl -fsSL -X POST https://mainnet.qelt.ai \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_getTransactionReceipt","params":["0xTX_HASH"],"id":1}'
```  
- `status: "0x1"` 表示交易成功；  
- `status: "0x0"` 表示交易被回滚。

### 调用智能合约（仅限读取）  
```bash
curl -fsSL -X POST https://mainnet.qelt.ai \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_call","params":[{"to":"0xCONTRACT","data":"0xCALLDATA"},"latest"],"id":1}'
```  

### 估算交易所需Gas费用  
```bash
curl -fsSL -X POST https://mainnet.qelt.ai \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_estimateGas","params":[{"from":"0xFROM","to":"0xTO","data":"0xDATA","value":"0x0"}],"id":1}'
```  

### 获取事件日志  
- 请指定区块范围进行查询；从创世区块（`"0x0"`）开始查询会扫描整个链，可能导致速率限制或超时。建议使用最近1,000个区块的数据，如需更多历史记录可分页查询。  
```bash
# First get the current block number
LATEST=$(curl -fsSL -X POST https://mainnet.qelt.ai \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}' | python3 -c "import sys,json; print(json.load(sys.stdin)['result'])")

# Then query a bounded recent range (last ~1000 blocks ≈ 83 minutes on QELT)
# Clamp at 0 so the start block is never negative on a low-height chain (e.g. fresh testnet).
FROM_HEX=$(python3 -c "latest=int('$LATEST',16); print(hex(max(0, latest - 1000)))")

curl -fsSL -X POST https://mainnet.qelt.ai \
  -H "Content-Type: application/json" \
  -d "{\"jsonrpc\":\"2.0\",\"method\":\"eth_getLogs\",\"params\":[{\"fromBlock\":\"$FROM_HEX\",\"toBlock\":\"latest\",\"address\":\"0xCONTRACT\",\"topics\":[\"0xTOPIC\"]}],\"id\":1}"
```  
- 如需完整的历史日志，请使用`https://archivem.qelt.ai`，并每次查询不超过10,000个区块以避免超时。

### 获取合约代码  
```bash
curl -fsSL -X POST https://mainnet.qelt.ai \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_getCode","params":["0xCONTRACT","latest"],"id":1}'
```  
- `0x` 表示合约未被部署；  
- 其他值表示合约已部署。

### 获取随机数（Nonce）  
```bash
curl -fsSL -X POST https://mainnet.qelt.ai \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_getTransactionCount","params":["0xADDRESS","latest"],"id":1}'
```  

### 发送预签名交易  
⚠️ **写入操作**：执行前请务必获得用户确认。  
```bash
curl -fsSL -X POST https://mainnet.qelt.ai \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_sendRawTransaction","params":["0xSIGNED_TX_HEX"],"id":1}'
```  
成功执行后返回交易哈希值。

### 获取链信息  
```bash
# Chain ID
curl -fsSL -X POST https://mainnet.qelt.ai \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_chainId","params":[],"id":1}'

# Gas price
curl -fsSL -X POST https://mainnet.qelt.ai \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_gasPrice","params":[],"id":1}'
```  

## 网络参数  

| 参数          | 主网         | 测试网         |
|---------------|--------------|--------------|
| 链ID         | 770 (0x302)      | 771 (0x303)      |
| RPC接口        | `https://mainnet.qelt.ai`   | `https://testnet.qelt.ai`   |
| 存档接口        | `https://archivem.qelt.ai`   | `https://archive.qelt.ai`   |
| 索引器接口      | `https://mnindexer.qelt.ai` | `https://tnindexer.qelt.ai` |
| 区块确认时间     | 5秒           | 5秒           |
| Gas上限        | 50,000,000       | 50,000,000       |
| 基础交易费用     | 0             | 0             |
| 使用的EVM版本     | Cancun         | Cancun         |
| 测试网水龙头      | `https://testnet.qeltscan.ai/faucet` |               |

## MetaMask配置（主网）  
```json
{
  "chainId": "0x302",
  "chainName": "QELT Mainnet",
  "nativeCurrency": { "name": "QELT", "symbol": "QELT", "decimals": 18 },
  "rpcUrls": ["https://mainnet.qelt.ai"],
  "blockExplorerUrls": ["https://qeltscan.ai"]
}
```  

## 常见错误及解决方法  

| 错误类型 | 原因           | 解决方案         |
|---------|-----------------|-------------------------|
| `execution reverted` | 合约调用失败     | 检查ABI编码是否正确           |
| `nonce too low` | 随机数过期       | 使用`eth_getTransactionCount`获取最新随机数 |
| `insufficient funds` | 缺乏足够的QELT来支付Gas费用 | 为钱包充值或使用测试网水龙头       |
| `unknown block` | 无法找到相关区块     | 使用`https://archivem.qelt.ai`查询历史数据     |
| HTTP 429/503     | 被速率限制       | 实施指数级重试策略         |