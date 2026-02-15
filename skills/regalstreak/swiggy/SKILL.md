---
name: swiggy
description: "在印度，您可以通过 Swiggy 的 MCP 服务器订购食物、杂货，并预订餐厅。Swiggy 提供食物配送服务、Instamart 的杂货购物服务以及 Dineout 的餐厅预订服务，所有流程都遵循以安全为首要目标的确认机制。"
---

# Swiggy 技能

通过 Swiggy 的 MCP 服务器，在印度订购食物、生活用品并预订餐厅。

## 安装

该技能包含一个名为 `swiggy` 的命令行工具（CLI）二进制文件。安装完成后：
```bash
cd skills/swiggy
npm link
```

这将创建一个全局可用的 `swiggy` 命令。可以通过 `which swiggy` 来验证其是否已安装。

## 使用场景

- **食物配送**：例如：“订购印度香饭”、“哪些餐厅营业到很晚？”、“为团队预订午餐”
- **生活用品（Instamart）**：例如：“购买鸡蛋和牛奶”、“购买一周所需的生活用品”、“查询食谱所需食材”
- **餐厅预订（Dineout）**：例如：“预订周六晚上8点的晚餐”、“预订科拉曼加拉地区的意大利餐厅”

## 可用命令

### 食物配送
```bash
# Search restaurants
swiggy food search "biryani" --location "Koramangala, Bengaluru"

# Get menu
swiggy food menu <restaurant-id>

# Cart management
swiggy food cart add <item-id> --quantity 2
swiggy food cart show
swiggy food cart clear

# Order (requires confirmation)
swiggy food order --address "home" --confirm
```

### Instamart（生活用品）
```bash
# Search products
swiggy im search "eggs" --location "HSR Layout, Bengaluru"

# Cart operations
swiggy im cart add <item-id> --quantity 3
swiggy im cart show
swiggy im cart clear

# Checkout (requires confirmation)
swiggy im order --address "home" --confirm
```

### Dineout（餐厅预订）
```bash
# Search restaurants
swiggy dineout search "Italian Indiranagar"

# Get details
swiggy dineout details <restaurant-id>

# Check availability
swiggy dineout slots <restaurant-id> --date 2026-01-30

# Book table (free bookings only, requires confirmation)
swiggy dineout book <restaurant-id> --date 2026-01-30 --time 20:00 --guests 2 --confirm
```

## 重要提示：安全规则

### ⚠️ **切勿自动下单！**
**在下单前务必获得用户的明确确认。**

1. **先查看购物车预览**：
   - 所有商品及其数量和价格
   - 总金额
   - 送货地址
   - 预计送达时间（针对食物/生活用品）

2. **请求用户确认**：
   ```
   Ready to order:
   - 2x Chicken Biryani (₹500)
   - 1x Raita (₹60)
   Total: ₹560 + delivery
   Deliver to: Home (HSR Layout)
   ETA: 30-40 mins
   
   Confirm order? (yes/no)
   ```

3. **只有在用户确认后**：
   - 使用 `--confirm` 标志执行下单命令
   - 将订单信息记录到 `memory/swiggy-orders.json` 文件中

### 注意事项：
Swiggy MCP 目前仅支持 **货到付款**（COD）方式。一旦下单，订单**无法取消**。请务必在确认前再次核对信息。

### 地址处理
- 用户可能会输入“家”、“办公室”等地址——系统会从 `USER.md` 文件中获取实际地址，或请求用户提供更详细的地址信息。
- 在预览界面中务必确认送货地址。
- 对于餐厅预订，地址仅用于搜索，不用于实际配送。

## 工作流程示例

- **食物订购流程**
```bash
# 1. Search
swiggy food search "biryani near Koramangala"

# 2. Browse menu (use restaurant ID from search)
swiggy food menu rest_12345

# 3. Add to cart
swiggy food cart add item_67890 --quantity 1

# 4. Preview cart
swiggy food cart show

# 5. Show preview to user, ask confirmation

# 6. If confirmed, order
swiggy food order --address "HSR Layout, Sector 2, Bengaluru" --confirm
```

- **生活用品购买流程**
```bash
# 1. Search items
swiggy im search "eggs" --location "Koramangala"
swiggy im search "milk" --location "Koramangala"

# 2. Add to cart
swiggy im cart add item_11111 --quantity 2
swiggy im cart add item_22222 --quantity 1

# 3. Preview
swiggy im cart show

# 4. Confirm with user

# 5. Checkout
swiggy im order --address "Koramangala, Bengaluru" --confirm
```

- **餐厅预订流程**
```bash
# 1. Search
swiggy dineout search "Italian Indiranagar"

# 2. Check details
swiggy dineout details rest_99999

# 3. Check slots
swiggy dineout slots rest_99999 --date 2026-01-30

# 4. Show options to user, confirm choice

# 5. Book
swiggy dineout book rest_99999 --date 2026-01-30 --time 20:00 --guests 2 --confirm
```

## 错误处理

- **无搜索结果**：建议用户扩大搜索范围或更换地址。
- **商品缺货**：提供替代商品建议。
- **无可用时间段**：建议用户更改预订时间或日期。
- **需要身份验证**：用户需要通过 OAuth 进行身份验证（由 MCP 负责处理）。

## 使用技巧

- **团队订单**：逐步构建购物车，询问团队成员的偏好。
- **预算购物**：按价格筛选搜索结果，并实时显示总金额。
- **根据食谱购物**：逐个搜索所需食材，再逐步添加到购物车中。
- **夜间配送**：在搜索条件中注明配送时间。

## 订单记录

订单成功后，将相关信息追加到 `memory/swiggy-orders.json` 文件中：
```json
{
  "timestamp": "2026-01-28T21:16:00+05:30",
  "type": "food",
  "items": [...],
  "total": "₹560",
  "address": "HSR Layout",
  "orderId": "..."
}
```

## 身份验证

Swiggy MCP 使用 OAuth 进行身份验证。首次使用该技能时系统会自动触发身份验证流程。`swiggy` CLI 通过 `mcporter` 工具来处理身份验证过程。

## 依赖项

- 该技能依赖于 `mcporter` 技能（在后台使用该技能）。
- 需要 Node.js 运行环境来运行 `swiggy` CLI 工具。

## 已知限制

- 目前仅支持货到付款方式（不支持在线支付）。
- 订单一旦提交无法取消。
- Dineout 服务仅提供免费预订服务。
- 使用 MCP 时请勿同时打开 Swiggy 应用程序（以避免会话冲突）。

---

**请记住：每次下单前都必须获得用户的确认。** 🐾