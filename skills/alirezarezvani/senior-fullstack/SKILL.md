---
name: senior-fullstack
description: 这是一个全栈开发工具包，提供了针对 Next.js、FastAPI、MERN（MongoDB、Express、React）以及 Django 等技术栈的项目框架，并具备代码质量分析功能。适用于新项目的搭建、代码库质量的评估，以及全栈架构模式的实现。
---

# 高级全栈开发技能

具备使用项目脚手架和代码质量分析工具进行全栈开发的技能。

---

## 目录

- [常用术语](#常用术语)
- [工具](#工具)
- [工作流程](#工作流程)
- [参考指南](#参考指南)

---

## 常用术语

当听到以下需求时，请使用此技能：
- “搭建一个新的项目”
- “创建一个 Next.js 应用”
- “使用 React 配置 FastAPI”
- “分析代码质量”
- “检查代码库中的安全问题”
- “应该使用哪种技术栈”
- “设置一个全栈项目”
- “生成项目模板”

---

## 工具

### 项目脚手架

用于生成包含模板代码的全栈项目结构。

**支持的模板：**
- `nextjs` - 支持 Next.js 14 及更高版本，包含 App Router、TypeScript 和 Tailwind CSS
- `fastapi-react` - FastAPI 后端 + React 前端 + PostgreSQL
- `mern` - 使用 MongoDB、Express、React 和 TypeScript 的全栈框架
- `django-react` - Django REST Framework + React 前端

**使用方法：**

```bash
# List available templates
python scripts/project_scaffolder.py --list-templates

# Create Next.js project
python scripts/project_scaffolder.py nextjs my-app

# Create FastAPI + React project
python scripts/project_scaffolder.py fastapi-react my-api

# Create MERN stack project
python scripts/project_scaffolder.py mern my-project

# Create Django + React project
python scripts/project_scaffolder.py django-react my-app

# Specify output directory
python scripts/project_scaffolder.py nextjs my-app --output ./projects

# JSON output
python scripts/project_scaffolder.py nextjs my-app --json
```

**参数：**
| 参数 | 说明 |
|---------|--------|
| `template` | 模板名称（nextjs, fastapi-react, mern, django-react） |
| `project_name` | 新项目目录的名称 |
| `--output, -o` | 输出目录（默认：当前目录） |
| `--list-templates, -l` | 列出所有可用模板 |
| `--json` | 以 JSON 格式输出 |

**输出内容：**
- 包含所有必要文件的项目结构 |
- 包配置（package.json, requirements.txt） |
- TypeScript 配置 |
- Docker 和 docker-compose 设置 |
- 环境文件模板 |
- 运行项目的下一步指导

---

### 代码质量分析工具

用于分析全栈代码库中的质量问题。

**分析类别：**
- 安全漏洞（硬编码的密钥、注入风险） |
- 代码复杂性指标（圈复杂度、嵌套深度） |
- 依赖项健康状况（过时的包、已知的 CVE） |
- 测试覆盖率估算 |
- 文档质量

**使用方法：**

```bash
# Analyze current directory
python scripts/code_quality_analyzer.py .

# Analyze specific project
python scripts/code_quality_analyzer.py /path/to/project

# Verbose output with detailed findings
python scripts/code_quality_analyzer.py . --verbose

# JSON output
python scripts/code_quality_analyzer.py . --json

# Save report to file
python scripts/code_quality_analyzer.py . --output report.json
```

**参数：**
| 参数 | 说明 |
|---------|--------|
| `project_path` | 项目目录路径（默认：当前目录） |
| `--verbose, -v` | 显示详细分析结果 |
| `--json` | 以 JSON 格式输出 |
| `--output, -o` | 将报告写入文件 |

**输出内容：**
- 总分（0-100 分，附带等级评定） |
- 按严重程度划分的安全问题（关键、高、中、低） |
- 复杂度较高的文件 |
- 存在 CVE 的脆弱依赖项 |
- 测试覆盖率估算 |
- 文档完整性 |
- 优先级建议

**示例输出：**

```
============================================================
CODE QUALITY ANALYSIS REPORT
============================================================

Overall Score: 75/100 (Grade: C)
Files Analyzed: 45
Total Lines: 12,500

--- SECURITY ---
  Critical: 1
  High: 2
  Medium: 5

--- COMPLEXITY ---
  Average Complexity: 8.5
  High Complexity Files: 3

--- RECOMMENDATIONS ---
1. [P0] SECURITY
   Issue: Potential hardcoded secret detected
   Action: Remove or secure sensitive data at line 42
```

---

## 工作流程

### 工作流程 1：启动新项目

1. 根据需求选择合适的技术栈 |
2. 搭建项目结构 |
3. 进行初步的质量检查 |
4. 设置开发环境 |

```bash
# 1. Scaffold project
python scripts/project_scaffolder.py nextjs my-saas-app

# 2. Navigate and install
cd my-saas-app
npm install

# 3. Configure environment
cp .env.example .env.local

# 4. Run quality check
python ../scripts/code_quality_analyzer.py .

# 5. Start development
npm run dev
```

### 工作流程 2：审计现有代码库

1. 运行代码质量分析 |
2. 查看安全问题 |
3. 先解决关键问题 |
4. 制定改进计划 |

```bash
# 1. Full analysis
python scripts/code_quality_analyzer.py /path/to/project --verbose

# 2. Generate detailed report
python scripts/code_quality_analyzer.py /path/to/project --json --output audit.json

# 3. Address P0 issues immediately
# 4. Create tickets for P1/P2 issues
```

### 工作流程 3：技术栈选择

使用技术栈指南来评估不同的选项：

1. **需要 SEO 吗？** → 使用支持服务器端渲染（SSR）的 Next.js |
2. **后端需要处理大量 API 吗？** → 选择 FastAPI 或 NestJS |
3. **需要实时功能吗？** → 添加 WebSocket 层 |
4. **团队技能如何？** → 选择与团队技能相匹配的技术栈 |

详细比较请参阅 `references/tech_stack_guide.md`。

---

## 参考指南

### 架构模式（`references/architecture_patterns.md`）

- 前端组件架构（原子设计、容器/表现层设计）
- 后端架构模式（清晰架构、仓库模式）
- API 设计（REST 规范、GraphQL 模式设计）
- 数据库模式（连接池、事务、读复制）
- 缓存策略（缓存策略、HTTP 缓存头）
- 认证架构（JWT + 刷新令牌、会话）

### 开发工作流程（`references/development_workflows.md`）

- 本地开发环境设置（Docker Compose、环境配置）
- Git 工作流程（基于主分支的提交）
- CI/CD 流程（GitHub Actions 示例）
- 测试策略（单元测试、集成测试、端到端测试）
- 代码审查流程（PR 模板、检查清单）
- 部署策略（蓝绿部署、金丝雀部署、功能开关）
- 监控与可观测性（日志记录、指标监控、健康检查）

### 技术栈指南（`references/tech_stack_guide.md`）

- 前端框架比较（Next.js、React+Vite、Vue）
- 后端框架（Express、Fastify、NestJS、FastAPI、Django）
- 数据库选择（PostgreSQL、MongoDB、Redis）
- 对象关系映射（ORM）工具（Prisma、Drizzle、SQLAlchemy）
- 认证解决方案（Auth.js、Clerk、自定义 JWT）
- 部署平台（Vercel、Railway、AWS）
- 根据使用场景推荐的技术栈（MVP、SaaS、企业级应用）

---

## 快速参考

### 技术栈决策矩阵

| 需求 | 推荐技术栈 |
|---------|-------------------|
| 需要 SEO 支持的网站 | 使用支持服务器端渲染的 Next.js |
| 内部仪表盘 | 使用 React + Vite |
| 以 API 为主的后端 | FastAPI 或 Fastify |
| 企业级应用 | NestJS + PostgreSQL |
| 快速原型开发 | Next.js + API 路由 |
| 需要大量文档的数据存储 | MongoDB |
| 复杂查询 | 使用 PostgreSQL |

### 常见问题及解决方案

| 问题 | 解决方案 |
|------|-------------------|
| 多次查询 | 使用 DataLoader 或懒加载机制 |
| 构建速度慢 | 检查打包大小、采用懒加载 |
| 认证逻辑复杂 | 使用 Auth.js 或 Clerk |
| 类型错误 | 在 tsconfig 中启用严格模式 |
| CORS 问题 | 正确配置中间件 |