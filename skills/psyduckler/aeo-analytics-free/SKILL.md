---
name: aeo-analytics-free
description: >
  **跟踪AI可见性**：该功能用于检测品牌是否被AI助手（如Gemini、ChatGPT、Perplexity）在特定提示中提及或引用。系统会定期进行扫描，记录品牌被提及或引用的频率，分析趋势，并识别潜在的商业机会。主要使用Gemini API的免费 tier（包含“grounding”功能）来进行数据采集；若免费 tier无法满足需求，则会采用网络搜索作为备用方法。适用于以下场景：  
  - 检查AI模型是否提及用户品牌；  
  - 跟踪品牌在AI中的引用情况随时间的变化；  
  - 评估品牌相关内容的效果；  
  - 监测竞争对手在AI生成内容中的曝光度；  
  - 审查品牌在AI生成答案中的呈现情况。  
  该功能与以下工具配合使用：  
  - `aeo-prompt-research-free`（用于识别相关提示）；  
  - `aeo-content-free`（用于创建或更新品牌相关内容）。  
  通过这些工具的协同工作，该功能能够全面评估品牌在AI领域的可见性，并为品牌策略提供数据支持。
---
# AEO Analytics（免费版）

> **来源：** [github.com/psyduckler/aeo-skills](https://github.com/psyduckler/aeo-skills/tree/main/aeo-analytics-free)  
> **所属项目：** [AEO Skills Suite](https://github.com/psyduckler/aeo-skills)  
  - [Prompt Research](https://github.com/psyduckler/aeo-skills/tree/main/aeo-prompt-research-free) → [Content](https://github.com/psyduckler/aeo-skills/tree/main/aeo-content-free) → [Analytics](https://github.com/psyduckler/aeo-skills/tree/main/aeo-analytics-free)

该工具用于追踪人工智能助手是否提及并引用您的品牌，以及这些情况随时间的变化情况。

## 使用要求

- **主要依赖：** Gemini API密钥（可从 aistudio.google.com 免费获取），用于将 AI 的回答与原始数据进行关联分析。  
- **备用方案：** 仅使用 `web_search` 功能——虽然数据准确性较低，但无需 API 密钥。  
- `web_fetch` 功能为可选选项，可用于更深入地分析被引用的网页。

## 输入参数

- **域名**（必填）：您品牌的官方网站（例如：`tabiji.ai`）  
- **品牌名称**（必填）：需要在搜索结果中查找的品牌名称（例如：`["tabiji", "tabiji.ai"]`）  
- **提示语**（首次扫描时需要提供）：要追踪的目标提示语列表，这些提示语可来自 `aeo-prompt-research-free` 的输出结果。  
- **数据文件路径**（可选）：用于存储扫描记录的文件路径。默认路径为 `aeo-analytics/<domain>.json`。

## 命令说明

该工具支持以下三个命令：

### `scan` — 执行新的可见性扫描  
针对所有指定的提示语，向 AI 模型发起查询并记录结果。

### `report` — 生成可见性报告  
分析累计的扫描数据，并生成格式化的报告。

### `add-prompts` / `remove-prompts` — 管理需要追踪的提示语  
向追踪列表中添加或删除提示语。

---

## 扫描流程

### 第一步：加载或初始化数据  
检查该域名对应的数据文件是否存在。如果存在，则加载该文件；如果不存在，则创建一个新的数据文件。  
详细的数据格式规范请参见 `references/data-schema.md`。

### 第二步：执行查询  
对于每个需要追踪的提示语：

**方法一：使用 Gemini API 进行关联分析（推荐方式）：**  
具体 API 详情请参阅 `references/gemini-grounding.md`：  
1. 使用 `googleSearch` 工具将提示语发送到 Gemini API。  
2. 从响应中提取以下信息：  
   - **回答内容**：AI 的回答结果  
   - **引用来源**：被引用的网页链接及标题  
   - **搜索关键词**：AI 所使用的搜索词  

3. 分析结果：  
   - **是否提及品牌？** 在回答文本中搜索品牌名称（不区分大小写，以单词边界进行匹配）  
   - **提及的句子**：提取包含品牌名称的句子  
   - **是否被引用？** 检查品牌域名是否出现在引用来源的 URL 中  
   - **被引用的网址**：列出所有被引用的品牌相关网址  
   **情感倾向**：判断提及内容的情绪倾向（正面/中性/负面）  
   **竞争对手**：从回答和引用内容中提取其他品牌名称及域名  

**方法二：使用 Web 搜索（无 Gemini API 密钥时使用）：**  
1. 使用 `web_search` 功能搜索指定的提示语内容。  
2. 检查搜索结果中是否包含品牌域名。  
3. 将此结果记录为“Web 代理”方式获取的数据（准确性较低）。

### 第三步：保存结果  
将扫描结果追加到数据文件中。切勿覆盖之前的扫描记录——历史数据非常重要。

### 第四步：生成简要总结  
扫描完成后，输出以下信息：  
- 扫描的提示语列表  
- 当前的提及率和引用率  
- 与上次扫描相比的变化情况（如有）  
- 任何显著的变化（新增的提及或丢失的引用）

---

## 报告生成流程

### 单个提示语的详细信息  
对于每个被追踪的提示语，显示以下内容：  
```
1. "[prompt text]"
   Scans: [total] (since [first scan date])
   Mentioned: [count]/[total] ([%]) — [trend arrow] [trend description]
   Cited: [count]/[total] ([%])
   Latest: [✅/❌ Mentioned] + [✅/❌ Cited]
   Sentiment: [positive/neutral/negative]
   Competitors mentioned: [list]
```  

如果该提示语在最近一次扫描中被提及，会显示具体的提及内容；如果没有被提及，则会列出被引用的来源，并评估其被引用的可能性（高/中/低）。

### 总结部分  
```
VISIBILITY SCORE
  Brand mentioned: [X]/[total] prompts ([%]) in latest scan
  Brand cited: [X]/[total] prompts ([%]) in latest scan

TRENDS (last [N] days, [N] scans)
  Mention rate: [%] → [trend]
  Citation rate: [%] → [trend]
  Most improved: [prompt] ([old rate] → [new rate])
  Most volatile: [prompt] (mentioned [X]/[N] scans)
  Consistently absent: [list of prompts never mentioned]

COMPETITOR SHARE OF VOICE
  [Competitor 1] — mentioned in [X]/[total] prompts
  [Competitor 2] — mentioned in [X]/[total] prompts
  [Brand] — mentioned in [X]/[total] prompts

NEXT ACTIONS
  → [Prioritized recommendations based on gaps and trends]
```  

### 建议策略：  
- **高机会**：提示语未被提及，且引用中未出现该品牌的相关内容——建议创建新内容。  
- **接近成功**：提示语被提及但未被引用——建议更新内容以提高其被引用的可能性。  
- **变化较大**：提及率在 20%–60% 之间——说明现有内容需要加强。  
- **成功**：提及率超过 80%，引用率超过 50%——建议保持现有内容并持续监测其影响力变化。

---

## 数据管理  
- 数据文件保存路径：`aeo-analytics/<domain>.json`  
- 数据结构规范：参见 `references/data-schema.md`  
- 每次扫描的结果都会被追加到 `scans` 数组中，历史数据不会被删除。  
- 添加或删除提示语不会影响之前的扫描记录。  
- 新添加的提示语初始扫描次数为 0（不会补充历史数据）。

## 使用提示：  
- 建议定期（每周或每两周）执行扫描，以获取有意义的数据趋势。  
- 在发布新的 AEO 内容后，建议等待 2–4 周再查看数据变化。  
- Gemini 的关联分析结果可能会因每次运行而有所不同，这是正常现象；多次扫描后的数据汇总比单次结果更可靠。  
- 最好同时追踪 10–20 个提示语，以便更准确地观察趋势；数量过多可能会导致数据波动。  
- 该工具构成了完整的 AEO 工作流程：研究（aeo-prompt-research-free）→ 创作/更新内容（aeo-content-free）→ 数据分析（本工具）→ 重复上述流程。