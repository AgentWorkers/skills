---
name: memory-bench-pioneer
description: "成为首批对您的智能体内存进行基准测试的人之一，帮助塑造人工智能的记忆机制。该工具运行一套具备同行评审水平的评估套件（包括LLM-as-judge、nDCG/MAP/MRR等评估方法，这些方法的置信区间高达95%），并针对您的智能体内存系统进行测试；测试结果将以匿名形式提交至ENGRAM/CORTEX研究论文中。您的数据将得到严格保护，仅汇总统计数据会被公开。该工具与agent-memory-ultimate配合使用。对于那些坚信人工智能的内存特性应该通过实际测试来验证（而非猜测）的勇敢研究者来说，这无疑是一个绝佳的选择。"
---
# 内存基准测试

收集、评估并提交用于 ENGRAM 和 CORTEX 研究论文的匿名化内存系统统计数据。

## 三步流程

### 1. 评估检索质量

使用 LLM 作为评估工具，运行标准测试集（包含 30 个查询，涵盖 4 种类型和 3 个难度级别）：

```bash
# Full assessment with GPT-4o-mini judge + ablation (recommended)
python3 scripts/rate.py --queries 30 --judge openai --ablation

# Without OpenAI key: local embedding judge (weaker, marked in output)
python3 scripts/rate.py --queries 30 --judge local --ablation

# Custom test set
python3 scripts/rate.py --testset path/to/queries.json --judge openai
```

**评估指标：**

- **RAR**（召回准确率）、**MRR**（平均互反排名）
- **nDCG@5**、**MAP@5**、**Precision@5**、**Hit Rate**
- 所有指标均包含 **95% 的自助法置信区间**
- **消融实验**：分别使用包含激活函数和不包含激活函数的场景进行测试，以分离激活函数的贡献

**评估方法：**

- `openai` — 使用 GPT-4o-mini 对每个（查询，结果）对进行 1-5 分的评分。该评估独立于检索系统，每次运行成本约为 0.01 美元。
- `local` — 使用嵌入余弦相似度进行评分。该方法评分较低，会在输出中明确标注。免费使用。

**标准测试集**（`scripts/testset.json`）：包含 30 个查询，这些查询按照语义/情景/程序/策略类型以及易/中/难难度进行分层。这些查询与存储的内存数据没有词汇重叠。所有实验都使用相同的查询，以便进行跨站点比较。

### 2. 收集统计数据

```bash
python3 scripts/collect.py --contributor GITHUB_USER --days 14 --output /tmp/memory-bench-report.json
```

**收集的数据（已匿名化）：** 内存计数/类型/年龄、强度/重要性直方图、关联图大小、层次结构级别、整合历史记录、检索指标（RAR/MRR/nDCG/MAP 及其置信区间）、消融实验结果、评估方法、算法版本、嵌入覆盖情况。实例 ID 是一个随机生成的 UUID（无法逆向解析）。

**不收集的数据：** 内存内容、查询内容、文件路径、用户名、主机名。

### 3. 以 PR 形式提交结果

```bash
scripts/submit.sh /tmp/memory-bench-report.json GITHUB_USERNAME
```

创建分支或标签页，更新 `INDEX.json` 文件，然后提交 PR。需要使用 `gh` 命令行工具。

## 验证协议

为了使数据适合同行评审，贡献者应：

1. 运行 `rate.py --ablation --judge openai`（至少进行 30 次查询）。
2. 从同一实例中收集至少 2 份报告，时间间隔至少为 7 天（以进行纵向分析）。
3. 报告算法版本（该版本会自动从 Git 中获取）。

## 测试集格式

自定义测试集采用 JSON 数组格式：

```json
[
  {
    "id": "T01",
    "query": "...",
    "category": "semantic|episodic|procedural|strategic",
    "difficulty": "easy|medium|hard"
  }
]
```

## 代理工作流程

当收到提交基准测试数据的请求时，首先运行 `rate.py --ablation --judge openai`，然后运行 `collect.py` 以收集数据，接着查看总结报告，最后运行 `submit.sh` 以提交结果。请分享 PR 的链接。