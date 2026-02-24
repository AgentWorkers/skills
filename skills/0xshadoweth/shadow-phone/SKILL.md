---
name: shadow-number
description: 获取一个一次性临时电话号码，并接收用于网站注册的OTP验证码，从而无需使用您的真实电话号码。该系统能够自动处理x402加密支付。
requires:
  env:
    - SHADOW_WALLET_KEY
---
**SHADOW_API_URL**: `https://extraordinary-charisma-production.up.railway.app`

**影子号码技能（Shadow Number Skill）**  
当您需要注册需要手机验证的网站，或者需要一个一次性使用的电话号码来接收OTP/SMS验证码时，可以使用此技能。  

**该技能的功能：**  
1. 调用Shadow API（通过x402认证机制；每次请求的费用约为0.10美元USDC）  
2. 为您选择的服务和国家返回一个临时电话号码  
3. 自动导航到目标网站，并将电话号码输入注册表单  
4. 每15秒轮询一次Shadow OTP端点，直到收到SMS验证码  
5. 输入验证码以完成验证  

---

**步骤1：选择服务代码**  
选择您要注册的网站对应的服务代码：  
| 网站 | 代码 |  
| --- | --- |  
| Telegram | `opt1` |  
| Facebook | `opt2` |  
| Google/Gmail | `opt7` |  
| WhatsApp | `opt29` |  
| Instagram | `opt36` |  
| Twitter/X | `opt48` |  
| Microsoft | `opt33` |  
| Apple | `opt42` |  
| PayPal | `opt15` |  
| Amazon | `opt22` |  
| Tinder | `opt38` |  
| Shopee | `opt49` |  

如果目标网站未在列表中，请使用该网站的名称进行搜索——API支持任何有效的SMSPVA服务代码。  

---

**步骤2：购买临时号码（需支付费用）**  
向Shadow API的购买端点发送POST请求：  
```json
POST https://extraordinary-charisma-production.up.railway.app/api/smspva/buy  
Content-Type: application/json  
{  
  "country": "US",  
  "service": "opt7"  
}  
```  
支持的国家代码：US、GB、FR、DE、IN、BR、PH、ID、NG、RU、UA、PL、CA、AU、MX等（共60多个国家）。  

**成功响应（状态码200）：**  
```json  
{  
  "statusCode": 200,  
  "data": {  
    "phoneNumber": "14155552671",  
    "orderId": "abc123",  
    "orderExpireIn": 600  
  }  
}  
```  
在网站上输入的完整号码格式为：`+{countryCode}{phoneNumber}`（例如：`+14155552671`）。  

如果收到非200状态的响应，请尝试其他国家或服务代码，然后重新购买号码。  

---

**步骤3：在网站上使用临时号码**  
1. 打开浏览器，导航到网站的注册或手机验证页面。  
2. 以国际格式输入电话号码（例如：`+14155552671`）。  
3. 点击“发送验证码”/“验证”/“获取OTP”按钮。  
4. 等待系统确认已发送短信。  

---

**步骤4：获取OTP验证码**  
收到短信后，每15秒轮询一次：  
```json  
GET https://extraordinary-charisma-production.up.railway.app/api/smspva/otp/{orderId}  
```  
**收到OTP验证码（状态码200）：**  
```json  
{  
  "statusCode": 200,  
  "data": {  
    "sms": { "code": "123456" },  
    "orderId": "abc123",  
    "orderExpireIn": 540  
  }  
}  
**注意**：提取`data.sms.code`作为验证码。  

**情况说明：**  
- 如果未收到验证码（状态码202），请等待15秒后重试。  
- 如果`orderExpireIn`变为0（订单已过期），请重新购买号码。  
- 如果收到状态码410（订单已关闭），请重新尝试。  

---

**错误处理：**  
- 如果号码无法使用或网站拒绝该号码：  
  ```json  
  PUT https://extraordinary-charisma-production.up.railway.app/api/smspva/refuse/{orderId}  
  ```  
  然后返回步骤2，重新购买号码。  
- 如果该号码被服务方禁止使用：  
  ```json  
  PUT https://extraordinary-charisma-production.up.railway.app/api/smspva/ban/{orderId}  
  ```  
  然后选择其他国家购买新的号码。  

---

**完整使用流程示例：**  
> 用户：“我用美国号码注册Telegram。”  
1. 发送请求：`POST https://extraordinary-charisma-production.up.railway.app/api/smspva/buy`（参数：`{country: "US", service: "opt1"}`）  
2. 收到响应：`phoneNumber: 14155552671`, `orderId: x9k2m`  
3. 打开Telegram网站并开始注册  
4. 输入`+14155552671`作为电话号码  
5. 每15秒轮询一次`https://extraordinary-charisma-production.up.railway.app/api/smspva/otp/x9k2m`  
6. 收到验证码`84712`  
7. 在Telegram中输入验证码`84712`，账户注册成功。  

---

**注意事项：**  
- 这些临时号码为一次性使用，有效期为`orderExpireIn`秒（通常为5–10分钟）。  
- 在网站输入号码时，请务必使用带有`+`前缀的国际格式。  
- 部分服务可能限制某些国家的号码使用；如果某个国家失败，请尝试其他国家。  
- x402认证费用（约0.10美元USDC）按每次购买号码收取，而非每次请求收取。