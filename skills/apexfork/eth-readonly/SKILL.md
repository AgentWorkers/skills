---
name: eth-readonly
description: 只读的以太坊区块链查询功能：通过 RPC 和 Etherscan API 可以查询区块、交易、账户余额、合约信息以及日志记录。
user-invocable: true
homepage: https://github.com/Fork-Development-Corp/openclaw-web3-skills/tree/master/eth-readonly
metadata: {"openclaw":{"requires":{"anyBins":["cast","curl"]},"tipENS":"apexfork.eth"}}
---
# 仅读的以太坊查询功能

您是一个仅读的以太坊辅助工具，可帮助用户查询区块链状态、查看历史数据以及探索智能合约。**该功能仅用于读取数据——无需钱包，也不会发送任何交易。** 如果 `Foundry` 的 `cast` 工具在您的路径中可用，请优先使用它；否则，您可以使用 `curl` 来构建原始的 JSON-RPC 请求。

## 安全第一

**请注意：** 该功能仅支持读取操作，不涉及私钥管理、钱包操作或交易签名。您可以安全地探索区块链数据，而无需承担任何资金损失或泄露秘密的风险。

## RPC 配置

### 公共 RPC 端点（立即可用）

**免费公共端点**（无需 API 密钥）：
```bash
# Ethereum mainnet
export ETH_RPC_URL="https://ethereum.publicnode.com"
export ETH_RPC_URL="https://rpc.ankr.com/eth" 
export ETH_RPC_URL="https://eth.llamarpc.com"

# Sepolia testnet  
export SEPOLIA_RPC_URL="https://rpc.ankr.com/eth_sepolia"
export SEPOLIA_RPC_URL="https://ethereum-sepolia.publicnode.com"
```

**主要服务提供商**（需要 API 密钥）：
```bash
# Infura
export ETH_RPC_URL="https://mainnet.infura.io/v3/${INFURA_PROJECT_ID}"

# Alchemy  
export ETH_RPC_URL="https://eth-mainnet.g.alchemy.com/v2/${ALCHEMY_API_KEY}"

# QuickNode
export ETH_RPC_URL="https://${QUICKNODE_ENDPOINT}.quiknode.pro/${QUICKNODE_TOKEN}/"
```

**本地节点**（如果您自己运行了以太坊节点）：
```bash
export ETH_RPC_URL="http://localhost:8545"
```

### 使用方式
```bash
# Use environment variable
cast block-number --rpc-url $ETH_RPC_URL

# Or specify directly
cast balance vitalik.eth --rpc-url https://ethereum.publicnode.com
```

**⚠️ 调用限制：** 公共端点存在调用限制。Infura 的免费账户每天允许 10 万次请求；Alchemy 的免费账户每月允许 3 亿次计算单元的请求。在进行日志查询时，请使用较小的时间范围。

## 链路 ID 核验

在进行任何交易之前，请务必验证所使用的区块链链路的 ID：

```bash
cast chain-id --rpc-url $ETH_RPC_URL
```

常见的链路 ID 包括：1（主网）、11155111（sepolia）、17000（holesky）。

## 检测可用的工具

```bash
command -v cast && echo "cast available" || echo "using curl fallback"
```

## 查询区块链状态

### 实时查询示例

**获取最新区块（无需 API 密钥）：**
```bash
cast block-number --rpc-url https://ethereum.publicnode.com
```

**查询 Vitalik 的以太币余额：**
```bash
cast balance vitalik.eth --rpc-url https://ethereum.publicnode.com
# Output: 2139127306712808209 (wei) = ~2139 ETH
```

**查找最近的一笔交易：**
```bash
cast tx 0x... --rpc-url https://ethereum.publicnode.com
```

### 常见的查询模式

```bash
# Account balance (using env var)
cast balance 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045 --rpc-url $ETH_RPC_URL

# Transaction receipt
cast receipt 0xTXHASH --rpc-url $ETH_RPC_URL

# Contract code
cast code 0xA0b86a33E6441929FD1F423c7ecE8F6DD15fA5E3 --rpc-url $ETH_RPC_URL  # USDC

# ENS resolution
cast resolve-name vitalik.eth --rpc-url $ETH_RPC_URL
cast lookup-address 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045 --rpc-url $ETH_RPC_URL
```

**对应的 JSON-RPC 请求示例（使用 `curl`）：**
```bash
# Block number
curl -s -X POST https://ethereum.publicnode.com \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_blockNumber","id":1}'

# Balance  
curl -s -X POST $ETH_RPC_URL \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_getBalance","params":["0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045","latest"],"id":1}'
```

### Nonce（账户的交易次数）

这对于调试卡住或待处理的交易非常有用：

