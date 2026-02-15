---
name: google-chat
description: 通过 Webhook 或 OAuth 将消息发送到 Google Chat 的空间（channels）和用户。当您需要向 Google Chat 的频道（spaces）发送通知、警报或消息，或者向特定用户发送私信时，可以使用此功能。该功能支持传入的 Webhook（用于预定义的频道）以及 OAuth 2.0（用于向任意空间或用户发送动态消息）。
---

# Google Chat消息发送

有两种方法可以向Google Chat发送消息：

1. **Webhooks** - 快速且预先配置好的发送渠道（消息会以机器人的形式显示）  
2. **OAuth** - 可以动态地向任何聊天空间或用户发送消息（需要身份验证）

## 快速入门

### 方法1：Webhooks（推荐用于已知的聊天空间）

向预先配置好的聊天空间发送消息：

```bash
python3 scripts/send_webhook.py "$WEBHOOK_URL" "Your message here"
```

**带线程的消息发送示例：**
```bash
python3 scripts/send_webhook.py "$WEBHOOK_URL" "Reply message" --thread_key "unique-thread-id"
```

**配置：** 将Webhook信息保存在`google-chat-config.json`文件中：

```json
{
  "webhooks": {
    "acs_engineering_network": "https://chat.googleapis.com/v1/spaces/...",
    "general": "https://chat.googleapis.com/v1/spaces/..."
  }
}
```

**读取配置并发送消息：**
```bash
WEBHOOK_URL=$(jq -r '.webhooks.acs_engineering_network' google-chat-config.json)
python3 scripts/send_webhook.py "$WEBHOOK_URL" "Deploy completed ✅"
```

### 方法2：OAuth（用于动态消息发送）

**首次设置：**
1. 将OAuth凭据保存到一个文件中（例如`google-chat-oauth-credentials.json`）
2. 运行身份验证流程（会打开浏览器并保存访问令牌）：

```bash
python3 scripts/send_oauth.py \
  --credentials google-chat-oauth-credentials.json \
  --token google-chat-token.json \
  --space "General" \
  "Test message"
```

**按名称向聊天空间发送消息：**
```bash
python3 scripts/send_oauth.py \
  --credentials google-chat-oauth-credentials.json \
  --token google-chat-token.json \
  --space "Engineering Network" \
  "Deploy completed"
```

**注意：** 使用OAuth发送的消息会自动添加`🤖`表情符号前缀。可以使用`--no-emoji`选项来禁用此功能：  
```bash
python3 scripts/send_oauth.py \
  --credentials google-chat-oauth-credentials.json \
  --token google-chat-token.json \
  --space "Engineering Network" \
  "Message without emoji" \
  --no-emoji
```

**列出可用的聊天空间：**
```bash
python3 scripts/send_oauth.py \
  --credentials google-chat-oauth-credentials.json \
  --token google-chat-token.json \
  --list-spaces
```

**向私信（DM）发送消息（需要知道聊天空间的ID）：**
```bash
# Note: Google Chat API doesn't support creating new DMs by email
# You need the space ID of an existing DM conversation
python3 scripts/send_oauth.py \
  --credentials google-chat-oauth-credentials.json \
  --token google-chat-token.json \
  --space-id "spaces/xxxxx" \
  "The report is ready"
```

**通过ID向聊天空间发送消息（更快）：**
```bash
python3 scripts/send_oauth.py \
  --credentials google-chat-oauth-credentials.json \
  --token google-chat-token.json \
  --space-id "spaces/AAAALtlqgVA" \
  "Direct message to space"
```

## 所需依赖库**

安装以下Python包：  
```bash
pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

**所需的OAuth权限范围：**
- `https://www.googleapis.com/auth/chat.messages` - 发送消息  
- `https://www.googleapis.com/auth/chat.spaces` - 访问聊天空间信息  
- `https://www.googleapis.com/auth/chat.memberships.readonly` - 列出聊天空间成员（用于识别私信接收者）

## OAuth设置指南

