---
name: grocery-list
description: 独立的购物清单、食谱和膳食计划功能，支持本地数据存储，无需依赖任何外部服务。
homepage: https://clawdhub.com/skills/grocery-list
metadata: { "clawdbot": { "emoji": "🛒", "requires": { "bins": ["uv"] } } }
---

# 购物清单与餐食规划工具

这是一个功能齐全的购物清单、食谱及餐食规划工具，支持使用本地的 JSON 数据存储方式，无需订阅任何外部服务。

## 主要功能

- **多份清单**：可创建针对不同购物渠道（如 Costco、Target 等）的清单。
- **智能分类**：食材被自动分类为“农产品”、“乳制品”、“肉类”、“烘焙食品”、“冷冻食品”、“食品储藏室”等类别。
- **数量解析**：例如，“2 加仑牛奶”会被解析为数量 2，单位为“加仑”。
- **食谱保存**：用户可以保存包含食材信息的食谱。
- **餐食规划**：可根据日期和餐食类型（早餐/午餐/晚餐）来规划餐食。
- **食谱导入清单**：只需一条命令即可将食谱中的食材添加到相应的购物清单中。
- **家庭成员分配**：用户可以为家庭成员分配需要购买的食材。
- **通知功能**：支持通过 `notify` 命令实现心跳信号或定时任务的集成。

## 命令说明

### 列表管理

```bash
uv run {baseDir}/scripts/grocery.py lists                    # Show all lists
uv run {baseDir}/scripts/grocery.py list "Grocery"           # Show items in a list
uv run {baseDir}/scripts/grocery.py list "Grocery" --unchecked
uv run {baseDir}/scripts/grocery.py list create "Costco"     # Create new list
uv run {baseDir}/scripts/grocery.py list delete "Costco"     # Delete a list
```

### 食材管理

```bash
uv run {baseDir}/scripts/grocery.py add "Grocery" "Milk"
uv run {baseDir}/scripts/grocery.py add "Grocery" "Milk" --category dairy --qty "2 gallons"
uv run {baseDir}/scripts/grocery.py add "Grocery" "Chicken" --assignee "Erin"
uv run {baseDir}/scripts/grocery.py check "Grocery" "Milk"
uv run {baseDir}/scripts/grocery.py uncheck "Grocery" "Milk"
uv run {baseDir}/scripts/grocery.py remove "Grocery" "Milk"
uv run {baseDir}/scripts/grocery.py clear "Grocery"          # Clear checked items
```

### 食谱管理

```bash
uv run {baseDir}/scripts/grocery.py recipes                  # List all recipes
uv run {baseDir}/scripts/grocery.py recipe "Tacos"           # View a recipe
uv run {baseDir}/scripts/grocery.py recipe add "Tacos" --ingredients "ground beef,tortillas,cheese,lettuce,tomatoes"
uv run {baseDir}/scripts/grocery.py recipe add "Tacos" --category "Mexican" --servings 4
uv run {baseDir}/scripts/grocery.py recipe delete "Tacos"
uv run {baseDir}/scripts/grocery.py recipe search "chicken"
```

### 餐食规划

```bash
uv run {baseDir}/scripts/grocery.py meals                    # Show this week's meals
uv run {baseDir}/scripts/grocery.py meals --date 2026-01-15
uv run {baseDir}/scripts/grocery.py meal add --date 2026-01-15 --type dinner --recipe "Tacos"
uv run {baseDir}/scripts/grocery.py meal add-to-list --date 2026-01-15 --list "Grocery"
uv run {baseDir}/scripts/grocery.py meal remove --date 2026-01-15 --type dinner
```

### 通知功能

```bash
uv run {baseDir}/scripts/grocery.py notify                   # Pending alerts for heartbeat
uv run {baseDir}/scripts/grocery.py stats                    # Quick summary
```

## 自动分类功能

系统内置了以下分类，并能自动识别食材类别：

- **农产品**：水果、蔬菜
- **乳制品**：牛奶、奶酪、鸡蛋、酸奶
- **肉类**：鸡肉、牛肉、猪肉、鱼类
- **烘焙食品**：面包、卷饼、百吉饼
- **冷冻食品**：冰淇淋、冷冻餐食
- **食品储藏室**：罐头食品、意大利面、大米
- **饮料**：饮品、汽水、果汁
- **零食**：薯片、饼干
- **家居用品**：清洁用品、纸制品
- **个人用品**：洗漱用品、药品
- **其他**：未分类的食材

## JSON 数据输出

所有命令都支持使用 `--json` 选项以编程方式访问数据：

```bash
uv run {baseDir}/scripts/grocery.py list "Grocery" --json
uv run {baseDir}/scripts/grocery.py recipes --json
uv run {baseDir}/scripts/grocery.py meals --json
```

## 数据存储方式

数据存储在本地文件 `~/.clawdbot/grocery-list/data.json` 中，无需使用云存储服务。

## 使用示例

- **将牛奶和鸡蛋添加到购物清单中**：  
  ```bash
uv run {baseDir}/scripts/grocery.py add "Grocery" "Milk" --category dairy
uv run {baseDir}/scripts/grocery.py add "Grocery" "Eggs" --category dairy
```

- **查看购物清单上的物品**：  
  ```bash
uv run {baseDir}/scripts/grocery.py list "Grocery" --unchecked
```

- **规划周六的晚餐（墨西哥卷饼）**：  
  ```bash
uv run {baseDir}/scripts/grocery.py meal add --date 2026-01-18 --type dinner --recipe "Tacos"
```

- **将墨西哥卷饼的食材添加到购物清单中**：  
  ```bash
uv run {baseDir}/scripts/grocery.py meal add-to-list --date 2026-01-18 --list "Grocery"
```

- **标记已购买的牛奶**：  
  ```bash
uv run {baseDir}/scripts/grocery.py check "Grocery" "Milk"
```