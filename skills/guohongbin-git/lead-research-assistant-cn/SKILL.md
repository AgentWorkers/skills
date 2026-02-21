---
name: lead-research-assistant-cn
description: "销售线索研究助手 | Sales Lead Research Assistant  
功能概述：  
- 识别高质量的销售线索（Identify high-quality sales leads）  
- 分析目标公司（Analyze target companies）  
- 提供有效的联系策略（Provide contact strategies）  
关键词：  
销售线索（Sales leads）  
线索研究（Lead research）  
客户开发（Customer development）  
使用场景：  
帮助企业筛选和评估潜在客户，提高销售转化率。  
触发词：  
销售线索（Sales leads）  
线索研究（Lead research）  
客户开发（Customer development）"
metadata:
  openclaw:
    emoji: 🎯
    fork-of: "https://github.com/anthropics/skills"
---# 领先的研究助理（Lead Research Assistant）

这项技能通过分析您的产品/服务、了解理想客户画像，并提供可行的外联策略，帮助您识别和评估潜在的业务机会。

## 适用场景

- 寻找适合您产品/服务的潜在客户或合作伙伴
- 编制需要联系以建立合作关系的公司名单
- 确定适合销售外联的目标客户
- 研究符合您理想客户画像的公司
- 为业务发展活动做准备

## 功能概述

1. **深入了解您的业务**：分析您的产品/服务、价值主张以及目标市场。
2. **识别目标公司**：根据以下标准找到符合您理想客户画像的公司：
   - 行业和领域
   - 公司规模和地理位置
   - 使用的技术栈和工具
   - 发展阶段和资金状况
   - 您的产品能够解决的公司痛点
3. **对潜在客户进行优先级排序**：根据匹配度和相关性对公司的潜力进行评分。
4. **提供联系策略**：针对每个潜在客户提出个性化的沟通建议。
5. **丰富数据**：收集有关决策者和公司背景的相关信息。

## 使用方法

### 基本使用方法

只需描述您的产品/服务以及您的需求即可：

```
I'm building [product description]. Find me 10 companies in [location/industry] 
that would be good leads for this.
```

### 结合代码库使用

为了获得更准确的结果，您可以从产品的源代码目录中运行该技能：

```
Look at what I'm building in this repository and identify the top 10 companies 
in [location/industry] that would benefit from this product.
```

### 高级使用方法

为了进行更有针对性的研究，您可以进一步优化使用方法：

```
My product: [description]
Ideal customer profile:
- Industry: [industry]
- Company size: [size range]
- Location: [location]
- Current pain points: [pain points]
- Technologies they use: [tech stack]

Find me 20 qualified leads with contact strategies for each.
```

## 使用步骤

当用户请求进行潜在客户研究时，请按照以下步骤操作：

1. **了解产品/服务**
   - 如果在代码目录中，通过分析代码库来了解产品的功能。
   - 提出关于产品价值主张的问题以获取更多细节。
   - 明确产品的关键特性和优势。
   - 了解该产品能解决的具体问题。

2. **定义理想客户画像**
   - 确定目标行业和领域。
   - 确定公司规模范围。
   - 考虑地理位置偏好。
   - 了解相关的痛点。
   - 记录任何技术需求。

3. **进行研究并识别潜在客户**
   - 搜索符合上述标准的公司。
   - 寻找表明有需求的线索（如招聘信息、技术栈更新、行业动态）。
   - 关注公司的成长指标（如资金状况、扩张计划、招聘活动）。
   - 识别提供互补产品或服务的公司。
   - 检查公司的预算情况。

4. **进行优先级排序和评分**
   为每个潜在客户生成一个匹配度评分（1-10分）。
   - 考虑以下因素：
     - 与理想客户画像的契合度
     - 立即需求的迹象
     - 预算情况
     - 行业竞争状况
     - 时机选择。

5. **提供可执行的输出结果**
   - 为每个潜在客户提供以下信息：
     - **公司名称**和官网链接
     **适合的理由**：基于该公司业务背景的具体原因
     **优先级评分**（1-10分）及说明
     **决策者信息**：需要联系的角色或职位（例如“工程副总裁”）
     **沟通策略**：个性化的沟通建议
     **价值主张**：说明您的产品如何解决他们的具体问题
     **开场白**：用于沟通的推荐话题
     **LinkedIn链接**（如有）以便方便联系

6. **格式化输出结果**
   以清晰、易于阅读的格式呈现结果：

   ```markdown
   # Lead Research Results
   
   ## Summary
   - Total leads found: [X]
   - High priority (8-10): [X]
   - Medium priority (5-7): [X]
   - Average fit score: [X]
   
   ---
   
   ## Lead 1: [Company Name]
   
   **Website**: [URL]
   **Priority Score**: [X/10]
   **Industry**: [Industry]
   **Size**: [Employee count/revenue range]
   
   **Why They're a Good Fit**:
   [2-3 specific reasons based on their business]
   
   **Target Decision Maker**: [Role/Title]
   **LinkedIn**: [URL if available]
   
   **Value Proposition for Them**:
   [Specific benefit for this company]
   
   **Outreach Strategy**:
   [Personalized approach - mention specific pain points, recent company news, or relevant context]
   
   **Conversation Starters**:
   - [Specific point 1]
   - [Specific point 2]
   
   ---
   
   [Repeat for each lead]
   ```

7. **提供后续建议**
   - 建议将结果保存为CSV文件以供CRM系统导入。
   - 提供撰写个性化沟通邮件的帮助。
   - 根据时机建议确定沟通的优先级。
   - 建议对重点潜在客户进行进一步深入研究。

## 示例

### 示例1：来自Lenny的邮件

**用户**：“我正在开发一款用于在AI编码助手查询中屏蔽敏感数据的工具。请帮我找到潜在客户。”

**输出**：生成一份优先级排序的公司列表，这些公司：
- 使用AI编码助手（如Copilot、Cursor等）。
- 处理敏感数据（金融科技、医疗保健、法律行业）。
- 在GitHub代码库中显示使用编码辅助工具的痕迹。
- 可能曾在代码中意外泄露过敏感数据。
- 包含相关决策者的LinkedIn链接。

### 示例2：本地企业

**用户**：“我从事远程团队生产力咨询工作。请为我找到湾区内最近转为远程办公模式的10家公司。”

**输出**：识别出以下公司：
- 最近发布了远程工作职位招聘信息。
- 宣布了远程优先的政策。
- 正在招聘远程团队。
- 存在远程工作方面的挑战。
- 为每家公司提供个性化的沟通策略。

## 提高效果的建议

- **明确说明**您的产品及其独特价值。
- 如果适用，从代码库中运行该技能以自动获取更多背景信息。
- **详细说明**您的理想客户画像。
- **指定具体限制条件**（如行业、地理位置或公司规模）。
- **要求对有潜力的潜在客户进行进一步研究**以获取更深入的信息。

## 相关应用场景

- 在识别潜在客户后起草个性化的沟通邮件。
- 生成可用于CRM系统的合格潜在客户列表。
- 对特定公司进行详细研究。
- 分析竞争对手的客户群体。
- 寻找合作机会。