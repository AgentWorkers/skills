---
name: opentangl
description: >
  **设置并运行 OpenTangl：**  
  OpenTangl 是一个自主的 AI 开发引擎，它可以扫描您的代码库，根据产品愿景提出相应的开发任务，编写代码，执行代码验证，创建 Pull Request（PR），并完成代码合并——整个过程形成一个闭环。该工具支持任何 JavaScript（JS）或 TypeScript（TS）项目。
metadata: {"clawdbot":{"emoji":"🤖","requires":{"anyBins":["node","git","gh"],"anyEnv":["OPENAI_API_KEY","ANTHROPIC_API_KEY"]}}}
---
# OpenTangl

OpenTangl 可以为任何 JavaScript/TypeScript 项目设置一个自动化的开发循环。它能够读取项目愿景，提出开发任务，编写代码，验证代码构建结果，创建 Pull Request (PR)，使用大型语言模型 (LLM) 进行代码审查，并最终完成代码合并。

## 先决条件

在开始使用之前，请确保以下工具已安装，并且配置正确（仅列出未安装的工具）：

- **Node.js** ≥ 18 （运行 `node --version` 检查）
- 配置了远程仓库的 **git** （运行 `git --version` 检查）
- 已经通过身份验证的 **GitHub CLI** （运行 `gh auth status` 检查）——用于创建和合并 PR
- 一个 **LLM API 密钥** — OpenAI（使用 `OPENAI_API_KEY`）或 Anthropic（使用 `ANTHROPIC_API_KEY`）

如果缺少任何工具，请明确告知用户如何安装，并在问题解决之前暂停使用 OpenTangl。

## 第 1 步 — 克隆 OpenTangl

```bash
git clone https://github.com/8co/opentangl.git
cd opentangl
npm install
```

如果用户已经克隆了 OpenTangl，请直接跳到第 2 步。

## 第 2 步 — 确定目标项目

询问用户：
- 您是 **(a)** 从零开始开发新项目，**(b)** 在改进现有项目，还是 **(c)** 不确定该怎么做？

### 路径 A：新项目
1. 询问：**“您想开发什么？”** 获取用户对项目的 2-3 句描述。
2. 询问：**“项目类型是什么？”** 可能是前端应用（React/Vite、Next.js）、后端 API（Serverless、Express），或者全栈应用。
3. 使用相应的工具搭建项目框架：
   - React + Vite：`npm create vite@latest {name} -- --template react-ts`
   - Next.js：`npx create-next-app@latest {name} --typescript`
   - Serverless：`npx serverless create --template aws-nodejs --path {name}`
   - Express：手动创建 `package.json` 和 `src/index.ts`
4. 初始化 Git：`git init && git add . && git commit -m "初始项目搭建"
5. 在创建 GitHub 仓库之前，询问用户是否确认：`gh repo create {name} --public --source . --push`
6. 记录新项目的路径（相对于 OpenTangl 的根目录）。

### 路径 B：现有项目
1. 询问：**“您的项目位于哪里？”** 如果用户回答“当前目录”，则使用当前目录作为项目路径。
2. 通过扫描项目根目录自动识别项目类型：
   - **配置文件**：`tsconfig.json` → TypeScript 项目；`vite.config.ts` → Vite 项目；`next.config.*` → Next.js 项目；`serverless.yml` → Serverless 项目
   - **包管理器**：`package-lock.json` → npm 项目；`yarn.lock` → yarn 项目；`pnpm-lock.yaml` → pnpm 项目
   - **构建/测试命令**：查看 `package.json` 中的 `build`、`test`、`lint`、`typecheck` 命令
   - **代码目录**：默认为 `src/`
   - **目标分支**：检查 `git symbolic-ref refs/remotes/origin/HEAD` 或 `main`/`master` 分支
3. 向用户展示识别到的项目信息并获取确认
4. 询问：**“这个项目是否包含其他相关仓库？”** 如果有，对每个相关仓库重复上述步骤。

### 路径 C：不确定
请求用户提供项目目录的路径。确认路径后，根据项目类型选择对应的步骤（路径 A 或 B）。

## 第 3 步 — 生成 `projects.yaml` 文件

在 OpenTangl 的根目录下创建 `projects.yaml` 文件。每个项目条目应包含以下信息：

```yaml
projects:
  - id: my-app                          # Short kebab-case ID (used in CLI flags)
    name: my-app                        # Human-readable name
    path: ../my-app                     # Relative path from OpenTangl root to the project
    type: react-vite                    # Project type (see below)
    description: React dashboard app    # One-line description
    scan_dirs:
      - src                             # Directories containing source code
    skip_patterns:
      - node_modules
      - dist
      - "*.test.*"
    verify:                             # Commands that must pass before committing
      - command: npm
        args: [run, build]
    package_manager: npm                # npm | yarn | pnpm
    merge:
      target_branch: main               # Branch PRs merge into
