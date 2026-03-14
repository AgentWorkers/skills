---
name: python
description: 使用 Python 进行实际项目的设置、依赖项的安装、脚本的执行以及环境问题的排查，同时提供安全的默认配置。适用于需要处理 `pyproject.toml` 或 `requirements.txt` 文件、虚拟环境搭建、运行 Python 脚本/测试、基础打包操作，或解决常见 Python 错误（如解释器不匹配、`pip` 解决器冲突、模块缺失、构建失败）的情况。
metadata:
  openclaw:
    emoji: "🐍"
    requires:
      bins: ["python3"]
      anyBins: ["pip", "pip3"]
    install:
      - id: "brew"
        kind: "brew"
        formula: "python"
        bins: ["python3"]
        label: "Install Python + pip (brew)"
      - id: "apt"
        kind: "apt"
        package: "python3-pip"
        bins: ["pip3"]
        label: "Install pip (apt)"
---
# Python

使用此技能可确保 Python 工作流程在本地/开发环境中具有可重复性和低风险。

## 安全默认设置

- 更倾向于使用项目级别的虚拟环境（`.venv`），而非全局安装。
- 建议使用 `python3 -m pip ...` 来避免解释器和 pip 的不匹配问题。
- 在安装之前检查依赖文件（`requirements*.txt`、`pyproject.toml`）。
- 避免在未经用户批准的情况下执行未知的设置脚本或随机安装脚本。

## 标准工作流程

1. 检测当前环境：

```bash
python3 --version
python3 -c "import sys; print(sys.executable)"
{baseDir}/scripts/python_env_tool.py doctor
```

2. 创建或刷新虚拟环境（venv）：

```bash
{baseDir}/scripts/python_env_tool.py bootstrap --venv .venv --requirements requirements.txt
```

3. 安装项目包（如果存在 `pyproject.toml`）：

```bash
{baseDir}/scripts/python_env_tool.py install --venv .venv --editable
```

4. 从虚拟环境的解释器中运行测试/工具：

```bash
.venv/bin/python -m pytest -q
.venv/bin/python -m pip list --outdated
```

## 任务指南

```bash
# Install specific packages into venv
{baseDir}/scripts/python_env_tool.py install --venv .venv --package requests --package pydantic

# Install from requirements file
{baseDir}/scripts/python_env_tool.py install --venv .venv --requirements requirements-dev.txt

# Recreate corrupted venv from scratch
{baseDir}/scripts/python_env_tool.py bootstrap --venv .venv --recreate --requirements requirements.txt
```

## 故障排除规则

- 如果出现 `ModuleNotFoundError`，请确认命令是通过 `.venv/bin/python` 来执行的，然后重新安装依赖项。
- 如果系统使用的是外部管理的环境（`externally-managed-environment`），请停止全局安装尝试，改用虚拟环境。
- 如果因本地依赖项导致构建失败，请升级 `pip setuptools wheel`，然后再试。
- 如果系统中安装了多个 Python 版本，请在修复问题之前始终打印并确认 `sys.executable` 的值。

## 集成辅助工具

使用这些辅助工具来确保环境设置的重复性和故障诊断的便利性：

```bash
{baseDir}/scripts/python_env_tool.py --help
{baseDir}/scripts/python_env_tool.py doctor
```