---
name: wandb
description: 监控并分析权重（weights）和偏差（biases）的训练过程。适用于检查训练状态、检测故障、分析损失曲线（loss curves）、比较不同训练运行结果，或监控实验进展。相关触发事件包括：`wandb`、`training runs`、`how's training`、`did my run finish`、`any failures`、`check experiments`、`loss curve`、`gradient norm`、`compare runs`。
---

# 权重与偏差（Weights & Biases）

监控、分析并比较权重与偏差的训练过程。

## 设置（Setup）

```bash
wandb login
# Or set WANDB_API_KEY in environment
```

## 脚本（Scripts）

### 描述一次训练运行（全面健康状况分析）（Describe a Run (Full Health Analysis)）

```bash
~/clawd/venv/bin/python3 ~/clawd/skills/wandb/scripts/characterize_run.py ENTITY/PROJECT/RUN_ID
```

分析内容：
- 损失曲线趋势（从开始到当前，变化百分比，方向）
- 梯度范数的健康状况（检测梯度是否出现爆炸性增长或消失）
- 评估指标（如果有的话）
- 运行停滞情况（通过“心跳”指标检测）
- 进度及预计完成时间
- 配置参数的亮点
- 整体运行健康状况评估

选项：`--json` 用于生成机器可读的输出格式。

### 监控所有正在运行的作业（Watch All Running Jobs）

```bash
~/clawd/venv/bin/python3 ~/clawd/skills/wandb/scripts/watch_runs.py ENTITY [--projects p1,p2]
```

提供所有正在运行的作业的快速健康状况总结，以及最近的失败或完成情况。非常适合用于晨间简报。

选项：
- `--projects p1,p2` — 指定要检查的项目
- `--all-projects` — 检查所有项目
- `--hours N` — 检查已完成运行的时间范围（默认：24小时）
- `--json` — 生成机器可读的输出格式

### 比较两次训练运行（Compare Two Runs）

```bash
~/clawd/venv/bin/python3 ~/clawd/skills/wandb/scripts/compare_runs.py ENTITY/PROJECT/RUN_A ENTITY/PROJECT/RUN_B
```

进行对比分析：
- 配置参数的差异（突出显示重要参数）
- 同一阶段的损失曲线
- 梯度范数的比较
- 评估指标
- 性能指标（token/秒，步骤/小时）
- 确定哪次运行更优

## Python API 快速参考（Python API Quick Reference）

```python
import wandb
api = wandb.Api()

# Get runs
runs = api.runs("entity/project", {"state": "running"})

# Run properties
run.state      # running | finished | failed | crashed | canceled
run.name       # display name
run.id         # unique identifier
run.summary    # final/current metrics
run.config     # hyperparameters
run.heartbeat_at # stall detection

# Get history
history = list(run.scan_history(keys=["train/loss", "train/grad_norm"]))
```

## 主要指标名称的变体（Metric Key Variations）

脚本会自动处理以下指标名称的转换：
- 损失（Loss）：`train/loss`、`loss`、`train_loss`、`training_loss`
- 梯度（Gradients）：`train/grad_norm`、`grad_norm`、`gradient_norm`
- 步骤数（Steps）：`train/global_step`、`global_step`、`step`、`_step`
- 评估指标（Eval）：`eval/loss`、`eval_loss`、`eval_acc`

## 健康状况阈值（Health Thresholds）

- **梯度 > 10**：梯度值过高（严重问题）
- **梯度 > 5**：梯度值波动较大（警告）
- **梯度 < 0.0001**：梯度值接近于零（警告）
- **“心跳”时间 > 30分钟**：运行停滞（严重问题）
- **“心跳”时间 > 10分钟**：运行速度较慢（警告）

## 集成说明（Integration Notes）

- 用于晨间简报时，使用 `watch_runs.py --json` 并解析输出结果。
- 如需详细分析某次训练运行，使用 `characterize_run.py`。
- 进行A/B测试或超参数比较时，使用 `compare_runs.py`。