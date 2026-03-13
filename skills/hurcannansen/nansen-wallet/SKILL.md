---
name: nansen-wallet
description: 钱包管理功能：包括创建、列出、查看、导出、发送和删除钱包。这些功能可用于创建新的钱包、查询钱包余额以及发送代币。
metadata:
  openclaw:
    requires:
      env:
        - NANSEN_API_KEY
      bins:
        - nansen
    primaryEnv: NANSEN_API_KEY
    install:
      - kind: node
        package: nansen-cli
        bins: [nansen]
allowed-tools: Bash(nansen:*)
---
# 钱包

## 身份验证设置

```bash
# Save API key (non-interactive)
nansen login --api-key <key>
# Or via env var:
NANSEN_API_KEY=<key> nansen login

# Verify
nansen research profiler labels --address 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045 --chain ethereum
```

## 钱包创建（两步代理流程）

创建钱包需要用户提供密码。代理程序**严禁**自行生成或存储密码。

> **步骤 1（代理 → 用户）：** 要求用户提供钱包密码（至少 12 个字符）。
>
> **步骤 2（代理执行）：** 使用用户提供的密码运行 `create` 命令。

```bash
NANSEN_WALLET_PASSWORD="<password_from_user>" nansen wallet create
```

钱包创建完成后，命令行界面（CLI）会自动将密码保存到以下位置：
- **操作系统密钥链**（macOS 的 Keychain、Linux 的 secret-tool、Windows 的 Credential Manager）——最安全的方式
- `~/.nansen/wallets/.credentials` 文件——在密钥链不可用的情况下作为不安全的备用方案（例如在容器或持续集成（CI）环境中）

**所有后续的钱包操作都会自动获取密码**——无需使用环境变量或用户输入。

如果使用了 `~/.nansen/wallets/.credentials` 文件作为备用方案，CLI 会在每次操作时显示警告。如需后续切换到更安全的存储方式，请运行 `nansen wallet secure`。

### 密码获取的优先级（自动排序）：
1. `NANSEN_WALLET_PASSWORD` 环境变量（如果已设置）
2. 操作系统密钥链（在创建钱包时自动保存）
3. `~/.nansen/wallets/.credentials` 文件（不安全的备用方案，会显示警告）
4. 包含操作说明的结构化 JSON 文件（如果上述方式均不可用）

### 对代理程序的重要规则：
- **严禁**自行生成密码——必须始终要求用户提供密码
- **严禁**将密码存储在文件、内存、日志或对话记录中
- **严禁**使用 `--human` 标志——该标志会启用交互式提示，而代理程序无法处理这些提示
- 钱包创建完成后，后续操作无需再输入密码——密钥链会自动处理密码
- 如果出现 `PASSWORD_REQUIRED` 错误，请要求用户再次提供密码

## 创建钱包

```bash
# Ask the user for a password first, then:
NANSEN_WALLET_PASSWORD="<password_from_user>" nansen wallet create
# Or with a custom name:
NANSEN_WALLET_PASSWORD="<password_from_user>" nansen wallet create --name trading
```

## 列出钱包信息及显示详情

```bash
nansen wallet list
nansen wallet show <name>
nansen wallet default <name>
```

## 发送交易

```bash
# Send native token (SOL, ETH) — password auto-resolved from keychain
nansen wallet send --to <addr> --amount 1.5 --chain solana

# Send entire balance
nansen wallet send --to <addr> --chain evm --max

# Dry run (preview, no broadcast)
nansen wallet send --to <addr> --amount 1.0 --chain evm --dry-run
```

## 导出钱包信息

```bash
# Password auto-resolved from keychain
nansen wallet export <name>
nansen wallet delete <name>
```

## 忘记密码

```bash
# Remove saved password from all stores (keychain + .credentials file)
nansen wallet forget-password
```

## 迁移到更安全的存储方式

```bash
nansen wallet secure
```

有关从 `~/.nansen/.env`、`.credentials` 或仅使用环境变量的设置进行迁移的详细步骤，请参阅 `nansen-wallet-migration` 技能文档。

## 命令行参数（Flags）

| 参数 | 用途 |
|------|---------|
| `--to` | 收件人地址 |
| `--amount` | 要发送的金额 |
| `--chain` | 交易链（`evm` 或 `solana`） |
| `--max` | 发送全部余额 |
| `--dry-run` | 预览交易（不进行广播） |
| `--human` | 启用交互式提示（仅适用于人类用户使用的终端——代理程序禁止使用此选项） |
| `--unsafe-no-password` | 跳过加密步骤（密钥以明文形式存储——不推荐使用） |

## 环境变量

| 变量 | 用途 |
|-----|---------|
| `NANSEN_WALLET_PASSWORD` | 钱包加密密码——仅在首次创建钱包时需要。之后由操作系统密钥链负责管理密码 |
| `NANSEN_API_KEY` | API 密钥（也可通过 `nansen login --api-key <key>` 设置） |
| `NANSEN_EVM_RPC` | 自定义的 EVM RPC 端点 |
| `NANSEN_SOLANA_RPC` | 自定义的 Solana RPC 端点 |