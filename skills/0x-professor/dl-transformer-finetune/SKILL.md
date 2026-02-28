---
name: dl-transformer-finetune
description: 构建用于Transformer模型微调的运行计划，其中包含任务设置、超参数以及模型训练结果。这些计划可用于Hugging Face或PyTorch框架下的可重复微调工作流程。
---
# DL Transformer Fine-tune

## 概述

为Transformer模型及其下游任务生成可复制的微调运行计划。

## 工作流程

1. 定义基础模型、任务类型和数据集。
2. 设置训练超参数和评估频率。
3. 生成运行计划及模型卡片框架。
4. 导出可用于训练管道的配置文件。

## 使用捆绑资源

- 运行 `scripts/build_finetune_plan.py` 以获得确定的运行计划输出。
- 阅读 `references/finetune-guide.md` 以获取超参数的基准指导信息。

## 规范与限制

- 通过指定种子值和输出目录来确保运行计划的可复现性。
- 必须包含评估和回滚策略。