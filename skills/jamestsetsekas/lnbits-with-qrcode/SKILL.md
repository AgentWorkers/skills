---
name: lnbits
description: 管理 LNbits Lightning 钱包（查看余额、进行支付、生成发票）
homepage: https://lnbits.com
metadata: {"clawdbot":{"emoji":"⚡","requires":{"bins":["python3"],"pip":["qrcode[pil]"],"env":["LNBITS_API_KEY", "LNBITS_BASE_URL"]},"primaryEnv":"LNBITS_API_KEY"}}
---

# LNbits 钱包管理器

该工具可帮助用户安全、高效地管理 LNbits Lightning Network 钱包。

## 🛑 重要协议 🛑

1. **切勿泄露敏感信息**：严禁显示管理员密钥（admin_key）、用户 ID 或钱包 ID。
2. **明确确认**：在支付前必须获取用户的确认（“是/否”）。
    *   **格式示例**：“我即将向 **[收款地址/备注]** 发送 **[金额] 萨托希**。继续吗？(y/n)”
3. **先检查余额**：在执行支付操作前，请务必先调用 `balance` 函数以确认余额是否足够。
4. **务必包含发票和二维码**：生成发票时，必须：
    (a) 显示 `payment_request` 字符串以便用户复制；
    (b) 在同一行输出 `MEDIA:` 后跟 `qr_file` 的路径。切勿省略此步骤。

## 使用方法

### 0. 设置/创建钱包
如果用户尚未拥有 LNbits 钱包，您可以在演示服务器上为他们创建一个钱包。

```bash
python3 {baseDir}/scripts/lnbits_cli.py create --name "My Wallet"
```

**操作步骤**：
1. 运行相应命令。命令行工具（CLI）会将包含 `adminkey` 和 `base_url` 的 JSON 数据输出到终端。
2. **切勿泄露敏感信息**：切勿在聊天中重复、引用或显示 `adminkey` 或任何其他敏感信息。用户只能通过终端看到命令的输出结果；这是这些信息唯一应该出现的地方。
3. 用简单的语言向用户说明操作步骤，例如：
    > “已创建一个新的钱包。命令输出中包含了您的 **adminkey** 和 **base_url**。请将这些信息从终端复制到您的配置文件或 `.env` 文件中，分别设置为 `LNBITS_API_KEY` 和 `LNBITS_BASE_URL`。切勿将这些信息粘贴到聊天中。”

### 1. 查看余额
获取钱包当前的余额（单位：萨托希）。

```bash
python3 {baseDir}/scripts/lnbits_cli.py balance
```

### 2. 生成发票（接收资金）
生成一个 Bolt11 格式的发票以接收资金。**系统会自动生成二维码**。
*   **金额**：以萨托希为单位的金额（整数）。
*   **备注**：可选的收款说明。
*   **--no-qr**：如果不需要二维码，则省略该选项。

```bash
# Invoice with QR code (default)
python3 {baseDir}/scripts/lnbits_cli.py invoice --amount 1000 --memo "Pizza"

# Invoice without QR code
python3 {baseDir}/scripts/lnbits_cli.py invoice --amount 1000 --memo "Pizza" --no-qr
```

**⚠️ 必须包含的响应格式**：
生成发票时，您的回复必须包含以下内容：
1. **可供用户复制的发票文本**：显示完整的 `payment_request` 字符串。
2. **二维码图像**：在同一行输出 `MEDIA:` 后跟 `qr_file` 的路径。

**格式要求**：
```
Here is your 100 sat invoice:

lnbc1u1p5abc123...

MEDIA:./clawd/.lnbits_qr/invoice_xxx.png
```

**重要提示**：`MEDIA:` 和文件路径必须在同一行显示，这样才能将二维码图像正确发送给用户。

### 2b. 从现有发票生成二维码
将任何 Bolt11 格式的字符串转换为二维码图像文件。

```bash
python3 {baseDir}/scripts/lnbits_cli.py qr <bolt11_string>
```

返回结果：`{"qr_file": "./.lnbits_qr/invoice_xxx.png", "bolt11": "..."}`

### 3. 支付发票（发送资金）
**⚠️ 需要用户确认**：先解码发票信息，确认余额，再征求用户同意后执行支付操作。

```bash
# Step 1: Decode to verify amount/memo
python3 {baseDir}/scripts/lnbits_cli.py decode <bolt11_string>

# Step 2: Pay (Only after user CONFIRMS)
python3 {baseDir}/scripts/lnbits_cli.py pay <bolt11_string>
```

## 错误处理
如果 CLI 返回错误信息（例如 `{"error": "Insufficient funds"}`），请向用户清晰地说明问题原因。切勿直接显示原始的错误堆栈跟踪信息。