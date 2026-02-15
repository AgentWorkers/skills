---
name: zepto
description: 只需几秒钟，您就可以在 Zepto 上订购食品杂货了。只需告诉他们您需要什么，然后通过 WhatsApp 收到付款链接，在手机上完成支付即可。系统会自动记住您经常购买的物品。该服务覆盖 Zepto 提供配送服务的整个印度地区。
metadata: {"openclaw":{"emoji":"🛒","requires":{"config":["browser.enabled"]}}}
---

# zepto

**在30秒内通过Zepto下单购买杂货。从聊天到结账，一切一步到位。**

告诉你的AI你需要的商品，它会帮你完成购物，生成支付链接，然后通过WhatsApp发送给你。你可以在手机上完成支付，货物将在10分钟后送达。

## 💬 示例

**快速下单：**
```
"Order milk and bread from Zepto"
"Add vegetables - tomatoes, onions, potatoes"  
"Get me Amul butter and cheese"
```

**常购商品：**
```
"Add my usual milk" → AI picks the brand you always order
"Order the usual groceries" → AI suggests your frequent items
```

**完整购物清单：**
```
"Add milk, bread, eggs, coriander, ginger, and tea bags"
→ AI adds everything, shows total: ₹X
→ Sends payment link to WhatsApp
→ You pay, groceries arrive
```

---

## 🔒 安全与隐私

**此技能的功能：**
- ✅ 在zepto.com上进行浏览器自动化操作（使用你的本地浏览器和会话）
- ✅ 将订单历史记录存储在`~/.openclaw/skills/zepto/order-history.json`文件中（仅限本地使用，不会共享）
- ✅ 通过WhatsApp发送支付链接（每次支付都需要你的同意）
- ✅ 所有认证过程均遵循Zepto的官方流程（手机 + OTP）

**此技能不支持的功能：**
- ❌ 不支持自动支付（你需要点击链接并手动完成支付）
- ❌ 不会向外部服务器发送任何数据（除了通过你的渠道发送到Zepto.com和WhatsApp的数据）
- ❌ 不会后台持续运行任务（仅在你同意的情况下，会一次性检查订单状态）
- ❌ 不会存储支付信息或OTP代码
- ❌ 无法访问你的银行或UPI应用程序

**数据存储：**
- 订单历史记录：`~/.openclaw/skills/zepto/order-history.json`（仅限本地使用，有助于“常购商品”功能）
- 浏览器会话：由OpenClaw的浏览器管理（标准Chrome/Chromium配置文件）

**用户控制：**
- 你可以控制何时下单
- 你需要批准每个支付链接
- 你可以随时删除订单历史记录文件
- 所有浏览器操作都在你的个人资料中可见

---

## 🚨 关键工作流程规则

**在创建订单时，请务必遵循以下步骤：**

### 规则1：先查看购物车
```bash
# Before adding ANY items, ALWAYS check cart state
node zepto-agent.js get-cart
```

**原因：**购物车中可能包含之前会话中的商品。添加重复商品是浪费资源。

### 规则2：使用智能购物功能（推荐）
```bash
# This handles everything: clears unwanted, checks duplicates, adds missing
node zepto-agent.js smart-shop "milk, bread, eggs"
```

**功能：**
1. 检查当前购物车状态
2. 清除现有商品（如果有）
3. 对于每个商品：检查是否已存在于购物车中 → 如果存在则跳过 → 仅添加未购买的商品
4. 返回结果：`{ added: [], skipped: [], failed: [] }`

### 规则3：除非快照数据不足，否则切勿截图
- 快照会显示所有参考链接、按钮和文本
- 只有在快照不完整或不清楚时，才需要截图进行视觉调试
- **在99%的情况下，快照就足够了**

### 规则4：检测“已在购物车中”的提示
当你看到以下提示时：
```
"Decrease quantity 1 Increase quantity"  → Item is IN CART
button "Remove" [ref=eXX]                 → Item is IN CART
```