**使用 `cast`：**
```bash
# Confirmed nonce
cast nonce 0xADDRESS --rpc-url http://localhost:8545

# Pending nonce (includes mempool txs)
cast nonce 0xADDRESS --block pending --rpc-url http://localhost:8545
```

**使用 `curl`：**
```bash
curl -s -X POST http://localhost:8545 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_getTransactionCount","params":["0xADDRESS","latest"],"id":1}'
```

如果确认的 `nonce` 小于待处理的 `nonce`，则表示内存池中存在未确认的交易。有关交易管理和替换的更多信息，请参阅 `/foundry` 功能。

## 调用智能合约（仅读）

**使用 `cast`：**
```bash
cast call 0xCONTRACT "balanceOf(address)" 0xADDRESS --rpc-url http://localhost:8545
```

**使用 `curl`（`eth_call`）：**
```bash
curl -s -X POST http://localhost:8545 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_call","params":[{"to":"0xCONTRACT","data":"0xABI_ENCODED_DATA"},"latest"],"id":1}'
```

在构建原始数据负载时，可以使用 `cast calldata` 来对函数调用进行 ABI 编码。

## 交易分析（仅读）

**查询交易详情：**
```bash
cast tx 0xTXHASH --rpc-url $ETH_RPC_URL
cast receipt 0xTXHASH --rpc-url $ETH_RPC_URL
```

**解码交易数据：**
```bash
cast 4byte-decode 0xCALLDATA
cast abi-decode "transfer(address,uint256)" 0xOUTPUT
```

## 气体价格分析

**当前的气体价格：**
```bash
# Via Etherscan
curl -s "https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey=$ETHERSCAN_API_KEY" | jq '.result'

# Via RPC
cast gas-price --rpc-url $ETH_RPC_URL
cast base-fee --rpc-url $ETH_RPC_URL
```

## 事件日志查询

**⚠️ 必须指定合约地址，并使用特定的区块范围。** 全范围查询可能会立即耗尽 RPC 调用限制。

```bash
# Good: specific contract + block range
cast logs 0xA0b86a33E6441929FD1F423c7ecE8F6DD15fA5E3 --from-block 19000000 --to-block 19001000 \
  "Transfer(address,address,uint256)" --rpc-url $ETH_RPC_URL

# BAD: will likely fail on public RPCs
cast logs --from-block 0 --to-block latest "Transfer(address,address,uint256)"
```

使用 `curl` 时，请务必在请求中包含 `"address": "0xCONTRACT"` 以及具体的 `fromBlock`/`toBlock` 参数。

## Etherscan API 集成

**设置：**
```bash
export ETHERSCAN_API_KEY="your_api_key_here"  # Get free key at etherscan.io/apis
```

### 智能合约源代码
```bash
# Get verified contract source
curl -s "https://api.etherscan.io/api?module=contract&action=getsourcecode&address=0xA0b86a33E6441929FD1F423c7ecE8F6DD15fA5E3&apikey=$ETHERSCAN_API_KEY" | jq '.result[0].SourceCode'

# Check if contract is verified
curl -s "https://api.etherscan.io/api?module=contract&action=getabi&address=0xA0b86a33E6441929FD1F423c7ecE8F6DD15fA5E3&apikey=$ETHERSCAN_API_KEY"
```

### 交易历史记录
```bash
# 获取账户的交易记录（最近 10 笔）
curl -s "https://api.etherscan.io/api?module=account&action=txlist&address=0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045&startblock=0&endblock=99999999&page=1&offset=10&sort=desc&apikey=$ETHERSCAN_API_KEY" | jq '.result[] | {hash: .hash, value: .value, gas: .gas}'

# 获取 ERC-20 代币的转移记录
curl -s "https://api.etherscan.io/api?module=account&action=tokentx&address=0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045&page=1&offset=10&sort=desc&apikey=$ETHERSCAN_API_KEY" | jq '.result[] | {tokenName: .tokenName, tokenSymbol: .tokenSymbol, value: .value}'
```

### Gas Tracker
```

# 当前的气体价格
curl -s "https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey=$ETHERSCAN_API_KEY" | jq '.result'
# 输出示例：{"SafeGasPrice": "12", "ProposeGasPrice": "13", "FastGasPrice": "14"}
```

### Block & Network Stats
```

# 根据区块编号获取区块信息
curl -s "https://api.etherscan.io/api?module=proxy&action=eth_getBlockByNumber&tag=0x10d4f&boolean=true&apikey=$ETHERSCAN_API_KEY" | jq '.result | {number: .number, timestamp: .timestamp, gasUsed: .gasUsed}'

# 获取以太币的总供应量
curl -s "https://api.etherscan.io/api?module=stats&action=ethsupply&apikey=$ETHERSCAN_API_KEY" | jq '.result'
```

**调用限制：** 免费账户每秒允许 5 次请求，每天最多 10 万次请求。更多高级功能需购买专业套餐。