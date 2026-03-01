---
name: dependency-update-checker
description: 这是一个命令行工具（CLI），用于检查 `package.json`、`requirements.txt`、`pyproject.toml` 以及其他包文件中的依赖项是否已经过时。
version: 1.0.0
author: skill-factory
metadata:
  openclaw:
    requires:
      bins:
        - python3
        - npm
        - pip
---
# 依赖项更新检查器

## 功能说明

这是一个命令行工具（CLI），通过运行相应的包管理器命令来检测依赖项是否过时。目前支持以下包管理器：
- **npm**：使用 `npm outdated` 命令检查 `package.json` 文件中的依赖项
- **pip**：使用 `pip list --outdated` 命令检查 `requirements.txt` 文件中的依赖项
- **poetry**：如果安装了 `poetry`，则使用 `poetry show --outdated` 命令检查 `pyproject.toml` 文件中的依赖项

该工具会根据当前目录中的文件自动识别需要使用的包管理器，并执行相应的检查。

## 使用场景

- 需要快速了解多个项目中的过时依赖项情况
- 在更新或部署项目之前需要检查依赖项的状态
- 管理使用不同包管理器的多个项目
- 需要一个统一的接口来跨不同的软件生态系统检查依赖项更新

## 使用方法

- 检查当前目录中的依赖项：
  ```bash
  ```bash
python3 scripts/main.py check
```
  ```

- 检查特定的包管理器：
  ```bash
  ```bash
python3 scripts/main.py check --manager npm
python3 scripts/main.py check --manager pip
python3 scripts/main.py check --manager poetry
```
  ```

- 输出格式（JSON）：
  ```bash
  ```bash
python3 scripts/main.py check --format json
```
  ```

## 示例

### 示例 1：检查所有依赖项
```bash
```bash
cd /path/to/project
python3 scripts/main.py check
```
```
输出：
```json
{
  "dependencies": {
    "package1": "1.2.3",
    "package2": "4.5.6",
    // ...
  }
}
```

### 示例 2：JSON 格式输出
```bash
```bash
python3 scripts/main.py check --format json
```
```
输出：
```json
{
  "dependencies": {
    "package1": "1.2.3",
    "package2": "4.5.6",
    // ...
  }
}
```

## 系统要求

- Python 3.x
- **npm**：用于检查 Node.js 项目的依赖项
- **pip**：用于检查 Python 项目的依赖项
- **poetry**：（可选）用于检查使用 `poetry` 生成 `pyproject.toml` 文件的项目的依赖项

## 限制

- 该工具仅作为命令行工具使用，不提供自动集成功能
- 需要确保所需的包管理器已安装，并且其路径（PATH）已设置正确
- 有些包管理器可能不支持 JSON 格式输出（此时会切换为文本解析）
- 仅检查直接依赖项，不检查间接依赖项
- 该工具仅用于检查依赖项的状态，不负责自动更新依赖项
- 在使用私有仓库或自定义包源时可能会出现问题
- 检查远程仓库的性能受网络速度影响
```