---
name: near-name-service
description: 管理 NEAR 名称服务（.near 域名）：检查域名可用性、进行注册、解析以及管理域名相关操作。
---

# NEAR 域名服务技能

轻松管理 `.near` 域名。

## 描述

该技能提供了一个命令行界面（CLI），用于与 NEAR 域名服务进行交互。您可以查询域名是否可用、注册新域名、将域名解析到对应的账户信息，以及管理您拥有的 `.near` 域名。

## 功能

- 查询 `.near` 域名的可用性
- 注册一个新的 `.near` 域名
- 将 `.near` 域名解析到对应的账户 ID
- 列出您拥有的所有 `.near` 域名
- 简单易用的命令行界面

## 命令

### `near-name check <name>`
检查指定的 `.near` 域名是否可用。

**参数：**
- `name` - 域名（不包含 `.near` 后缀）

**示例：**
```bash
near-name check mydomain
```

### `near-name register <name> [account_id]`
注册一个新的 `.near` 域名。

**参数：**
- `name` - 域名（不包含 `.near` 后缀）
- `account_id` - 要注册域名的账户 ID（可选，使用默认值）

**示例：**
```bash
near-name register mydomain myaccount.near
```

### `near-name resolve <name>`
将指定的 `.near` 域名解析到其对应的账户 ID。

**参数：**
- `name` - 需要解析的域名

**示例：**
```bash
near-name resolve mydomain.near
```

### `near-name list [account_id]`
列出某个账户拥有的所有 `.near` 域名。

**参数：**
- `account_id` - 要列出域名的账户 ID（可选，使用默认值）

## 配置

设置您的默认账户：
```bash
export NEAR_ACCOUNT="myaccount.near"
```

## 价格

- 注册费用：约 5-10 NEAR（价格因域名长度而异）
- 年度续费费用：约 0.1 NEAR
- 更短的域名（少于 4 个字符）价格更高

## 参考资料

- NEAR 域名服务：https://near.org/names/
- 域名注册协议：naming.near
- NEAR 命令行工具：https://docs.near.org/tools/near-cli