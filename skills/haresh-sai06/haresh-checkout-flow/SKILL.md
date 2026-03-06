---  
**名称：haresh-checkout-flow**  
**描述：“通过 n8n Webhook 集成处理电子商务结账流程”**  
**用户可调用：** 是  

---

# 结账流程技能（Checkout Flow Skill）  

## 目的  
管理完整的结账流程，包括商品验证、身份验证、配送和支付。  

## 使用场景  
- 用户希望结账或下单  
- 用户请求进行支付  
- 用户希望完成购买  

## 工作流程（Workflow）  

### 第 1 步：验证购物车（Step 1: Validate Cart）  
调用 n8n Webhook（地址：`http://localhost:5678/webhook/checkout-validate`），检查购物车中商品的可用性和库存状态。  

### 第 2 步：检查身份验证（Step 2: Check Authentication）  
根据用户上下文判断用户是否已登录。如果是未登录的用户（即“访客”），提供登录选项或允许其以访客身份继续操作。  

### 第 3 步：收集配送信息（Step 3: Collect Shipping Information）  
向已登录的用户显示保存的配送地址；对于未登录的用户，则收集配送相关信息。  

### 第 4 步：处理支付（Step 4: Payment Processing）  
向用户展示支付选项，并调用 n8n Webhook（地址：`http://localhost:5678/webhook/checkout-process`）进行支付处理。  

### 第 5 步：确认订单（Step 5: Order Confirmation）  
向用户显示订单摘要，并获取最终确认。  

## 安全要求（Security Requirements）  
- 通过 JWT 令牌验证用户的身份状态  
- 绝不对用户的支付信息进行存储或记录  
- 在将数据发送到后端之前，对所有输入进行严格验证  

## 错误处理（Error Handling）  
- 如果购物车验证失败，显示具体错误信息  
- 如果支付失败，允许用户尝试其他支付方式  
- 如果库存发生变化，及时通知用户