```

**支持的项目类型**：`typescript-node`、`serverless-js`、`serverless-ts`、`react-vite`、`react-next`、`express`（或其他自定义类型）。

对于 **多项目环境**，可以在 `projects.yaml` 中添加 `environment` 字段，将相关项目归类到同一个愿景下：

```yaml
  - id: my-api
    environment: my-product
    # ...
  - id: my-frontend
    environment: my-product
    # ...
```

## 第 4 步 — 创建项目愿景文档

在 `docs/environments/{environment}/product-vision.md` 文件中编写项目愿景文档（单项目使用项目 ID 作为环境名称；多项目环境使用 `environment` 字段）。

愿景文档包含两个部分：

### 项目起源与发展方向（由用户编写，OpenTangl 不会修改）

请用户描述：
- **项目简介**：关于项目的 2-3 句描述
- **长期发展方向**：未来 6-12 个月的规划
- **最重要的原则**：指导项目决策的 3-5 条原则

### 当前优先事项（由 OpenTangl 在每次运行后维护）

询问用户：**“您希望首先实现或改进的 3-5 个功能是什么？”**

将这些需求记录为 **活跃任务**：

```markdown
### Active Initiatives

1. **{Priority}** — {What and why}
   - Status: not started
```

如果用户不确定，可以建议用户扫描代码库并协助确定优先事项。

## 第 5 步 — 配置大型语言模型 (LLM)

在 OpenTangl 的根目录下创建 `.env` 文件：

**针对 OpenAI 的配置：**
```
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o
DEFAULT_AGENT=openai
```

**针对 Anthropic (Claude) 的配置：**
```
ANTHROPIC_API_KEY=sk-ant-...
ANTHROPIC_MODEL=claude-sonnet-4-20250514
DEFAULT_AGENT=anthropic
```

用户可以通过运行 `--agent openai|anthropic` 在运行时切换使用不同的 LLM 提供商。

## 第 6 步 — 首次运行

初始化一个空的任务队列：

```bash
mkdir -p tasks
echo "tasks: []" > tasks/queue.yaml
```

**向用户展示运行命令并获取确认**。之后，OpenTangl 会自动创建分支、提交代码并提交 Pull Request：

```bash
npx tsx src/cli.ts autopilot --projects {project-id} --cycles 1 --feature-ratio 0.8
```

对于多项目环境，需要分别为每个项目执行这些操作。

## 开发循环的工作流程：
1. OpenTangl 读取愿景文档并扫描项目代码库
2. 提出符合愿景的开发任务
3. 自动执行每个任务（编写代码、运行验证）
4. 创建 Pull Request，使用 LLM 进行代码审查，通过后进行合并
5. 更新愿景文档以反映项目进展

首次运行完成后，与用户一起检查运行结果，确认所有步骤是否正常完成，并查看更新后的愿景文档。

## 持续使用方法

在需要开发循环时，随时运行 OpenTangl：

```bash
npx tsx src/cli.ts autopilot --projects {ids} --cycles {n} --feature-ratio 0.8
```

**常用参数：**
- `--cycles N`：指定要运行的循环次数
- `--feature-ratio 0.8`：80% 用于新功能开发，20% 用于维护和测试（可调整）
- `--agent openai|anthropic`：用于指定使用的 LLM 提供商

**后台运行**：即使终端关闭，OpenTangl 也会继续运行：

```bash
nohup caffeinate -dims npx --yes tsx src/cli.ts autopilot --projects {ids} --cycles 3 --feature-ratio 0.8 > /tmp/opentangl.log 2>&1 &
```

可以使用 `tail -f /tmp/opentangl.log` 命令监控运行日志。

## 常见问题解决方法：
- **“没有待处理的任务”**：队列为空。运行 OpenTangl 以生成新的开发任务，或更新愿景文档中的优先事项。
- **构建失败**：OpenTangl 会尝试最多 3 次，失败后标记任务为失败并跳过。
- **需要人工处理的 Pull Request**：LLM 审查者指出了关键问题。请查看 GitHub 上的相关问题以获取详细信息。
- **“需要 OPENAI_API_KEY”**：请创建 `.env` 文件并添加 API 密钥（参见第 5 步）。
- **合并冲突**：OpenTangl 具有内置的冲突解决机制；如果无法自动解决冲突，会将 Pull Request 提交给用户处理。