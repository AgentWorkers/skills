---
name: gumroad-admin
version: 1.0.0
description: Gumroad Admin CLI：用于查看销售数据、管理产品以及调整折扣设置。
author: abakermi
metadata:
  openclaw:
    emoji: "💸"
    requires:
      env: ["GUMROAD_ACCESS_TOKEN"]
---

# Gumroad 管理

通过 OpenClaw 管理您的 Gumroad 商店。

## 设置

1. 从 Gumroad 获取访问令牌（设置 > 高级 > 应用程序）。
2. 将其设置为：`export GUMROAD_ACCESS_TOKEN="your_token"`

## 命令

### 销售
```bash
gumroad-admin sales --day today
gumroad-admin sales --last 30
```

### 产品
```bash
gumroad-admin products
```

### 折扣
```bash
gumroad-admin discounts create --product <id> --code "TWITTER20" --amount 20 --type percent
```