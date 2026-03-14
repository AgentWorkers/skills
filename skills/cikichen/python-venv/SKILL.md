---
name: python-venv
description: "Python环境管理技巧：能够自动检测项目类型及已存在的环境，并根据使用频率推荐合适的开发环境。尽量减少干扰，仅在必要时才提示用户进行相关操作。"
---
# Python环境管理技巧

## 核心原则

1. **重用现有环境** - 不要重新创建，而是重用现有的虚拟环境。
2. **根据项目类型自动选择工具** - 根据`lock`文件自动选择合适的工具。
3. **按流行度推荐工具**：`uv` > `pip` > `conda` > `venv`。
4. **尽量减少干扰** - 只在必要时才询问用户。

---

## 工具流行度排名

| 优先级 | 工具 | 适用场景 |
|------|------|---------|
| 🥇 | `uv` | 新项目，快速安装 |
| 🥈 | `pip` | 兼容性优先 |
| 🥉 | `conda` | 数据科学项目，需要特定版本 |
| 4 | `venv` | 内置环境，无需额外安装 |
| 5 | `poetry` | 如果存在`poetry.lock`文件 |
| 6 | `pipenv` | 如果存在`Pipfile`文件 |

---

## 决策流程

```
┌─────────────────────────────────────┐
│  Detect project dependency files     │
└─────────────────────────────────────┘
              ↓
    ┌─────────┴─────────┐
    ↓                   ↓
  Clear decision       Unclear
    ↓                   ↓
  Use directly     Detect existing env
                        ↓
                  ┌─────┴─────┐
                  ↓           ↓
              Has env        No env
                  ↓           ↓
              Reuse      Assess complexity
                            ↓
                  ┌─────────┴─────────┐
                  ↓                   ↓
              Simple task       Needs deps
                  ↓                   ↓
            System Python      Recommend uv/conda
```

---

## 1. 明确的情况下（直接执行，无需询问）

当检测到以下文件时，直接使用相应的工具：

| 检测到的文件 | 执行命令 |
|--------------|---------|
| 存在`uv.lock` | `uv sync` 或 `uv pip install -r requirements.txt` |
| 存在`poetry.lock` | `poetry install` |
| 存在`environment.yml` | `conda env create -f environment.yml` |
| 存在`Pipfile.lock` | `pipenv install` |

---

## 2. 检测是否存在现有环境（优先重用）

**重用示例：**
```
Detected existing .venv/ directory
→ Activate: source .venv/bin/activate
→ Run: uv pip install <package>
```

---

## 3. 情况复杂时（需要评估）

| 情况 | 应采取的行动 |
|----------|--------|
| 仅使用标准库，没有第三方库 | 使用系统自带的Python环境（`python3`） |
| 需要简单安装依赖项 | 使用系统自带的Python环境（临时创建） |
| 有`requirements.txt`文件 | 推荐使用`uv` > `pip` > `venv` |
| 有`pyproject.toml`文件 | 推荐使用`uv` > `pip` |
| 多文件项目，需要隔离环境 | 推荐使用`uv` |

---

## 4. 何时询问用户（仅在这些情况下）

✅ **需要询问用户的情况**：
1. 项目为空且需要安装第一个依赖项时。
2. 项目同时存在`requirements.txt`和`pyproject.toml`文件时。
3. 用户明确要求使用其他工具（例如：“我想要使用`conda`”。

❌ **无需询问用户的情况**：
- 存在`uv.lock`文件但用户未指定工具。
- 存在`.venv`目录。
- 仅仅是普通的`pip`安装任务。

---

## 推荐使用的工具（无明确规定的情况）

```
First: uv
  ├── uv venv (create)
  ├── uv pip install (install)
  └── uv sync (sync)

Backup: pip
  ├── python3 -m venv .venv
  └── pip install

Special: conda
  ├── conda create -n envname python=x.x
  └── conda env create
```

---

## 检测命令

```bash
# Check available tools
which uv
which conda
which pip
which python3

# Check project files
ls -la *.lock pyproject.toml requirements.txt environment.yml Pipfile 2>/dev/null

# Check existing environments
ls -la .venv/ venv/ env/ 2>/dev/null
conda info --envs 2>/dev/null

# Check current environment
echo $VIRTUAL_ENV
echo $CONDA_PREFIX
```

---

## 交互示例（仅在需要时显示）

```
🔍 Detection result:
- Project file: pyproject.toml
- Existing env: None
- Recommended: uv (fastest)

Running: uv pip install <package>
```

```
🔍 Detection result:
- Project file: requirements.txt
- Existing env: None
- Recommended: uv

Available options:
1) uv (recommended) - faster
2) pip - better compatibility
3) venv - uses stdlib
4) conda - if specific version needed

Enter option or press Enter to use recommended:
```

---

## 快速命令参考

| 功能 | `uv` | `pip` | `conda` | `venv` |
|--------|-----|-----|-------|------|
| 创建环境 | `uv venv` | - | `conda create` | `python3 -m venv` |
| 安装包 | `uv pip install` | `pip install` | `conda install` | `pip install` |
| 安装依赖项 | `uv sync` | `pip install -r` | `conda env create` | `pip install -r` |
| 激活环境 | （自动执行） | （自动执行） | `conda activate` | `source venv/bin/activate` |

---

## 核心原则

**“多执行，少询问”** - 在能够直接决定的情况下直接执行操作，只有在确实不清楚时才询问用户。