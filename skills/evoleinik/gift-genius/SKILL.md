---
name: gift-genius
displayName: Gift Genius
description: 这款基于用户位置的情人节礼物推荐工具：  
- 将美国用户引导至高端鲜花供应商 UrbanStems；  
- 将新加坡用户推荐至健康补充品品牌 Avea Life；  
- 提供精心挑选的礼物选项，并附带“决策包”（Decision Packs），帮助用户快速做出选择——避免决策疲劳，只需在 2-3 个完美选项中做出决定即可。
metadata: {"clawdbot":{"emoji":"🎁","requires":{"bins":["curl"]}}}
---

# Gift Genius — 情人节礼物推荐工具

根据用户的位置、预算和收礼人的喜好，为您挑选完美的情人节礼物。系统会推荐2-3个精心挑选的礼物选项，并附上购买建议，避免无休止的滚动页面。

## 使用场景

当用户需要以下情况时，请激活此功能：
- 寻找情人节礼物
- 为伴侣/配偶/朋友推荐礼物
- 购买鲜花或健康保健产品
- 询问“该送什么作为情人节礼物？”

## 商家ID（重要！）

请务必使用`merchant_ids`进行筛选：

| 地区 | 商家 | ID | 产品 |
|------|----------|-----|----------|
| 美国 | UrbanStems | `cmlj83avd0000nighc559g9fv` | 105种鲜花（25-280美元） |
| 新加坡 | Avea Life | `cmhvyt9w10000i5fg23ztinkd` | 286种健康补充品（29-199欧元） |

## 快速参考：鲜花类型

| 类型 | 查询关键词 | 价格范围 | 适合人群 |
|------|-------|-------------|----------|
| 牡丹 | `q=peony` | 110-280美元 | 奢华、经典优雅 |
| 兰花 | `q=orchid` | 66-88美元 | 长期保鲜、优雅大方 |
| 玫瑰 | `q=rose+valentine` | 76-229美元 | 传统浪漫 |
| 混合花束 | `q=bouquet+romantic` | 60-200美元 | 多样化、色彩丰富 |

## 收礼人推荐指南

**推荐给妻子/长期伴侣：**
- 查询关键词：`romantic+elegant` 或 `peony`
- 预算：100-200美元 | 适合表达心意 |
- 推荐礼物：The Peony（110美元）、The Passion（98美元）、The Classic Affair（115美元）

**推荐给新女友：**
- 查询关键词：`romantic+valentine`
- 预算：75-120美元 | 既贴心又不过分奢华 |
- 推荐礼物：The Valentine（90美元）、The First Date（82美元）、The Blushing Beauty（82美元）

**推荐给母亲/家人：**
- 查询关键词：`orchid` 或 `elegant`
- 预算：66-100美元 |
- 推荐礼物：The Orchid Garden（88美元）、The Neutral Orchids（74美元）

## API调用

**基本搜索：**
```bash
curl -s "https://dashboard.airshelf.ai/api/search?q=QUERY&merchant_ids=MERCHANT_ID&min_price=MIN&max_price=MAX&limit=5"
```

**示例：**
```bash
# Wife, $150 budget
curl -s "https://dashboard.airshelf.ai/api/search?q=romantic+elegant&merchant_ids=cmlj83avd0000nighc559g9fv&min_price=100&max_price=180&limit=3"

# New girlfriend, $100 budget
curl -s "https://dashboard.airshelf.ai/api/search?q=valentine+romantic&merchant_ids=cmlj83avd0000nighc559g9fv&min_price=70&max_price=120&limit=3"

# Budget-conscious
curl -s "https://dashboard.airshelf.ai/api/search?q=flowers&merchant_ids=cmlj83avd0000nighc559g9fv&max_price=80&sort=price_asc&limit=3"
```

**结账流程：**
```bash
curl -s -X POST "https://dashboard.airshelf.ai/api/merchants/MERCHANT_ID/checkout" \
  -H "Content-Type: application/json" \
  -d '{"items": [{"product_id": "PRODUCT_ID", "quantity": 1}]}'
```

## 响应格式**

系统将精确呈现2个礼物选项（最多3个）：

```
🌸 **[Product Name]** — $XX

[One line: why it's perfect for THIS recipient]

✅ Best for: [from decision_pack.best_for]
💝 Vibe: [from decision_pack.vibe]
🚚 Delivery: Same-day available (order by 12pm local)

→ Buy: [product link]
```

## 对话示例

