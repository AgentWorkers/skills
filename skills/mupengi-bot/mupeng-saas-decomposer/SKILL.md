---
name: saas-decomposer
description: "**Web SaaS服务分解与AI本地化开发计划生成**  
分析现有的SaaS服务，识别可由AI代理替代的功能，并制定基于技能的本地化实施路线图。该流程由以下关键步骤触发：**SaaS分析**、**服务分解**、**本地化处理**、**SaaS功能替换**以及**利用AI构建新服务**等。"
author: 무펭이 🐧
---
# saas-decomposer

> **SaaS → AIaaS 转换分析引擎**  
> 该工具用于分解现有的 SaaS 服务，并识别可通过 AI 技能替代的部分，从而制定国际化发展路线图。

## 核心概念：SaaS → AIaaS 转换分析  

Mupengism 的核心愿景是：“SaaS 时代的终结，AIaaS 时代的到来”。  
- 整个价值 2000 亿美元的 SaaS 市场正在发生变革：  
  - 从销售软件的时代，迈向 **部署 AI 功能的时代**。  
  - 该工具能够分析现有 SaaS 功能中哪些部分可以被 AI 技能替代。  

---

## 主要功能  

### 1. SaaS 服务分解  
**输入**：SaaS 服务的 URL 或名称  
**流程**：  
1. 使用 `web_fetch` 工具爬取服务的首页或功能页面。  
2. 提取核心功能列表。  
3. 将每个功能分解为独立的任务。  
4. 为这些功能分配 AI 替代的可能性评分（1-5 分）。  
5. 显示这些功能当前是否已被 Mupeng 的现有技能覆盖。  

**输出格式**：  
```
## [Service Name] Decomposition Results

### Function List
- Function A (AI replacement: ⭐⭐⭐⭐⭐) → Existing skill: copywriting
- Function B (AI replacement: ⭐⭐⭐) → New skill needed
- Function C (AI replacement: ⭐) → Infrastructure development needed

### AI Replacement Rate: 70%
### New Skills Needed: 3
### Estimated Development Time: 2 weeks
```  

---

### 2. 国际化规划  
根据分解结果生成开发路线图：  
- 根据技能的替代效果优先级进行开发计划安排。  
- 利用现有的技能进行功能复用。  
- 自动生成新的技能规范草案。  
- **成本对比**：分析使用 SaaS 订阅服务与自行开发技能的成本差异。  

**示例**：  
```
### Internalization Roadmap

#### Phase 1: Quick Wins (1 week)
- [Use existing skill] Automate email templates with copywriting
- [Use existing skill] Automate customer responses with auto-reply

#### Phase 2: New Skill Development (2 weeks)
- lead-scorer: Lead scoring algorithm
- campaign-optimizer: A/B test automation

#### Phase 3: Infrastructure (4 weeks)
- Build data pipeline
- Real-time sync system

### Cost Comparison
- HubSpot Pro: $800/mo → Mupeng skillpack: $120/mo (85% savings)
```  

---

### 3. 竞品 SaaS 对比分析  
能够同时分析同一类别中的 3-5 个 SaaS 服务：  
- 提供功能对比表。  
- 分析 AI 技能的替代范围。  
- 计算“我们的技能包能够替代这些 SaaS 服务的百分比”。  

**示例**：  
```
### Marketing SaaS Comparison

| Function | HubSpot | Mailchimp | ActiveCampaign | Mupeng Replacement |
|----------|---------|-----------|----------------|-------------------|
| Email automation | ✅ | ✅ | ✅ | ⭐⭐⭐⭐⭐ auto-reply |
| Lead scoring | ✅ | ❌ | ✅ | ⭐⭐⭐ (new skill) |
| A/B testing | ✅ | ✅ | ✅ | ⭐⭐⭐⭐ copywriting |
| CRM integration | ✅ | ⚠️ | ✅ | ⭐⭐ (infrastructure needed) |

**Overall Replacement Rate**: 65%
```  

---

### 4. 行业特定的 SaaS → AIaaS 转换模板  
提供针对不同行业的预定义分解模板：  

#### 营销领域  
- **SaaS**：HubSpot, Mailchimp  
- **Mupeng 替代方案**：`自动回复` + `文案撰写` + `邮件发送` + `SEO 内容规划`  

