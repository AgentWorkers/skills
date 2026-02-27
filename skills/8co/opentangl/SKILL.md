---
name: opentangl
description: 这不仅仅是一个代码生成工具，而是一个完整的开发团队。你负责制定项目的愿景，而这个工具会负责编写实际的代码。它具备自动构建、提交 Pull Request（PR）、代码审查以及跨多个代码仓库进行代码合并的功能。只需将这个工具应用于任何 JavaScript 或 TypeScript 项目，它就能自动规划功能、编写代码、验证构建结果、提交 PR、审查代码差异，并最终完成代码合并。它能够将多个代码仓库统一管理，就像管理一个完整的产品一样。当你希望快速发布代码（而无需亲自编写代码时），就可以使用这个工具。它集成了人工智能代码生成、自动化开发流程、多代码仓库协同工作等功能，支持 TypeScript 和 JavaScript 语言，同时兼容 GitHub、OpenAI、Anthropic、Claude、GPT、LLM 等技术，以及各种开发工具和持续集成/持续部署（CI/CD）流程。
homepage: https://github.com/8co/opentangl
category: development
tags: ["ai-agents", "code-generation", "autonomous-development", "multi-repo", "typescript", "javascript", "github", "pull-requests", "openai", "anthropic", "claude", "gpt", "llm", "devtools", "workflow-automation", "ci-cd", "code-review", "codegen"]
metadata: {"clawdbot":{"emoji":"🤖","requires":{"bins":["node","git","gh"]}}}
---
# OpenTangl

该技能可为您的任何 JavaScript/TypeScript 项目配置一个自动化开发循环。它会检测您的项目设置，生成相应的配置文件，并使 OpenTangl 能够自主运行。

**请按以下步骤操作。** 在进入下一步之前，请确保每个步骤都已完成。在每个关键环节都等待用户的确认。切勿跳过步骤或合并步骤——用户需要在这些步骤之间完成自己的操作。

## 先决条件

在使用此技能之前，用户必须已经克隆并安装了 OpenTangl。如果用户尚未安装，请为他们运行以下命令：

```
git clone https://github.com/8co/opentangl.git
cd opentangl
npm install
```

**请勿代表用户运行这些命令。** 等待用户确认 OpenTangl 已成功安装。

确认安装完成后，检查所需工具是否已安装。运行以下检查并报告结果：

- **Node.js** ≥ 18：运行 `node --version` 并显示输出结果
- **git**：运行 `git --version` 并显示输出结果
- **GitHub CLI**：运行 `gh auth status` 并显示输出结果（用于创建和合并 Pull Request）

将所有检查结果告知用户。如果缺少任何工具，请明确告知他们如何安装，并在问题解决之前停止操作。

## 第一步 — 确定目标项目

询问用户：

> 您是在改进现有的项目（选项 **(a)**，还是从零开始创建新项目（选项 **(b)**？

### 选项 A：现有项目

1. 询问：“您的项目位于哪里？” 接受用户提供的路径。如果用户回答“当前目录”，则使用 `cwd`（当前工作目录）。
2. 告知用户，您将在他们的项目目录中读取配置文件以检测项目设置。仅检查用户提供的目录内的文件，不要扫描其他目录。检查以下文件：
   - **类型**：`tsconfig.json` → TypeScript；`vite.config.ts` → Vite；`next.config.*` → Next.js；`serverless.yml` → Serverless
   - **包管理器**：`package-lock.json` → npm；`yarn.lock` → yarn；`pnpm-lock.yaml` → pnpm
   - **构建/测试命令**：查看 `package.json` 中的 `build`、`test`、`lint`、`typecheck` 脚本
   - **源代码目录**：默认为 `src/`（如果存在）
   - **目标分支**：检查 `git symbolic-ref refs/remotes/origin/HEAD`，或确认是否使用 `main` 或 `master` 分支
3. 展示检测到的所有信息，并在继续之前获得用户的确认。
4. 询问：“该项目是否包含其他相关仓库？” 如果是，请对每个相关仓库重复上述检测过程。

### 选项 B：新项目

建议用户在继续之前先创建项目框架并进行初始化。根据用户要构建的技术栈，推荐合适的工具：
- React + Vite：`npm create vite@latest {name} -- --template react-ts`
- Next.js：`npx create-next-app@latest {name} --typescript`
- Express：手动创建 `package.json` 和 `src/index.ts`

用户还需要初始化 Git 并创建一个 GitHub 仓库：

```
cd {name}
git init && git add . && git commit -m "Initial scaffold"
gh repo create {name} --public --source . --push
```

