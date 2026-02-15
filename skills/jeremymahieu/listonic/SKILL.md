---
name: listonic
version: 1.0.0
description: "访问 Listonic 购物清单：查看清单中的商品、添加/勾选/删除商品以及管理清单。"
metadata: {"clawdbot":{"emoji":"🛒","requires":{"bins":["python3"]}}}
---

# Listonic

通过非官方的Web API管理Listonic购物清单。

## 设置

使用**一种**认证方式创建`~/.openclaw/credentials/listonic/config.json`文件。

### 推荐方式：令牌认证（支持Google登录）

```json
{
  "refreshToken": "your-refresh-token"
}
```

（可选，高级功能：）

```json
{
  "accessToken": "short-lived-access-token",
  "clientId": "listonicv2",
  "clientSecret": "fjdfsoj9874jdfhjkh34jkhffdfff",
  "redirectUri": "https://listonicv2api.jestemkucharzem.pl"
}
```

### 备用方式：邮箱/密码认证

```json
{
  "email": "you@example.com",
  "password": "your-listonic-password"
}
```

## 工作流程

1. `lists`：显示可用的购物清单
2. `items <list>`：查看当前清单中的商品
3. `add-item <list> "名称"`：向清单中添加商品
4. `check-item` / `uncheck-item`：切换商品的完成状态
5. `delete-item`：仅在用户明确要求删除时执行删除操作

## 重要提示

- 本工具使用的是**非官方的逆向工程API**，如果Listonic对其进行了修改，功能可能会失效。
- 对于具有破坏性的操作（如`delete-item`、`delete-list`），请务必先获得用户的确认。
- `list`参数可以是清单ID或清单名称（支持完全匹配或部分匹配）。

## 命令

### 显示所有清单
```bash
bash scripts/listonic.sh lists
```

### 显示清单中的商品
```bash
bash scripts/listonic.sh items 12345
bash scripts/listonic.sh items "Groceries"
```

### 添加商品
```bash
bash scripts/listonic.sh add-item "Groceries" "Milk"
bash scripts/listonic.sh add-item "Groceries" "Flour" --amount 2 --unit kg
```

### 切换商品的完成状态
```bash
bash scripts/listonic.sh check-item "Groceries" 987654
bash scripts/listonic.sh uncheck-item "Groceries" 987654
```

### 删除商品
```bash
bash scripts/listonic.sh delete-item "Groceries" 987654
```

### 创建/重命名/删除清单
```bash
bash scripts/listonic.sh add-list "BBQ Party"
bash scripts/listonic.sh rename-list "BBQ Party" "BBQ"
bash scripts/listonic.sh delete-list "BBQ"
```

### 原始JSON输出
```bash
bash scripts/listonic.sh --json lists
bash scripts/listonic.sh --json items "Groceries"
```