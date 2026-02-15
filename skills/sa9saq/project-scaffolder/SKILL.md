---
description: 使用最佳实践模板为 Next.js、Express、Python、Go 等框架搭建新项目。
---

# 项目脚手架工具

该工具可生成包含合理默认设置和最佳实践的项目模板。

## 系统要求

- Node.js 18.0 或更高版本（用于 JavaScript/TypeScript 项目）
- Python 3.8 或更高版本（用于 Python 项目）
- `git`（用于版本控制初始化）

## 使用说明

1. **询问用户**：所需使用的框架/模板、项目名称以及目标目录。
2. **使用相应的模板创建项目**。
3. **项目创建完成后**：初始化 `git`，创建 `.gitignore` 文件，并根据需要安装依赖项（请先询问用户是否需要安装）。

## 模板示例

### Next.js（应用路由 + TypeScript）
```bash
npx create-next-app@latest my-app --typescript --tailwind --eslint --app --src-dir --use-npm
```

### Express.js API
```bash
mkdir my-api && cd my-api
npm init -y
npm install express cors helmet dotenv
npm install -D nodemon
mkdir -p src/{routes,middleware}
```
创建 `src/index.js` 文件，包含基本的 Express 应用代码（如 CORS、helmet、JSON 解析器以及健康检查端点）。
在 `package.json` 文件中添加以下脚本：`"dev": "nodemon src/index.js"` 和 `"start": "node src/index.js"`。

### Python CLI 工具
```bash
mkdir my-tool && cd my-tool
python3 -m venv .venv
source .venv/bin/activate
```
创建 `main.py` 文件，包含基本的 `argparse` 代码结构、`requirements.txt` 文件以及 `README.md` 文件。

### Python FastAPI
```bash
mkdir my-api && cd my-api
python3 -m venv .venv
pip install fastapi uvicorn
```
创建 `main.py` 文件，包含 FastAPI 应用代码、健康检查端点以及 CORS 中间件。

### 静态 HTML 网站
```bash
mkdir my-site && cd my-site
mkdir -p {css,js,img}
```
创建 `index.html` 文件（响应式布局）、`css/style.css` 文件以及 `js/main.js` 文件。

### Go CLI 工具
```bash
mkdir my-cli && cd my-cli
go mod init github.com/user/my-cli
```
创建 `main.go` 文件，包含基本的命令行参数解析代码。

### 常见的后置操作步骤
```bash
git init
# Generate appropriate .gitignore (node_modules/, .env, .venv/, __pycache__/, etc.)
git add -A && git commit -m "chore: initial scaffold"
```

## 特殊情况处理

- **目标目录已存在**：在覆盖目录前发出警告并询问用户是否确认覆盖。切勿直接覆盖现有文件。
- **缺少运行时环境**：在创建项目前检查系统是否安装了 `node` 或 `python3`；如果缺少依赖项，请及时告知用户。
- **自定义技术栈**：如果用户使用自定义的技术栈，请组合相关代码片段，而非使用固定模板。

## 安全注意事项

- **不要在生成的 `.env` 文件中写入真实的 API 密钥或敏感信息**，请使用占位符（如 `YOUR_API_KEY_HERE`）。
- **务必将 `.env` 文件添加到 `.gitignore` 文件中**。
- **设置安全默认配置**（例如为 Express 应用启用 `helmet` 中间件、配置 CORS 策略等）。

## 其他说明

- 在运行 `npm install` 或 `pip install` 命令前，请先询问用户——这些操作可能需要一定时间或网络连接。
- 根据用户的需求调整模板设置（例如选择 TypeScript 或 JavaScript 作为开发语言，以及使用 `npm`、`yarn` 或 `pnpm` 作为包管理工具）。
- 必须为每个项目创建 `README.md` 文件，其中包含基本的安装和配置指南。