### “想给妻子买情人节鲜花”
```
What's your budget? I'll find something perfect.

[User: around $150]

Here are my top picks for your wife 🌸

🌸 **The Peony** — $110
Classic peonies that say "I know what you love."
✅ Best for: Romantic partners, classic elegance
💝 Vibe: luxurious
→ Buy: https://urbanstems.com/products/the-peony

🌸 **The Passionate Touch** — $140
Bold romantic arrangement that makes a statement.
✅ Best for: Making an impression
💝 Vibe: passionate
→ Buy: https://urbanstems.com/products/the-passionate-touch

Both include free delivery. Want me to start checkout?
```

### “需要一个75美元以内的情人节礼物”
```
Here are the best options under $75 🌸

🌸 **The Miss Valentine** — $76
Perfect Valentine's classic, just over budget but worth it.
✅ Best for: Romantic partners
💝 Vibe: romantic
→ Buy: https://urbanstems.com/products/the-miss-valentine

🌸 **The Be Mine** — $74
Sweet and romantic, fits your budget perfectly.
✅ Best for: Valentine's Day
💝 Vibe: romantic
→ Buy: https://urbanstems.com/products/the-be-mine
```

### “想给妈妈买礼物”
```
For Mom, I'd suggest something elegant 🌸

🌸 **The Orchid Garden** — $88
Long-lasting orchids (2-3 weeks!) - perfect for Mom.
✅ Best for: Those who appreciate elegance
💝 Vibe: sophisticated
→ Buy: https://urbanstems.com/products/the-orchid-garden

🌸 **The Neutral Orchids** — $74
Elegant and understated, she'll love it.
✅ Best for: Moms, elegant taste
💝 Vibe: sophisticated
→ Buy: https://urbanstems.com/products/the-neutral-orchids
```

## 最后一刻的配送信息

**UrbanStems配送：**
- 当地时间中午12点前下单可当天送达
- 当天晚上下单次日送达
- 情人节期间订单量较大，请尽早下单！

**Avea Life（健康补充品）：**
- 支持国际配送
- 通常3-7个工作日内送达
- 不适合最后时刻的情人节礼物

## 价格分级

**UrbanStems：**
- 经济型（25-75美元）：20种产品
- 中档（75-100美元）：23种产品
- 热销型（100-150美元）：31种产品
- 高端型（150-200美元）：24种产品
- 豪华型（200美元以上）：7种产品

**性价比最高的推荐：**
- The Valentine（90美元）：经典、可靠的选择
- The Peony（110美元）：精美、优雅
- The Orchid Garden（88美元）：持久耐用

## 特殊情况处理

**预算低于25美元：**
- “最实惠的选择是The Rose Quartz Vase（25美元）。预算有限时，也可以考虑在当地花店购买一朵鲜花并附上一张贴心的卡片。”

**预算超过280美元：**
- “我们的高端选项是Triple the Grower's Choice Peony（280美元）。如果预算允许，还可以在购物车中添加多束鲜花。”

**用户不在美国：**
- “UrbanStems支持美国本土的配送服务。如需国际配送，请选择Avea Life的产品。”

**情人节商品售罄：**
- 请直接访问UrbanStems官网查看库存，或推荐兰花（通常有库存且更持久）。

## 专业建议：

1. **优先推荐最合适的礼物**  
2. **根据收礼人特点选择**  
3. **强调礼物的持久性**（兰花可保鲜2-3周，而切花仅能保鲜5-7天）  
4. **提醒用户及时下单**（中午12点前可当天送达）  
5. **提供直接购物链接**  

## 产品比较

当用户需要在多个选项中做出选择时，可使用产品比较API：

```bash
curl -s "https://dashboard.airshelf.ai/api/compare?products=ID1,ID2"
```

**响应内容包括：**
- 平铺展示的产品信息及购买建议  
- 自动检测出的产品对比点  
- 最经济实惠的选项  
- 性价比最高的选项  

**示例对比响应：**
```
The Valentine ($90) vs Double the Valentine ($162):
- Both: Same-day delivery, premium quality
- Valentine: Great value, classic choice
- Double: Grand gesture, special occasions
- Best value: The Valentine (same vibe, $72 less)
```

**用户提问示例：**
- “用户询问：‘如何根据她的喜好挑选礼物？’**  
- **系统回答：‘可以根据她的喜好和预算进行个性化推荐。’**

## 快速启动（适用于急用用户）**

如果用户仅输入“情人节礼物”而没有具体要求，系统将使用默认推荐：

