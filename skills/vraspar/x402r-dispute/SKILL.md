---
name: x402r-dispute
description: 根据 x402r 可退款支付协议，向商家付款并处理支付纠纷。
version: 0.2.0
author: x402r
tags: [x402r, payments, disputes, web3, arbitration]
---
# x402r CLI

该工具帮助用户使用 x402r 协议进行托管支付并处理支付纠纷。x402r 协议为 HTTP 402 错误响应（402）添加了可退款的功能——买家可以通过链上仲裁来申请退款。

## 设置

```bash
npx --yes @x402r/cli config --key <private-key> --arbiter-url https://www.moltarbiter.com/arbiter
```

操作者、网络和远程过程调用（RPC）信息会自动从仲裁者那里获取。用户需要持有 Base Sepolia ETH（作为交易手续费）以及 USDC（用于支付）。

测试商家示例：`https://fantastic-optimism-production-602a.up.railway.app/weather`

## 命令

### pay

```bash
npx --yes @x402r/cli pay <url>
npx --yes @x402r/cli pay <url> --output response.json
```

执行托管支付操作，并将支付信息保存到 `~/.x402r/last-payment.json` 文件中，以便后续处理纠纷。

### dispute

```bash
npx --yes @x402r/cli dispute "reason" --evidence "details"
```

一步完成链上退款请求的提交及证据文件的上传。该命令会使用 `pay` 命令保存的支付信息，并生成一个用于查看纠纷进展的仪表板链接。

选项：
- `-e/--evidence <text>`：指定提交的证据内容
- `-f/--file <path>`：指定证据文件的路径
- `-p/--payment-json <json>`：指定支付信息的 JSON 格式化字符串
- `-n/--nonce <n>`：指定随机数（用于防止重复请求）
- `-a/--amount <n>`：指定退款金额

### status

```bash
npx --yes @x402r/cli status
```

检查纠纷的处理状态。首先尝试通过仲裁者的 API 获取结果，若无法获取则通过链上机制获取结果。

选项：
- `--id <compositeKey>`：指定纠纷的唯一标识符
- `-p/--payment-json`：指定支付信息的 JSON 格式化字符串
- `-n/--nonce`：指定随机数（用于防止重复请求）

### show

```bash
npx --yes @x402r/cli show
```

显示与特定纠纷相关的所有证据（包括付款方、商家和仲裁者的信息）。

选项：
- `-p/--payment-json`：指定支付信息的 JSON 格式化字符串
- `-n/--nonce`：指定随机数（用于防止重复请求）

### verify

```bash
npx --yes @x402r/cli verify
```

重新执行仲裁者的智能评估过程，以验证退款承诺的哈希值是否具有确定性（即评估结果是否唯一）。

选项：
- `-p/--payment-json`：指定支付信息的 JSON 格式化字符串
- `-n/--nonce`：指定随机数（用于防止重复请求）

### list

```bash
npx --yes @x402r/cli list
```

列出所有由仲裁者处理的纠纷记录。

选项：
- `-r/--receiver <addr>`：指定纠纷的接收者地址
- `--offset <n>`：指定查询结果的起始索引
- `--count <n>`：指定显示的纠纷记录数量

## 典型工作流程

1. `npx --yes @x402r/cli pay <merchant-url>`：执行托管支付并保存相关状态信息
2. `npx --yes @x402r/cli dispute "reason" --evidence "details"`：提交纠纷申请并附上证据
3. `npx --yes @x402r/cli status`：查看仲裁者的裁决结果
4. `npx --yes @x402r/cli show`：查看所有相关方的证据信息
5. `npx --yes @x402r/cli verify`：验证裁决结果是否具有确定性

## 注意事项

- 在执行不同命令时，系统会自动保存相关状态信息：
  - `pay` 命令会将支付信息保存到 `~/.x402r/last-payment.json` 文件中，以便后续的纠纷处理
  - `dispute` 命令会使用这些保存的信息
  - `status`、`show` 和 `verify` 命令会读取这些保存的信息
- 如果没有保存状态信息，需要手动通过 `---payment-json` 和 `--nonce` 参数提供必要的信息
- `verify` 命令需要连接仲裁者服务器，无法通过链上机制进行替代处理