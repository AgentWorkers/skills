# WhatsApp 智能上下文管理器 - 技能指南

本技能为 WhatsApp 客户服务代理提供了一个基于人工智能的上下文管理系统，使他们能够即时访问客户历史记录、进行情感分析，并获得智能的回复建议。

## 快速安装

```bash
# Download and extract
unzip whatsapp-context-manager.zip
cd whatsapp-context-manager

# Verify installation (no dependencies needed!)
python install_check_whatsapp.py

# Run tests
python test_whatsapp.py

# Try examples
python examples_whatsapp.py
```

## 该系统能解决什么问题？

**在没有该系统的情况下：**
- ❌ 代理在收到客户消息时无法了解背景信息
- ❌ 无法判断客户是 VIP 还是首次来电
- 需要切换系统才能查看订单状态
- 无法判断消息的紧急程度
- 只能凭猜测回复，而非基于智能分析

**使用该系统后：**
- ✅ 2 秒内获取完整的客户信息
- ✅ 自动进行情感分析（愤怒/高兴/中立）
- ✅ 智能判断消息的优先级（紧急/高/普通/低）
- ✅ 直接显示订单状态
- ✅ 提供基于 AI 的回复建议
- ✅ 识别 VIP 客户

## 基本用法

### 1. 初始化系统

```python
from whatsapp_context_manager import ContextManager

# Create context manager (creates local database)
manager = ContextManager("production.db")
```

### 2. 处理收到的 WhatsApp 消息

```python
# When a WhatsApp message arrives
context = manager.process_incoming_message(
    phone="+1234567890",
    message_content="Where is my order?!",
    agent_id="agent_001"
)
```

### 3. 向代理显示上下文信息

```python
# Show agent what they need to know
print(f"Priority: {context.priority.value}")        # "critical"
print(f"Sentiment: {context.sentiment.value}")      # "negative"
print(f"Category: {context.category}")              # "order_status"
print(f"VIP Customer: {context.customer.is_vip}")   # True/False

# Key insights
for insight in context.key_insights:
    print(f"💡 {insight}")

# Warnings
for warning in context.warnings:
    print(f"⚠️ {warning}")

# Suggested responses
for response in context.suggested_responses:
    print(f"💬 {response}")
```

### 4. 发送回复

```python
# Agent sends reply
manager.send_message(
    phone="+1234567890",
    message_content="Your order #12345 is on the way!",
    agent_id="agent_001"
)
```

## 代理的界面示例（控制面板）

```
┌──────────────────────────────────────────────────────┐
│                  AGENT DASHBOARD                     │
├──────────────────────────────────────────────────────┤
│ Customer: +1234567890                                │
│ Name: John Doe                                       │
│ VIP: YES                                             │
├──────────────────────────────────────────────────────┤
│ Priority: CRITICAL                                   │
│ Sentiment: NEGATIVE                                  │
│ Category: ORDER_STATUS                               │
├──────────────────────────────────────────────────────┤
│ KEY INSIGHTS:                                        │
│   • 🌟 VIP Customer - Prioritize response            │
│   • 📦 Active Order: #ORD-12345 - shipped            │
│   • 🚚 Tracking: TRK-ABC123                          │
│   • ⚡ Customer expects fast replies (~2min)         │
├──────────────────────────────────────────────────────┤
│ WARNINGS:                                            │
│   • 🚨 CRITICAL: Requires immediate attention!       │
│   • 😡 Customer is very upset - handle with care     │
├──────────────────────────────────────────────────────┤
│ SUGGESTED RESPONSES:                                 │
│   1. Let me check your order status right away.     │
│   2. Your order #ORD-12345 is shipped.               │
└──────────────────────────────────────────────────────┘
```

## 核心功能

### 1. 自动情感分析

从消息中检测客户情绪：

```python
# System automatically analyzes sentiment
context = manager.process_incoming_message(phone, "This is TERRIBLE!", agent_id)
print(context.sentiment.value)  # "very_negative"

context = manager.process_incoming_message(phone, "Thanks!", agent_id)
print(context.sentiment.value)  # "positive"
```

**情绪等级：**
- 😡 `非常负面` - 愤怒、暴怒、可能存在欺诈
- 😟 `负面` - 失望、有问题
- 😐 `中立` - 询问信息、请求帮助
- 😊 `正面` - 表示感谢、感到满意
- 🤩 `非常正面` - 表示非常满意