如果还没有OAuth凭据：
1. 访问[Google Cloud Console](https://console.cloud.google.com)  
2. 选择你的项目或创建一个新的项目  
3. 启用**Google Chat API**  
4. 转到**APIs & Services → Credentials**  
5. 创建**OAuth 2.0 Client ID**（适用于桌面应用程序）  
6. 下载JSON文件并保存为`google-chat-oauth-credentials.json`  
该JSON文件的内容应如下所示：  
```json
{
  "installed": {
    "client_id": "...apps.googleusercontent.com",
    "client_secret": "GOCSPX-...",
    "redirect_uris": ["http://localhost"],
    ...
  }
}
```

## Webhook设置指南

要为Google Chat聊天空间创建Webhook：
1. 在浏览器中打开Google Chat  
2. 进入目标聊天空间  
3. 点击聊天空间名称 → **Apps & integrations**  
4. 点击**Manage webhooks** → **Add webhook**  
5. 为Webhook命名（例如：“Agustin Networks”）  
6. 复制Webhook的URL  
7. 将该URL添加到`google-chat-config.json`文件中  

## 选择合适的方法

**在以下情况下使用Webhooks：**
- 需要反复向相同的聊天空间发送消息  
- 消息需要以机器人的形式显示  
- 对发送速度有较高要求（无需进行OAuth身份验证）  
- 配置是固定的  

**在以下情况下使用OAuth：**
- 需要动态地向不同的聊天空间发送消息  
- 消息需要从你配置的Google Chat应用程序发送  
- 聊天空间的名称是在运行时确定的  
- 需要列出并查找可用的聊天空间  

**OAuth的局限性：**
- 无法通过电子邮件地址创建新的私信（Google Chat API的限制）  
- 要发送私信，需要知道目标聊天空间的ID  
- 可以使用`--list-spaces`命令来查找可用的私信空间ID  

## 消息格式

两种方法都支持纯文本消息。对于更复杂的格式（如卡片、按钮等），需要构建JSON格式的数据：

**使用Webhook发送带有卡片的消息：**
```python
import json
import urllib.request

payload = {
    "cardsV2": [{
        "cardId": "unique-card-id",
        "card": {
            "header": {"title": "Deploy Status"},
            "sections": [{
                "widgets": [{
                    "textParagraph": {"text": "Production deploy completed successfully"}
                }]
            }]
        }
    }]
}

data = json.dumps(payload).encode("utf-8")
req = urllib.request.Request(webhook_url, data=data, headers={"Content-Type": "application/json"})
urllib.request.urlopen(req)
```

## 故障排除**

**Webhook错误：**
- 确认Webhook URL正确且处于活动状态  
- 检查聊天空间是否存在，以及Webhook是否已被删除  
- 确保消息内容不为空  

**OAuth错误：**
- 如果访问令牌过期，请重新运行身份验证流程  
- 确认Google Chat API已在Cloud Console中启用  
- 检查用户是否具有访问目标聊天空间的权限  
- 对于私信，确保发送者的电子邮件地址正确且与目标聊天空间属于同一工作区  

**权限问题：**
- 使用Webhook时，发送者必须是聊天空间的成员  
- 使用OAuth时，发送者必须具有访问目标聊天空间或用户的权限  
- 在企业工作区中，某些功能可能受到管理员政策的限制  

## 示例**

**向工程团队聊天空间发送通知：**
```bash
WEBHOOK=$(jq -r '.webhooks.acs_engineering_network' google-chat-config.json)
python3 scripts/send_webhook.py "$WEBHOOK" "🚀 Production deploy v2.1.0 completed"
```

**向特定用户发送任务提醒：**
```bash
python3 scripts/send_oauth.py \
  --credentials google-chat-oauth-credentials.json \
  --token google-chat-token.json \
  --dm juan@empresa.com \
  "Your report is ready for review: https://docs.company.com/report"
```

**使用Webhook将多条消息合并发送：**
```bash
WEBHOOK=$(jq -r '.webhooks.general' google-chat-config.json)
THREAD_KEY="deploy-$(date +%s)"

python3 scripts/send_webhook.py "$WEBHOOK" "Starting deploy..." --thread_key "$THREAD_KEY"
# ... deployment happens ...
python3 scripts/send_webhook.py "$WEBHOOK" "Deploy completed ✅" --thread_key "$THREAD_KEY"
```