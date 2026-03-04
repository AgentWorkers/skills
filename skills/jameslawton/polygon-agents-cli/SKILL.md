---
name: polygon-agent-cli
description: 完整的Polygon代理工具包：基于会话的智能合约钱包（Sequence）、代币操作（通过Trails发送/交换/桥接/存入）、支持ERC-8004标准的链上身份验证与信誉系统、支持x402微支付功能。提供统一的命令行接口（CLI）进行操作，数据存储采用AES-256-GCM加密技术。
---
# Polygon Agent Kit

## 先决条件

- Node.js 22+  
- 全局安装：`npm install -g @polygonlabs/agent-cli`  
- 使用方式：`polygon-agent <command>`  
- 存储路径：`~/.polygon-agent/`（采用 AES-256-GCM 加密）

## 架构  

| 钱包类型          | 创建工具        | 用途                                      | 是否需要资金？ |
| ---------------- | --------------- | ----------------------------------------- | -------- |
| EOA（Externally Owned Account） | `setup`      | 使用 Sequence Builder 进行身份验证       | 否       |
| 生态系统钱包       | `wallet create`   | 主要的支出钱包                     | 是       |

## 环境变量  

### 必需的环境变量  

| 变量                        | 用途                                      | 设置时机                                      |
| ----------------------------- | ------------------------------------------- | -------------------------------------- |
| `SEQUENCE_PROJECT_ACCESS_KEY` | 钱包创建、交易、余额查询、Trails 操作         |                         |

**一个密钥，三个名称**：`SEQUENCE_INDEXER_ACCESS_KEY`、`TRAILS_API_KEY` 和 `SEQUENCE PROJECT_ACCESS_KEY` 的值是相同的。请一次性设置这三个密钥：  

```bash
export SEQUENCE_PROJECT_ACCESS_KEY=<access-key-from-setup>
export SEQUENCE_INDEXER_ACCESS_KEY=$SEQUENCE_PROJECT_ACCESS_KEY
export TRAILS_API_KEY=$SEQUENCE_PROJECT_ACCESS_KEY
```

### 可选的环境变量  

| 变量                           | 默认值                                      |                                           |
| ---------------------------------- | ----------------------------------------------------- |
| `SEQUENCE_ECOSYSTEM_CONNECTOR_URL` | `https://agentconnect.polygon.technology/`            |                                           |
| `SEQUENCE_DAPP_origin`             | 与连接器 URL 的来源地址相同                         |                                           |
| `TRAILS_TOKEN_MAP_JSON`            | 用于查询令牌信息的 JSON 文件路径                         |                                           |
| `POLYGON_AGENT_DEBUG FETCH`        | 关闭时将日志输出到 `~/.polygon-agent/fetch-debug.log`     |                                           |
| `POLYGON_AGENT_DEBUG_FEE`          | 关闭时将费用信息输出到标准错误流                         |                                           |

## 完整的设置流程  

```bash
# Phase 1: Setup (creates EOA + Sequence project, returns access key)
polygon-agent setup --name "MyAgent"
# → save privateKey (not shown again), eoaAddress, accessKey

# Phase 2: Create ecosystem wallet (auto-waits for browser approval)
export SEQUENCE_PROJECT_ACCESS_KEY=<accessKey>
polygon-agent wallet create --usdc-limit 100 --native-limit 5

# Phase 3: Fund wallet
polygon-agent fund
# → reads walletAddress from session, builds Trails widget URL with toAddress=<walletAddress>
# → ALWAYS run this command to get the URL — never construct it manually or hardcode any address
# → send the returned `fundingUrl` to the user; `walletAddress` in the output confirms the recipient

# Phase 4: Verify (SEQUENCE_INDEXER_ACCESS_KEY is the same as your project access key)
export SEQUENCE_INDEXER_ACCESS_KEY=$SEQUENCE_PROJECT_ACCESS_KEY
polygon-agent balances

# Phase 5: Register agent on-chain (ERC-8004, Polygon mainnet)
polygon-agent agent register --name "MyAgent" --broadcast
# → mints ERC-721 NFT, emits agentId in Registered event
# → use agentId for reputation queries and feedback
```

## 命令参考  

### 设置钱包  

```bash
polygon-agent setup --name <name> [--force]
```

### 操作相关命令  

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

### 代理（ERC-8004）  

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

### ERC-8004 合约（Polygon 主网）  

- IdentityRegistry：`0x8004A169FB4a3325136EB29fA0ceB6D2e539a432`  
- ReputationRegistry：`0x8004BAa17C55a88189AE136b182e5fdA19dE9b63`  

## 关键行为说明  

