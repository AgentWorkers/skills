---
name: food-cal-order
description: >
  通过浏览器自动化功能来订购外卖服务，该功能由日历事件触发。支持两种模式：  
  1. **直接模式**（指定服务及餐厅）：用户可以直接选择特定的服务和餐厅进行订单；  
  2. **探索模式**（基于条件的搜索）：用户可以根据需求在所有可用的外卖服务中进行搜索。  
  支持的外卖平台包括 DoorDash、Uber Eats 和 Grubhub。  
  当日历事件与用户的订餐习惯相匹配时，该工具会自动启动相应的订购流程，并生成用于控制浏览器的子代理（sub-agents）。
---
# 食物日历订单功能

通过浏览器自动化来下单，该功能由日历事件触发。

## 安全性与前提条件

> **使用本功能前请阅读以下内容。**

- **Chrome 配置文件访问权限：** 本功能会访问您本地 Chrome 的配置文件，其中包含您的登录信息、支付方式和配送地址。子代理将直接与这些信息进行交互。
- **实际收费：** 确认订单后，系统会从您保存的支付方式中扣除费用。此操作为实时交易，没有模拟环境（sandbox）。
- **触发源的可靠性：** 只有您自己创建的日历事件才能触发此功能。由他人创建或修改的事件（如共享日历、外部邀请）可能无法准确反映您的意图。在操作前请验证事件的来源。
- **强制确认：** 在下单前会显示一个预结算摘要，您必须明确选择“是”才能继续；其他任何回答都会导致订单取消。

## 模式

### 直接模式
指定服务和餐厅。

```
Title: "DoorDash: Chipotle"
Description: "burrito bowl, chicken, guac"
```

### 发现模式
根据条件搜索所有服务，以找到最合适的选项。

```
Title: "Thai food, high ratings, under $30, food for 2"
Description: "no shellfish, prefer noodles"
```

## 日历事件解析

**请务必阅读日历事件的标题和描述。**

> **安全提示：** 仅处理看起来是由日历所有者创建的事件。如果事件最近被外部人员修改（例如，共享日历的参与者或外部邀请），请在预确认摘要中明确说明，以便用户做出判断。

### 标题 → 模式 + 目标餐厅

| 模式匹配规则 | 对应模式 |
|-------------|------------|
| `{服务}: {餐厅}`     | 直接模式 |
| 仅基于菜系/条件    | 发现模式 |

### 描述 → 订单详情 + 限制条件

描述中包含两种类型的信息：

1. **订单详情**：需要订购的食物（菜品、数量、份数）
2. **限制条件**：必须遵守的规则（尤其是与食品安全相关的）

解析描述并提取以下信息：

| 字段          | 例子                | 优先级      |
|---------------|------------------|-----------|
| `items`        | "墨西哥卷饼碗，鸡肉，鳄梨酱"      | 订单详情     |
| `servings`      | "为2人准备的食物"         | 订单详情     |
| `allergies`      | "对坚果过敏"           | **绝对禁止**    |
| `dietary`      | "素食"              | **绝对禁止**    |
| `preferences`    | "偏好面条"            | 尽量满足    |
| `budget`       | "预算低于30美元"         | 限制条件     |
| `delivery_notes`   | "门禁代码1234"          | 传递给结算系统 |
| `special_requests` | "生日蛋糕蜡烛"          | 尽量满足    |

**过敏或饮食限制是不可协商的。** 如果不确定某项食物是否安全，请跳过该选项并选择明显安全的替代品。遇到疑问时，宁可保守处理——错误的食品会引起不适，而过敏反应可能非常危险。

### 解析示例

```
Title: "DoorDash: Chipotle"
Description: "2 burrito bowls (chicken), guac on the side. Nut allergy. Gate code: 5521"
```

提取的信息：
- **订单详情：** 2个墨西哥卷饼碗（鸡肉），配鳄梨酱
- **过敏信息：** 对坚果过敏
- **配送说明：** 门禁代码5521

