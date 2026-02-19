---
name: mlops-validation-cn
version: 1.0.0
description: 严格的验证流程包括输入验证、代码检查（linting）、测试以及安全性测试。
license: MIT
---
# MLOps 验证 ✅

自动化质量与安全检查。

## 特性

### 1. 提交前钩子（Pre-commit Hooks） 🔧

设置自动化检查：

```bash
cp references/pre-commit-config.yaml ../your-project/.pre-commit-config.yaml
cd ../your-project
pre-commit install
```

在每次提交时执行以下检查：
- Ruff（代码格式检查）
- MyPy（类型检查）
- Bandit（安全检查）

### 2. 测试 fixture 🧪

共享的 pytest 设置：

```bash
cp references/conftest.py ../your-project/tests/
```

提供以下测试 fixture：
- `sample_df` – 测试用数据框
- `temp_dir` – 临时目录
- `sample_config` – 配置字典
- `train_test_split` – 数据预分割工具

## 快速入门

```bash
# Copy pre-commit config
cp references/pre-commit-config.yaml ./.pre-commit-config.yaml

# Install hooks
pre-commit install

# Run manually
pre-commit run --all-files

# Setup test fixtures
cp references/conftest.py tests/

# Run tests
pytest tests/ -v --cov=src
```

## 命令

```bash
# Type check
mypy src/

# Lint
ruff check src/ tests/

# Format
ruff format src/ tests/

# Test
pytest tests/ --cov=src

# Security scan
bandit -r src/
```

## 作者

改编自 [MLOps 编程课程](https://github.com/MLOps-Courses/mlops-coding-skills)

## 更新日志

### v1.0.0 (2026-02-18)
- 完成从 OpenClaw 的迁移
- 添加了提交前配置功能
- 添加了测试 fixture