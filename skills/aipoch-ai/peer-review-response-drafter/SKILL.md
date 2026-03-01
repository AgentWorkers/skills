---
name: peer-review-response-drafter
description: 协助起草专业的同行评审回复信。当用户提及“评审者评论”、“回复信”、“同行评审”、“修改后重新提交”、“R&R”（Review and Revise）或需要帮助回复学术期刊的评审者时，系统将自动触发该功能。
  when user mentions "reviewer comments", "response letter", "peer review", "revise
  and resubmit", "R&R", "reviewer feedback", or needs help responding to academic
  journal reviewers.
version: 1.0.0
category: Research
tags: []
author: AIPOCH
license: MIT
status: Draft
risk_level: Medium
skill_type: Tool/Script
owner: AIPOCH
reviewer: ''
last_updated: '2026-02-06'
---
# 同行评审回复起草工具

本工具帮助研究人员针对学术期刊投稿中的同行评审意见，撰写专业、礼貌且有效的回复。

## 概述

该工具能够解析评审意见，起草结构化的回复，并调整语言风格，以确保：
- 使用专业且礼貌的语言
- 清晰地逐点回应评审意见
- 以建设性的方式处理分歧
- 保持一致的学术写作风格

## 使用场景

- 在论文修改后回复同行评审意见
- 为期刊重新投稿准备作者回复信
- 处理主要的或次要的修改要求
- 为会议投稿起草反驳信
- 将非正式的笔记转化为正式的回复语言

## 工作流程

### 第一步：解析输入数据
收集并整理以下信息：
- **评审意见**：评审者的原始评论（通常带有编号或分段）
- **论文背景**：论文标题、期刊名称、修订轮次（如适用）
- **作者的修改内容**：针对每条评论所做的修改的简要说明
- **语言风格偏好**：正式的学术风格 / 外交风格 / 坚定的风格（默认为外交风格）

### 第二步：构建回复信
使用标准的学术回复信格式：

```
Dear Editor and Reviewers,

Thank you for your constructive feedback on our manuscript titled 
"[Title]" submitted to [Journal]. We have carefully addressed all 
comments and revised the manuscript accordingly. Below is our 
point-by-point response to each reviewer's comments.

Reviewer #1:
[Numbered responses]

Reviewer #2:
[Numbered responses]

...

Sincerely,
[Authors]
```

### 第三步：起草个别回复
针对每条评审意见，生成以下内容的回复：
1. **致谢**：感谢评审者的建议
2. **已采取的措施**：描述所做的修改
3. **修改位置**：修改所在的页面/行号
4. **可选说明**：如果未进行修改，提供简要解释

#### 回复模板

**接受建议**：
```
Comment: The methodology section lacks detail on data preprocessing.

Response: We thank the reviewer for this important observation. 
We have expanded the methodology section to include detailed 
descriptions of data preprocessing steps, including normalization, 
outlier removal, and feature selection procedures (Page 5, Lines 120-135).
```

**部分接受并作出修改**：
```
Comment: The authors should use Method X instead of Method Y.

Response: We appreciate the reviewer's suggestion. While Method X 
is indeed widely used, we found that Method Y is more appropriate 
for our specific dataset due to [brief rationale]. However, we have 
added a comparative discussion of both methods in the revised 
manuscript (Page 8, Lines 200-210) to acknowledge this alternative 
approach.
```

**礼貌地拒绝**：
```
Comment: The authors should remove Figure 3 as it seems redundant.

Response: We thank the reviewer for this suggestion. Upon careful 
consideration, we believe Figure 3 provides essential visual 
support for the key finding discussed in Section 4.2. To enhance 
clarity, we have revised the figure caption to better emphasize 
its unique contribution (Page 10, Figure 3 caption).
```

### 第四步：调整语言风格
根据具体情况调整语言风格：

| 语言风格 | 使用场景 | 例句 |
|------|----------|------------------|
| 外交风格 | 一般性修改 | “我们感谢……” / “我们非常感谢……” / “我们已经对……进行了修改……” |
| 坚定风格 | 为研究方法辩护 | “我们尊重地指出……” / “我们的方法是有根据的，因为……” |
| 感激风格 | 显著改进 | “我们对此表示感谢……” / “这大大提升了……的质量……” |

