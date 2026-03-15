---
name: next-browser
description: 使用 Nextbrowser 的云 API 来启动云浏览器，以便 Openclaw 执行自主的浏览器任务。主要用途是创建带有配置文件（持久化的登录信息/cookies）的浏览器会话，Openclaw 可以通过这些会话来管理社交媒体和其他在线账户。次要用途是在家用代理环境下运行任务子代理，实现快速、自主的浏览器自动化操作，同时具备浏览器隐身功能和验证码破解能力。详细文档请访问 docs.nextbrowser.com。
---
# Nextbrowser

Nextbrowser 提供基于云的浏览器服务以及通过 API 实现的自动化浏览器操作功能。

**文档链接：**  
- **云 API：** https://docs.nextbrowser.com/getting-started

## 设置

**API 密钥** 从 openclaw 的配置文件中读取，存储在 `skills.entries.next-browser.apiKey` 中。  
如果未配置，请告知用户：  
> 要使用 Nextbrowser，您需要一个 API 密钥。您可以在 https://app.nextbrowser.com/user-settings 获取密钥（新注册用户可免费获得 2000 个信用点）。然后进行配置：  
> ```  
> openclaw config set skills.entries.next-browser.apiKey "YOUR_API_KEY"  
> ```  

**重要提示：** Nextbrowser 的 API 密钥可能有多种格式和前缀。  
**切勿自行验证密钥格式**——只需使用用户提供的密钥即可。如果密钥无效，API 会返回认证错误，此时再要求用户验证密钥。  

**基础 URL：** `https://app.nextbrowser.com/api/v1`  

所有请求都需要添加以下头部信息：`Authorization: x-api-key <API_KEY>`  

---

## 1. 凭据管理器（Credentials Manager）  
凭证管理器能够安全地存储并在多次浏览器运行或自动化任务中重用认证数据。  

```bash  
# 列出所有凭证  
curl "https://app.nextbrowser.com/api/v1/users/credentials" -H "Authorization: x-api-key $API_KEY"  
```  

---

## 2. 配置文件（Profiles）  
配置文件可以跨浏览器会话保存 cookie 和登录状态。创建一个配置文件后，登录您的账户并重复使用该配置文件。  

```bash  
# 列出所有配置文件  
curl "https://app.nextbrowser.com/api/v1/browser/profiles" -H "Authorization: x-api-key $API_KEY"  

# 创建浏览器配置文件  
curl -X POST "https://app.nextbrowser.com/api/v1/browser/profiles" \
  -H "Authorization: x-api-key $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "<profile-name>", "browser_settings": {"os_type": "<os-type>", "browser_type": "chrome"},  
    "proxy_settings": {"protocol": "<http|https|socks5>","country": "<iso-2-country-code>","mode": "built-in"},  
    "credentials": ["<credential-id>"]}'  

# 删除配置文件  
curl -X DELETE "https://app.nextbrowser.com/api/v1/browser/profiles/<profile-id>" \
  -H "Authorization: x-api-key $API_KEY"  
```  

---

## 3. 地理位置信息（Locations）  
这些接口提供了用于代理和浏览器配置的地理位置元数据。在创建配置文件或根据特定网络条件运行任务之前，可以使用这些接口动态获取支持的国家、地区、城市和互联网服务提供商（ISP）信息。  

```bash  
# 列出国家  
curl "https://app.nextbrowser.com/api/v1/location/countries?" \
  -H "Authorization: x-api-key $API_KEY"  
```  

```bash  
# 列出地区  
curl "https://app.nextbrowser.com/api/v1/location/regions?" \
  -H "Authorization: x-api-key $API_KEY"  
```  

```bash  
# 列出城市  
curl "https://app.nextbrowser.com/api/v1/location/cities?" \
  -H "Authorization: x-api-key $API_KEY"  
```  

```bash  
# 列出互联网服务提供商  
curl "https://app.nextbrowser.com/api/v1/location/isps?" \
  -H "Authorization: x-api-key $API_KEY"  
```  

---

## 4. 任务（Tasks）  
Nextbrowser 可以像子代理一样自动执行浏览器任务。您只需提供任务指令，它会完成相应的操作。  

**建议设置：**  
- **始终使用 `fast` 模式**：该模式专为浏览器任务优化，执行速度比其他模式快 3-5 倍。  
- **始终设置 `skip_plan_approval` 为 `true`**：该模式适用于自动化任务，可跳过审批流程从而提升性能。  

```bash  
curl -X POST "https://app.nextbrowser.com/api/v1/chat/tasks" \
  -H "Authorization: x-api-key $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "task_description": "'\
    访问 Reddit.com 账户，检查账户是否已登录（若未登录，则使用存储的凭证）；  
    在 AI Agents 主题下找到 10 条相关帖子，对其中 8 条进行点赞，并发布 3 条具有讽刺幽默风格的评论；  
    确保评论能够成功发布（若不确定是否合适，请请求审批）。完成任务后，应至少查看 10 条相关帖子、给予 8 个赞并发布 3 条评论。"  
    ",  
    "mode": "fast",  
    "profile_id": "<profile-id>",  
    "skip_plan_approval": true,  
    "send_email_notification": false  
  }'  
```  

### 终端接口：停止聊天会话/任务  
执行任务后，会返回一个会话 ID，可用于停止该聊天会话：  
```bash  
curl -X PUT "https://app.nextbrowser.com/api/v1/chat/sessions/<chat-session-id>/stop" \
  -H "Authorization: x-api-key $API_KEY"  
```  

### 终端接口：查询任务进度  
```bash  
curl "https://app.nextbrowser.com/api/v1/chat/tasks/<task-id>" \
  -H "Authorization: x-api-key $API_KEY"  
```  

**查询参数（可选）：**  
- **from_step**：整数，表示要查询的步骤索引（默认值为 1）。  

### 响应格式：  
```json  
{
  "success": true,  
  "payload": {  
    "status": "finished",  
    "output": "任务已完成：共查看 10 条相关帖子，给予 8 个赞并发布 3 条评论。"  
    "isSuccess": true,  
    "steps": [  
      {  
        "created_at": "2025-01-01T10:00:00Z",  
        "finished_at": "2025-01-01T10:00:05Z",  
        "description": "打开了 Reddit 搜索页面",  
        "status": "completed",  
        "step_number": 1  
      },  
      // ... 其他步骤  
    ],  
    "total_steps": 5  
  },  
  "errors": {},  
  "description": "任务查询成功"  
}  
```  

### 字段说明：  
- **status**：任务的整体状态（`processing`、`finished` 或 `failed`）。  
- **output**：任务的最终结果（如有）。  
- **isSuccess**：任务是否成功完成（`true` 或 `false`）。  
- **steps**：从 `from_step` 开始的任务步骤列表（默认从第 1 步开始）。  
- **step_number**：任务中的步骤编号（从 1 开始）。  
- **total_steps**：任务的总步骤数（与 `from_step` 无关）。  

### 任务选项：  
| 选项 | 描述                          |  
|--------|------------------------|  
| `task_description` | 任务指令（必填）                |  
| `mode` | 始终使用 `fast` 模式                |  
| `profile_id` | 使用指定配置文件进行身份验证            |  
| `skip_plan_approval` | 始终设置为 `true` 以跳过审批流程       |  
| `send_email_notification` | 若设置为 `true`，任务完成后会发送通知邮件    |  

---

## 完整 API 参考  
有关所有接口的详细信息，请参阅 [references/api.md]（包括 Sessions、Files、Skills 和 Skills Marketplace 等内容）。