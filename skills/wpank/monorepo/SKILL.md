---
name: monorepo
model: standard
description: 使用 Turborepo、Nx 和 pnpm 工作区来构建和管理单仓库项目（monorepos），涵盖工作区结构、依赖管理、任务编排、缓存、持续集成/持续部署（CI/CD）以及发布等环节。适用于搭建单仓库项目、优化构建过程或管理共享包的场景。
---

# 单一仓库管理

构建高效、可扩展的单一仓库，以实现代码共享、统一工具链以及跨多个包和应用程序的原子级更改。

## 适用场景

- 设置新的单一仓库或从多仓库架构迁移
- 优化构建和测试性能
- 管理跨包的共享依赖项
- 为单一仓库配置持续集成/持续部署（CI/CD）流程
- 对包进行版本控制和发布

## 为什么使用单一仓库？

**优势：**代码和依赖项的共享、跨项目的原子级提交、统一的工具链、更便捷的代码重构、更好的代码可见性。

**挑战：**大规模构建时的性能问题、CI/CD流程的复杂性、访问控制以及庞大的Git历史记录管理。

## 工具选择

### 包管理器

| 工具 | 推荐理由 | 备注 |
|---------|---------------|-------|
| **pnpm** | 推荐使用 | 速度快、规则严格、对工作区的支持出色 |
| **npm** | 也可使用 | 内置工作区功能，但安装速度较慢 |
| **Yarn** | 也可使用 | 功能成熟，但在多数方面pnpm更胜一筹 |

### 构建系统

| 工具 | 适用场景 | 权衡点 |
|------|----------|-----------|
| **Turborepo** | 适用于大多数项目 | 配置简单、缓存速度快、支持Vercel集成 |
| **Nx** | 适用于大型组织或复杂的项目结构 | 功能丰富，但学习曲线较陡 |
| **Lerna** | 适用于旧项目 | 目前处于维护模式，建议逐步迁移 |

**建议：**除非你需要Nx的代码生成、依赖关系图可视化或插件生态系统，否则优先选择Turborepo。

## 工作区结构

**约定：**`apps/`用于可部署的应用程序，`packages/`用于共享库。

## Turborepo的设置

### 根目录配置

```yaml
# pnpm-workspace.yaml
packages:
  - "apps/*"
  - "packages/*"
```

### 流程配置

```json
// package.json (root)
{
  "name": "my-monorepo",
  "private": true,
  "scripts": {
    "build": "turbo run build",
    "dev": "turbo run dev",
    "test": "turbo run test",
    "lint": "turbo run lint",
    "type-check": "turbo run type-check",
    "clean": "turbo run clean && rm -rf node_modules"
  },
  "devDependencies": {
    "turbo": "^2.0.0",
    "prettier": "^3.0.0"
  },
  "packageManager": "pnpm@9.0.0"
}
```

**关键概念：**
- `dependsOn: ["^build"]` — 先构建依赖项（按拓扑顺序）
- `outputs` — 需要缓存的文件（对于仅产生副作用的任务可省略）
- `inputs` — 会导致缓存失效的文件（默认为所有文件）
- `persistent: true` — 适用于长时间运行的开发服务器
- `cache: false` — 禁用开发任务的缓存

### 包配置

```json
// packages/ui/package.json
{
  "name": "@repo/ui",
  "version": "0.0.0",
  "private": true,
  "exports": {
    ".": { "import": "./dist/index.js", "types": "./dist/index.d.ts" },
    "./button": { "import": "./dist/button.js", "types": "./dist/button.d.ts" }
  },
  "scripts": {
    "build": "tsup src/index.ts --format esm,cjs --dts",
    "dev": "tsup src/index.ts --format esm,cjs --dts --watch"
  },
  "devDependencies": {
    "@repo/config-ts": "workspace:*",
    "tsup": "^8.0.0"
  }
}
```

## Nx的设置

```bash
npx create-nx-workspace@latest my-org

# Generate projects
nx generate @nx/react:app my-app
nx generate @nx/js:lib utils
```

```json
// nx.json
{
  "targetDefaults": {
    "build": {
      "dependsOn": ["^build"],
      "inputs": ["production", "^production"],
      "cache": true
    },
    "test": {
      "inputs": ["default", "^production"],
      "cache": true
    }
  },
  "namedInputs": {
    "default": ["{projectRoot}/**/*"],
    "production": ["default", "!{projectRoot}/**/*.spec.*"]
  }
}
```

### Nx的优势：`nx affected`能够精确判断哪些项目发生了变化，从而避免不必要的构建。

## 依赖项管理（使用pnpm）

