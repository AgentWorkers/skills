---
name: xmtp-cli-permissions
description: 通过 XMTP CLI 管理组权限。适用于列出、检查或更新组权限的操作。
license: MIT
metadata:
  author: xmtp
  version: "1.0.0"
---

# 命令行界面（CLI）权限

用于列出成员及其权限、获取组信息或更新组权限。

## 适用场景

- 列出某个组的成员及其权限
- 获取组的详细信息
- 更新权限规则（例如：更新元数据、仅限管理员操作）

## 规则

- `list-info`：用于列出组的权限信息（`permissions list`）或获取组的详细权限信息（`permissions info`），需要提供组 ID。
- `update-permissions`：用于更新组的权限设置（`permissions update-permissions`），需要指定要修改的权限和功能。

## 快速入门

```bash
xmtp permissions list --group-id <id>
xmtp permissions info --group-id <id>
xmtp permissions update-permissions --group-id <id> --features update-metadata --permissions admin-only
```

详情请参阅 `rules/list-info.md` 和 `rules/update-permissions.md` 文件。