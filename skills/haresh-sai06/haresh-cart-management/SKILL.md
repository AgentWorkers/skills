---

**名称：haresh-cart-management**  
**描述：“通过n8n Webhook集成管理购物车操作”**  
**用户可调用：** 是  

---

# 购物车管理技能  

## 目的  
处理所有购物车操作，包括添加商品、删除商品以及更新商品数量。  

## 使用场景  
- 用户希望将商品添加到购物车中  
- 用户希望从购物车中删除商品  
- 用户希望更改商品的数量  

## 支持的操作  

### 添加商品到购物车  
1. 从用户消息中提取`product_id`  
2. 验证`product_id`的格式  
3. 检查商品数量（默认为1）  
4. 调用n8n Webhook：`http://localhost:5678/webhook/cart-add`  
5. 向用户确认操作成功  

### 从购物车中删除商品  
1. 提取要删除的`product_id`  
2. 检查当前商品数量  
3. 如果商品数量大于1，则请求用户确认  
4. 调用n8n Webhook：`http://localhost:5678/webhook/cart-remove`  
5. 在删除商品之前务必获得用户的确认  

### 更新商品数量  
1. 提取`product_id`和新的商品数量  
2. 验证数量是否为正整数  
3. 调用n8n Webhook：`http://localhost:5678/webhook/cart-update`  
4. 向用户确认数量更新成功  

## 安全规则  
- 绝不允许使用负数量  
- 在删除商品之前必须获得用户的确认  
- 在执行任何操作之前必须验证`product_id`是否存在