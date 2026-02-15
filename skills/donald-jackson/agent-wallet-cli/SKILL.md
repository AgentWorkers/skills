---
name: agent-wallet
description: 通过 `agent-wallet-cli` 管理加密钱包（Ethereum、Solana、Polygon、Arbitrum、Base）。支持查看余额、发送代币（ETH/SOL/ERC-20/SPL）、签署交易消息、管理授权请求、查看交易历史以及执行钱包生命周期操作（初始化、解锁、锁定、导出）。该工具支持 HD 钱包（BIP-39 标准）、用于临时访问的会话令牌，以及可自动化的 JSON 输出格式。开源项目地址：https://github.com/donald-jackson/agent-wallet-cli
metadata: {"openclaw":{"requires":{"bins":["agent-wallet-cli"],"env":["WALLET_PASSWORD (sensitive, optional): Wallet encryption password — piped via stdin to unlock. Only needed for unlock/init/import.","WALLET_SESSION_TOKEN (sensitive, optional): Time-limited session token (wlt_...) from unlock. Used for all operations."]},"install":[{"id":"agent-wallet-cli","kind":"node","package":"agent-wallet-cli","bins":["agent-wallet-cli"],"label":"Install agent-wallet-cli (npm)"}],"source":{"repository":"https://github.com/donald-jackson/agent-wallet-cli","license":"MIT"}}}
---

# 代理钱包（Agent Wallet）

这是一个专为AI代理设计的自托管加密货币钱包命令行工具。你的密钥和资金完全由你控制——在初始化之后，代理程序永远不会看到你的助记词。

