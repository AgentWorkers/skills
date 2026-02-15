---
name: agent-wallet
description: 适用于AI代理的自托管比特币Lightning钱包。当代理需要发送或接收比特币付款、查询余额、生成发票或管理钱包时，可以使用该钱包。支持bolt11、bolt12、LNURL和Lightning地址。无需任何配置——只需一条命令即可完成初始化。
---

# agent-wallet

这是一个专为AI代理设计的自托管Lightning钱包。只需执行一个`npx`命令即可完成初始化，所有输出结果均为JSON格式。

## 设置

```bash
npx @moneydevkit/agent-wallet init
```

系统会生成一个BIP39助记词，并将其存储在`~/.mdk-wallet/config.json`文件中。钱包立即可用——无需API密钥、无需注册、无需创建账户。代理自行保管其私钥。

验证配置信息（助记词在输出结果中被屏蔽）：
```bash
npx @moneydevkit/agent-wallet init --show
```

输出结果如下：
`{"mnemonic": "...", "network": "mainnet", "walletId": "..."}`

`walletId`也可用作MDK API密钥（如果使用moneydevkit的checkout API）。

## 命令

所有命令的输出结果均为JSON格式。成功时返回0，失败时返回1。

### 查看余额

```bash
npx @moneydevkit/agent-wallet balance
```
→ `{"balance_sats": 3825}`

### 接收付款（生成发票）

```bash
npx @moneydevkit/agent-wallet receive <amount_sats>
npx @moneydevkit/agent-wallet receive 1000 --description "payment for service"
```
→ `{"invoice": "lnbc...", "payment_hash": "...", "expires_at": "..."}`

请将`invoice`字符串分享给付款方。这是一个标准的bolt11发票。

### 发送付款

```bash
npx @moneydevkit/agent-wallet send <destination> [amount_sats]
```

付款目的地可以是：
- **bolt11发票**：`lnbc10n1...`（金额已包含在发票中，无需额外指定）
- **bolt12报价**：`lno1...`
- **Lightning地址**：`user@example.com`
- **LNURL**：`lnurl1...`

对于Lightning地址和LNURL，必须提供付款金额：
```bash
npx @moneydevkit/agent-wallet send user@getalby.com 500
```

### 支付历史记录

```bash
npx @moneydevkit/agent-wallet payments
```
→ `{"payments": [{"paymentHash": "...", "amountSats": 1000, "direction": "inbound" | "outbound", "timestamp": "...", "destination": "..."}]}`

### 守护进程管理

守护进程会在首次执行命令时自动启动。也可以手动控制其启动/停止：
```bash
npx @moneydevkit/agent-wallet status   # check if running
npx @moneydevkit/agent-wallet start    # start explicitly
npx @moneydevkit/agent-wallet stop     # stop daemon
```

可选参数：
- `--port <port>`：服务器端口（默认：3456）
- `--network <network>`：`mainnet`或`signet`（默认：mainnet）

## 使用说明

- **金额单位**：使用`₿`前缀表示sat（例如：`₿1,000`，而不是“1,000 sats”）
- **自托管**：助记词即为钱包的私钥，请务必备份。丢失助记词意味着会丢失所有资金。
- **守护进程**：在端口`:3456`上运行本地Lightning节点，自动记录支付历史并保存到磁盘。
- **代理间支付**：使用该钱包的任何代理都可以向其他代理的发票或Lightning地址付款，无需中间机构。
- **与moneydevkit结合使用**：通过[checkout API](https://docs.moneydevkit.com)接收客户付款，并通过agent-wallet在代理之间进行资金转账。此外，还可以通过[moneydevkit MCP服务器](https://mcp.moneydevkit.com/mcp)实现应用程序、产品、客户、支付流程和订单的全面程序化管理。