### 2. 消息分类

自动对消息进行分类：

```python
# System automatically categorizes
context = manager.process_incoming_message(phone, "Where is my package?", agent_id)
print(context.category)  # MessageCategory.ORDER_STATUS

context = manager.process_incoming_message(phone, "Refund please!", agent_id)
print(context.category)  # MessageCategory.PAYMENT
```

**分类类别：**
- 📦 `订单状态` - 交付、追踪、物流信息
- 💳 `支付` - 退款、账单、交易问题
- 🔴 `投诉` - 存在问题、产品故障
- 🛍️ `产品咨询` - 价格、库存、产品特性
- 🆘 `支持` - 帮助、操作指南、常见问题
- 💰 `销售` - 购买、感兴趣
- ⭐ `反馈` - 评价、意见
- ❓ `其他` - 未分类

### 3. 优先级计算

根据多种因素智能判断消息的优先级：

```python
# System calculates priority
context = manager.process_incoming_message(
    phone="+1234567890",
    message_content="My payment failed!!!",
    agent_id="agent_001"
)
print(context.priority.value)  # "critical"
```

**优先级等级：**
- 🔴 `紧急` - 客户愤怒、存在支付问题、VIP 客户不满意
- 🟠 `高` - 投诉、情绪负面
- 🟡 `普通` - 一般性咨询
- 🟢 `低` - 信息请求、正面反馈

### 4. 回复建议

AI 会提供合适的回复建议：

```python
context = manager.process_incoming_message(
    phone="+1234567890",
    message_content="When will my order arrive?",
    agent_id="agent_001"
)

# Get suggestions
for response in context.suggested_responses:
    print(response)
# Output:
# "Let me check your order status right away."
# "Your order #12345 is currently shipped."
# "Expected delivery is tomorrow."
```

## 高级功能

### 订单集成

添加并跟踪客户订单：

```python
from whatsapp_context_manager import Order
from datetime import datetime, timedelta

# Add order to system
order = Order(
    order_id="ORD-12345",
    customer_id=context.customer.customer_id,
    status="shipped",
    amount=99.99,
    items=[
        {"name": "Wireless Headphones", "quantity": 1, "price": 99.99}
    ],
    created_at=datetime.now().isoformat(),
    updated_at=datetime.now().isoformat(),
    tracking_number="TRK-ABC123",
    estimated_delivery=(datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d")
)

manager.add_order(order)

# Now when customer asks about order, agent sees all details
context = manager.process_incoming_message(phone, "Order status?", agent_id)
print(context.active_orders[0].tracking_number)  # "TRK-ABC123"
```

### VIP 客户管理

标记并管理 VIP 客户：

```python
# Update customer to VIP
manager.update_customer_info(
    phone="+1234567890",
    name="John Doe",
    email="john@example.com",
    is_vip=True,
    tags=["premium", "loyal", "high-value"],
    notes="Always responds best to quick, direct answers"
)

# Future messages automatically show VIP status
context = manager.process_incoming_message(phone, "Hello", agent_id)
print(context.customer.is_vip)  # True
print(context.customer.tags)    # ["premium", "loyal", "high-value"]
```

### 对话历史记录

查看完整的对话历史：

```python
# Get context (includes recent messages)
context = manager.process_incoming_message(phone, "Need help", agent_id)

# View recent messages
for msg in context.recent_messages:
    direction = "Customer" if msg.direction == "inbound" else "Agent"
    print(f"{direction}: {msg.content}")
```

### 客户资料

查看客户的完整资料：

```python
context = manager.process_incoming_message(phone, "Hello", agent_id)

customer = context.customer
print(f"Phone: {customer.phone}")
print(f"Name: {customer.name}")
print(f"Total Messages: {customer.total_messages}")
print(f"VIP: {customer.is_vip}")
print(f"Tags: {customer.tags}")
print(f"Notes: {customer.notes}")
print(f"Last Contact: {customer.last_contact}")
print(f"Sentiment History: {customer.sentiment_history}")
```

## 常见使用场景

### 使用场景 1：查询订单状态

