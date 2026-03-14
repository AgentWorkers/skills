---
name: lay-summary-gen
description: 将复杂的医学摘要转化为通俗易懂的总结，适用于患者、护理人员以及普通公众。在保持科学准确性的同时，确保内容的可读性。
  patients, caregivers, and the general public. Ensures readability while maintaining
  scientific accuracy.
version: 1.0.0
category: General
tags:
- patient-education
- plain-language
- health-literacy
- communication
author: AIPOCH
license: MIT
status: Draft
risk_level: Medium
skill_type: Tool/Script
owner: AIPOCH
reviewer: ''
last_updated: '2026-02-06'
---
# Lay Summary Gen

该工具为非专业读者生成医学研究的通俗易懂的摘要。

## 主要功能

- 将复杂的医学术语转换为简单的语言
- 去除专业术语
- 优化阅读难度（适合6-8年级学生）
- 提取关键信息
- 支持欧盟临床测试规则（EU CTR）的要求

## 输入参数

| 参数 | 类型 | 是否必填 | 说明 |
|-----------|------|----------|-------------|
| `abstract` | str | 是 | 医学研究的原始摘要 |
| `target_audience` | str | 否 | 目标读者群体（例如：“患者”、“公众”、“媒体”） |
| `max_words` | int | 否 | 最大字数限制（默认：250字） |

## 输出格式

```json
{
  "lay_summary": "string",
  "reading_level": "string",
  "key_takeaways": ["string"],
  "word_count": "int",
  "jargon_replaced": [{"term": "plain"}]
}
```

## 风险评估

| 风险指标 | 评估结果 | 风险等级 |
|----------------|------------|-------|
| 代码执行 | 在本地执行Python/R脚本 | 中等 |
| 网络访问 | 无外部API调用 | 低 |
| 文件系统访问 | 读取输入文件、写入输出文件 | 中等 |
| 指令篡改 | 遵循标准提示指南 | 低 |
| 数据泄露 | 输出文件保存在工作区 | 低 |

## 安全性检查清单

- [ ] 无硬编码的凭据或API密钥
- [ ] 无未经授权的文件系统访问
- [ ] 输出内容不包含敏感信息
- [ ] 有防止提示注入的安全机制
- [ ] 输入文件路径经过验证（防止遍历敏感目录）
- [ ] 输出目录限制在工作区内
- [ ] 脚本在沙箱环境中执行
- [ ] 错误信息经过处理（不显示堆栈跟踪）
- [ ] 依赖关系已审核

## 先决条件

无需额外的Python包。

## 评估标准

### 成功指标
- [ ] 脚本能够正常执行主要功能
- [ ] 输出内容符合质量标准
- [ ] 能够优雅地处理边缘情况
- [ ] 性能表现可接受

### 测试用例
1. **基本功能**：输入有效数据 → 输出符合预期
2. **边缘情况**：输入无效数据 → 脚本能够优雅地处理错误
3. **性能**：处理大型数据集时 → 处理时间在可接受范围内

## 生命周期状态

- **当前阶段**：草案阶段
- **下一次审查日期**：2026-03-06
- **已知问题**：无
- **计划中的改进**：
  - 优化性能
  - 增加更多功能支持