**看到这些提示时，请** **不要** 点击“添加”按钮！

---

## 完整流程
1. **认证** - 使用手机和OTP进行验证
2. **地址确认** - 核实送货地址
3. **购物** - 搜索并添加商品（优先显示你常购的商品！）
4. **生成支付链接** - 通过WhatsApp生成Juspay支付链接

---

## 步骤0：订单历史记录与常购商品

**你的订单历史记录存储在：`{SKILL_DIR}/order-history.json`中**

（其中`{SKILL_DIR}`是你的技能目录，通常为`~/.openclaw/skills/zepto/`）

**智能选择逻辑：**
1. 当用户请求某件商品时（例如：“添加牛奶”）
2. 检查`order-history.json`中是否已购买过该商品
3. **如果已购买2次以上** → 自动选择用户最常购买的版本
4. **如果购买0-1次** → 显示选项并让用户进行选择

### 自动化订单历史记录抓取工具

**运行条件：** 用户请求“更新我的Zepto订单历史”或“刷新订单历史”

**流程：**
1. 导航到账户页面
2. 获取所有已完成的订单链接
3. 依次访问每个订单
4. 使用DOM抓取技术提取商品信息
5. 构建购买频率统计
6. 保存到`order-history.json`文件

**自动化抓取工具的优势：**
- ✅ 无需手动查看截图
- ✅ 更快捷（通过程序自动访问所有订单）
- ✅ 数据始终是最新的
- ✅ 可以随时重新运行

**示例：**
```
User: "Update my Zepto order history"

Response:
"🔍 Scanning your Zepto orders...
📦 Found 6 delivered orders
🔄 Extracting items...
✅ Updated! Found:
   - Coriander: 4 orders
   - Milk: 3 orders
   - Bread: 2 orders
   - Potato: 2 orders
   + 15 other items

Your usuals are ready!"
```

---

**智能选择逻辑（利用历史记录）：**

**示例：**
```
User: "Add milk"

[Check order-history.json]
→ "Amul Taaza Toned Fresh Milk | Pouch (500ml)" ordered 3x

Response:
"🥛 Adding your usual milk!
Amul Taaza Toned Fresh Milk (500ml) - ₹29
📊 You've ordered this 3 times
✅ Added to cart"
```

**如果商品仅购买过一次或从未购买过：**
```
User: "Add milk"

[Check order-history.json]
→ "Amul Taaza" ordered 1x only

Response:
"🥛 Found some milk options:
1. Amul Taaza Toned (500ml) - ₹29 ⭐ 4.8 (100k) - You've ordered this once
2. Amul Gold (1L) - ₹68 ⭐ 4.9 (80k) - Most popular
3. Mother Dairy (500ml) - ₹30 ⭐ 4.7 (60k)

Which one? (or tell me a number)"
```

**更新订单历史记录：** 每次成功下单后，都会更新JSON文件中的商品信息。

---

## 步骤1：认证（仅首次使用时）

**检查是否已登录：**
```bash
browser open url=https://www.zepto.com profile=openclaw
browser snapshot --interactive profile=openclaw
# Look for "login" button vs "profile" link
```

**如果未登录，请开始认证流程：**

### 1.1：获取电话号码**
询问用户：“你的Zepto电话号码是多少？（10位数字）”

### 1.2：输入电话号码并请求OTP**
```bash
# Click login button
browser act profile=openclaw request='{"kind":"click","ref":"{login_button_ref}"}'

# Type phone number
browser act profile=openclaw request='{"kind":"type","ref":"{phone_input_ref}","text":"{phone}"}'

# Click Continue
browser act profile=openclaw request='{"kind":"click","ref":"{continue_button_ref}"}'
```

### 1.3：从用户处获取OTP**
询问用户：“我已经将OTP发送到了{phone}。你收到的OTP是多少？”

