---
name: next-browser
description: 使用 Nextbrowser 的云 API 来启动云浏览器，以便 Openclaw 执行自主的浏览器任务。主要用途是创建带有配置文件（持久化的登录信息/cookies）的浏览器会话，Openclaw 可以通过这些会话来管理社交媒体和其他在线账户。次要用途是在家用代理环境下运行任务子代理，实现快速、自主的浏览器自动化操作，同时具备浏览器隐身功能和验证码破解能力。更多详细信息请参阅 docs.nextbrowser.com。
---
# Nextbrowser

Nextbrowser 提供了基于云的浏览器服务以及通过 API 实现的自动化浏览器操作功能。

**文档链接：**  
- **云 API：** [https://docs.nextbrowser.com/getting-started](https://docs.nextbrowser.com/getting-started)

## 设置

**API 密钥** 从 openclaw 的配置文件中读取，存储在 `skills.entries.next-browser.apiKey` 中。  

如果未配置，请告知用户：  
> 要使用 Nextbrowser，您需要一个 API 密钥。您可以在 [https://app.nextbrowser.com/user-settings](https://app.nextbrowser.com/user-settings) 获取密钥（新注册用户可免费获得 2000 个信用点）。然后进行配置：  
> ```  
> openclaw config set skills.entries.next-browser.apiKey "YOUR_API_KEY"  
> ```  

**注意：** Nextbrowser 的 API 密钥可能具有多种格式和前缀。  
**请不要自行验证密钥格式**——只需使用用户提供的密钥即可。如果密钥无效，API 会返回认证错误，此时再要求用户验证密钥即可。  

**基础 URL：** `https://app.nextbrowser.com/api/v1`  

所有请求都需要添加以下头部信息：  
`Authorization: x-api-key <API_KEY>`  

---

## 1. 凭据管理器（Credentials Manager）  

凭据管理器能够安全地存储并在多次浏览器运行或自动化任务中重用认证信息。  

```bash  
# 列出所有凭据  
curl "https://app.nextbrowser.com/api/v1/users/credentials" -H "Authorization: x-api-key $API_KEY"  
```  

---

## 2. 配置文件（Profiles）  

配置文件可以跨浏览器会话保存 cookie 和登录状态。创建一个配置文件后，在浏览器中登录您的账户，即可重复使用该配置。  

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

这些端点提供了可用于代理和浏览器配置的地理位置数据。在创建配置文件或在特定网络条件下运行任务之前，可以使用这些信息动态获取支持的国家、地区、城市和互联网服务提供商（ISP）的信息。  

```bash  
# 列出所有国家  
curl "https://app.nextbrowser.com/api/v1/location/countries?  
  limit=<limit>&  
  offset=<offset>&  
  name=<name>&  
  code=<iso2-code>&  
  connection_type=<connection-type>"  
  -H "Authorization: x-api-key $API_KEY"  
```  

```bash  
# 列出所有地区  
curl "https://app.nextbrowser.com/api/v1/location/regions?  
  country__code=<iso2-country>&  
  limit=<limit>&  
  offset=<offset>&  
  name=<name>&  
  code=<region-code>&  
  connection_type=<connection-type>"  
  -H "Authorization: x-api-key $API_KEY"  
```  

```bash  
# 列出所有城市  
curl "https://app.nextbrowser.com/api/v1/location/cities?  
  country__code=<iso2-country>&  
  limit=<limit>&  
  offset=<offset>&  
  name=<name>&  
  code=<city-code>&  
  region__code=<region-code>&  
  connection_type=<connection-type>"  
  -H "Authorization: x-api-key $API_KEY"  
```  

```bash  
# 列出所有互联网服务提供商  
curl "https://app.nextbrowser.com/api/v1/location/isps?  
  country__code=<iso2-country>&  
  limit=<limit>&  
  offset=<offset>&  
  name=<name>&  
  code=<isp-code>&  
  region__code=<region-code>&  
  city__code=<city-code>&  
  connection_type=<connection-type>"  
  -H "Authorization: x-api-key $API_KEY"  
```  

---

## 4. 任务（Tasks，子代理功能）  

Nextbrowser 可以像子代理一样执行自动化浏览器任务。您只需提供相应的指令，它就会完成任务。  

**建议设置：**  
- **始终使用 `fast` 模式**——该模式针对浏览器任务进行了优化，执行速度比其他模式快 3-5 倍。  
- **始终设置 `skip_plan_approval` 为 `true`**——该模式适用于自动化任务，可跳过审批流程从而提升性能。  

```bash  
curl -X POST "https://app.nextbrowser.com/api/v1/chat/tasks" \
  -H "Authorization: x-api-key $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "task_description": "'\
    访问 Reddit.com 账户，检查账户是否已登录（如果未登录，请使用存储的凭据）。\
    在 AI Agents 主题下找到 10 条相关帖子，给其中 8 条点赞，并发表 3 条具有讽刺意味的评论（类似 Reddit 上的幽默用户可能会发的内容）。确保评论成功发布；如果您不确定这样的评论是否合适，请请求审批。完成任务后，应至少查看 10 条相关帖子、给 8 条帖子点赞并发表 3 条评论。\'"  
    "mode": "fast",  
    "profile_id": "<profile-id>",  
    "skip_plan_approval": true  
  }'  
```  

### 任务完成状态查询（Poll for completion）  

```bash  
curl "https://app.nextbrowser.com/api/v1/chat/tasks/<task-id>" \
  -H "Authorization: x-api-key $API_KEY"  

curl "https://app.nextbrowser.com/api/v1/chat/tasks/<task-id>?from_step=3" \
  -H "Authorization: x-api-key $API_KEY"  
```  

**可选查询参数：**  
- **from_step**：整数，表示要查询的步骤索引（大于等于 1）。如果未提供或无效，默认值为 1。该参数用于仅查询新步骤的完成情况。  

### 响应数据（Response）  

```json  
{
  "success": true,  
  "payload": {  
    "status": "finished",  
    "output": "任务已完成。共查看 10 条相关帖子，给 8 条帖子点赞并发表了 3 条评论。"  
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
- **output**：任务的最终结果（如果有的话）。  
- **isSuccess**：任务是否成功完成（`true` 表示成功）。  
- **steps**：从 `from_step` 开始的任务步骤列表（默认从步骤 1 开始）。  
- **step_number**：任务中的步骤编号（数组中的顺序编号，始终从 1 开始）。  
- **total_steps**：任务的总步骤数（与 `from_step` 无关）。  

### 任务选项（Task Options）  

| 选项          | 描述                                      |  
|-----------------|-----------------------------------------|  
| `task_description`    | 你需要执行的操作（必填）                          |  
| `mode`         | 始终使用 `fast` 模式                              |  
| `profile_id`      | 使用指定的配置文件进行身份验证                      |  
| `skip_plan_approval`   | 始终设置 `true` 以跳过审批流程                        |  

---

## 完整 API 参考文档  

有关所有端点的详细信息（包括 Sessions、Files、Skills 和 Skills Marketplace），请参阅 [references/api.md](references/api.md)。