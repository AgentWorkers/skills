---
name: soul-weaver
version: 1.0.1
description: 通过授权的 API 访问生成 OpenClaw 代理配置文件。这需要手动验证以及申请官方的 API 密钥。
author: AI Soul Weaver Team
tags:
  - openclaw
  - soul-weaver
  - ai
  - agent
  - configuration
category: productivity
permissions:
  - network
platform:
  - openclaw
---
# Soul Weaver 技能

## 描述

通过授权的 API 访问生成 OpenClaw 代理配置文件。用户必须先在官方网站上手动验证配置，然后通过官方渠道申请 API 密钥。

## 安全说明

- 需要通过正规申请流程获取官方 API 密钥。
- 用户必须先在官方网站上手动验证配置。
- 仅使用授权的 API 端点。
- 不会自动修改或替换任何系统文件。
- 需要使用有效的 API 凭据进行明确的用户操作。

## 使用流程

### 第一步：手动验证
首先访问官方网站，手动创建并验证配置。

### 第二步：申请 API 密钥
通过官方的 AI Soul Weaver 平台申请 API 密钥：

**网站**: https://sora2.wboke.com

您需要：
1. 在网站上注册账户。
2. 登录您的账户。
3. 在账户控制面板中申请 API 访问权限。

### 第三步：授权访问
使用您的授权凭据使用该技能：

```javascript
const result = await handler({
  apiKey: "your_authorized_key", // Required: API key from official application
  apiEndpoint: "https://your-api-endpoint.com", // Optional: custom endpoint
  aiName: "MyAI",
  celebrityName: "musk", 
  profession: "Entrepreneur",
  language: "EN"
});
```

## 返回内容

返回 6 个配置文件：SOUL.md、IDENTITY.md、MEMORY.md、USER.md、TOOLS.md、AGENTS.md

## 重要提示

- 自动化生成功能需要 API 密钥。
- 密钥必须通过正规申请流程获取。
- 严格禁止未经授权的 API 访问。
- 所有 API 调用都会被记录并用于安全监控。
- 用户需负责密钥的安全管理和妥善保管。