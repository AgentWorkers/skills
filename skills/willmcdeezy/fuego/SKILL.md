---
name: fuego
description: 本地Solana代理钱包，配备用于转账（SOL、USDC、USDT）、Jupiter交易以及x402代币购买的本地基础设施。
homepage: https://fuego.cash
version: 1.4.0
metadata:
  {
    "openclaw":
      {
        "emoji": "🔥",
        "requires": { "bins": ["curl", "node", "cargo"], "env": [] },
        "optional": { "bins": [], "env": [] },
      },
  }
---
# Fuego SKILL

这是一个基于Solana的本地代理钱包工具，支持SOL、USDC、USDT等币种的转账，以及Jupiter平台的代币交换和x402支付功能。

## 快速入门

### 1. 安装fuego-cli
```bash
npm install -g fuego-cli
```

### 2. 创建钱包
```bash
fuego create

# Output:
# Address: DmFyLRiJtc4Bz75hjAqPaEJpDfRe4GEnRLPwc3EgeUZF
# Wallet config: ~/.fuego/wallet-config.json
# Backup: ~/.config/solana/fuego-backup.json
```

### 3. 安装Fuego项目

**前提条件：** 需要Rust 1.85及以上版本和Cargo工具来构建服务器。

```bash
# For OpenClaw agents (auto-detects ~/.openclaw/workspace)
fuego install

# For manual installs (specify path)
fuego install --path ~/projects/fuego
```

### 4. 配置Jupiter API密钥（可选 - 用于代币交换）

如果您希望通过Jupiter进行代币交换，需要一个API密钥：
1. 访问 https://portal.jup.ag 注册
2. 创建一个新的API密钥（免费 tier可用）
3. 将密钥添加到您的Fuego配置文件 `~/.fuego/config.json` 中：

```json
{
  "rpcUrl": "https://api.mainnet-beta.solana.com",
  "network": "mainnet-beta",
  "jupiterKey": "your-jupiter-api-key-here"
}
```

如果没有这个密钥，代币交换将无法进行。不过，余额检查和转账功能仍然可以使用。

### 5. 启动服务器
```bash
fuego serve

# Output:
# Fuego server running on http://127.0.0.1:8080
```

### 6. 显示钱包地址
```bash
fuego address

# Output:
# Your Fuego Address
# Name: default
# Public Key: DmFy...eUZF
```

将钱包地址分享给他人，以便他们可以向您的钱包充值。他们可以从任何Solana钱包（如Phantom、Solflare等）发送SOL。

### 7. 充值钱包

**选项A：MoonPay（将法定货币转换为加密货币）**
- 访问：https://buy.moonpay.com/?currency=SOL&address=YOUR_ADDRESS
- 最低充值金额：约30美元
- 充值立即到钱包

**选项B：手动转账**
- 他人复制上述地址
- 从他们的钱包向您的Fuego地址发送SOL
- 每笔交易需要支付0.001 SOL的交易费用

---

## 发送交易

**推荐使用CLI：**

```bash
fuego send <recipient> <amount> --token USDC --yes
```

这个命令会：
- 使用最新的区块哈希构建交易
- 在本地完成签名（不会暴露任何网络密钥）
- 向区块链提交交易并处理错误
- 返回签名和交易浏览器链接
- 支持地址簿中的联系人
- 通过 `--token` 标志支持SOL、USDC、USDT等币种

**示例：**
```bash
fuego send GvCoHGGBR97Yphzc6SrRycZyS31oUYBM8m9hLRtJT7r5 0.25 --token USDC --yes
```

---

## 通过Jupiter进行代币交换

### 第一步：获取报价
在执行交易前，务必向用户显示预期的汇率：

```bash
fuego quote --input BONK --output USDC --amount 100000
```

输出内容包括：
- 输入金额（自动处理小数位）
- 预期输出金额
- 价格影响
- 路由详情

### 第二步：执行交换
用户确认报价后：

```bash
fuego swap --input BONK --output USDC --amount 100000 --slippage 1.0
```

