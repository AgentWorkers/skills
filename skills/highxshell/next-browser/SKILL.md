---
name: next-browser
description: 使用 Nextbrowser 的云 API 来启动云浏览器，以便 Openclaw 执行自主的浏览器任务。主要用途是创建带有个人资料（持久化的登录信息/cookies）的浏览器会话，Openclaw 可以通过这些会话来管理社交媒体和其他在线账户。次要用途是在家用代理环境下运行任务子代理，实现快速的自主浏览器自动化操作，同时具备浏览器隐藏功能和验证码破解能力。详细文档请访问 docs.nextbrowser.com。
---
# Nextbrowser

Nextbrowser 提供了基于云的浏览器服务以及通过 API 实现的自动化浏览器操作功能。

**文档链接：**  
- 云 API：https://docs.nextbrowser.com/getting-started

## 设置

**API 密钥** 从 openclaw 的配置文件（`skills.entries.next-browser.apiKey`）中读取。  
如果未配置该密钥，请告知用户：  
> 要使用 Nextbrowser，您需要一个 API 密钥。您可以在 https://app.nextbrowser.com/user-settings 获取密钥（新注册用户可免费获得 2000 个信用点）。完成配置后，请继续使用 Nextbrowser。  
> ```
> openclaw config set skills.entries.next-browser.apiKey "nb_your_key_here"
> ```

基础 URL：`https://app.nextbrowser.com/api/v1`  
所有请求都需要添加以下头部信息：`Authorization: x-api-key <apiKey>`  

---

## 1. 凭据管理器（Credentials Manager）  
凭证管理器能够安全地存储并在多次浏览器运行或自动化任务中重复使用认证数据。  
```bash
# List credentials
curl "https://app.nextbrowser.com/api/v1/users/credentials" -H "Authorization: x-api-key $API_KEY"
```

---

## 2. 个人资料（Profiles）  
个人资料功能可以跨浏览器会话保存 cookie 和登录状态。您可以创建一个新的个人资料，登录到您的账户，然后在该个人资料下执行后续操作。  
```bash
# List profiles
curl "https://app.nextbrowser.com/api/v1/browser/profiles" -H "Authorization: x-api-key $API_KEY"

# Create browser profile
curl -X POST "https://app.nextbrowser.com/api/v1/browser/profiles" \
  -H "Authorization: x-api-key $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "<profile-name>", "browser_settings": {"os_type": "<os-type>", "browser_type": "chrome"},
   "proxy_settings":{"protocol":"<http|https|socks5>","country":"<iso-2-country-code>","mode":"built-in"},
   "credentials": ["<credential-id>"]}'

# Delete profile
curl -X DELETE "https://app.nextbrowser.com/api/v1/browser/profiles/<profile-id>" \
  -H "Authorization: x-api-key $API_KEY"
```

---

## 3. 地理位置信息（Locations）  
地理位置信息接口可用于配置代理服务器和浏览器设置。在创建个人资料或根据特定网络条件运行任务之前，可以利用这些接口动态获取支持的国家、地区、城市和 ISP 信息。  
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
```bash
# List Cities
curl "https://app.nextbrowser.com/api/v1/location/cities?\
country__code=<iso2-country>&\
limit=<limit>&\
offset=<offset>&\
name=<name>&\
code=<city-code>&\
region__code=<region-code>&\
connection_type=<connection-type>" \
  -H "Authorization: x-api-key $API_KEY"
```  
```bash
# List ISPs
curl "https://app.nextbrowser.com/api/v1/location/isps?\
country__code=<iso2-country>&\
limit=<limit>&\
offset=<offset>&\
name=<name>&\
code=<isp-code>&\
region__code=<region-code>&\
city__code=<city-code>&\
connection_type=<connection-type>" \
  -H "Authorization: x-api-key $API_KEY"
```  

---

## 4. 任务执行（Tasks, Subagent）  
Nextbrowser 可以作为自动化任务的“子代理”来执行浏览器操作。您只需提供相应的指令，它就会完成相应的任务。  
- **建议始终使用 `fast` 模式**：该模式专为浏览器任务优化，执行速度比其他模式快 3-5 倍。  
- **建议始终将 `skip_plan_approval` 设置为 `true`**：该选项适用于自动化任务，可跳过审批流程从而提升性能。  
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
    "skip_plan_approval": true
  }'
```

### 任务完成状态查询  
您可以通过特定接口查询任务的完成状态。  
**响应格式：**  
```json
{
    "success": true,
    "payload": {
        "status": "finished",
        "output": "Task completed. 10 relevant posts are viewed, 8 upvotes are done and 3 comments posted.",
        "isSuccess": true
    },
    "errors": {},
    "description": "Task retrieved successfully"
}
```  
可能的状态值：`processing`（处理中）、`finished`（已完成）、`failed`（失败）  

### 任务配置选项  
| 选项                | 描述                                      |
|------------------|----------------------------------------|
| `task_description`     | 您需要输入的指令或提示                         |
| `mode`             | 始终使用 `fast` 模式                         |
| `profile_id`         | 使用指定的个人资料进行身份验证                   |
| `skip_plan_approval`     | 始终将 `skip_plan_approval` 设置为 `true`                   |

---

## 完整 API 参考  
有关所有 API 接口的详细信息，请参阅 [references/api.md](references/api.md)，其中包含 Sessions、Files、Skills 和 Skills Marketplace 等相关内容。