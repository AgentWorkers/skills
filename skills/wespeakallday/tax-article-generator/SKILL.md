---
name: tax-article-generator
description: 生成关于南非税收/增值税（VAT）/SARS合规性的相关文章
version: 1.0.0
author: Migration from Agent Zero
---
# 税务/增值税文章生成工具

## 概述
该工具能够自动生成关于南非税务合规性的文章，涵盖SARS（南非税务局）的截止日期、增值税（VAT）、预付税款（PAYE）以及临时税款的相关内容。

## 目的
- 为PayLessTax博客生成符合搜索引擎优化（SEO）要求的税务文章
- 确保SARS截止日期的准确性及合规性信息的准确性
- 使用JSON模式创建结构化内容，以便于自动化处理

## 输入变量（模板占位符）
| 变量 | 描述 | 示例 |
|----------|-------------|---------|
| ARTICLE_TITLE | 文章的完整标题 | SARS 2026纳税季：重要的合规日期 |
| MAINKeyword | 主要SEO关键词 | SARS 2026合规性 |
| YEAR | 税务年度 | 2026 |
| DEADLINE_1_DATE | 第一个截止日期 | 2026年8月31日 |
| DEADLINE_1_NAME | 第一个截止日期的说明 | 预付税款第一阶段 |
| DEADLINE_2_DATE | 第二个截止日期 | 2027年2月28日 |
| DEADLINE_3_DATE | 第三个截止日期 | 2027年9月30日 |
| PENALTY_INFO | 处罚信息 | 应缴税款的10% |
| INTEREST_RATE | 利率计算公式 | 市场利率 + 4% |
| CTA_TEXT | 行动号召 | 下载我们的检查清单 |

## 文章类型
### SARS合规指南
- 按年度划分的截止日期概述
- 预付税款的缴纳日期
- 年度申报窗口
- 增值税提交时间表
- 处罚信息

### 增值税文章
- VAT 201表格的详细信息
- A/B/C/D/E类别的申报要求
- 逾期提交的处罚措施
- 进出口税规则

### 预付税款文章
- EMP201表格的提交日期
- 每月申报要求
- UIF/SDL相关组件

### 预付税款指南
- IRP6表格的使用说明
- 第一、第二、第三阶段的申报流程
- 预估税款计算方法
- 申报金额低于实际金额时的处罚措施

## 输出格式
```json
{
  "title": "generated title",
  "author": "PayLessTax Team",
  "content": "# Markdown content...",
  "seo_metadata": {...}
}
```

## 触发方式
- 定期的税务日历事件
- 手动通过命令行界面（CLI）执行
- 可选：通过WordPress/WooCommerce的Webhook触发

## 所需API及依赖库
- 内置的Python库（无需外部API）
- 无需任何敏感信息（仅用于内容生成）
- 可选：使用WordPress REST API进行文章发布

## 相关文件
- index.py - 文章生成逻辑代码
- schemas/ - 各文章类型的JSON模式文件
- templates/ - 使用Jinja2模板生成的文件