**参数：**
- `--input` - 输入代币符号（如SOL、USDC、BONK等）或发行地址
- `--output` - 输出代币符号或发行地址
- `--amount` - 代币数量（例如：100000 BONK对应100000个BONK）
- `--slippage` - 容错率（默认：0.5%）

交换脚本会自动：
- 从链上获取正确的代币小数位
- 使用BigInt确保精度（避免浮点数错误）
- 如果无法确定小数位，则会抛出错误（防止金额错误）

**前提条件：**
- 必须在 `~/.fuego/config.json` 中配置Jupiter API密钥
- 请参考快速入门的第4步进行设置。

---

## 代理就绪架构

```
Agent/Script
       ↓ POST /build-transfer-sol
Fuego Server (localhost:8080)
  • Builds unsigned transaction with fresh blockhash
  • Returns base64-encoded transaction + memo
       ↓ Unsigned Transaction
Agent/Script
  • Loads ~/.fuego/wallet.json (simple JSON, no password!)
  • Signs transaction locally
       ↓ Signed Transaction
Fuego Server (localhost:8080)
  • POST /submit-transaction
  • Broadcasts to Solana mainnet
       ↓ On-chain
Solana Network
```

**安全模型：**
- 私钥永远不会离开您的设备（所有转账操作都在客户端进行签名）
- 严格的文件权限设置（chmod 600）确保安全
- 服务器仅限本地访问（localhost）
- 使用标准的Solana格式，兼容所有CLI工具

**唯一例外：x402支付**
 `/x402-purch` 端点负责整个支付流程（包括签名），因为x402支付需要服务器端生成支付证明。这是一个有意的安全权衡：服务器仅在处理特定x402支付交易时临时访问私钥，之后立即将其从内存中清除。这样可以在保持其他操作本地处理的同时，实现无缝的代理购买功能。

---

## API参考

### GET /wallet-address
动态获取本地钱包地址。

```bash
curl http://127.0.0.1:8080/wallet-address
```

**响应：**
```json
{
  "success": true,
  "data": {
    "address": "DmFyLRiJtc4Bz75hjAqPaEJpDfRe4GEnRLPwc3EgeUZF",
    "network": "mainnet-beta",
    "source": "wallet"
  }
}
```

### POST /balance - 检查SOL余额
```bash
curl -X POST http://127.0.0.1:8080/balance \
  -H "Content-Type: application/json" \
  -d '{"network": "mainnet-beta", "address": "YOUR_ADDRESS"}'
```

**响应：**
```json
{
  "success": true,
  "data": {
    "sol": 1.234567890,
    "lamports": 1234567890,
    "network": "mainnet-beta"
  }
}
```

### POST /tokens - 检查所有代币余额
```bash
curl -X POST http://127.0.0.1:8080/tokens \
  -H "Content-Type: application/json" \
  -d '{"network": "mainnet-beta", "address": "YOUR_ADDRESS"}'
```

返回SOL余额以及所有SPL代币（如USDC、USDT、BONK等）的余额。

### POST /build-transfer-sol - 构建SOL转账
```bash
curl -X POST http://127.0.0.1:8080/build-transfer-sol \
  -H "Content-Type: application/json" \
  -d '{
    "network": "mainnet-beta",
    "from_address": "YOUR_ADDRESS",
    "to_address": "RECIPIENT_ADDRESS",
    "amount": "0.001",
    "yid": "agent-transfer-123"
  }'
```

**响应：**
```json
{
  "success": true,
  "data": {
    "transaction": "AQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAAEDAb...",
    "blockhash": "J7rBdM33dHKtJwjp...AbCdEfGhIjKl",
    "memo": "fuego|SOL|f:YOUR_ADDRESS|t:RECIPIENT|a:1000000|yid:agent-transfer-123|n:",
    "network": "mainnet-beta"
  }
}
```

### POST /build-transfer-usdc - 构建USDC转账
```bash
curl -X POST http://127.0.0.1:8080/build-transfer-usdc \
  -H "Content-Type: application/json" \
  -d '{
    "network": "mainnet-beta",
    "from_address": "YOUR_ADDRESS",
    "to_address": "RECIPIENT_ADDRESS",
    "amount": "10.50",
    "yid": "agent-usdc-456"
  }'
```