```python
# Customer: "Where is my order?"
context = manager.process_incoming_message(
    phone="+1234567890",
    message_content="Where is my order?",
    agent_id="agent_001"
)

# Agent sees:
if context.active_orders:
    order = context.active_orders[0]
    print(f"Order ID: {order.order_id}")
    print(f"Status: {order.status}")
    print(f"Tracking: {order.tracking_number}")
    print(f"Est. Delivery: {order.estimated_delivery}")

# Suggested response
print(context.suggested_responses[0])
# "Your order #ORD-12345 is shipped. Tracking: TRK-ABC123"
```

### 使用场景 2：处理愤怒的客户

```python
# Customer: "This is TERRIBLE! I want a refund NOW!!!"
context = manager.process_incoming_message(
    phone="+1234567890",
    message_content="This is TERRIBLE! I want a refund NOW!!!",
    agent_id="agent_001"
)

# System detects:
print(context.priority.value)   # "critical"
print(context.sentiment.value)  # "very_negative"

# Agent sees warnings:
for warning in context.warnings:
    print(warning)
# "🚨 CRITICAL: Requires immediate attention!"
# "😡 Customer is very upset - handle with care"

# Suggested response
print(context.suggested_responses[0])
# "I sincerely apologize for the inconvenience. Let me help resolve this."
```

### 使用场景 3：多客户优先级队列

```python
# Process messages from multiple customers
customers = [
    ("+1111111111", "Can I get some info?"),
    ("+2222222222", "My payment failed!!!"),
    ("+3333333333", "I have a complaint"),
    ("+4444444444", "Thanks for the help!"),
]

contexts = []
for phone, message in customers:
    context = manager.process_incoming_message(phone, message, "agent_001")
    contexts.append((phone, context))

# Sort by priority
priority_order = {
    MessagePriority.CRITICAL: 0,
    MessagePriority.HIGH: 1,
    MessagePriority.NORMAL: 2,
    MessagePriority.LOW: 3
}
contexts.sort(key=lambda x: priority_order[x[1].priority])

# Agent dashboard shows:
# 1. 🔴 +2222222222 - CRITICAL - Payment failed
# 2. 🟠 +3333333333 - HIGH - Complaint
# 3. 🟡 +1111111111 - NORMAL - Info request
# 4. 🟢 +4444444444 - LOW - Thank you message
```

### 使用场景 4：区分首次来电和重复来电的客户

```python
# System automatically tracks
context = manager.process_incoming_message(
    phone="+9999999999",  # New number
    message_content="Hello",
    agent_id="agent_001"
)

# Check if first time
if context.customer.total_messages == 1:
    print("👋 First time customer!")
    # Show introduction, onboarding info
else:
    print(f"📊 Returning customer ({context.customer.total_messages} messages)")
    # Show history, previous orders
```

## 集成示例

### 与 WhatsApp Business API 集成

```python
from whatsapp_business_api import WhatsAppClient
from whatsapp_context_manager import ContextManager

# Initialize
wa_client = WhatsAppClient(api_key="your_key")
manager = ContextManager("production.db")

# Handle incoming messages
@wa_client.on_message
def handle_message(phone, message):
    # Get context
    context = manager.process_incoming_message(
        phone=phone,
        message_content=message,
        agent_id="auto_agent"
    )
    
    # Display to agent dashboard
    display_to_agent(context)
    
    # If critical, alert supervisor
    if context.priority == MessagePriority.CRITICAL:
        notify_supervisor(context)
```

### 与 Web 控制面板集成

```python
from flask import Flask, jsonify
from whatsapp_context_manager import ContextManager

app = Flask(__name__)
manager = ContextManager()

@app.route('/api/message', methods=['POST'])
def process_message():
    data = request.json
    
    # Process message
    context = manager.process_incoming_message(
        phone=data['phone'],
        message_content=data['message'],
        agent_id=data['agent_id']
    )
    
    # Return context as JSON
    return jsonify(context.to_dict())
```

## 最佳实践

### 1. 始终通过系统处理所有消息

```python
# Good ✅
context = manager.process_incoming_message(phone, message, agent_id)
# Agent has full context

# Bad ❌
# Responding without context
send_reply_directly(phone, "Hello")  # Agent is blind
```

### 2. 标记 VIP 客户

```python
# Identify high-value customers early
if customer_is_high_value(phone):
    manager.update_customer_info(
        phone=phone,
        is_vip=True,
        tags=["high-value", "premium"]
    )
```

### 3. 跟踪订单

```python
# Add orders to system for automatic context
when_order_placed():
    manager.add_order(order)
    
# Now agents automatically see order status when customer asks
```

