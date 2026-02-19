---
name: mlops-initialization-cn
version: 1.0.0
description: 使用 uv/git/VS Code 的最佳实践进行 MLOps 项目初始化
license: MIT
---
# MLOps 项目初始化 🚀

使用现代的Python工具链来设置新的MLOps项目。

## 特点

### 1. 项目初始化 📦

创建完整的项目结构：

```bash
./scripts/init-project.sh my-mlops-project
```

生成以下内容：
- `src/` 目录结构
- 包含 `uv` 的 `pyproject.toml` 文件
- `.gitignore` 文件（用于指定Python/MLOps相关的文件和目录）
- `.vscode/settings.json` 文件（用于配置VS Code）
- Git仓库

### 2. 配置模板 📋

复制参考配置文件：

```bash
# pyproject.toml template
cp references/pyproject.toml ../your-project/

# VS Code settings
cp references/vscode-settings.json ../your-project/.vscode/
```

## 快速入门

```bash
# Initialize new project
./scripts/init-project.sh my-project
cd my-project

# Add dependencies
uv add pandas numpy scikit-learn

# Sync environment
uv sync

# Verify
uv run python -c "import sys; print(sys.executable)"
```

## 您将获得的内容

- ✅ `src/` 目录下的项目结构
- ✅ 已锁定的依赖项（`uv.lock` 文件）
- 已配置的Ruff和MyPy工具
- 已设置的VS Code环境
- Git仓库

## 参考资料

- `references/pyproject.toml` - 完整的配置示例
- `references/vscode-settings.json` - VS Code的配置文件

## 作者

本文档改编自 [MLOps编程课程](https://github.com/MLOps-Courses/mlops-coding-skills)

## 更新日志

### v1.0.0 (2026-02-18)
- 首次将项目转换为OpenClaw格式
- 添加了项目初始化脚本
- 添加了参考配置文件