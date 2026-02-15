---
name: next-browser
description: 使用 Nextbrowser 的云 API 来启动云浏览器，以便 Openclaw 执行自主的浏览器任务。主要用途是创建带有配置文件（持久化的登录信息/cookie）的浏览器会话，Openclaw 可以通过这些会话来管理社交媒体和其他在线账户。次要用途是在住宅代理环境下运行任务子代理，实现快速的自主浏览器自动化操作，同时具备浏览器隐身功能和 CAPTCHA 解决能力。更多详细信息请参阅 docs.nextbrowser.com。
---

# Nextbrowser

Nextbrowser 提供基于云的浏览器服务以及通过 API 实现的自动化浏览器操作功能。

**文档链接：**  
- 云 API：https://docs.nextbrowser.com/getting-started

## 设置

**API 密钥** 从 openclaw 的配置文件（`skills.entries.next-browser.apiKey`）中读取。  
如果未配置该密钥，请告知用户：  
> 要使用 Nextbrowser，您需要一个 API 密钥。您可以在 https://app.nextbrowser.com/user-settings 获取密钥（新用户注册可免费获得 2000 个信用点）。完成配置后，即可开始使用。  
**配置步骤：**  
```
> openclaw config set skills.entries.next-browser.apiKey "nb_your_key_here"
> ```

基础 URL：`https://app.nextbrowser.com/api/v1`  

所有请求都需要添加以下请求头：`Authorization: x-api-key <apiKey>`  

---

## 1. 用户资料（Profiles）

用户资料可以跨浏览器会话保存 cookie 和登录状态。创建一个用户资料，登录到您的账户，然后重复使用该资料。  
**操作步骤：**  
```bash
# List profiles
curl "https://app.nextbrowser.com/api/v1/browser/profiles" -H "Authorization: x-api-key $API_KEY"

# Create browser profile
curl -X POST "https://app.nextbrowser.com/api/v1/browser/profiles" \
  -H "Authorization: x-api-key $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "<profile-name>", "browser_settings": {"os_type": "<os-type>", "browser_type": "chrome"},
   "proxy_settings":{"protocol":"<http|https|socks5>","country":"<iso-2-country-code>","mode":"built-in"}}'

# Delete profile
curl -X DELETE "https://app.nextbrowser.com/api/v1/browser/profiles/<profile-id>" \
  -H "Authorization: x-api-key $API_KEY"
```

---

## 2. 凭据管理器（Credentials Manager）

凭证管理器能够安全地存储并在多次浏览器运行或自动化任务中重复使用用户的认证信息。  
**操作步骤：**  
```bash
# List credentials
curl "https://app.nextbrowser.com/api/v1/users/credentials" -H "Authorization: x-api-key $API_KEY"
```

---

## 3. 地理位置信息（Locations）

地理位置信息接口可用于配置代理服务器和浏览器设置。在创建用户资料或根据特定网络条件运行任务之前，可以使用这些接口动态获取支持的国家、地区、城市和 ISP 信息。  
**操作步骤：**  
```bash
# List Countries
curl "https://app.nextbrowser.com/api/v1/location/countries?\
limit=<limit>&\
offset=<offset>&\
name=<name>&\
code=<iso2-code>&\
connection_type=<connection-type>" \
  -H "Authorization: x-api-key $API_KEY"
```  
**参考示例：**  
```bash
# List Regions
curl "https://app.nextbrowser.com/api/v1/location/regions?\
country__code=<iso2-country>&\
limit=<limit>&\
offset=<offset>&\
name=<name>&\
code=<region-code>&\
city__code=<city-code>&\
connection_type=<connection-type>" \
  -H "Authorization: x-api-key $API_KEY"
```  
**补充说明：**  
这些接口可用于确定目标地区的网络环境，从而优化浏览器行为。  

---

## 4. 任务执行（Tasks, Subagent）

Nextbrowser 可以作为“子代理”来执行自动化浏览器任务。您只需提供相应的指令，它就会完成相应的操作。  
**使用建议：**  
- **始终使用 `fast` 模式**：该模式专为浏览器任务优化，执行速度比其他模式快 3-5 倍。  
- **始终设置 `skip_plan_approval` 为 `true`**：该选项适用于自动化任务，可跳过审批流程，从而提升执行效率。  
**操作步骤：**  
```bash
curl -X POST "https://app.nextbrowser.com/api/v1/chat/tasks" \
  -H "Authorization: x-api-key $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "task_description": "'"\
Go to Reddit.com account, check if the account is logged in (if not, use credentials stored). \
Find 10 relevant posts on the topic of AI Agents, upvote 8 of them and post 3 witty-sounding comments \
that a cynical and funny Reddit user would post. Ensure that the comment is posted, ask for approval \
if you are not sure whether such comment is okay. By the end, you should have at least 10 relevant posts \
viewed, 8 upvotes, and 3 comments."\
"'",
    "mode": "fast",
    "profile_id": "<profile-id>",
    "credentials": ["<credential-id>"],
    "skip_plan_approval": true
  }'
```

### 任务完成状态查询（Poll for Completion）  
**操作步骤：**  
```bash
curl "https://app.nextbrowser.com/api/v1/chat/tasks/<task-id>" -H "Authorization: x-api-key $API_KEY"
```  
**返回值：**  
`processing`（处理中）、`finished`（已完成）、`failed`（失败）  

### 任务配置选项（Task Options）  

| 选项          | 描述                        |
|------------------|---------------------------|
| `task_description` | 您需要用户输入的指令                |
| `mode`         | 始终使用 `fast` 模式                |
| `profile_id`     | 使用指定的用户资料进行身份验证          |
| `credentials`    | 用于登录的凭证 ID 列表                |
| `skip_plan_approval` | 始终设置为 `true`（跳过计划审批）           |

---

## 完整 API 参考

有关所有 API 接口的详细信息，请参阅 [references/api.md](references/api.md)，其中包含 Sessions、Files、Skills 和 Skills Marketplace 等内容的说明。