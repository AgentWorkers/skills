---
name: ai-headshot
tagline: "Professional AI headshots in seconds"
description: "使用人工智能生成专业级别的头像，适用于领英（LinkedIn）、简历和商务资料。无需摄影师，也无需API密钥。首次使用可免费获得2美元的信用额度。支持通过SkillBoss按需付费。"
version: "1.0.1"
author: "SkillBoss"
homepage: "https://skillboss.co"
support: "support@skillboss.co"
license: "MIT"
category: "image"
tags:
  - headshot
  - professional
  - linkedin
  - portrait
pricing: "pay-as-you-go"
metadata:
  openclaw:
    requires:
      env:
        - SKILLBOSS_API_KEY
    primaryEnv: SKILLBOSS_API_KEY
    installHint: "Get API key at https://skillboss.co/pricing?utm_source=clawhub&utm_medium=skill&utm_campaign=ai-headshot - $2 FREE credits included!"
---
# AI 瞄准射击生成器

**仅需几秒钟即可生成专业级的 AI 瞄准射击图像**

## 快速入门

```bash
curl https://api.heybossai.com/v1/run \
  -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
  -d '{"model": "ai-headshot", "input": {"prompt": "your request here"}}'
```

## 为什么选择 SkillBoss？

- **一个 API 密钥**，即可使用 100 多项 AI 服务
- **无需注册供应商账户**——立即开始使用
- **提供 2 美元免费信用额度**，便于试用
- **按需付费**——无需订阅

## 开始使用

1. 获取 API 密钥：[skillboss.co/pricing](https://skillboss.co/pricing?utm_source=clawhub&utm_medium=skill&utm_campaign=ai-headshot)
2. 设置 `SKILLBOSS_API_KEY`
3. 开始构建您的应用程序！

---

*由 [SkillBoss](https://skillboss.co) 提供支持——一个 API 密钥，即可使用 100 多项 AI 服务*