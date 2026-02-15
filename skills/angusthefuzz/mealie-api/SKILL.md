---
name: mealie
description: 与Mealie食谱管理器进行交互（包括管理食谱、购物清单和制定饮食计划）。这是一个自托管的食谱及饮食计划管理API客户端。
metadata:
  openclaw:
    emoji: 🍳
    requires:
      bins: [node]
      env: [MEALIE_URL, MEALIE_API_TOKEN]
---
# Mealie Skill

这是一个用于 [Mealie](https://mealie.io) 的 API 客户端。Mealie 是一个自托管的食谱管理器和饮食计划工具，可以帮助用户管理食谱、购物清单和饮食计划。

## 环境变量

请将这些变量设置到您的代理程序的 `.env` 文件中（路径：`~/.openclaw/.env`），或者在 `~/.openclaw/skills/mealie/` 目录下创建一个专门用于此技能的 `.env` 文件：

- `MEALIE_URL` — 您的 Mealie 实例 URL（例如：`https://recipes.example.com`）
- `MEALIE_API_TOKEN` — 您的 API 令牌（在 Mealie 的 `/user/profile/api-tokens` 页面上生成）

该脚本仅从 `.env` 文件中读取 `MEALIE_URL` 和 `MEALIE_API_TOKEN` 变量；其他变量将被忽略。

## 获取 API 令牌

1. 登录到您的 Mealie 实例。
2. 转到用户个人资料 → API 令牌。
3. 创建一个具有描述性名称的新令牌。
4. 将生成的令牌复制到您的 `.env` 文件中。

## 命令

### 食谱管理
```bash
node ~/.openclaw/skills/mealie/scripts/mealie.js recipes              # List all recipes
node ~/.openclaw/skills/mealie/scripts/mealie.js recipe <slug>        # Get recipe details
node ~/.openclaw/skills/mealie/scripts/mealie.js search "query"       # Search recipes
node ~/.openclaw/skills/mealie.js create-recipe <url>                 # Import recipe from URL
node ~/.openclaw/skills/mealie.js delete-recipe <slug>                # Delete recipe
```

### 购物清单管理
```bash
node ~/.openclaw/skills/mealie/scripts/mealie.js lists                # List shopping lists
node ~/.openclaw/skills/mealie.js list <id>                           # Show list items
node ~/.openclaw/skills/mealie.js add-item <listId> "item" [qty]      # Add item
node ~/.openclaw/skills/mealie.js check-item <listId> <itemId>        # Mark checked
node ~/.openclaw/skills/mealie.js uncheck-item <listId> <itemId>      # Mark unchecked
node ~/.openclaw/skills/mealie.js delete-item <listId> <itemId>       # Delete item
```

### 饮食计划管理
```bash
node ~/.openclaw/skills/mealie/scripts/mealie.js mealplan [days]      # Show meal plan (default 7 days)
node ~/.openclaw/skills/mealie.js add-meal <date> <recipeSlug> [meal] # Add meal to plan
node ~/.openclaw/skills/mealie.js delete-meal <planId>                # Remove meal from plan
```

### 其他功能
```bash
node ~/.openclaw/skills/mealie.js stats                               # Show statistics
node ~/.openclaw/skills/mealie.js tags                                # List all tags
node ~/.openclaw/skills/mealie.js categories                          # List all categories
```

## 示例用法
```bash
# List all recipes
node ~/.openclaw/skills/mealie/scripts/mealie.js recipes

# Search for pasta recipes
node ~/.openclaw/skills/mealie/scripts/mealie.js search "pasta"

# Get a specific recipe
node ~/.openclaw/skills/mealie/scripts/mealie.js recipe spaghetti-carbonara

# Add milk to shopping list
node ~/.openclaw/skills/mealie/scripts/mealie.js add-item abc123 "Milk" "1 gallon"

# Show this week's meal plan
node ~/.openclaw/skills/mealie/scripts/mealie.js mealplan 7

# Add a recipe to Tuesday's dinner
node ~/.openclaw/skills/mealie/scripts/mealie.js add-meal 2026-02-17 chicken-tacos dinner
```

## API 详细信息

- 该客户端使用承载式令牌（Bearer token）进行身份验证。
- 所有 API 端点均位于 `/api/` 目录下。
- 列表相关的 API 支持分页功能（使用 `--page` 和 `--per-page` 参数）。
- 食谱的标识符采用易于识别的字符串格式（例如：`spaghetti-carbonara`）。

本技能的实现基于 [Mealie 的 API 文档](https://docs.mealie.io)。