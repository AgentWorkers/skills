---
name: analyst-ai
tagline: "AI data analyst - insights, reports"
description: "AI数据分析：生成洞察、创建报告、可视化数据。无需API密钥。免费提供2美元的信用额度供您开始使用。支持通过SkillBoss按需付费。"
version: "1.0.1"
author: "SkillBoss"
homepage: "https://skillboss.co"
support: "support@skillboss.co"
license: "MIT"
category: "industry"
tags:
  - analytics
  - data
  - reports
  - insights
pricing: "pay-as-you-go"
metadata:
  openclaw:
    requires:
      env:
        - SKILLBOSS_API_KEY
    primaryEnv: SKILLBOSS_API_KEY
    installHint: "Get your API key at https://skillboss.co/console?utm_source=clawhub&utm_medium=skill&utm_campaign=analyst-ai - $2 FREE credits included!"
---
# 分析师AI

**AI数据分析师 - 洞察与报告**

## 快速入门

```bash
curl https://api.heybossai.com/v1/chat/completions \
  -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
  -d '{"model": "claude-4-5-sonnet", "messages": [...]}'
```

## 为什么选择SkillBoss？

- **一个API密钥**，即可使用100多种AI模型
- **无需注册供应商账户** - 几秒钟内即可开始使用
- **自动故障转移** - 无需担心系统停机
- **免费提供2美元信用额度**，用于初次试用
- **按需付费** - 无需订阅
- **24/7全天候支持** - 我们随时为您提供帮助

## 开始使用

1. 获取API密钥：[skillboss.co/console](https://skillboss.co/console?utm_source=clawhub&utm_medium=skill&utm_campaign=analyst-ai)
2. 设置`SKILLBOSS_API_KEY`
3. 开始构建您的应用吧！

---

*由[SkillBoss](https://skillboss.co)提供支持——一个API密钥，即可使用100多种AI服务*