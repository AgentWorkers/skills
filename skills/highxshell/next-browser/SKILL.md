---
name: next-browser
description: 使用 Nextbrowser 的云 API 来启动云浏览器，以便 Openclaw 执行自主的浏览器任务。主要用途是创建带有配置文件（持久化的登录信息/cookies）的浏览器会话，Openclaw 可以通过这些会话来管理社交媒体和其他在线账户。次要用途是在家用代理环境下运行任务子代理，实现快速、自主的浏览器自动化操作，同时具备浏览器隐身功能和验证码破解能力。更多详细信息请参阅 docs.nextbrowser.com 的文档。
---
# Nextbrowser

Nextbrowser 提供基于云的浏览器服务以及通过 API 实现的自动化浏览器操作功能。

**文档链接：**  
- 云 API：https://docs.nextbrowser.com/getting-started

## 设置

**API 密钥** 从 openclaw 的配置文件（`skills.entries.next-browser.apiKey`）中读取。  
如果未配置该密钥，请告知用户：  
> 要使用 Nextbrowser，您需要一个 API 密钥。您可以在 https://app.nextbrowser.com/user-settings 获取密钥（新用户注册可免费获得 2000 个信用点）。完成配置后，请继续使用 Nextbrowser。  
**配置示例：**  
```
> openclaw config set skills.entries.next-browser.apiKey "nb_your_key_here"
> ```

基础 URL：`https://app.nextbrowser.com/api/v1`  

所有请求都需要添加以下请求头：`Authorization: x-api-key <apiKey>`

---

## 1. 凭据管理器（Credentials Manager）

凭证管理器能够安全地存储并在多次浏览器运行或自动化任务中重用认证数据。  
**详情：**  
```bash
# List credentials
curl "https://app.nextbrowser.com/api/v1/users/credentials" -H "Authorization: x-api-key $API_KEY"
```

---

## 2. 帖户信息（Profiles）

账户信息（Profiles）能够跨浏览器会话保留 Cookie 和登录状态。  
**操作步骤：**  
1. 创建一个账户；  
2. 在浏览器中登录；  
3. 之后即可重复使用该账户信息。  
**详情：**  
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

地理位置信息（Locations）端点提供了可用于代理设置和浏览器配置的元数据。  
**用途：**  
在创建账户或根据特定网络条件运行任务之前，可以利用这些信息动态获取支持的国家、地区、城市和互联网服务提供商（ISP）的信息。  
**详情：**  
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

Nextbrowser 可以作为自动化任务执行器来运行浏览器操作。  
**使用建议：**  
- 始终选择 `fast` 模式——该模式专为浏览器任务优化，执行速度比其他模式快 3-5 倍。  
- 始终设置 `skip_plan_approval` 为 `true`——该选项可跳过计划审批流程，从而提升任务执行效率。  
**详情：**  
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

### 完成状态查询端点（Poll for Completion）  
**请求参数（可选）：**  
- `from_step`：整数，表示要查询的步骤索引（>= 1）。如果该参数缺失或无效，默认值为 1。该参数用于仅查询新的任务步骤。  
**响应内容：**  
```json
{
  "success": true,
  "payload": {
    "status": "finished",
    "output": "Task completed. 10 relevant posts are viewed, 8 upvotes are done and 3 comments posted.",
    "isSuccess": true,
    "steps": [
      {
        "created_at": "2025-01-01T10:00:00Z",
        "finished_at": "2025-01-01T10:00:05Z",
        "description": "Opened Reddit search page",
        "status": "completed",
        "step_number": 1
      }
      // ... more steps starting from from_step
    ],
    "total_steps": 5
  },
  "errors": {},
  "description": "Task retrieved successfully"
}
```

### 响应字段说明：**  
- `status`：任务的整体状态（`processing`、`finished` 或 `failed`）。  
- `output`：任务的最终输出结果（如有）。  
- `isSuccess`：任务是否成功完成（`true` 表示成功，`false` 表示失败）。  
- `steps`：从 `from_step` 开始的任务步骤列表（默认从步骤 1 开始）。  
- `step_number`：任务中的当前步骤编号（数组中的索引始终从 1 开始）。  
- `total_steps`：任务的总步骤数（与 `from_step` 无关）。  

### 任务配置选项：  
| 选项          | 描述                                      |
|----------------|-----------------------------------------|
| `task_description` | 你需要输入的提示或指令                         |
| `mode`         | 始终使用 `fast` 模式                         |
| `profile_id`     | 使用指定的账户信息进行身份验证                   |
| `skip_plan_approval` | 始终设置为 `true`，以跳过计划审批流程                 |

---

## 完整 API 参考

有关所有端点的详细信息，请参阅 [references/api.md](references/api.md)，其中包含 Sessions、Files、Skills 和 Skills Marketplace 的相关内容。