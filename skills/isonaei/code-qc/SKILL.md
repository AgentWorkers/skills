---
name: code-qc
description: 对任何代码库执行结构化的质量控制审计。当需要对项目的代码质量进行质量控制（QC）、审计或审查时，可以使用此工具。该工具支持 Python、TypeScript、GDScript 以及各类通用项目。它会生成一份标准化的报告，其中包含 PASS、WARN 和 FAIL 的评估结果，涵盖测试、导入语句、类型检查、静态分析、冒烟测试（smoke tests）以及代码文档等方面。同时，该工具也可用于比较不同时期的质量控制结果。
---
# 代码质量控制（Code QC）

这是一种针对代码库的结构化质量审计工具。它将静态分析任务委托给相应的工具（如 ruff、eslint、gdlint），并重点关注人工智能能够提供的功能：语义理解、模块间的一致性以及动态测试的生成。

## 快速入门

1. 确定项目类型（请参阅相应语言的配置文件）。
2. 如果存在 `.qc-config.yaml` 文件，请加载它（用于自定义阈值或排除项）。
3. 运行包含 8 个阶段的审计流程（或使用 `--quick` 选项运行部分阶段）。
4. 生成包含审计结果的报告。
5. 保存审计结果作为基准，以便后续比较。

## 配置（`.qc-config.yaml`）

这是一个可选的项目级配置文件，适用于单仓库项目及自定义设置：

```yaml
# .qc-config.yaml
thresholds:
  test_failure_rate: 0.05    # >5% = FAIL, 0-5% = WARN, 0% = PASS
  lint_errors_max: 0         # Max lint errors before FAIL
  lint_warnings_max: 50      # Max warnings before WARN
  type_errors_max: 0         # Max type errors before FAIL (strict by default)

exclude:
  dirs: [vendor, third_party, generated]
  files: ["*_generated.py", "*.pb.go"]

changed_only: false          # Only check git-changed files (CI mode)
fail_fast: false             # Stop on first failure
quick_mode: false            # Only run Phase 1, 3, 3.5, 6

languages:
  python:
    min_coverage: 80
    ignore_rules: [T201]     # Allow print in this project
  typescript:
    strict_mode: true        # Require tsconfig strict: true
    ignore_rules: []         # eslint rules to ignore
  gdscript:
    godot_version: "4.2"
```

## 执行模式

| 模式          | 运行的阶段          | 适用场景                |
|----------------|------------------|----------------------|
| 完整模式（默认）      | 所有 8 个阶段        | 全面审计                |
| `--quick`       | 第 1、3、3.5、6 阶段      | 快速检查                |
| `--changed-only`   | 所有阶段（仅检查更改的部分） | 用于持续集成（CI）中的拉取请求检查 |
| `--fail-fast`    | 所有阶段          | 快速发现第一个问题             |
| `--fix`       | 第 3 阶段（包含自动修复）     | 应用自动修复功能             |

## 各阶段概述

| 阶段编号 | 阶段名称        | 主要内容                | 使用的工具                |
|---------|------------------|----------------------|----------------------|
| 1       | 测试套件        | 运行现有的测试并统计代码覆盖率    | pytest --cov / jest --coverage       |
| 2       | 导入完整性检查    | 验证所有模块是否能够正确导入       | `scripts/import_check.py`         |
| 3       | 静态分析        | 使用相应的工具进行代码检查       | ruff / eslint / gdlint         |
| 3.5      | 类型检查        | 静态类型验证             | mypy / tsc --noEmit         | （GDScript 除外）         |
| 4       | 动态测试        | 通过人工智能生成测试用例来验证业务逻辑 | （针对每个项目生成）         |
| 5       | 用户界面/前端验证    | 验证 UI 组件是否能够正确加载       | （根据框架不同而异）           |
| 6       | 文件一致性检查    | 检查语法错误及 Git 代码状态       | `scripts/syntax_check.py`         |
| 7       | 文档检查        | 检查文档字符串及文档的准确性     | `scripts/docstring_check.py`         |

## 各阶段详细信息

### 阶段 1：测试套件

运行项目的测试套件，并统计代码覆盖率。系统会自动检测测试运行器：

**记录内容：** 总测试次数、通过次数、失败次数、错误次数、跳过的测试次数、测试耗时以及代码覆盖率。

**判断标准：**
- 未找到任何测试用例 → **跳过此阶段**（不视为失败；可能项目仅包含配置文件）
- 失败率为 0% → **通过**  
- 失败率 ≤ 阈值（默认为 5%） → **警告**  
- 失败率 > 阈值 → **失败**  

