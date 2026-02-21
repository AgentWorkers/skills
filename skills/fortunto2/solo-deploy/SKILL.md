---
name: solo-deploy
description: >
  将项目部署到托管平台：  
  - 阅读 `stack.yaml` 文件以获取详细的配置信息；  
  - 检测本地可用的 CLI 工具（如 Vercel、Wrangler、Supabase、Fly、SST 等）；  
  - 设置数据库；  
  - 推送代码；  
  - 验证部署后的效果是否正常。  
  此步骤应在用户请求“部署项目”、“将代码推送到生产环境”或 `/build` 命令执行完成后执行。  
  **请勿在构建过程完成之前执行此步骤。**
license: MIT
metadata:
  author: fortunto2
  version: "1.2.0"
  openclaw:
    emoji: "🚀"
allowed-tools: Read, Grep, Bash, Glob, Write, Edit
argument-hint: "[platform]"
---
# /deploy

将项目部署到其托管平台。系统会读取堆栈模板 YAML 文件（`templates/stacks/{stack}.yaml`）以获取详细的部署配置（包括平台、命令行工具、基础设施层、持续集成/持续交付（CI/CD）以及监控设置），检测已安装的命令行工具，配置数据库和环境，推送代码，并验证部署是否成功。

## 参考文档

- `templates/principles/dev-principles.md` — 持续集成/持续交付（CI/CD）相关原则、密钥管理、DNS 配置以及共享基础设施规则（适用于 solo-factory 模型）
- `templates/stacks/*.yaml` — 包含部署、基础设施、CI/CD 和监控设置的信息的堆栈模板（适用于 solo-factory 模型）

> 路径都是相对于 `solo-factory/` 目录的。如果文件不存在，可以尝试在 `1-methodology/` 目录下查找（该目录包含 solopreneur 相关的符号链接）。

## 使用时机

在 `/build` 阶段完成所有任务后执行此步骤。`/deploy` 是负责实际部署的环节。

部署流程：`/build` → **`/deploy`** → `/review`

## 可用的 MCP 工具（如有）

- `session_search(query)` — 查找之前类似项目的部署方式
- `project_code_search(query, project)` — 在不同项目中查找部署模式
- `codegraph_query(query)` — 检查项目依赖关系和堆栈配置

如果 MCP 工具不可用，可以退而使用全局搜索（Glob + Grep）和手动读取配置文件的方法。

## 部署前的检查

### 1. 确认构建已完成
- 检查 `.solo/states/build` 文件是否存在。如果不存在，提示“构建未完成，请先运行 `/build`”。

### 2. 检测可用的命令行工具

并行执行以下操作以检测本地已安装的命令行工具：
```bash
vercel --version 2>/dev/null && echo "VERCEL_CLI=yes" || echo "VERCEL_CLI=no"
wrangler --version 2>/dev/null && echo "WRANGLER_CLI=yes" || echo "WRANGLER_CLI=no"
npx supabase --version 2>/dev/null && echo "SUPABASE_CLI=yes" || echo "SUPABASE_CLI=no"
fly version 2>/dev/null && echo "FLY_CLI=yes" || echo "FLY_CLI=no"
sst version 2>/dev/null && echo "SST_CLI=yes" || echo "SST_CLI=no"
gh --version 2>/dev/null && echo "GH_CLI=yes" || echo "GH_CLI=no"
```

记录下所有可用的工具。如果工具已经全局安装，可以直接使用，无需通过 `npx` 命令来调用它们。

### 3. 加载项目配置信息（并行读取）

- `CLAUDE.md` — 堆栈名称、架构和部署平台信息
- `docs/prd.md` — 产品需求和部署说明
- `docs/workflow.md` — 持续集成/持续交付（CI/CD）策略（如果存在）
- `package.json` 或 `pyproject.toml` — 项目依赖关系和脚本信息
- `fly.toml`, `wrangler.toml`, `sst.config.ts` — 平台配置文件（如果存在）
- `docs/plan/*/plan.md` — 当前的部署计划（查找与部署相关的阶段或任务）

**基于计划的部署：** 如果当前部署计划中包含了具体的部署步骤（例如“将 Python 后端部署到 VPS 上”、“运行 deploy.sh 命令”或“在服务器上设置 Docker”），这些步骤应被视为主要的部署指令。部署计划会指定项目特有的部署目标，而这些目标可能不会在通用的堆栈配置文件中体现。因此，在执行标准平台部署操作的同时或替代标准操作时，还需要执行计划中的部署任务。

