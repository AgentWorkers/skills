---
name: structs-diplomacy
description: 在Structs中，该模块负责处理权限管理、地址分配以及玩家之间的协作。适用于以下场景：授予或撤销对象的权限、注册新地址、管理多地址账户、将权限委托给其他玩家，以及设置基于地址的访问控制规则。
---
# Diplomacy 模块的结构与功能

**重要提示**：包含破折号（如 `3-1`、`4-5`）的实体 ID 会被 CLI 解析器误认为是标志（flags）。因此，在使用与该模块相关的所有交易命令时，必须在位置参数前添加 `--` 以明确指定参数的类型。

## 操作流程

1. **查询权限**：`structsd query structs permission [id]`、`permission-by-object [object-id]`、`permission-by-player [player-id]`
2. **授予对象权限**：`structsd tx structs permission-grant-on-object TX_FLAGS -- [object-id] [player-id] [permissions]`（权限是可叠加的）
3. **撤销对象权限**：`structsd tx structs permission-revoke-on-object -- [object-id] [player-id] [permissions]`
4. **设置对象权限**：`structsd tx structs permission-set-on-object -- [object-id] [player-id] [permissions]`（会覆盖现有权限并应用新权限）
5. **地址级权限**：`structsd tx structs permission-grant-on-address -- [address] [permissions]`、`permission-revoke-on-address -- [address] [permissions]`、`permission-set-on-address -- [address] [permissions]`
6. **地址管理**：
   - 注册地址：`structsd tx structs address-register TX_FLAGS -- [player-id] [address] [proof-pubkey] [proof-signature] [permissions]`
   - 撤销地址：`structsd tx structs address-revoke -- [address]`
   - 更改玩家的主地址：`structsd tx structs player-update-primary-address -- [player-id] [new-address]`

## 命令参考

| 功能 | 命令                |
|--------|-------------------|
| 授予对象权限 | `structsd tx structs permission-grant-on-object -- [object-id] [player-id] [permissions]` |
| 撤销对象权限 | `structsd tx structs permission-revoke-on-object -- [object-id] [player-id] [permissions]` |
| 设置对象权限 | `structsd tx structs permission-set-on-object -- [object-id] [player-id] [permissions]` |
| 授予地址权限 | `structsd tx structs permission-grant-on-address -- [address] [permissions]` |
| 撤销地址权限 | `structsd tx structs permission-revoke-on-address -- [address] [permissions]` |
| 设置地址权限 | `structsd tx structs permission-set-on-address -- [address] [permissions]` |
| 注册地址 | `structsd tx structs address-register -- [player-id] [address] [proof-pubkey] [proof-signature] [permissions]` |
| 撤销地址 | `structsd tx structs address-revoke -- [address]` |
| 更改玩家的主地址 | `structsd tx structs player-update-primary-address -- [player-id] [new-address]` |

**TX_FLAGS**：`--from [key-name] --gas auto --gas-adjustment 1.5 -y`

## 其他查询命令

| 功能 | 命令                |
|--------|-------------------|
| 按 ID 查询权限 | `structsd query structs permission [id]` |
| 按对象查询权限 | `structsd query structs permission-by-object [object-id]` |
| 按玩家查询权限 | `structsd query structs permission-by-player [player-id]` |
| 查询地址信息 | `structsd query structs address [address]` |
| 查询玩家拥有的所有地址 | `structsd query structs address-all-by-player [player-id]` |

## 验证机制

- **权限验证**：`structsd query structs permission-by-object [object-id]`（列出具有该对象访问权限的玩家）
- **地址验证**：`structsd query structs address [address]`（验证地址的注册状态及玩家关联关系）
- **查询玩家的所有地址**：`structsd query structs address-all-by-player [player-id]`（获取玩家拥有的所有地址）

## 错误处理

- **权限错误**：签名者没有访问该对象的权限。请使用 `permission-by-object` 命令检查当前拥有的权限。
- **地址已注册**：请先使用 `address-revoke` 命令撤销现有权限，或将该地址关联到其他玩家。
- **验证失败**：地址注册需要有效的公钥（proof pubkey）和签名（signature）。请检查授权流程是否正确。
- **对象未找到**：可能是对象 ID 已过期，请重新查询以确认对象是否存在。

## 相关文档

- [knowledge/entities/entity-relationships](https://structs.ai/knowledge/entities/entity-relationships)：对象类型与 ID 的相关信息
- [protocols/authentication](https://structs.ai/protocols/authentication)：地址注册的授权机制