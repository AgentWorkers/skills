---
name: mlops-automation-cn
version: 1.0.0
description: 任务自动化、容器化、持续集成与持续部署（CI/CD），以及实验跟踪
license: MIT
---
# MLOps自动化 🤖

自动化任务处理、容器管理、持续集成/持续交付（CI/CD）以及机器学习（ML）实验。

## 特点

### 1. 任务执行器（Task Runner）⚡

支持 `justfile` 模板：

```bash
cp references/justfile ../your-project/
```

可用任务：
- `just check` - 运行所有检查
- `just test` - 运行测试
- `just build` - 构建软件包
- `just clean` - 删除临时文件
- `just train` - 运行训练任务

### 2. Docker 🐳

多阶段构建流程：

```bash
cp references/Dockerfile ../your-project/
docker build -t my-model .
docker run my-model
```

优化措施：
- 层级缓存机制（在复制源代码之前进行 uv sync 操作）
- 构建最小化的运行时镜像
- 使用非 root 用户权限运行 Docker 容器

### 3. 持续集成/持续交付（CI/CD，基于 GitHub Actions）🔄

自动化构建流程：

```bash
cp references/ci-workflow.yml ../your-project/.github/workflows/ci.yml
```

在提交代码或创建 Pull Request（PR）时自动执行以下操作：
- 代码风格检查（使用 Ruff 和 MyPy）
- 测试（使用 pytest 和 coverage 工具）
- 构建软件包并生成 Docker 镜像

## 快速入门

```bash
# Setup task runner
cp references/justfile ./

# Setup CI
mkdir -p .github/workflows
cp references/ci-workflow.yml .github/workflows/ci.yml

# Setup Docker
cp references/Dockerfile ./

# Test locally
just check
docker build -t test .
```

## MLflow 跟踪功能

```python
import mlflow

mlflow.autolog()
with mlflow.start_run():
    mlflow.log_param("lr", 0.001)
    model.fit(X, y)
    mlflow.log_metric("accuracy", acc)
```

## 作者

本文档源自 [MLOps 编程课程](https://github.com/MLOps-Courses/mlops-coding-skills)

## 更新日志

### v1.0.0 (2026-02-18)
- 完成从 OpenClaw 的迁移
- 添加了 `justfile` 模板
- 添加了 Dockerfile 文件
- 集成了持续集成（CI）工作流程