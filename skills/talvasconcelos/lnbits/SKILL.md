---
name: lnbits
description: 管理 LNbits Lightning 钱包（查看余额、进行支付、生成发票）
homepage: https://lnbits.com
metadata: {"clawdbot":{"emoji":"⚡","requires":{"bins":["python3"],"env":["LNBITS_API_KEY", "LNBITS_BASE_URL"]},"primaryEnv":"LNBITS_API_KEY"}}
---

# LNbits 钱包管理器

该工具可帮助用户安全、高效地管理 LNbits Lightning Network 钱包。

## 🛑 关键安全协议 🛑

1. **切勿泄露敏感信息**：严禁显示管理员密钥、用户 ID 或钱包 ID。
2. **明确确认**：在支付前必须获取用户的确认（“是/否”）。
    *   *格式*：“我即将向 **[收件地址/备注]** 发送 **[金额] 萨托希**。继续吗？(y/n)”
3. **先检查余额**：在执行支付操作前，请务必先调用 `balance` 函数以确认余额是否足够。

## 使用方法

### 0. 设置/创建钱包
如果用户尚未拥有 LNbits 钱包，您可以在演示服务器上为他们创建一个钱包。

```bash
python3 {baseDir}/scripts/lnbits_cli.py create --name "My Wallet"
```

**操作步骤**：
1. 运行相关命令。
2. 获取 `adminkey`（管理员密钥）和 `base_url`（默认值为 https://demo.lnbits.com）。
3. **重要提示**：请指导用户妥善保管这些凭据：
    > “我已经为您创建了一个新的钱包！请将这些信息添加到您的 Moltbot 配置文件或 `.env` 文件中：
    > `export LNBITS_BASE_URL=https://demo.lnbits.com`
    > `export LNBITS_API_KEY=<adminkey>`

### 1. 查看余额
查看当前钱包的余额（单位：萨托希）。

```bash
python3 {baseDir}/scripts/lnbits_cli.py balance
```

### 2. 生成收款发票
生成一个 Bolt11 格式的发票以接收资金。
*   **金额**：以萨托希为单位的收款金额（整数）。
*   **备注**：可选的收款说明。

```bash
python3 {baseDir}/scripts/lnbits_cli.py invoice --amount 1000 --memo "Pizza"
```

### 3. 支付发票
**⚠️ 需要确认**：先解码发票信息，核实余额，再征求用户确认，最后执行支付操作。

```bash
# Step 1: Decode to verify amount/memo
python3 {baseDir}/scripts/lnbits_cli.py decode <bolt11_string>

# Step 2: Pay (Only after user CONFIRMS)
python3 {baseDir}/scripts/lnbits_cli.py pay <bolt11_string>
```

## 错误处理
如果命令行界面返回 JSON 格式的错误信息（例如 `{"error": "Insufficient funds"}`），请为用户清晰地说明错误原因，切勿直接显示原始的错误堆栈跟踪信息。