```
Title: "Thai food, high ratings, under $30, food for 2"
Description: "no shellfish, prefer noodles, gluten-free if possible, leave at door"
```

提取的信息：
- **份数：** 2人份
- **预算：** 30美元
- **过敏信息：** 对贝类过敏
- **饮食限制：** 无麸质（尽量满足）
- **偏好：** 偏好面条
- **配送说明：** 放在门口

## 支持的服务

- **DoorDash** — 前缀为 `DoorDash:`，网址 `doordash.com`
- **Uber Eats** — 前缀为 `UberEats:` 或 `UberEats:`，网址 `ubereats.com`
- **Grubhub** — 前缀为 `Grubhub:`，网址 `grubhub.com`

## 直接模式的执行方式

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
1. Open {service_url} using Chrome profile (NOTE: this profile contains your saved logins,
   payment methods, and delivery addresses — a real charge will be made on confirmation)
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

7b. PAUSE — present order summary to user and request explicit confirmation:
    "Ready to place order:
     • Restaurant: {restaurant} via {service}
     • Items: {items}
     • Total: ${amount}
     • Delivery to: {address}
     • ETA: {eta}
     Confirm? (yes / no / cancel)"

    WAIT for user response.
    - "yes" → proceed to step 8
    - anything else → ABORT, do NOT place order

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

## 发现模式的执行方式

### 第一阶段：信息收集（并行）

同时为所有服务创建子代理以收集信息：

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
1. Open {service_url} using Chrome profile (NOTE: this profile contains your saved logins,
   payment methods, and delivery addresses — a real charge will be made on confirmation)
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

| 服务 | 餐厅 | 评分 | 人均价格 | 预计送达时间 | 是否符合限制条件 |
|------|------|--------|------------|------------------|
| ... | ... | ... | ... | ... |

**选择最佳选项的标准：**
1. **优先考虑食品安全** — 排除安全性“不明确”或“需谨慎”的餐厅（除非没有其他安全选项）
2. 必须符合菜系和饮食限制
3. 预算必须可行（预留25%用于费用和小费）
4. 优先选择评分较高的餐厅
5. 优先选择配送速度较快的餐厅
6. 菜单内容符合用户偏好

**制定订单计划：**
- 根据份数和偏好选择合适的菜品：
  - 为2人：通常选择1道开胃菜+2道主菜，或2-3道可共享的菜品
- 保持预算在指定范围内
- **绝对不能包含与过敏或饮食限制冲突的菜品**
- 尽量满足用户偏好（例如，如果用户偏好面条，则选择含面条的菜品）
- 如果某项食物的过敏信息不明确，选择明显安全的替代品

### 第三阶段：下单

为选定的服务创建订单子代理（使用上述直接模式的指令）。

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

每周检查一次，删除超过24小时的记录。

## 错误处理

| 错误类型 | 处理方式 |
|---------|-----------|
| 未登录   | 中止操作，并通知用户通过Chrome登录 |
| 餐厅关闭 | 直接模式：中止订单；发现模式：选择下一个最佳选项 |
| 未找到匹配项 | 通知用户并建议调整搜索条件 |
| 预算超出 | 选择更便宜的选项或减少订单内容，并记录调整情况 |
| 物品不可用 | 选择最接近的替代品，并在确认信息中注明 |
| 过敏原冲突 | **绝对不要订购该物品**。选择安全的替代品或跳过该选项，并在报告中注明 |
| 过敏原信息不明确 | 跳过该物品，选择明显安全的替代品，并在报告中注明不确定性 |

## 参考文件

关于各服务的特殊注意事项和用户界面元素的位置，请参阅 `references/` 目录下的文件：
- [doordash.md](references/doordash.md)
- [ubereats.md](references/ubereats.md)
- [grubhub.md](references/grubhub.md)

这些文件详细说明了各服务的特殊规则和用户界面元素的位置。关键操作步骤已包含在上述子代理的指令中，确保子代理能够独立完成任务。