### 4. 读取堆栈模板 YAML 文件

从 `CLAUDE.md` 文件中提取堆栈名称（通常位于 `stack:` 字段或相关的技术堆栈描述部分）。

读取堆栈模板文件以获取详细的部署配置：

**查找顺序**（先找到哪个文件就使用哪个）：
1. `templates/stacks/{stack}.yaml` — 位于当前技能对应的仓库（solo-factory）内
2. `1-methodology/stacks/{stack}.yaml` — 可能是 solopreneur 文档中的符号链接
3. `.solo/stacks/{stack}.yaml` — 用户本地自定义的配置文件（来自 `/init` 目录）

从 YAML 文件中提取以下配置信息：
- `deploy` — 部署目标平台（例如 `vercel`, `cloudflare_workers`, `cloudflare_pages`, `fly.io`, `docker`, `app_store`, `play_store`, `local`）
- `deploy_cli` — 命令行工具及其使用场景（例如 `vercel` 可用于本地预览或环境变量配置）
- `infra` — 基础设施工具和层级（例如 `sst.config.ts` 中定义的层级）
- `ci_cd` — 持续集成/持续交付系统（例如 `github_actions`）
- `monitoring` — 监控工具（例如 `posthog`）
- `database` / `orm` — 数据库和对象关系映射（ORM）配置（如果需要迁移）
- `storage` — 存储服务配置（例如 R2、D1、KV 等）
- `notes` — 堆栈特定的部署说明

**所有部署决策应以 YAML 文件中的配置为准**。YAML 文件中的配置会覆盖默认的配置设置。

### 5. 检测部署平台（如果 YAML 文件不存在则使用默认配置）

如果未找到堆栈配置文件，将使用以下默认配置矩阵：

| 堆栈名称 | 部署平台 | 技术层级 |
|-------|----------|------|
| `nextjs-supabase` / `nextjs-ai-agents` | Vercel + Supabase | 第 1 层 |
| `cloudflare-workers` | Cloudflare Workers | 第 1 层 |
| `astro-static` / `astro-hybrid` | Cloudflare Pages | 第 1 层 |
| `python-api` | Fly.io（快速部署）或 Pulumi + Hetzner（生产环境） | 第 2/4 层 |
| `python-ml` | 跳过（无需使用命令行工具） | — |
| `ios-swift` | 跳过（应用发布需要手动操作） | — |
| `kotlin-android` | 跳过（应用发布需要手动操作） | — |

如果 `$ARGUMENTS` 参数指定了具体的部署平台，优先使用该参数的值，而不是默认配置。

**自动部署平台**（根据 YAML 文件中的 `deploy` 字段或默认配置）：
- `vercel` / `cloudflare_pages` — 推送代码后自动部署。如果项目已经关联到相应的 GitHub 仓库，只需执行推送操作即可。初次部署时可能需要手动执行部署命令。
- `cloudflare-workers` — 需要使用 `wrangler deploy` 命令进行部署。
- `fly.io` — 需要执行 `fly deploy` 命令。

## 部署步骤

### 第 1 步：Git — 清理代码并推送更改

```bash
git status
git log --oneline -5
```

如果代码有未提交的更改，请先提交这些更改：
```bash
git add -A
git commit -m "chore: pre-deploy cleanup"
```

确保远程仓库存在并执行推送操作：
```bash
git remote -v
git push origin main
```

如果远程仓库不存在，请创建一个新的 GitHub 仓库：
```bash
gh repo create {project-name} --private --source=. --push
```

**对于支持自动部署的平台（如 Vercel 或 Cloudflare Pages）：** 推送代码后部署会自动触发。如果项目已经关联到 GitHub 仓库，可以跳过手动部署步骤。

### 第 2 步：配置数据库

- **如果项目中包含 `supabase/` 目录或检测到 Supabase 依赖关系**，则执行相应的数据库配置步骤：
```bash
# If supabase CLI available:
supabase db push          # apply migrations
supabase gen types --lang=typescript --local > db/types.ts  # optional: regenerate types
```
如果系统中没有相应的命令行工具，引导用户通过 Supabase 控制台进行数据库迁移。

- **如果项目中包含 `drizzle.config.ts` 文件**，则执行 Drizzle ORM 的配置步骤：
```bash
npx drizzle-kit push      # push schema to database
npx drizzle-kit generate  # generate migration files (if needed)
```

