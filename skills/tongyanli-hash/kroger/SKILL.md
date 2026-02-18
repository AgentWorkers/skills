---
name: kroger
description: 通过 Kroger API 搜索 Kroger 的商品并将商品添加到用户的 Kroger 购物车中。该功能适用于用户需要查找食品杂货、将商品添加到购物车、查询 Kroger 商店位置或管理购物清单的场景。支持按商品名称搜索、购物车管理以及通过邮政编码查找商店位置。
---
# Kroger

您可以通过Kroger的公共API来搜索产品、将商品添加到购物车以及查找门店位置。

## 先决条件

- 在https://developer.kroger.com上拥有Kroger开发者账户
- 注册一个具有**Product**（产品）和**Cart**（购物车）API访问权限的应用程序
- 在Kroger应用程序设置中配置了OAuth重定向URI

## 环境变量

在使用之前，请设置以下环境变量：

```bash
export KROGER_CLIENT_ID="your-client-id"
export KROGER_CLIENT_SECRET="your-client-secret"
```

可选参数：
- `KROGER_TOKEN_FILE` — 令牌存储路径（默认：`~/.kroger-tokens.json`）
- `KROGER_REDIRECT_URI` — OAuth回调URL（默认：`http://localhost:8888/callback`）
- `KROGER_LOCATION_ID` — 用于根据门店位置查询商品可用性的门店ID

## 设置（一次性操作）

### 1. 注册Kroger开发者应用

1. 访问https://developer.kroger.com
2. 创建一个应用程序
3. 启用**Product**和**Cart**权限
4. 将重定向URI设置为`http://localhost:8888/callback`
5. 记录客户端ID（Client ID）和客户端密钥（Client Secret）

### 2. 进行身份验证

运行身份验证流程——系统会打开浏览器页面，让您登录Kroger：

```bash
scripts/kroger.sh auth
```

如果重定向URI不是`localhost`（例如，托管在云服务器上），请使用手动身份验证流程：
1. 打开`scripts/kroger.sh auth`命令生成的`AUTH_URL`
2. 登录Kroger
3. 复制重定向后的URL（即使页面出现错误也请复制）
4. 提取`code`参数并运行以下命令：

```bash
scripts/kroger.sh exchange <code>
```

令牌会自动更新。只有在令牌过期时才需要重新进行身份验证。

## 功能操作

### 搜索产品

```bash
scripts/kroger.sh search "cannellini beans"
```

最多返回5个产品结果，包括产品ID、描述和品牌信息。

### 将商品添加到购物车

```bash
scripts/kroger.sh add <productId> [quantity]
```

需要先完成OAuth登录。默认购买数量为1件。

### 查找附近的门店

```bash
scripts/kroger.sh locations <zipcode>
```

最多返回5家门店的信息。通过设置`KROGER_LOCATION_ID`可以按门店筛选产品搜索结果。

### 检查身份验证状态

```bash
scripts/kroger.sh token
```

## 工作流程：购物清单 → 购物车

将购物清单添加到Kroger的典型流程如下：
1. 搜索每件商品：`scripts/kroger.sh search "<item>"`
2. 从搜索结果中选择最符合需求的产品
3. 将商品添加到购物车：`scripts/kroger.sh add <productId> <qty>`
4. 对所有商品重复此操作

当需要添加大量商品时，可以先批量搜索所有商品，然后让用户确认选择，最后将所有商品一起添加到购物车中。