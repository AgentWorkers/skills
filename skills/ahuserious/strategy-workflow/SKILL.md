---
name: strategy-workflow
description: 从构思到验证的全面策略开发工作流程。适用于创建交易策略、运行回测、参数优化或进行前瞻性验证的场景。
version: "2.0.0"
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---
# 战略工作流程

这是一个全面的量化交易策略开发工作流程，从策略假设的提出到经过验证后的生产部署。

## 概述

本技能提供了一个完整的框架，用于开发、测试和验证交易策略。它支持以下功能：
- 基于假设的策略开发
- 在Vast.ai上进行的多GPU回测
- 使用Optuna进行贝叶斯超参数优化
- 前向验证和样本外测试
- 自动生成交易报告（tearsheet）

## 入口点

### 控制平面（集群编排）

始终运行的监控循环，用于管理硬件利用率和自我修复：

```bash
bash scripts/start_swarm_watchdogs.sh
```

对于本地环境，请设置明确的路径：

```bash
VENV_PATH=/path/to/.venv/bin/activate \
RESULTS_ROOT=/path/to/backtests \
STATE_ROOT=/path/to/backtests/state \
LOGS_ROOT=/path/to/backtests/logs \
bash scripts/start_swarm_watchdogs.sh
```

### 工作平面（并行执行）

一个统一的封装器，用于启动控制平面并启动并行任务：

```bash
scripts/backtest-optimize --parallel
```

### 多GPU、多符号执行

```bash
cd WORKFLOW && ./launch_parallel.sh
```

### 单符号管道

针对单一资产进行集中优化：

```bash
scripts/backtest-optimize --single --symbol SYMBOL --engine native --prescreen 50000 --paths 1000 --by-regime
```

## 策略开发

### 1. 假设制定

用可衡量的术语定义你的策略假设：
- 你正在利用哪些市场效率低下之处？
- 预期的持有期是多少？
- 进场/出场条件是什么？
- 目标风险调整后的回报是多少？

### 2. 特征选择

识别用于生成交易信号的相关特征：
- 基于价格的特征（OHLCV、回报、波动率）
- 技术指标（EMA、RSI、Bollinger Bands）
- 多时间帧特征（MTF重采样）
- 量量分析（PVSRA、VWAP）
- 市场微观结构（订单流、价差）

### 3. 信号生成

将特征转换为可执行的交易信号：
- 方向性偏好（趋势跟随、均值回归）
- 进场条件（阈值交叉、模式识别）
- 出场条件（止盈、止损、跟踪止损）
- 仓位大小规则

### 4. 仓位大小调整

实施基于风险的仓位大小调整：
- 固定比例法
- Kelly准则
- 波动率调整法
- 根据市场状况调整的仓位大小

## 回测

### 飞行前验证

**每次优化运行前必须执行**：

```bash
python validation.py --check-all --data-path DATA_PATH --symbol SYMBOL
```

验证检查：
- 数据长度至少为90天，且无缺失值/NaN
- 交易数量至少为30笔，以确保统计显著性
- MTF重采样正确实现
- 无前瞻性偏差

### 在Vast.ai上进行的多GPU执行

部署到云端的GPU实例上，进行大规模参数扫描：

```bash
# Copy workflow files
scp -P PORT workflow_files root@HOST:/root/WORKFLOW/

# Run optimization
ssh -p PORT root@HOST "cd /root/WORKFLOW && python optimize_strategy.py \
  --data-path /root/data --symbol SYMBOL --mode aggressive \
  --prescreen 5000 --paths 200 --engine gpu"
```

### 使用向量化回测进行预筛选

**阶段0**：GPU加速的参数筛选：
- 生成N组随机参数组合
- 在GPU上批量评估
- 根据交易数量（至少30笔）进行筛选
- 根据夏普比率筛选出表现最佳的K个参数组合

性能基准（RTX 5090，730d回测周期，250k个参数组合）：每种模式大约需要4秒。

### 使用NautilusTrader进行完整回测

**阶段1**：对表现最佳的参数组合进行事件驱动的回测：
- 高保真模拟，包含真实的交易执行情况
- 模拟滑点和佣金
- 多资产投资组合回测

## 参数优化

### 使用Optuna进行超参数搜索

**阶段2**：基于贝叶斯的超参数优化，从预筛选结果开始：

```python
import optuna

study = optuna.create_study(
    direction="maximize",
    sampler=optuna.samplers.TPESampler(seed=42),
    pruner=optuna.pruners.MedianPruner()
)

study.optimize(objective, n_trials=1000)
```

