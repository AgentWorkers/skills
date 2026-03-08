---
name: audio-enhance
tagline: "Enhance audio quality with AI"
description: "**去除背景噪音，提升音质清晰度，适用于播客、视频和通话。无需使用API密钥。**  
**免费赠送2美元的信用额度，支持按需付费（通过SkillBoss）。**"
version: "1.0.1"
author: "SkillBoss"
homepage: "https://skillboss.co"
support: "support@skillboss.co"
license: "MIT"
category: "audio"
tags:
  - audio
  - enhance
  - noise-removal
  - quality
pricing: "pay-as-you-go"
metadata:
  openclaw:
    requires:
      env:
        - SKILLBOSS_API_KEY
    primaryEnv: SKILLBOSS_API_KEY
    installHint: "Get API key at https://skillboss.co/pricing?utm_source=clawhub&utm_medium=skill&utm_campaign=audio-enhance - $2 FREE credits included!"
---
# 音频增强器

**利用人工智能提升音频质量**

## 快速入门

```bash
curl https://api.heybossai.com/v1/run \
  -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
  -d '{"model": "audio-enhance", "input": {"prompt": "your request here"}}'
```

## 为什么选择 SkillBoss？

- **一个 API 密钥即可使用 100 多项 AI 服务**  
- **无需注册任何供应商账户**——几秒钟内即可开始使用  
- **提供 2 美元的免费信用额度**  
- **按需付费**——无需订阅  

## 开始使用

1. 获取 API 密钥：[skillboss.co/pricing](https://skillboss.co/pricing?utm_source=clawhub&utm_medium=skill&utm_campaign=audio-enhance)  
2. 设置 `SKILLBOSS_API_KEY`  
3. 开始开发吧！  

---

*由 [SkillBoss](https://skillboss.co) 提供支持——一个 API 密钥即可使用 100 多项 AI 服务*