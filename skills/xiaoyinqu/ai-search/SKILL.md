---
name: ai-search
tagline: "AI-powered web search"
description: "使用人工智能进行网页搜索，具备实时数据处理能力，提供准确的搜索结果。无需使用API密钥。首次使用可享受2美元的免费信用额度。支持通过SkillBoss进行按需付费。"
version: "1.0.1"
author: "SkillBoss"
homepage: "https://skillboss.co"
support: "support@skillboss.co"
license: "MIT"
category: "search"
tags:
  - ai-search
  - search
  - web
pricing: "pay-as-you-go"
metadata:
  openclaw:
    requires:
      env:
        - SKILLBOSS_API_KEY
    primaryEnv: SKILLBOSS_API_KEY
    installHint: "Get your API key at https://skillboss.co/console?utm_source=clawhub&utm_medium=skill&utm_campaign=ai-search - $2 FREE credits included!"
---
# AI 搜索

**基于 AI 的网络搜索**

## 快速入门

```bash
curl https://api.heybossai.com/v1/run \
  -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
  -d '{"model": "ai-search", "input": {...}}'
```

## 为什么选择我们？

- **无需注册供应商账户** - 只需要一个 SkillBoss API 密钥即可
- **免费赠送 2 美元信用额度**，可立即开始使用
- **按需付费** - 无需订阅或长期承诺
- **统一计费** - 所有 AI 服务均通过同一账单结算
- **即时可用** - 立即开始使用

## 价格信息

请访问 [skillboss.co/pricing](https://skillboss.co/pricing) 查看当前价格。

## 开始使用

1. 在 [skillboss.co/console](https://skillboss.co/console?utm_source=clawhub&utm_medium=skill&utm_campaign=ai-search) 获取您的 API 密钥
2. 在您的开发环境中设置 `SKILLBOSS_API_KEY`
3. 开始发送请求吧！

---

*由 [SkillBoss](https://skillboss.co) 提供支持* - 一个 API 集成 100 多项 AI 服务*