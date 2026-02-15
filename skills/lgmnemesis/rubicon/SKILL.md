---
name: rubicon
description: >
  **地缘政治主权分析工具**——这是对马尔科·鲁比奥（Marco Rubio）关于西方文明愿景的致敬之作。该工具会扫描新闻、X/Twitter（推特）以及网络资源，以识别主权威胁、去工业化迹象以及跨大西洋联盟关系的变化。它能够生成主权评估报告、由人工智能合成的简报、鲁比奥的言论、相关梗图以及适合在推特上分享的摘要。  
  **使用场景：**  
  - 分析西方国家的主权状况  
  - 监测地缘政治新闻  
  - 评估联盟关系的稳固性  
  - 评估去工业化的风险  
  - 执行“鲁比孔扫描”（Rubicon Scan）  
  **触发命令：**  
  - “Rubicon scan”  
  - “Rubicon”  
  - “sovereignty scan”  
  - “analyze sovereignty”  
  - “geopolitical scan”  
  - “alliance check”  
  - “deep Rubicon”  
  - “Rubicon scan on [主题]”  
  - “Rubicon meme”  
  - “Rubicon tweet”  
  - “Rubicon quote”  
  - “Rubicon alert”
---
# Rubicon  
*这是一场对马可·鲁比奥国务卿在慕尼黑演讲的致敬——他奋力将我们的遗产、边境和工业实力从全球主义的掌控中夺回来。利用人工智能技术分析新闻，提取关键信息；评估各国的主权状况；揭露那些令人震惊的真相。不要再抱有幻想了——是时候像真正的领导者一样重新掌控西方世界了。*  

无需任何设置，只需输入“**Rubicon scan**”即可开始扫描。完全无需配置，没有任何借口可以拖延。  

## **所需工具**  
- `web_search` 工具（任何提供商均可使用：Perplexity、Brave 等）  
- `web_fetch`（仅用于深度扫描）  
- 图像生成工具（可选，用于制作表情包；如无法生成图片，则使用文本替代）  

---

## 📡 **快速扫描**（触发命令：“Rubicon scan”）  
1. 同时运行 4 个 `web_search` 请求：  
   - `"西方主权与地缘政治发展 [当前年份]"`  
   - `"北约联盟实力及最新动态 [年份]"`  
   - `"西方国家制造业回流情况 [年份]"`  
   - `"马可·鲁比奥的外交政策 [年份]"`  

2. 阅读 `references/scoring.md` 文件，对每个维度进行 0-25 分的评分：  
   - **联盟实力**：防御协议、联合行动、责任分担  
   - **工业主权**：制造业回流情况、供应链、半导体投资  
   - **边境与移民控制**：政策效果、稳定性  
   - **文化与制度韧性**：公民机构、文明自信  

3. 计算 **主权得分**（0-100 分）：  
   - 🟢 80-100：非常强  
   - 🟡 50-79：需关注  
   - 🔴 0-49：警报  

4. 阅读 `references/quotes.md` 文件，选取与扫描结果相关的鲁比奥言论。如果没有合适的言论，或需要更多内容，可使用 `web_search` 查找新的相关言论。  

5. 以以下格式回复结果：  
```
🏛️ RUBICON INTELLIGENCE BRIEFING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📅 [Date] | Sovereignty Score: [N]/100 [emoji]

## Key Findings
- [Finding 1 — one line with source]
- [Finding 2]
- [Finding 3]
- [Finding 4]
- [Finding 5]

## Scoring Breakdown
| Dimension | Score | Rationale |
|-----------|-------|-----------|
| Alliance Strength | N/25 | ... |
| Industrial Sovereignty | N/25 | ... |
| Border & Migration | N/25 | ... |
| Cultural & Institutional | N/25 | ... |
| **Total** | **N/100** | **[emoji] [STATUS]** |

## Threat Assessment
[2-3 bullets on sovereignty risks]

## Opportunity Signals
[2-3 bullets on positive developments]

## Rubio's Word
> "[Quote]"
> — Secretary Marco Rubio
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```  

