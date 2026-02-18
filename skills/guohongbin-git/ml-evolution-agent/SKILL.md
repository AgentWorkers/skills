---
name: ml-evolution-agent
description: "自动进化的机器学习竞赛代理。它从每次实验中学习，积累多层记忆（HCC），并持续提升负载均衡（LB）的评分。该代理的设计灵感来源于MLE-Bench #1中的ML-Master方法论。"
metadata:
  openclaw:
    emoji: "🤖"
    version: "1.0.0"
    author: "OpenClaw Agent"
    requires:
      bins: ["kaggle", "python3"]
    tags: ["machine-learning", "kaggle", "auto-ml", "evolution", "memory"]
---
# ML Evolution Agent 🤖

这是一个能够自动进化的机器学习竞赛代理，它从每次实验中学习。

## 该技能的功能

1. 为Kaggle风格的竞赛自动进化机器学习模型。
2. 采用HCC多层记忆架构（包括情节记忆、模式记忆、知识记忆和策略记忆层）。
3. 实现持续改进——每个阶段都会从前一次的失败或成功中学习。
4. 具有资源感知能力，会遵守系统限制（如时间、内存和API配额）。

## 适用场景

- 当用户提到Kaggle竞赛时。
- 需要处理表格数据的分类或回归任务。
- 需要突破目标最低分数（LB score）。
- 用户希望实现自动化的机器学习实验过程。

## 快速入门

```python
# Initialize
from ml_evolution import MLEvolutionAgent

agent = MLEvolutionAgent(
    competition="playground-series-s6e2",
    target_lb=0.95400,
    data_dir="./data"
)

# Run evolution
agent.evolve(max_phases=10)
```

## HCC记忆架构

```
Layer 1: Episodic Memory
├── Experiment logs (phase, CV, LB, features, params)
├── Success/failure records
└── Resource usage tracking

Layer 2: Pattern Memory
├── What works (success patterns)
├── What fails (failure patterns)
└── When to use each approach

Layer 3: Knowledge Memory
├── Feature engineering techniques
├── Model configurations
├── Hyperparameter knowledge
└── Domain-specific features

Layer 4: Strategic Memory
├── Auto-evolution rules
├── Resource management rules
├── Exploration-exploitation balance
└── Competition-specific strategies
```

## 经过实际竞赛验证的技巧

### 特征工程
| 技巧 | 效果 | 最适合的场景 |
|-----------|--------|----------|
| 目标统计信息 | 提高最低分数（LB）0.00018分 | 所有表格数据 |
| 频率编码 | 提高最低分数（LB）0.00005分 | 高基数特征 |
| 平滑目标编码 | 防止过拟合 |  
| 医疗指标 | 提高交叉验证（CV）分数0.00006分 | 健康数据 |

### 模型配置
| 模型 | 最佳参数 | 权重占比 |
|-------|-------------|--------|
| CatBoost | 迭代次数：1000-1200次，学习率：0.04-0.05，深度：6-7层 | 50% |
| XGBoost | 预训练次数：1000-1200次，学习率：0.04，最大深度：6层 | 25-30% |
| LightGBM | 预训练次数：1000-1200次，学习率：0.04，叶子节点数：40 | 20-25% |

### 资源限制
- 特征数量：少于60个（避免超时）
- 迭代次数：少于1200次（避免系统异常终止）
- 训练时间：少于20分钟（系统限制）
- 每日提交次数：10次（Kaggle配额）

## 进化规则

```python
# Auto-evolution decision tree
if phase_improved:
    keep_features()
    try_similar_approach()
elif phase_degraded > 0.0001:
    rollback()
    try_new_direction()
else:
    fine_tune_params()

# Overfitting detection
if cv_lb_gap > 0.002:
    increase_regularization()
    reduce_features()
    simplify_model()
```

## 文件结构

```
ml-evolution-agent/
├── SKILL.md              # This file
├── HCC_MEMORY.md         # Memory architecture details
├── FEATURE_ENGINEERING.md # Feature techniques library
├── MODEL_CONFIGS.md      # Optimal model configurations
├── EVOLUTION_RULES.md    # Auto-evolution decision rules
└── templates/
    ├── train_baseline.py # Baseline training script
    ├── train_evolved.py  # Evolution training script
    └── memory.json       # Example memory state
```

## 示例结果

**Playground S6E2（2026年2月）**
- 初始最低分数：0.95347
- 最佳最低分数：0.95365（提升0.00018分）
- 进化阶段：14个
- 成功率：36%
- 是否突破目标分数：是（从0.95361提升到0.95365）

## 主要经验总结

1. **简单策略优于复杂策略**——使用目标统计信息通常比复杂的特征工程更有效。
2. **资源限制至关重要**——特征数量过多可能导致超时。
3. **CatBoost表现最佳**——在处理表格数据时始终是最优选择。
4. **需注意每日提交次数限制**——Kaggle对提交次数有明确限制。

## 安装方法

```bash
clawhub install ml-evolution-agent
```

---

*该算法基于实际竞赛经验开发，经过14个阶段的实验不断优化而成。*