### 网格搜索与贝叶斯优化

| 方法 | 适用场景 |
|--------|----------|
| 网格搜索 | 参数空间较小，需要全面覆盖 |
| 随机搜索 | 参数空间较大，快速探索 |
| 贝叶斯优化（TPE） | 高效的优化方法，平衡了探索和利用 |
| CMA-ES | 适用于连续参数，目标函数平滑 |

### 策略剪枝

- **MedianPruner**：如果某个策略的表现低于已完成试验的中位数，则将其剔除
- **PercentilePruner**：剔除表现最差的X%的试验
- **HyperbandPruner**：多精度优化方法
- **SuccessiveHalvingPruner**：激进型的提前停止策略

### 分布式优化

对于大规模运行，使用持久化存储：

```python
# JournalStorage for multi-process
storage = optuna.storages.JournalStorage(
    optuna.storages.JournalFileStorage("journal.log")
)

# RDBStorage for distributed clusters
storage = optuna.storages.RDBStorage("postgresql://...")
```

## 前向验证

### 滚动窗口验证

随着时间的推移滑动训练/测试窗口：

```
[Train 1][Test 1]
    [Train 2][Test 2]
        [Train 3][Test 3]
```

参数设置：
- `train_window`：训练周期长度
- `test_window`：样本外测试长度
- `step_size`：窗口前进的步长

### 固定窗口前向验证

在滑动测试窗口的同时扩大训练窗口：

```
[Train 1      ][Test 1]
[Train 1 + 2      ][Test 2]
[Train 1 + 2 + 3      ][Test 3]
```

当历史市场环境的变化能够提高模型鲁棒性时，使用此方法。

### 时期选择标准

智能选择训练周期：
- **考虑市场环境**：使训练周期与预期部署条件相匹配
- **波动率调整**：包含高波动率和低波动率时期
- **包含重要事件**：确保涵盖重大市场事件
- **近期数据加权**：在保持多样性的同时，强调最近的数据

### 样本外测试

最终验证阶段：
- 保留20-30%的数据用于样本外测试
- 不要在样本外数据上调整参数
- 进行蒙特卡洛压力测试
- 根据市场环境条件分析性能

## 目标指标和限制

### 利用率目标

- CPU利用率目标：≥70%
- GPU利用率目标：≥70%
- 在进行GPU扫描时，不允许GPU出现空闲状态

### 硬件监控钩子

由以下脚本实现：
- `hooks/hardware_capacity_watchdog.py`
- `scripts/process_auditor.py`

### 容量监控

控制平面循环监控：
- 工作节点的健康状况和活跃度
- 进度文件的更新情况
- 资源利用率
- 作业队列长度

自我修复措施：
- 工作节点崩溃时自动重启
- 为利用率不足的资源分配任务
- 设置冷却机制，防止系统过载

## 生成交易报告

生成QuantStats风格的性能报告：

```bash
scripts/generate-tearsheet STRATEGY_NAME \
  --trades /path/to/trades.csv \
  --capital 10000 \
  --output ./tearsheets
```

有关详细的可视化选项，请参阅`tearsheet-generator`技能文档。

## 多提供者协调

### PAL MCP集成

将PAL作为MCP服务器，用于整合多个模型提供者的研究和共识机制：

- 配置模板：`config/mcp/pal.mcp.json.example`
- 文档：`docs/reference/PAL_MCP_INTEGRATION.md`
- 支持的提供者：OpenRouter、OpenAI、Anthropic、xAI、本地模型

## 资源

### 文档

- [VectorBT文档](https://vectorbt.dev/)
- [NautilusTrader文档](https://nautilustrader.io/)
- [Optuna文档](https://optuna.readthedocs.io/)
- [QuantStats](https://github.com/ranaroussi/quantstats)

### 项目参考文件

- `config/workflow_defaults.yaml` - 默认配置
- `config/model_policy.yaml` - 模型策略（建议性配置）
- `docs/guides/SWARM_OPTIMIZATION_RUNBOOK.md` - 详细的运行手册
- `hooks/pipeline-hooks.md` - 钩子合约
- `docs/reference/VECTORBT_graph_ingEST.md` - VectorBT PRO集成指南

### 结果结构

```
Backtests/optimizations/{SYMBOL}/{MODE}/
  best_sharpe/
    config.json      # Best Sharpe configuration
    metrics.json     # Performance metrics
  best_returns/
  lowest_drawdown/
  best_winrate/
  all_trials.json    # All Optuna trials
  phase0_top500.json # Prescreening results
```