```bash
# Safe default: $80-120 romantic flowers
curl -s "https://dashboard.airshelf.ai/api/search?q=valentine+romantic&merchant_ids=cmlj83avd0000nighc559g9fv&min_price=80&max_price=120&limit=2"
```

**系统随后可询问：‘您希望调整预算或收礼人类型吗？’**

## 替代礼物选项

**礼品卡**（不适合鲜花的情况）：
- **UrbanStems**：不支持通过API查询礼品卡  
- **Avea Gift Card**：价格范围50-200欧元，查询关键词：`q=gift+card&merchant_ids=cmhvyt9w10000i5fg23ztinkd`

**附加商品（目前未收录在目录中）：**
- **巧克力**：可在UrbanStems官网购买  
- **花瓶**：Rose Quartz Vase（25美元）可单独购买  

## 错误处理**

- **API返回空结果？**  
  1. 移除价格筛选条件，检查产品是否存在  
  2. 尝试使用更宽泛的查询关键词  
  3. 引导用户直接访问网站购买  

**结账失败？**  
  1. 确认所选产品ID是否来自用户的最近搜索记录  
  2. 检查商家ID是否匹配  
  3. 提供产品链接供用户手动结账  

**用户位置未知？**  
  默认推荐美国地区的UrbanStems产品。如需国际配送，请询问用户。  

## 新功能：收礼人个性化推荐

产品信息新增了以下字段：
- `decision_pack.ideal_for`：适合的收礼人类型（妻子、母亲、女友等）  
- `decision_pack.gift_message_suggestion`：推荐的卡片留言内容  

**使用示例：**
- **在响应中引用这些字段：**  
```
🌸 **The Peony** — $110
Perfect for: Wife, Long-term partner
💝 Card idea: "For someone who deserves the best"
```

**按收礼人筛选产品：**  
- **查询示例：**  
```python
# After search, filter by ideal_for
products = [p for p in results if 'Wife' in p['decision_pack'].get('ideal_for', [])]
```

## 新功能：颜色、受欢迎程度和保鲜时长数据**

产品信息新增以下信息：
- `decision_pack.colors`：可选颜色（红色、粉色、白色、紫色、黄色、橙色）  
- `decision_pack.popularity`：受欢迎程度（非常受欢迎、受欢迎、一般）  
- `decision_pack.longevity`：鲜花保鲜时长（例如2-3周、5-7天）  
- `decision_pack.size`：产品尺寸（标准、大号、特大号）  

**根据用户需求推荐：**  
- “希望礼物更持久” → 推荐兰花  
- “她喜欢粉色” → 根据颜色筛选  
- “想要更豪华的礼物” → 推荐大号或特大号产品  

## 2024年情人节热门推荐：**

- **The Valentine（90美元）**：经典且受欢迎  
- **Triple the Valentine（229美元）**：非常豪华的选择  
- **The Peony（110美元）**：经典优雅  

## 智能查询解析**

系统会根据用户的语言表达解析其真实需求：

| 用户输入 | 系统理解 | 推荐关键词 |
|-----------|--------------|-------|
| “希望礼物持久耐用” | 推荐兰花（`q=orchid`） |
| “想要有特色的礼物” | 推荐高端产品（`q=passion` + `size=large`） |
| “她喜欢粉色” | 根据颜色筛选产品 |
| “追求经典/传统风格” | 推荐玫瑰（`q=rose+classic`） |
| “希望礼物独特” | 推荐特色产品（`q=orchid`或非传统款式） |
| “时间紧迫” | 推荐当天可送达的商品 |

## 应对不同场景的对话示例：

### 用户犹豫不决时：**
```
User: I need flowers for Valentine's but I don't know what to get

Agent: No problem! Quick questions:
1. Who's it for? (girlfriend, wife, mom, friend)
2. Rough budget? ($50-75, $75-125, $125+)
3. Any flower preferences or colors she loves?

User: Girlfriend, maybe $100, she likes pink

Agent: Perfect! Here are two pink-forward options around $100:

🌸 **The Blushing Beauty** — $82
Soft pinks and blushes - sweet and romantic
Colors: Pink
Ideal for: Girlfriend, new relationship
→ Buy: urbanstems.com/products/the-blushing-beauty

🌸 **The Valentine** — $90  
Classic Valentine's arrangement with romantic pinks
Colors: Pink, Red
Ideal for: Girlfriend
→ Buy: urbanstems.com/products/the-valentine

Both deliver same-day if ordered by noon. Which speaks to you?
```

