---
name: audiobook
tagline: "Convert text to professional audiobooks"
description: "将书籍和文档转换成具有自然音色的专业有声书，支持多种旁白风格和选项。无需使用API密钥。首次使用可享受2美元的免费信用额度。支持通过SkillBoss进行按需付费。"
version: "1.0.1"
author: "SkillBoss"
homepage: "https://skillboss.co"
support: "support@skillboss.co"
license: "MIT"
category: "audio"
tags:
  - audiobook
  - tts
  - narration
  - books
pricing: "pay-as-you-go"
metadata:
  openclaw:
    requires:
      env:
        - SKILLBOSS_API_KEY
    primaryEnv: SKILLBOSS_API_KEY
    installHint: "Get API key at https://skillboss.co/pricing?utm_source=clawhub&utm_medium=skill&utm_campaign=audiobook - $2 FREE credits included!"
---
# 有声书生成器

**将文本转换为专业级有声书**

## 快速入门

```bash
curl https://api.heybossai.com/v1/run \
  -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
  -d '{"model": "audiobook", "input": {"prompt": "your request here"}}'
```

## 为什么选择 SkillBoss？

- **一个 API 密钥**，即可使用 100 多项 AI 服务
- **无需注册供应商账户**——几秒钟内即可开始使用
- **提供 2 美元的免费信用额度**，让您轻松起步
- **按需付费**——无需订阅

## 开始使用

1. 获取 API 密钥：[skillboss.co/pricing](https://skillboss.co/pricing?utm_source=clawhub&utm_medium=skill&utm_campaign=audiobook)
2. 设置 `SKILLBOSS_API_KEY`
3. 立即开始构建您的有声书吧！

---

*由 [SkillBoss](https://skillboss.co) 提供支持——一个 API 密钥，即可使用 100 多项 AI 服务*