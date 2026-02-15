---
name: near-subaccount
description: 创建、列出、删除和管理 NEAR 子账户，并支持批量分发操作。
---

# NEAR子账户管理技能

轻松创建和管理NEAR子账户。

## 说明

该技能提供了用于创建、列出和删除NEAR子账户的工具，同时支持批量操作，以便将NEAR代币分配给多个子账户。

## 功能

- 创建子账户
- 列出某个账户下的所有子账户
- 删除子账户
- 批量将NEAR代币分配给多个子账户
- 支持简洁的命令行界面

## 命令

### `near-subaccount create <subaccount_name> [master_account]`
创建一个新的子账户。

**参数：**
- `subaccount_name` - 子账户的名称（不含 `.master.account` 后缀）
- `master_account` - 主账户（可选，使用默认值）

**示例：**
```bash
near-subaccount create wallet myaccount.near
# Creates: wallet.myaccount.near
```

### `near-subaccount list [account_id]`
列出某个账户下的所有子账户。

**参数：**
- `account_id` - 需要列出子账户的账户ID（可选，使用默认值）

**示例：**
```bash
near-subaccount list myaccount.near
```

### `near-subaccount delete <subaccount_id> [master_account]`
删除一个子账户。

**参数：**
- `subaccount_id` - 要删除的子账户的完整ID
- `master_account` - 主账户（可选，使用默认值）

### `near-subaccount distribute <file.json> [amount]`
从主账户批量将NEAR代币分配给JSON文件中列出的子账户。

**参数：**
- `file.json` - 包含子账户列表的JSON文件
- `amount` - 每个子账户应接收的NEAR代币数量（默认值：0.1）

**JSON格式示例：**
```json
{
  "subaccounts": [
    "wallet1.myaccount.near",
    "wallet2.myaccount.near",
    "wallet3.myaccount.near"
  ]
}
```

## 配置

设置您的默认账户：
```bash
export NEAR_ACCOUNT="myaccount.near"
```

## 前提条件

- 已安装并配置了NEAR CLI
- 主账户拥有足够的余额用于创建子账户（每个子账户至少需要0.1 NEAR）

## 参考资料

- NEAR CLI：https://docs.near.org/tools/near-cli
- 子账户文档：https://docs.near.org/concepts/account/subaccounts