- **如果 `wrangler.toml` 文件中配置了 D1 数据库服务**，则执行相应的配置步骤：
```bash
wrangler d1 migrations apply {db-name}
```

如果数据库配置尚未完成，列出所需的信息后继续下一步操作——不要因此阻塞整个部署流程。

### 第 3 步：设置环境变量

读取 `.env.example` 或 `.env.local.example` 文件以确定所需的环境变量。

生成针对特定平台的配置指令：

- **Vercel：**
```bash
# If vercel CLI is available and project is linked:
vercel env ls  # show current env vars

# Guide user:
echo "Set env vars: vercel env add VARIABLE_NAME"
echo "Or via dashboard: https://vercel.com/[team]/[project]/settings/environment-variables"
```

- **Cloudflare：**
```bash
wrangler secret put VARIABLE_NAME  # interactive prompt for value
# Or in wrangler.toml [vars] section for non-secret values
```

- **Fly.io：**
```bash
fly secrets set VARIABLE_NAME=value
fly secrets list
```

**请注意：** 不要直接创建或修改包含敏感信息的 `.env` 文件。应让用户自行设置环境变量。

### 第 4 步：执行平台部署

- **如果 Vercel 不支持自动部署**，则执行相应的部署步骤：
```bash
vercel link          # first time: link to project
vercel               # deploy preview
vercel --prod        # deploy production (after verifying preview)
```

- **对于 Cloudflare Workers/Pages：** 执行相应的部署步骤：
```bash
wrangler deploy              # Workers
wrangler pages deploy ./out  # Pages (check build output dir)
```

- **对于 Fly.io：** 执行相应的部署步骤：
```bash
fly launch   # first time — creates app, sets region
fly deploy   # subsequent deploys
```

- **如果项目中包含 `sst.config.ts` 文件**，则执行相应的部署步骤：
```bash
sst deploy --stage prod    # production
sst deploy --stage dev     # staging
```

### 第 5 步：验证部署结果

部署完成后，验证系统是否正常运行：

```bash
# 1. HTTP status check
STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://{deployment-url})

# 2. Check for runtime errors in page body
BODY=$(curl -s https://{deployment-url} | head -200)

# 3. Check Vercel deployment logs for errors
vercel logs --output=short 2>&1 | tail -30
```

**如果 HTTP 状态码不是 200，或者页面显示错误信息：**
1. 检查 `vercel env ls` 命令，确认所有必要的环境变量是否都已设置。
2. 如果有环境变量缺失，使用 `vercel env add NAME production <<< "value"` 命令添加它们。
3. 如果环境变量设置错误，使用 `vercel env rm NAME production` 命令删除错误的变量，然后重新添加。
4. 修复环境变量后，使用 `vercel --prod --yes` 命令重新部署。
5. 重新检查 HTTP 状态码和页面内容。

**常见的运行时错误及解决方法：**
- “需要 Supabase URL/Key” → 在 Vercel 配置中添加 `NEXT_PUBLIC_SUPABASE_URL` 和 `NEXT_PUBLIC_SUPABASE_ANON_KEY`。
- “DATABASE_URL 未设置” → 在 Vercel 配置中添加 `DATABASE_URL`。
- “缺少 Stripe 密钥” → 添加相应的密钥或删除相关的代码。
- 页面为空或显示错误信息 → 检查构建日志，可能需要使用 `vercel --prod` 命令重新部署。

**只有在页面显示 HTTP 200 状态码且页面正常加载后，才能输出 `<solo:done/>`。** 如果问题无法解决，请输出 `<solo:redo/>` 以返回到构建阶段。

### 第 6 步：部署后的日志监控

验证部署成功后，通过查看生产环境的日志来捕获可能在实际运行环境中出现的错误（例如环境变量缺失、数据库连接问题、服务器崩溃或 API 超时）。

根据堆栈配置文件中的 `logs` 字段执行相应的日志检查命令：

- **Vercel（Next.js）：**
  ```bash
vercel logs --output=short 2>&1 | tail -50
```
  查找 `Error`, `FUNCTION_INVOCATION_FAILED`, `EDGE_FUNCTION_INVOCATION_FAILED`, `504 GATEWAY_TIMEOUT`, `unhandled rejections` 等错误。

- **Cloudflare Workers：**
  ```bash
wrangler tail --format=pretty 2>&1 | head -100
```
  查找 `Error`, 未捕获的异常、D1 查询失败或访问错误。

