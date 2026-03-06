---
name: seo-content-engine
description: 自动化SEO内容研究、大纲生成以及初稿撰写功能。非常适合内容创作者和营销机构使用。
author: LobsterLabs
version: 0.1.0
metadata: {"clawdbot":{"emoji":"📝","requires":{"bins":["curl"]}}}
---
# SEO内容生成工具 📝  
专为OpenClaw设计的自动化SEO内容生成工具。能够研究主题、生成优化后的文章大纲，并撰写初稿。  

## 功能介绍  

- 🔍 **主题研究**：分析任何关键词下排名靠前的内容  
- 📋 **大纲生成**：创建符合SEO规范的文章结构  
- ✍️ **初稿撰写**：撰写1500至2500字的文章，并设置合理的标题层级  
- 🎯 **关键词整合**：推荐并融入主要/次要关键词  
- 📊 **竞争对手分析**：识别内容空白点及排名前5的网站差异  

## 命令  

### 研究主题  
```
Research "[keyword/topic]" for SEO content
```  

### 生成大纲  
```
Create outline for "[article title]" targeting "[primary keyword]"
```  

### 撰写初稿  
```
Write draft for "[article title]" using outline, 2000 words, tone: [professional/casual/technical]
```  

### 完整工作流程  
```
Create SEO article about "[topic]" - research, outline, and draft (2000 words)
```  

## 输出格式  

每篇文章包含：  
- 元标题（50-60个字符）  
- 元描述（150-160个字符）  
- H1标题  
- 引言（150-200字）  
- 带有正确层级结构的H2/H3段落  
- 结论及行动号召（CTA）  
- 推荐的内部/外部链接  
- 常见问题解答（FAQ）部分（3-5个问题）  

## 配置选项  

可选的环境变量：  
- `CONTENT_TONE`：默认语气（专业|随意|技术性|友好）  
- `DEFAULT_LENGTH`：默认字数（默认：2000字）  
- `INCLUDE_FAQ`：是否包含FAQ部分（true|false，默认：true）  

## 使用示例  

**用户**：要求生成一篇关于“最适合小型企业的AI自动化工具”的SEO文章（2500字）  

**助手**：  
1. 研究“AI自动化工具 小型企业”关键词下排名前10的网站  
2. 分析内容空白点及关键词使用机会  
3. 生成优化后的文章大纲  
4. 撰写2500字的初稿，并设置H2/H3结构  
5. 添加元标签和FAQ部分  

✅ 文章已完成！[查看初稿]  

## 定价方案  

该工具支持LobsterLabs的内容服务：  
- 单篇文章：300-500美元  
- 月度套餐（4篇文章）：1500-2500美元  
- 白标服务：每月3000美元起  

联系方式：PayPal 492227637@qq.com  

## 更新日志  

### 0.1.0（2026-03-06）  
- 初始版本发布  
- 基本的研究、大纲生成及初稿撰写流程  
- SEO优化功能加入