---
name: agent-wallet
description: 通过 `agent-wallet-cli` 管理加密钱包（Ethereum、Solana、Polygon、Arbitrum、Base）。该工具可用于查询余额、发送代币（ETH/SOL/ERC-20/SPL）、签署交易消息、管理交易批准、查看交易历史、处理 X402 支付以及执行钱包生命周期操作（初始化、解锁、锁定、导出）。支持 HD 钱包（BIP-39 标准）、用于临时访问的会话令牌，以及支持 JSON 格式的数据输出以便自动化处理。该项目为开源项目：https://github.com/donald-jackson/agent-wallet-cli
metadata: {"openclaw":{"requires":{"bins":["agent-wallet-cli"],"env":["WALLET_PASSWORD (sensitive, optional): Wallet encryption password — passed via --password or piped via stdin. Only needed for init/import/unlock/export.","WALLET_SESSION_TOKEN (sensitive, optional): Time-limited session token (wlt_...) from unlock. Used for all operations via --token."]},"install":[{"id":"agent-wallet-cli","kind":"node","package":"agent-wallet-cli","bins":["agent-wallet-cli"],"label":"Install agent-wallet-cli (npm)"}],"source":{"repository":"https://github.com/donald-jackson/agent-wallet-cli","license":"MIT"}}}
---
# 代理钱包（Agent Wallet）

这是一个专为AI代理设计的自托管加密货币钱包命令行工具。你的私钥和资产完全由你控制——在初始化完成后，代理程序永远不会看到你的助记词。

