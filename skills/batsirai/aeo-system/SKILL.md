---
name: aeo-system
description: "**答案引擎优化（Answer Engine Optimization）**：帮助您的AI助手推荐您的品牌。执行AEO（Answer Engine Optimization）审计，构建答案意图图（Answer Intent Maps），跟踪AI推荐的效果，并为任何品牌或产品类别维护一个7层结构的AEO基础设施。"
requiredEnv:
  - PERPLEXITY_API_KEY  # Required for Answer Intent Map automation
  - OPENAI_API_KEY      # Optional — enables ChatGPT query automation
  - BRAVE_API_KEY       # Recommended — enables web-based infrastructure checks
permissions:
  - network: Queries Perplexity API, OpenAI API, and target brand websites
  - filesystem: Writes audit reports and intent map data to working directory
source:
  url: https://github.com/Batsirai/carson-skills
  author: Carson Jarvis (@CarsonJarvisAI)
  github: https://github.com/Batsirai/carson-skills
  verified: true
security:
  note: API keys are loaded from environment variables. No credentials are embedded in the skill or scripts.
---
# AEO（Answer Engine Optimization）系统

> 当用户提出购买相关问题时，可以利用AI助手（如ChatGPT、Perplexity、Claude、Gemini）来推荐您的品牌。

---

## AEO简介

AEO是一种专门针对AI驱动的答案引擎进行优化的方法，其原理类似于SEO针对搜索引擎的优化方式。例如，当用户向Perplexity询问“哪种镁补充剂对睡眠效果最好？”时，AEO系统会判断您的品牌是否会被推荐出来。

该技能使OpenClaw代理具备以下功能：

1. **审计**品牌在所有7个层面的AEO基础设施状况。
2. **映射**不同类别下AI平台推荐的品牌及其排名位置。
3. **跟踪**各品牌排名每周的变化情况。
4. **构建**缺失的基础设施（如Answer Hub、brand-facts.json、数据结构等）。
5. **通过每周90分钟的维护流程来持续维护该系统。

---

## 适用场景

- 用户请求对某个品牌或URL进行AEO审计。
- 用户询问“在[特定类别]中有哪些品牌被AI推荐？”
- 用户请求为某个类别生成Answer Intent Map。
- 用户需要查看品牌的Answer Hub、brand-facts.json或数据结构信息。
- 用户希望跟踪AI推荐结果的长期变化。
- 用户希望执行每周的AEO维护操作。

---

## AEO的7层框架

| 层次 | 名称 | 功能 | 优先级 |
|-------|------|-----------|---------|
| 1 | Answer Intent Map | 包含所有购买意图相关查询及其对应的AI推荐品牌的电子表格 | 基础层 |
| 2 | Answer Hub | 为该类别提供详细解答的页面 | 高优先级 |
| 3 | Brand-Facts Page | 以人类可读的形式展示品牌信息（中立、基于事实、可引用） | 高优先级 |
| 4 | brand-facts.json | 机器可读的品牌数据文件（位于`/.well-known/brand-facts.json`） | 中等优先级 |
| 5 | Schema Markup | 产品、常见问题解答及组织结构的数据 | 中等优先级 |
| 6 | Citation Network | 确保品牌信息被AI模型引用 | 高优先级 |
| 7 | GPT Shopping | 通过Google Merchant Center整合购物推荐信息 | 高优先级 |

---

## 先决条件

**必备条件：**
- `PERPLEXITY_API_KEY`：用于直接发起API请求（可在perplexity.ai/settings/api免费获取）
- Node.js v18及以上版本（用于`answer-intent-map.js`脚本）

**可选条件：**
- `OPENAI_API_KEY`：用于自动化ChatGPT查询
- `BRAVE_API_KEY`：用于检查相关基础设施

**无API密钥时：**该技能将以“手动辅助”模式运行，用户需要自行生成查询并分析结果。

---

## 核心工作流程

### 工作流程1：全面AEO审计

**触发条件：**“对[品牌URL]进行AEO审计”

**步骤：**
1. 检查品牌的网站，分析其AEO基础设施：
   - 是否有Answer Hub页面（如`/guides/`）
   - 是否有Brand-Facts页面
   - 是否有机器可读的数据文件（`/.well-known/brand-facts.json`）
   - 检查产品页面上的数据结构标记（使用Rich Results API或web_fetch）
   - 是否有Wikidata条目
   - 检查品牌是否符合Google Merchant Center的收录标准

2. 为每个层面打分（0–3分）：
   - **0**：不存在
   - **1**：存在但不完整或过时
   - **2**：存在、可用但存在小问题
   - **3**：完整、最新、已优化

3. 生成审计报告，内容包括：
   - 各层面的当前得分
   - 实施的优先级顺序
   - 每个缺失层面的具体改进措施

**输出：**Markdown格式的报告文件，文件名为`aeo-audit-[品牌]-[日期].md`

---

### 工作流程2：生成Answer Intent Map

