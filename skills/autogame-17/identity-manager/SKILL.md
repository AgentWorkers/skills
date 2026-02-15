---
name: identity-manager
description: 严格管理用户身份映射（Feishu OpenID ↔ 名称/角色）。在回复之前，可以使用此功能通过用户ID来查找用户信息；或者在数据库中注册新用户。这样可以避免用户身份的混淆或错误识别。
---

# 身份管理器

这是一个专门用于存储和检索用户身份信息的工具。

## 使用方法

### 1. 根据ID查找用户
查询发送消息的用户。
```bash
node skills/identity-manager/index.js lookup "ou_cdc63fe05e88c580aedead04d851fc04"
# Output: { "name": "张昊阳", "role": "Master", "alias": "zhy" }
```

### 2. 注册/更新用户
创建新用户或更新现有用户的资料。
```bash
node skills/identity-manager/index.js register \
  --id "ou_..." \
  --name "李四" \
  --role "Guest" \
  --alias "Lisi"
```

### 3. 列出所有用户
显示所有用户的信息。
```bash
node skills/identity-manager/index.js list
```

### 4. 自动扫描（全局发现）
扫描所有已加入的群组聊天，并自动注册所有成员。
```bash
node skills/identity-manager/auto_scan.js
```

## 数据存储
数据存储在 `memory/userRegistry.json` 文件中。