### POST /build-transfer-usdt - 构建USDT转账
```bash
curl -X POST http://127.0.0.1:8080/build-transfer-usdt \
  -H "Content-Type: application/json" \
  -d '{
    "network": "mainnet-beta",
    "from_address": "YOUR_ADDRESS",
    "to_address": "RECIPIENT_ADDRESS",
    "amount": "25.75",
    "yid": "agent-usdt-789"
  }'
```

### POST /submit-transaction - 广播已签名的交易
```bash
curl -X POST http://127.0.0.1:8080/submit-transaction \
  -H "Content-Type: application/json" \
  -d '{
    "network": "mainnet-beta",
    "transaction": "BASE64_SIGNED_TRANSACTION"
  }'
```

**响应：**
```json
{
  "success": true,
  "data": {
    "signature": "5J7XzY...9KpQrS",
    "explorer_link": "https://explorer.solana.com/tx/5J7XzY...9KpQrS?cluster=mainnet-beta"
  }
}
```

---

## 代理集成方式

### 对于编写代码的代理（如Node.js等）

**只需通过subprocess调用CLI即可。**

CLI负责所有工作：构建交易、签名、提交和错误处理。无需将其封装成类，直接使用即可。

**Node.js/TypeScript示例：**
```javascript
import { execSync } from 'child_process';

// Send payment
const result = execSync(
  'fuego send GvCo... 0.25 --token USDC --yes',
  { encoding: 'utf-8' }
);
console.log(result);
```

### 替代方案：原始API集成（不推荐）

如果您必须使用原始API调用而非CLI，请使用下面文档中的端点。但强烈建议使用CLI。

---

## 完整API参考

### GET /
根端点 - 返回服务器状态。

```bash
curl http://127.0.0.1:8080/
```

**响应：**
```
Fuego Server
```

### GET /health
健康检查端点。

```bash
curl http://127.0.0.1:8080/health
```

**响应：**
```json
{
  "status": "healthy",
  "service": "fuego-server",
  "version": "0.1.0"
}
```

### GET /network
获取默认的网络配置。

```bash
curl http://127.0.0.1:8080/network
```

**响应：**
```json
{
  "network": "mainnet-beta"
}
```

### GET /wallet-address
动态获取本地钱包地址。

```bash
curl http://127.0.0.1:8080/wallet-address
```

**响应：**
```json
{
  "success": true,
  "data": {
    "address": "DmFyLRiJtc4Bz75hjAqPaEJpDfRe4GEnRLPwc3EgeUZF",
    "network": "mainnet-beta",
    "source": "wallet"
  }
}
```

### POST /latest-hash
获取最新的区块哈希，用于构建交易。

```bash
curl -X POST http://127.0.0.1:8080/latest-hash \
  -H "Content-Type: application/json" \
  -d '{"network": "mainnet-beta"}'
```

**响应：**
```json
{
  "success": true,
  "data": {
    "blockhash": "J7rBdM33dHKtJwjp...",
    "network": "mainnet-beta"
  }
}
```

### POST /sol-balance - 检查SOL余额
```bash
curl -X POST http://127.0.0.1:8080/sol-balance \
  -H "Content-Type: application/json" \
  -d '{"network": "mainnet-beta", "address": "YOUR_ADDRESS"}'
```

**响应：**
```json
{
  "success": true,
  "data": {
    "address": "YOUR_ADDRESS",
    "lamports": 105113976,
    "sol": 0.105113976,
    "network": "mainnet-beta"
  }
}
```

### POST /usdc-balance - 检查USDC余额
```bash
curl -X POST http://127.0.0.1:8080/usdc-balance \
  -H "Content-Type: application/json" \
  -d '{"network": "mainnet-beta", "address": "YOUR_ADDRESS"}'
```

**响应：**
```json
{
  "success": true,
  "data": {
    "usdc": 150.250000,
    "raw_amount": "150250000",
    "network": "mainnet-beta"
  }
}
```

