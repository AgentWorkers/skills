---
name: tandoor-recipes
description: 在 Tandoor Recipe Manager 中，您可以管理食谱、膳食计划和购物清单。当用户需要创建新食谱、规划饮食、搜索现有食谱或管理自己的购物清单时，可以使用该工具。
metadata: { "openclaw": { "emoji": "🍽️", "requires": { "bins": ["node"], "env": ["TANDOOR_URL", "TANDOOR_API_TOKEN"] }, "primaryEnv": "TANDOOR_API_TOKEN" } }
---

# Tandoor 食谱管理器

用户可以通过 Tandoor 食谱管理器来管理食谱、膳食计划和购物清单。

## 使用方法

**所需环境变量：** `TANDOOR_URL`（Tandoor 服务端地址）和 `TANDOOR_API_TOKEN`  

```bash
node ./scripts/tandoor.js <command> [args...]
```

---

## 功能介绍

### 🔍 查找食谱

**按名称搜索：**
```bash
node ./scripts/tandoor.js search-recipes "pasta"
node ./scripts/tandoor.js search-recipes "chicken" 20  # limit to 20 results
```

**查看完整食谱详情：**
```bash
node ./scripts/tandoor.js get-recipe 42
```

---

### 📅 膳食计划

**查看可用的餐食类型（早餐、午餐、晚餐等）：**
```bash
node ./scripts/tandoor.js get-meal-types
```

**将食谱添加到膳食计划中：**
```bash
node ./scripts/tandoor.js add-to-meal-plan <recipe_id> "<meal_type>" "<YYYY-MM-DD>"
# Example: Add recipe 42 as Dinner on Feb 10th
node ./scripts/tandoor.js add-to-meal-plan 42 "Dinner" "2025-02-10"
```

**查看指定日期范围内的膳食计划：**
```bash
node ./scripts/tandoor.js get-meal-plans "2025-02-08" "2025-02-14"
```

---

### 🛒 购物清单

**查看当前购物清单：**
```bash
node ./scripts/tandoor.js get-shopping-list
node ./scripts/tandoor.js get-shopping-list "true"   # show checked items
node ./scripts/tandoor.js get-shopping-list "both"   # show all
```

**将商品添加到购物清单中：**
```bash
node ./scripts/tandoor.js add-shopping-item "<food>" "<amount>" "<unit>" "[note]"
# Example:
node ./scripts/tandoor.js add-shopping-item "Chicken Breast" "500" "g" "For stir fry"
```

**勾选商品：**
```bash
node ./scripts/tandoor.js check-shopping-item <item_id>
```

**删除商品：**
```bash
node ./scripts/tandoor.js remove-shopping-item <item_id>
```

---

### ➕ 创建新食谱

```bash
node ./scripts/tandoor.js create-recipe "<name>" "<ingredients>" "<instructions>" [servings]
```

示例：
```bash
node ./scripts/tandoor.js create-recipe "Grilled Cheese" \
  "2 slices bread
2 slices cheese
1 tbsp butter" \
  "1. Butter the bread
2. Add cheese between slices
3. Grill until golden brown" \
  2
```

---

### 📚 浏览参考资料

```bash
node ./scripts/tandoor.js get-keywords          # all keywords
node ./scripts/tandoor.js get-keywords "italian" # search keywords
node ./scripts/tandoor.js get-foods "chicken"    # search foods
node ./scripts/tandoor.js get-units              # all units
```

---

## 工作流程

### 为本周规划晚餐

1. **搜索用户可能喜欢的食谱：**
   ```bash
   node ./scripts/tandoor.js search-recipes "chicken"
   ```
2. **记录搜索结果中的食谱 ID：**
3. **查看可用的餐食类型**（确认“晚餐”这一餐食类型是否存在）：
   ```bash
   node ./scripts/tandoor.js get-meal-types
   ```
4. **将每个食谱分配到相应的日期**（每天重复此步骤）：
   ```bash
   node ./scripts/tandoor.js add-to-meal-plan 42 "Dinner" "2025-02-10"
   node ./scripts/tandoor.js add-to-meal-plan 15 "Dinner" "2025-02-11"
   # ... continue for each day
   ```

---

### 查看今天的膳食计划

1. **获取今天的膳食计划：**
   ```bash
   node ./scripts/tandoor.js get-meal-plans "2025-02-08"
   ```
2. **如果用户需要食谱详情，可查看完整食谱内容：**
   ```bash
   node ./scripts/tandoor.js get-recipe <recipe_id>
   ```

---

### 将食谱食材添加到购物清单

1. **获取食谱详情以查看所有食材：**
   ```bash
   node ./scripts/tandoor.js get-recipe <recipe_id>
   ```
2. **从响应中解析食材信息**（查看 `steps[].ingredients[]`）：
3. **将每种食材添加到购物清单中：**
   ```bash
   node ./scripts/tandoor.js add-shopping-item "Chicken Breast" "500" "g"
   node ./scripts/tandoor.js add-shopping-item "Onion" "2" "piece"
   # ... continue for each ingredient
   ```

---

### 创建并安排新食谱

1. **创建新食谱：**
   ```bash
   node ./scripts/tandoor.js create-recipe "Pasta Carbonara" \
     "200g spaghetti
   100g pancetta
   2 eggs
   50g parmesan" \
     "1. Cook pasta
   2. Fry pancetta
   3. Mix eggs with parmesan
   4. Combine all and serve" \
     2
   ```
2. **记录新食谱的 ID：**
3. **将新食谱添加到膳食计划中：**
   ```bash
   node ./scripts/tandoor.js add-to-meal-plan <new_recipe_id> "Dinner" "2025-02-12"
   ```

---

### 从购物清单中删除已勾选的商品

1. **查看已勾选的商品：**
   ```bash
   node ./scripts/tandoor.js get-shopping-list "true"
   ```
2. **根据 ID 删除已勾选的商品：**
   ```bash
   node ./scripts/tandoor.js remove-shopping-item <item_id>
   ```

---

## 故障排除

**“找不到食材”或“找不到对应的餐食类型”**  
请先在 Tandoor 服务端中查找正确的名称：
```bash
node ./scripts/tandoor.js get-foods "chicken"
node ./scripts/tandoor.js get-units "gram"
```

**“找不到对应的餐食类型”**  
运行 `get-meal-types` 命令以获取所有餐食类型的名称（不区分大小写）。