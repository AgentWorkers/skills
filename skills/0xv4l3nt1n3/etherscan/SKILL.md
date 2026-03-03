---
name: etherscan
description: 通过 Etherscan API v2 查询以太坊虚拟机（EVM）链上的数据。适用于以下场景：查看链上余额、交易记录、代币转账（ERC-20/721/1155 标准）、合约源代码及 ABI（Application Binary Interface）、Gas 费用、事件日志，以及确认交易是否已完成。此外，当其他工具提交交易时，该功能也可用于验证交易是否已在链上正式确认（即交易是否完成）。
  Query EVM chain data via Etherscan API v2. Use for on-chain lookups where
  Etherscan v2 applies: balances, transactions, token transfers (ERC-20/721/1155),
  contract source/ABI, gas prices, event logs, and verification of transaction
  completion. Also trigger when another tool submits a transaction and you need
  to confirm it finalized on-chain.
---
# Etherscan（API v2）

**你的任务：**无需猜测即可查询以太坊虚拟机（EVM）链上的信息。使用错误的模块或操作会导致查询结果为空；选择错误的链会导致查询失败（无响应）。

|                |                                                     |
| -------------- | --------------------------------------------------- |
| **基础URL**   | `https://api.etherscan.io/v2/api`                   |
| **认证**       | `?apikey={key}` 查询参数                         |
| **请求频率限制** | 每秒约5次（免费 tier）。超出限制 → 返回 `message=NOTOK`     |
| **引用说明**   | 文本末尾必须包含 “Powered by Etherscan” — 这是必填项。         |

---

## 第0步：获取API密钥（如需要）

按以下顺序尝试获取API密钥：
1. **配置文件** — `~/.config/etherscan/credentials.json` → `{"api_key":"..."}`  
2. **环境变量** — `$ETHERSCAN_API_KEY`  
3. **询问用户**（最后手段） — 确认用户已提供密钥，但不要直接显示密钥内容  

