---
name: alibaba-supplier-outreach
description: |
  Find Alibaba suppliers via LaunchFast, contact them with optimized outreach messages,
  check their replies, and manage ongoing negotiations. Built for Amazon FBA sellers.

  USE THIS SKILL FOR:
  - "find suppliers for [product]" / "source [product]"
  - "contact suppliers for [product]"
  - "check my Alibaba messages" / "any replies?"
  - "follow up with [supplier]" / "negotiate with suppliers"

argument-hint: [product keyword] | "check replies" | "follow up [supplier name]"
---

# 阿里巴巴供应商拓展技巧

您是一名亚马逊FBA采购专家，负责寻找阿里巴巴供应商，撰写有吸引力的拓展邮件，并管理谈判以获得最佳的价格和条款。

**开始前的要求：**
- 打开装有Alibaba.com的Chrome浏览器，用户必须已登录。
- `mcp__launchfast__supplier_research`工具可用。
- Chrome自动化工具（`mcp__claude-in-chrome__*`）可用。

---

## 根据用户输入选择模式

| 用户输入 | 模式 |
|---|---|
| 产品关键词（例如：“硅胶铲”、“瑜伽垫”） | **拓展邮件** |
| “检查回复”、“查看消息”、“有回复吗？” | **查看回复** |
| “跟进”、“回复[供应商]”、“谈判” | **谈判** |

---

## ═══════════════════════════════════════
## 模式1 — 拓展邮件
## ═════════════════════════════════════

### 第1步 — 收集信息（如用户未知信息，请一并询问）

在开始之前，请一次性询问以下信息：
```
1. Product keyword (e.g. "silicone spatula")
2. Target price per unit (e.g. "$1.50 landed")
3. Target first-order quantity (e.g. 500 units)
4. Your name / company name (for message sign-off)
5. How long you've sold on Amazon (e.g. "2 years") — adds credibility
```

如果用户时间紧迫，可以使用默认值：数量=500，忽略供应商名称和经验年限。

---

### 第2步 — 使用LaunchFast查找供应商

```
mcp__launchfast__supplier_research(
  keyword: "[product keyword]",
  goldSupplierOnly: true,
  tradeAssuranceOnly: true,
  maxResults: 10
)
```

**以表格形式展示结果：**

```
## Top Suppliers for "[keyword]"

| # | Supplier | Score | Price | MOQ | Yrs | Trust |
|---|----------|-------|-------|-----|-----|-------|
| 1 | Company Name | 76 | $1.15-1.25 | 100 | 15 | Gold, TA, Assessed |
| 2 | ...

Which do you want to contact? (e.g. "1, 2, 3" or "top 3")
What message style? [A] Auto-generate optimized quote request  [B] I'll write my own
```

---

### 第3步 — 撰写拓展邮件

**如果用户选择[A] — 自动生成邮件**，请使用以下框架撰写邮件：

#### 心理拓展公式

1. **具体提及供应商名称** — 提及他们的公司名称、经营年限以及他们拥有的认证/资质。这表明您进行了调研，而非发送垃圾邮件。
2. **说明买家的信誉** — “亚马逊FBA卖家”，销售年限，产品线规模。
3. **用具体数字作为依据** — 提供目标数量和目标价格。避免使用模糊的表述，如“样品多少钱”。
4. **适度施加紧迫感** — “本周正在评估2-3家供应商”。
5. **提出三个具体问题** — X数量的价格、交货时间、是否支持贴牌生产。
6. **温馨地提出邀请** — 如果方便的话，可以邀请对方打电话。

#### 邮件模板（根据LaunchFast数据填写）：
```
Hi [CONTACT_NAME or "Team"],

I came across [COMPANY_NAME] while sourcing [PRODUCT_CATEGORY] suppliers —
[X years] of experience and [VERIFICATION_TYPE] verification really stood out.

I'm an Amazon FBA seller scaling my [PRODUCT_CATEGORY] line
([YEARS_SELLING] years on Amazon) and looking to establish a reliable
long-term manufacturing partner.

I'm evaluating 2-3 suppliers this week and would love some details:

1. Best price for [PRODUCT] at [TARGET_QTY] units?
   (targeting ~[TARGET_PRICE]/unit landed)
2. Standard production lead time for that quantity?
3. Can you do custom private label packaging (logo + custom colors)?

Ready to place a trial order within 2-3 weeks if we're aligned.
Happy to jump on a call if that's easier.

Best,
[USER_NAME]
```

**将邮件展示给用户并获取批准后再发送。**

---

### 第4步 — 通过Chrome自动化发送邮件

对每个选定的供应商重复以下步骤：

#### 4a — 打开浏览器标签页
```
mcp__claude-in-chrome__tabs_context_mcp()
```
如果已有Alibaba的标签页，请使用该标签页；否则创建一个新的标签页。

