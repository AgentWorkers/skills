---
name: sponge-wallet
description: 管理加密钱包、转账代币、在去中心化交易所（DEX）上进行交易、查询账户余额，并通过 x402 微支付功能访问付费 API（如搜索、图像生成、预测市场、网络爬虫、文档解析、销售线索挖掘等）。当用户询问钱包余额、代币转账、交易详情、区块链支付或付费 API 服务时，可使用该功能。
---

# Sponge 钱包技能

这是一个支持多链加密货币的钱包，提供转账、交换以及付费 API 访问功能。

## 认证

**重要提示**：如果任何工具返回 “Not authenticated” 或 “Invalid API key”，请执行登录流程。

登录分为两个阶段（因为 Claude Code 是非交互式地执行命令的）：

**第1阶段** — 启动设备登录流程（返回一个 URL 和代码，格式为 JSON）：
```bash
node <skill-path>/scripts/wallet.mjs login
```
将 `verification_url` 和 `user_code` 显示给用户，告诉他们在浏览器中打开该 URL 并输入代码。

**第2阶段** — 用户确认批准后，请求令牌：
```bash
node <skill-path>/scripts/wallet.mjs login --poll <device_code> <interval> <expires_in>
```
使用第1阶段输出中的 `device_code`、`interval` 和 `expires_in` 值。

凭据会自动保存到 `~/.spongewallet/credentials.json` 文件中。

凭据的解析顺序如下：
1. `SPONGE_API_KEY` 环境变量（如果已设置，则跳过已保存的凭据）
2. `~/.spongewallet/credentials.json`（通过登录保存的凭据）

其他认证命令：
- `node wallet.mjs whoami` — 显示当前的认证状态
- `node wallet.mjs logout` — 删除已保存的凭据

## 执行方式

```bash
node <skill-path>/scripts/wallet.mjs <tool_name> '<json_args>'
```

输出结果为 JSON 格式，其中 `status` 可能为 “success” 或 “error”。

## 可用工具

### 钱包与余额

| 工具 | 描述 | 必需参数 | 可选参数 |
|------|-------------|----------|----------|
| `get_balance` | 查看各链路的余额 | — | `chain` |
| `get_solana_tokens` | 查找钱包中的所有 SPL 代币 | `chain` | — |
| `search_solana_tokens` | 在 Jupiter 代币数据库中搜索 | `query` | `limit` |

### 转账

| 工具 | 描述 | 必需参数 | 可选参数 |
|------|-------------|----------|----------|
| `evm_transfer` | 在 Ethereum 或 Base 上转账 ETH/USDC | `chain`, `to`, `amount`, `currency` | — |
| `solana_transfer` | 在 Solana 上转账 SOL/USDC | `chain`, `to`, `amount`, `currency` | — |

### 交换

| 工具 | 描述 | 必需参数 | 可选参数 |
|------|-------------|----------|----------|
| `solana_swap` | 通过 Jupiter 进行代币交换 | `chain`, `input_token`, `output_token`, `amount` | `slippage_bps` |

### 交易

| 工具 | 描述 | 必需参数 | 可选参数 |
|------|-------------|----------|----------|
| `get_transaction_status` | 查查交易状态 | `transaction_hash`, `chain` | — |
| `get_transaction_history` | 查看历史交易 | — | `limit`, `chain` |

### 资金注入与提取

| 工具 | 描述 | 必需参数 | 可选参数 |
|------|-------------|----------|----------|
| `request_funding` | 从所有者处请求资金 | `amount`, `chain`, `currency` | — |
| `withdraw_to_main_wallet` | 将资金退还给所有者 | `chain`, `amount` | `currency` |

### 付费 API（Sponge x402）

| 工具 | 描述 | 必需参数 | 可选参数 |
|------|-------------|----------|----------|
| `sponge` | 统一的付费 API 接口 | `task` | 详见 [REFERENCE.md](REFERENCE.md) |
| `create_x402_payment` | 创建 x402 支付请求 | `chain`, `to`, `amount` | `token`, `decimals` |

## 链路参考

**测试地址** (`sponge_test_*`): `sepolia`, `base-sepolia`, `solana-devnet`, `tempo`
**生产地址** (`sponge_live_*`): `ethereum`, `base`, `solana`

## 常见工作流程

### 检查余额 → 转账 → 验证

```bash
node wallet.mjs get_balance '{"chain":"base"}'
node wallet.mjs evm_transfer '{"chain":"base","to":"0x...","amount":"10","currency":"USDC"}'
node wallet.mjs get_transaction_status '{"transaction_hash":"0x...","chain":"base"}'
```

### 在 Solana 上交换代币

```bash
node wallet.mjs search_solana_tokens '{"query":"BONK"}'
node wallet.mjs solana_swap '{"chain":"solana","input_token":"SOL","output_token":"BONK","amount":"0.5"}'
```

### Sponge 付费 API

```bash
node wallet.mjs sponge '{"task":"search","query":"AI research papers"}'
node wallet.mjs sponge '{"task":"image","prompt":"sunset over mountains"}'
node wallet.mjs sponge '{"task":"predict","semantic_search":"will-trump-win-2028"}'
node wallet.mjs sponge '{"task":"crawl","url":"https://example.com"}'
node wallet.mjs sponge '{"task":"parse","document_url":"https://example.com/doc.pdf"}'
node wallet.mjs sponge '{"task":"prospect","apollo_query":"Stripe","apollo_endpoint":"companies"}'
```

## 错误处理

| 错误类型 | 处理方法 |
|-------|------------|
| `Not authenticated` | 执行 `node wallet.mjs login` 进行登录 |
| `Invalid API key` | 执行 `node wallet.mjs login` 重新认证 |
| `Chain 'X' is not allowed` | 使用正确的链路类型（测试地址或生产地址） |
| `Insufficient balance` | 使用 `request_funding` 请求资金 |
| `Address not in allowlist` | 将接收者添加到允许列表中 |

详细参数说明请参阅 [REFERENCE.md](REFERENCE.md)。