---
name: skill-analyzer
description: Comprehensive skill analysis tool that evaluates OpenClaw skills from 5 dimensions: functionality, security, usability, documentation, and best practices. Uses pure Python (no external dependencies). Provides weighted scoring, strengths/weaknesses analysis, and risk assessment. Use when user wants to analyze, review, or improve an existing skill.
---

# 技能分析器（Skill Analyzer）——全面技能评估工具

## 概述

技能分析器从5个维度对OpenClaw的技能进行评估，以提供全面的性能评估结果。它有助于识别优势、劣势以及改进的空间。该工具完全使用Python编写，无需任何外部依赖。

## 分析维度（共5个）

### 1. 功能性分析（25%）
- 核心功能的实现完整性
- 边缘情况的处理能力
- 错误处理与系统的稳健性
- 命令行界面的质量

### 2. 安全性分析（25%）
- 输入验证
- 凭据管理
- 无硬编码的敏感信息
- 安全的执行方式

### 3. 可用性分析（20%）
- 用户体验的质量
- 文档的清晰度
- 安装的复杂性
- 示例代码的可用性

### 4. 文档质量（15%）
- SKILL.md文件的完整性
- 文档的开头信息（名称、描述）
- 使用示例
- 标签的覆盖范围

### 5. 最佳实践（15%）
- 代码的结构与组织
- 错误处理方式
- 配置管理

## 使用方法

### 系统要求
- Python 3.7及以上版本（仅使用标准库，无需额外依赖）

### 分析某项技能

```bash
# Analyze a local skill
python3 scripts/analyzer.py --path /path/to/skill

# Analyze with detailed output
python3 analyzer.py --path /path/to/skill --verbose

# Output to JSON
python3 analyzer.py --path /path/to/skill --output report.json

# Compare two skills
python3 analyzer.py --compare skill1 skill2
```

### 维度评分标准

每个维度的评分范围为0-10：
- 8-10：优秀
- 6-7：良好
- 4-5：一般
- 2-3：低于平均水平
- 0-1：较差/需要改进

## 示例输出

```
==========================================
Skill Analysis Report: example-skill
==========================================

Overall Score: 7.5/10

Dimension Scores:
  Functionality:    8/10 ████████░░
  Security:         9/10 █████████░
  Usability:        7/10 ███████░░░
  Documentation:    6/10 ██████░░░░
  Best Practices:   7/10 ███████░░░

Strengths:
  ✓ Good security practices
  ✓ Clean code structure
  ✓ Proper error handling

Risk Level: LOW
```

## 注意事项

- 可以在任何包含技能文件的目录中运行该工具
- 完全使用Python编写，无需安装pip
- 可安全地应用于任何技能分析
- 不会修改被分析的技能文件本身