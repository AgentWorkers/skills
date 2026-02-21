---
name: lemlist
description: >
  官方的Lemlist API集成，用于销售自动化和多渠道营销。  
  当用户需要执行以下操作时，可以使用此功能：  
  - 管理营销活动（创建、列出、暂停、启动、获取统计数据）  
  - 向营销活动中添加、更新或删除潜在客户（leads）  
  - 通过电子邮件、LinkedIn、WhatsApp或SMS发送消息  
  - 设置和管理营销活动事件的Webhook  
  - 配置营销活动的发送时间表  
  - 管理用户退订（电子邮件和域名）  
  - 导出营销活动数据（潜在客户、活动记录、联系人信息）  
  - 为潜在客户添加额外的信息  
  - 控制Lemwarm的邮件发送策略（如邮件发送的时机）  
  - 使用序列化步骤来执行营销流程  
  - 管理收件箱标签和对话记录  
  示例：  
  - “列出我的Lemlist营销活动”  
  - “将潜在客户添加到我的营销活动中”  
  - “暂停我的营销活动”  
  - “查看营销活动的统计数据”  
  - “为邮件打开事件设置Webhook”  
  - “导出我的潜在客户信息”
---
# Lemlist

您可以使用Lemlist API来管理活动（campaigns）、潜在客户（leads）、任务序列（sequences）、日程安排（schedules）、活动（activities）、收件箱（inbox）、Webhook触发器（webhooks）、取消订阅（unsubscribes）、数据导出（exports）以及客户信息 enrichment（数据增强）等操作。

完整的API端点参考：`references/api-endpoints.md`  
官方API文档：https://developer.lemlist.com/api-reference

## 设置

### 1. 获取API密钥

1. 登录到 [Lemlist](https://app.lemlist.com)  
2. 转到 **设置 > 集成 > API密钥**（Settings > Integrations > API Keys）  
3. 创建一个新的API密钥——请立即将其复制下来（仅显示一次）。

### 2. 在OpenClaw中配置

将API密钥添加到 `~/.openclaw/openclaw.json` 文件中：

```json
{
  "skills": {
    "entries": {
      "lemlist": {
        "apiKey": "your-lemlist-api-key"
      }
    }
  }
}
```

（或使用另一种显式的配置方式：）

```json
{
  "skills": {
    "entries": {
      "lemlist": {
        "env": {
          "LEMLIST_API_KEY": "your-lemlist-api-key"
        }
      }
    }
  }
}
```

### 3. 验证配置

运行以下命令以验证配置是否正确：`Get my Lemlist team info`

### Docker沙箱环境

如果使用Docker沙箱环境，需要显式传递API密钥：

```json
{
  "agents": {
    "defaults": {
      "sandbox": {
        "docker": {
          "env": ["LEMLIST_API_KEY"]
        }
      }
    }
  }
}
```

## 认证

基础URL：`https://api.lemlist.com/api`

使用基本认证（Basic Auth）进行身份验证，用户名必须为空（在密钥前加上冒号）：

```
Authorization: Basic base64(:LEMLIST_API_KEY)
```

## Python辅助函数

所有API调用都应使用以下模式进行：

```python
import urllib.request, os, json, base64

API_KEY = os.environ["LEMLIST_API_KEY"]
AUTH = base64.b64encode(f":{API_KEY}".encode()).decode()
BASE = "https://api.lemlist.com/api"

def api(path, method="GET", data=None):
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(f"{BASE}{path}", data=body, method=method)
    req.add_header("Authorization", f"Basic {AUTH}")
    req.add_header("User-Agent", "OpenClaw/1.0")
    if data:
        req.add_header("Content-Type", "application/json")
    return json.load(urllib.request.urlopen(req))
```

## API端点概览

| 功能领域 | 相关API端点 |
|---------|-------------------|
| **团队**    | GET `/team`, `/team/members`, `/team/credits`, `/team/senders` |
| **活动**    | GET/POST `/campaigns`, PATCH `/campaigns/:id`, POST `pause`/`start` |
| **任务序列** | GET `/campaigns/:id/sequences`, POST/PATCH/DELETE |  
| **潜在客户** | GET/POST/PATCH/DELETE `/campaigns/:id/leads/:idOrEmail` |
| **全局潜在客户** | GET `/leads`, POST `pause`/`start`/`interested`/`notinterested` |
| **潜在客户信息** | POST/PATCH/DELETE `/leads/:id/variables` |
| **活动**    | GET `/activities` （可过滤：`campaignId`, `type`） |
| **日程安排** | 创建/读取/删除日程：`CRUD` `/schedules`, POST `/campaigns/:id/schedules` |
| **取消订阅** | GET `/unsubscribes`, POST/DELETE `/unsubscribes/:value` |
| **Webhook**   | 创建/读取/删除Webhook：`GET/POST/DELETE` （每个团队最多200个Webhook） |
| **收件箱** | 获取/发送邮件/LinkedIn消息/WhatsApp消息/SMS：`GET `/inbox`, POST `email`/`linkedin`/`whatsapp`/`sms` |
| **收件箱标签** | 创建/读取/修改标签：`CRUD `/inbox/labels`, 通过 `/conversations/labels/:contactId` 分配标签 |
| **公司**    | 获取/查看公司信息：`GET `/companies`, `/companies/:id/notes` |
| **联系人**   | 获取/查看联系人信息：`GET `/contacts`, `/contacts/:idOrEmail` |
| **数据导出** | 同步导出：`GET `/campaigns/:id/export`；异步导出：`/export/start` |
| **数据增强** | 增强潜在客户信息：`POST `/leads/:id/enrich`, 获取信息：`GET `/enrich/:id`, 批量处理：`POST `/enrich` |
| **任务**    | 创建/修改/忽略任务：`GET/POST/PATCH `/tasks`, POST `/tasks/ignore` |
| **Lemwarm**   | 启用/暂停Lemwarm功能：`POST `start`/`pause`；修改设置：`GET/PATCH `/lemwarm/:mailboxId` |

有关请求和响应的详细信息，请参阅 `references/api-endpoints.md`。

## 分页

参数：`offset`（默认值0），`limit`（最大值100），`page`（基于1的页码，可覆盖`offset`设置）。

分页响应包含 `pagination: { totalRecords, currentPage, nextPage, totalPage }`。部分旧版本的API端点可能返回纯数组格式的数据。

## ID前缀

- `cam_`：代表活动（campaign）  
- `lea_`：代表潜在客户（lead）  
- `skd_`：代表日程安排（schedule）  
- `seq_`：代表任务序列（sequence）  
- `tea_`：代表团队（team）  
- `usr_`：代表用户（user）  

## 注意事项：

- **必须设置User-Agent**：设置为 `User-Agent: OpenClaw/1.0`；Python默认的User-Agent会被Cloudflare阻止（导致403错误）。  
- **基本认证格式**：用户名必须为空，并且需要使用 `base64(":key")` 的格式（而非 `base64("key")`）。  
- **活动无法直接删除**：只能通过API暂停或停止活动。  
- **电子邮件地址编码**：在URL路径参数中，`@` 需要转换为 `%40`。  
- **Webhook自动删除**：如果收到404或410错误，系统会自动删除相应的Webhook。  
- **无速率限制**：公共API没有请求速率限制。  
- **变量删除**：`DELETE /leads/:id/variables` 仅删除变量信息，不会删除潜在客户记录。  
- **数据导出**：`/export` 用于同步导出数据，`/export/start` 用于异步导出（适用于大量数据）。  
- **限制**：每页显示100条记录；每个团队最多200个Webhook；每个团队最多100个API密钥。