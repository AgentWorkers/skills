---
name: anylist
description: 通过 AnyList 管理购物清单和待购商品。当用户询问购物清单、所需购买的物品或需要添加/勾选待购项时，可以使用该功能。
homepage: https://www.anylist.com
metadata:
  clawdbot:
    emoji: "🛒"
    requires:
      bins: ["anylist"]
---

# AnyList CLI

通过 AnyList 管理购物清单。

## 安装

```bash
npm install -g anylist-cli
```

## 设置

```bash
# Authenticate interactively
anylist auth

# Or set environment variables for non-interactive use
export ANYLIST_EMAIL="your@email.com"
export ANYLIST_PASSWORD="your-password"
```

## 命令

### 列表操作

```bash
anylist lists              # Show all lists
anylist lists --json       # Output as JSON
```

### 商品信息

```bash
anylist items "Grocery"              # Show items in a list
anylist items "Grocery" --unchecked  # Only unchecked items
anylist items "Grocery" --json       # Output as JSON
```

### 添加商品

```bash
anylist add "Grocery" "Milk"
anylist add "Grocery" "Milk" --category dairy
anylist add "Grocery" "Chicken" --category meat --quantity "2 lbs"
```

**分类：** 食品、肉类、海鲜、乳制品、面包、冷冻食品、罐头食品、调味品、饮料、零食、意大利面、米饭、谷物、早餐食品、烘焙食品、香料、家居用品、个人护理用品、其他

### 商品管理

```bash
anylist check "Grocery" "Milk"      # Mark as checked
anylist uncheck "Grocery" "Milk"    # Mark as unchecked
anylist remove "Grocery" "Milk"     # Remove from list
anylist clear "Grocery"             # Clear all checked items
```

## 使用示例

**用户：“购物清单上有什么？”**
```bash
anylist items "Grocery" --unchecked
```

**用户：“在购物清单中添加牛奶和鸡蛋”**
```bash
anylist add "Grocery" "Milk" --category dairy
anylist add "Grocery" "Eggs" --category dairy
```

**用户：“勾选‘面包’这一项”**
```bash
anylist check "Grocery" "Bread"
```

**用户：“添加制作墨西哥卷饼所需的食材”**
```bash
anylist add "Grocery" "Ground beef" --category meat
anylist add "Grocery" "Taco shells" --category other
anylist add "Grocery" "Lettuce" --category produce
anylist add "Grocery" "Tomatoes" --category produce
anylist add "Grocery" "Cheese" --category dairy
```

## 注意事项

- 列表名称和商品名称不区分大小写
- 如果某项商品已经存在于清单中，再次添加该商品会将其从清单中移除（这对于制作食谱非常有用）
- 使用 `--json` 参数可进行脚本编写或程序化操作