---
name: mlops-prototyping-cn
version: 1.0.0
description: 使用流水线（pipeline）机制进行结构化Jupyter笔记本原型设计
license: MIT
---
# MLOps 原型开发 🔬

创建标准化、可复现的 Jupyter 笔记本。

## 功能

### 1. 笔记本结构检查 ✅

验证笔记本是否遵循最佳实践：

```bash
./scripts/check-notebook.sh notebook.ipynb
```

检查内容包括：
- H1 标题
- 导入部分
- 配置/常量
- 数据加载
- 管道（Pipeline）的使用

### 2. 模板 📝

使用以下结构：
1. **标题与目的**
2. **导入**（标准库 → 第三方库 → 本地库）
3. **配置**（所有常量放在顶部）
4. **数据集**（加载、验证、分割）
5. **分析**（数据探索与可视化）
6. **建模**（使用 `sklearn.pipeline.Pipeline`）
7. **评估**（在测试数据上进行性能评估）

## 快速入门

```bash
# Check your notebook
./scripts/check-notebook.sh my-notebook.ipynb

# Follow structure in notebook
# Use Pipeline for all transforms
# Set RANDOM_STATE everywhere
```

## 关键规则

✅ **务必执行**：
- 将所有参数放入配置（Config）部分
- 使用 `sklearn.pipeline.Pipeline`
- 在进行任何数据转换之前先对数据进行分割
- 在所有代码中设置 `random_state`

❌ **禁止**：
- 在代码中使用魔术数字（即不可预测的数值）
- 手动执行数据转换（应使用管道）
- 在整个数据集上进行模型训练（这可能导致数据泄露）

## 作者

本文档改编自 [MLOps 编程课程](https://github.com/MLOps-Courses/mlops-coding-skills)

## 更新日志

### v1.0.0 (2026-02-18)
- 完成从 OpenClaw 到本文档的转换
- 添加了笔记本检查工具