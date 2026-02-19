---
name: agent-wallet
description: 通过 `agent-wallet-cli` 管理加密钱包（Ethereum、Solana、Polygon、Arbitrum、Base）。支持查看余额、发送代币（ETH/SOL/ERC-20/SPL）、签署交易消息、管理交易批准、查看交易历史记录、执行 x402 支付以及执行钱包生命周期操作（初始化、解锁、锁定、导出）。该工具支持硬件钱包（BIP-39 标准），并提供会话令牌以实现限时访问功能，同时支持 JSON 格式输出以便自动化使用。开源项目：https://github.com/donald-jackson/agent-wallet-cli
metadata: {"openclaw":{"requires":{"bins":["agent-wallet-cli"],"env":["WALLET_PASSWORD (sensitive, optional): Wallet encryption password — passed via --password or piped via stdin. Only needed for init/import/unlock/export.","WALLET_SESSION_TOKEN (sensitive, optional): Time-limited session token (wlt_...) from unlock. Used for all operations via --token."]},"install":[{"id":"agent-wallet-cli","kind":"node","package":"agent-wallet-cli","bins":["agent-wallet-cli"],"label":"Install agent-wallet-cli (npm)"}],"source":{"repository":"https://github.com/donald-jackson/agent-wallet-cli","license":"MIT"}}}
---
# 代理钱包（Agent Wallet）

这是一个专为AI代理设计的自托管加密货币钱包命令行工具。你的私钥和资产完全由你控制——代理在初始化后永远不会看到你的助记词。

- **开源项目**：[github.com/donald-jackson/agent-wallet-cli](https://github.com/donald-jackson/agent-wallet-cli) — 使用前请进行审计。
- **npm包**：[npmjs.com/package/agent-wallet-cli](https://www.npmjs.com/package/agent-wallet-cli)
- **自托管模式**：私钥采用Argon2id + AES-256-GCM算法进行本地加密，无需依赖服务器或第三方服务。
- **基于会话的访问机制**：代理使用限时会话令牌进行操作，从不直接使用你的密码。
- **支持多链**：支持Ethereum、Solana、Polygon、Arbitrum、Base等区块链，支持原生货币和代币。

## 安全模型

1. 你创建或导入钱包时需要设置密码，该密码会以加密形式存储在`~/.agent-wallet-cli/`目录中。
2. 你（或代理）使用密码解锁钱包后，会获得一个限时会话令牌（格式为`wlt_...`）。
3. 代理仅使用该会话令牌进行操作，令牌会自动过期（默认1小时，最长24小时）。
4. 该工具不收集任何用户数据、不进行数据分析，也不发送任何网络请求——所有操作仅通过公共区块链的RPC接口完成。

**重要提示：** 如果你将钱包密码提供给代理，代理将能够执行所有与密码相关的操作（如初始化、导入、解锁、导出等）。为确保最高安全性，请自行解锁钱包，并仅向代理提供会话令牌。会话令牌仅用于签名交易和查询余额，无法用于修改密码或导出助记词。

**在使用该工具处理真实资金之前，请务必：**
- 审查源代码：[github.com/donald-jackson/agent-wallet-cli](https://github.com/donald-jackson/agent-wallet-cli)
- 确认安装的npm包与源代码库一致：`npm info agent-wallet-cli`
- 先使用少量资金进行测试
- 将会话令牌的有效时间设置为较短（默认1小时）
- 如可能，请在隔离环境中运行该工具。

## 安装与配置

```bash
npm install -g agent-wallet-cli
```

验证安装结果：`agent-wallet-cli --version`

## 使用流程

1. **初始化钱包（首次使用）**：`agent-wallet-cli init --password "$WALLET_PASSWORD"`
   - 会显示一次助记词，请务必安全地保存它。
2. **导入现有钱包**：`agent-wallet-cli import --password "$WALLET_PASSWORD" --mnemonic "word1 word2 ..."`
3. **解锁钱包**：`agent-wallet-cli unlock --password "$WALLET_PASSWORD" --duration 3600`
   - 会返回一个有效期为3600秒的会话令牌（格式为`wlt_...`）。
4. **使用钱包**：在所有命令后添加`--token wlt_...`参数（无需输入密码）。
5. **锁定钱包**：使用`agent-wallet-cli lock`命令完成操作。

**注意：** 可以省略`--password`和`--mnemonic`参数，系统会通过标准输入安全地提示用户输入相关信息（推荐用于交互式使用）。在自动化环境中使用时，虽然可以省略`--password`参数，但系统会提示相关安全风险。

## 全局配置选项

所有命令都支持以下选项：
- `--format json|text`（默认：json）
- `--wallet-dir <path>`（默认：`~/.agent-wallet-cli`）
- `--quiet`：抑制输出信息
- `--name <name>`：钱包名称（默认：“default”）

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
agent-wallet-cli balance --token <wlt_...> --chain <chain> [--network mainnet] [--token-address usdc]
```

**重要提示：** `--token`参数用于指定会话令牌（格式为`wlt_...`），`--token-address`参数用于指定代币/合约的地址或别名。

### 转账
```bash
# Native (ETH/SOL)
agent-wallet-cli send --token <wlt_...> --chain <chain> --to <addr> --amount <amt> --yes [--dry-run] [--no-relay]
# ERC-20/SPL token
agent-wallet-cli send --token <wlt_...> --chain <chain> --to <addr> --amount <amt> --token-address <addr|alias> --yes [--no-relay]
```

- `--yes`：跳过确认提示（非交互式使用时必需）
- `--dry-run`：模拟转账操作但不实际发送交易
- `--no-relay`：禁用无Gas费用的转账机制
- `--network <network>`：指定目标区块链网络（默认：mainnet）

### x402支付功能
```bash
agent-wallet-cli x402 <url> --token <wlt_...> [--method GET] [--header "Key:Value"] [--body <data|@file>] [--max-amount <amt>] [--dry-run] [--yes]
```

该工具支持自动处理HTTP请求中的402 Payment Required响应，会使用稳定币支付指定金额并重试请求。
- `--max-amount <amount>`：指定最大支付金额（以人类可读格式输入，例如“0.10”）
- `--dry-run`：仅显示支付要求而不实际支付
- `--yes`：跳过支付确认
- `--header`：可重复使用多个请求头
- `--body`：指定请求体内容，或使用`@filepath`从文件中读取请求体

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

EVM Layer-2网络（Base、Polygon、Arbitrum）的完整路径为`--chain ethereum --network <l2name>`。

## 代币别名

可以使用缩写形式代替合约地址，例如：`usdc`、`usdt`、`dai`、`weth`、`wbtc`。

## 安全注意事项：

- **完全自托管**：私钥始终存储在你的设备上，加密后不会离开本地。
- 该工具不收集用户数据、不发送任何网络请求（除非是用于区块链查询的公共RPC接口）。
- 会话令牌仅提供临时访问权限，应将其视为临时密码。
- 在进行大额转账前务必使用`--dry-run`功能进行测试。
- 操作完成后请锁定钱包。
- 绝不要记录或分享会话令牌或助记词。
- 请务必审查源代码：[github.com/donald-jackson/agent-wallet-cli](https://github.com/donald-jackson/agent-wallet-cli)