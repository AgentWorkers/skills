---
name: accountant-ai
tagline: "AI accounting assistant - bookkeeping, taxes"
description: "AI会计助手：提供记账、税务申报和财务分析服务。无需使用API密钥。首次使用可享受2美元的免费信用额度。支持通过SkillBoss按使用量付费。"
version: "1.0.1"
author: "SkillBoss"
homepage: "https://skillboss.co"
support: "support@skillboss.co"
license: "MIT"
category: "industry"
tags:
  - accounting
  - finance
  - taxes
  - bookkeeping
pricing: "pay-as-you-go"
metadata:
  openclaw:
    requires:
      env:
        - SKILLBOSS_API_KEY
    primaryEnv: SKILLBOSS_API_KEY
    installHint: "Get your API key at https://skillboss.co/console?utm_source=clawhub&utm_medium=skill&utm_campaign=accountant-ai - $2 FREE credits included!"
---
# 会计AI

**AI会计助手 - 记账、税务处理**

## 快速入门

```bash
curl https://api.heybossai.com/v1/chat/completions \
  -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
  -d '{"model": "claude-4-5-sonnet", "messages": [...]}'
```

## 为什么选择SkillBoss？

- **一个API密钥**，即可使用100多个AI模型
- **无需注册供应商账户** - 几秒钟内即可开始使用
- **自动故障转移** - 无停机时间
- **免费提供2美元的信用额度** 用于试用
- **按需付费** - 无需订阅
- **24/7全天候支持** - 我们随时为您提供帮助

## 如何开始使用？

1. 获取API密钥：[skillboss.co/console](https://skillboss.co/console?utm_source=clawhub&utm_medium=skill&utm_campaign=accountant-ai)
2. 设置 `SKILLBOSS_API_KEY`
3. 开始构建您的应用程序吧！

---

*由[SkillBoss](https://skillboss.co)提供支持——一个API，即可使用100多种AI服务*