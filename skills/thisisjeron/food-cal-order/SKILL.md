---
name: food-cal-order
description: 通过浏览器自动化功能来订购外卖服务，该功能由日历事件触发。支持两种模式：  
1. **直接模式**（指定服务及餐厅）；  
2. **探索模式**（根据预设条件在所有可用的外卖服务中搜索）。  
支持的外卖平台包括 DoorDash、Uber Eats 和 Grubhub。  
当日历事件与用户的订餐习惯匹配时，系统会自动启动该功能，并生成用于控制浏览器的子代理（sub-agents）。
---

# 食物日历订购功能

通过浏览器自动化脚本，在日历事件触发时下达食物配送订单。

## 使用模式

### 直接模式
指定具体的服务和餐厅。

```
Title: "DoorDash: Chipotle"
Description: "burrito bowl, chicken, guac"
```

### 发现模式
根据预设条件搜索，以找到最合适的选项。

```
Title: "Thai food, high ratings, under $30, food for 2"
Description: "no shellfish, prefer noodles"
```

## 日历事件解析

**务必同时阅读日历事件的标题和描述。**

### 标题 → 使用模式 + 目标餐厅
| 模式匹配规则 | 使用模式 |
|-------------|-----------|
| `{服务名称}: {餐厅名称}` | 直接模式 |
| 仅基于菜系或条件 | 发现模式 |

### 描述 → 订单详情 + 附加要求
描述中包含以下两类信息：
1. **订单详情**：需要订购的食物（菜品、数量、份量）
2. **附加要求**：必须遵守的约束条件（尤其是与食品安全相关的要求）

解析描述内容，提取以下关键信息：
| 字段 | 例子 | 优先级 |
|---------|---------|---------|
| `items` | "墨西哥卷饼碗、鸡肉、鳄梨酱" | 订单详情 |
| `servings` | "为2人准备的食物" | 订单详情 |
| `allergies` | "对坚果过敏" | **严格禁止** |
| `dietary` | "素食"、"清真"、"无麸质" | **严格禁止** |
| `preferences` | "偏好面条"、"辣度更高"、"不含洋葱" | 尽量满足 |
| `budget` | "价格低于30美元" | 价格约束 |
| `delivery_notes` | "门禁码1234"、"放在门口" | 用于支付时输入 |
| `special_requests` | "生日蛋糕蜡烛"、"额外纸巾" | 尽量满足 |

**过敏或饮食方面的要求是不可协商的。** 如果不确定某项食物是否安全，请跳过该选项并选择明确安全的替代品。遇到疑问时，宁可保守处理——错误的食品可能会引起不适，而过敏反应则可能非常危险。

### 解析示例

```
Title: "DoorDash: Chipotle"
Description: "2 burrito bowls (chicken), guac on the side. Nut allergy. Gate code: 5521"
```

解析结果：
- **订单详情**：2份墨西哥卷饼碗（鸡肉）、鳄梨酱（配菜）
- **过敏信息**：对坚果过敏
- **配送要求**：门禁码5521

```
Title: "Thai food, high ratings, under $30, food for 2"
Description: "no shellfish, prefer noodles, gluten-free if possible, leave at door"
```

解析结果：
- **订单详情**：2人份食物
- **价格约束**：价格低于30美元
- **过敏信息**：对贝类过敏
- **饮食要求**：无麸质（尽量满足）
- **偏好**：偏好面条
- **配送要求**：放在门口

## 支持的服务平台
- **DoorDash**：前缀为 `DoorDash:`，网址为 `doordash.com`
- **Uber Eats**：前缀为 `UberEats:` 或 `Uber Eats:`，网址为 `ubereats.com`
- **Grubhub**：前缀为 `Grubhub:`，网址为 `grubhub.com`

## 直接模式的执行流程
创建一个子代理，并为其提供具体的执行指令：

```
sessions_spawn(
  task: """
Order food delivery via browser automation.

SERVICE: {service}
RESTAURANT: {restaurant}
ITEMS: {items}
ALLERGIES: {allergies or "none"}
DIETARY: {dietary or "none"}
PREFERENCES: {preferences or "none"}
DELIVERY_NOTES: {delivery_notes or "none"}
ADDRESS: {address or "use saved default"}

⚠️ ALLERGY/DIETARY RULES:
- NEVER add items containing allergens listed above
- When customizing items, REMOVE ingredients that conflict (e.g., "no peanuts")
- If an item cannot be made safe → skip it, note why in report
- Check item descriptions and ingredient lists on the menu

BROWSER STEPS:
1. Open {service_url} using Chrome profile (has saved login/payment)
2. Verify logged in (account icon visible, not "Sign In")
   - If not logged in → ABORT, report "Please log into {service} in Chrome first"
3. Search for "{restaurant}" using search bar
4. Click matching restaurant from results
   - If not found or closed → ABORT, report reason
5. For each item in ITEMS:
   - Find item on menu (use semantic matching)
   - Check description for allergen conflicts before adding
   - Click to open customization modal
   - Select required options (size, protein, etc.)
   - Apply customizations as specified
   - Apply allergy-related modifications (remove conflicting ingredients)
   - Apply PREFERENCES if customization options exist
   - Click "Add to cart/bag/order"
6. Open cart and verify:
   - Contents match ITEMS
   - No allergen conflicts in final order
   - Note any substitutions or issues
7. Proceed to checkout
   - Confirm delivery address (use saved default)
   - Add DELIVERY_NOTES if supported (special instructions field)
   - Confirm payment method (use saved default)
   - Note delivery ETA and total
8. Click "Place Order"
9. Wait for confirmation, capture order number and ETA

REPORT FORMAT:
✅ Order confirmed: {restaurant} via {service}, ETA {time}, total ${amount}
   Allergy accommodations: {what was modified or "N/A"}
— OR —
❌ Failed: {reason}

Do NOT checkout if cart doesn't match requested items.
Do NOT checkout if allergen safety cannot be confirmed.
""",
  label: "food-order-{service}"
)
```

