---
name: elpa
description: "通过触发外部子模型训练任务（例如 PyTorch/Prophet/TiDE/transformers），来编排符合 ELPA 标准的集成预测工作流程；随后根据验证过程中的误差计算 ELPA 的在线/离线权重。当需要面向生产环境的集成模型训练时，应使用该方法，而非轻量级的模拟适配器。"
---
# ELPA

## 概述

该技能并不用于训练简单的适配器（toy adapters），而是会从用户自己的训练代码库中触发实际的子模型训练命令，并根据实际的验证错误（validation errors）来构建 ELPA 路由（routing）和权重（weights）。

默认的模型池（model pool）规模被设计得大于 4 个模型，并且可以自由扩展。

## 工作流程

1. 准备训练配置文件（JSON 格式），参见 `assets/elpa_train_template.json`。
2. 运行命令计划（command plan）的预测试（dry-run），以验证所有子模型的训练命令是否正确。
3. 在资源充足的情况下，执行实际的子模型训练。
4. 为每个模型准备验证错误数据。
5. 根据这些验证错误数据，生成 ELPA 集成策略（ELPA integration policy）的 JSON 文件。

## 1) 准备配置文件

根据 `assets/elpa_train_template.json` 创建配置文件：

- 将每个模型的实际训练入口点（training entrypoint）添加到 `train_cmd` 中。
- 为每个模型指定其运行模式（`online` 或 `offline`）。
- 根据需要添加更多模型；ELPA 不受模型数量的限制（最多可支持 4 个模型）。

## 2) 预测试命令计划（不进行训练）

```bash
python3 scripts/elpa_orchestrator.py \
  --config assets/elpa_train_template.json \
  --run-dir .runtime/elpa_run \
  --manifest-out .runtime/elpa_run/train_manifest.json
```

该步骤会打印并记录所有将要执行的命令，但不会实际进行训练。

## 3) 执行实际训练

```bash
python3 scripts/elpa_orchestrator.py \
  --config /path/to/your_train_config.json \
  --run-dir .runtime/elpa_run \
  --manifest-out .runtime/elpa_run/train_manifest.json \
  --execute
```

请仅在具备所需机器学习依赖项和硬件的环境中执行此步骤。

## 4) 构建 ELPA 集成策略

在每个子模型生成验证错误后，运行以下命令：

```bash
python3 scripts/elpa_integrator.py \
  --config /path/to/your_integrate_config.json \
  --output .runtime/elpa_run/elpa_policy.json
```

输出内容包括：

- 每个模型的验证错误评分（validation error scores）
- `online_weights` 和 `offline_weights`
- 最优在线模型（`best_online_model`）和最优离线模型（`best_offline_model`）
- ELPA 控制参数（`beta`、`dirty_interval`、`amplitude_window`、`mutant_epsilon`）

## 模型扩展

若需要支持更多模型，只需在配置文件中添加新的模型块（model block），并指定模型的运行模式（`online` 或 `offline`）以及实际的训练命令（`train_cmd`）。添加模型时无需修改任何脚本。

## 相关文件

- `scripts/elpa_orchestrator.py`：用于执行子模型训练命令的规划器/执行器。
- `scripts/elpa_integrator.py`：根据验证错误数据生成 ELPA 评分和权重的工具。
- `assets/elpa_train_template.json`：适用于多模型训练的模板文件。
- `assets/elpa_integrate_template.json`：用于构建 ELPA 集成策略的模板文件。
- `references/config-schema.md`：配置文件中的字段参考和占位符说明。