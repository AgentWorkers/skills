---
name: variant-pathogenicity-predictor
description: 将 REVEL、CADD 和 PolyPhen 的评分结果整合起来，以预测变异体的致病性。
version: 1.0.0
category: Bioinfo
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
# 变异致病性预测器

该工具整合了REVEL、CADD、PolyPhen等算法，用于预测基因突变的致病性。

## 使用方法

```bash
python scripts/main.py --variant "chr17:43094692:G:A" --gene "BRCA1"
python scripts/main.py --vcf variants.vcf --output report.json
```

## 参数

- `--variant`：突变信息，格式为 `chr:pos:ref:alt`
- `--vcf`：包含突变的VCF文件
- `--gene`：目标基因的符号
- `--scores`：要使用的预测算法（REVEL、CADD、PolyPhen）

## 集成使用的预测算法

- REVEL（Rare Exome Variant Ensemble Learner）
- CADD（Combined Annotation Dependent Depletion）
- PolyPhen-2（Polymorphism Phenotyping）
- SIFT（Sorting Intolerant From Tolerant）
- MutationTaster

## 输出结果

- 突变的致病性分类
- 根据ACMG指南的解释结果
- 各个预测算法的得分详情
- 预测结果的置信度评估

## 风险评估

| 风险指标 | 评估内容 | 风险等级 |
|----------------|------------|-------|
| 脚本执行 | 在本地执行Python/R脚本 | 中等 |
| 网络访问 | 无外部API调用 | 低 |
| 文件系统访问 | 读取输入文件、写入输出文件 | 中等 |
- 脚本篡改 | 遵循标准提示指南 | 低 |
| 数据泄露 | 输出文件保存在工作区 | 低 |

## 安全性检查清单

- [ ] 无硬编码的凭证或API密钥
- [ ] 无未经授权的文件系统访问
- [ ] 输出内容不包含敏感信息
- [ ] 有防止脚本注入的保护机制
- [ ] 输入文件路径经过验证（防止遍历敏感目录）
- [ ] 输出目录限制在工作区内
- [ ] 脚本在沙箱环境中执行
- [ ] 错误信息经过处理（不暴露堆栈追踪）
- [ ] 依赖库已审核

## 先决条件

无需额外安装Python包。

## 评估标准

### 成功指标

- [ ] 脚本能成功执行主要功能
- [ ] 输出结果符合质量标准
- [ ] 能妥善处理边缘情况
- [ ] 性能表现可接受

### 测试用例

1. **基本功能**：输入标准数据 → 输出预期结果
2. **边缘情况**：输入无效数据 → 脚本能优雅地处理错误
3. **性能**：处理大规模数据集时，处理时间在可接受范围内

## 开发阶段

- **当前阶段**：草案阶段
- **下一次审查日期**：2026-03-06
- **已知问题**：无
- **计划改进**：
  - 优化性能
  - 支持更多预测算法