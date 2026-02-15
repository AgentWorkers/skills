---
name: pay-for-service
description: 向一个 x402 端点发起带有自动 USDC 支付的付费 API 请求。当您或用户需要调用付费 API、发起 x402 请求、使用付费服务或为 API 调用付费时，请使用此功能。在使用该功能之前，请先通过“搜索服务”（search-for-service）找到相应的服务。
user-invocable: true
disable-model-invocation: false
allowed-tools: ["Bash(npx awal@latest status*)", "Bash(npx awal@latest balance*)", "Bash(npx awal@latest x402 pay *)"]
---

# 发送付费的 X402 请求

使用 `npx awal@latest x402 pay` 命令来调用支持自动 USDC 支付的 API 端点。

## 确认钱包已初始化并完成身份验证

```bash
npx awal@latest status
```

如果钱包尚未完成身份验证，请参考 `authenticate-wallet` 技能。

## 命令语法

```bash
npx awal@latest x402 pay <url> [-X <method>] [-d <json>] [-q <params>] [-h <json>] [--max-amount <n>] [--json]
```

## 选项

| 选项                        | 描述                                                  |
| ----------------------------- |--------------------------------------------------------- |
| `-X, --method <方法>`       | HTTP 方法（默认：GET）                                      |
| `-d, --data <json>`       | 请求体（以 JSON 字符串形式提供）                         |
| `-q, --query <参数>`       | 查询参数（以 JSON 字符串形式提供）                         |
| `-h, --headers <json>`       | 自定义 HTTP 请求头（以 JSON 字符串形式提供）                   |
| `--max-amount <金额>`       | 最大支付金额（单位：USDC 原子单位，1000000 = $1.00）                   |
| `--correlation-id <ID>`     | 相关操作的标识符                                      |
| `--json`                | 输出结果以 JSON 格式显示                                   |

## USDC 金额说明

X402 使用 USDC 原子单位进行计费（小数点后有 6 位）：

| 原子单位 | 美元（USD） |
| -------- | -------- |
| 1000000   | $1.00                |
| 100000   | $0.10                |
| 50000    | $0.05                |
| 10000    | $0.01                |

**重要提示**：使用 `$` 标记的金额必须使用单引号括起来，以防止 Bash 变量扩展（例如：`'$1.00'` 而不是 `$1.00`）。

## 示例

```bash
# Make a GET request (auto-pays)
npx awal@latest x402 pay https://example.com/api/weather

# Make a POST request with body
npx awal@latest x402 pay https://example.com/api/sentiment -X POST -d '{"text": "I love this product"}'

# Limit max payment to $0.10
npx awal@latest x402 pay https://example.com/api/data --max-amount 100000
```

## 先决条件

- 必须完成身份验证（使用 `npx awal@latest status` 命令检查，详情请参阅 `authenticate-wallet` 技能） |
- 钱包中必须有足够的 USDC 余额（使用 `npx awal@latest balance` 命令检查） |
- 如果不知道 API 端点地址，可以使用 `search-for-service` 技能来查找相应的服务。

## 错误处理

- “未完成身份验证”：请先运行 `awal auth login <email>` 命令进行登录，或参考 `authenticate-wallet` 技能 |
- “未找到支持 X402 支付的 API”：可能是错误的 URL；请使用 `search-for-service` 命令查找正确的 API 端点 |
- “余额不足”：请为钱包充值 USDC（使用 `fund` 技能） |