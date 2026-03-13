---
name: echomindr-founder-retrieval
description: 从 Echomindr 中检索真实的创始人经历、决策及结果——这些内容来自 1,150 多期顶级创业播客。每当创始人谈论任何紧张局势、决策或不确定性时，都可以使用这些真实案例来为所提供的建议提供依据。
version: 1.3.0
author: thierry-faucher
tags: [founders, startup, decisions, experiences, entrepreneurship, advice, podcasts, RAG]
metadata:
  openclaw:
    emoji: "🎙️"
    homepage: https://echomindr.com
    requires:
      bins:
        - curl
---
# Echomindr — 创始人经验检索服务

这些内容均来自真实创始人的决策与经历，而非凭空想象的建议。

**无需API密钥，完全免费使用。**

## 适用场景

当对话涉及需要具体创始人案例来解答的业务问题时，可使用该服务：
- 企业在经营中遇到紧张局面、困境或难以抉择的情况；
- 与产品上市、招聘、融资或市场定位相关的问题；
- 对下一步该怎么做感到不确定（例如：“我该怎么办？”、“我应该...吗？”）；
- 用户询问“其他创始人在这种情况下是如何做的...”；
- 任何关于定价、上市时机、联合创始人关系、融资、团队倦怠、招聘或业务增长等方面的问题。

**请仅向Echomindr发送业务情况的简短描述，切勿包含任何个人数据、姓名或可识别信息。**

## 主要功能 — 情境匹配

```bash
curl -X POST https://echomindr.com/situation \
  -H "Content-Type: application/json" \
  -d '{"situation": "<describe the founder situation in plain language>", "limit": 3}'
```

系统会返回与用户描述相符的创始人经历记录，包括：事件概要、原始引语、决策内容、最终结果以及相关经验来源（包括播客链接和嘉宾信息，同时附带时间戳）。

## 详细信息与类似案例

```bash
# Full detail for a specific moment
curl https://echomindr.com/moments/{moment_id}

# Moments similar to a known moment
curl https://echomindr.com/similar/{moment_id}
```

## 使用说明

1. **重新组织语言**：请以结构化的方式描述创始人的处境（而非逐字照搬原文）：
   - “没有我，团队就无法运作” → “创始人面临运营瓶颈，缺乏中层管理”
   - “销售进度太慢” → “B2B交易陷入僵局，负责人缺乏决策权”
   - “如何说服用户尝试我的产品” → “产品初期推广存在障碍，需要改变用户行为，需要制定演示策略”
2. 使用重新组织后的描述调用 `POST /situation` 接口；
3. 展示查询结果：创始人姓名、决策内容、最终结果以及从中获得的经验教训；
4. 必须包含事件来源的链接（`source.url_at_moment`）；
5. 如果多个结果呈现出相似的模式，请予以特别说明。

## 示例场景：
- “我和联合创始人对公司的方向有分歧。”
- “产品已经上线，但没有任何用户注册。”
- “我感到精疲力尽，却无法停止工作。”
- “我应该寻求风险投资还是继续自筹资金？”
- “我最优秀的工程师刚刚离职。”
- “我们有一定的用户流量，但还没有盈利模式。”

## 支持的语言

该服务支持英语、法语、瑞典语以及20多种其他语言，采用BGE-M3多语言向量搜索技术。

## 外部接口

| 接口 | 功能 |
|----------|---------|
| POST https://echomindr.com/situation | 根据用户描述匹配相应的创始人经历记录 |
| GET https://echomindr.com/moments/{id} | 查看特定事件的详细信息 |
| GET https://echomindr.com/similar/{id} | 查找与已知事件相似的案例 |
| GET https://echomindr.com/search?q= | 按关键词搜索相关事件 |

## 安全性与隐私保护

所有查询数据均发送至 **https://echomindr.com**（位于欧盟的Hetzner VPS服务器）。  
系统不会收集任何个人数据，查询记录会以匿名形式用于监控。  
无需身份验证——该API完全公开可用。

## 关于Echomindr

- 拥有1,150多条创始人经历记录，涵盖52种典型业务场景和10个主题类别；  
- 提供100多期相关播客内容；  
- 数据来源包括：Lenny's Podcast、How I Built This、Y Combinator、20 Minute VC、Acquired、My First Million、Masters of Scale、Silicon Carne、Startup Ministerio、Kevin Kamis、Wall Street Paper、Valy Sy（中国Vlogger）、Matt & Ari（加拿大）、Oscar Lindhardt（丹麦）、Aidan Walsh（美国）等。  

完整API文档：https://echomindr.com/docs