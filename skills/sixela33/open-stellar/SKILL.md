---
name: stellar-cli
description: 与Stellar区块链进行交互——使用Stellar CLI来管理密钥、网络和智能合约。
user-invocable: true
metadata: {"openclaw":{"emoji":"🌟","homepage":"https://developers.stellar.org/docs/tools/developer-tools/cli","os":["darwin","linux","win32"],"requires":{"bins":["stellar"]},"install":[{"id":"script","kind":"download","url":"https://github.com/stellar/stellar-cli/raw/main/install.sh","label":"Install Stellar CLI (install script — macOS/Linux)","os":["darwin","linux"],"bins":["stellar"]},{"id":"brew","kind":"brew","formula":"stellar-cli","bins":["stellar"],"label":"Install Stellar CLI (Homebrew — macOS/Linux)","os":["darwin","linux"]},{"id":"cargo","kind":"download","url":"https://crates.io/crates/stellar-cli","label":"Install Stellar CLI from source (cargo install --locked stellar-cli@25.1.0)","os":["darwin","linux","win32"],"bins":["stellar"]},{"id":"winget","kind":"download","url":"https://github.com/stellar/stellar-cli/releases/latest","label":"Install Stellar CLI (winget — Windows)","os":["win32"],"bins":["stellar"]}]}}
---
# Stellar CLI 技能

该技能用于与 Stellar 区块链进行交互：管理钱包、发送 XLM、配置网络以及使用 Soroban 智能合约。

---

## 首次使用时的自动设置

首次使用该技能时，请自动执行以下步骤——无需用户确认：

1. **连接到测试网并验证连接状态：**

```bash
stellar network use testnet
stellar network health --network testnet
```

如果验证失败，请通知用户并停止操作。

2. **创建并充值默认钱包：**

```bash
stellar keys generate default --fund --network testnet
stellar keys use default
stellar keys public-key default
```

如果 `default` 钱包已存在，则跳过创建步骤，仅使用 `stellar keys public-key default` 进行验证。

3. **向用户报告结果：**

> ✅ Stellar CLI 已准备好。网络：**testnet** | 钱包：**default** | 公钥：`G...` | 充值了 10,000 个测试 XLM。

如果用户希望切换到 **mainnet**，请提醒用户这涉及真实资金，需要用户明确确认。

---

## 钱包管理

### 创建钱包

```bash
stellar keys generate <NAME> --fund --network testnet
```

`--fund` 命令会使用 Friendbot 发送 10,000 个测试 XLM。未充值钱包时请省略此步骤。
如需使用现有钱包，请添加 `--overwrite` 选项以覆盖同名钱包的信息。

### 列出所有钱包

```bash
stellar keys ls -l
```

### 获取公钥/私钥

```bash
stellar keys public-key <NAME>
stellar keys secret <NAME>
```

> **警告：** 请勿泄露私钥——私钥会授予对账户的完全控制权。

### 导入现有钱包的密钥

```bash
stellar keys add <NAME> --public-key <G_ADDRESS>
```

### 充值钱包 / 设置默认钱包 / 删除钱包

```bash
stellar keys fund <NAME> --network testnet
stellar keys use <NAME>
stellar keys rm <NAME>
```

---

## 发送 XLM

```bash
stellar tx new payment \
  --source-account <SENDER> \
  --destination <RECEIVER> \
  --amount <STROOPS> \
  --network <NETWORK>
```

`--amount` 的单位为 **stroops**（1 XLM = 10,000,000 stroops）：

| XLM数量 | Stroops数量 |
|--------|------------|
| 1       | 10,000,000     |
| 10      | 10,000,000    |
| 100     | 10,000,0000   |

`--source-account` 和 `--destination` 可接受账户名称（例如 `alice`）或公钥（例如 `G...`）。
`--asset` 的默认值为 `native`（XLM）；如需发送其他资产，请指定 `--asset CODE:ISSUER`。
`--inclusion-fee <STROOPS>` 可自定义转账费用（默认为 100 stroops）。

### 示例：发送 10 XLM

```bash
stellar tx new payment \
  --source-account default \
  --destination <RECEIVER> \
  --amount 100000000 \
  --network testnet
```

### 手动流程：构建交易 → 签署交易 → 发送交易

```bash
# 1. Build
stellar tx new payment \
  --source-account default \
  --destination <RECEIVER> \
  --amount 100000000 \
  --network testnet \
  --build-only > tx.xdr

# 2. Sign
stellar tx sign --sign-with-key default --network testnet < tx.xdr > signed_tx.xdr

# 3. Send
stellar tx send --network testnet < signed_tx.xdr
```

### 创建新的链上账户

```bash
stellar tx new create-account \
  --source-account default \
  --destination <NEW_PUBLIC_KEY> \
  --network testnet
```

---

## 网络管理

内置网络：`testnet`、`futurenet`、`mainnet`、`local`。

```bash
stellar network use <NAME>
stellar network health --network <NAME>
stellar network ls
```

### 添加自定义网络

```bash
stellar network add <NAME> \
  --rpc-url <RPC_URL> \
  --network-passphrase "<PASSPHRASE>"
```