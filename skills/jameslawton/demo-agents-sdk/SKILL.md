---
name: polygon-agent-kit
description: 完整的Polygon代理工具包。基于会话的智能合约钱包（Sequence），代币操作（通过Trails发送/交换/桥接/存入），支持ERC-8004标准的链上身份验证与信誉系统，支持x402微支付功能。提供统一的命令行接口（CLI）入口点，数据存储采用AES-256-GCM加密技术。
---
# Polygon Agent Kit

## 先决条件
- Node.js 20+  
- 全局安装：`npm install -g github:0xPolygon/polygon-agent-kit`  
- 进入点：`polygon-agent <command>`  
- 存储路径：`~/.polygon-agent/`（使用 AES-256-GCM 加密）

## 架构

| 钱包 | 创建工具 | 用途 | 是否支持资金操作？ |
|--------|-----------|---------|-------|
| EOA | `setup` | 通过 Sequence Builder 进行身份验证 | 不支持 |
| 生态系统钱包 | `wallet create` | 主要支出钱包 | 支持 |

## 环境变量

### 必需的环境变量  
| 变量 | 使用场景 |  
|----------|------|  
| `SEQUENCE_PROJECT_ACCESS_KEY` | 钱包创建、交易操作 |  
| `SEQUENCE_INDEXER_ACCESS_KEY` | 检查账户余额 |  

### 可选的环境变量  
| 变量 | 默认值 |  
|----------|---------|  
| `SEQUENCE_ECOSYSTEM_CONNECTOR_URL` | `https://agentconnect.staging.polygon.technology/` |  
| `SEQUENCE_DAPP_origin` | 与连接器 URL 相同 |  
| `NGROK_AUTHTOKEN` | 自动设置（匿名隧道）；如需使用命名隧道，请手动设置 |  
| `TRAILS_API_KEY` | 默认使用 `SEQUENCEPROJECT_ACCESS_KEY` |  
| `TRAILS_TOKEN_MAP_JSON` | 用于查询令牌信息 |  
| `POLYGON_AGENT_DEBUG FETCH` | 关闭（日志输出至 `~/.polygon-agent/fetch-debug.log`） |  
| `POLYGON_AGENT_DEBUG_FEE` | 关闭（费用信息输出至标准错误流） |  

## 完整的设置流程  
```bash
# Phase 1: Setup (creates EOA + Sequence project, returns access key)
node cli/polygon-agent.mjs setup --name "MyAgent"
# → save privateKey (not shown again), eoaAddress, accessKey

# Phase 2: Create ecosystem wallet (auto-waits for browser approval)
export SEQUENCE_PROJECT_ACCESS_KEY=<accessKey>
node cli/polygon-agent.mjs wallet create --usdc-limit 100 --native-limit 5

# Phase 3: Fund wallet
node cli/polygon-agent.mjs fund
# → opens Trails widget URL, fund via swap/bridge

# Phase 4: Verify
export SEQUENCE_INDEXER_ACCESS_KEY=<indexerKey>
node cli/polygon-agent.mjs balances

# Phase 5: Register agent on-chain (ERC-8004, Polygon mainnet)
node cli/polygon-agent.mjs agent register --name "MyAgent" --broadcast
# → mints ERC-721 NFT, emits agentId in Registered event
# → use agentId for reputation queries and feedback
```  

## 命令参考  

### 设置  
```bash
polygon-agent setup --name <name> [--force]
```  

### 钱包操作  
```bash
polygon-agent wallet create [--name <n>] [--chain polygon] [--timeout <sec>] [--no-wait]
  [--native-limit <amt>] [--usdc-limit <amt>] [--usdt-limit <amt>]
  [--token-limit <SYM:amt>]  # repeatable
  [--usdc-to <addr> --usdc-amount <amt>]  # one-off scoped transfer
  [--contract <addr>]  # whitelist contract (repeatable)
polygon-agent wallet import --ciphertext '<blob>|@<file>' [--name <n>] [--rid <rid>]
polygon-agent wallet list
polygon-agent wallet address [--name <n>]
polygon-agent wallet remove [--name <n>]
```  

