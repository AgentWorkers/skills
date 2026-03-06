---
name: solana-wallet
description: 管理 Solana 和 Polygon 钱包，执行 Polymarket 的天气套利交易，发布信息到 X（Twitter）平台，并执行 Raydium 的交易操作——所有这些都可以通过自然语言指令来完成。
version: 1.1.2
homepage: https://github.com/inspi-writer001/raphael-solana
user-invocable: true
metadata:
  openclaw:
    emoji: "🤖"
    primaryEnv: MASTER_ENCRYPTION_PASSWORD_CRYPTO
    requires:
      env:
        - MASTER_ENCRYPTION_PASSWORD_CRYPTO
        - MASTER_ENCRYPTED
        - MASTER_SALT
        - SOLANA_RPC_URL
        - X_API_KEY
        - X_API_SECRET
        - X_ACCESS_TOKEN
        - X_ACCESS_TOKEN_SECRET
        - X_BEARER_TOKEN
      anyBins:
        - node
        - tsx
    install:
      node:
        - "."
    os:
      - macos
      - linux
---
# Solana + Polymarket + X Wallet Agent Skill

**源代码：** https://github.com/inspi-writer001/raphael-solana  
所有由该技能执行的代码都存储在该公共仓库中。在提供凭据或启用实时交易之前，请先查看代码。

您可以通过自然语言控制Solana钱包、Polygon EVM钱包、Polymarket天气套利扫描器以及X/Twitter策略。

## 设置  
该技能是自包含的。执行 `clawhub install solana-wallet` 后，源代码和依赖项会自动安装——无需手动克隆仓库。  
将您的凭据添加到 `~/.openclaw/.env` 文件中（详见下方的**环境变量**部分）。

## 执行规则  
1. **此技能附带了命令行界面（CLI）。命令前缀为：**  
   ```
   node --experimental-transform-types {baseDir}/bin/solana-wallet.ts
   ```  
   `{baseDir}` 由 OpenClaw 解析为该技能的安装目录。  
2. CLI 仅读取下方**环境变量**部分中列出的环境变量，不会读取其他变量。  
3. **优先使用插件工具（如果可用）——所有13个工具都可以作为直接插件调用使用，无需执行命令。**  
4. 以下 Node.js 警告是正常的且无害的：`ExperimentalWarning`、`bigint` 的弃用、`punycode`。在解析输出时可以忽略它们。  