- **默认为“Dry-run”模式**：所有写入操作都需要使用 `--broadcast` 参数才能执行。  
- **智能默认设置**：`--wallet main`、`--chain polygon`；在创建钱包后会自动等待连接完成。  
- **费用优先级**：当 USDC 和原生 POL 都可用时，系统会自动选择 USDC。  
- **`fund` 命令**：从钱包会话中读取 `walletAddress` 并将其设置为 Trails 界面中的 `toAddress`。务必执行 `polygon-agent fund` 命令以获取正确的 URL，切勿手动构造或硬编码地址。返回的 JSON 包含 `fundingUrl` 和 `walletAddress`，以便在分享前确认收款人信息。  
- **`deposit` 命令**：通过 Trails 的 `getEarnPools` 功能选择 TVL（Total Value Locked）最高的池子进行存款；如果会话失败，可使用 `--contract <depositAddress>` 重新创建钱包。  
- **`x402-pay` 命令**：向指定的地址发送交易请求；智能钱包会自动使用 EOA（Externally Owned Account）权限进行交易，并根据 EIP-3009 协议签名交易。链路会自动从响应中检测出交易链。  
- **`send-native --direct` 命令**：绕过 ValueForwarder 合约，直接进行 EOA 转账。  
- **会话权限**：如果没有指定 `--usdc-limit` 等参数，会话将使用默认权限，可能导致交易失败。  

## 关键提示：钱包批准 URL  

当 `wallet create` 命令在 `url` 或 `approvalUrl` 字段中输出 URL 时，**必须** 将完整的、未截断的 URL 发送给用户。该 URL 包含用于会话批准的加密参数（公钥、回调令牌）。如果 URL 的任何部分被截断，批准操作将会失败：  
- **切勿** 缩短、总结 URL，也不要在多条消息中分批发送。  
- **请** 确保输出 CLI 返回的原始 URL。  

## 回调模式  

`wallet create` 命令会自动启动一个本地 HTTP 服务器，并打开一个 **Cloudflare Quick Tunnel**（地址：`*.trycloudflare.com`），无需账户或令牌即可使用。如果 `cloudflared` 二进制文件尚未安装，系统会在首次使用时自动将其下载到 `~/.polygon-agent/bin/cloudflared`。无论代理程序运行在何处，连接器 UI 都会通过该隧道发送加密后的会话数据。会话数据接收完成后，隧道和服务器会自动关闭。  

**注意**：`approvalUrl` 仅在 CLI 进程运行期间有效。请立即打开该链接并在超时窗口（默认 300 秒）内完成钱包批准操作。切勿重复使用之前的 URL，因为隧道会在 CLI 结束后关闭。  

**手动备用方案**（如果 cloudflared 无法使用）：CLI 会忽略 `callbackUrl` 参数，此时连接器 UI 会在浏览器中显示加密后的数据。此时 CLI 会提示用户手动操作：  

```text
After approving in the browser, the encrypted blob will be shown.
Paste it below and press Enter:
> <paste blob here>
```

加密后的数据还会被保存到 `/tmp/polygon-session-<rid>.txt` 文件中，以供后续参考。  

## 故障排除  

| 问题                                      | 解决方案                                                                                                      |
| ----------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| `Sequence Builder` 已经配置             | 使用 `--force` 参数进行强制操作                                                                                         |
| 缺少 `SEQUENCE_Project_ACCESS_KEY`         | 先运行 `setup` 命令                                                                                              |
| 未找到钱包                                   | 使用 `wallet list` 命令查看钱包列表，然后重新运行 `wallet create`                         |
| 会话过期                                   | 重新运行 `wallet create` 命令（会话有效期为 24 小时）                                                                                   |
| 费用设置错误                                 | 将 `POLYGON_AGENT_DEBUG_FEE` 设置为 1，并确保钱包中有足够的资金                                                                                   |
| 等待回调超时                                 | 添加 `--timeout 600` 参数                                                                                               |
| 回调模式设置为“manual”（无隧道支持）           | 如果 cloudflared 不可用，请从浏览器中复制加密数据并粘贴；数据会保存到 `/tmp/polygon-session-<rid>.txt` 文件中     |
| 访问 `*.trycloudflare.com` 时出现 404 错误         | CLI 过时导致隧道关闭，请重新运行 `wallet create` 命令，并立即打开新的 `approvalUrl`         |
| 浏览器中显示 “Auto-send failed” 错误             | 复制错误信息中显示的加密数据，然后运行 `wallet import --ciphertext '<blob>'` 命令         |
| 存款操作被拒绝                                 | 使用 `--contract <depositAddress>` 重新创建钱包                                                                                   |
| Trails 界面中的收款人地址错误                 | 执行 `polygon-agent fund` 命令（切勿手动构造 URL）；输出中的 `walletAddress` 即为预填充的收款人地址     |

## 文件结构  

```text
~/.polygon-agent/
├── .encryption-key       # AES-256-GCM key (auto-generated, 0600)
├── builder.json          # EOA privateKey (encrypted), eoaAddress, accessKey, projectId
├── wallets/<name>.json   # walletAddress, session, chainId, chain
└── requests/<rid>.json   # Pending wallet creation requests
```