### 代理操作（ERC-8004）  
```bash
polygon-agent balances [--wallet <n>] [--chain <chain>]
polygon-agent send --to <addr> --amount <num> [--symbol <SYM>] [--broadcast]
polygon-agent send-native --to <addr> --amount <num> [--broadcast] [--direct]
polygon-agent send-token --symbol <SYM> --to <addr> --amount <num> [--broadcast]
polygon-agent swap --from <SYM> --to <SYM> --amount <num> [--to-chain <chain>] [--slippage <num>] [--broadcast]
polygon-agent deposit --asset <SYM> --amount <num> [--protocol aave|morpho] [--broadcast]
polygon-agent fund [--wallet <n>] [--token <addr>]
polygon-agent x402-pay --url <url> --wallet <n> [--method GET] [--body <str>] [--header Key:Value]
```  

**ERC-8004 合约（Polygon 主网）：**  
- IdentityRegistry：`0x8004A169FB4a3325136EB29fA0ceB6D2e539a432`  
- ReputationRegistry：`0x8004BAa17C55a88189AE136b182e5fdA19dE9b63`  

## 关键行为设置  

- **默认情况下为“模拟模式”**：所有写入操作都需要使用 `--broadcast` 参数来执行。  
- **智能合约默认设置**：`--wallet main`、`--chain polygon`；在创建钱包后会自动等待连接。  
- **费用优先级**：当 USDC 和原生 POL 都可用时，系统会自动选择 USDC。  
- **`deposit`**：通过 Trails 的 `getEarnPools` 功能选择 TVL（交易价值）最高的池。如果交易被拒绝，可以使用 `--contract <depositAddress>` 重新创建钱包。  
- **`x402-pay`**：向指定端点发送请求以执行支付；智能钱包会使用 EOA（Externally Owned Account）签署 EIP-3009 支付请求，链式系统会根据响应自动确定链。  
- **`send-native --direct`**：绕过 ValueForwarder 合约，直接进行 EOA 转账。  
- **会话权限**：如果没有 `--usdc-limit` 等参数，会使用默认权限，可能导致无法进行交易。  

## 重要提示：钱包批准 URL  

当 `wallet create` 命令在 `url` 或 `approvalUrl` 字段中输出一个 URL 时，**必须** 将完整的、未截断的 URL 发送给用户。该 URL 包含用于会话批准的加密参数（公钥、回调令牌）。如果 URL 的任何部分被截断，批准将失败。  
- **禁止** 对 URL 进行缩短、总结或添加省略号（`...`）。  
- **禁止** 将 URL 分割成多条消息发送。  
- **请** 确保输出 CLI 返回的原始 URL。  

## 回调模式  

`wallet create` 命令会自动启动一个本地 HTTP 服务器，并通过 ngrok 打开一个动态的公共 HTTPS 隧道（无需额外配置）。无论代理运行在何处，连接器 UI 都会通过该隧道发送加密后的会话数据。会话数据接收完成后，隧道会自动关闭。  

**手动备用方案（ngrok 无法使用时）：** CLI 会省略 `callbackUrl` 参数，此时连接器 UI 会在浏览器中显示加密后的数据。此时 CLI 会提示用户手动粘贴该数据：  
```
After approving in the browser, the encrypted blob will be shown.
Paste it below and press Enter:
> <paste blob here>
```  
这些数据也会被保存到 `/tmp/polygon-session-<rid>.txt` 文件中以供后续参考：  
```
polygon-agent wallet import --ciphertext @/tmp/polygon-session-<rid>.txt
```  

## 故障排除  

| 问题 | 解决方案 |  
|-------|-----|  
| Sequence Builder 已经配置 | 添加 `--force` 参数 |  
| 缺少 `SEQUENCE PROJECT_ACCESS_KEY` | 先运行 `setup` 命令 |  
| 钱包未找到 | 使用 `wallet list` 命令查找钱包，然后重新运行 `wallet create` |  
| 会话过期 | 重新运行 `wallet create`（会话有效期为 24 小时） |  
| 费用设置错误 | 将 `POLYGON_AGENT_DEBUG_FEE` 设置为 1，并确保钱包中有足够的资金 |  
| 等待回调超时 | 添加 `--timeout 600` 参数 |  
| 回调模式设置为手动（无隧道）**：** 在提示时从浏览器中粘贴加密数据；数据保存到 `/tmp/polygon-session-<rid>.txt` 文件中 |  
| 存款请求被拒绝 | 使用 `--contract <depositAddress>` 重新创建钱包 |  

## 文件结构  
```
~/.polygon-agent/
├── .encryption-key       # AES-256-GCM key (auto-generated, 0600)
├── builder.json          # EOA privateKey (encrypted), eoaAddress, accessKey, projectId
├── wallets/<name>.json   # walletAddress, session, chainId, chain
└── requests/<rid>.json   # Pending wallet creation requests
```