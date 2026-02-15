---
name: luban-cli
description: Luban CLI 的开发与管理：适用于 MLOps（机器学习运维）场景。在构建或使用 Luban CLI 时，可以利用该技能来管理实验环境、训练任务以及在线服务。
---

# Luban CLI 技能

该技能提供了一个结构化的框架，用于开发和使用 **Luban CLI**——一个专门用于模型生命周期管理（MLOps）的工具。

## 核心功能

Luban CLI 主要关注 MLOps 的三个核心方面：
1. **实验环境 (`env`)**：管理开发工作空间。
2. **训练任务 (`job`)**：协调模型训练工作负载。
3. **在线服务 (`svc`)**：部署和扩展推理服务。

## 开发工作流程

在开发或扩展 Luban CLI 时，请遵循以下步骤：
1. **初始化项目**：使用 `templates/cli_boilerplate.py` 中的模板作为 CLI 结构的起点。
2. **定义命令**：参考 `references/mlops_guide.md` 以了解每个实体的标准命令模式和所需属性。
3. **实现 CRUD 操作**：确保每个实体（`env`、`job`、`svc`）都支持完整的生命周期管理：
   - **创建**：配置新资源。
   - **读取**：列出并描述现有资源。
   - **更新**：修改配置或进行扩展。
   - **删除**：清理资源。

## 使用模式

### 管理实验环境
```bash
luban env list
luban env create --name research-v1 --image pytorch:2.0
```

### 管理训练任务
```bash
luban job create --script train.py --gpu 1
luban job status --id job_001
```

### 管理在线服务
```bash
luban svc create --model-path ./models/v1 --replicas 3
luban svc scale --id my-service --replicas 5
```

## 相关资源
- `templates/cli_boilerplate.py`：一个基于 Python 的 CLI 结构，使用 `argparse` 库进行参数解析。
- `references/mlops_guide.md`：关于 MLOps 实体和操作的详细规范。