### POST /usdt-balance - 检查USDT余额
```bash
curl -X POST http://127.0.0.1:8080/usdt-balance \
  -H "Content-Type: application/json" \
  -d '{"network": "mainnet-beta", "address": "YOUR_ADDRESS"}'
```

**响应：**
```json
{
  "success": true,
  "data": {
    "usdt": 75.500000,
    "raw_amount": "75500000",
    "network": "mainnet-beta"
  }
}
```

### POST /tokens - 检查所有代币余额
```bash
curl -X POST http://127.0.0.1:8080/tokens \
  -H "Content-Type: application/json" \
  -d '{"network": "mainnet-beta", "address": "YOUR_ADDRESS"}'
```

返回SOL余额以及所有SPL代币（如USDC、USDT、BONK等）的余额。

**响应：**
```json
{
  "success": true,
  "data": {
    "wallet": "DmFyLRiJtc4Bz75hjAqPaEJpDfRe4GEnRLPwc3EgeUZF",
    "network": "mainnet",
    "sol_balance": 0.105113976,
    "sol_lamports": 105113976,
    "token_count": 2,
    "tokens": [
      {
        "symbol": "USDC",
        "ui_amount": 28.847897,
        "decimals": 6,
        "mint": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
      }
    ]
  }
}
```

### POST /all-transactions - 获取交易历史
```bash
curl -X POST http://127.0.0.1:8080/all-transactions \
  -H "Content-Type: application/json" \
  -d '{"network": "mainnet-beta", "address": "YOUR_ADDRESS", "limit": 20}'
```

返回所有钱包交易记录。Fuego的交易（备注中包含 `fuego|` 的交易）会在仪表板上以详细格式显示。

### POST /build-transfer-sol - 构建SOL转账
```bash
curl -X POST http://127.0.0.1:8080/build-transfer-sol \
  -H "Content-Type: application/json" \
  -d '{
    "network": "mainnet-beta",
    "from_address": "YOUR_ADDRESS",
    "to_address": "RECIPIENT_ADDRESS",
    "amount": "0.001",
    "yid": "agent-transfer-123"
  }'
```

**响应：**
```json
{
  "success": true,
  "data": {
    "transaction": "AQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAAEDAb...",
    "blockhash": "J7rBdM33dHKtJwjp...AbCdEfGhIjKl",
    "memo": "fuego|SOL|f:YOUR_ADDRESS|t:RECIPIENT|a:1000000|yid:agent-transfer-123|n:",
    "network": "mainnet-beta"
  }
}
```

### POST /build-transfer-usdc - 构建USDC转账
```bash
curl -X POST http://127.0.0.1:8080/build-transfer-usdc \
  -H "Content-Type: application/json" \
  -d '{
    "network": "mainnet-beta",
    "from_address": "YOUR_ADDRESS",
    "to_address": "RECIPIENT_ADDRESS",
    "amount": "10.50",
    "yid": "agent-usdc-456"
  }'
```

### POST /build-transfer-usdt - 构建USDT转账
```bash
curl -X POST http://127.0.0.1:8080/build-transfer-usdt \
  -H "Content-Type: application/json" \
  -d '{
    "network": "mainnet-beta",
    "from_address": "YOUR_ADDRESS",
    "to_address": "RECIPIENT_ADDRESS",
    "amount": "25.75",
    "yid": "agent-usdt-789"
  }'
```

### POST /submit-transaction - 广播已签名的交易
```bash
curl -X POST http://127.0.0.1:8080/submit-transaction \
  -H "Content-Type: application/json" \
  -d '{
    "network": "mainnet-beta",
    "transaction": "BASE64_SIGNED_TRANSACTION"
  }'
```

**响应：**
```json
{
  "success": true,
  "data": {
    "signature": "5J7XzY...9KpQrS",
    "explorer_link": "https://explorer.solana.com/tx/5J7XzY...9KpQrS?cluster=mainnet-beta"
  }
}
```

