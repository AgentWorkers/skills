---
name: readme-generator
description: 根据项目结构、框架和代码生成一份高质量的 `README.md` 文件。
version: 1.0.0
author: Sovereign Skills
tags: [openclaw, agent-skills, automation, productivity, free, readme, documentation, generator]
triggers:
  - generate readme
  - create readme
  - write readme
  - readme generator
---
# readme-generator — 生成高质量 README 文件的工具

该工具能够分析项目的结构，并自动生成一份全面的、兼容常用开发框架的 README.md 文件。

## 使用步骤

### 1. 分析项目结构

请查看以下文件（如果存在）：
- `package.json` / `pyproject.toml` / `Cargo.toml` / `go.mod`：项目名称、描述、版本及依赖信息
- `tsconfig.json`：TypeScript 配置文件
- `docker-compose.yml` / `Dockerfile`：容器化相关配置
- `.github/workflows/`：持续集成/持续部署（CI/CD）相关文件
- `LICENSE` / `LICENSE.md`：许可证信息
- 主入口文件：`src/index.*`、`src/main.*`、`app.*`、`main.*`、`index.*`
- 测试目录：`tests/` / `test/` / `__tests__/` / `spec/`

```bash
# Get file tree (depth 3, ignore common dirs)
find . -maxdepth 3 -not -path '*/node_modules/*' -not -path '*/.git/*' -not -path '*/dist/*' -not -path '*/__pycache__/*' | head -100
# Windows alternative:
Get-ChildItem -Recurse -Depth 3 -Exclude node_modules,.git,dist,__pycache__ | Select-Object -First 100 FullName
```

### 2. 识别开发框架及生态系统

| 识别信号 | 对应的框架 |
|--------|-----------|
| `next.config.*` 或依赖项中包含 `"next"` | Next.js |
| 依赖项中包含 `"express"` | Express.js |
| 依赖项中包含 `"fastapi"` | FastAPI |
| 依赖项中包含 `"django"` | Django |
| 依赖项中包含 `"flask"` | Flask |
| 依赖项中包含 `"react"`（未使用 Next.js） | React（CRA/Vite） |
| 依赖项中包含 `"vue"` | Vue.js |
| 依赖项中包含 `"svelte"` | SvelteKit |
- `Cargo.toml` 中包含 `[[bin]]` | Rust CLI 工具 |
- `Cargo.toml` 中包含 `actix-web`/`axum` | Rust Web 框架 |
- `go.mod` | Go 语言项目 |

### 3. 确定安装及运行命令

根据识别出的开发框架，确定相应的安装和运行命令：

**Node.js：**
- 查看 `pnpm-lock.yaml` 或 `yarn.lock` 文件，确定使用的包管理器，然后执行 `pnpm install` 或 `yarn install`。
- 查看 `package.json` 中的 `scripts` 部分，获取可用的命令。

**Python：**
- 查看 `poetry.lock` 或 `Pipfile` 文件，确定使用的包管理器，然后执行 `poetry install` 或 `pipenv install`。
- 查看 `requirements.txt` 文件，执行 `pip install -r requirements.txt`。

**Rust：**
- 执行 `cargo build` 或 `cargo run`。

**Go：**
- 执行 `go build` 或 `go run .`。

### 4. 生成徽章（Badges）

根据识别出的开发框架，生成相应的徽章链接。常见的徽章包括：许可证类型、编程语言、运行时版本、持续集成状态、测试覆盖率等。

### 5. 拼凑 README 文件内容

使用以下结构来组织 README 文件的内容：

```markdown
# Project Name

Brief description from package.json/pyproject.toml or inferred from code.

## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [API Reference](#api-reference)  ← only if applicable
- [Configuration](#configuration)  ← only if env vars detected
- [Testing](#testing)
- [Deployment](#deployment)  ← only if Docker/CI detected
- [Contributing](#contributing)
- [License](#license)

## Features
- Bullet list of key capabilities (infer from code structure, routes, exports)

## Prerequisites
- Runtime version (node >= 18, python >= 3.10, etc.)
- Required system tools (Docker, database, etc.)

## Installation
[Package-manager-specific install commands from Step 3]

## Usage
[Dev/start commands, example API calls if it's a server]

## API Reference
[Only for libraries/APIs — list exported functions or endpoints]

## Configuration
[Environment variables — reference env-setup skill if complex]

## Testing
[Test runner command: npm test, pytest, cargo test, etc.]

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feat/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feat/amazing-feature`)
5. Open a Pull Request

## License
[Detected license or "See LICENSE file"]
```

### 6. 根据框架定制内容

- **Next.js：** 添加关于页面路由、API 路由、环境变量的内容。
- **Express/FastAPI：** 文档化路由结构、中间件以及 API 端点。
- **React/Vue：** 文档化组件结构、状态管理方式以及构建输出结果。
- **命令行工具（CLI）：** 文档化命令行参数和选项。
- **库（Libraries）：** 重点介绍 API 文档、安装方法及使用示例。

### 7. 输出结果

将生成的 README 文件写入项目根目录下的 `README.md` 文件中。如果该文件已存在，请先询问用户是否需要覆盖，或者建议将其保存为 `README.generated.md`。

## 特殊情况处理

- **单仓库（Monorepo）：** 生成一个主 README 文件，其中包含对子包的引用；同时为每个子包生成单独的 README 文件。
- **空项目：** 生成一个包含待办事项的简单 README 模板。
- **没有包清单文件（package manifest）：** 根据文件扩展名和目录结构来推断项目依赖。
- **已有 README 文件：** 在覆盖之前先询问用户，展示差异并建议添加新的内容。

## 错误处理

| 错误类型 | 处理方式 |
|---------|-----------|
| 无法识别开发框架 | 生成通用版本的 README 文件，并提示用户指定具体的开发框架。 |
| 项目缺少描述信息 | 使用目录名称作为默认描述，并提示用户补充。 |
| 项目缺少许可证文件 | 提示用户添加许可证文件。 |
- 项目规模过大：** 限制文件扫描深度，重点分析 `src/` 目录和项目配置文件。 |

---
*由 Clawb（SOVEREIGN）开发——更多功能即将推出！*