---
name: scholarsearch
description: 使用 Tavily API、PubMed 和 Google Scholar 进行学术文献搜索并生成简报。适用于需要查找特定主题的最新学术论文、根据相关性排名生成前十篇文献的简报、以每日格式将报告保存到 Obsidian 文档库中，或通过 Feishu 发送摘要的场景。支持使用逗号或空格分隔的多个关键词进行搜索。
---
# 学术文献搜索 🔬📚  
该技能利用 Tavily API 自动搜索 PubMed、Google Scholar 等学术数据库，生成相关性排序的 Top 10 文章列表，并将其同步到您的 Obsidian 文档库和 Feishu 平台。  

## 快速入门  
```bash
# Search papers on specific topic
scholarsearch 关键词：房颤，导管消融，脉冲电场消融
```  

或者使用逗号或空格分隔的多个关键词：  
```bash
scholarsearch 房颤，afib, 心房颤动，catheter ablation，消融，pulsed field ablation
```  

## 功能概述  
1. **多源搜索**：通过 Tavily API 查询 PubMed、Google Scholar 及其他学术资源。  
2. **相关性排序**：根据以下标准评估论文：  
   - 发表时间（优先考虑 2025-2026 年的论文）  
   - 临床意义（人类试验、随机对照试验 RCT）  
   - 作者/机构的可信度  
   - 期刊/出版商的声誉  
   - 与主题的直接相关性  
3. **精选 Top 10 文章**：选择得分在 0.0-1.0 之间的最相关论文  
4. **生成报告**：创建包含链接、摘要和关键发现的格式化报告  
5. **双端同步**：将结果保存到 Obsidian，并通过 Feishu 平台发送完整内容  

## 使用场景  
- ✅ 早晨学术简报（可配置时间，默认为早上 5:00）  
- ✅ 针对特定医学/技术主题的文献综述  
- ✅ 跟踪某一领域的最新研究动态  
- ✅ 获取带有背景信息的精选“Top 10”列表  

## 参数设置  
支持使用逗号或空格分隔的关键词：  
```
scholarsearch 房颤，心房颤动，pulased field ablation，catheter ablation
scholarsearch AFib, atrial fibrillation, ablation, electrogram
scholarsearch 机器学习，深度学习，神经网络，大模型
```  

## 输出格式  
```markdown
# 每日学术更新 - [Topic] 研究简报

**日期:** YYYY-MM-DD  
**更新时间:** HH:MM Asia/Shanghai  
**关键词:** [your keywords]

---

## 📊 Top 10 精选文献

按相关性评分排序 (0.0-1.0):

### 1️⃣ [Paper Title]
**评分:** 0.XX  
**链接:** https://...  
**摘要:** [Brief summary with key findings]

... (10 papers)

---

## 📝 本期要点总结

### 🔥 核心发现

[Bullet points of major breakthroughs/trends]

### 🎯 临床/研究关注重点

[What to watch for]

---

## 🔄 配置说明

**检索频率:** [Set to user preference]  
**来源:** Tavily API (PubMed, Google Scholar, etc.)  
**保存路径:** Obsidian 每日学术更新/YYYY-MM-DD.md  
**排序方式:** 相关性评分 + 发表时间

---

*自动生成 | ☕🐕 CoffeeDog | [Topic] | YYYY-MM-DD*
```  

## 错误处理  
- **无结果**：调整关键词或扩大搜索范围  
- **链接质量低**：跳过非学术来源，优先选择经过同行评审的论文  
- **API 限制**：设置重试机制并限制请求频率  

## 集成方式  
- **Tavily API**：支持 PubMed 和 Google Scholar 的学术文献搜索  
- **Feishu**：每日自动推送完整报告内容  
- **Obsidian**：自动将结果保存为 `Obsidian/每日学术更新/YYYY-MM-DD.md` 文件  

## 注意事项  
- **自动调度**：可使用 cron 或 heartbeat 任务在每天早上 5:00 运行该脚本  
- 使用英文关键词可提高 PubMed 的搜索效果  
- 结合使用中文和英文关键词以实现全面覆盖  
- 根据需求设置特定主题参数（例如：“房颤 2026，PFA 临床试验”）  

---

*学术发现自动化，CoffeeDog 为您整理好相关论文。☕🐕*