## 发现模式的执行流程

### 第一阶段：信息收集（并行处理）
同时为所有服务平台创建子代理以收集相关信息：

```
sessions_spawn(
  task: """
Search for restaurants on {service}. RECON ONLY — do NOT order.

CRITERIA:
- Cuisine: {cuisine}
- Budget: {budget}
- Rating: {rating_preference}
- Servings: {servings}
- Allergies: {allergies or "none"}
- Dietary: {dietary or "none"}
- Preferences: {preferences}

⚠️ ALLERGY/DIETARY RULES:
- Only recommend restaurants where allergen-safe options clearly exist
- Flag any restaurant where the menu is ambiguous about allergens
- When noting menu highlights, confirm dishes are safe given stated allergies/dietary

BROWSER STEPS:
1. Open {service_url} using Chrome profile
2. Verify logged in
3. Search for "{cuisine}" or "{cuisine} food"
4. Apply filters if available (rating, price level, delivery time)
5. For top 3 restaurants:
   - Note: name, rating (stars + review count), price level ($/$$/$$$)
   - Note: delivery time estimate, delivery fee
   - Click into restaurant, scan menu for items matching cuisine
   - Note 2-3 standout dishes and typical entree price
   - Check if menu items list ingredients or allergen info
   - Flag any allergen concerns for highlighted dishes

RETURN FORMAT:
## {service} Results

### 1. {Restaurant Name}
- Rating: {stars} ({count} reviews)
- Price: {$/$$/$$S} (~${X}/person)
- Delivery: {time} min, ${fee} fee
- Menu highlights: {dishes matching criteria}
- Allergen safety: {safe / caution / unclear} — {notes}
- Fits constraints: {yes/no + notes}

### 2. ...
### 3. ...

**Best match:** {pick} because {reason}
""",
  label: "food-recon-{service}"
)
```

### 第二阶段：决策
所有信息收集子代理返回后，汇总并比较结果：
| 服务平台 | 餐厅名称 | 评分 | 人均价格 | 预计送达时间 | 是否满足约束条件 |
|---------|------------|---------|------------|----------------------|
| ... | ... | ... | ... | ... |

**选择最终订单的依据包括：**
1. **食品安全性**：优先选择食品安全性明确的餐厅；如果无法确保安全，则排除相关餐厅。
2. **是否符合菜系和饮食要求**
3. **价格是否在预算范围内**（预留25%用于支付费用和小费）
4. **评分越高越好**
5. **配送速度越快越好**
6. **菜单是否符合用户偏好**

**根据上述条件规划订单**：
- 为2人订购时：通常选择1份开胃菜+2份主菜，或2-3份可共享的菜品
- 确保价格在预算范围内
- **绝对不能包含与过敏或饮食要求冲突的菜品**
- 尽量满足用户的偏好（例如，如果用户偏好面条，则应选择含面条的菜品）
- 如果某项食物的过敏信息不明确，选择明确安全的替代品

### 第三阶段：下达订单
为选定的服务平台创建订单子代理，并使用之前设定的直接模式指令来下达订单。

## 状态跟踪
将订单状态信息存储在 `memory/food-order-state.json` 文件中：

```json
{
  "ordered": {
    "{calendar_event_id}": {
      "at": "2026-02-06T19:00:00",
      "mode": "discovery",
      "criteria": "Thai food, high ratings, under $30, food for 2",
      "constraints": {
        "allergies": ["shellfish"],
        "dietary": ["gluten-free"],
        "delivery_notes": "leave at door"
      },
      "service": "doordash",
      "restaurant": "Thai Basil",
      "items": ["spring rolls", "pad thai (no shrimp)", "green curry"],
      "status": "confirmed",
      "eta": "7:35 PM",
      "total": 28.47
    }
  }
}
```

每周检查一次，删除超过24小时的订单记录。

## 错误处理机制
| 错误类型 | 处理方式 |
|---------|-------------|
| 未登录 | 中断操作，并提示用户通过Chrome浏览器登录 |
| 餐厅已关闭 | 直接模式：放弃当前订单；发现模式：选择下一个合适的餐厅 |
| 未找到符合条件的餐厅 | 通知用户并建议调整搜索条件 |
| 超出预算 | 选择价格更低的选项或减少订单内容，并记录调整情况 |
- 某项食物不可用 | 选择最接近的替代品，并在确认信息中注明 |
- 存在过敏原冲突 | **绝对不要订购该食物**，选择安全的替代品或跳过该选项，并在报告中记录这一情况 |

## 参考文件
关于各服务平台的特殊注意事项和用户界面元素的位置，请参考以下文件：
- [doordash.md](references/doordash.md)
- [ubereats.md](references/ubereats.md)
- [grubhub.md](references/grubhub.md)

这些文件详细说明了各服务平台的独特功能（如促销弹窗、小费提示等）。子代理所需的操作步骤已在上述代码中详细说明，确保其能够独立完成任务。