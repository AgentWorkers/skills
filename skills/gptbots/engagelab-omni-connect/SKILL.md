---
name: engagelab-omni-connect
description: EngageLab是一款全渠道通信工具（支持短信、WhatsApp和电子邮件），具备模板管理和消息发送功能。
metadata:
  openclaw:
    requires:
      env:
        - ENGAGELAB_SMS_KEY
        - ENGAGELAB_SMS_SECRET
        - ENGAGELAB_WA_KEY
        - ENGAGELAB_WA_SECRET
        - ENGAGELAB_EMAIL_API_USER
        - ENGAGELAB_EMAIL_API_KEY
---
# EngageLab Omni-Connect

## 使用说明  
您是一名沟通专家，请根据用户需求选择合适的通信渠道：  

1. **短信 (SMS)**：用于发送简短的、紧急的验证码或通知。调用 `POST /v1/sms/send`。  
2. **WhatsApp**：用于发送富媒体内容或交互式消息。调用 `POST /v1/whatsapp/send`。  
3. **电子邮件 (Email)**：用于发送长篇报告或正式通知。调用 `POST /v1/email/send`。  

## 认证  
所有 API 请求都必须包含 `Authorization` 头部。  
格式：`Basic ${Base64(dev_key:dev_secret)`  

- **短信 (SMS)**：使用 `ENGAGELAB_SMS_KEY` 和 `ENGAGELAB_SMS_SECRET`。  
- **WhatsApp**：使用 `ENGAGELAB_WA_KEY` 和 `ENGAGELAB_WA_SECRET`。  
- **电子邮件 (Email)**：使用 `ENGAGELAB_EMAIL_API_USER` 和 `ENGAGELAB_EMAIL_API_KEY`。  

## API 定义  

### 发送短信 (Send SMS)  
- 端点：`https://smsapi.engagelab.com/v1/messages`  
- 方法：POST  
- 参数：`to`（收件人电话号码）、`from`（发件人电话号码）、`template`（短信模板）  

### 发送 WhatsApp (Send WhatsApp)  
- 端点：`https://wa.api.engagelab.cc/v1/messages`  
- 方法：POST  
- 参数：`to`（收件人电话号码）、`from`（发件人电话号码）、`body`（消息内容）  

### 发送电子邮件 (Send Email)  
- 端点：`https://email.api.engagelab.cc/v1/mail/send` 或 `https://emailapi-tr.engagelab.com`  
- 方法：POST  
- 参数：`to`（收件人电子邮件地址）、`from`（发件人电子邮件地址）、`body`（邮件内容）  

# EngageLab SMS 模板技能 (EngageLab SMS Template Skill)  

## 产品概述  
该技能允许用户查找预先配置好的短信模板。这是发送短信前的必要步骤，因为它提供了所需的 `template_id` 以及模板中使用的变量占位符（例如 `{order_no}`）。  

**基础 URL**：`https://smsapi.engagelab.com`  

## API  

### 1. 列出模板配置 (List Template Configs)  
检索当前账户下的所有模板配置。  
- **方法**：`GET`  
- **路径**：`/v1/template-configs`  
- **认证**：必需（基本认证）  

### 2. 获取模板详情 (Get Template Details)  
检索特定模板的详细配置。  
- **方法**：`GET`  
- **路径**：`/v1/template-configs/{templateId}`  
- **认证**：必需（基本认证）  

## 响应示例  
```json
{
  "template_id": "123456789",
  "template_name": "Order Notification",
  "template_content": "Your order {order_no} has shipped.",
  "status": 2,
  "sign_name": "Company Name"
}
```  

## 工作流程  
1. **查找模板**：在列表中查找符合需求的模板（例如，“Verification”）。  
2. **检查内容**：查看 `template_content`，确认模板中的变量占位符。  
3. **验证状态**：确保模板状态为“approved”（通常为 2）后再尝试发送。  

# EngageLab SMS 发送器技能 (EngageLab SMS Sender Skill)  

## 产品概述  
EngageLab SMS 允许开发者通过简单的 REST API 发送交易性和营销短信。所有短信都必须使用预先配置并经过审核的模板。  

**端点**：`POST https://smsapi.engagelab.com/v1/messages`  

## 使用场景  
- 发送验证码（OTP）。  
- 发送交易通知（订单更新、提醒）。  
- 发送营销信息。  

