---
name: last30days
description: 研究过去30天内Reddit、X/Twitter以及网络上关于任何主题的讨论内容。将研究结果整理成可操作的见解或可供复制的提示。
metadata: {"clawdbot":{"emoji":"📅","requires":{"bins":["bird"]}}}
---

# last30days 📅  
利用过去30天内Reddit、X/Twitter以及网络上的讨论来研究任何主题。该功能会汇总相关见解并提供可操作的提示。  

## 概述  
AI领域每月都在发生变化。通过这个技能，你可以及时了解人们当前的讨论和实际使用情况——而非六个月前的信息。  

**功能说明：**  
- 使用新鲜度过滤器（过去30天内）搜索网页、Reddit和X/Twitter；  
- 获取真实用户的实践经验，而不仅仅是SEO相关的内容；  
- 将搜索结果整合成可操作的见解；  
- 生成基于当前最佳实践的提示（可直接复制使用）。  

**适用场景：**  
- 技术研究（哪些方法对ChatGPT、Midjourney、Claude等有效）；  
- 趋势发现（哪些内容正在流行，人们推荐什么）；  
- 产品反馈（真实用户对某产品的评价）；  
- 需要关注最新动态的快速变化领域。  

**所需工具：**  
- Brave Search（内置在Clawdbot中）；  
- `bird` CLI工具（用于X/Twitter，可选但推荐）；  
- 无需额外的API密钥。  

## 使用方法  
当用户请求某个主题的最新信息时，可以执行以下操作：  

### 第1步：网页搜索（使用Brave浏览器并设置新鲜度过滤器）  
```
web_search(query="[topic]", freshness="pm", count=5)
```  
- `pm`：过去一个月的数据；  
- 其他选项：`pd`（24小时内数据），`pw`（一周内的数据）。  

### 第2步：Reddit搜索  
```
web_search(query="site:reddit.com [topic]", freshness="pm", count=5)
```  
重点关注r/ClaudeAI、r/ChatGPT、r/LocalLLaMA、r/MachineLearning、r/StableDiffusion等板块。  

### 第3步：X/Twitter搜索  
```bash
bird search "[topic]" -n 10 --plain
```  
寻找分享真实使用经验的用户，而非只是为了吸引关注的帖子。  

### 第4步：深入探究（可选）  
对于有价值的链接，可以使用`web_fetch`工具获取完整内容：  
```
web_fetch(url="https://reddit.com/...", maxChars=10000)
```  

### 第5步：结果整合  
将搜索结果整理成以下内容：  
1. **有效方法**：人们实际在做什么？  
2. **常见错误**：应避免哪些问题？  
3. **工具/技术**：具体使用的方法；  
4. **可复制提示**：结合最佳实践生成的、可直接使用的提示。  

## 输出格式  
```markdown
## 📅 Last 30 Days: [Topic]

### What's Working
- [Pattern 1]
- [Pattern 2]

### Common Mistakes
- [Mistake 1]

### Key Techniques
- [Technique with source]

### Sources
- [URL 1] - [brief description]
- [URL 2] - [brief description]

### Ready-to-Use Prompt (if applicable)
```  
[根据搜索结果生成的提示]  
```
```  

**示例：**  
- `/last30days Midjourney v7提示技巧`  
- `/last30days Claude代码最佳实践`  
- `/last30days 人们对M4 MacBook的评价`  
- `/last30days 实际有效的Suno音乐生成提示`  

**注意事项：**  
- 无需额外API密钥（使用Brave浏览器和bird工具）；  
- bird工具需要X/Twitter的cookies（已配置好）；  
- 优先关注高质量内容（高赞帖子和经过验证的用户分享）。