---
description: 通过分析项目结构和配置，自动生成全面的 README.md 文件。
---

# README 生成器

该工具会分析项目目录，并生成一份完整且实用的 README.md 文件。

## 使用要求

- 需要具备对目标项目文件系统的访问权限
- 不需要使用任何 API 密钥或外部服务

## 使用说明

### 第一步：扫描项目目录

```bash
# Project structure (exclude noise)
find . -maxdepth 3 -not -path '*/node_modules/*' -not -path '*/.git/*' -not -path '*/__pycache__/*' -not -path '*/venv/*' -not -path '*/.venv/*' | head -80

# Package metadata
cat package.json 2>/dev/null || cat pyproject.toml 2>/dev/null || cat Cargo.toml 2>/dev/null || cat go.mod 2>/dev/null

# Available scripts/commands
jq '.scripts' package.json 2>/dev/null

# License detection
ls LICENSE* LICENCE* 2>/dev/null

# Entry points
ls src/index.* src/main.* main.* app.* cli.* 2>/dev/null
```

### 第二步：读取关键文件（每个文件的前 50 行）
- 主入口文件
- 配置文件（如 `tsconfig`、`pyproject` 等）
- 现有的 README 文件（以保留其编写意图）

### 第三步：根据以下结构生成 README 文件

```markdown
# Project Name
Brief description.

## Features
- Key feature list

## Installation
Steps to install (npm install, pip install, etc.)

## Usage
CLI examples and/or programmatic usage with code blocks.

## API Reference (if applicable)
Document exported functions/endpoints.

## Project Structure
Tree view with brief descriptions of key files.

## Development
Clone, install, test, contribute steps.

## License
Detected license type.
```

### 第四步：保存生成的结果
- 如果项目中不存在 `README.md` 文件，则将其保存为 `README.md`。
- 如果已经存在 `README.md` 文件，则将其保存为 `README.generated.md`，并让用户自行决定是否替换原有文件。
- 在覆盖现有 README 文件之前，务必先询问用户是否同意。

## 特殊情况处理

- **单仓库项目（Monorepo）**：检测到多个 `package.json` 或 `go.mod` 文件时，生成一个包含子包链接的根目录 README 文件。
- **空项目**：生成一个包含项目名称和基本设置信息的简短 README 文件。
- **项目中的注释语言非英语**：无论代码中的注释使用何种语言，生成的 README 文件都将以英语显示。
- **私有/内部项目**：跳过 “发布”（Publishing）相关内容，重点介绍项目的开发环境设置。

## 使用提示

- **如实记录**：仅记录项目中实际存在的内容，不要虚构功能。
- **注重实用性**：安装和使用说明部分最为重要，应予以优先处理。
- **使用真实示例**：使用项目中实际的文件名和命令。
- 根据项目的复杂程度调整各部分的详细程度（简单脚本对应的 README 文件可以简短一些）。