### 1.4：输入OTP**
```bash
browser snapshot --interactive profile=openclaw  # Get OTP input refs
browser act profile=openclaw request='{"kind":"type","ref":"{otp_input_ref}","text":"{otp}"}'
# OTP auto-submits after 6 digits
```

**结果：** 用户现在已登录！会话在浏览器重启后仍然有效。

---

## 步骤2：地址确认

**🚨 关键：在进行任何购物操作之前，请务必确认地址！**

### 地址选择规则

**默认行为：**
1. 大多数用户保存了多个地址（如家、办公室等）
2. **始终显示当前地址并请求用户确认** —— 绝不要默认使用某个地址
3. 如果有订单历史记录，检查上次使用的地址
4. 在继续操作前等待用户的明确确认

**在首页上，地址显示在页面顶部：**
```bash
browser snapshot --interactive profile=openclaw
# Look for button with heading level=3 containing the address
# Example ref: e16 with text like "Home - [Address Details]..."
# Delivery time shown nearby (e.g., "10 minutes")
```

**购物前务必询问用户确认地址：**
```
📍 I see your delivery address is set to:
{Address Name} - {Full Address}
⏱️ Delivery in ~{X} minutes

Is this correct? Should I proceed with this address?
```

**程序化地址选择（新功能！）**
**使用`zepto-agent.js select-address`命令：**

```bash
node zepto-agent.js select-address "Home"
node zepto-agent.js select-address "sanskar"     # Fuzzy matching works!
node zepto-agent.js select-address "kundu blr"
```

**工作原理：**
1. **模糊匹配** —— 不区分大小写，支持部分匹配
   - “sanskar” → “Sanskar Blr” ✅
   - “home” → “New Home” ✅
   - “kundu” → “Kundu Blr” ✅
2. **检测是否已选择过该地址** —— 如果用户已经选择了该地址，则跳过此步骤
3. **确认地址变更** —— 点击后确认地址是否发生变化

**示例：**
```bash
# Current address: "Kundu Blr"
node zepto-agent.js select-address "sanskar"

# Output:
# ℹ️ Opening Zepto...
# ✅ Zepto opened
# ℹ️ 📍 Selecting address: "sanskar"
# ℹ️ Current: Kundu Blr
# ✅ Clicked: Sanskar BlrA-301, A, BLOCK-B...
# 🎉 Address changed to: Sanskar blr
```

**当用户说“将地址改为X”或“送到X”时：**
```bash
# Just call the command with their address name/query
node zepto-agent.js select-address "{user_query}"
```

**无需手动操作！** 脚本会自动完成以下操作：**
- 打开地址选择弹窗
- 通过模糊匹配找到地址
- 点击地址
- 确认地址变更
- 关闭弹窗

**手动选择（备用方案）：**
如果程序化方法失败或找不到地址：

```bash
# Click the address button (ref e16 or similar)
browser act profile=openclaw request='{"kind":"click","ref":"e16"}'
# This opens address selection modal with all saved addresses
```

**使用JavaScript选择地址：**
```bash
# Replace {USER_ADDRESS_NAME} with the actual address name user selected
browser act profile=openclaw request='{"fn":"() => { const input = document.querySelector('input[placeholder*=\"address\"]'); if (!input) return { error: 'Modal not found' }; let modal = input; for (let i = 0; i < 15; i++) { if (!modal.parentElement) break; modal = modal.parentElement; if (window.getComputedStyle(modal).position === 'fixed') break; } const divs = Array.from(modal.querySelectorAll('div')); const match = divs.find(d => d.textContent && d.textContent.trim().startsWith('{USER_ADDRESS_NAME}')); if (!match) return { error: 'Address not found' }; let p = match; for (let i = 0; i < 10; i++) { if (!p) break; const s = window.getComputedStyle(p); if (p.onclick || p.getAttribute('onClick') || s.cursor === 'pointer') { p.scrollIntoView({ block: 'center' }); setTimeout(() => {}, 300); p.click(); return { clicked: true, text: match.textContent.substring(0, 100) }; } p = p.parentElement; } return { error: 'No clickable parent' }; }()","kind":"evaluate"}'
```

