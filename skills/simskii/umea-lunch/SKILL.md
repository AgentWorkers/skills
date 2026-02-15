---
name: umea-lunch
description: 获取乌梅奥（Umeå）当地餐厅的今日午餐菜单。在询问有关午餐、餐厅或乌梅奥食物的信息时可以使用此数据。数据实时更新，来源于 umealunchguide.se 网站。
---

# 乌梅奥午餐指南

通过 umealunchguide.se 获取并显示乌梅奥餐厅的午餐菜单。

## 快速入门

运行脚本以获取当天的菜单：

```bash
python3 /root/clawd/skills/umea-lunch/scripts/fetch_lunch.py
```

### 选项

```bash
# Get menus for a specific date (YYYY-MM-DD)
python3 /root/clawd/skills/umea-lunch/scripts/fetch_lunch.py --date 2026-01-29

# Filter by restaurant name (case-insensitive partial match)
python3 /root/clawd/skills/umea-lunch/scripts/fetch_lunch.py --restaurant tonka

# List all available restaurants
python3 /root/clawd/skills/umea-lunch/scripts/fetch_lunch.py --list

# Combine filters
python3 /root/clawd/skills/umea-lunch/scripts/fetch_lunch.py --date 2026-01-29 --restaurant "o'learys"
```

## 输出格式

脚本会输出包含餐厅信息和午餐菜目的 JSON 数据：

```json
{
  "date": "2026-01-28",
  "restaurants": [
    {
      "name": "Restaurant Name",
      "address": "Street 123",
      "phone": "090-123456",
      "website": "https://...",
      "courses": [
        {
          "title": "Dish Name",
          "description": "Description of the dish",
          "price": "149",
          "tags": ["Vegetarisk", "Glutenfri"]
        }
      ]
    }
  ]
}
```

## 响应指南

在展示午餐选项时，请遵循以下规则：
- 按餐厅进行分类
- 显示菜肴名称、描述和价格
- 标明饮食标签（🥗 素食、🌱 纯素食、🌾 无麸质、🥛 无乳糖）
- 如果用户需要路线指引，请提供餐厅地址