- **Cloudflare Pages（Astro）：**
  ```bash
wrangler pages deployment tail --project-name={name} 2>&1 | head -100
```

- **Fly.io（Python API）：**
  ```bash
fly logs --app {name} 2>&1 | tail -50
fly status --app {name}
```
  查找 `ERROR`, `CRITICAL`, 不健康的实例或连接错误。

- **如果使用了 Supabase Edge Functions：**
  ```bash
supabase functions logs --scroll 2>&1 | tail -30
```

**处理日志错误的方法：**
  - **环境变量缺失** → 使用相应的命令行工具进行修复（参见第 3 步），然后重新部署。
  - **数据库连接错误** → 检查连接字符串或 IP 允许列表。
  - **运行时崩溃或未处理的错误** → 输出 `<solo:redo/>` 以返回到构建阶段进行修复。
  - 如果 30 行日志中都没有错误记录，说明部署成功，可以继续下一步操作。

**如果新部署后没有流量，请发送几个测试请求：**
```bash
curl -s https://{deployment-url}/           # homepage
curl -s https://{deployment-url}/api/health  # API health (if exists)
```
然后再次检查日志，确认没有新的错误出现。

### 第 7 步：生成部署报告

```
Deployment: {project-name}

  Platform:  {platform}
  URL:       {deployment-url}
  Branch:    main
  Commit:    {sha}

  Done:
    - [x] Code pushed to GitHub
    - [x] Deployed to {platform}
    - [x] Database migrations applied (or N/A)

  Manual steps remaining:
    - [ ] Set environment variables (listed above)
    - [ ] Custom domain (optional)
    - [ ] PostHog / analytics setup (optional)

  Next: /review — final quality gate
```

## 部署完成

**仅当部署成功时输出以下标记**：
```
<solo:done/>
```
**请注意：** 此标记只能输出一次——系统会在检测到第一次部署成功时输出该标记。** 不要在响应的其他地方重复输出该标记。**

## 错误处理

### 命令行工具未找到
**原因：** 相应的命令行工具未安装。
**解决方法：** 安装相应的工具：`npm i -g vercel`, `npm i -g wrangler`, `brew install flyctl`, `brew install supabase/tap/supabase`。

### 部署失败
**原因：** 本地构建成功，但在目标平台上失败（可能是 Node 版本不同或环境变量缺失）。
**解决方法：** 查看平台的构建日志，确保 `package.json` 中指定的构建工具与目标平台匹配，并设置缺失的环境变量。

### 数据库连接失败
**原因：** `DATABASE_URL` 未设置或网络配置问题导致连接失败。
**解决方法：** 检查连接字符串和平台的数据库配置信息。

### Git 推送失败
**原因：** 远程仓库与本地仓库的代码不一致。
**解决方法：** 执行 `git pull --rebase origin main` 命令解决冲突，然后再次推送代码。

## 部署验证

在报告部署成功之前，请执行以下操作：
1. 使用 `curl -s -o /dev/null -w "%{http_code}"` 命令检查部署 URL 的响应状态。
2. 确认 HTTP 状态码为 200（而不是 404、500 或重定向循环）。
3. 确认页面内容符合预期（不是空白页面或显示错误信息）。
4. 确认所有条件都满足后，才能报告部署成功。

**重要规则：**
1. **必须使用已安装的命令行工具**——在尝试其他方法之前，确保已安装 `vercel`, `wrangler`, `supabase`, `fly`, `sst` 等工具。
2. **了解自动部署功能**——如果平台支持自动部署，只需执行推送操作，无需手动执行部署命令。
3. **切勿直接在代码中存储敏感信息**——不要在 `.env` 文件中保存敏感环境变量或 API 密钥。
4. **先进行预览部署**——先进行预览部署，验证后再推进到生产环境。
5. **先在本地进行构建测试**——在部署前使用 `pnpm build` 或 `uv build`（或其他等效命令）进行测试。
6. **部署后务必查看日志**——在确认部署成功之前，务必检查日志以捕获运行时出现的错误。
7. **提供完整的部署信息**——包括部署 URL 和平台控制台的链接。
8. **优先使用配置文件**——建议使用 `sst.config.ts` 或 `fly.toml` 作为基础设施配置文件，而不是手动配置。
9. **确认部署成功后再宣布**——确认部署 URL 返回 HTTP 200 状态码，并且日志显示正常信息，而不仅仅是“部署命令成功”。
10. **严格遵守这些规则**，以确保部署的稳定性和安全性。