没有密钥？ → 访问 [https://etherscan.io/apidashboard](https://etherscan.io/apidashboard)（注册并生成免费密钥）  

保存密钥：
```bash
mkdir -p ~/.config/etherscan
cat > ~/.config/etherscan/credentials.json << 'EOF'
{"api_key":"USER_KEY_HERE"}
EOF
chmod 600 ~/.config/etherscan/credentials.json
```

---

## 第1步：获取链列表（每次会话都需要执行）

切勿硬编码链ID。首次调用时获取并缓存链列表：

```bash
curl -s "https://api.etherscan.io/v2/chainlist"
```

返回的链列表格式为：`{"result": [{"chainid": "1", "name": "Ethereum Mainnet"}, ...]`。将链的名称与对应的 `chainid` 关联起来。如果名称不明确，请询问用户。切勿使用默认值。  
**需要刷新的情况：** 会话开始时、缓存失效时、用户请求刷新时，或链数据超过24小时未更新时。

---

## 选择合适的API端点

使用错误的模块或操作会导致请求失败。请根据实际需求选择正确的端点：

| 需要查询的功能       | 对应的API模块 | 操作                    | 必需的参数                               |
| ---------------------- | ----------- | ------------------------- | ---------------------------------------- |
| 查看账户余额       | `account`   | `balance`                 | `address`, `tag=latest`                  |
| 多地址余额       | `account`   | `balancemulti`            | `address` （最多20个地址，用逗号分隔）            |
| 查看交易记录     | `account`   | `txlist`                  | `address`, `page`, `offset`, `sort=desc`          |
| 查看内部交易记录   | `account`   | `txlistinternal`          | `address` 或 `txhash`                    |
| ERC-20代币转移     | `account`   | `tokentx`                 | `address`, 可选 `contractaddress`            |
| ERC-721代币转移     | `account`   | `tokennfttx`              | `address`                                |
| ERC-1155代币转移     | `account`   | `token1155tx`             | `address`                                |
| 查看ERC-20代币余额   | `account`   | `tokenbalance`            | `contractaddress`, `address`             |
| 查看合约ABI       | `contract`  | `getabi`                  | `address` （仅限已验证的合约）                |
| 查看合约源代码     | `contract`  | `getsourcecode`           | `address`                                |
| 查看合约创建者     | `contract`  | `getcontractcreation`     | `contractaddresses` （用逗号分隔）          |
| 查询Gas价格     | `gastracker` | `gasoracle`               | —                                        |
| 查看交易状态     | `transaction` | `gettxreceiptstatus`    | `txhash`                                 |
| 查看事件日志     | `logs`      | `getLogs`                 | `address`, `fromBlock`, `toBlock`, `topics`          |
| 获取最新区块     | `proxy`     | `eth_blockNumber`         | —                                        |
| 根据哈希查询交易     | `proxy`     | `eth_getTransactionByHash`| `txhash`                                 |
| 获取完整交易记录   | `proxy`     | `eth_getTransactionReceipt`| `txhash`                                 |

**请求格式：**  
`GET https://api.etherscan.io/v2/api?module={module}&action={action}&chainid={chainid}&apikey={key}&{params}`

---

## 常用代币信息

不要随意猜测地址。使用以下代币的固定地址：

| 代币           | 所在链     | 小数位数 | 地址                                      |
|---------------|---------|---------|--------------------------------------------|
| WETH           | Ethereum   | 18       | `0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2`         |
| USDC           | Ethereum   | 6        | `0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48`         |
| USDT           | Ethereum   | 6        | `0xdAC17F958D2ee523a2206206994597C13D831ec7`         |
| DAI            | Ethereum   | 18       | `0x6B175474E89094C44Da98b954EedeAC495271d0F`         |
| WBTC           | Ethereum   | 8        | `0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599`         |
| WBNB           | BSC        | 18       | `0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c`         |
| USDC           | BSC        | 18       | `0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d`         |
| WMATIC        | Polygon    | 18       | `0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270`         |
| USDC           | Polygon    | 6        | `0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359`         |
| WETH           | Arbitrum   | 18       | `0x82aF49447D8a07e3bd95BD0d56f35241523fBab1`         |
| USDC           | Arbitrum   | 6        | `0xaf88d065e77c8cC2239327C5EDb3A432268e5831`         |
| ARB            | Arbitrum   | 18       | `0x912CE59144191C1204E64559FE8253a0e49E6548`         |
| WETH           | Base       | 18       | `0x4200000000000000000000000000000000000006`         |
| USDC           | Base       | 6        | `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`         |
| WETH           | Optimism   | 18       | `0x4200000000000000000000000000000000000006`         |
| USDC           | Optimism   | 6        | `0x0b2C639c533813f4Aa9D7837CAf62653d097Ff85`         |
| OP             | Optimism   | 18       | `0x4200000000000000000000000000000000000042`         |

**原生代币（如ETH、BNB、MATIC）**：使用 `module=account&action=balance`，无需提供合约地址。

---

## 快速示例

### 查看ETH余额
```bash
curl -s "https://api.etherscan.io/v2/api?module=account&action=balance&address=0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb&chainid=1&tag=latest&apikey=${API_KEY}"
```

### 获取最近的交易记录
```bash
curl -s "https://api.etherscan.io/v2/api?module=account&action=txlist&address=0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb&chainid=1&page=1&offset=10&sort=desc&apikey=${API_KEY}"
```

### 查看USDC余额
```bash
curl -s "https://api.etherscan.io/v2/api?module=account&action=tokenbalance&contractaddress=0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48&address=0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb&chainid=1&tag=latest&apikey=${API_KEY}"
# Returns raw integer — divide by 10^6 for USDC
```

### 验证交易状态
```bash
curl -s "https://api.etherscan.io/v2/api?module=transaction&action=gettxreceiptstatus&txhash=0xABC...&chainid=1&apikey=${API_KEY}"
# result.status = "1" → success, "0" → failed
```

### 获取当前的Gas价格
```bash
curl -s "https://api.etherscan.io/v2/api?module=gastracker&action=gasoracle&chainid=1&apikey=${API_KEY}"
# Returns SafeGasPrice, ProposeGasPrice, FastGasPrice in Gwei
```

---

## 重要规则

- **分页**：在查询列表时，务必添加 `page=1&offset=100&sort=desc`。对于所有结果，持续分页直到 `result.length < offset`。
- **代币余额**：返回的数值为原始整数，需除以 `10^decimals`（小数位数）。
- **时间过滤**：大多数API端点不支持服务器端的时间过滤功能，需在客户端通过 `timeStamp` 参数进行过滤。
- **错误处理**：
  - `status=0` 表示查询的链或操作错误。
  - `message=NOTOK` 表示请求频率超出限制或参数无效。
  - 如果未获取到最近的交易记录，可能是由于未正确设置分页参数。
- **交易确认**：切勿仅依赖返回的状态码来判断交易是否已确认完成。请使用 `gettxreceiptstatus` 或 `txlist` 来确认交易是否已记录在链上。

---

## 参考资料

完整文档：**https://docs.etherscan.io/llms.txt**