### 4. 使用系统提供的回复建议

```python
# Get AI suggestions
context = manager.process_incoming_message(phone, message, agent_id)

# Show to agent for quick selection
for i, response in enumerate(context.suggested_responses, 1):
    print(f"{i}. {response}")
```

### 5. 监控优先级队列

```python
# Get all pending messages
pending_contexts = get_all_pending_messages()

# Sort by priority
pending_contexts.sort(key=lambda x: priority_order[x.priority])

# Agents work from top (critical) to bottom (low)
```

## 性能优化技巧

### 1. 数据库管理

```python
# Use separate databases for different purposes
dev_manager = ContextManager("development.db")
prod_manager = ContextManager("production.db")
test_manager = ContextManager("test.db")
```

### 2. 批量处理

```python
# Process multiple messages efficiently
for phone, message in message_queue:
    context = manager.process_incoming_message(phone, message, agent_id)
    process_context(context)
```

### 3. 定期清理数据

```python
# Archive old conversations (optional)
# System stores everything by default
# Implement custom archival if needed
```

## 安全特性

- **本地存储**：所有数据存储在 SQLite 中
- **无外部依赖**：纯 Python 代码，不使用第三方库
- **数据完整性**：使用 SHA-256 校验和
- **安全查询**：参数化 SQL，防止注入攻击
- **隐私保护**：不会将数据发送到外部服务

## 故障排除

### 问题：数据库被锁定

```python
# Use different database per process
manager1 = ContextManager("agent1.db")
manager2 = ContextManager("agent2.db")
```

### 问题：测试数据过旧

```python
# Clean up test databases
import os
if os.path.exists("test.db"):
    os.remove("test.db")
```

### 问题：没有回复建议

```python
# Make sure orders are added to system
order = Order(...)
manager.add_order(order)
```

## 文件结构

```
whatsapp-context-manager/
├── whatsapp_context_manager.py  # Main library
├── examples_whatsapp.py         # 8 usage examples
├── test_whatsapp.py             # Complete test suite
├── README_WHATSAPP.md           # Full documentation
├── install_check_whatsapp.py    # Installation check
├── requirements_whatsapp.txt    # Dependencies (none!)
├── LICENSE_WHATSAPP             # MIT License
└── .gitignore_whatsapp          # Git ignore rules
```

## 系统要求

- Python 3.8 或更高版本
- 无需任何外部依赖库！

## 测试

```bash
# Run all tests
python test_whatsapp.py

# Should show:
# ✅ Sentiment analysis tests passed
# ✅ Message categorization tests passed
# ✅ Priority calculation tests passed
# ✅ Customer management tests passed
# ✅ Message storage tests passed
# ✅ Order management tests passed
# ✅ VIP customer tests passed
# ✅ Sentiment tracking tests passed
# ✅ Response suggestions tests passed
# ✅ Priority queue tests passed
# ✅ Conversation flow tests passed
# ✅ Context export tests passed
# ✅ ALL TESTS PASSED
```

## 示例

运行示例以体验系统功能：

```bash
python examples_whatsapp.py
```

示例包括：
1. 基本消息处理
2. 处理有活跃订单的客户
3. 处理愤怒客户的场景
4. VIP 客户的处理方式
5. 查看对话历史记录
6. 多客户优先级队列
7. 代理控制面板界面
8. 将上下文信息导出为 JSON 格式

## 获取帮助

- 📖 阅读完整文档：`README_WHATSAPP.md`
- 💻 查看示例代码：`examples_whatsapp.py`
- 🧪 运行测试：`test_whatsapp.py`
- 🐛 在 GitHub 上报告问题
- ⭐ 如果本工具对你有帮助，请给仓库点赞！

## 下一步操作

1. ✅ 安装并验证系统：`python install_check_whatsapp.py`
2. ✅ 运行测试：`python test_whatsapp.py`
3. ✅ 测试示例功能：`python examples_whatsapp.py`
4. ✅ 将系统集成到你的 WhatsApp 系统中
5. ✅ 根据需求进行定制

## 许可证

MIT 许可证 - 详情请参阅 `LICENSE_WHATSAPP` 文件

## 作者

**cerbug45**
- GitHub：[@cerbug45](https://github.com/cerbug45)

---

**将你的 WhatsApp 客户服务从被动响应式提升为主动服务吧！** 🚀