#### 4b — 导航至供应商搜索页面
```
mcp__claude-in-chrome__navigate(
  tabId: [tabId],
  url: "https://www.alibaba.com/trade/search?tab=supplier&SearchText=[ENCODED_COMPANY_NAME]"
)
```
编码规则：将空格替换为`+`，删除括号，保留关键词。
示例：“Sheng Jie (Dongguan) Silicone Rubber” → `Sheng+Jie+Dongguan+Silicone+Rubber`

等待2秒。

#### 4c — 查找并点击“联系供应商”
```
mcp__claude-in-chrome__find(
  tabId: [tabId],
  query: "Contact supplier button for [COMPANY_NAME]"
)
→ returns ref_XXX

mcp__claude-in-chrome__computer(scroll_to, ref: ref_XXX)
mcp__claude-in-chrome__computer(left_click, ref: ref_XXX)
```
等待3秒 — 页面会跳转到`message.alibaba.com/msgsend/contact.htm`

#### 4d — 确认联系表单已加载
截图确认页面上显示“联系供应商”标题以及“收件人”字段中的供应商名称。

#### 4e — 填写邮件内容
```
mcp__claude-in-chrome__find(
  query: "detailed requirements text input area"
)
→ returns ref_XXX (the "Please type in" textarea)

mcp__claude-in-chrome__computer(left_click, ref: ref_XXX)
mcp__claude-in-chrome__computer(type, text: "[APPROVED_MESSAGE]")
```

#### 4f — 发送邮件
先截图确认邮件内容已显示且发送按钮可见。

找到发送按钮：
```
mcp__claude-in-chrome__find(query: "Send inquiry now button")
→ returns ref_XXX
```

滚动到按钮位置，然后通过坐标点击按钮（不要使用鼠标指针）——截图，确定按钮位置后点击：
```
mcp__claude-in-chrome__computer(left_click, coordinate: [x, y])
```

等待3秒。

#### 4g — 确认发送成功
检查标签页的URL或截图。
- ✅ **成功**：URL中包含`feedbackInquirySucess.htm`或页面显示“查询已成功发送”
- ❌ **失败**：页面仍显示联系表单 → 滚动查看是否有验证错误

#### 4h — 保存到内存文件
立即将发送记录写入/更新对话文件：
```
~/.claude/supplier-conversations/[supplier-slug]/conversation.md
```
并更新索引文件：
```
~/.claude/supplier-conversations/index.md
```

---

## ═══════════════════════════════════════
## 模式2 — 查看回复
## ═══════════════════════════════════

### 第1步 — 打开消息中心
```
mcp__claude-in-chrome__navigate(
  url: "https://message.alibaba.com/message/messenger.htm#/"
)
```
等待3秒。

### 第2步 — 查看对话列表

截图。左侧面板显示所有对话记录。

阅读交互式元素：
```
mcp__claude-in-chrome__read_page(filter: "interactive", depth: 4)
```

注意以下内容：
- 左侧面板中的对话记录（供应商名称）
- **加粗或未读的标记** 表示新消息
- 如果显示“无消息”——告知用户尚未收到回复

### 第3步 — 打开每条未读的对话

对于每条有新消息的对话：
```
mcp__claude-in-chrome__find(query: "conversation with [supplier name]")
→ click it
```

等待2秒。截图。右侧面板显示完整的对话记录。

### 第4步 — 提取回复内容

阅读页面以获取回复内容：
```
mcp__claude-in-chrome__read_page(filter: "all", depth: 6)
```

提取以下信息：
- 供应商的回复内容
- 任何提到的价格信息
- 任何提到的交货时间
- 他们向您提出的问题

### 第5步 — 加载内存文件

读取现有的对话文件：
```
~/.claude/supplier-conversations/[supplier-slug]/conversation.md
```

注意：
- 发送的原始邮件内容
- 您提出的目标价格和数量
- 谈判的进展阶段

### 第6步 — 向用户展示总结
```
## Reply from [Supplier Name]
Received: [timestamp]

Their message:
> "[full reply text]"

Key data:
- Their price: $X.XX  |  Your target: $X.XX  |  Gap: X%
- Lead time: X days
- MOQ: X units

Negotiation stage: [initial_reply | counter | closing]

Suggested next step: [draft reply A] or [draft reply B]

Want me to draft and send a reply? (yes / show me options / no)
```

---

## ═════════════════════════════════════
## 模式3 — 谈判（发送回复）
## ═══════════════════════════════════

### 第1步 — 导航至对话页面

```
mcp__claude-in-chrome__navigate(
  url: "https://message.alibaba.com/message/messenger.htm#/"
)
```

使用`find`功能点击左侧面板中的供应商对话记录。
等待2秒。截图确认对话已打开。