## 插件工具（优先使用这些工具——无需执行命令）  
这13个工具由 [`src/plugin.ts`](https://github.com/inspi-writer001/raphael-solana/blob/main/src/plugin.ts) 注册，并包含在该技能包的 `{baseDir}/src/plugin.ts` 文件中。当技能被激活时，OpenClaw 会自动加载这些工具。  

### 钱包与 Polymarket  
| 工具 | 使用场景 |  
|---|---|  
| `create_evm_wallet` | 用户希望为 Polymarket 创建一个钱包 |  
| `list_evm_wallets` | 用户查询现有的 EVM 钱包 |  
| `check_usdc_balance` | 用户检查 USDC 是否已转入 Polygon |  
| `start_weather_arb` | 用户启动天气套利扫描器 |  
| `stop_weather_arb` | 用户停止天气套利扫描器 |  
| `get_strategy_status` | 用户查询扫描器状态、城市数据、交易信息及 X/Twitter 消息数量 |  

### X / Twitter  
| 工具 | 使用场景 |  
|---|---|  
| `x_post_tweet` | 用户发布推文 |  
| `x_reply` | 用户回复特定推文 |  
| `x_search` | 用户搜索最新推文（需 Basic+ 级别） |  
| `x_getmentions` | 用户查看机器人的最新被提及情况 |  
| `xResolve_user` | 用户通过 @handle 查找 Twitter 用户 |  
| `start_x_strategy` | 用户启动提及监控、关键词推送或交易发布 |  
| `stop_x_strategy` | 用户停止 X 战略 |  

## CLI 命令参考  
以下所有命令的前缀均为：  
```
node --experimental-transform-types {baseDir}/bin/solana-wallet.ts
```  

### Solana 钱包命令  
| 用户指令 | 命令 |  
|---|---|  
| 查看 Solana 余额 | `<prefix> balance <wallet-name>` |  
| 创建 Solana 钱包 | `<prefix> wallet create <name> [--network devnet\|mainnet-beta]` |  
| 列出 Solana 钱包 | `<prefix> wallet list` |  
| 转移 SOL 代币 | `<prefix> transfer sol <wallet> <to-address> <amount>` |  
| 转移 SPL 代币 | `<prefix> transfer spl <wallet> <to-address> <mint> <amount>` |  
| 转移 MATIC 代币 | `<prefix> transfer matic <wallet> <to-address> <amount>` |  
| 转移 ERC-20 代币（如 USDC） | `<prefix> transfer erc20 <wallet> <to-address> <token-address> <amount>` |  
| 交换代币 | `<prefix> swap <wallet> SOL <output-mint> <amount>` |  
| 查找交易机会 | `<prefix> find-pairs` |  

### EVM / Polygon 钱包命令  
| 用户指令 | 命令 |  
|---|---|  
| 创建 Polygon 钱包 | `<prefix> evm-wallet create <name>` |  
| 列出 Polygon 钱包 | `<prefix> evm-wallet list` |  
| 查看 MATIC/ERC-20 余额 | `<prefix> evm-wallet balance <name> [--token <address>]` |  

### X / Twitter 命令  
| 用户指令 | 命令 |  
|---|---|  
| 发布推文 | `<prefix> x tweet <text>` |  
| 回复推文 | `<prefix> x reply <tweet-id> <text>` |  
| 搜索推文 | `<prefix> x search <query> [--max 10]` |  
| 查看被提及情况 | `<prefix> x mentions [--since <tweet-id>]` |  
| 查找用户 | `<prefix> x resolve <handle>` |  
| 启动 X 战略 | （完整命令见下方） |  

**启动 X 战略（完整命令）：**  
```
node --experimental-transform-types {baseDir}/bin/solana-wallet.ts scanner start x \
  --handle <bot-handle> \
  [--keywords "pump.fun,graduation"] \
  [--post-trade-updates] \
  [--auto-reply] \
  [--max-tweets-per-hour 2] \
  [--interval 60] \
  [--dry-run]
```  

### 扫描器命令  
| 用户指令 | 命令 |  
|---|---|  
| 启动天气套利 | （完整命令见下方） |  
| 停止扫描器 | `node --experimental-transform-types {baseDir}/bin/solana-wallet.ts scanner stop` |  
| 查看扫描器状态 | `node --experimental-transform-types {baseDir}/bin/solana-wallet.ts scanner status` |  

**启动天气套利（完整命令）：**  
```
node --experimental-transform-types {baseDir}/bin/solana-wallet.ts scanner start polymarket-weather <evm-wallet-name> \
  --amount <usdc-per-trade> \
  [--cities nyc,london,seoul,chicago,dallas,miami,paris,toronto,seattle] \
  [--max-position <usdc>] \
  [--min-edge 0.20] \
  [--min-fair-value 0.40] \
  [--interval <seconds>] \
  [--dry-run]
```  

## 典型代理流程：Polymarket 天气套利  
1. 创建 EVM 钱包（使用插件：`create_evm_wallet` 或 CLI：`evm-wallet create polymarket1`）  
2. 告诉用户：“将 USDC（Polygon PoS 网络）发送到：<address>`  
3. 检查余额直至资金到账：`check_usdc_balance { wallet_name: "polymarket1" }`  
4. 启动模拟运行：`start_weather_arb { wallet_name: "polymarket1", trade_amount_usdc: 5, dry_run: true }`  
5. 2 分钟后检查结果：`get_strategy_status`  
6. 如果结果合理，停止模拟运行并重新启动：`start_weather_arb { ..., dry_run: false }`  

## 典型代理流程：X / Twitter  
1. 确认已设置 X 服务凭据：`X_API_KEY`、`X_API_SECRET`、`X_ACCESS_TOKEN`、`X_ACCESS_TOKEN_SECRET`、`X_BEARER_TOKEN`  
2. 启动模拟运行以进行验证：`start_x_strategy { handle: "mybot", dry_run: true, post-trade_updates: true }`  
3. 查看状态：`get_strategy_status`（显示当前小时发送的推文）  
4. 确认正常运行后，停止模拟运行并开始正式运行  

## 支持的天气套利城市  
| 关键字 | 城市 |  
|---|---|  
| `nyc` | 纽约市 |  
| `london` | 伦敦 |  
| `seoul` | 首尔 |  
| `chicago` | 芝加哥 |  
| `dallas` | 达拉斯 |  
| `miami` | 迈阿密 |  
| `paris` | 巴黎 |  
| `toronto` | 多伦多 |  
| `seattle` | 西雅图 |  

## 环境变量  
以下是该技能读取的所有环境变量的完整列表。它不会读取其他变量。  

### 必需的环境变量  
| 变量 | 说明 | 用途 |  
|---|---|---|  
| `MASTER_ENCRYPTION_PASSWORD_crypto` | 您选择的密码——仅存储在内存中，不会写入磁盘 | 用于钱包解密 |  
| `MASTER_ENCRYPTED` | AES-256-GCM 加密的主密钥（由 `pnpm setup` 生成） | 用于钱包解密 |  
| `MASTER_SALT` | PBKDF2 密钥派生盐（由 `pnpm setup` 生成） | 用于钱包解密 |  

### 可选的环境变量  
| 变量 | 默认值 | 说明 | 用途 |  
|---|---|---|---|  
| `SOLANA_RPC_URL` | `https://api.devnet.solana.com` | Solana JSON-RPC 端点 | 用于查询余额、转账、交换操作 |  
| `RAPHAEL_DATA_DIR` | `~/.raphael` | 存储加密钱包文件和扫描器状态的目录 | 用于存储钱包数据 |  
| `WALLET_STORE_PATH` | `$RAPHAEL_DATA_DIR/wallets.json` | Solana 钱包 JSON 文件的路径 | 用于存储钱包数据 |  
| `PUMPPORTAL_WS` | `wss://pumpportal.fun/api/data` | pump.fun 的 WebSocket 服务器（无需密钥） | 用于连接 pump.fun 扫描器 |  
| `X_API_KEY` | — | OAuth 1.0a 消费者密钥 | 用于 X 服务（发布推文、回复） |  
| `X_API_SECRET` | — | OAuth 1.0a 消费者密钥 | 用于 X 服务 |  
| `X_ACCESS_TOKEN` | — | OAuth 1.0a 用户访问令牌 | 用于 X 服务 |  
| `X_ACCESS_TOKEN_SECRET` | — | OAuth 1.0a 用户访问令牌密钥 | 用于 X 服务 |  
| `X_BEARER_TOKEN` | — | OAuth 2.0 仅限应用使用的令牌 | 用于 X 服务（搜索、时间线功能） |  

X 相关功能是可选的——即使没有这些变量，该技能也能正常运行。您可以从 [developer.x.com](https://developer.x.com) 的“项目与应用”→“密钥和令牌”部分获取所需的权限。  

### 钱包加密模型  
私钥从不以明文形式存储。该技能在您的本地机器上使用双层 AES-256-GCM 加密技术进行加密——不会将任何密钥或钱包数据发送到远程服务器。  

```
MASTER_ENCRYPTION_PASSWORD_CRYPTO  (your password, memory only)
  ↓ PBKDF2 — 100,000 iterations, SHA-256
MASTER_ENCRYPTED + MASTER_SALT     (encrypted blob — useless without the password)
  ↓ AES-256-GCM decrypt → master key
wallet private key                 (AES-256-GCM, per-wallet salt → ~/.raphael/)
```  

`MASTER_ENCRYPTED` 和 `MASTER_SALT` 是 `pnpm setup` 的输出结果，它们与您的密码和机器配置相关。未经授权共享这些信息会导致安全风险。  

**规则：**  
- 在进行实时交易前务必确认（除非用户明确表示“直接执行”或“无需模拟运行”）  
- 首次使用扫描器或 X 战略时，建议使用 `--dry-run` 或 `dry_run: true`  
- 在完成 Solana 交易后，提供 Solana Explorer 的 URL  
- 绝不显示私钥  
- 对于 Polymarket：必须使用 **Polygon PoS 网络**（而非 Solana 或 Ethereum 主网）  
- 对于 X 服务：禁止自动点赞或自动转发推文（违反服务条款）；该代理仅负责读取和发布文本信息  
- 对于 devnet Solana 资金转账：建议使用 `solana airdrop 2 <address> --url devnet`  
- X 搜索功能需要 Basic+ 级别（每月费用 $100）；若该功能不可用，请优雅地跳过。