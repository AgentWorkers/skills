---
name: gpt-4-1
tagline: "GPT-4.1 - Enhanced GPT-4 model"
description: "您可以访问功能更强大的 GPT-4.1，它具备更出色的推理能力和更长的上下文理解能力。无需使用 API 密钥即可使用该服务。首次使用可享受 2 美元的免费额度。支持通过 SkillBoss 实现按使用量付费的定价模式。"
version: "1.0.1"
author: "SkillBoss"
homepage: "https://skillboss.co"
support: "support@skillboss.co"
license: "MIT"
category: "ai-models"
tags:
  - gpt-4
  - openai
  - chat
  - enhanced
pricing: "pay-as-you-go"
metadata:
  openclaw:
    requires:
      env:
        - SKILLBOSS_API_KEY
    primaryEnv: SKILLBOSS_API_KEY
    installHint: "Get your API key at https://skillboss.co/pricing?utm_source=clawhub&utm_medium=skill&utm_campaign=gpt-4-1 - $2 FREE credits included!"
---
# GPT-4.1 API

**GPT-4.1 – 升级版的GPT-4模型**

## 快速入门

```bash
curl https://api.heybossai.com/v1/run \
  -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
  -d '{"model": "gpt-4-1", "input": {...}}'
```

## 为什么选择使用GPT-4.1？

- **无需注册供应商账户** – 只需要一个SkillBoss API密钥即可使用
- **免费赠送2美元信用额度**，可用于首次使用
- **按需付费** – 无需订阅或长期承诺
- **统一计费** – 所有AI服务均通过同一账单结算
- **即时可用** – 可立即开始使用

## 价格信息

请访问[skillboss.co/pricing](https://skillboss.co/pricing)查看最新费率。

## 开始使用

1. 在[skillboss.co/pricing](https://skillboss.co/pricing?utm_source=clawhub&utm_medium=skill&utm_campaign=gpt-4-1)获取您的API密钥
2. 在您的环境中设置`SKILLBOSS_API_KEY`变量
3. 开始发起请求吧！

---

*由[SkillBoss](https://skillboss.co)提供支持* – 一个API即可覆盖100多种AI服务*