**代码覆盖率报告（Python）：**  
```bash
pytest --cov=<package> --cov-report=term-missing --cov-report=json
```

### 阶段 2：导入完整性检查（Python/GDScript）

**Python：** 在项目根目录下运行 `scripts/import_check.py`。

**GDScript：** 验证场景文件或预加载引用是否有效（详见 `gdscript-profile.md`）。

#### 导入失败的严重性分类

根据以下规则对导入失败进行分类：

| 导入文件模式 | 分类        | 说明                          |
|------------|-------------|--------------------------------------------|
| `__init__.py`, `main.py`, `app.py`, `cli.py` | **关键**      | 核心入口文件                        |
| `src/`, `lib/` 目录下的模块或顶级包   | **关键**      | 核心功能模块                        |
| `*_test.py`, `test_*.py`, `conftest.py` | **非关键**      | 测试相关辅助模块                        |
| `examples/`, `scripts/`, `tools/` 目录下的模块 | **非关键**      | 辅助代码模块                        |
| 导入语句中提及 `cuml`, `triton`, `tensorrt` | **非关键**      | 与硬件相关的依赖                    |
| 导入语句中提及缺失的系统库       | **非关键**      | 与环境相关的依赖                    |
| 依赖项在 `[project.optional-dependencies]` 中列出 | **非关键**      | 明确声明为可选依赖                    |

### 阶段 3：静态分析

**请勿使用 grep**，应使用相应语言的标准代码检查工具。

#### 标准模式  
```bash
# Python
ruff check --select E722,T201,B006,F401,F841,UP,I --statistics <project>

# TypeScript  
npx eslint . --format json

# GDScript
gdlint <project>
```

#### 自动修复模式（`--fix`）

当使用 `--fix` 选项时，系统会自动修复检测到的问题：

**注意：** 在应用自动修复后，需要重新运行检查以报告那些无法自动修复的问题。

### 阶段 3.5：类型检查（新功能）

在进行运行时检查之前，先进行静态类型分析。

**Python：**  
```bash
mypy <package> --ignore-missing-imports --no-error-summary
# or if pyproject.toml has [tool.pyright]:
pyright <package>
```

**TypeScript：**  
```bash
npx tsc --noEmit
```

**GDScript：** Godot 4 支持内置的静态类型检查功能，但暂无独立的类型检查工具。需要手动估算代码的类型覆盖率：

**使用 `gdscript-profile.md` 中的 `estimate_type_coverage()` 函数来计算每个文件的类型覆盖率：**  
```python
# From gdscript-profile.md
def estimate_type_coverage(gd_file: str) -> float:
    """Count typed vs untyped declarations."""
    # See full implementation in gdscript-profile.md
```

同时，请注意 `@warning_ignore` 注解，这些注释可能会掩盖类型错误。

**记录内容：** 总错误数及错误类型。

### 阶段 4：动态测试（业务逻辑）

测试项目的 **后端/核心功能**，不包括 UI 组件（这部分在阶段 5 中进行测试）。

**API 发现规则：**
1. **入口点：** 查找 `main()`, `cli()`, `app`, `create_app()`, `__main__.py` 等函数。
2. **服务层：** 查找名为 `*Service`, `*Manager`, `*Handler` 的类或模块。
3. **公共 API：** 检查 `__init__.py` 文件中的 `__all__` 导出项。
4. **FastAPI/Flask：** 查找路由装饰器（如 `@app.get`, `@router.post`）。
5. **CLI：** 查找 `@app.command()` 等装饰器。
6. **SDK：** 查找没有 `_` 前缀的公共方法。

**对于每个检测到的 API，生成一个简单的测试用例：**
```python
def smoke_test_user_service():
    """Test UserService basic CRUD."""
    from myproject.services.user import UserService
    svc = UserService(db=":memory:")
    user = svc.create(name="test")
    assert user.id is not None
    fetched = svc.get(user.id)
    assert fetched.name == "test"
    return "PASS"
```

**测试指南：**
- 导入相关模块并创建实例。
- 使用内存或临时资源（例如 `:memory:`、`tempdir`）。
- 每个测试用例的运行时间应小于 5 秒。
- 确保能够捕获并清晰地报告异常。

### 阶段 5：用户界面/前端验证

单独测试 UI 组件的功能。