## 输入格式
支持多种输入格式：
- 复制的评审意见
- 从PDF文件中提取的文本
- 包含评论ID的结构化JSON数据
- 带有分段的Markdown格式

## 输出格式
生成的回复信应包含：
- 适当的称呼语和结束语
- 与评审意见对应的编号回复
- 对论文中修改位置的引用
- 全文保持专业的学术语言风格

## 使用示例

```
User: Help me draft a response to these reviewer comments:

Reviewer 1:
1. The introduction should better motivate the problem
2. Figure 2 is unclear
3. Have you considered Smith et al. 2023?

My changes:
1. Added motivation paragraph
2. Redrew Figure 2 with clearer labels
3. Added citation and discussion

Journal: Nature Communications
```

## 参数设置

| 参数 | 类型 | 是否必填 | 默认值 | 说明 |
|-----------|------|----------|---------|-------------|
| `--interactive` | 标志 | 否 | - | **交互模式**：提供引导式提示（使用`input()`函数）。适合首次使用或需要复杂回复的情况 |
| `--input-file` | 字符串 | 否 | - | 评审意见文件的路径（自动化模式） |
| `--output` | 字符串 | 否 | - | 回复信的输出文件路径 |
| `--tone` | 字符串 | 否 | "diplomatic" | 回复语言风格："diplomatic"（外交风格）、"formal"（正式风格）或"assertive"（坚定风格） |
| `--format` | 字符串 | 否 | "markdown" | 输出格式："markdown"、"plain_text"或"latex" |
| `--include-diff` | 布尔值 | 否 | 是否需要总结所做的修改 |

**使用模式**：
- **交互模式**：使用`--interactive`进行引导式设置（推荐给首次使用者）
- **文件模式（推荐用于自动化）**：使用`--input-file`输入预先准备好的评审意见文件

## 技术说明

- **难度**：较高 - 需要理解学术规范，能够根据上下文调整语言风格，并巧妙处理批评意见
- **限制**：不验证回复内容的事实准确性；技术性内容需人工审核
- **安全性**：不调用外部API；所有处理都在本地完成

## 参考资料

- `references/response_templates.md` - 常见的回复模板
- `references/tone_guide.md` - 学术语言风格指南
- `references/examples/` - 回复信示例

## 质量检查清单
在最终确定之前，请验证：
- 每条评审意见都有相应的回复
- 回复与评论的编号/字母顺序一致
- 所有修改都附有页面/行号引用
- 分歧以建设性的方式表达
- 语言风格保持专业且不具攻击性

## 风险评估

| 风险指标 | 评估内容 | 风险等级 |
|----------------|------------|-------|
| 代码执行 | 在本地执行的Python/R脚本 | 中等 |
| 网络访问 | 不调用外部API | 低 |
| 文件系统访问 | 读取输入文件、写入输出文件 | 中等 |
| 指令篡改 | 使用标准的提示系统 | 低 |
| 数据泄露 | 输出文件保存在工作区 | 低 |

## 安全性检查

- 未使用硬编码的凭证或API密钥
- 无未经授权的文件系统访问
- 输出文件不包含敏感信息
- 有防止脚本注入的安全措施
- 输入文件路径经过验证
- 输出目录限制在工作区内
- 脚本在沙箱环境中执行
- 错误信息经过处理（不显示堆栈追踪）
- 依赖项经过审核

## 先决条件

```bash
# Python dependencies
pip install -r requirements.txt
```

## 评估标准

### 成功指标
- 能够成功执行主要功能
- 输出符合质量标准
- 能够优雅地处理边缘情况
- 性能表现可接受

### 测试用例
1. **基本功能**：标准输入 → 预期输出
2. **边缘情况**：无效输入 → 良好的错误处理
3. **性能**：处理大量数据时仍能保持可接受的处理速度

## 开发阶段
- **当前阶段**：草案阶段
- **下一次审查日期**：2026-03-06
- **已知问题**：无
- **计划中的改进**：
  - 性能优化
  - 新功能的添加