**用户确认地址后：**
```
✅ Delivery address confirmed: {address_name}
📍 {full_address}
⏱️ ETA: {eta} mins

Ready to shop! What would you like to add to cart?
```

**⚠️ 地址选择非常重要 —— 请务必完成此步骤！**

---

## 步骤3：购物

### 3A：探索模式（浏览与发现）

当用户请求“探索”、“展示给我”、“有什么好吃的”、“找点什么”或“发现商品”时：

**常见的探索需求：**
- “展示价格在50卢比以下的健康零食”
- “乳制品有哪些不错的选择？”
- “找些早餐食品”
- “有水果促销吗？”
- “找些蛋白棒”

**浏览商品类别：**
```bash
# Navigate to category pages
browser navigate url=https://www.zepto.com profile=openclaw
browser snapshot --interactive profile=openclaw

# Categories available on homepage:
# - Fruits & Vegetables
# - Dairy, Bread & Eggs
# - Munchies (snacks)
# - Cold Drinks & Juices
# - Breakfast & Sauces
# - Atta, Rice, Oil & Dals
# - Cleaning Essentials
# - Bath & Body
# - Makeup & Beauty
```

**过滤与排序：**
```bash
# Example: Browse "Munchies" category
browser navigate url=https://www.zepto.com/pn/munchies profile=openclaw
browser snapshot --interactive profile=openclaw

# Take screenshot to show user the options
browser screenshot profile=openclaw
```

**探索结果格式：**
```
🔍 Found some great options in {category}:

1. **{Product Name}** - ₹{price} ({discount}% OFF)
   ⭐ {rating} ({review_count} reviews)
   📦 {size/quantity}
   
2. **{Product Name}** - ₹{price}
   ⭐ {rating} ({review_count} reviews)
   
3. **{Product Name}** - ₹{price} ({discount}% OFF)
   ⭐ {rating} ({review_count} reviews)

Want me to add any of these? Just tell me the number(s)!
```

**智能过滤提示：**
- 价格范围：从用户查询中提取（如“价格在50卢比以下”）
- 优惠信息：查找带有“₹X OFF”标签的商品
- 高评分商品：优先显示评分4.5及以上的商品
- 热门商品：按评论数量排序（k表示千条评论）
- 健康导向：使用关键词如“蛋白质”、“无糖”、“有机”、“小米”

**交互式探索：**
展示选项后，用户可以：
- 按数量添加商品：“添加1个和3个”
- 请求更多商品：“再展示一些”
- 细化搜索：例如“展示更便宜的选项”或“有什么巧克力口味的？”
- 切换类别：“现在展示乳制品”

### 3B：直接搜索（特定商品）

**强制预检查：**
在添加任何商品之前：
1. 点击购物车按钮
2. 查看当前购物车内容
3. 如果购物车中有商品：询问用户“保留现有商品还是先清空购物车？”
4. 如果购物车为空：继续购物

**多商品购物流程：**
当用户提供商品列表（例如：“添加牛奶、黄油、面包”）时：
1. **一次添加一个商品并验证：**
   - 搜索商品
   - 点击“添加”按钮
   - 等待0.5秒，确认商品是否已添加到购物车
   - 如果验证失败：最多尝试3次
2. **然后显示最终购物车摘要**，包括所有商品和总价

**重要提示：** 未经验证切勿批量添加商品！每次添加商品后，页面引用链接都会发生变化。

**商品选择逻辑：**
- 首先检查`order-history.json`文件
- 如果商品已购买2次以上 → 自动选择用户最常购买的版本
- 如果商品购买0次或有多个不确定的版本 → **显示选项并询问用户**
- 根据用户的请求选择最匹配的商品（例如，用户要求“Yakult Light”，则选择评分最高的版本）
- 如果无法确定商品版本：```
🥛 Found multiple milk options:
1. Amul Taaza (500ml) - ₹29 ⭐ 4.8 (100k)
2. Amul Gold (1L) - ₹68 ⭐ 4.9 (80k)
3. Mother Dairy (500ml) - ₹30 ⭐ 4.7 (60k)

Which one? (or tell me a number)
```

