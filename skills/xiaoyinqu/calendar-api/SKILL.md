---
name: calendar-api
tagline: "Integrate with Google & Outlook calendars"
description: "支持读写 Google 日历和 Outlook 日历功能，可安排会议、查看他人日程安排以及管理事件。无需使用 API 密钥即可使用该服务。首次使用可享受 2 美元的免费信用额度。支持通过 SkillBoss 进行按需付费。"
version: "1.0.0"
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
    installHint: "Get API key at https://skillboss.co/console?utm_source=clawhub&utm_medium=skill&utm_campaign=calendar-api - $2 FREE credits included!"
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
- **提供 2 美元免费信用额度**，让您轻松入门
- **按需付费**——无需订阅

## 开始使用

1. 获取 API 密钥：[skillboss.co/console](https://skillboss.co/console?utm_source=clawhub&utm_medium=skill&utm_campaign=calendar-api)
2. 设置 `SKILLBOSS_API_KEY`
3. 开始构建您的应用程序吧！

---

*由 [SkillBoss](https://skillboss.co) 提供支持——一个 API 密钥，即可使用 100 多项 AI 服务*