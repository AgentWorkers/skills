---
name: lead-research-assistant-cn
description: "销售线索研究助手：该工具可帮助您深入分析您的产品/服务，自动搜索目标公司，并为您制定可行的联系策略。非常适合销售、商务拓展和市场营销人员使用。相关关键词包括：“寻找客户”、“销售线索”、“潜在客户”以及“商务拓展”。该工具由 ComposioHQ/awesome-claude-skills 开发。"
metadata:
  openclaw:
    emoji: 🎯
    fork-of: ComposioHQ/awesome-claude-skills/lead-research-assistant
---
# 领先的研究助理（Lead Research Assistant）

该技能通过分析您的产品/服务、了解您的理想客户画像，并提供可行的拓展策略，帮助您识别和评估潜在的业务机会。

## 适用场景

- 寻找适合您产品/服务的潜在客户或合作伙伴
- 编制需要联系以建立合作关系的公司名单
- 确定销售拓展的目标对象
- 研究符合您理想客户画像的公司
- 为业务发展活动做准备

## 功能介绍

1. **深入了解您的业务**：分析您的产品/服务、价值主张以及目标市场。
2. **识别目标公司**：根据以下标准找到符合您理想客户画像的公司：
   - 行业和领域
   - 公司规模和地理位置
   - 他们使用的技术栈和工具
   - 公司所处的成长阶段和资金状况
   - 您的产品能够解决的痛点
3. **对潜在客户进行优先级排序**：根据匹配度和相关性对 companies 进行评分。
4. **提供联系方式策略**：建议如何针对每个潜在客户制定个性化的沟通方案。
5. **丰富数据**：收集有关决策者和公司背景的相关信息。

## 使用方法

### 基本用法

只需描述您的产品/服务以及您的需求：

```
I'm building [product description]. Find me 10 companies in [location/industry] 
that would be good leads for this.
```

### 结合代码库使用

为了获得更好的结果，您可以从产品的源代码目录中运行该技能：

```
Look at what I'm building in this repository and identify the top 10 companies 
in [location/industry] that would benefit from this product.
```

### 高级用法

为了进行更精准的研究：

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

当用户请求进行潜在客户研究时：

1. **了解产品/服务**
   - 如果在代码目录中，分析代码库以了解产品功能。
   - 提出关于产品价值主张的问题以获取更多信息。
   - 明确产品的核心特性和优势。
   - 了解该产品能解决的具体问题。

2. **定义理想客户画像**
   - 确定目标行业和领域。
   - 确定公司规模范围。
   - 考虑地理位置偏好。
   - 了解相关的痛点。
   - 记录任何技术需求。

3. **进行研究并识别潜在客户**
   - 搜索符合上述标准的公司。
   - 寻找表明有需求的线索（如招聘信息、技术栈更新、最新新闻等）。
   - 关注公司的成长指标（如资金状况、扩张计划、招聘活动）。
   - 识别提供互补产品/服务的公司。
   - 检查公司的预算情况。

4. **进行优先级排序和评分**
   为每个潜在客户打分（1-10分）。
   - 考虑以下因素：
     - 与理想客户画像的匹配程度
     - 立即需求的迹象
     - 预算情况
     - 市场竞争状况
     - 时间节点。

5. **提供可执行的输出结果**
   - 为每个潜在客户提供以下信息：
     - **公司名称**和官网链接
     **适合的原因**：基于该公司业务特点的具体理由
     **优先级评分**（1-10分）及评分依据
     **决策者信息**：需要联系的角色/职位（例如“工程副总裁”）
     **沟通策略**：个性化的沟通建议
     **价值主张**：说明您的产品如何解决他们的具体问题
     **开场白**：用于沟通的要点
     **LinkedIn 链接**（如有）以便轻松建立联系

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

7. **提供后续步骤**
   - 建议将结果保存为 CSV 文件以便导入客户关系管理系统（CRM）。
   - 提供起草个性化沟通邮件的服务。
   - 根据时间节点建议确定沟通的优先级。
   - 建议对重点潜在客户进行进一步研究。

## 示例

### 示例 1：来自 Lenny 的邮件

**用户**：“我正在开发一款用于在 AI 编码助手查询中隐藏敏感数据的工具。请帮我找到潜在客户。”

**输出**：生成一份优先级排序的公司列表，这些公司：
- 使用 AI 编码助手（如 Copilot、Cursor 等）。
- 处理敏感数据（金融科技、医疗保健、法律行业）。
- 在其 GitHub 仓库中有使用编码辅助工具的记录。
- 可能曾在代码中意外泄露敏感数据。
- 包含相关决策者的 LinkedIn 链接。

### 示例 2：本地企业

**用户**：“我从事远程团队生产力咨询工作。请为我找到湾区内最近转为远程办公模式的 10 家公司。”

**输出**：识别出以下公司：
- 最近发布了远程工作职位招聘信息。
- 宣布了优先考虑远程办公的政策。
- 正在招聘远程团队。
- 存在远程工作方面的挑战。
- 为每家公司提供个性化的沟通策略。

## 提高效果的建议

- **明确说明**您的产品及其独特价值。
- 如果适用，可以从代码库中运行该技能以自动获取更多背景信息。
- **详细说明**您的理想客户画像。
- **指定具体要求**（如行业、地理位置或公司规模）。
- **请求对有潜力的潜在客户进行进一步研究**以获取更深入的信息。

## 相关应用场景

- 在识别潜在客户后起草个性化的沟通邮件。
- 生成可用于客户关系管理的 CSV 文件。
- 对特定公司进行详细研究。
- 分析竞争对手的客户群体。
- 寻找合作机会。