---
name: picnic
description: 在 Picnic 超市订购食品杂货：搜索产品、管理购物车、安排配送。
---

# 野餐食品杂货订购

使用 `picnic` 命令行工具（CLI）来搜索产品、管理购物车，并从 Picnic 网站订购食品杂货。

## 设置（仅需执行一次）

```bash
cd {baseDir} && npm install
```

然后登录：
```bash
node {baseDir}/picnic-cli.mjs login <email> <password> DE
```

如果需要两步验证（2FA）：
```bash
node {baseDir}/picnic-cli.mjs verify-2fa <code>
```

## 命令

所有命令的输出格式为 JSON。可以在任意目录下运行这些命令：

```bash
# Check login status
node {baseDir}/picnic-cli.mjs status

# Search for products
node {baseDir}/picnic-cli.mjs search "Milch"
node {baseDir}/picnic-cli.mjs search "Bio Eier"

# View cart
node {baseDir}/picnic-cli.mjs cart

# Add to cart (productId from search results)
node {baseDir}/picnic-cli.mjs add <productId> [count]

# Remove from cart
node {baseDir}/picnic-cli.mjs remove <productId> [count]

# Clear cart
node {baseDir}/picnic-cli.mjs clear

# Get available delivery slots
node {baseDir}/picnic-cli.mjs slots

# Select a delivery slot
node {baseDir}/picnic-cli.mjs set-slot <slotId>

# View delivery history
node {baseDir}/picnic-cli.mjs deliveries

# Get user info
node {baseDir}/picnic-cli.mjs user

# Browse categories
node {baseDir}/picnic-cli.mjs categories
```

## 典型的订购流程

1. 搜索产品：`search "bananas"`（搜索“香蕉”）
2. 添加商品到购物车：`add s1234567 2`（将商品 `s1234567` 添加到购物车，数量为 2 件）
3. 查看购物车内容：`cart`（查看购物车中的商品）
4. 查看可用的配送时间：`slots`（查看可用的配送时间段）
5. 选择配送时间：`set-slot <slotId>`（选择指定的配送时间）
6. 在最终结账前请务必与用户确认（实际结账操作需要在 Picnic 应用程序中完成）

## 注意事项

- 配置信息存储在 `~/.config/picnic/config.json` 文件中
- 国家代码：`DE`（德国）或 `NL`（荷兰）
- 产品编号以字母 `s` 开头（例如：`s1234567`）
- 在修改购物车内容或选择配送时间之前，务必先与用户确认
- 最终的结账/支付操作必须在 Picnic 应用程序中完成