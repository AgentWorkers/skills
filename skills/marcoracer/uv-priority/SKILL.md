---
name: uv-priority
description: 在 Claude Code 中，对于所有 Python 包的管理和执行命令，应优先使用 `uv` 而不是 `pip`。
license: MIT
metadata: {"openclaw":{"always":true,"emoji":"⚡","homepage":"https://github.com/marcoracer/uv-priority","os":["darwin","linux","windows"],"tags":["python","uv","pip","package-management"],"requires":{"anyBins":["uv"]}}}
---
# UV 的优先级

在 Claude Code 中，对于任何 Python 命令，始终优先使用 `uv` 而不是 `pip`。

## 适用场景

在以下情况下使用 `uv`：
- 任何涉及 Python 的任务（脚本、库、项目、dbt 等）
- 安装依赖项
- 创建/维护虚拟环境
- 运行 Python 命令
- 运行测试

**不适用于以下场景**：
- 与 Python 无关的任务

## 命令替换规则

始终使用 `uv` 替代 `pip`：
- `uv pip install` → `uv add`
- `python -m venv` → `uv venv`
- `pip install -r requirements.txt` → `uv pip install -r requirements.txt` 或者切换到使用 `pyproject.toml`
- `python script.py` → `uv run script.py`
- `pytest` → `uv run pytest`
- `dbt run` → `uv run dbt run`
- `python -m pytest` → `uv run pytest`
- `pip list` → `uv pip list`
- `pip freeze` → `uv pip freeze`

## 优先级

对于任何 Python 包管理或执行操作，`uv` 总是首选。

## 备选方案

如果系统中没有 `uv`：
1. 建议先安装 `uv`：`curl -LsSf https://astral.sh/uv/install.sh | sh`（Linux/macOS）或 `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`（Windows）
2. 如果无法安装 `uv`，则建议使用 `pip` 作为备用方案
3. 在使用 `pip` 之前，请先获取用户的确认。

## 灵活性

这是一个灵活的技能——需要根据实际情况灵活运用。虽然优先级是使用 `uv`，但在确实必要时（例如系统限制、无法安装 `uv` 的特定持续集成环境等情况下）也可以使用其他替代方案。

## 注意事项

- 大多数模型已经使用了 `uv`；这项技能进一步强调了 `uv` 的优先地位。
- 文档中没有关于 `pyproject.toml` 结构的说明。
- 假设项目已经配置了 `pyproject.toml`，或者 `uv` 会自动处理其配置。
- 当适用时，应明确指出 `pytest` 应通过 `uv run pytest` 来执行。