```bash
# Install in specific package
pnpm add react --filter @repo/ui
pnpm add -D typescript --filter @repo/ui

# Install workspace dependency
pnpm add @repo/ui --filter web

# Install in root (shared dev tools)
pnpm add -D eslint -w

# Run script in specific package
pnpm --filter web dev
pnpm --filter @repo/ui build

# Run in all packages
pnpm -r build

# Filter patterns
pnpm --filter "@repo/*" build
pnpm --filter "...web" build    # web + all its dependencies

# Update all dependencies
pnpm update -r
```

### `.npmrc`文件配置

```ini
# Hoist shared dependencies for compatibility
shamefully-hoist=true

# Strict peer dependency management
auto-install-peers=true
strict-peer-dependencies=true
```

## 共享配置

### TypeScript配置

```json
// packages/config-ts/base.json
{
  "compilerOptions": {
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "module": "ESNext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "declaration": true
  }
}

// apps/web/tsconfig.json
{
  "extends": "@repo/config-ts/base.json",
  "compilerOptions": { "outDir": "dist", "rootDir": "src" },
  "include": ["src"]
}
```

## 构建优化

### 远程缓存

```bash
# Turborepo + Vercel remote cache
npx turbo login
npx turbo link

# Now builds share cache across CI and all developers
# First build: 2 minutes. Cache hit: 0 seconds.
```

### 缓存配置

```json
{
  "tasks": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**", ".next/**"],
      "inputs": ["src/**/*.tsx", "src/**/*.ts", "package.json"]
    }
  }
}
```

**重要提示：**务必精确定义`inputs`。如果构建过程仅依赖于`src/`目录中的文件，就不要因为`README.md`的更改而触发缓存失效。

## 持续集成/持续部署（CI/CD）

### GitHub Actions

```yaml
name: CI
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0    # Required for affected commands

      - uses: pnpm/action-setup@v4
        with:
          version: 9

      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: "pnpm"

      - run: pnpm install --frozen-lockfile
      - run: pnpm turbo run build test lint type-check
```

### 仅部署受影响的部分

```yaml
- name: Deploy affected apps
  run: |
    AFFECTED=$(pnpm turbo run build --dry-run=json --filter='[HEAD^1]' | jq -r '.packages[]')
    if echo "$AFFECTED" | grep -q "web"; then
      pnpm --filter web deploy
    fi
```

## 包的发布

```bash
# Setup Changesets
pnpm add -Dw @changesets/cli
pnpm changeset init

# Workflow
pnpm changeset          # Create changeset (describe what changed)
pnpm changeset version  # Bump versions based on changesets
pnpm changeset publish  # Publish to npm
```

### 最佳实践

1. **锁定依赖版本** — 在整个工作区内使用固定版本或锁定文件
2. **集中配置规则** — 在共享包中统一配置ESLint、TypeScript和Prettier
3. **保持依赖关系图的无环状态** — 避免包之间的循环依赖
4. **精确定义缓存的范围** — 错误的缓存配置会导致资源浪费或构建失败
5. **在前端和后端之间共享代码规范** — 确保代码定义的一致性
6. **在包中编写单元测试，在应用程序中进行端到端测试** — 使测试范围与包的范围相匹配
7. **为每个包编写`README.md`文档** — 说明包的功能、开发流程和使用方法
8. **使用变更集进行版本控制** — 实现自动化且可审查的发布流程

## 常见问题及解决方法

| 问题 | 解决方法 |
|---------|-----|
| 循环依赖 | 将共享代码重构为独立的第三方包 |
| “幽灵依赖”（依赖项未在`package.json`中列出） | 使用pnpm的严格模式 |
| 缓存配置错误 | 将缺失的文件添加到`inputs`数组中 |
| 过度共享代码 | 仅共享真正可复用的代码 |
| CI配置中缺少`fetch-depth: 0` | 此参数对于正确比较构建历史记录至关重要 |
| 缓存开发任务 | 将`cache`设置为`false`并将`persistent`设置为`true`

## 绝对不要做的事情

- **绝对不要在工作区依赖版本中使用通配符（*）** — 应使用`workspace:*`来指定依赖版本 |
- **绝对不要在CI过程中省略`--frozen-lockfile`选项** — 这有助于确保构建结果的可重复性 |
- **绝对不要缓存开发服务器的任务** — 这些任务运行时间较长，不适合缓存 |
- **绝对不要创建循环依赖关系** — 这会破坏构建顺序 |
- **在没有充分理解的情况下使用`shamefully-hoist`功能** — 这只是一个临时解决方案，不应作为常规做法

## 相关技能

- **相关内容：** [服务层架构](../service-layer-architecture/) — 单一仓库应用程序中的API设计模式
- **相关内容：** [postgres-job-queue](../postgres-job-queue/) — 单一仓库服务的后台任务处理机制