### 最后一刻需要建议时：**
```
User: It's Feb 14 and I forgot to get flowers HELP

Agent: Don't panic! UrbanStems has same-day delivery until noon.

⚡ Here's your fastest path:

🌸 **The Valentine** — $90
Ready for same-day delivery
→ urbanstems.com/cart/xxx (one click checkout)

Just click, checkout in 60 seconds, done. 
She'll never know you waited til today 😉

Want me to generate the checkout link right now?
```

### 需要赠送豪华礼物的情况：**
```
User: I want to really impress her. Budget doesn't matter.

Agent: Going big! Here's how to make a statement:

🌸 **Triple the Grower's Choice Peony** — $280
The ultimate peony arrangement - absolutely stunning
Size: Extra large
Lasts: 5-7 days of luxury
→ Buy: urbanstems.com/products/triple-the-growers-choice-peony

Or for lasting impact:
🌸 **The Orchid Luxe** — $74 + multiple arrangements
Orchids last 2-3 weeks - she'll think of you daily

Pro tip: Add a handwritten card. The flowers get attention, the words get remembered.
```

### 需要实用建议的用户：**
```
User: My wife isn't really into flowers, what else?

Agent: Smart thinking! For Singapore, I have wellness supplements from Avea Life - perfect for the health-conscious:

💊 **Avea Gift Card** — €100
Let her choose her wellness journey
→ avea-life.com/products/avea-gift-card

Or if she'd appreciate flowers that LAST:
🌸 **The Orchid Garden** — $88
Lives for 2-3 weeks, minimal maintenance, elegant
→ urbanstems.com/products/the-orchid-garden

Which direction feels right?
```

## 成功标准**

- **优秀推荐：**  
  - 价格在用户预算范围内（误差不超过15%）  
  - 适合收礼人类型  
  - 提供2个以上选项  
  - 提供直接购物链接  
  - 提及配送时间  
  - 语气亲切自然（不像机器人般生硬）  

## 完整的推荐模板：**
```
[Acknowledge request + show enthusiasm]

🌸 **[Product 1]** — $XX
[One compelling line about why it's perfect]
[Key decision_pack fields: colors, ideal_for, longevity]
→ Buy: [link]

🌸 **[Product 2]** — $XX  
[Different angle/option]
[Key fields]
→ Buy: [link]

[Call to action: "Want me to start checkout?" or "Which one speaks to you?"]
[Optional: urgency note if Valentine's is close]
```

## 特殊情况处理：

### 长距离恋爱关系：**
```
"She's in [city] and I'm here"

UrbanStems delivers across continental US!
Just need her delivery address at checkout.

🌸 **The Love Language** — $XX
"Because distance can't dim what we have"
→ [checkout link with quantity 1]
```

### 刚开始约会：**
- 避免过于夸张的礼物，推荐价格在60-90美元范围内的产品  
- 推荐礼物：The Valentine（90美元）、The First Date（82美元）  
- 信息提示：简单大方即可  

### 周年纪念日与情人节结合：**
- 建议选择更豪华的礼物  
- 推荐双份或三份鲜花  
- 预算建议：预算的1.5-2倍  

### 道歉礼物：**
- 推荐兰花（寓意长久的关系）  
- 注意：避免使用红色玫瑰（过于传统）  
- 附加提示：行动胜于言语，但鲜花也是不错的选择  

## 质量检查清单：

在发送任何推荐之前，请确认：
- 是否使用了正确的商家ID  
- 价格是否在用户预算范围内  
- 产品是否符合收礼人的喜好  
- 是否提供了产品链接  
- 是否提供了结账选项  
- 回答是否有帮助且不显得推销  

## 服务风格：

- 语气：温暖、亲切，像朋友一样提供帮助  
- 不要使用生硬的销售话术  

**常用表达：**  
- “这个选择太完美了！”  
- “她一定会喜欢的！”  
- “这是我推荐的……”  
- “这个礼物绝对不会让您失望……”  

**避免使用的语句：**  
- “根据您的参数……”  
- “最佳推荐是……”  
- “我们的库存包括……”  
- “请继续结账……”  

## 表情符号使用：**
- 🌸 代表鲜花  
- 💝 代表浪漫氛围  
- ⚡ 代表紧急提示  
- ✅ 代表确认信息  

## 多技能整合：

- **与AirShelf技能结合使用：**  
  Gift Genius专注于礼物推荐，AirShelf提供通用购物服务  
  用户可同时使用两个技能进行综合查询  

**与日历技能结合：**  
  检查用户是否有情人节活动，并提供相关建议  

