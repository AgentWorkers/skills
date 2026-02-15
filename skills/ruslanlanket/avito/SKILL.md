---
name: avito
description: 通过 API 管理 Avito.ru 账户、商品以及消息功能。可用于发布商品信息、查看账户余额、阅读聊天记录以及获取账户信息。
---

# Avito

本技能提供了用于与 Avito.ru API 进行交互的工具。

## 所需条件

- Python 的 `requests` 库。
- Avito 的客户端 ID（Client ID）和客户端密钥（Client Secret）。

## 设置

请将您的凭据设置到环境中，或在系统提示时提供这些凭据。

## 功能

### 认证

使用您的客户端凭据获取访问令牌。

```bash
python3 scripts/auth.py <client_id> <client_secret>
```

### 账户信息

获取有关您的账户的信息，包括您的 `user_id`。

```bash
python3 scripts/get_self.py <token>
```

### 账户余额

查看您的账户余额。

```bash
python3 scripts/get_balance.py <token> <user_id>
```

### 商品管理

列出您当前发布的广告。

```bash
python3 scripts/list_items.py <token>
```

### 消息系统（Messenger）

列出您账户中的聊天记录。

```bash
python3 scripts/list_chats.py <token> <user_id>
```

*注意：使用消息系统 API 可能需要订阅 Avito 的特定服务。*

## 待办事项

- 实现商品创建功能（POST /items）。
- 实现商品状态更新功能（编辑、删除）。
- 实现 Webhook 注册功能。
- 实现消息发送和接收功能。