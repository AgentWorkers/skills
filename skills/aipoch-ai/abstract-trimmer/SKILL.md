---
name: abstract-trimmer
description: 将学术摘要压缩以符合严格的字数限制，同时确保保留关键信息、科学准确性和可读性。支持多种压缩策略，适用于期刊投稿、会议申请和科研基金申请。
  key information, scientific accuracy, and readability. Supports multiple compression 
  strategies for journal submissions, conference applications, and grant proposals."
version: 1.0.0
category: General
tags: ["abstract", "editing", "compression", "academic-writing", "word-count"]
author: AIPOCH
license: MIT
status: Draft
risk_level: Medium
skill_type: Tool/Script
owner: AIPOCH
reviewer: ''
last_updated: '2026-02-15'
---
# 摘要精简工具

这是一个精准编辑工具，通过智能压缩技术减少摘要的词数，同时保持科学严谨性，满足期刊和会议的严格要求。

## 特点

- **智能压缩**：提供多种压缩策略（激进型、保守型、平衡型）
- **关键信息保留**：保留关键发现和统计数据
- **结构完整性**：保持“背景-方法-结果-结论”的结构
- **数据安全性**：保护数字、P值和置信区间
- **批量处理**：高效处理多个摘要
- **质量验证**：压缩后检查可读性和准确性

## 使用方法

### 基本用法

```bash
# Trim abstract from file
python scripts/main.py --input abstract.txt --target 250

# Trim abstract from command line
python scripts/main.py --text "Your abstract here..." --target 200

# Check word count only
python scripts/main.py --input abstract.txt --target 250 --check-only
```

### 参数

| 参数 | 类型 | 默认值 | 是否必填 | 说明 |
|-----------|------|---------|----------|-------------|
| `--input`, `-i` | str | 无 | 否 | 包含摘要的输入文件 |
| `--text`, `-t` | str | 无 | 否 | 摘要文本（替代 `--input`） |
| `--target`, `-T` | int | 250 | 否 | 目标词数 |
| `--strategy`, `-s` | str | “balanced” | 否 | 压缩策略（保守型/平衡型/激进型） |
| `--output`, `-o` | str | 无 | 否 | 输出文件路径 |
| `--check-only`, `-c` | 标志 | 否 | 仅检查词数，不进行压缩 |
| `--format` | str | “json” | 否 | 输出格式（json/文本） |

### 高级用法

```bash
# Aggressive trimming with text output
python scripts/main.py \
  --input abstract.txt \
  --target 200 \
  --strategy aggressive \
  --format text \
  --output trimmed.txt

# Batch check multiple abstracts
for file in *.txt; do
  python scripts/main.py --input "$file" --target 250 --check-only
done
```

## 压缩策略

| 策略 | 方法 | 适用场景 |
|----------|----------|----------|
| **保守型** | 删除填充词，简化句子 | 轻微压缩（10-20个词） |
| **平衡型** | 合并句子，精简短语 | 中等程度压缩（20-50个词） |
| **激进型** | 删除次要细节，使用缩写 | 大幅度压缩（50个词以上） |

## 输出格式

### JSON 输出

```json
{
  "trimmed_abstract": "Compressed abstract text...",
  "original_words": 320,
  "final_words": 248,
  "reduction_percent": 22.5
}
```

### 文本输出

```
Compressed abstract text...
```

## 技术难度：**低**

⚠️ **AI自动审核状态**：需要人工检查

该工具要求：
- Python 3.7及以上环境
- 无外部依赖

## 依赖项

### 必需的Python包

```bash
pip install -r requirements.txt
```

### 所需文件

无需外部依赖项（仅使用Python标准库）。

## 风险评估

| 风险指标 | 评估结果 | 风险等级 |
|----------------|------------|-------|
| 代码执行 | 在本地执行Python脚本 | 低 |
| 网络访问 | 无需网络访问 | 低 |
| 文件系统访问 | 仅读写文本文件 | 低 |
| 指令篡改 | 遵循标准提示指南 | 低 |
| 数据泄露 | 无敏感数据泄露 | 低 |

## 安全性检查

- [x] 无硬编码的凭据或API密钥
- [x] 无未经授权的文件系统访问
- [x] 输出内容不泄露敏感信息
- [x] 有防止命令注入的保护措施
- [x] 输入文件路径经过验证
- [x] 输出目录限制在工作区内
- [x] 脚本在沙箱环境中执行
- [x] 错误信息经过处理
- [x] 依赖项经过审核

## 先决条件

```bash
# No dependencies required
python scripts/main.py --help
```

## 评估标准

### 成功指标
- [ ] 成功将摘要压缩到目标词数
- [ ] 保留关键的科学信息
- [ ] 保持语法正确性
- [ ] 得体地处理边缘情况

### 测试用例
1. **基本压缩**：输入摘要 → 压缩至目标词数
2. **检查模式**：使用 `--check-only` 标志 → 报告词数统计
3. **文件读写**：正确读取和写入文件
4. **不同策略**：三种策略均能正常工作 → 不同的压缩程度

## 生命周期状态

- **当前阶段**：草案阶段
- **下一次审查日期**：2026-03-15
- **已知问题**：无
- **计划中的改进**：
  - 加强对数值数据的保护
  - 支持结构化摘要
  - 批量处理模式

## 参考资料

请参阅 `references/`：
- 压缩策略文档
- 保护元素指南
- 各期刊的词数限制

## 限制

- **语言**：针对英语学术摘要优化
- **内容类型**：适用于结构化摘要（BMRC格式）
- **不进行重写**：仅删除/压缩内容，不重新表述
- **最终审核**：自动压缩结果需人工验证

---

**✂️ 注意：此工具可帮助您遵守字数限制，但切勿牺牲科学准确性。请确保压缩后的摘要仍能完整地反映您的研究结果。**