**触发条件：**“为[类别]生成Answer Intent Map”或运行`scripts/answer-intent-map.js`

**步骤：**
1. 生成四种类型的查询列表：
   - **类别查询**：“[产品类型]的最佳选择”
   - **对比查询**：“[品牌]与[竞争对手]”
   - **品牌查询**：“[品牌]是否值得购买”
   - **信息查询**：“[成分]对[健康问题]有帮助吗”

2. 对每个查询，在可用平台中发起查询：
   - Perplexity API（返回结构化JSON及引用信息）
   - OpenAI API（返回文本结果，需通过解析提取品牌名称）
   - 对于Claude和Gemini，使用浏览器进行查询

3. 从响应中提取以下信息：
   - 被提及的品牌名称及其排名
   - 引用的来源URL
   - 关键的原文引用

4. 将结果保存为JSON文件，并生成Markdown格式的总结报告

**运行脚本：**
```bash
node scripts/answer-intent-map.js \
  --category "magnesium supplements" \
  --brand "MyBrand" \
  --queries 20

# Or with a config file:
node scripts/answer-intent-map.js --config ./aeo-config.json
```

---

### 工作流程3：每周维护

**触发条件：**“执行每周AEO维护”或通过定时任务触发

**步骤：**
1. 加载品牌的Answer Intent Map（优先级最高的15个查询）
2. 使用ChatGPT和Perplexity重新查询这些查询
3. 与上周的记录进行对比，检测排名变化
4. 生成维护报告：
   - 排名变化
   - 本周新增的引用来源
   - 推荐的Answer Hub更新内容
5. 检查`brand-facts.json`中的`lastUpdated`时间戳是否过期
6. （如有需要）通过浏览器检查Google Merchant Center的审核状态

**输出：**Markdown格式的报告文件，文件名为`aeo-weekly-report-[日期].md`

**使用检查清单：**`templates/weekly-maintenance-checklist.md`

---

### 工作流程4：引用网络分析

**触发条件：**“分析[类别]的引用情况”

**步骤：**
1. 通过Perplexity API生成20个类别查询
2. 从响应中提取所有独特的来源URL
3. 按域名分类并统计数量
4. 确定在该类别中被引用最多的10个外部来源
5. 生成优先级列表，用于后续的推广工作

**输出：**按引用频率排序的引用分析报告

---

### 工作流程5：构建基础设施

**触发条件：**“为[品牌]构建AEO基础设施”或“设置brand-facts.json”

**步骤：**
1. 获取品牌详细信息（或从`aeo-config.json`中加载）
2. 使用模板生成以下文件：
   - `brand-facts.json`
   - Answer Hub页面（`templates/answer-hub-template.md`）
   - 产品页面的数据结构标记（JSON-LD格式）

3. 提供每个文件的实现指南。

---

## 配置说明

请在工作目录中创建`aeo-config.json`文件：

```json
{
  "brandName": "Your Brand Name",
  "brandUrl": "https://yourbrand.com",
  "category": "Magnesium Supplements",
  "priorityQueries": [
    "best magnesium supplement for sleep",
    "best magnesium glycinate supplement",
    "magnesium supplement for anxiety"
  ],
  "competitors": [
    "Competitor Brand A",
    "Competitor Brand B",
    "Competitor Brand C"
  ],
  "answerHubUrl": "https://yourbrand.com/guides/best-magnesium-supplements-2026",
  "brandFactsJsonUrl": "https://yourbrand.com/.well-known/brand-facts.json"
}
```

---

## 输出文件

| 文件名 | 说明 |
|------|-------------|
| `aeo-audit-[品牌]-[日期].md` | 基础设施审计报告 |
| `answer-intent-map-[类别]-[日期].json` | AI查询结果 |
| `answer-intent-map-[类别]-[日期].md` | 人类可读的竞争分析报告 |
| `aeo-weekly-report-[日期].md` | 周报 |
| `citation-analysis-[类别]-[日期].md` | 引用网络分析报告 |

---

## 使用示例

---


## 平台限制

| 平台 | 访问方式 | 备注 |
|----------|--------|-------|
| Perplexity | 通过API访问（结构化数据，可靠性高） | 直接返回引用信息 |
| ChatGPT | 通过OpenAI API访问 | 需要解析文本以提取品牌名称 |
| Claude | 需要浏览器支持 | 生成查询并提供空白日志；代理通过浏览器执行查询 |
| Gemini | 需要浏览器支持 | 生成查询并提供空白日志；代理通过浏览器执行查询 |

**注意：**对于Claude和Gemini，该技能会生成查询列表和空白日志模板；用户需使用浏览器收集查询结果。

**请求限制：**Perplexity免费账户的请求限制约为每分钟20次。如需超过50次查询，请在脚本中添加`--delay 3000`参数。

---

## 文件结构

---


*AEO系统 v1.0 — 2026年2月*
*由Carson Jarvis (@CarsonJarvisAI)开发*