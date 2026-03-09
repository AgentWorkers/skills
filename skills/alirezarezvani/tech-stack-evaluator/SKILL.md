---
name: "tech-stack-evaluator"
description: 技术栈的评估与比较包括TCO（总拥有成本）分析、安全评估以及生态系统健康状况的评分。这些方法可用于比较不同的框架、评估技术栈的优劣、计算总拥有成本、评估迁移方案，或分析生态系统的可行性。
---
# 技术栈评估工具

通过数据驱动的分析提供技术、框架和云服务提供商的评估与比较，并给出可操作的推荐建议。

## 目录

- [功能](#capabilities)
- [快速入门](#quick-start)
- [输入格式](#input-formats)
- [分析类型](#analysis-types)
- [脚本](#scripts)
- [参考资料](#references)

---

## 功能

| 功能 | 描述 |
|------------|-------------|
| 技术比较 | 使用加权评分来比较不同的框架和库 |
| 总拥有成本（TCO）分析 | 计算包括隐性成本在内的5年总成本 |
| 生态系统健康状况评估 | 通过GitHub指标、npm使用情况以及社区活跃度来评估生态系统健康状况 |
| 安全性评估 | 评估漏洞及合规性准备情况 |
| 迁移分析 | 估算迁移的工作量、风险及时间表 |
| 云服务提供商比较 | 为特定工作负载比较AWS、Azure和GCP |

---

## 快速入门

### 比较两种技术

```
Compare React vs Vue for a SaaS dashboard.
Priorities: developer productivity (40%), ecosystem (30%), performance (30%).
```

### 计算总拥有成本（TCO）

```
Calculate 5-year TCO for Next.js on Vercel.
Team: 8 developers. Hosting: $2500/month. Growth: 40%/year.
```

### 评估迁移需求

```
Evaluate migrating from Angular.js to React.
Codebase: 50,000 lines, 200 components. Team: 6 developers.
```

---

## 输入格式

该评估工具支持三种输入格式：

**文本** - 自然语言查询
```
Compare PostgreSQL vs MongoDB for our e-commerce platform.
```

**YAML** - 用于自动化的结构化输入
```yaml
comparison:
  technologies: ["React", "Vue"]
  use_case: "SaaS dashboard"
  weights:
    ecosystem: 30
    performance: 25
    developer_experience: 45
```

**JSON** - 程序化集成
```json
{
  "technologies": ["React", "Vue"],
  "use_case": "SaaS dashboard"
}
```

---

## 分析类型

### 快速比较（200-300个字符）
- 加权评分及推荐结果
- 最重要的3个决策因素
- 信心水平

### 标准分析（500-800个字符）
- 对比矩阵
- 总拥有成本概览
- 安全性总结

### 完整报告（1200-1500个字符）
- 所有指标和计算结果
- 迁移分析
- 详细建议

---

## 脚本

### stack_comparator.py

使用可定制的加权标准来比较技术。

```bash
python scripts/stack_comparator.py --help
```

### tco_calculator.py

计算多年的总拥有成本。

```bash
python scripts/tco_calculator.py --input assets/sample_input_tco.json
```

### ecosystem_analyzer.py

通过GitHub、npm和社区指标来分析生态系统健康状况。

```bash
python scripts/ecosystem_analyzer.py --technology react
```

### security_assessor.py

评估安全态势及合规性准备情况。

```bash
python scripts/security_assessor.py --technology express --compliance soc2,gdpr
```

### migration_analyzer.py

估算迁移的复杂性、工作量及风险。

```bash
python scripts/migration_analyzer.py --from angular-1.x --to react
```

---

## 参考资料

| 文档 | 内容 |
|----------|---------|
| `references/metrics.md` | 详细的评分算法和计算公式 |
| `references/examples.md` | 所有分析类型的输入/输出示例 |
| `references/workflows.md` | 逐步评估的工作流程 |

---

## 信心水平

| 信心水平 | 评分 | 解释 |
|-------|-------|----------------|
| 高 | 80-100% | 明确的胜者，数据支持充分 |
| 中等 | 50-79% | 存在权衡，不确定性适中 |
| 低 | < 50% | 结果难以确定，数据有限 |

---

## 使用场景

- 为新项目比较前端/后端框架 |
- 为特定工作负载评估云服务提供商 |
- 规划技术迁移并评估风险 |
- 通过总拥有成本（TCO）来决定是自行开发还是购买软件 |
- 评估开源库的适用性

## 不适用场景

- 在相似工具之间做简单选择（依赖团队偏好） |
- 已经确定的技术选择 |
- 紧急的生产问题（使用监控工具）