**请勿代表用户运行这些命令。** 在用户确认项目已创建并连接到 GitHub 仓库后，再继续下一步。

## 第二步 — 生成 `projects.yaml` 文件

在 OpenTangl 的根目录下创建 `projects.yaml` 文件。每个项目条目需要包含以下信息：

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

**支持的类型**：`typescript-node`、`serverless-js`、`serverless-ts`、`react-vite`、`react-next`、`express`（或其他描述性字符串）。

对于**多项目设置**，可以添加一个 `environment` 字段，将相关项目归类到同一个开发愿景下：

```yaml
  - id: my-api
    environment: my-product
    # ...
  - id: my-frontend
    environment: my-product
    # ...
```

## 第三步 — 创建愿景文档

在 `docs/environments/{environment}/product-vision.md` 文件中创建项目愿景文档（对于单个项目，使用项目 ID 作为环境名称；对于多项目设置，使用 `environment` 字段）。

愿景文档包含两个部分：

### 起源与方向（由用户编写，OpenTangl 不会修改）

请用户描述：
- **项目简介**：关于项目的 2-3 句描述
- **长期发展方向**：未来 6-12 个月的规划
- **最重要的原则**：指导项目决策的 3-5 个原则

### 当前优先事项（每次运行后由 OpenTangl 维护）

询问用户：“您希望首先实现或改进的 3-5 个目标是什么？”

将这些目标记录为“活跃任务”：

```markdown
### Active Initiatives

1. **{Priority}** — {What and why}
   - Status: not started
```

如果用户不确定，可以建议他们查看项目代码库并协助确定优先事项。

## 第四步 — 配置大型语言模型（LLM）

用户需要在 OpenTangl 的根目录下创建一个 `.env` 文件，并填写自己的 API 密钥。**请勿直接接收或处理用户的 API 密钥**——只需提供模板，让用户自行创建文件。

首先，通过读取项目中的 `.gitignore` 文件来确认 `.env` 文件是否已被包含在其中。如果没有，请将其添加到 `.gitignore` 文件中，并告知用户。

然后提供相应的模板供用户填写：

**对于 OpenAI：**
```
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o
DEFAULT_AGENT=openai
```

**对于 Anthropic (Claude)：**
```
ANTHROPIC_API_KEY=sk-ant-...
ANTHROPIC_MODEL=claude-sonnet-4-20250514
DEFAULT_AGENT=anthropic
```

告知用户：“在 OpenTangl 的根目录下创建一个 `.env` 文件，并粘贴上述模板中的其中一个，然后填写您的 API 密钥。该文件会被 Git 忽略，不会被提交到代码库中。”

等待用户的确认后再继续下一步。

## 第五步 — 准备首次运行

初始化一个空的任务队列：

```bash
mkdir -p tasks
echo "tasks: []" > tasks/queue.yaml
```

然后向用户提供启动自动化开发流程的命令。**请勿代表用户运行此命令**——只需将命令展示给用户，让他们自行执行：

对于单个项目：
```
npx tsx src/cli.ts autopilot --projects {project-id} --cycles 1 --feature-ratio 0.8
```

对于多项目设置：
```
npx tsx src/cli.ts autopilot --projects {api-id},{ui-id} --cycles 1 --feature-ratio 0.8
```

**自动化流程的工作流程：**
1. OpenTangl 读取愿景文档并扫描项目代码库
2. 提出符合愿景要求的任务
3. 执行每个任务（编写代码、运行验证）
4. 创建 Pull Request（PR），并与大型语言模型（LLM）一起审查这些任务
5. 如果代码无误，将 PR 提交到代码库并合并
6. 更新愿景文档以反映项目进展

建议用户在首次运行后查看结果——检查生成的 Pull Request 和更新后的愿景文档。

## 故障排除：

- **“没有待处理的任务”**：任务队列为空。运行自动化流程以让大型语言模型提出任务，或向愿景文档中添加更具体的优先事项。
- **构建失败**：OpenTangl 会尝试最多 3 次，如果所有尝试都失败，则将任务标记为失败并跳过。
- **需要人工处理的 Pull Request**：大型语言模型审查者指出了关键问题。请查看 GitHub 上生成的 issue 以获取详细信息。
- **“需要 OPENAI_API_KEY”**：请创建 `.env` 文件并填写 API 密钥（参见第 4 步）。
- **合并冲突**：OpenTangl 具有内置的冲突解决机制。如果无法自动解决冲突，PR 会被提交给用户进行人工审核。