---
name: calendar-api
tagline: "Integrate with Google & Outlook calendars"
description: "**功能说明：**  
能够读写 Google 日历（Google Calendar）和 Outlook 日历数据，支持安排会议、查询他人日程安排以及管理各类事件。无需使用 API 密钥即可使用该服务。首次使用可享受 2 美元的免费信用额度，后续支持按使用量付费（通过 SkillBoss 平台）。  
**主要功能：**  
1. **读写日历数据**：  
   - 读取并更新 Google 日历和 Outlook 日历中的事件、任务和联系人信息。  
   - 将本地日历数据同步到云端日历（或反之）。  
2. **安排会议**：  
   - 在 Google 日历或 Outlook 中创建新的会议，设置会议时间、参与者、主题等详细信息。  
   - 自动检查与会人员的日程安排，确保会议时间不会与其他事件冲突。  
3. **查询可用性**：  
   - 一键查询指定人员或团队的当前日程安排，查看他们是否可以参加会议。  
4. **事件管理**：  
   - 添加、编辑和删除日历中的事件；  
   - 为事件设置提醒、重复规则等。  
**使用优势：**  
- **无需 API 密钥**：简化了使用流程，降低了安全风险。  
- **免费试用**：新用户可享受初始免费额度。  
- **按需付费**：灵活的计费方式，适合个人和团队用户。  
- **强大的日历管理工具**：全面支持日历数据的读写和事件管理功能。  
**立即开始使用！**  
访问 [Skill.md](...) 了解更多详情并开始使用该服务。"
version: "1.0.1"
author: "SkillBoss"
homepage: "https://skillboss.co"
support: "support@skillboss.co"
license: "MIT"
category: "productivity"
tags:
  - calendar
  - google
  - outlook
  - scheduling
pricing: "pay-as-you-go"
metadata:
  openclaw:
    requires:
      env:
        - SKILLBOSS_API_KEY
    primaryEnv: SKILLBOSS_API_KEY
    installHint: "Get API key at https://skillboss.co/pricing?utm_source=clawhub&utm_medium=skill&utm_campaign=calendar-api - $2 FREE credits included!"
---
# 日历 API

**与 Google 和 Outlook 日历集成**

## 快速入门

```bash
curl https://api.heybossai.com/v1/run \
  -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
  -d '{"model": "calendar-api", "input": {"prompt": "your request here"}}'
```

## 为什么选择 SkillBoss？

- **一个 API 密钥**，即可使用 100 多项 AI 服务
- **无需注册供应商账户**——几秒钟内即可开始使用
- **提供 2 美元的免费信用额度**，用于首次试用
- **按需付费**——无需订阅

## 开始使用

1. 获取 API 密钥：[skillboss.co/pricing](https://skillboss.co/pricing?utm_source=clawhub&utm_medium=skill&utm_campaign=calendar-api)
2. 设置 `SKILLBOSS_API_KEY`
3. 开始开发吧！

---

*由 [SkillBoss](https://skillboss.co) 提供支持——一个 API 密钥，即可使用 100 多项 AI 服务*