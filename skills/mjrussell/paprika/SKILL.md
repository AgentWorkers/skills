---
name: paprika
description: 您可以从 Paprika Recipe Manager 中获取食谱、膳食计划和购物清单。当用户询问有关食谱、膳食规划或烹饪的问题时，可以使用这些信息。
homepage: https://www.paprikaapp.com
metadata:
  clawdbot:
    emoji: "📖"
    requires:
      bins: ["paprika"]
---

# Paprika Recipe CLI

Paprika Recipe Manager 的命令行界面（CLI）。用于访问食谱、膳食计划和购物清单。

## 安装

```bash
npm install -g paprika-recipe-cli
```

## 设置

```bash
# Authenticate interactively
paprika auth

# Or set environment variables
export PAPRIKA_EMAIL="your@email.com"
export PAPRIKA_PASSWORD="your-password"
```

## 命令

### 食谱

```bash
paprika recipes                       # List all recipes
paprika recipes --category "Dinner"   # Filter by category
paprika recipes --json

paprika recipe "Pasta Carbonara"      # View by name
paprika recipe <uid>                  # View by UID
paprika recipe "Pasta" --ingredients-only
paprika recipe "Pasta" --json

paprika search "chicken"              # Search recipes
```

### 膳食计划

```bash
paprika meals                         # Show all planned meals
paprika meals --date 2026-01-08       # Filter by date
paprika meals --json
```

### 购物清单

```bash
paprika groceries                     # Show unpurchased items
paprika groceries --all               # Include purchased
paprika groceries --json
```

### 分类

```bash
paprika categories                    # List all categories
```

## 使用示例

**用户：“我有哪些晚餐食谱？”**
```bash
paprika recipes --category "Dinner"
```

**用户：“显示意大利面碳ara 食谱。”**
```bash
paprika recipe "Pasta Carbonara"
```

**用户：“制作千层面需要哪些食材？”**
```bash
paprika recipe "Lasagna" --ingredients-only
```

**用户：“我的膳食计划里有什么？”**
```bash
paprika meals
```

**用户：“我的购物清单里有什么？”**
```bash
paprika groceries
```

**用户：“查找鸡肉食谱。”**
```bash
paprika search "chicken"
```

## 注意事项

- 食谱名称支持部分匹配
- 使用 `--json` 进行程序化访问
- 需要启用 Paprika 的云同步功能