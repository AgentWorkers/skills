---
name: go4me
description: 通过 Go4Me 的地址查询功能，将 XCH（Chia 的货币单位）发送给 Twitter 用户。该功能适用于以下场景：通过用户的 Twitter 账号名称向其发送 XCH、查询用户的 XCH 地址，或在 Go4Me 上给用户打赏。相关指令包括：“send XCH to @user”、“tip @user”、“lookup @user on go4me”以及“what's @user's XCH address”。
---

# Go4Me 技能

通过解析 Twitter 用户的 Go4Me 地址，向他们发送 XCH（Go4Me 的货币）。

## 依赖项

- **sage-wallet** — 用于 XCH 交易

## 命令

| 命令 | 描述 |
|---------|-------------|
| `/go4me lookup <user>` | 获取用户的 XCH 地址和个人信息 |
| `/go4me send <user> <amount>` | 向用户发送 XCH（金额单位为 XCH 或 mojo） |
| `/go4me tip <user>` | 向用户发送 1 mojo 的小费 |

## 自然语言表达

- “向 @hoffmang 发送 1 XCH”
- “给 @sage_wallet 送点小费”
- “@bramcohen 的 XCH 地址是什么？”
- “在 Go4Me 上查找 DracattusDev”

## 查找用户地址的脚本

```bash
source scripts/go4me-lookup.sh
go4me_lookup "DracattusDev"  # Returns JSON or exits 1
```

## 工作流程

### 查找用户信息

1. 如果用户名中包含 `@`，则将其删除。
2. 运行 `go4me_lookup "<username>"` 命令。
3. 解析 JSON 响应中的 `xchAddress`、`fullName` 和 `username` 字段。
4. 如果返回的退出代码为 1，说明该用户不存在于 Go4Me 上。

### 发送 XCH

1. 如上所述，先查找用户信息。
2. 如果找不到用户，输出错误信息。
3. 显示确认信息：
   ```
   Send <amount> to @<username> (<fullName>)?
   Address: <xchAddress>
   [Yes] [No]
   ```
4. 确认后，调用 sage-wallet 的 `send_xch` 函数发送 XCH：
   ```bash
   curl -s --cert $CERT --key $KEY -X POST https://127.0.0.1:9257/send_xch \
     -H "Content-Type: application/json" \
     -d '{"address":"<xchAddress>","amount":"<mojos>","fee":"0","memos":[],"auto_submit":true}'
   ```
5. 显示交易结果。

### 发送小费

与发送 XCH 的命令相同，只是金额设置为 1 mojo。

## 金额转换

| 输入 | Mojos |
|-------|-------|
| `1`（无单位） | 1 mojo |
| `1 mojo` | 1 |
| `0.001 XCH` | 1000000000 |
| `1 XCH` | 1000000000000 |

**金额解析规则**：
- 如果金额中包含 “XCH”，则将其转换为 mojo（`XCH × 10^12`）。
- 对于较小的金额，默认单位为 mojo；对于较大的金额，默认单位为 XCH。

## 错误处理

| 错误类型 | 显示信息 |
|-----------|----------|
| 用户不存在于 Go4Me | “用户 @{username} 不存在于 Go4Me 上” |
| XCH 地址无效 | “从 Go4Me 返回的 XCH 地址无效” |
| 账户余额不足 | “账户余额不足，无法完成交易” |
| 网络错误 | “无法连接到 Go4Me” |

## 可用的数据字段

| 字段 | 示例值 |
|-------|---------|
| `username` | DracattusDev |
| `fullName` | 🌱Drac 🍊 |
| `xchAddress` | xch1rvgc3naytvzhv4lxhzphrdr2fzj2ka340tdj8fflt4872t2wqveq9lwz7t |
| `description` | 用户简介 |
| `avatarUrl` | 用户头像链接 |
| `totalBadgeScore` | 220 |