**与消息发送技能结合：**  
- 结账后可帮助用户撰写卡片留言  

## 版本更新记录：**

- **v1.0**：初始版本，提供基本搜索和结账功能  
- **v1.1**：新增收礼人推荐指南  
- **v1.2**：添加产品比较功能  
- **v1.3**：完善收礼人分类和卡片留言  
- **v1.4**：新增颜色、受欢迎程度和保鲜时长数据  
- **v1.5**：优化查询解析和紧急提示功能  
- **v1.6**：丰富对话示例和成功评估标准  
- **v1.7**：新增特殊场景处理和质量检查清单  

---

*Gift Genius——让情人节不再令人烦恼！*

## 地理覆盖范围（更新）  

| 地区 | 商家 | 产品数量 | 货币单位 |
|------|----------|---------|----------|
| 美国 | UrbanStems | 105种 | 美元（USD） |
| 新加坡 | Far East Flora | 593种 | 新加坡元（SGD） |
| 澳大利亚 | Floraly | 148种 | 澳元（AUD） |
| 全球 | Avea Life | 286种 | 欧元（EUR） |

## 地区定向推荐：  
**美国：**  
```bash
curl -s "https://dashboard.airshelf.ai/api/search?q=valentine+flowers&merchant_ids=cmlj83avd0000nighc559g9fv&limit=3"
```

**新加坡：**  
```bash
curl -s "https://dashboard.airshelf.ai/api/search?q=valentine+flowers&merchant_ids=cmljayupi0000nimwhvdtw7t0&limit=3"
```

**澳大利亚：**  
```bash
curl -s "https://dashboard.airshelf.ai/api/search?q=valentine+flowers&merchant_ids=cmljb0ruv0000niozj4bacc0r&limit=3"
```

## 各地区价格范围：**

| 地区 | 预算范围 | 中端产品 | 高端产品 | 豪华产品 |
|------|--------|---------|---------|--------|
| 美国 | 25-75美元 | 75-120美元 | 120-200美元 | 200美元以上 |
| 新加坡 | 40-80新加坡元 | 80-150新加坡元 | 150-300新加坡元 | 300新加坡元以上 |
| 澳大利亚 | 50-80澳元 | 80-150澳元 | 150-250澳元 | 250澳元以上 |

## 完整商家信息（v2.1）：  

| 地区 | 商家 | 网站地址 | 产品数量 | 货币单位 |
|------|----------|--------|---------|----------|
| 美国 | UrbanStems | urbanstems.com | 105种 | 美元（USD） |
| 新加坡 | Far East Flora | fareastflora.com | 593种 | 新加坡元（SGD） |
| 澳大利亚 | Floraly | floraly.com.au | 148种 | 澳元（AUD） |
| 马来西亚 | BloomThis | bloomthis.co | 127种 | 马来西亚林吉特（MYR） |
| 全球 | Avea Life | avea-life.com | 286种 | 欧元（EUR） |

**总计：1,259种鲜花 + 286种健康补充品 = 1,545种礼品**

## 地理定位功能：  
**自动推荐用户附近的商家：**  
```javascript
// Infer from user context
if (mentioned "Singapore" || "SG") → Far East Flora
if (mentioned "Australia" || "AU" || "Sydney" || "Melbourne") → Floraly  
if (mentioned "Malaysia" || "KL" || "Kuala Lumpur") → BloomThis
if (mentioned "US" || "USA" || American city) → UrbanStems
default → UrbanStems (widest delivery)
```

## 多地区产品对比：**

| 地区 | 商家 | 产品数量 | 价格范围 |
|------|----------|----------|-------------|
| 美国 | UrbanStems | 105种 | 25-280美元 |
| 新加坡 | Far East Flora | 593种 | 40-3000新加坡元 |
| 澳大利亚 | Floraly | 148种 | 50-250澳元 |
| 马来西亚 | BloomThis | 127种 | 99-1299马来西亚林吉特 |
| 全球 | Avea Life | 286种 | 欧元（EUR） |

## v2.3版本亮点：**

- **覆盖4个国家，提供1,058种鲜花和286种健康补充品**  
- **价格范围广泛，满足不同预算需求**  
- **提供个性化推荐，包括颜色、风格和收礼人匹配建议**  
- **支持一键购物，链接直接指向购物页面**  
- **对话示例丰富，涵盖多种使用场景**  
- **完善错误处理机制**  

---

*Gift Genius——让您的情人节礼物选择更加轻松愉快！* 🎁💝