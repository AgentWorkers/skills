---
name: revolut
description: "Revolut Business API CLI：支持账户信息、余额查询、交易记录、交易对手方信息、支付操作以及外汇兑换功能，并提供CSV文件导出功能。该工具会自动更新OAuth令牌。仅适用于企业账户（不支持个人账户）。"
version: 1.0.0
metadata: {"clawdbot":{"emoji":"💶","requires":{"bins":["python3"]}}}
---

# Revolut Business API

这是一个用于操作**Revolut Business**账户的完整命令行工具（CLI），支持账户管理、交易处理、支付、货币兑换、数据导出等功能。

**入口文件：`python3 {baseDir}/scripts/revolut.py`

## 设置

### 交互式设置向导（推荐）
```bash
python3 {baseDir}/scripts/setup.py
```
该向导会指导您完成所有设置步骤：生成API密钥、上传Revolut证书、配置OAuth回调以及进行身份验证。

### 手动设置
- 需要Python 3.10及以上版本，并安装`pip install PyJWT cryptography`库。
- 拥有Revolut Business账户以及相应的API证书。
- 详细操作指南请参阅[README](https://github.com/christianhaberl/revolut-openclaw-skill)。

### 凭据存储位置
凭据文件存储在`~/.clawdbot/revolut/`目录下：
- `private.pem` — RSA私钥（用于JWT签名）
- `certificate.pem` — X509证书（上传至Revolut）
- `tokens.json` — OAuth令牌（系统自动管理）
- `config.json` — 客户端ID、域名及重定向URI

### 环境变量（在`.env`文件中配置）
- `REVOLUT_CLIENT_ID` — 从Revolut API设置中获取的客户端ID
- `REVOLUT_ISS_DOMAIN` — 您的重定向URI域名（不含`https://`前缀）

## 命令列表

### 账户与余额查询
```bash
python3 {baseDir}/scripts/revolut.py accounts          # List all accounts with balances
python3 {baseDir}/scripts/revolut.py balance            # Total EUR balance
python3 {baseDir}/scripts/revolut.py accounts --json    # JSON output
```

### 交易管理
```bash
python3 {baseDir}/scripts/revolut.py transactions                    # Last 20
python3 {baseDir}/scripts/revolut.py tx -n 50                       # Last 50
python3 {baseDir}/scripts/revolut.py tx --since 2026-01-01           # Since date
python3 {baseDir}/scripts/revolut.py tx --since 2026-01-01 --to 2026-01-31
python3 {baseDir}/scripts/revolut.py tx -a Main                     # Filter by account
python3 {baseDir}/scripts/revolut.py tx --type card_payment          # Filter by type
python3 {baseDir}/scripts/revolut.py tx --json                      # JSON output
```

支持的交易类型：`card_payment`（卡片支付）、`transfer`（转账）、`exchange`（货币兑换）、`topup`（充值）、`atm`（ATM取款）、`fee`（手续费）、`refund`（退款）

### 交易对手方信息
```bash
python3 {baseDir}/scripts/revolut.py counterparties     # List all
python3 {baseDir}/scripts/revolut.py cp --name "Lisa"   # Search by name
python3 {baseDir}/scripts/revolut.py cp --json
```

### 支付操作
```bash
# Send payment (with confirmation prompt)
python3 {baseDir}/scripts/revolut.py pay -c "Lisa Dreischer" --amount 50.00 --currency EUR -r "Lunch"

# Create draft (no immediate send)
python3 {baseDir}/scripts/revolut.py pay -c "Lisa Dreischer" --amount 50.00 --draft -r "Lunch"

# Skip confirmation
python3 {baseDir}/scripts/revolut.py pay -c "Lisa Dreischer" --amount 50.00 -y
```

### 货币兑换
```bash
python3 {baseDir}/scripts/revolut.py exchange --amount 100 --sell EUR --buy USD
python3 {baseDir}/scripts/revolut.py fx --amount 500 --sell EUR --buy GBP
```

### 内部转账
```bash
python3 {baseDir}/scripts/revolut.py transfer --from-account <ID> --to-account <ID> --amount 100
```

### 数据导出（CSV格式）
```bash
python3 {baseDir}/scripts/revolut.py export                           # Print CSV to stdout
python3 {baseDir}/scripts/revolut.py export -n 200 -o transactions.csv  # Save to file
python3 {baseDir}/scripts/revolut.py export --since 2026-01-01 -o jan.csv
```

### 令牌状态查询
```bash
python3 {baseDir}/scripts/revolut.py token-info
```

## 令牌自动刷新
- 访问令牌在约40分钟后失效。
- 在每次API调用前会自动使用刷新令牌进行更新。
- 初始认证完成后无需手动操作。

## 安全注意事项
- 私钥和令牌存储在`~/.clawdbot/revolut/`目录中，属于敏感信息，请妥善保管。
- 所有支付操作均需用户明确确认（可使用`--yes`选项跳过确认步骤）。
- 使用`--draft`选项创建的支付请求需要用户在Revolut应用程序中审批。
- 严禁泄露您的私钥、令牌或客户端认证令牌（JWT）。