#### 项目管理  
- **SaaS**：Notion, Jira  
- **Mupeng 替代方案**：`决策记录` + `每日报告` + `Git 自动化管理`  

#### 客户管理  
- **SaaS**：Salesforce, Zendesk  
- **Mupeng 替代方案**：`自动回复` + `通知中心` + `数据抓取工具`  

#### 会计  
- **SaaS**：QuickBooks  
- **Mupeng 替代方案**：`发票生成` + `费用跟踪工具`  

#### 内容创作  
- **SaaS**：Canva, Buffer  
- **Mupeng 替代方案**：`卡片新闻生成` + `社交媒体发布工具` + `内容复用系统`  

#### 学生事务管理（AssoAI 模型）  
- **SaaS**：EveryTime, Notion, CampusGroups  
- **Mupeng 替代方案**：参考文档：`memory/2026-02-09-insight-university-saas.md`  

---

## 分析框架  
```
1. Crawl      — Collect service functions (web_fetch + data-scraper)
2. Decompose  — Break into atomic tasks
3. Score      — AI replaceability score (1-5)
4. Map        — Map to existing Mupeng skills
5. Gap        — Identify missing skills
6. Plan       — Generate development roadmap
7. Compare    — Cost comparison (SaaS vs AIaaS)
```  

---

## 使用示例  

### 基本功能分解  
```
User: "Decompose HubSpot"
→ Execute Crawl + Decompose + Score + Map
→ Output decomposition results report
```  

### 国际化规划生成  
```
User: "What do I need to replace Notion with AI?"
→ Execute Decompose + Internalize
→ Output roadmap + cost comparison
```  

### 竞品分析  
```
User: "Compare marketing SaaS"
→ Simultaneously analyze HubSpot, Mailchimp, ActiveCampaign
→ Cross-comparison table + replacement rate calculation
```  

---

## 事件通知  
分析完成后，会生成以下事件：  
`events/saas-analysis-YYYY-MM-DD.json`  

### 用户用途  
`business-planner`：在商业计划中利用分析结果。  

---

## 参考文件  
分析过程中可参考的文档：  
- `memory/2026-02-09-insight-university-saas.md` — 大学 SaaS 市场分析（CampusGroups, EveryTime）  
- `memory/2026-02-09-assoai-pitchdeck.md` — AssoAI（学生事务管理 SaaS 的 AI 自动化方案）  
- `memory/consolidated/doyak-business-plan.md` — “将 SaaS 许可证减少 50%，转而使用 AI”（Publicis Sapient）  
- `memory/research/absorb-frameworks.md` — 框架分析（MetaGPT, OpenHands 等）  
- `SOUL.md` — Mupengism 的愿景：“整个 2000 亿美元的 SaaS 市场正在发生变革”  

---

## AI 替代可能性评分标准  
| 评分 | 含义 | 示例 |  
|-------|---------|----------|  
| ⭐⭐⭐⭐⭐ | 可立即通过现有技能替代 | 自动邮件回复、内容生成功能 |  
| ⭐⭐⭐⭐ | 需要少量技能开发（1-2 周） | 客户评分系统、A/B 测试 |  
| ⭐⭐⭐ | 需要中等程度的开发（2-4 周） | 工作流引擎、仪表盘 |  
| ⭐⭐ | 需要基础设施建设（1-2 个月） | 实时同步功能、数据管道 |  
| ⭐ | 需要长期研发（3 个月以上） | 高级机器学习模型、复杂集成方案 |  

---

## 故障排除  
### 如果 `web_fetch` 失败  
- 使用浏览器工具获取当前页面的快照进行分析。  
- 优先爬取帮助中心、价格页面等公开文档。  

### 如果竞争对手信息不足  
- 首先参考行业通用模板。  
- 利用同类 SaaS 服务的拆解模式进行补充。  

### 如果成本对比数据缺失  
- 爬取相关 SaaS 服务的价格页面。  
- 根据行业平均水平估算订阅费用。  

---

🐧 由 **무펭이** 开发 — [Mupengism](https://github.com/mupeng) 生态系统的一部分