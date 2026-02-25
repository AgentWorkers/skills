---
name: opentangl
description: 这不仅仅是一个代码生成工具，而是一个完整的开发团队。只需将其指向任何 JavaScript/TypeScript 项目以及产品的愿景，它就能自动完成以下任务：规划功能、编写代码、验证构建结果、创建 Pull Request（PR）、审查代码差异，并最终完成代码合并。它能够像管理一个完整产品一样同时管理多个代码仓库。当你希望无需亲自编写代码就能发布产品时，就可以使用它。
homepage: https://github.com/8co/opentangl
metadata: {"clawdbot":{"emoji":"🤖","requires":{"bins":["node","git","gh"],"env":["OPENAI_API_KEY"]},"primaryEnv":"OPENAI_API_KEY"}}
---
# OpenTangl

该技能可为任何 JavaScript/TypeScript 项目配置一个自动化的开发循环。它能够检测项目的设置情况，生成相应的配置文件，并使 OpenTangl 能够自主运行。

## 先决条件

在使用此技能之前，用户必须已经克隆并安装了 OpenTangl。如果用户尚未安装，请为他们执行以下命令：

```
git clone https://github.com/8co/opentangl.git
cd opentangl
npm install
```

**请勿代用户运行这些命令**。请等待用户确认 OpenTangl 已成功安装。

确认安装完成后，检查用户是否具备以下工具：
- **Node.js** ≥ 18：运行 `node --version` 并显示输出结果
- **git**：运行 `git --version` 并显示输出结果
- **GitHub CLI**：运行 `gh auth status` 并显示输出结果（用于创建和合并 Pull Request）

将所有检查结果告知用户。如果缺少任何工具，请明确告知他们如何安装，并等待问题解决后再继续。

## 第一步 — 确定目标项目

询问用户：
> 您是想要改进现有的项目（选项 **(a)**，还是从零开始创建一个新项目（选项 **(b)**？

### 选项 A：现有项目

1. 询问：“您的项目位于哪里？”接受用户提供的路径。如果用户回答“当前目录”，则使用 `cwd`（当前工作目录）。
2. 告知用户，系统会读取项目目录中的配置文件以检测项目设置。仅检查用户提供的目录内的文件，不要扫描其他位置。需要检查的文件包括：
   - **类型**：`tsconfig.json`（TypeScript 项目）、`vite.config.ts`（Vite 项目）、`next.config.*`（Next.js 项目）、`serverless.yml`（Serverless 项目）
   - **包管理器**：`package-lock.json`（npm 项目）、`yarn.lock`（yarn 项目）、`pnpm-lock.yaml`（pnpm 项目）
   - **构建/测试命令**：查看 `package.json` 中的 `build`、`test`、`lint`、`typecheck` 脚本
   - **源代码目录**：默认为 `src/`（如果存在）
   - **目标分支**：检查 `git symbolic-ref refs/remotes/origin/HEAD`，或判断是否使用 `main` 分支或 `master` 分支
3. 展示检测到的所有信息，并在继续之前获得用户的确认。
4. 询问：“该项目是否还关联有其他代码仓库？”如果有其他仓库，请对每个仓库重复上述检测流程。

### 选项 B：新项目

建议用户在继续之前先搭建并初始化项目。根据用户的项目类型，推荐相应的工具：
- **React + Vite**：使用 `npm create vite@latest {name} -- --template react-ts`
- **Next.js**：使用 `npx create-next-app@latest {name} --typescript`
- **Express**：用户需要手动创建 `package.json` 和 `src/index.ts`

用户还需要初始化 Git 并创建一个 GitHub 仓库：

```
cd {name}
git init && git add . && git commit -m "Initial scaffold"
gh repo create {name} --public --source . --push
```

**请勿代用户运行这些命令**。在用户确认项目已创建并关联了 GitHub 仓库后，再继续下一步。

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

支持的项目类型包括：`typescript-node`、`serverless-js`、`serverless-ts`、`react-vite`、`react-next`、`express`（或其他描述性字符串）。

对于 **多项目环境**，可以添加一个 `environment` 字段，将相关项目归类到同一个开发愿景下：

