---
name: code-refactor-for-reproducibility
description: >
  **使用场景：**  
  在重构研究代码以供发表、为现有分析脚本添加文档、创建可复现的计算工作流程，或准备代码与合作者共享时使用。该工具可将研究代码转换为适合发表的、可复现的工作流程；同时会添加文档、实现错误处理机制、制定环境规范，并确保科学出版物中的计算过程具有可复现性。
allowed-tools: "Read Write Bash Edit"
license: MIT
metadata:
  skill-author: AIPOCH
  version: "1.0"
---
# 研究代码可复现性重构工具

## 工作流程概述

在对研究代码库进行重构时，请按照以下顺序操作：

1. **分析** — 识别现有代码中的可复现性问题
2. **重构** — 添加文档注释、参数化处理和错误处理机制
3. **指定运行环境** — 固定依赖关系并创建环境配置文件
4. **验证** — 运行测试，确保代码行为未发生改变

---

## 第一步：分析代码中的可复现性问题

请仔细阅读每个源文件，检查是否存在以下问题。在做出任何修改之前，务必记录下发现的问题。

**检查清单：**
- 缺少文档注释（docstrings）
- 硬编码的绝对路径
- 未设置随机种子
- 仅使用 `except:` 语句处理异常（缺乏详细的错误处理）
- 未固定的导入语句（可能导致代码依赖关系混乱）
- 未解释的魔法数字（即没有明确来源的常量）

**示例 — 手动检测问题：**

```python
import ast, pathlib

def find_hardcoded_paths(source: str) -> list[str]:
    """Return string literals that look like absolute paths."""
    tree = ast.parse(source)
    return [
        node.s for node in ast.walk(tree)
        if isinstance(node, ast.Constant)
        and isinstance(node.s, str)
        and node.s.startswith("/")
    ]

source = pathlib.Path("analysis.py").read_text()
print(find_hardcoded_paths(source))
```

---

## 第二步：按照最佳实践进行重构

请根据实际情况应用相应的改进措施。务必先备份原始代码。

### 2a. 添加文档注释

```python
# Before
def load_data(path):
    import pandas as pd
    return pd.read_csv(path)

# After
def load_data(path: str) -> "pd.DataFrame":
    """Load a CSV dataset from disk.

    Parameters
    ----------
    path : str
        Path to the CSV file (relative to project root).

    Returns
    -------
    pd.DataFrame
        Raw dataset with original column names preserved.
    """
    import pandas as pd
    return pd.read_csv(path)
```

### 2b. 对硬编码的值进行参数化处理

```python
from pathlib import Path
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, default=Path("data/raw.csv"))
    parser.add_argument("--output", type=Path, default=Path("results/"))
    return parser.parse_args()

args = parse_args()
df = pd.read_csv(args.data)
args.output.mkdir(parents=True, exist_ok=True)
```

### 2c. 设置随机种子

```python
import random
import numpy as np

SEED = 42  # document this constant at module level

random.seed(SEED)
np.random.seed(SEED)

# scikit-learn
from sklearn.ensemble import RandomForestClassifier
clf = RandomForestClassifier(random_state=SEED)

# PyTorch
import torch
torch.manual_seed(SEED)
torch.backends.cudnn.deterministic = True
```

### 2d. 添加错误处理和日志记录功能

```python
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

def load_data(path: Path) -> "pd.DataFrame":
    """Load dataset with validation."""
    import pandas as pd
    if not path.exists():
        raise FileNotFoundError(f"Data file not found: {path}")
    logger.info("Loading data from %s", path)
    df = pd.read_csv(path)
    if df.empty:
        raise ValueError(f"Loaded dataframe is empty: {path}")
    logger.info("Loaded %d rows, %d columns", *df.shape)
    return df
```

---

## 第三步：生成环境配置文件

请参考 `references/environment-setup.md`，了解完整的 Dockerfile 和 Conda 环境模板。

### requirements.txt (pip)

```bash
pip install pipreqs
pipreqs src/ --output requirements.txt --force
```

验证重构效果：
```bash
python -m venv .venv_test && source .venv_test/bin/activate
pip install -r requirements.txt
python -c "import pandas, numpy, sklearn"
deactivate && rm -rf .venv_test
```

### environment.yml (Conda)

```yaml
name: my-research-env
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.9
  - numpy=1.24.3
  - pandas=2.0.1
  - scikit-learn=1.2.2
  - matplotlib=3.7.1
  - pip:
    - some-pip-only-package==0.5.0
```

```bash
conda env create -f environment.yml
conda activate my-research-env
```

---

## 第四步：编写文档

### 创建 `README.md` 文件

请生成一个 `README.md` 文件，其中至少应包含以下内容：

```markdown
## Requirements
<!-- List Python version and key packages with versions -->

## Installation
```
bash
conda env create -f environment.yml
conda activate my-research-env
```

## Data
<!-- Describe input data format, source, and where to place files -->

## Running the Analysis
```
python main.py --data data/raw.csv --output results/
```

## Expected Outputs
<!-- Describe files created and how to interpret them -->

## Reproducing Results
- Random seed: 42 (set in `config.py`)
- Hardware: results validated on CPU; GPU results may differ slightly
```

---

## 第五步：验证代码的可复现性

在完成所有修改后，请确保代码行为未发生改变：

```bash
# 1. Run the full pipeline and capture output checksums
python main.py --data data/raw.csv --output results/
md5sum results/*.csv > checksums_refactored.md5
diff checksums_original.md5 checksums_refactored.md5

# 2. Run unit tests
pytest tests/ -v --tb=short

# 3. Confirm determinism across two clean runs
python main.py --output results_run1/
python main.py --output results_run2/
diff -r results_run1/ results_run2/
```

**可复现性验证清单：**
- [ ] 输出文件的校验和与重构前的基准值一致
- [ ] 所有测试均通过
- [ ] 代码流程运行两次后产生的结果完全相同
- [ ] `requirements.txt` 和 `environment.yml` 能在新的环境中正常安装
- [ ] 源代码中不再包含硬编码的绝对路径
- [ ] 随机种子已设置并进行了记录
- [ ] 所有公开函数都配有文档注释
- [ ] `README` 文件中提供了完整的复现步骤说明

---

## 最佳实践总结

| 最佳实践 | 描述 |
|---------|---------|
| 仅使用相对路径 | 避免使用硬编码的绝对路径 |
| 固定依赖版本 | 确保依赖关系的稳定性 |
| 为所有公开函数添加文档注释 | 便于他人理解代码功能 |
| 根据基准值验证输出结果 | 确保代码行为的稳定性 |
| 自动化环境配置 | 提高开发效率 |

## 参考资料

- `references/guide.md` — 综合用户指南
- `references/environment-setup.md` — Dockerfile 和完整的环境配置模板
- `references/examples/` — 可供参考的代码示例
- `references/api-docs/` — 完整的 API 文档

---

**技能 ID**: 455 | **版本**: 1.0 | **许可证**: MIT