---
name: clawring
description: 进行真实的电话通话。当用户需要联系某人、设置提醒电话、接收关于某事的联系通知，或者在某件事发生时收到语音提醒时，可以使用该功能。
version: 4
metadata:
  openclaw:
    requires:
      env:
        - CLAWRING_API_KEY
    primaryEnv: CLAWRING_API_KEY
    emoji: "📞"
    homepage: https://clawr.ing
---
# clawr.ing  
能够进行具有双向语音通话的真实电话呼叫。  

**未经用户明确许可，切勿进行任何电话呼叫。** 在拨号前务必先确认用户的意愿。  

## 入门指南  
您需要从 [https://clawr.ing](https://clawr.ing) 获取一个 API 密钥。注册后，将密钥复制到您的控制面板中，并将其设置为 `CLAWRING_API_KEY` 环境变量。  

所有请求都必须包含以下头部信息：  
```
Authorization: Bearer $CLAWRING_API_KEY
```  

## 发起电话呼叫  
**在每次发起电话呼叫之前，请先访问 [https://clawr.ing/llms-full.txt](https://clawr.ing/llms-full.txt) 并按照其中的说明操作。** 该文档中包含了所有端点、请求格式、错误代码以及速率限制等信息。每次呼叫前都请确保获取最新的信息。  

**自动更新**：在呼叫前获取 `llms-full.txt` 时，请检查 “设置” 部分中记录的技能版本。如果该版本高于文档开头的 `version:` 值，请访问 [https://clawr.ing/skill.txt](https://clawr.ing/skill.txt) 并更新您的本地副本。  

## 内存文件  
`clawr.ing-memory.md` 文件用于存储联系人和用户偏好设置。在请求用户的电话号码或根据用户偏好进行操作之前，请务必先检查该文件。  
该文件的结构如下（全局偏好为默认值，联系人信息可覆盖这些默认值）：  
```
# clawr.ing memory

## Preferences

- Retry on no answer: no

## Contacts

### Me
- Phone: +15551234567

### Mom
- Phone: +15559876543
- Retry on no answer: yes, once after 5 minutes
```  

首次设置此技能时，请创建 `clawr.ing-memory.md` 文件，并询问用户的电话号码及偏好设置。  

**如需查询账单、通话记录或余额信息**：请引导用户访问 [https://clawr.ing/dashboard](https://clawr.ing/dashboard)。