---
name: recipes
version: 1.0.0
description: "这是一个用于AI代理为其人类用户查找食谱的命令行工具（CLI），它使用了TheMealDB API。该工具无需进行身份验证（即无需登录或提供用户名/密码）。"
homepage: https://www.themealdb.com
metadata:
  openclaw:
    emoji: "🍳"
    requires:
      bins: ["bash", "curl", "jq"]
    tags: ["recipes", "food", "cooking", "meals", "themealdb", "cli"]
---

# 食谱查询

这是一个用于AI代理帮助人类用户查找食谱的命令行工具。例如：“用鸡肉可以做什么菜？”——现在你的代理可以为你提供帮助。

该工具使用了TheMealDB API，无需注册账户或API密钥。

## 使用方法

```
"Search for pasta recipes"
"Give me a random dinner idea"
"What Italian dishes can I make?"
"Tell me about meal ID 52772"
```

## 命令

| 功能 | 命令                |
|--------|-------------------|
| 搜索食谱 | `recipes search "查询内容"`     |
| 查看详情 | `recipes info <食谱ID>`     |
| 随机生成食谱 | `recipes random`       |
| 列出分类 | `recipes categories`     |
| 按地区/菜系筛选 | `recipes area <地区>`     |

### 示例

```bash
recipes search "chicken"          # Find chicken recipes
recipes info 52772                # Get full recipe by ID
recipes random                    # Surprise me!
recipes categories                # List all categories
recipes area Italian              # Italian dishes
recipes area Mexican              # Mexican dishes
```

## 输出结果

**搜索/列表结果：**
```
[52772] Spaghetti Bolognese — Italian, Beef
```

**食谱详情/随机生成结果：**
```
🍽️  Spaghetti Bolognese
   ID: 52772 | Category: Beef | Area: Italian
   Tags: Pasta,Meat

📝 Ingredients:
   • 500g Beef Mince
   • 2 Onions
   • 400g Tomato Puree
   ...

📖 Instructions:
[Full cooking instructions]

🎥 Video: [YouTube URL if available]
📎 Source: [Recipe source if available]
```

## 可用地区（菜系）：

美国菜、英国菜、加拿大菜、中国菜、克罗地亚菜、荷兰菜、埃及菜、菲律宾菜、法国菜、希腊菜、印度菜、爱尔兰菜、意大利菜、牙买加菜、日本菜、肯尼亚菜、马来西亚菜、墨西哥菜、摩洛哥菜、波兰菜、葡萄牙菜、俄罗斯菜、西班牙菜、泰国菜、突尼斯菜、土耳其菜、乌克兰菜、越南菜

## 注意事项：

- 该工具使用TheMealDB的免费API，无需认证。
- 食谱ID是数据库中的唯一标识符。
- 过滤命令（如`recipes area <地区>`）仅返回食谱ID；如需查看详情，请使用`recipes info <食谱ID>`。
- 分类页面会提供食谱的详细描述。

---

## 代理实现说明

**脚本位置：`{skill_folder}/recipes`（实际脚本位于`scripts/recipes`目录下）**

**当用户询问食谱或烹饪相关内容时：**
1. 运行`./recipes search "食材或菜肴名称"`以获取可选食谱。
2. 运行`./recipes info <食谱ID>`以获取包含食材和制作步骤的完整食谱信息。
3. 运行`./recipes random`以获取晚餐灵感。
4. 运行`./recipes area <菜系>`以按菜系筛选食谱。

**工作流程示例：**
```
User: "What can I make for dinner?"
1. recipes random  →  Get a random idea
2. recipes info <id>  →  Full recipe details

User: "I want something Italian"
1. recipes area Italian  →  List Italian dishes
2. recipes info <id>  →  Pick one and get full recipe
```

**不适用场景：**
- 营养信息、热量计算、饮食限制（这些功能不在该工具的API范围内）。