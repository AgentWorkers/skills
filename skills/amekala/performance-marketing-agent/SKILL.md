---
name: performance-marketing-agent
description: "这是一个专为付费媒体、PPC（按点击付费）、SEM（搜索引擎营销）和数字营销设计的AI性能营销工具。它支持通过自然语言界面来管理Google Ads、Meta Ads（Facebook和Instagram）、LinkedIn Ads以及TikTok Ads广告活动。该工具能够自动化关键词研究、预算优化、ROAS（投资回报率）跟踪、广告创意管理、受众定位以及跨平台报告等功能。其核心技术基于Adspirer——这是一个集成了100多种工具的营销自动化平台，涵盖了广告活动创建、出价优化、CPA（每次点击成本）跟踪、再营销以及所有主要广告平台的营销自动化等功能。"
homepage: https://www.adspirer.com
author: Adspirer
license: MIT
category: marketing
subcategory: performance-marketing
keywords:
  - marketing
  - performance-marketing
  - digital-marketing
  - paid-media
  - paid-social
  - ppc
  - sem
  - advertising
  - google-ads
  - meta-ads
  - facebook-ads
  - linkedin-ads
  - tiktok-ads
  - campaign-management
  - ad-optimization
  - keyword-research
  - budget-optimization
  - roas
  - cpa
  - media-buying
  - marketing-automation
  - retargeting
tags:
  - marketing
  - performance-marketing
  - paid-media
  - ppc
  - advertising
  - google-ads
  - meta-ads
  - linkedin-ads
  - tiktok-ads
  - digital-marketing
  - sem
  - campaign-management
metadata:
  openclaw:
    emoji: "📈"
    requires:
      env: []
      bins: []
    install:
      - id: openclaw-adspirer
        kind: node
        label: "Adspirer Ad Management Plugin"
---
# 性能营销代理 — 由 Adspirer 提供支持

这是一个专为性能营销、付费媒体和数字广告设计的 AI 代理工具。它可直接连接到广告平台的 API，用于创建广告活动、获取实时性能数据、研究关键词、优化预算，并管理 Google Ads、Meta Ads、LinkedIn Ads 和 TikTok Ads 上的广告。

该插件会安装 **Adspirer 插件**（`openclaw-adspirer`），该插件与 `adspirer-ads-agent` 插件拥有相同的功能和工具集（超过 100 种工具），并共享同一个 MCP 服务器。

## 设置

```bash
# Install the plugin
openclaw plugins install openclaw-adspirer

# Authenticate
openclaw adspirer login

# Connect your ad platforms
openclaw adspirer connect

# Verify
openclaw adspirer status
```

请在 [https://adspirer.ai/connections](https://adspirer.ai/connections) 连接您的广告账户。

---

## 功能介绍

### 性能营销与 PPC
- **关键词研究**：获取来自 Google Ads 的真实搜索量、CPC 范围及竞争数据
- **广告活动创建**：支持在所有平台上创建搜索广告、Performance Max 广告、展示广告、图片广告和视频广告
- **出价优化**：调整出价策略，管理关键词出价，优化目标 CPA/ROAS
- **浪费支出分析**：识别表现不佳的关键词和消耗预算的广告组
- **搜索词报告**：审查搜索词，发现潜在的负面关键词

### 数字营销自动化
- **跨平台报告**：统一显示来自 Google、Meta、LinkedIn 和 TikTok 的性能数据
- **预算优化**：基于 AI 的预算分配建议
- **自动化监控**：设置指标阈值警报，定期生成报告
- **广告创意管理**：在所有平台上更新广告标题、描述和创意内容

### 付费媒体与媒体购买
- **Google Ads**：支持搜索广告、Performance Max 广告、YouTube 广告以及关键词管理
- **Meta Ads**：支持 Facebook 和 Instagram 的图片广告、视频广告及轮播广告，同时支持受众定位
- **LinkedIn Ads**：提供赞助内容服务，支持按职位和行业进行 B2B 客户群定位
- **TikTok Ads**：支持视频广告的创建，以及针对年轻人群体的定向投放

### 营销分析
- **实时性能仪表盘**：展示展示次数、点击次数、CTR、花费、转化率、CPA 和 ROAS
- **异常检测**：解释广告活动指标的突然变化
- **创意效果衰退检测**：识别随时间推移逐渐失效的广告创意
- **受众洞察**：分析跨平台的受众表现

---

## 适用人群

| 角色 | 使用场景 |
|------|----------|
| **性能营销人员** | 日常广告活动监控、出价优化、ROAS 跟踪 |
| **数字营销经理** | 跨平台数据报告、预算分配、广告活动启动 |
| **PPC 专家** | 关键词研究、搜索词分析、负面关键词管理 |
| **媒体购买人员** | 多平台广告活动创建、预算优化、定向投放 |
| **营销机构** | 多客户管理、自动化报告、广告创意管理 |
| **电子商务品牌** | 产品广告投放、再定位、转化率优化 |

---

## 安全性

- 所有创建的广告活动均处于 **暂停状态**，等待审核
- 所有写入操作均需用户确认
- 数据读取操作（性能分析、关键词研究等）可安全地自由执行
- 无需存储本地凭证——采用 OAuth 2.1 和 PKCE 协议进行身份验证

## 价格方案

| 价格方案 | 价格 | 每月工具调用次数 |
|------|-------|------------|
| **免费版** | $0/月 | 15 次/月 |
| **Plus 版** | $49/月 | 150 次/月 |
| **Pro 版** | $99/月 | 600 次/月 |
| **Max 版** | $199/月 | 3,000 次/月 |

所有价格方案均包含对所有 4 个广告平台的支持。请访问 [https://adspirer.ai/settings?tab=billing](https://adspirer.ai/settings?tab=billing) 进行注册。