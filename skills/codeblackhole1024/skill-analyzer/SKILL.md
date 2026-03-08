---
name: skill-analyzer
description: Quality scanner for OpenClaw skills. Evaluates functionality, security, usability, documentation, and best practices with weighted scoring. Use when: (1) Analyzing skill quality before publishing, (2) Finding improvement opportunities, (3) Security review of third-party skills. Pure Python - no dependencies.
---

# 技能分析器（Skill Analyzer）——全面技能评估工具

## 概述

技能分析器（Skill Analyzer）从5个维度对OpenClaw的技能进行全面评估，帮助用户了解自己的技能优势、劣势以及提升空间。该工具完全使用Python编写，无需任何外部依赖。

## 分析维度（共5个）

### 1. 功能性分析（25%）
- 核心功能的实现完整性
- 边缘情况的处理能力
- 错误处理机制的健全性
- 命令行界面的质量

### 2. 安全性分析（25%）
- 输入数据的验证
- 凭据管理
- 无硬编码的敏感信息
- 安全的执行方式

### 3. 可用性分析（20%）
- 用户体验质量
- 文档的清晰度
- 安装的复杂性
- 示例代码的可用性

### 4. 文档质量（15%）
- SKILL.md文件的完整性
- 文档的开头信息（名称、描述）
- 使用示例
- 标签的覆盖范围

### 5. 最佳实践（15%）
- 代码的结构和组织方式
- 错误处理机制
- 配置管理方式

## 使用方法

### 系统要求
- Python 3.7及以上版本（仅使用标准库，无需额外安装）

### 分析技能

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

- 该工具可以在包含技能文件的任意目录中运行
- 完全基于Python编写，无需安装pip
- 安全地分析任何技能文件
- 不会修改被分析的技能文件本身