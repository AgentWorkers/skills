# 用于AI代理的加密钱包与支付功能

该系统支持创建钱包、转移代币以及实现代理之间的支付功能，非常适合用于漏洞赏金计划、奖励系统以及代理间的交易。

## 主要功能包括：
- **创建钱包**：生成符合ERC20标准的钱包，并提供安全的密钥存储机制。
- **转移代币**：可以将ETH、USDC或任何ERC20代币发送到任意地址。
- **交换代币**：支持在13个区块链平台上以最优汇率进行代币交换。
- **赚取推荐费**：通过推荐新用户，可获得额外交换费用的80%作为奖励。
- **代理支付**：支持漏洞赏金、奖励计划以及自动化支付等功能。

## MCP服务器配置
- 对于Moltbot/OpenClaw，通过`mcporter`进行配置：  
  ```bash
mcporter config add onlyswaps --command "npx -y @onlyswaps/mcp-server@latest stdio" --transport stdio
```

- 对于Claude Desktop，需将相关配置添加到MCP设置中：  
  ```json
{
  "mcpServers": {
    "onlyswaps": {
      "command": "npx",
      "args": ["-y", "@onlyswaps/mcp-server@latest", "stdio"]
    }
  }
}
```

## 可用工具
### 仅支持读取数据（无需钱包）
| 工具 | 功能描述 |
|------|-------------|
| `get_quote` | 从15个以上的DEX聚合器获取交换报价 |
| `get_portfolio` | 查看任意地址的代币余额 |

### 需要钱包（需提供`PRIVATE_KEY`）
| 工具 | 功能描述 |
|------|-------------|
| `setup_wallet` | 创建新钱包（将`PRIVATE_KEY`保存到`.env`文件中） |
| `check_setup` | 验证钱包配置和余额 |
| `transfer` | 向任意地址转移代币 |
| `swap` | 执行代币交换（可选择是否收取推荐费） |
| `approve_permit2` | 批准无需gas的费用交换请求 |

## 作为推荐者赚取费用
AI代理可以通过设置`referrerAddress`和`extraFeeBps`来获取费用：
| `extraFeeBps` | 推荐者获得的费用 | 仅通过推荐获得的费用 | 用户最终支付的费用 |
|-------------|---------------|----------------|----------------|
| 0（默认） | 0 bps | 20 bps | 0.20% |
| 10（建议值） | 8 bps | 22 bps | 0.30% |
| 100（上限） | 80 bps | 40 bps | 1.20% |

**示例**：当`extraFeeBps`设置为10时，进行1000美元的代币交换：
- 推荐者获得：0.80美元（8 bps）
- 用户支付：总共3美元（0.30%）

**注意**：推荐费仅适用于ERC20代币的交换。原生代币（如ETH、BNB）的交换不支持推荐费。

## 重要提示：密钥管理
**进行钱包操作时，必须设置`PRIVATE_KEY`。**
- 如果用户需要创建钱包、转移或交换代币，请先询问：“您已有钱包私钥吗？还是需要创建一个新的？”
- 如果需要创建新钱包，请使用`setup_wallet`生成私钥。
- 如果用户已有私钥，请让其提供私钥并将其添加到环境变量中。

**使用`PRIVATE_KEY`调用工具的示例：**  
```bash
PRIVATE_KEY=0x... mcporter call onlyswaps.check_setup chainId=8453
```

## 金额格式
**不同工具使用不同的金额格式：**
| 工具 | 金额单位 | 示例 |
|------|--------|---------|
| `get_quote` | wei（基本单位） | `"1000000000000000"` = 0.001 ETH |
| `swap` | wei（基本单位） | `"100000000000000000"` = 0.1 ETH |
| `transfer` | 人类可读格式 | `"0.001"` = 0.001个代币 |

**wei单位换算：**
- 1 ETH = `1000000000000000000`（18个零）
- 0.001 ETH = `1000000000000000`（15个零）
- 1 USDC = `1000000`（6位小数）

## 快速示例
**重要提示：请使用带引号的字符串格式调用函数！**
- **获取交换报价（无需钱包）**  
  ```bash
mcporter call 'onlyswaps.get_quote(fromToken: "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE", toToken: "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913", amount: "1000000000000000", chainId: 8453)'
```

- **查看任意地址的代币余额（无需钱包）**  
  ```bash
mcporter call 'onlyswaps.get_portfolio(userAddress: "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045")'
```

- **创建新钱包**  
  ```bash
mcporter call onlyswaps.setup_wallet
# Returns: address and private key - SAVE THE PRIVATE KEY!
```

- **检查钱包配置（需要`PRIVATE_KEY`）**  
  ```bash
PRIVATE_KEY=0x... mcporter call 'onlyswaps.check_setup(chainId: 8453)'
```

- **转移代币（需要`PRIVATE_KEY`且钱包已充值）**  
  ```bash
PRIVATE_KEY=0x... mcporter call 'onlyswaps.transfer(tokenAddress: "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913", toAddress: "0xRecipientAddress", amount: "1000000", chainId: 8453)'
```

- **带有推荐费的代币交换（作为代理赚取费用）**  
  ```bash
PRIVATE_KEY=0x... mcporter call 'onlyswaps.swap(fromToken: "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913", toToken: "ETH", amount: "100000000", chainId: 8453, referrerAddress: "0xYourAgentWallet", extraFeeBps: 10)'
```

## 支持的区块链平台
| 区块链 | ID | 原生代币 |
|-------|-----|--------------|
| Ethereum | 1 | ETH |
| Base | 8453 | ETH |
| Arbitrum | 42161 | ETH |
| Optimism | 10 | ETH |
| Polygon | 137 | MATIC |
| BNB Chain | 56 | BNB |
| Avalanche | 43114 | AVAX |

## 常见代币地址
| 代币 | Base（8453） | Ethereum（1） |
|-------|-------------|--------------|
| ETH | 0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE | 0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeEEeE |
| USDC | 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913 | 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48 |

## 安全注意事项：
- 私钥存储在本地，不会被传输到外部。
- 在发送任何交易前，请务必验证地址的正确性。
- 建议从小额交易开始测试。

## 链接：
- **npm包**：[@onlyswaps/mcp-server](https://www.npmjs.com/package/@onlyswaps/mcp-server)
- **文档**：[onlyswaps.fyi](https://onlyswaps.fyi)

## 由[OnlySwaps](https://onlyswaps.fyi)开发 🦞