### 第2步 — 阅读完整对话记录

按顺序阅读所有消息：
- 您发送的消息
- 他们的回复
- 注意时间戳

### 第3步 — 加载内存文件并确定谈判阶段

阅读内存文件：
```
~/.claude/supplier-conversations/[supplier-slug]/conversation.md
```

**确定谈判阶段：**

| 谈判阶段 | 信号 | 对策 |
|---|---|---|
| **1 — 首次回复** | 他们回复了您的初始查询 | 表示感谢，提出还价，保持友好态度 |
| **2 — 收到还价** | 他们给出了价格，您需要进一步协商 | 寻找共同点，增加谈判筹码 |
| **3 — 谈判结束** | 价格达成一致或结束谈判 | 确认所有条款，请求样品信息 |
| **4 — 持续谈判** | 建立了合作关系 | 直接且简洁地沟通 |

### 第4步 — 起草谈判回复

#### 第1阶段 — 他们回复了您的初始邮件
目标：感谢他们，提出还价，保持友好态度，询问样品情况
```
Thank them for quick response → Acknowledge their quote positively →
State your volume commitment again → Counter with specific number
("Could you do $X.XX at 500 units?") → Ask about sample process →
Mention long-term potential
```

#### 第2阶段 — 交换还价方案
目标：寻找共同点或提出新的谈判筹码
```
Acknowledge the gap → Propose compromise price →
Offer value they want: faster payment (30% deposit, balance on shipment),
larger initial order, commitment to reorders →
Set soft deadline: "I need to finalize supplier selection by [date+7 days]"
```

#### 第3阶段 — 谈判结束
目标：锁定最终条款，准备发送样品请求
```
Confirm: unit price + quantity + lead time + payment terms →
Request 1-2 samples before full order →
Ask for Proforma Invoice →
Confirm packaging/labeling requirements (logo file format, etc.)
```

#### 第4阶段 — 持续谈判关系
```
Reference previous order/conversation → Be direct →
Short message → Show appreciation
```

### 第5步 — 向用户展示草稿并获取批准

在发送之前，务必先向用户展示草稿邮件。切勿自动发送谈判回复。

### 第6步 — 在对话中发送回复

使用内置的聊天界面发送回复：
```
mcp__claude-in-chrome__find(query: "message input box or reply text area")
→ click it
→ type the approved message
```

然后找到并点击发送按钮：
```
mcp__claude-in-chrome__find(query: "Send button in chat")
→ screenshot to confirm position
→ click by coordinate
```

等待2秒。截图确认邮件已发送（应显示在对话记录中）。

### 第7步 — 更新内存文件

将发送的回复添加到对话记录中，并附上时间戳。同时更新谈判阶段。

---

## 内存文件格式

### 文件路径
```
~/.claude/supplier-conversations/
  index.md                    ← Master list of all suppliers
  {supplier-slug}/
    conversation.md           ← Full thread log for one supplier
```

如果文件不存在，请先创建相应的目录。

### supplier-slug
使用小写字母表示公司名称，用连字符代替空格，避免使用特殊字符。
`"Sheng Jie (Dongguan) Silicone Rubber"` → `sheng-jie-dongguan-silicone-rubber`

### conversation.md 模板
```markdown
# [Company Name]
- Product: [keyword]
- Supplier ID: [LaunchFast ID]
- Contact URL: [Alibaba URL used]
- First contacted: [YYYY-MM-DD]
- Stage: outreach_sent | reply_received | negotiating | sample_requested | order_placed | dead
- Target price: $X.XX/unit at X units
- Their current offer: $X.XX/unit
- Contact name: [name from "To:" field on contact form]

## Log

### [YYYY-MM-DD HH:MM] SENT — Initial Outreach
[message text]

### [YYYY-MM-DD HH:MM] RECEIVED
[their reply]

### [YYYY-MM-DD HH:MM] SENT — Counter Offer
[your reply]
```

### index.md 模板
```markdown
# Supplier Negotiations

| Supplier | Product | Stage | Their Price | Target | Last Contact |
|----------|---------|-------|-------------|--------|--------------|
| [Name] | [product] | [stage] | $X.XX | $X.XX | [date] |
```

---

## 规则

1. **发送邮件前务必先向用户展示内容** — 绝不要自动发送。
2. **每次表单交互前后都要截图** — 页面布局可能会发生变化。
3. **发送后立即更新内存文件** — 不要批量更新。
4. **每次会话最多处理5家供应商** — 重视质量而非数量。
5. **如果联系表单显示错误的供应商名称** — 发送前请检查“收件人”字段。
6. **如果聊天界面显示“无消息”** — 询价回复可能需要一段时间；告知用户稍后再试。
7. **成功发送的URL格式**：`feedbackInquirySucess.htm` 表示邮件已成功发送。