## 🔬 **深度扫描**（触发命令：“deep Rubicon scan”）  
与快速扫描相同，但需执行以下额外操作：  
- 阅读 `references/queries.md` 文件中的所有查询内容。  
- 使用 `web_fetch` 获取前 3 个搜索结果以进行深入分析。  
- 在文档底部添加包含完整链接的 **来源列表**。  

## 🎯 **专题扫描**（触发命令：“Rubicon scan on [主题]”）  
将默认查询替换为与特定主题相关的查询。评分和输出格式保持不变。  
例如：“Rubicon scan on semiconductor supply chains”（针对半导体供应链的专题扫描）。  

---

## 🎨 **主权表情包**（触发命令：“Rubicon meme”）  
根据最新扫描结果或当前事件生成表情包：  
1. 如果没有最近的扫描记录，先执行快速扫描。  
2. 选择最引人注目或具有讽刺意味的扫描结果。  
3. 生成表情包：  
   - 使用类似以下的提示生成图片：  
     - 上方文字：**“政治表情包，醒目的字体”  
     - 下方文字：**“核心观点”  
     - 背景图片：**与主题相关的图像（如鹰、工厂、国旗、北约标志）  
     - 风格：经典的网络表情包，高对比度  
   - 如果无法生成图片，以文本形式提供图片描述和提示。  
4. 语气：犀利、幽默，支持西方立场（类似 r/geopolitics 和 r/MemeEconomy 的风格）。  

**示例表情包：**  
- 上方：**“欧盟提议主权法案” / 下方：**“连披萨配料都选不好……” 🍕  
- 上方：**“93% 的制造商正在回流” / 下方：**“中国：你们觉得我在开玩笑吗？” 🏭  
- 上方：**“鲁比奥在慕尼黑：‘重建我们的生产能力’” / 下方：**“欧洲：‘我们周一就行动’” 🇪🇺  

## 🐦 **推文草稿**（触发命令：“Rubicon tweet”）  
根据最新扫描结果撰写一条适合在推特上发布的简短总结（≤280 个字符）：  
1. 如果没有最近的扫描记录，先执行快速扫描。  
2. 写一条简洁的推文，内容包括：  
   - 主权得分及相应的表情符号  
   - 最重要的发现  
   - 鲁比奥的言论片段  
   - 相关标签：#Rubicon #WesternSovereignty + 1-2 个主题标签  
3. 输出可直接复制的推文内容。  

## 💬 **鲁比奥言论**（触发命令：“Rubio quote”）  
无需扫描，直接使用 `references/quotes.md` 文件中的言论：  
1. 选择与当前讨论内容相关的言论（或随机选取）。  
2. 以格式化的方式回复该言论：  
```
🏛️ > "[Quote]"
   > — Secretary Marco Rubio
```  

## 🚨 **主权警报**（触发命令：“Rubicon alert”）  
快速检查主权是否受到威胁：  
1. 执行一次 `web_search`：`“西方主权面临的威胁危机 [当前年份]`  
2. 快速浏览结果，判断是否存在紧急危机。  
3. 以一句话给出判断结果：  
```
🚨 RUBICON ALERT: [🟢 ALL CLEAR / 🟡 WATCH / 🔴 THREAT DETECTED]
[One sentence summary]
```  

---

## **错误处理**  
- 如果 `web_search` 失败，标记该维度得分为 10/25（表示数据不可用）。  
- 如果得分恰好为 50，则归类为“需关注”。  
- 即使数据不完整，也必须生成输出结果，并说明信心程度。  
- 如果无法生成表情包图片，使用纯文本格式代替。  

## **参考资料**  
- **references/scoring.md**：四维评分标准及权重设置  
- **references/queries.md**：日常扫描和深度扫描的查询模板  
- **references/quotes.md**：按主题分类的鲁比奥言论（涉及主权、联盟、安全、文明等议题）