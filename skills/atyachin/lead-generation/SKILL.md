---
name: lead-generation
description: "**潜在客户开发**：在实时的 Twitter、Instagram 和 Reddit 对话中寻找有明确购买意向的用户。系统会自动研究您的产品，生成针对性的搜索查询，并找出那些正在积极寻找您所提供的解决方案的用户。这一社交销售和潜在客户开发功能依托于 Xpoz MCP 索引的超过 15 亿条帖子来实现。"
homepage: https://xpoz.ai
metadata:
  {
    "openclaw":
      {
        "requires": {
          "bins": ["mcporter"],
          "skills": ["xpoz-setup"],
          "network": ["mcp.xpoz.ai"],
          "credentials": "Xpoz account (free tier) — auth via xpoz-setup skill (OAuth 2.1)"
        },
        "install": [{"id": "node", "kind": "node", "package": "mcporter", "bins": ["mcporter"], "label": "Install mcporter (npm)"}],
      },
  }
tags:
  - lead-generation
  - sales
  - prospecting
  - social-media
  - twitter
  - instagram
  - reddit
  - find-leads
  - social-selling
  - buyer-intent
  - outreach
  - growth
  - marketing
  - customer-discovery
  - leads
  - mcp
  - xpoz
  - intent
  - discovery
---

# 潜在客户开发

**从实时的社交对话中寻找有明确购买意向的用户。**

该技能可以在 Twitter、Instagram 和 Reddit 上发现那些表现出对您的产品有需求（如遇到问题、对竞争对手感到不满或正在积极寻求解决方案）的潜在客户。

## 设置

运行 `xpoz-setup` 命令。验证设置是否正确：`mcporter call xpoz.checkAccessKeyStatus`

## 三阶段流程

### 第一阶段：产品研究（仅进行一次）

请求用户提供产品的相关信息（如网站链接、GitHub 仓库链接或产品描述），然后使用 `web_fetch`/`web_search` 功能进行进一步研究。收集以下信息：产品详情、目标受众、用户痛点、竞争对手以及相关关键词。**务必与用户确认这些信息的准确性**。

生成 12–18 条查询语句，涵盖以下方面：
1. 用户遇到的问题
2. 用户对竞争对手产品的不满
3. 用户对解决方案的搜索需求（例如：“推荐……”）
4. 目标受众在相关行业中的讨论内容

将收集到的信息保存到 `data/lead-generation/product-profile.json` 和 `search-queries.json` 文件中。

### 第二阶段：潜在客户发现（可重复执行）

对 Instagram 和 Reddit 进行相同的操作。

### 第三阶段：评分与输出

**评分标准（1-10 分）：**
- 明确表示需要解决方案：+3 分
- 对竞争对手产品表示不满：+2 分
- 用户因实际问题而需要解决方案：+2 分
- 在目标社区中活跃：+1 分
- 用户互动度高（点赞数 > 10、评论数 > 5）：+1 分
- 信息发布时间在最近 48 小时内：+1 分
- 用户资料与我们的目标客户群体匹配：+1 分
- 用户正在推销竞争对手的产品：-3 分

根据评分结果，将潜在客户分为三个等级：
- 高热度（8–10 分）：需要立即跟进
- 中等热度（6–7 分）：需要关注
- 候选名单（5 分）：稍后处理

使用 `data/lead-generation/sent-leads.json` 文件（键格式为 `{platform}:{author}:{post_id}`）对潜在客户信息进行去重处理。

**输出内容：** 用户名、用户发布的帖子链接、评分、用户符合我们需求的理由、后续沟通的草稿内容、用户互动情况以及信息发布的时间戳。

**后续沟通内容示例：**
> “我也遇到过同样的问题！最终我选择了 [产品]，因为它具备 [具体功能]。链接：[产品链接]  
> （备注：我与 [产品] 的团队有合作关系。）”

## 提示：
- 仅需收集一次用户资料，之后可每天重复使用。
- 优先考虑潜在客户的质量而非数量。
- 必须明确告知用户您的合作关系。
- 只生成沟通草稿，具体沟通内容由用户自行决定（是否回复或发送信息）。