**搜索过程：**
```bash
browser navigate url=https://www.zepto.com/search?query={item} profile=openclaw
browser snapshot --interactive profile=openclaw
```

**选择最佳商品**
**规则：** 选择评分最高的商品（除非订单历史记录中有其他说明）。
格式：`{rating} ({count})`，其中k表示千条评论，M表示百万条评论。

**添加到购物车：**
```bash
browser act profile=openclaw request='{"kind":"click","ref":"{ADD_button_ref}"}'
```

**查看购物车摘要（添加所有商品后必须显示）**
```bash
browser navigate url=https://www.zepto.com/?cart=open profile=openclaw
browser snapshot profile=openclaw  # Get cart summary
```

**购物车摘要格式：**
```
🛒 Added to cart:
1. Item 1 - ₹XX
2. Item 2 - ₹YY
3. Item 3 - ₹ZZ

💰 Total: ₹{total}

Ready to checkout? (say "yes" or "checkout" or "lessgo")
```

**重要提示：** 商品数量映射：**
当用户提供购物清单和数量时（例如：“3份jeera，2份saffola燕麦”）：
1. **在进行任何购物车操作之前，务必先创建一个映射文件**
2. 将每个商品名称与其用户请求的数量关联起来
3. 在删除或修改商品之前，**务必核对这个映射**
4. 绝不要假设商品的数量是固定的 —— 必须核对映射信息

**示例映射：**
```json
{
  "jeera": 3,
  "saffola_oats": 2,
  "milk": 1
}
```

**在删除重复商品或调整数量之前：**
- 截取购物车快照
- 根据商品名称与映射文件进行匹配
- 确认数量与用户请求一致
- 如果不确定，请先询问用户

**错误处理 —— 商品缺货：**
**如果商品找不到或已售罄：**
```
❌ {item} is currently unavailable.

🔍 Suggestions:
- {similar_item_1}
- {similar_item_2}

What would you like instead?
```

**不要自动添加替代商品** —— 等待用户提供下一个商品或做出选择。

---

## 步骤4：生成支付链接

在所有商品添加到购物车并且用户确认结账后：

### 4.1：打开购物车并进入支付页面**
```bash
# Open cart modal
browser act profile=openclaw request='{"kind":"click","ref":"{cart_button_ref}"}'
# Example ref from homepage: e44

# Wait for cart to open, take snapshot
browser snapshot --interactive profile=openclaw

# Click "Click to Pay ₹{amount}" button
browser act profile=openclaw request='{"kind":"click","ref":"{click_to_pay_button_ref}"}'
# Example ref: e3579
```

### 4.2：提取Juspay支付链接**
```bash
# Wait 2 seconds for navigation to complete
browser act profile=openclaw request='{"fn":"async () => { await new Promise(r => setTimeout(r, 2000)); return window.location.href; }","kind":"evaluate"}'
```

**链接格式：**
```
https://payments.juspay.in/payment-page/signature/zeptomarketplace-{order_id}
```

**示例：**
```
https://payments.juspay.in/payment-page/signature/zeptomarketplace-{ORDER_ID_EXAMPLE}
```

### 4.3：通过WhatsApp发送链接**
```bash
message action=send channel=whatsapp target={user_phone} message="🛒 *Your Zepto order is ready!*

*Cart Summary ({item_count} items):*
1. {item1} - ₹{price1}
2. {item2} - ₹{price2}
3. {item3} - ₹{price3}

*💰 Total: ₹{total}*

📍 Delivering to: {address_name} - {address}
⏱️ ETA: {eta} minutes

*🔗 Click here to pay:*
{juspay_payment_link}

⚠️ *IMPORTANT: After payment, message me \"DONE\" to confirm your order!*
(Don't rely on the payment page - just tell me when you've paid and I'll verify it) 🚀"
```

