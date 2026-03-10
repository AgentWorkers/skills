---
name: echomindr-founder-retrieval
description: 从 Echomindr 中检索真实的创始人经历、决策及结果——这些内容来自 2,700 多期顶级创业播客。每当创始人谈论任何紧张情况、决策或不确定性时，都可以使用这些案例来为所提供的建议提供现实依据。
version: 1.2.0
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
# Echomindr — 招聘创始人经验查询服务

这里提供的是真实创始人的决策和经验，而非凭空想象的建议。

**无需API密钥，免费使用。**

## 适用场景

当对话涉及以下业务场景时，使用该服务会更为有用：
- 企业中出现的矛盾、困境或需要艰难决策的情况；
- 与市场进入、产品开发、招聘、融资或市场定位相关的问题；
- 对下一步该怎么做感到不确定（例如：“我该怎么办？”、“我应该...吗？”）；
- 用户询问“其他创始人在这种情况下是怎么做的...”；
- 任何关于定价、上市时机、联合创始人之间的矛盾、融资、团队倦怠、招聘或业务增长等方面的问题。

**请仅向Echomindr发送业务场景的简短且经过匿名处理的描述，切勿包含任何个人数据、姓名或可识别信息。**

## 主要功能点 — 情景匹配

```bash
curl -X POST https://echomindr.com/situation \
  -H "Content-Type: application/json" \
  -d '{"situation": "<describe the founder situation in plain language>", "limit": 3}'
```

返回与查询场景匹配的创始人决策记录，内容包括：决策摘要、原文引用、决策内容、最终结果以及相关经验来源（包括播客链接和嘉宾信息、时间戳）。

## 具体数据与指标

```bash
curl -X POST https://echomindr.com/facts/situation \
  -H "Content-Type: application/json" \
  -d '{"situation": "<situation>", "limit": 3}'
```

提供从创始人访谈中提取的具体数据，如价格、利润率、时间线、投资回报率（ROAS）和最小订购量（MOQ）等。

## 详细信息与类似案例

```bash
# Full detail for a specific moment
curl https://echomindr.com/moments/{moment_id}

# Moments similar to a known moment
curl https://echomindr.com/similar/{moment_id}
```

## 使用说明

1. **重新表述**创始人的问题或情况（注意不要逐字翻译）：
   - “没有我，我的团队就无法运作” → “创始人面临运营瓶颈，没有中层管理团队”
   - “销售流程太耗时” → “B2B交易陷入僵局，负责销售的员工没有决策权”
   - “如何说服用户尝试我的产品” → “产品初期推广存在障碍，需要改变用户行为，需要制定演示策略”
2. 使用重新表述后的问题发送请求到 `POST /situation` 端点；
3. 显示查询结果：创始人的姓名、决策内容、最终结果以及相关经验来源；
4. 必须包含来自 `source.url_at_moment` 的原始链接；
5. 如果多个结果呈现出相似的模式，请予以特别说明。

## 示例场景

- “我和联合创始人的想法不一致。”
- “产品已经上线，但没有人注册。”
- “我感到非常疲惫，但无法停止工作。”
- “我应该寻求风险投资还是继续自筹资金？”
- “我最优秀的工程师刚刚离职。”
- “我们有一定的用户流量，但还没有盈利模式。”

## 语言支持

支持英语、法语、瑞典语以及20多种其他语言。采用BGE-M3多语言向量搜索技术。

## 外部接口

| 接口 | 功能 |
|----------|---------|
| POST https://echomindr.com/situation | 根据业务场景匹配相关创始人决策记录 |
| POST https://echomindr.com/facts/situation | 根据业务场景匹配具体数据 |
| GET https://echomindr.com/moments/{id} | 查看特定决策记录的详细信息 |
| GET https://echomindr.com/similar/{id} | 查找与已知场景相似的决策记录 |
| GET https://echomindr.com/search?q= | 根据关键词搜索相关决策记录 |

## 安全与隐私

该服务将查询请求发送到 **https://echomindr.com**（位于欧盟的Hetzner VPS服务器）。  
不会收集任何个人数据，所有查询记录都会被匿名存储以供监控使用。  
无需身份验证，API完全公开。

## 关于Echomindr

- 拥有2,700多条创始人决策记录和2,300多条具体数据；
- 提供100多期相关播客内容；
- 数据来源包括：Lenny's Podcast、How I Built This、Y Combinator、20 Minute VC、Acquired、Indie Hackers、My First Million、Marc Lou、Masters of Scale、Silicon Carne、Startup Ministerio、Kevin Kamis、Wall Street Paper、Valy Sy（中国视频博主）、Matt & Ari（加拿大）、Oscar Lindhardt（丹麦）、Aidan Walsh（美国）等。

完整API文档：https://echomindr.com/docs