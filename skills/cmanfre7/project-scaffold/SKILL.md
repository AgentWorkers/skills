# project-scaffold

该项目模板用于快速创建具有最佳实践结构、工具配置的新项目。

## 使用方法

当Colt（或您）需要启动一个新项目时，可以使用此功能来生成完整的项目基础框架。

## 决策树

确定项目类型：

### Web应用（React / Next.js）
```
my-app/
├── src/
│   ├── app/              # Next.js app router
│   ├── components/       # Reusable UI components
│   ├── lib/              # Utilities, helpers, API clients
│   ├── styles/           # Global styles, Tailwind config
│   └── types/            # TypeScript type definitions
├── public/               # Static assets
├── tests/                # Test files
├── .gitignore
├── .eslintrc.json
├── tailwind.config.ts
├── tsconfig.json
├── package.json
└── README.md
```

**初始化命令：**
```bash
npx create-next-app@latest my-app --typescript --tailwind --eslint --app --src-dir
cd my-app && npm install
```

### API / 后端（FastAPI）
```
my-api/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI app entry
│   ├── routers/          # Route modules
│   ├── models/           # Pydantic models / DB models
│   ├── services/         # Business logic
│   └── config.py         # Settings / env vars
├── tests/
├── .gitignore
├── pyproject.toml
├── requirements.txt
└── README.md
```

**初始化命令：**
```bash
mkdir my-api && cd my-api
uv init && uv pip install fastapi uvicorn
```

### 移动应用（SwiftUI）
```
MyApp/
├── MyApp/
│   ├── App.swift
│   ├── ContentView.swift
│   ├── Models/
│   ├── Views/
│   ├── ViewModels/
│   └── Services/
├── MyAppTests/
├── MyAppUITests/
└── README.md
```

**初始化方法：** 使用Xcode或`swift package init --type executable`

### 命令行工具（Node / Python）
```
my-cli/
├── src/
│   └── index.ts          # Entry point
├── bin/
│   └── my-cli            # Executable wrapper
├── tests/
├── .gitignore
├── tsconfig.json
├── package.json
└── README.md
```

### 浏览器扩展
```
my-extension/
├── src/
│   ├── background.ts
│   ├── content.ts
│   ├── popup/
│   │   ├── popup.html
│   │   ├── popup.ts
│   │   └── popup.css
│   └── options/
├── icons/
├── manifest.json
├── .gitignore
├── tsconfig.json
├── package.json
└── README.md
```

## 模板生成后的检查清单

生成项目结构后，请执行以下操作：
1. `git init && git add -A && git commit -m "初始项目模板创建"`
2. 根据项目类型创建合适的`.gitignore`文件
3. 设置代码检查工具（如ESLint / Ruff）的配置
4. 添加一个包含项目名称和设置说明的基本README文件
5. 添加一个基本测试文件，以验证测试运行器是否正常工作

## 资产模板

### .gitignore（通用模板）
```
node_modules/
__pycache__/
.env
.env.local
dist/
build/
.next/
*.pyc
.DS_Store
*.log
coverage/
```