- **开源项目**：[github.com/donald-jackson/agent-wallet-cli](https://github.com/donald-jackson/agent-wallet-cli) — 使用前请进行审计。
- **npm包**：[npmjs.com/package/agent-wallet-cli](https://www.npmjs.com/package/agent-wallet-cli)
- **自托管模式**：私钥采用Argon2id + AES-256-GCM算法进行本地加密，无需依赖服务器或第三方服务。
- **基于会话的访问机制**：代理程序使用有效期有限的会话令牌，从不直接使用你的密码。
- **支持多链**：支持Ethereum、Solana、Polygon、Arbitrum、Base等区块链，支持原生货币和代币。

## 安全模型

1. **你**创建或导入钱包时需要设置密码，该密码会被加密并存储在`~/.agent-wallet-cli/`目录下。
2. **你**（或代理程序）使用密码解锁钱包后，会获得一个有效期有限的会话令牌（格式为`wlt_...`）。
3. **代理程序**仅使用会话令牌进行操作，该令牌会自动过期（默认时长为1小时，最长24小时）。
4. **无数据传输、无分析日志、无服务器请求**——所有操作仅通过公共区块链的RPC接口完成。

**重要提示：**如果将钱包密码提供给代理程序，它将能够执行所有与密码相关的操作（如初始化、导入、解锁和导出钱包）。为确保安全，请**自行解锁钱包**，并将会话令牌提供给代理程序。会话令牌仅用于签署交易和查询余额。

**在将真实资金委托给此工具之前，请务必：**
- 审查源代码：[github.com/donald-jackson/agent-wallet-cli](https://github.com/donald-jackson/agent-wallet-cli)
- 确认npm包与源代码仓库一致：`npm info agent-wallet-cli`
- 先用少量资金进行测试
- 将会话令牌的有效期设置为较短时间（默认1小时）
- 尽可能在隔离环境中使用该工具。

## 安装与配置

```bash
npm install -g agent-wallet-cli
```

验证安装结果：`agent-wallet-cli --version`

## 使用流程

1. **首次使用**：`agent-wallet-cli init --password "$WALLET_PASSWORD"`  
   - 会显示一次助记词，请妥善保存。
2. **导入现有钱包**：`agent-wallet-cli import --password "$WALLET_PASSWORD" --mnemonic "word1 word2 ..."`
3. **解锁钱包**：`agent-wallet-cli unlock --password "$WALLET_PASSWORD" --duration 3600`  
   - 会返回一个有效期为3600秒的会话令牌（格式为`wlt_...`）。
4. **使用钱包**：在所有命令后添加`--token wlt_...`参数（无需输入密码）。
5. **锁定钱包**：`agent-wallet-cli lock`  

**注意：**`--password`和`--mnemonic`参数可以省略，系统会通过标准输入（stdin）安全地提示你输入这些信息（推荐用于交互式使用）。在自动化环境中使用时，虽然可以省略`--password`，但系统会提示有关shell历史记录可能被记录的警告。

## 全局配置选项

所有命令均支持以下选项：
- `--format json|text`（默认：json）
- `--wallet-dir <path>`（默认：`~/.agent-wallet-cli`）
- `--quiet`（默认：不显示输出）
- `--name <name>`（默认：`default`）

## 命令列表

### 钱包管理
```bash
agent-wallet-cli init [--password <pw>] [--word-count 12|24] [--name <name>]
agent-wallet-cli import [--password <pw>] [--mnemonic "<phrase>"] [--name <name>]
agent-wallet-cli unlock [--password <pw>] [--duration <secs>] [--name <name>]
agent-wallet-cli lock [--name <name>]
agent-wallet-cli export [--password <pw>] --confirm [--name <name>]
```

### 地址与余额查询
```bash
agent-wallet-cli address --token <wlt_...> [--chain ethereum|solana] [--account-index 0]
agent-wallet-cli balance --token <wlt_...> --chain <chain> [--network <network>] [--token-address usdc]
```

**重要提示：**执行`--chain`选项时必须指定区块链名称。`--token`参数用于指定会话令牌，`--token-address`用于指定代币或合约的地址。**

**L2网络**：对于Base、Polygon、Arbitrum等网络，需使用`--chain ethereum --network base`（示例）。默认网络为`mainnet`。

### 转账操作
```bash
# Native (ETH/SOL)
agent-wallet-cli send --token <wlt_...> --chain <chain> --to <addr> --amount <amt> --yes [--dry-run] [--no-relay]
# ERC-20/SPL token
agent-wallet-cli send --token <wlt_...> --chain <chain> --to <addr> --amount <amt> --token-address <addr|alias> --yes [--no-relay]
```

- `--yes`：跳过确认提示（非交互式使用时必须使用此选项）。
- `--dry-run`：模拟转账操作而不实际发送交易。
- `--no-relay`：禁用无gas费用的转账机制。
- `--network <network>`：指定目标网络（默认：mainnet）。

### x402支付功能
```bash
agent-wallet-cli x402 <url> --token <wlt_...> [--method GET] [--header "Key:Value"] [--body <data|@file>] [--max-amount <amt>] [--dry-run] [--yes]
```

该工具支持自动处理HTTP请求中的402 Payment Required响应，会用稳定币支付指定金额并重试请求。

- `--max-amount <amount>`：指定最大支付金额（以人类可读格式输入，例如“0.10”）。
- `--dry-run`：仅显示支付要求信息而不执行支付。
- `--yes`：跳过支付确认步骤。
- `--header`：可多次重复使用该选项以设置请求头信息。
- `--body`：指定请求体内容，或使用`@filepath`从文件中读取请求体。

### 批准操作（ERC-20/SPL标准）
```bash
agent-wallet-cli approve --token <wlt_...> --chain <chain> --token-address <addr> --spender <addr> --amount <amt|unlimited> --yes [--network <net>]
agent-wallet-cli allowance --chain <chain> --token-address <addr> --owner <addr> --spender <addr> [--network <net>]
agent-wallet-cli transfer-from --token <wlt_...> --chain <chain> --token-address <addr> --from <addr> --to <addr> --amount <amt> --yes [--network <net>]
agent-wallet-cli approvals --token <wlt_...> [--chain ethereum] [--network mainnet] [--limit 20]
```

### 签名操作
```bash
agent-wallet-cli sign --token <wlt_...> --chain <chain> --message "text"
agent-wallet-cli sign --token <wlt_...> --chain <chain> --typed-data '<json|@file>'
agent-wallet-cli sign --token <wlt_...> --chain <chain> --data <hex>
```

### 交易历史查询
```bash
agent-wallet-cli history --token <wlt_...> --chain <chain> [--network mainnet] [--limit 10]
```

### 网络配置
```bash
agent-wallet-cli networks                                          # list all
agent-wallet-cli networks --set ethereum:mainnet --rpc-url <url>   # custom RPC
agent-wallet-cli networks --reset ethereum:mainnet                 # reset to default
```

## 支持的区块链与网络

| 区块链 | 可用网络 |
|-------|----------|
| Ethereum | mainnet, sepolia, polygon, arbitrum, base, base-sepolia |
| Solana | mainnet, devnet |

EVM L2网络（Base、Polygon、Arbitrum）需使用`--chain ethereum --network <l2name>`。

**执行`--chain`选项**是进行余额查询、转账、发送交易、批准交易、请求权限、执行转账操作等操作的必要条件。

## 代币别名

可以使用简称代替合约地址，例如：`usdc`、`usdt`、`dai`、`weth`、`wbtc`。

## 安全注意事项：

- **完全自托管**：私钥始终存储在你的设备上，加密后不会离开本地。
- 无数据分析功能，无网络请求（除非是用于区块链查询的公共RPC调用）。
- 会话令牌仅提供临时访问权限，请将其视为临时密码。
- 在进行大额转账前务必先执行`--dry-run`测试。
- 使用完钱包后请立即锁定钱包。
- 绝不要记录或分享会话令牌或助记词。
- 请务必审查源代码：[github.com/donald-jackson/agent-wallet-cli](https://github.com/donald-jackson/agent-wallet-cli)