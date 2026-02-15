---
name: authenticate-wallet
description: 登录钱包。当您或用户需要登录、连接钱包，或设置钱包时，以及当任何钱包操作因身份验证问题或“未登录”错误而失败时，可以使用此功能。在进行转账、交易或充值之前，必须先完成此登录步骤。
user-invocable: true
disable-model-invocation: false
allowed-tools: ["Bash(npx awal@latest status*)", "Bash(npx awal@latest auth *)", "Bash(npx awal@latest balance*)", "Bash(npx awal@latest address*)", "Bash(npx awal@latest show*)"]
---

# 使用支付钱包进行身份验证

当钱包未登录（通过 `npx awal status` 命令检测到）或钱包操作因身份验证错误而失败时，可以使用 `npx awal` CLI 命令进行身份验证。

如果您能够访问用户的电子邮件地址，您可以自行完成身份验证；否则，您需要请求相关人员提供他们的电子邮件地址以及收到的 OTP 代码。

## 身份验证流程

身份验证采用两步电子邮件 OTP 验证流程：

### 第一步：启动登录流程

```bash
npx awal@latest auth login <email>
```

系统会向用户的电子邮件地址发送一个 6 位的验证码，并返回一个 `flowId`。

### 第二步：验证 OTP

```bash
npx awal@latest auth verify <flowId> <otp>
```

使用第一步中获得的 `flowId` 以及用户电子邮件中的 6 位验证码来完成身份验证。如果您能够访问用户的电子邮件地址，可以直接读取 OTP 代码；否则，需要向相关人员索取该代码。

## 检查身份验证状态

```bash
npx awal@latest status
```

该命令会显示钱包服务器的运行状态以及身份验证结果，包括钱包的地址。

## 示例会话

```bash
# Check current status
npx awal@latest status

# Start login (sends OTP to email)
npx awal@latest auth login user@example.com
# Output: flowId: abc123...

# After user receives code, verify
npx awal@latest auth verify abc123 123456

# Confirm authentication
npx awal@latest status
```

## 可用的 CLI 命令

| 命令                                      | 功能                                      |
| -------------------------------------------- | -------------------------------------- |
| `npx awal@latest status`                     | 检查服务器运行状态和身份验证状态            |
| `npx awal@latest auth login <email>`         | 向用户电子邮件发送 OTP 代码，并返回 `flowId`           |
| `npx awal@latest auth verify <flowId> <otp>` | 使用 OTP 代码完成身份验证                    |
| `npx awal@latest balance`                    | 查看钱包中的 USDC 余额                        |
| `npx awal@latest address`                    | 获取钱包地址                              |
| `npx awal@latest show`                       | 打开钱包的辅助窗口                          |

## JSON 输出

所有命令都支持使用 `--json` 选项来生成机器可读的 JSON 输出格式：

```bash
npx awal@latest status --json
npx awal@latest auth login user@example.com --json
npx awal@latest auth verify <flowId> <otp> --json
```