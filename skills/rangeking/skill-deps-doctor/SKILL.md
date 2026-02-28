---
name: Skill Deps Doctor
description: "跨平台技能依赖检查工具——用于预先检测缺失的二进制文件、版本不匹配问题、系统库、中文/日文/韩文字体、Playwright/Chromium运行时环境以及项目级别的依赖关系。在运行相关技能之前使用该工具，可以有效避免运行时出现的依赖问题。"
metadata: {"clawdbot": {"emoji": "🧰", "requires": {"bins": ["python3", "skill-deps-doctor"]}, "install": [{"id": "skill-deps-doctor", "kind": "pip", "package": "skill-deps-doctor", "bins": ["skill-deps-doctor"], "label": "Install skill-deps-doctor (package: skill-deps-doctor) from PyPI"}]}}
---
# 🧰 技能依赖检查工具（Skill Deps Doctor）

> **作为 `openclaw doctor` 的补充工具** — `doctor` 主要用于检查网关配置和服务；而本工具则专注于检测技能运行时的依赖项（包括二进制文件、版本信息、库文件以及字体文件）。

使用该工具可以在技能运行时出现错误之前，提前发现缺失或损坏的依赖项。

## 检查内容：

- 🔎 **二进制文件的是否存在**：会扫描 `skills/*/SKILL.md` 文件中声明的 `requires.bins` 文件，确保它们存在于 `$PATH` 环境变量指定的路径下。
- 📌 **版本要求**：检查 Node.js 和 Python 的版本是否满足最低要求（例如 `node>=18`、`python3>=3.10`），并会实际验证版本是否符合要求。
- 🧩 **共享库**：通过 `ldconfig`（Linux 系统）检测 Playwright 和 Chromium 所依赖的本地库文件。
- 🔤 **中文（CJK）字体**：确保系统安装了正确的字体文件，以避免 PDF 文档显示乱码的问题。
- 🔗 **间接依赖项**：例如，当使用 Playwright 时，会检查其依赖的第三方库文件（如 `.so` 文件）。
- 📦 **项目配置文件**：通过 `--check-dir` 参数检查项目的配置文件（如 Node.js 的 `package.json`、Python 的 `pyproject.toml` 或 `requirements.txt`、Docker 的 `Dockerfile`）。
- 🎚️ **Playwright 检测**：包括 Node.js 和 Python 的版本检测，以及 Chromium 的无头浏览器启动测试。
- 📦 **依赖项配置文件**：支持多种配置模式（`--profile slidev`、`--profile whisper`、`--profile pdf-export`）。
- 🔌 **插件系统**：通过 Python 脚本来检测第三方插件及其依赖关系。

## 安装

```bash
pip install skill-deps-doctor
```

为了兼容性，旧的命令 `skill-deps-doctor` 仍然可以被使用。

## 使用方法：

### 基本检查

```bash
skill-deps-doctor --skills-dir /path/to/workspace/skills
```

### 扫描整个项目目录

```bash
skill-deps-doctor --skills-dir ./skills --check-dir ./project --probe
```

### 对整个 Monorepo 进行递归扫描

```bash
skill-deps-doctor --skills-dir ./skills --check-dir ./monorepo --recursive
```

### 配置不同的依赖项检查模式

```bash
skill-deps-doctor --skills-dir ./skills --profile slidev --profile pdf-export
skill-deps-doctor --skills-dir ./skills --list-profiles
```

### 生成修复脚本

```bash
skill-deps-doctor --skills-dir ./skills --fix > fix.sh
```

### 生成依赖项关系图

```bash
skill-deps-doctor --skills-dir ./skills --graph tree
skill-deps-doctor --skills-dir ./skills --graph dot | dot -Tsvg -o deps.svg
```

### 创建跨平台的修复方案

```bash
skill-deps-doctor --skills-dir ./skills --platform-matrix
```

### 生成 JSON 格式的输出文件（适用于持续集成）

```bash
skill-deps-doctor --skills-dir ./skills --json
```

### 生成环境快照并用于回归测试控制

```bash
# Save baseline
skill-deps-doctor --skills-dir ./skills --snapshot baseline.json

# Gate on new issues
skill-deps-doctor --skills-dir ./skills --baseline baseline.json --fail-on-new
# Exit: 0 = pass, 2 = errors, 3 = new findings vs baseline
```

### 验证配置文件的结构和插件契约

```bash
skill-deps-doctor --skills-dir ./skills --validate-hints
skill-deps-doctor --skills-dir ./skills --validate-plugins
```

### 自定义检查规则

```bash
skill-deps-doctor --skills-dir ./skills --hints-file my-hints.yaml
```

### 显示详细信息或简化输出

```bash
skill-deps-doctor --skills-dir ./skills -v        # Show all (including info)
skill-deps-doctor --skills-dir ./skills -q        # Errors only
skill-deps-doctor --skills-dir ./skills --no-plugins  # Skip third-party plugins
```

### 提供备用执行方式（适用于仓库或开发环境）

```bash
python {baseDir}/scripts/skill-deps-doctor.py --skills-dir ./skills
```

## 注意事项：

- **Linux**：依赖库的检查通过 `ldconfig` 完成；字体文件的检查使用 `fc-list`；会根据宿主系统的包管理器（如 `apt`、`yum`、`apk`、`pacman`）自动调整检查逻辑。
- **macOS / Windows**：同样支持二进制文件、版本和字体的检查；Playwright 的相关检查依赖于特定的检测脚本（`--probe` 参数）。
- **持续集成（CI）集成**：使用 `--json` 选项生成机器可读的输出格式；通过 `--snapshot` 和 `--baseline --fail-on-new` 选项实现回归测试的控制。