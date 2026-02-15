---
name: browser-use
description: **使用浏览器**  
通过云API来启动Clawdbot的云浏览器，并执行自主的浏览器任务。主要用途是创建带有用户配置文件（持久化的登录信息/cookies）的浏览器会话，这些会话可由Clawdbot进行控制；次要用途则是运行用于快速执行自主浏览器自动化任务的子代理程序。相关文档可访问：`docs.browser-use.com` 和 `docs.cloud-browser-use.com`。
---

# 浏览器使用（Browser Use）

“浏览器使用”（Browser Use）通过API提供云浏览器服务以及自主化的浏览器自动化功能。

**文档：**
- 开源库：https://docs.browser-use.com  
- 云API：https://docs.cloud.browser-use.com  

## 设置（Setup）  

**API密钥** 从 `skills.entries.browser-use.apiKey` 中读取。  
如果未配置，请告知用户：  
> 要使用“浏览器使用”功能，您需要一个API密钥。您可以在 [https://cloud.browser-use.com](https://cloud.browser-use.com) 获取一个API密钥（新注册用户可享受10美元的免费信用额度）。然后进行配置：  
> ```
> clawdbot config set skills.entries.browser-use.apiKey "bu_your_key_here"
> ```  

基础URL：`https://api.browser-use.com/api/v2`  

所有请求都需要添加以下头部信息：`X-Browser-Use-API-Key: <apiKey>`  

---

## 1. 浏览器会话（Browser Sessions，主要功能）  

**为Clawdbot启动云浏览器以进行直接控制。** 使用配置文件（profiles）来保存登录信息和cookies。  

### 创建浏览器会话  
```bash
# With profile (recommended - keeps you logged in)
curl -X POST "https://api.browser-use.com/api/v2/browsers" \
  -H "X-Browser-Use-API-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"profileId": "<profile-uuid>", "timeout": 60}'

# Without profile (fresh browser)
curl -X POST "https://api.browser-use.com/api/v2/browsers" \
  -H "X-Browser-Use-API-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"timeout": 60}'
```  

**响应：**  
```json
{
  "id": "session-uuid",
  "cdpUrl": "https://<id>.cdp2.browser-use.com",
  "liveUrl": "https://...",
  "status": "active"
}
```  

### 将Clawdbot连接到浏览器  
```bash
gateway config.patch '{"browser":{"profiles":{"browseruse":{"cdpUrl":"<cdpUrl-from-response>"}}}}'
```  

现在，您可以使用 `browser` 工具（并指定 `profile=browseruse`）来控制该浏览器会话。  

### 列出/停止浏览器会话  
```bash
# List active sessions
curl "https://api.browser-use.com/api/v2/browsers" -H "X-Browser-Use-API-Key: $API_KEY"

# Get session status
curl "https://api.browser-use.com/api/v2/browsers/<session-id>" -H "X-Browser-Use-API-Key: $API_KEY"

# Stop session (unused time is refunded)
curl -X PATCH "https://api.browser-use.com/api/v2/browsers/<session-id>" \
  -H "X-Browser-Use-API-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"status": "stopped"}'
```  

**定价：** 每小时0.06美元（按使用量计费）或每小时0.03美元（企业套餐）。每个会话最长持续4小时，按分钟计费，未使用的时长将退还费用。  

---

## 2. 配置文件（Profiles）  

配置文件用于在多个浏览器会话之间保存cookies和登录状态。创建一个配置文件后，在浏览器中登录您的账户，即可重复使用该配置文件。  
```bash
# List profiles
curl "https://api.browser-use.com/api/v2/profiles" -H "X-Browser-Use-API-Key: $API_KEY"

# Create profile
curl -X POST "https://api.browser-use.com/api/v2/profiles" \
  -H "X-Browser-Use-API-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "My Profile"}'

# Delete profile
curl -X DELETE "https://api.browser-use.com/api/v2/profiles/<profile-id>" \
  -H "X-Browser-Use-API-Key: $API_KEY"
```  

**提示：** 您也可以通过“Browser Use”的Chrome扩展程序将本地Chrome浏览器中的cookies同步到云端。  

---

## 3. 任务执行（Tasks，子代理功能）  

“浏览器使用”可作为子代理来自动执行浏览器相关任务。您只需提供指令，它便会完成相应的操作。  
**建议始终使用 `browser-use-llm` 模型**——该模型专为浏览器任务优化，执行速度比其他模型快3-5倍。  
```bash
curl -X POST "https://api.browser-use.com/api/v2/tasks" \
  -H "X-Browser-Use-API-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Go to amazon.com and find the price of the MacBook Air M3",
    "llm": "browser-use-llm"
  }'
```  

### 检查任务完成情况  
```bash
curl "https://api.browser-use.com/api/v2/tasks/<task-id>" -H "X-Browser-Use-API-Key: $API_KEY"
```  

**响应：**  
```json
{
  "status": "finished",
  "output": "The MacBook Air M3 is priced at $1,099",
  "isSuccess": true,
  "cost": "0.02"
}
```  

任务状态：`pending`（待处理）、`running`（运行中）、`finished`（已完成）、`failed`（失败）、`stopped`（已停止）  

### 任务选项（Task Options）  
| 选项 | 描述 |  
|--------|-------------|  
| `task` | 您需要执行的指令 |  
| `llm` | 始终使用 `browser-use-llm` 模型 |  
| `startUrl` | 启动页面地址 |  
| `maxSteps` | 最大操作次数（默认为100次） |  
| `sessionId` | 是否重用现有会话 |  
| `profileId` | 使用指定配置文件进行身份验证 |  
| `flashMode` | 更快的执行速度 |  
| `vision` | 是否启用视觉理解功能 |  

---

## 完整API参考（Full API Reference）  

有关所有端点的详细信息（包括会话管理、文件操作、技能功能以及技能市场等），请参阅 [references/api.md](references/api.md)。