### 4.4：等待用户发送“完成”消息并确认订单**

**用户发送“完成”或“已支付”消息后：**

**步骤1：导航到Zepto首页查看订单状态**
```bash
browser navigate url=https://www.zepto.com profile=openclaw
browser snapshot --interactive profile=openclaw
```

**步骤2：查找订单确认信息**
查看以下提示：
- “您的订单正在处理中”
- “订单已确认”
- “正在准备您的订单”
- “商品将在X分钟后送达”
- 提供订单追踪按钮/链接

**步骤3：自动清空购物车（支付后操作）**

**重要提示：** **支付完成后，购物车中的商品可能仍然显示！** 因为Zepto尚未同步订单状态！

**自动清空购物车（用户通常期望支付后购物车为空）：**
```bash
# Open cart
browser act profile=openclaw request='{"kind":"click","ref":"{cart_button_ref}"}'
browser snapshot --interactive profile=openclaw

# Click Remove button for each item
browser act profile=openclaw request='{"kind":"click","ref":"{remove_button_ref_1}"}'
browser act profile=openclaw request='{"kind":"click","ref":"{remove_button_ref_2}"}'
browser act profile=openclaw request='{"kind":"click","ref":"{remove_button_ref_3}"}'
# ... repeat for all items
```

**步骤4：向用户确认**

**如果订单已确认：**
```
✅ *Payment confirmed!*
🚚 Your order is on the way! Arriving in ~{X} mins.

Order details:
- {item_count} items, ₹{total}
- Delivery to: {address}

✅ Cart cleared ({item_count} items removed from previous order)
🛒 Ready for your next order! 🐺
```

**如果订单尚未显示：**
```
⏳ Payment processed, but order confirmation is still loading on Zepto's end.

Let me check again in 30 seconds...
```

**则设置后台任务尝试再次获取订单。**

**步骤1：返回Zepto首页**
```bash
browser navigate url=https://www.zepto.com profile=openclaw
```

**步骤2：在首页查看订单状态**
```bash
browser snapshot --interactive profile=openclaw
# Look for "Your order is on the way" or order tracking
```

**步骤3：打开购物车查看商品**
```bash
browser act profile=openclaw request='{"kind":"click","ref":"{cart_button_ref}"}'
browser snapshot --interactive profile=openclaw
```

**重要提示：** 因为Zepto尚未同步订单确认信息，购物车中的商品可能仍然显示！**

**步骤4：询问用户是否需要清空购物车**
```
✅ Payment confirmed! Your order is on the way.

⚠️ I can see {X} items still in the cart (from the previous order that just went through).

Should I:
1. Clear the cart (recommended for fresh start)
2. Keep the items (if you want to reorder them)

*Default: I'll clear the cart unless you say "keep it"*
```

**如果用户同意：**
```bash
# For each item in cart, click Remove button
browser act profile=openclaw request='{"kind":"click","ref":"{remove_button_ref_1}"}'
browser act profile=openclaw request='{"kind":"click","ref":"{remove_button_ref_2}"}'
# ... repeat for all items

# Or use JavaScript to clear all at once:
browser act profile=openclaw request='{"fn":"() => { const removeButtons = document.querySelectorAll(\"button\"); let count = 0; for (let btn of removeButtons) { if (btn.textContent.trim() === \"Remove\") { btn.click(); count++; } } return `Removed ${count} items`; }","kind":"evaluate"}'
```

**确认消息：**
```
✅ Cart cleared! ({X} items removed)
🛒 Ready for your next order!

Your current order ({item_count} items, ₹{total}) will arrive in ~{eta} mins.
```

**如果用户表示“保留这些商品”：**
```
✅ Got it! Keeping {X} items in cart.
🛒 Ready to add more items or proceed with these?
```

---

