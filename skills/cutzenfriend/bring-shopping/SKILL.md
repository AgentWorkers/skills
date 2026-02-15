---
name: bring-shopping
description: 通过非官方的 `bring-shopping` Node.js 库，使用电子邮件/密码登录方式来管理 Bring! 购物清单。该库支持添加购物清单、查看商品信息、添加/删除商品，以及在允许通过 API 访问的情况下对商品进行勾选/取消勾选操作。
---

# Bring Shopping

## 概述

使用 `bring-shopping` npm 包，可以通过电子邮件/密码凭据访问 Bring! 的商品列表。默认列表为 "Willig"，除非用户另有指定。

## 快速入门

1. 在技能文件夹中安装依赖项：
   - `npm install bring-shopping`
2. 在 Clawdbot 配置文件中（推荐）或 shell 中设置环境变量：
   - `BRING_EMAIL` 和 `BRING_PASSWORD`
3. 运行 CLI 脚本：
   - `node scripts/bring_cli.mjs items --list "Willig"`

## 功能

### 显示列表
- `node scripts/bring_cli.mjs lists`

### 显示商品信息
- `node scripts/bring_cli.mjs items --list "Willig"`

### 添加商品
- `node scripts/bring_cli.mjs add --item "Milch" --spec "2L" --list "Willig"`

### 删除商品
- `node scripts/bring_cli.mjs remove --item "Milch" --list "Willig"`

### 检查商品状态
- `node scripts/bring_cli.mjs check --item "Milch" --list "Willig"`

### 取消选中商品
- `node scripts/bring_cli.mjs uncheck --item "Milch" --spec "2L" --list "Willig"`

## 注意事项

- 将凭据存储在 Clawdbot 的配置文件中，以避免随技能一起被分发。
- 如果列表名称不明确，可以运行 `lists` 命令来询问使用哪个列表。
- 如果某件商品已被选中，执行 `uncheck` 命令后，该商品会重新被添加到购买列表中。