### POST /submit-versioned-transaction - 广播版本化的交易
```bash
curl -X POST http://127.0.0.1:8080/submit-versioned-transaction \
  -H "Content-Type: application/json" \
  -d '{
    "network": "mainnet-beta",
    "transaction": "BASE64_VERSIONED_TRANSACTION"
  }'
```

### POST /x402-purch - x402支付（服务器端签名）
完成包括服务器端签名在内的x402支付流程。适用于Purch.xyz等集成。

```bash
curl -X POST http://127.0.0.1:8080/x402-purch \
  -H "Content-Type: application/json" \
  -d '{
    "network": "mainnet-beta",
    "product_url": "https://amazon.com/dp/B071G6PFDR",
    "email": "user@example.com",
    "shipping_name": "John Doe",
    "shipping_address_line1": "123 Main St",
    "shipping_city": "Austin",
    "shipping_state": "TX",
    "shipping_postal_code": "78701",
    "shipping_country": "US"
  }'
```

---

## 安全最佳实践

### Fuego的安全性保障

1. **严格的文件权限** - 确保文件安全（私钥仅保存在本地）
2. **客户端签名**（有一个例外）：
   - 私钥从不通过网络传输（用于转账、交换等操作）
   - 签名在客户端脚本中完成
   - 服务器仅接收已签名的交易数据
   **例外：** x402支付需要服务器端签名以生成支付证明。私钥仅用于该特定交易，使用后立即清除
3. **仅限本地访问的服务器** - 服务器绑定到127.0.0.1（仅限本地访问）
   - 无需配置防火墙
4. **标准格式兼容性** - 与所有CLI工具兼容

### 代理安全检查清单

- 保护 `~/.fuego/wallet.json` 文件的安全（其中包含您的私钥！）
- 不要将钱包文件提交到版本控制系统中
- 始终在本地（localhost）运行服务器
- 定期备份 `~/.config/solana/fuego-backup.json`
- 在Solana浏览器中验证交易
- 定期检查钱包余额
- 使用强化的系统级用户隔离机制

---

## 故障排除

### 常见问题

- **“钱包未初始化”错误**
```bash
# Solution: Create wallet with fuego-cli
fuego create
```

- **“服务器未运行”错误**
```bash
# Solution: Start server
fuego serve
```

- **“连接被拒绝”错误**
```bash
# Check if server is running
curl http://127.0.0.1:8080/health

# If not running, start it
fuego serve
```

- **“找不到Fuego服务器”错误**
```bash
# Solution: Install the fuego project
fuego install
```

- **“交易模拟失败”错误**
```bash
# Usual cause: Insufficient balance
# Check all token balances first
curl -X POST http://127.0.0.1:8080/tokens \
  -H "Content-Type: application/json" \
  -d '{"network": "mainnet-beta", "address": "YOUR_ADDRESS"}'
```

- **“签名无效”错误**
```bash
# Wallet file might be corrupted
# Restore from backup
cp ~/.config/solana/fuego-backup.json ~/.fuego/wallet.json
```

- **版本不匹配/行为异常**
```bash
# Ensure all components are up to date
fuego update

# This updates both fuego-cli and the fuego project
# Restart server after updating: fuego serve
```

---

## 支持的代币与网络

### 可转账的代币（使用fuego send）

这些代币可以通过 `fuego send` 进行转账：
| 代币 | 发行地址 | 小数位 | 状态 |
|-------|-------------|----------|--------|
| **SOL** | Native | 9 | 正在运行 |
| **USDC** | `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v` | 6 | 正在运行 |
| **USDT** | `Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenEqw` | 6 | 正在运行 |

### 可交换的代币（使用fuego swap/Jupiter）

`fuego swap` 支持在Jupiter平台上交易的任何代币，包括：
- SOL、USDC、USDT
- BONK、JUP、PYTH、RAY、ORCA
- 在Jupiter上有流动性的任何SPL代币

完整代币列表请访问 https://jup.ag

### 网络支持
- **mainnet-beta** - 生产环境Solana网络
- **devnet** - 开发/测试网络
- **testnet** - Solana测试网络（有限使用）

准备好构建自主的Solana代理了吗？从Fuego开始吧。