---
name: ai-traffic-tracking
description: 当用户希望在 Google Analytics 4 (GA4) 或 Google Search Console (GSC) 中追踪与 AI 相关的搜索流量时，可以使用此方法。此外，当用户提到“AI 流量”、“ChatGPT 引荐流量”、“Perplexity 流量”、“AI 概览”、“GA4 中的 AI 来源”、“AI 搜索分析”、“追踪 AI 引荐流量”、“AI 搜索流量”或“如何追踪 AI 流量”等术语时，也适用此方法。
metadata:
  version: 1.0.0
---
# 分析：人工智能流量

本指南介绍了如何在 Google Analytics 4 和 Google Search Console 中追踪由人工智能驱动的搜索流量。

**使用说明**：
- **首次使用**时，可简要说明该功能的用途及其重要性，然后再展示主要输出内容；
- **后续使用**或用户要求跳过介绍时，可直接查看主要输出内容。

## 范围
- **人工智能搜索流量**：在 GA4 和 GSC 中进行追踪，并将人工智能来源与自然搜索流量区分开来；
- **Google AI 概览**：Google 搜索结果页面中的人工智能相关摘要信息（以前称为 SGE）；
- **人工智能驱动的搜索**：来自 ChatGPT、Perplexity、Gemini、Claude、Copilot 等平台的流量。

## 为何需要单独追踪人工智能流量？
- 人工智能流量正在快速增长，但 GA4 通常将其归类为“推荐流量”、“自然搜索流量”或“直接流量”；
- 人工智能访问者的购买意愿可能更强，转化率也更高；
- 将人工智能流量与自然搜索流量区分开来有助于评估人工智能对网站的影响。

## 在 GA4 中追踪人工智能驱动的搜索流量

### 方法 1：探索报告（推荐）

1. 进入“探索”功能；
2. 选择“自由形式”报告；
3. 设置维度：“会话来源”（或“会话来源/媒介”）；
4. 选择指标：会话数、参与率、事件数量等；
5. 添加过滤器：`会话来源`，并使用以下正则表达式进行筛选；
6. 配置报告格式并保存。

**常见的人工智能来源正则表达式**：
```
chatgpt\.com|openai\.com|openai|perplexity\.ai|perplexity|doubao\.com|chat\.qwen\.ai|copilot\.microsoft\.com|copilot\.com|(business\.)?gemini\.google|chat\.deepseek\.com|deepseek\.com|poe\.com|anthropic\.com|claude\.ai|bard\.google\.com|edgeservices\.bing\.com
```

### 方法 2：自定义渠道组

1. 进入“管理” → “数据展示” → “渠道组”；
2. 复制默认的渠道组，例如命名为“默认渠道组 + 人工智能聊天机器人”；
3. 添加新的渠道“人工智能聊天机器人”，并设置筛选条件：`来源`符合上述正则表达式；
4. 确保“人工智能聊天机器人”渠道在“推荐流量”渠道之上，以便优先显示；
5. 保存设置并在“流量获取”报告中使用该渠道组。

### 方法 3：自定义报告

1. 进入“报告” → “报告库” → 创建详细报告；
2. 使用“流量获取”模板；
3. 添加过滤器：`会话来源`，并使用上述正则表达式进行筛选；
4. 保存报告并将其添加到报告菜单中。

## 常见的人工智能来源域名

| 平台 | GA4 中的来源示例 |
|----------|---------------------|
| ChatGPT | chatgpt.com, openai |
| Perplexity | perplexity.ai, perplexity |
| Copilot | copilot.com, copilot.microsoft.com |
| Gemini | business.gemini.google, gemini.google |
| Claude | claude.ai, anthropic.com |
| Bing Chat | edgeservices.bing.com |

## Google AI 概览
- **GA4**：某些人工智能相关点击会包含特定的 URL 片段；可以使用 Google Tag Manager (GTM) 进行更详细的追踪（部分功能有限）；
- **GSC**：有关在 GSC 中分析人工智能流量的方法（包括筛选条件），请参阅 [Google Search Console 文档]。

## 检查清单
- [ ] 已在 GA4 中识别出所有的人工智能来源；
- [ ] 已创建用于追踪人工智能流量的报告；
- [ ] 如果使用了自定义渠道组，已将其设置为“推荐流量”之上；
- [ ] 如果需要，已将自定义报告添加到报告库中；
- [ ] （可选）已配置 GTM 和 URL 片段以用于追踪人工智能流量；
- [ ] （可选）已设置 GSC 中的人工智能相关查询过滤器（详情请参阅 [Google Search Console 文档]）。

## 输出格式
- 报告格式可以是探索报告、自定义渠道组报告或自定义报告；
- 正则表达式会根据用户实际追踪的来源进行相应调整。

## 相关技能
- **生成式引擎优化**：了解如何利用生成式技术提升网站效果；
- **流量分析**：分析流量来源、归因方式及 UTM 参数；
- **数据分析**：掌握如何使用 GA4 追踪用户行为和转化数据；
- **Google Search Console**：学习如何利用 GSC 分析人工智能流量；
- **robots.txt**：配置文件用于控制搜索引擎爬虫的访问权限。