| 使用的框架 | 测试方法                |
|-----------|----------------------|
| **Gradio** | `from project.ui import create_ui`（不调用 `launch()`） |
| **Streamlit** | `streamlit run app.py --headless`（无界面显示） |
| **PyQt/PySide** | 设置 `QT_QPAPLATFORM=offscreen` 并导入相关组件 |
| **React** | `npm run build`（构建成功）             |
| **Vue** | `npm run build`（构建成功）             |
| **Godot** | 场景文件能够正常解析，所需脚本存在             |
| **CLI** | 所有子命令的执行结果为 0（表示成功）           |

**功能区分：** 阶段 4 主要验证逻辑是否正确执行；阶段 5 主要验证 UI 是否能够正确渲染。

### 阶段 6：文件一致性检查

运行 `scripts/syntax_check.py` 以检查所有源文件的语法错误。

> **注意：** 阶段 2 主要检查代码的 **运行时** 导入行为（包括初始化代码）；阶段 6 主要检查代码的 **静态** 语法正确性。两者都是必要的：一个文件可能语法正确但无法导入（例如缺少依赖），或者相反（某个从未被导入的模块存在语法错误）。

**同时检查 Git 代码状态：**  
```bash
git status --short      # Should be clean (or report uncommitted changes)
git diff --check        # No conflict markers
```

### 阶段 7：文档检查

运行 `scripts/docstring_check.py`（默认会检查 `__init__.py` 文件）。

此外，还需要验证以下内容：
- 是否存在 `README.md` 文件且内容非空。
- 如果有引用，相关文档（如 `CHANGELOG`, `CONTRIBUTING.md`）是否存在。
- 文档中是否没有过时的待办事项标记（表明文档已完成更新）。

## 审计结果判断逻辑

```
# Calculate test failure rate
failure_rate = test_failures / total_tests

# Default thresholds (override in .qc-config.yaml)
FAIL_THRESHOLD = 0.05  # 5%
WARN_THRESHOLD = 0.00  # 0%
TYPE_ERRORS_MAX = 0    # Default: strict (any type error = FAIL)

# Verdict determination
if any([
    failure_rate > FAIL_THRESHOLD,
    critical_import_failure,
    type_check_errors > thresholds.type_errors_max,  # Configurable threshold
    lint_errors > thresholds.lint_errors_max,
]):
    verdict = "FAIL"
elif any([
    0 < failure_rate <= FAIL_THRESHOLD,
    optional_import_failures > 0,
    lint_warnings > thresholds.lint_warnings_max,
    missing_docstrings > 0,
    smoke_test_failures > 0,
]):
    verdict = "PASS WITH WARNINGS"
else:
    verdict = "PASS"
```

## 基线比较

将审计结果保存到 `.qc-baseline.json` 文件中：

```json
{
  "timestamp": "2026-02-15T15:00:00Z",
  "commit": "abc123",
  "verdict": "PASS WITH WARNINGS",
  "config": {
    "mode": "full",
    "thresholds": {"test_failure_rate": 0.05}
  },
  "phases": {
    "tests": {"total": 134, "passed": 134, "failed": 0, "coverage": 87.5},
    "imports": {"total": 50, "failed": 0, "optional_failed": 1, "critical_failed": 0},
    "types": {"errors": 0, "warnings": 5},
    "lint": {"errors": 0, "warnings": 12, "fixed": 8},
    "smoke": {"total": 14, "passed": 14},
    "docs": {"missing_docstrings": 3}
  }
}
```

在后续的审计中，报告各项指标的变化情况：

```
Tests:      134 → 140 (+6 ✅)
Coverage:   87% → 91% (+4% ✅)
Type errors: 0 → 0 (✅)
Lint warnings: 12 → 5 (-7 ✅)
```

## 报告输出

报告结果以三种格式生成：
1. **Markdown 格式（`qc-report.md`）**：供人类阅读的详细报告。
2. **JSON 格式（`.qc-baseline.json`）**：供持续集成（CI）或比较使用。
3. **摘要格式（聊天消息）**：简洁的 10 行摘要，适用于 Discord/Slack 等平台。

### 概要格式示例

```
📊 QC Report: my-project @ abc123
Verdict: ✅ PASS WITH WARNINGS

Tests:    134/134 passed (100%) | Coverage: 87%
Types:    0 errors
Lint:     0 errors, 12 warnings
Imports:  50/50 (1 optional failed)
Smoke:    14/14 passed

⚠️ Warnings:
- 3 missing docstrings
- 12 lint warnings (run with --fix)
```

## 语言特定配置文件

在运行审计之前，请阅读相应的配置文件：
- **Python**：`references/python-profile.md`
- **TypeScript**：`references/typescript-profile.md`
- **GDScript**：`references/gdscript-profile.md`
- **通用配置**：`references/general-profile.md`