```yaml
  - id: my-api
    environment: my-product
    # ...
  - id: my-frontend
    environment: my-product
    # ...
```

## 第三步 — 创建项目愿景文档

在 `docs/environments/{environment}/product-vision.md` 文件中编写项目愿景文档（对于单个项目，使用项目 ID 作为环境名称；对于多项目环境，使用 `environment` 字段）。

愿景文档包含两个部分：

### 项目起源与发展方向（由用户编写，OpenTangl 不会修改）

请用户描述：
- **项目简介**：用 2-3 句话介绍该项目
- **长期发展方向**：描述项目在未来 6-12 个月内的发展目标
- **核心原则**：列出指导项目决策的 3-5 个重要原则

### 当前优先事项（由 OpenTangl 在每次运行后维护）

询问用户：“您希望首先实现或改进的 3-5 个目标是什么？”

将这些目标记录为“活跃任务”（Active Initiatives）：

```markdown
### Active Initiatives

1. **{Priority}** — {What and why}
   - Status: not started
```

如果用户不确定，可以建议他们查看项目代码库并协助确定优先事项。

## 第四步 — 配置大型语言模型（LLM）

用户需要在 OpenTangl 的根目录下创建一个 `.env` 文件，并填写自己的 API 密钥。**请勿直接接收或处理用户的 API 密钥**——只需提供模板，让用户自行创建文件。

首先，通过读取 `.gitignore` 文件来确认 `.env` 文件是否已被包含在项目的排除列表中。如果没有，请将其添加到 `.gitignore` 文件中，并告知用户。

然后提供相应的模板供用户填写：
- **对于 OpenAI**：
```
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o
DEFAULT_AGENT=openai
```

- **对于 Anthropic (Claude)**：
```
ANTHROPIC_API_KEY=sk-ant-...
ANTHROPIC_MODEL=claude-sonnet-4-20250514
DEFAULT_AGENT=anthropic
```

告知用户：“在 OpenTangl 的根目录下创建一个 `.env` 文件，并将上述模板中的内容替换为自己的 API 密钥。该文件会被 Git 忽略，因此不会被提交到代码库。”

等待用户确认后再继续下一步。

## 第五步 — 准备首次运行

初始化一个空的任务队列：

```bash
mkdir -p tasks
echo "tasks: []" > tasks/queue.yaml
```

然后向用户提供启动自动化开发流程的命令。**请勿代用户运行此命令**——只需将命令展示给用户，让他们自行执行：

- 对于单个项目：
```
npx tsx src/cli.ts autopilot --projects {project-id} --cycles 1 --feature-ratio 0.8
```

- 对于多项目环境：
```
npx tsx src/cli.ts autopilot --projects {api-id},{ui-id} --cycles 1 --feature-ratio 0.8
```

**自动化开发流程的工作流程如下：**
1. OpenTangl 读取项目愿景文档并扫描项目代码库
2. 根据愿景提出相应的开发任务
3. 执行每个任务（包括编写代码、运行测试等）
4. 提交 Pull Request（PR），并与大型语言模型（LLM）协作进行代码审查
5. 如果代码通过审查，将 PR 合并到代码库
6. 更新项目愿景文档以反映开发进度

建议用户在首次运行后查看结果，包括生成的 Pull Request 和更新后的项目愿景文档。

## 故障排除：
- **“没有待处理的任务”**：说明任务队列为空。此时可以运行自动化流程让 LLM 提出新的任务，或者用户在愿景文档中添加更具体的优先事项。
- **构建失败**：OpenTangl 会尝试最多 3 次，如果失败会显示错误信息。如果所有尝试都失败，该任务将被标记为失败并跳过。
- **需要人工处理的 Pull Request**：LLM 审查者可能指出了关键问题。请查看 GitHub 上生成的 issue 以获取详细信息。
- **“需要 OPENAI_API_KEY”**：请用户创建 `.env` 文件并填写 API 密钥（参见第 4 步）。
- **合并冲突**：OpenTangl 具有内置的冲突解决机制。如果无法自动解决冲突，PR 会被提交给用户进行人工审核。