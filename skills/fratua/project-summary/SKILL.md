---
name: project-summary
description: 生成代码库的即时概览：语言、框架、架构、入口点以及关键文件
version: 1.0.0
author: Sovereign Skills
tags: [openclaw, agent-skills, automation, productivity, free, project, summary, overview, onboarding]
triggers:
  - summarize project
  - project overview
  - codebase summary
  - project summary
  - what is this project
---
# 项目概述 — 代码库的即时视图

本文档旨在为新入职的开发者提供项目结构概览，或为相关团队成员提供项目背景信息。

## 执行步骤

### 1. 扫描项目根目录

请首先阅读以下文件（均为可选）：
- `package.json` / `pyproject.toml` / `Cargo.toml` / `go.mod` / `*.sln` / `*.csproj`
- `README.md` — 项目说明文件
- `LICENSE` — 许可证文件
- `Dockerfile` / `docker-compose.yml` — 容器化配置文件
- `.github/workflows/*.yml` / `.gitlab-ci.yml` / `Jenkinsfile` — 测试/部署配置文件
- `tsconfig.json` / `babel.config.*` / `webpack.config.*` / `vite.config.*` — 编译/构建配置文件
- `.eslintrc*` / `.prettierrc*` — 代码格式化规则文件
- `pyproject.toml [tool.ruff]` — 项目配置文件（特定工具相关）

### 2. 确定项目使用的语言和框架

- **主要使用的语言**：根据文件扩展名来判断（具体方法请参见 **```bash
find . -type f -not -path '*/node_modules/*' -not -path '*/.git/*' -not -path '*/dist/*' -not -path '*/target/*' -not -path '*/__pycache__/*' -not -path '*/.venv/*' | sed 's/.*\.//' | sort | uniq -c | sort -rn | head -10
# Windows:
Get-ChildItem -Recurse -File -Exclude node_modules,.git,dist,target | Group-Object Extension | Sort-Object Count -Descending | Select-Object -First 10 Count,Name
```**）
- **使用的框架**：通过检查项目依赖项来确定（具体方法请参见 **README-generator** 技能文档中的检测表格）。

### 3. 分析项目架构

根据目录结构判断项目的架构模式：
| 目录结构 | 架构模式 |
|-----------|---------|
| `src/controllers/`, `src/models/`, `src/routes/` | MVC（模型-视图-控制器架构） |
| `src/features/*/`（每个目录包含组件、钩子及 API） | 基于功能的架构 |
| `src/domain/`, `src/application/`, `src/infrastructure/` | 清晰架构（Clean Architecture）/ 领域驱动设计（DDD） |
| `pages/` 或 `app/`（Next.js/Nuxt） | 基于文件的路由架构 |
| `cmd/`, `internal/`, `pkg/` | Go 项目的标准目录结构 |
| `src/lib.rs`, `src/main.rs` | Rust 项目的二进制文件/库文件 |
| 目录结构简单、文件数量较少 | 简单项目或脚本项目 |

### 4. 确定项目的入口点

```bash
# Look for common entry points
ls -la src/index.* src/main.* app.* main.* index.* manage.py server.* 2>/dev/null
# Check package.json "main", "module", "bin", "scripts.start"
# Check Cargo.toml [[bin]] or src/main.rs
# Check pyproject.toml [project.scripts]
```

### 5. 列出关键文件

列出最重要的文件，并为每个文件提供简短说明：
```markdown
## Key Files
| File | Purpose |
|------|---------|
| `src/index.ts` | Application entry point |
| `src/routes/` | API route definitions |
| `src/models/` | Database models / schemas |
| `src/middleware/` | Express middleware (auth, logging) |
| `prisma/schema.prisma` | Database schema |
| `docker-compose.yml` | Local development services |
| `.github/workflows/ci.yml` | CI pipeline — test + lint + build |
```

重点介绍新开发者需要了解的文件。跳过生成文件、自解释的配置文件以及样板文件。

### 6. 文档化测试环境

```bash
# Detect test framework
grep -l "jest\|vitest\|mocha\|pytest\|unittest\|cargo test\|go test" package.json pyproject.toml Cargo.toml Makefile 2>/dev/null
# Find test files
find . -name "*.test.*" -o -name "*.spec.*" -o -name "test_*" -not -path '*/node_modules/*' 2>/dev/null | head -20
```

说明测试框架的类型、测试文件的存放位置、运行测试的方法以及测试的数量。

### 7. 检查持续集成/持续部署（CI/CD）配置

如果存在 CI/CD 配置，请总结以下内容：
- 触发流程的条件（如代码提交、Pull Request 或定时任务）
- 执行的步骤（代码检查、测试、构建、部署）
- 部署的目标环境（如果可确定）

### 8. 列出项目依赖项

列出最重要的 10 个依赖项（并非所有依赖项）：
- 重点关注框架、数据库、认证组件、测试工具和构建工具
- 提供依赖项的总数估算

```markdown
## Key Dependencies
| Package | Purpose |
|---------|---------|
| express | Web framework |
| prisma | Database ORM |
| jsonwebtoken | JWT authentication |
| jest | Testing framework |
| **Total** | **47 dependencies (12 dev)** |
```

### 9. 输出结构化的项目概览

```markdown
# Project Summary: [name]

**Description:** [from package.json or README]
**Language:** TypeScript | **Framework:** Express.js | **Runtime:** Node.js 20
**Architecture:** MVC | **Package Manager:** pnpm
**License:** MIT

## Quick Start
[install + run commands]

## Structure
[architecture description + key directories]

## Key Files
[table from Step 5]

## Dependencies
[table from Step 8]

## Testing
- **Framework:** Jest
- **Run:** `pnpm test`
- **Coverage:** `pnpm test -- --coverage`

## CI/CD
- **Platform:** GitHub Actions
- **Triggers:** Push to main, PRs
- **Pipeline:** Lint → Test → Build → Deploy to Vercel

## Notes
[Anything unusual or important — monorepo setup, required services, known issues from README]
```

## 特殊情况处理

- **单仓库项目（Monorepo）**：仅总结项目根目录的结构，并简要描述每个包/工作区的功能。
- **没有项目配置文件（manifest file）**：根据文件扩展名和目录结构进行推断。
- **项目文件数量非常多（1000 个以上）**：将扫描范围限制在 `src/` 目录及根目录。
- **项目使用多种语言**：分别列出主要语言和次要语言，并标注各自所占的比例。
- **空项目或新项目**：说明项目的基本配置情况以及缺失的部分。

## 错误处理

| 错误类型 | 处理方法 |
|---------|-----------|
| 无法读取文件（权限问题） | 跳过该文件并记录无法读取的具体文件 |
- 项目文件数量过多导致扫描超时 | 将扫描范围限制在 `src/` 目录、根目录及 `find -maxdepth 3` 的结果 |
- 识别出的框架未知 | 标记为“自定义框架”并说明实际可检测到的组件 |
- 项目缺少 `README.md` 或项目说明文件 | 使用目录名称代替，并注明文件缺失的情况 |

---
*由 Clawb（SOVEREIGN）开发 — 更多相关技能即将推出*