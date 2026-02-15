---
name: my-life-feed
description: 通过 MyFeed REST API 管理我的信息流（MyFeed）中的内容和相关组。
metadata: {"clawdbot":{"emoji":"📋","requires":{"bins":["jq"],"env":["Myfeed_API_KEY"]}}}
---

# My Life Feed 技能

用于为朋友和群组添加信息，以及列出我的群组。

## 设置

1. 获取您的 API 密钥：请向应用程序所有者索取该密钥。
2. 设置环境变量：
   ```bash
   export MyFeed_API_KEY="your-api-key"
   ```

## 使用方法

所有命令均通过 `curl` 来调用 My Life Feed 的 REST API。

### 创建信息并邀请朋友
```bash
curl -X POST https://skill.myfeed.life/api -H "Authorization: ApiKey $MyFeed_API_KEY" -H "Content-Type: application/json" 
-d '{"request":"create_thing",
 "params":{
   "description":"Thing description", 
   "start_time": Thing starttime in epoch,
   "alarms":[
     {
        "type": "minutes / hours / days / weeks / months",
        "value": how many units
     }
    ],
   "invites": [
      {"phone_number":"Friend phone number"}
    ]
   
 }
}'
```

### 列出群组并获取群组 ID
```bash
curl -X POST https://skill.myfeed.life/api -H "Authorization: ApiKey $Myfeed_API_KEY" -H "Content-Type: application/json" -d '
{
 "request":"get_groups",
 "params":{
   "starting_from": 1739383324000
   }
}'| jq '.groups[] | {group_id,url_group,is_admin}'
```

### 创建信息并邀请群组
```bash
curl -X POST https://skill.myfeed.life/api -H "Authorization: ApiKey $Myfeed_API_KEY" -H "Content-Type: application/json" 
-d '{"request":"create_thing",
 "params":{
   "description":"Thing description", 
   "start_time": Thing starttime in epoch in miliseconds,
   "alarms":[
     {
        "type": "minutes / hours / days / weeks / months",
        "value": how many units
     }
    ],
   "invites": [
      {"group_id":group_id }
    ]
   
 }
}'
```

## 注意事项

- 可以通过列出具有特定名称的群组来获取群组 ID。
- API 密钥和令牌可让您完全访问您的 My Life Feed / MyFeed 账户，请妥善保管！
- 请注意请求速率限制：每个 API 密钥每 10 秒内只能发送 3 次请求。

## 示例
```bash
#Get the group id by group name. Now i'm looking for the group_id of the group that has "friends" in his name.
curl -X POST https://skill.myfeed.life/api -H "Authorization: ApiKey $Myfeed_API_KEY" -H "Content-Type: application/json" -d '
{
 "request":"get_groups",
 "params":{
   "starting_from": 1739383324000
   }
}'| jq '.groups[] | select(.group|contains ("friends"))'
# Add a thing and invite a group. When you invite a group, you can't invite other people. You are adding 2 reminders before the thing time in this invite: one with 10 minutes ahead and one with 4 hours. You are adding the thing for the group with the group_id 564564646. The thing time is 1770935248000. Start time needs to be in the future.
curl -X POST https://skill.myfeed.life/api -H "Authorization: ApiKey $Myfeed_API_KEY" -H "Content-Type: application/json" 
-d '{"request":"create_thing",
 "params":{
   "description":"Thing description", 
   "start_time": 1770935248000,
   "alarms":[
     {
        "type": "minutes",
        "value": 10
     },
     {
        "type": "hours",
        "value": 4
     }
    ],
   "invites": [
      {"group_id":564564646 }
    ]
   
 }
}'
#Invites friends to a thing. Add them reminders. Add the phone number of the friend in invitation. The format is country prefix + phone number like in the example. Make sure there is no + within phone number.  You are adding 2 reminders before the thing time in this invite: one with 10 minutes ahead and one with 4 hours. Start time needs to be in the future.
curl -X POST https://skill.myfeed.life/api -H "Authorization: ApiKey $MyFeedApiKey" -H "Content-Type: application/json" 
-d '{"request":"create_thing",
 "params":{
   "description":"Thing description", 
   "start_time": 1770935248000,
   "alarms":[
     {
        "type": "minutes",
        "value": 10
     },
     {
        "type": "hours",
        "value": 4
     }
    ],
   "invites": [
      {"phone_number":"19255264501"}
    ]
 }
}'
```