---
name: near-faucet
description: **OpenClaw技能：通过Faucet请求NEAR测试网代币**  
该技能支持发起Faucet请求、检查请求状态以及查询账户余额，并具备速率限制功能（即防止频繁请求导致的系统负担）。
---

# NEAR 测试网代币领取工具

这是一个用于领取 NEAR 测试网代币的简单工具。

## 描述

该工具允许用户通过代币领取请求轻松获取 NEAR 测试网代币，并配备了速率限制机制以防止滥用。

## 主要功能

- 请求 NEAR 测试网代币
- 查查代币领取请求的状态
- 对每个地址实施速率限制
- 提供简单的命令行接口（CLI）命令

## 命令

### `near-faucet request [account_id]`
为指定账户请求 NEAR 测试网代币。

**参数：**
- `account_id` - NEAR 账户 ID（可选，如未配置则使用默认值）

**示例：**
```bash
near-faucet request myaccount.testnet
```

### `near-faucet status [request_id]`
查看代币领取请求的状态。

**参数：**
- `request_id` - 需要查询的请求 ID（可选，省略时显示最新状态）

### `near-faucet balance [account_id]`
查询指定账户的测试网代币余额。

## 配置

您可以通过环境变量或配置文件设置默认账户：

```bash
export NEAR_ACCOUNT="myaccount.testnet"
```

## 安装

该工具会自动安装到您的 OpenClaw 工具目录中。

## 速率限制

- 每个账户每天最多可发起 1 次请求
- 每次请求最多可领取 10 个 NEAR 代币
- 请求处理时间：约 1-5 分钟

## 参考资料

- NEAR 测试网代币领取平台：https://wallet.testnet.near.org/
- NEAR 命令行工具（CLI）：https://docs.near.org/tools/near-cli