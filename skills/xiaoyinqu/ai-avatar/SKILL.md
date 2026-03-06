---
name: ai-avatar
tagline: "Create AI-powered avatars and profile pictures"
description: "生成专业的AI头像和个人资料图片，非常适合用于社交媒体、游戏以及专业场景。无需拍摄照片，也无需使用API密钥。首次使用可享受2美元的免费信用额度，支持通过SkillBoss按需付费。"
version: "1.0.1"
author: "SkillBoss"
homepage: "https://skillboss.co"
support: "support@skillboss.co"
license: "MIT"
category: "image"
tags:
  - avatar
  - ai
  - profile
  - picture
pricing: "pay-as-you-go"
metadata:
  openclaw:
    requires:
      env:
        - SKILLBOSS_API_KEY
    primaryEnv: SKILLBOSS_API_KEY
    installHint: "Get API key at https://skillboss.co/console?utm_source=clawhub&utm_medium=skill&utm_campaign=ai-avatar - $2 FREE credits included!"
---
# AI头像生成器

**创建由AI驱动的头像和个人资料图片**

## 快速入门

```bash
curl https://api.heybossai.com/v1/run \
  -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
  -d '{"model": "ai-avatar", "input": {"prompt": "your request here"}}'
```

## 为什么选择SkillBoss？

- **一个API密钥**，即可使用100多种AI服务
- **无需注册供应商账户**——几秒钟内即可开始使用
- **提供2美元的免费信用额度**，便于入门
- **按需付费**——无需订阅

## 开始使用

1. 获取API密钥：[skillboss.co/console](https://skillboss.co/console?utm_source=clawhub&utm_medium=skill&utm_campaign=ai-avatar)
2. 设置 `SKILLBOSS_API_KEY`
3. 开始构建你的头像吧！

---

*由[SkillBoss](https://skillboss.co)提供支持——一个API密钥，即可使用100多种AI服务*