**2. 手动进入购物车并点击“支付”**
**如果需要我再次尝试，请告诉我：**
```

**If delivery address becomes unserviceable:**
```
⚠️ 您的送货地址当前无法使用。
需要将订单发送到其他地址吗？
（我可以显示您保存的所有地址）
```

---

## 🎯 Complete Order Flow Summary

### Before Starting ANY New Order (Normal Flow - No Recent Payment):

**1. Check Address (ALWAYS)**
```
📍 当前地址：{address}
地址正确吗？
```

**2. Check Cart (if items exist)**
```
# 打开购物车
browser act profile=openclaw request='{"kind":"click","ref":"{cart_button_ref}'
browser snapshot --interactive profile=openclaw
```

**If items in cart from NORMAL browsing (not post-payment):**
```
⚠️ 我看到您的购物车中有{X}件商品：
1. {item1} - ₹{price1}
2. {item2} - ₹{price2}
您想：
1. 清空购物车吗？
2. 保留这些商品吗？
```

**Wait for user response before proceeding.**

---

### Post-Payment Behavior (After User Says "Done" or "Paid"):

**This is DIFFERENT from normal flow - auto-clear expected!**

**1. Navigate to zepto.com and check order status**
```
browser navigate url=https://www.zepto.com profile=openclaw
browser snapshot --interactive profile=openclaw
```

**2. Look for "Your order is on the way" or "Arriving in X mins"**

**3. Open cart and AUTO-CLEAR without asking**
```
# 打开购物车
browser act profile=openclaw request='{"kind":"click","ref":"{cart_button_ref}'
# 删除所有商品（这些商品来自刚刚完成的订单）
browser act profile=openclaw request='{"kind":"click","ref":"{remove_ref_1}'}
browser act profile=openclaw request='{"kind":"click","ref":"{remove_ref_2}'}
browser act profile=openclaw request='{"kind":"click","ref":"{remove_ref_3}'}
```

**4. Confirm to user**
```
✅ 支付已确认！您的订单正在处理中！商品将在约{X}分钟后送达。
✅ 购物车已清空（共删除了{item_count}件商品）
🛒 准备购买下一件商品！
```

**Why auto-clear in post-payment?**
- User expects cart to be empty after successful order
- Cart items are from the order they just paid for
- Zepto hasn't synced yet, so items persist temporarily
- Clearing prevents confusion and duplicate orders

---

### Start Fresh Shopping (After Cart Cleared)
```
✅ 购物车已清空！
✅ 地址已确认：{address}
您想购买什么？ 🛒
```

---

**Key Difference:**
- **Normal flow**: ASK before clearing cart (user might want those items)
- **Post-payment flow**: AUTO-CLEAR cart (user knows those items are ordered)

---

## Safety & Best Practices

✅ **DO:**
- Check auth status before every order
- Confirm address with user
- Extract payment link accurately
- Send link via WhatsApp
- Let user complete payment

❌ **DON'T:**
- Never click "Pay" button
- Never store OTP
- Never auto-submit payment
- Never change address without user confirmation

---

## Error Handling

**Phone number invalid:**
```
“电话号码应该是10位数字。请重新输入。”
```

**OTP verification failed:**
```
“OTP验证失败。请重新发送OTP。
请查看手机上的新验证码。”
```

**Location not serviceable:**
```
⚠️ 您当前的位置无法使用Zepto的服务。
店铺可能暂时关闭或位于配送范围之外。
您想尝试其他地址吗？
```

**Item not found:**
```
“在Zepto上找不到{item}。请尝试其他搜索词。”
```

---

## Session Persistence

**After successful authentication:**
- Browser cookies persist login
- No need to re-authenticate for future orders
- Address selection persists
- Can directly proceed to shopping

**To check if authenticated:**
```
browser navigate url=https://www.zepto.com profile=openclaw
browser snapshot --interactive profile=openclaw
# 如果存在“profile”链接 → 表示用户已登录
# 如果存在“login”按钮 → 需要重新认证**