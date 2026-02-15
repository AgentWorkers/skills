---
name: quantum-lab
description: 在现有的虚拟环境 `~/.venvs/qiskit` 中运行位于 `/home/bram/work/quantum_lab` 目录下的 Python 脚本和演示程序。当需要运行 `quant_math_lab.py`、`qcqi_pure_math_playground.py`、`quantum_app.py` 等脚本，或者仓库中的 Jupyter 笔记本时，请使用该虚拟环境（例如，通过 Telegram 或 OpenClaw）。
---

# 量子实验室（Quantum Lab）

## 概述
请在已创建的 qiskit venv 环境中运行 quantum_lab 仓库中的命令。建议使用 `scripts/` 目录中的辅助脚本，以确保 venv 和仓库根目录始终被正确设置。

## 命令列表（完整版）
请将 `<SKILL_DIR>` 替换为该技能安装的文件夹路径（例如：`~/clawd/skills/quantum-lab`）。

- `bash <SKILL_DIR>/scripts/qexec.sh python quant_math_lab.py`
- `bash <SKILL_DIR>/scripts/qexec.sh python qcqi_pure_math_playground.py`
- `bash <SKILL_DIR>/scripts/qexec.sh python quantum_app.py`
- `bash <SKILL_DIR>/scripts/qexec.sh python quantum_app.py self-tests`
- `bash <SKILL_DIR>/scripts/qexec.sh python quantum_app.py playground`
- `bash <SKILL_DIR>/scripts/qexec.sh python quantum_app.py notebook notebooks/SomeNotebook.ipynb`
- `bash <SKILL_DIR>/scripts/qexec.sh python -m quantumapp.server --host 127.0.0.1 --port 8000`

## 命令列表（简写版）
这些命令可用于快速通过 Telegram 或 OpenClaw 进行操作。`gl` 和 `ql` 都是有效的命令，且功能等效。

- `bash <SKILL_DIR>/scripts/gl self-tests`
- `bash <SKILL_DIR>/scripts/gl playground`
- `bash <SKILL_DIR>/scripts/gl app`
- `bash <SKILL_DIR>/scripts/gl lab-tests`
- `bash <SKILL_DIR>/scripts/gl playground-direct`
- `bash <SKILL_DIR>/scripts/gl notebook notebooks/SomeNotebook.ipynb`
- `bash <SKILL_DIR>/scripts/gl web 8000`

## 缩写命令的处理规则
如果用户仅输入了命令的前缀（如 `gl ...` 或 `ql ...`）而没有提供完整路径，系统会自动将其扩展为完整的命令：

- `gl <args>` → `bash <SKILL_DIR>/scripts/gl <args>`
- `ql <args>` → `bash <SKILL_DIR>/scripts/ql <args>`

## 注意事项：
- 仓库根目录的默认值为：`$HOME/work/quantum_lab`（可通过 `QUANTUM_LAB_ROOT` 进行修改）。
- venv 的默认路径为：`~/.venvs/qiskit`（可通过 `VENV_PATH` 进行修改）。
- 如果缺少依赖项，可执行：`bash <SKILL_DIR>/scripts/qexec.sh pip install -r requirements.txt`。