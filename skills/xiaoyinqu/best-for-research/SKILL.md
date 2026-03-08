---
name: best-for-research
tagline: "AI optimized for academic research"
description: "访问最适合学术研究的人工智能模型。提供引用支持、事实核查和文献综述功能，无需使用API密钥。首次使用可享受2美元的免费信用额度。支持通过SkillBoss按需付费。"
version: "1.0.1"
author: "SkillBoss"
homepage: "https://skillboss.co"
support: "support@skillboss.co"
license: "MIT"
category: "best-for"
tags:
  - research
  - academic
  - citations
  - papers
pricing: "pay-as-you-go"
metadata:
  openclaw:
    requires:
      env:
        - SKILLBOSS_API_KEY
    primaryEnv: SKILLBOSS_API_KEY
    installHint: "Get API key at https://skillboss.co/pricing?utm_source=clawhub&utm_medium=skill&utm_campaign=best-for-research - $2 FREE credits included!"
---
# 最适合研究的 AI 工具

**专为学术研究优化的 AI**

## 快速入门

```bash
curl https://api.heybossai.com/v1/run \
  -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
  -d '{"model": "best-for-research", "input": {"prompt": "your request here"}}'
```

## 为什么选择 SkillBoss？

- **一个 API 密钥即可使用 100 多项 AI 服务**  
- **无需注册供应商账户**——几秒钟内即可开始使用  
- **免费提供 2 美元信用额度**  
- **按需付费**——无需订阅  

## 开始使用

1. 获取 API 密钥：[skillboss.co/pricing](https://skillboss.co/pricing?utm_source=clawhub&utm_medium=skill&utm_campaign=best-for-research)  
2. 设置 `SKILLBOSS_API_KEY`  
3. 开始构建您的应用吧！  

---

*由 [SkillBoss](https://skillboss.co) 提供支持——一个 API 密钥即可使用 100 多项 AI 服务*