- **开源项目**：[github.com/donald-jackson/agent-wallet-cli](https://github.com/donald-jackson/agent-wallet-cli) — 使用前请进行审计。
- **npm包**：[npmjs.com/package/agent-wallet-cli](https://www.npmjs.com/package/agent-wallet-cli)
- **自托管模式**：密钥采用Argon2id和AES-256-GCM算法进行本地加密，无需依赖服务器或第三方服务。
- **基于会话的访问机制**：代理程序使用限时会话令牌进行操作，从不直接使用你的密码。
- **支持多链**：Ethereum、Solana、Polygon、Arbitrum、Base等区块链平台，支持原生代币和交易代币。

## 安全模型

1. 你创建或导入钱包时需要设置密码，该密码会以加密形式存储在`~/.agent-wallet-cli/`目录中。
2. 你（或代理程序）使用密码解锁钱包后，会获得一个限时会话令牌（格式为`wlt_...`）。
3. 代理程序仅使用会话令牌进行操作，该令牌会自动过期（默认有效期为1小时，最长24小时）。
4. 该工具不发送任何遥测数据、不进行数据分析，也不发起任何服务器请求——所有操作仅通过公共区块链的RPC接口完成。

**重要提示：** 如果你将钱包密码提供给代理程序，它将能够执行所有与密码相关的操作（如初始化、导入、解锁和导出钱包）。为确保安全，请**自行解锁钱包**，仅将会话令牌（`WALLET_SESSION_TOKEN`）提供给代理程序。会话令牌无法用于导出助记词或修改密码，仅可用于签名交易和查询余额。

密码通过标准输入（stdin）传递，绝不会作为命令行参数（CLI flags）传递。

**在将真实资金委托给该工具之前，请务必：**
- 审查源代码：[github.com/donald-jackson/agent-wallet-cli](https://github.com/donald-jackson/agent-wallet-cli)
- 确认npm包与源代码仓库一致：`npm info agent-wallet-cli`
- 先用少量资金进行测试
- 尽可能在一个隔离的环境中运行该工具

## 安装说明

```bash
npm install -g agent-wallet-cli
```

验证安装结果：`agent-wallet-cli --version`

## 使用流程

**切勿将`--password`作为命令行参数传递**，因为这可能导致密码泄露（会显示在shell历史记录和进程列表中）。请通过标准输入传递密码：

```bash
echo "$WALLET_PASSWORD" | agent-wallet-cli unlock --duration 3600
```

1. **初始化钱包（首次使用）**：`echo "$WALLET_PASSWORD" | agent-wallet-cli init`  
   - 仅显示一次助记词，并将其安全地保存下来。
2. **导入现有钱包**：`echo "$WALLET_PASSWORD" | agent-wallet-cli import --mnemonic "word1 word2 ..."`  
3. **解锁钱包**：`echo "$WALLET_PASSWORD" | agent-wallet-cli unlock --duration 3600`  
   - 会返回一个有效期为3600分钟的会话令牌（格式为`wlt_...`）。
4. **使用钱包**：在所有命令后添加`--token wlt_...`参数（无需输入密码）。
5. **锁定钱包**：操作完成后执行`agent-wallet-cli lock`。

## 全局配置选项

所有命令都支持以下选项：
- `--format json|text`（默认：json）
- `--wallet-dir <path>`（默认：`~/.agent-wallet-cli`）
- `--quiet`（默认：不显示输出）
- `--name <name>`（默认：`default`）

## 命令列表

### 钱包管理
```bash
echo "$WALLET_PASSWORD" | agent-wallet-cli init [--word-count 12|24] [--name <name>]
echo "$WALLET_PASSWORD" | agent-wallet-cli import --mnemonic "<phrase>" [--name <name>]
echo "$WALLET_PASSWORD" | agent-wallet-cli unlock [--duration <secs>] [--name <name>]
agent-wallet-cli lock [--name <name>]
echo "$WALLET_PASSWORD" | agent-wallet-cli export --confirm [--name <name>]
```

### 地址与余额查询
```bash
agent-wallet-cli address --token wlt_... [--chain ethereum|solana] [--account-index 0]
agent-wallet-cli balance --token wlt_... --chain <chain> [--network mainnet] [--token-address usdc]
```

### 转账操作
```bash
# Native (ETH/SOL)
agent-wallet-cli send --token wlt_... --chain <chain> --to <addr> --amount <amt> --yes [--dry-run]
# ERC-20/SPL token
agent-wallet-cli send --token wlt_... --chain <chain> --to <addr> --amount <amt> --token-address <addr|alias> --yes
```

**进行大额转账时，请务必添加`--yes`参数以跳过交互式确认（非TTY环境或代理程序使用时必须使用此参数）。**

### 批准操作（ERC-20/SPL标准）
```bash
agent-wallet-cli approve --token wlt_... --chain <chain> --token-address <addr> --spender <addr> --amount <amt|unlimited> --yes
agent-wallet-cli allowance --chain <chain> --token-address <addr> --owner <addr> --spender <addr>
agent-wallet-cli transfer-from --token wlt_... --chain <chain> --token-address <addr> --from <addr> --to <addr> --amount <amt>
agent-wallet-cli approvals --token wlt_... [--chain ethereum] [--limit 20]
```

### 签名操作
```bash
agent-wallet-cli sign --token wlt_... --chain <chain> --message "text"
agent-wallet-cli sign --token wlt_... --chain <chain> --typed-data '<json|@file>'
agent-wallet-cli sign --token wlt_... --chain <chain> --data <hex>
```

### 交易历史查询
```bash
agent-wallet-cli history --token wlt_... --chain <chain> [--network mainnet] [--limit 10]
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

对于基于EVM的侧链（如Base、Polygon、Arbitrum），请使用`--chain ethereum --network <l2name>`进行连接。

## 代币别名

可以使用简写形式代替合约地址，例如：`usdc`、`usdt`、`dai`、`weth`、`wbtc`。

## 安全注意事项：

- **完全自托管**：密钥始终存储在你的设备上，并采用加密方式保护。
- 该工具不收集任何分析数据或发送网络请求，仅通过公共区块链API进行查询和交易操作。
- 会话令牌仅提供临时访问权限，应将其视为临时密码使用。
- 在进行大额转账前，请务必执行`--dry-run`测试。
- 操作完成后请锁定钱包。
- 绝不要记录或分享会话令牌或助记词。
- 请定期审查源代码：[github.com/donald-jackson/agent-wallet-cli](https://github.com/donald-jackson/agent-wallet-cli)