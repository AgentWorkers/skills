---
name: managing-groups
description: 用于 XMTP 代理的群组对话管理功能。适用于创建群组、管理成员、设置权限或发送欢迎消息等场景。该功能会在群组创建、成员信息更新或权限调整时被触发。
license: MIT
metadata:
  author: xmtp
  version: "1.0.0"
---

# XMTP 组

用于管理组内对话、权限和成员。

## 适用场景

在以下情况下请参考这些指南：
- 创建新的组内对话
- 管理组成员（添加/删除）
- 设置组权限
- 发送欢迎消息
- 控制组访问权限

## 规则分类（按优先级）

| 优先级 | 分类 | 影响程度 | 前缀 |
|---------|---------|-----------|---------|
| 1      | 创建     | 关键        | `create-`     |
| 2      | 成员     | 高        | `members-`    |
| 3      | 权限     | 高        | `permissions-`   |
| 4      | 欢迎     | 中        | `welcome-`    |

## 快速参考

### 创建（关键）
- `create-group`  - 创建新的组内对话
- `create-dm`  - 创建私信

### 成员（高优先级）
- `members-add`  - 将成员添加到组中
- `members-remove` - 从组中删除成员
- `members-get-address` - 获取成员的以太坊地址

### 权限（高优先级）
- `permissions-roles` - 了解成员、管理员和超级管理员的角色
- `permissions-custom` - 设置自定义权限策略

### 欢迎（中等优先级）
- `welcome-on-install` - 在代理安装时发送欢迎消息
- `welcome-new-members` - 欢迎新加入组的成员

## 快速入门

```typescript
// Create a group
const group = await agent.createGroupWithAddresses(addresses, {
  groupName: "My Group",
  groupDescription: "A cool group",
});

// Welcome on new conversations
agent.on("group", async (ctx) => {
  await ctx.conversation.sendText("Hello group!");
});

agent.on("dm", async (ctx) => {
  await ctx.conversation.sendText("Hello! How can I help?");
});
```

## 使用方法

有关详细说明，请阅读各个规则文件：

```
rules/create-group.md
rules/members-add.md
rules/permissions-roles.md
rules/welcome-on-install.md
```