## API 参考  

### 请求头 (Request Headers)  
```http
Content-Type: application/json
Authorization: Basic ${base64(dev_key:dev_secret)}
```  

### 请求体 (Request Body, JSON)  
```json
{
    "to": [
        "923700056581"
    ],
    "template": {
        "id": "1233",
        "params": {
            "code": "039487"
        }
    }
}
```  
| 参数 | 类型 | 是否必需 | 说明 |  
|-----------|------|----------|-------------|  
| `to` | 数组 [字符串] | ✅ | 收件人电话号码（E.164 格式，例如 `["+8618701235678"]`）。 |  
| `template.id` | 字符串 | ✅ | 经审核的模板 ID。 |  
| `template.params` | 对象 | ❌ | 需要插入模板中的变量（例如 `{"code": "1234"}`）。 |  

### 响应（200 OK）  
```json
{
  "plan_id": "1972...",
  "total_count": 1,
  "accepted_count": 1,
  "message_id": "1972..."
}
```  

## 工作流程  
1. **获取模板信息**：使用 `engagelab-sms-template` 获取 `template_id` 和所需参数。  
2. **收集数据**：获取收件人电话号码和变量值。  
3. **发送短信**：构建 JSON 数据包并发送到指定端点。  
4. **验证发送结果**：检查 `accepted_count` 以确认消息是否成功送达。  

## 常见问题  
- **格式**：始终使用 E.164 格式输入收件人电话号码。  
- **部分成功**：即使返回 200 OK，也可能有部分收件人未收到消息。请比较 `accepted_count` 和 `total_count`。  
- **变量**：如果参数中缺少某个变量，占位符（例如 `{{name}}`）将会原样显示。  

# EngageLab WhatsApp 模板技能 (EngageLab WhatsApp Template Skill)  

## 产品概述  
该技能允许用户管理和查找预先配置好的 WhatsApp 模板。这是发送消息前的必要步骤，因为它提供了模板 ID、名称、语言、类别、组件和状态等信息。模板在使用前必须经过审核。  

**基础 URL**：`https://wa.api.engagelab.cc/v1`  

## API  

### 1. 列出模板 (List Templates)  
检索当前 WhatsApp 商业账户下的所有模板。  
- **方法**：`GET`  
- **路径**：`/templates`  
- **认证**：必需（基本认证）  
- **参数**：`name`（可选，模糊匹配）、`language_code`（可选）、`category`（可选：AUTHENTICATION、MARKETING、UTILITY）、`status`（可选：APPROVED、PENDING、REJECTED 等）  

### 2. 获取模板详情 (Get Template Details)  
检索特定模板的详细配置。  
- **方法**：`GET`  
- **路径**：`/templates/{template_id}`  
- **认证**：必需（基本认证）  

### 3. 创建模板 (Create Template)  
创建新模板以供审核。  
- **方法**：`POST`  
- **路径**：`/templates`  
- **认证**：必需（基本认证）  
- **请求体**：包含 `name`、`language`、`category` 的 JSON 数据。  

### 4. 更新模板 (Update Template)  
修改现有模板的组件。  
- **方法**：`PUT`  
- **路径**：`/templates/{template_id}`  
- **认证**：必需（基本认证）  
- **请求体**：包含更新后的组件信息的 JSON 数据。  

### 5. 删除模板 (Delete Template)  
删除模板（所有语言版本）。  
- **方法**：`DELETE`  
- **路径**：`/templates/{template_name}`  
- **认证**：必需（基本认证）  

## 响应示例  
```json
[
  {
    "id": "406979728071589",
    "name": "code",
    "language": "zh_CN",
    "status": "APPROVED",
    "category": "OTP",
    "components": [
      {
        "type": "HEADER",
        "format": "text",
        "text": "Registration Verification Code"
      },
      {
        "type": "BODY",
        "text": "Your verification code is {{1}}, please enter it within 5 minutes."
      }
    ]
  }
]
```  

## 工作流程  
1. **查找模板**：使用列表功能按名称、语言、类别或状态查找合适的模板。  
2. **检查模板内容**：确认模板中的占位符和所需参数。  
3. **验证状态**：确保模板状态为“APPROVED”后再使用。  
4. **创建/更新模板**：提交新模板或修改后的模板以供审核。  
5. **删除不再使用的模板**：释放资源。  

# EngageLab WhatsApp 发送器技能 (EngageLab WhatsApp Sender Skill)  

## 产品概述  
EngageLab WhatsApp 允许开发者通过简单的 REST API 发送交易性和营销消息。支持发送模板消息、文本消息、图片消息、音频消息、视频消息和贴纸消息。主动发送仅限于已审核的模板。  

**端点**：`POST https://wa.api.engagelab.cc/v1/messages`  

## 使用场景  
- 使用模板发送验证码（OTP）。  
- 发送包含图片、视频的营销信息。  
- 在 24 小时内发送交互式回复（文本、贴纸）。  

## API 参考  

### 请求头 (Request Headers)  
```http
Content-Type: application/json
Authorization: Basic ${base64(dev_key:dev_secret)}
```  

### 请求体 (Request Body, JSON)  
| 参数 | 类型 | 是否必需 | 说明 |  
|-----------|------|----------|-------------|  
| `from` | 字符串 | ❌ | 发件人 WhatsApp 账号（例如：“+8613800138000”）。默认使用控制台设置。 |  
| `to` | 数组 [字符串] | ✅ | 收件人 WhatsApp 账号（例如：“+447911123456”）。 |  
| `body` | 对象 | ✅ | 消息内容（包含消息类型、图片等）。 |  
| `request_id` | 字符串 | ❌ | 自定义跟踪 ID。 |  
| `custom_args` | 对象 | ✌ | 回调所需的键值对。 |  

### 响应（200 OK）  
```json
{
  "message_id": "cbggf4if6o9ukqaalfug",
  "request_id": "your-sendno-string"
}
```  

## 工作流程  
1. **获取模板信息**：使用 WhatsApp 模板技能获取模板 ID 和相关组件。  
2. **收集数据**：获取收件人信息和变量内容。  
3. **发送消息**：构建消息数据包并发送到指定端点。  
4. **验证发送结果**：检查 `message_id` 以确认消息是否成功送达。  

## 常见问题  
- 仅使用已审核的模板进行主动发送。  
- 确保电话号码包含国际区号。  
- 媒体文件必须符合格式和大小限制。  
- 变量内容必须与模板占位符匹配。  

# EngageLab 电子邮件发送器技能 (EngageLab Email Sender Skill)  

## 产品概述  
EngageLab Email 允许开发者通过 REST API 发送交易性和营销电子邮件。支持常规邮件发送、模板邮件、日历邀请和 MIME 格式。支持通过变量和 Handlebars 进行个性化设置。  

**端点**：`POST https://email.api.engagelab.cc/v1/mail/send`（土耳其地区：`https://emailapi-tr.engagelab.com`）  

## 使用场景  
- 发送个性化的交易邮件（确认通知、提醒）。  
- 进行带有跟踪功能的批量营销活动。  
- 发送日历邀请。  

## API 参考  

### 请求头 (Request Headers)  
```http
Content-Type: application/json;charset=utf-8
Authorization: Basic ${base64(api_user:api_key)}
```  

### 请求体 (Request Body, JSON)  
| 参数 | 类型 | 是否必需 | 说明 |  
|-----------|------|----------|-------------|  
| `from` | 字符串 | ✅ | 发件人邮箱地址（例如：“Team <support@engagelab.com>”）。 |  
| `to` | 数组 [字符串] | ✅ | 收件人邮箱地址（最多 100 个）。 |  
| `subject` | 字符串 | ✅ | 邮件主题。 |  
| `body` | 对象 | ✅ | 邮件内容（包含 HTML、文本等）。 |  
| `vars` | 对象 | ✌ | 用于替换的变量。 |  

**注意**：使用模板时，请调用 `/v1/mail/sendtemplate` 并传入 `template_invoke_name` 参数。  

### 响应（200 OK）  
```json
{
  "email_ids": ["1447054895514_15555555_32350_1350.sc-10_10_126_221-inbound0$111@qq.com"],
  "request_id": "<request_id>"
}
```  

## 工作流程  
1. **准备邮件内容**：定义邮件主题和正文，以及需要使用的变量。  
2. **添加选项**：附件、跟踪信息、发送方式等。  
3. **发送邮件**：将数据发送到指定端点。  
4. **验证发送结果**：检查邮件发送状态和任务 ID。