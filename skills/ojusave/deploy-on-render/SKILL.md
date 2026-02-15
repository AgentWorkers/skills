---
name: render
description: 在 Render 平台上部署和运行应用程序（使用蓝图（Blueprint）以及一键式仪表板深度链接，流程与 Codex 的渲染-部署流程相同）。适用于用户需要部署、托管或发布应用程序的情况；可以创建或编辑 `render.yaml` 文件；可以添加 Web 服务、静态资源、工作进程（workers）、定时任务（cron）、Postgres 数据库或键值存储（Key Value storage）；可以通过获取蓝图的深度链接来进行部署；当设置了 `RENDER_API_KEY` 时，可以通过 API 触发或验证部署过程；还可以通过 `mcporter` 连接到 Render 的 MCP 以直接创建服务；此外，还可以配置环境变量（env vars）、健康检查（health checks）、扩展能力（scaling）、预览功能（previews）以及项目设置（projects）。
metadata:
  { "openclaw": { "emoji": "☁️", "homepage": "https://render.com/docs", "version": "1.0.0" } }
---

# 在 Render 上部署应用程序

您可以使用蓝图（`render.yaml`）、仪表板或 API 在 Render 上部署和管理应用程序。此技能遵循 **Codex render-deploy** 流程：分析代码库 → 生成/验证蓝图 → 提交并推送 → 通过仪表板的一键链接进行部署 → 可选地通过 API 或 mcporter 进行验证或重新部署。

## 何时使用此技能

当用户希望执行以下操作时，请激活此技能：
- 在 Render 上部署、托管或发布应用程序
- 创建或编辑 `render.yaml` 蓝图（新的或现有的仓库）
- 添加 Web 服务、静态站点、私有服务、工作进程、定时任务；Postgres 数据库；或键值存储（Key Value）
- 配置环境变量、健康检查、扩展性设置、磁盘配置或区域选择
- 设置预览环境或项目
- 验证蓝图或获取仪表板/API 链接

## 部署方法选择

1. **如果设置了 `RENDER_API_KEY`** → 建议使用 REST API 或 MCP（最快；无需用户点击）。有关请求体的信息，请参阅 `references/rest-api-deployment.md`；如果配置了 mcporter，请参阅 `references/mcp-integration.md`。
2. **如果没有 API 密钥** → 使用蓝图 + 一键链接（用户提交并推送，然后点击链接进行部署）。

**检查 API 密钥：**

```bash
[ -n "$RENDER_API_KEY" ] && echo "RENDER_API_KEY is set" || echo "RENDER_API_KEY is not set"
```

## 新用户的快速入门流程

在进行深入分析之前，使用以下简短步骤来减少操作难度：
1. 询问用户是否希望从 **Git 仓库** 进行部署（对于蓝图和一键链接是必需的），或者仅获取指导。如果没有 Git 远程仓库，用户必须先创建一个并推送它。
2. 询问应用程序是否需要数据库、工作进程、定时任务或其他服务，以便选择合适的蓝图类型。

然后按照以下步骤进行操作：**部署到 Render**（蓝图 → 推送 → 一键链接 → 验证）。

## 先决条件检查

1. **Git 远程仓库** – 部署蓝图所必需。运行 `git remote -v`；如果没有，请用户创建一个 GitHub/GitLab/Bitbucket 仓库，并添加 `origin`，然后推送。
2. **Render CLI（可选）** – 用于本地验证：`render blueprints validate render.yaml`。安装方法：`brew install render` 或 [Render CLI](https://github.com/render-oss/cli)。
3. **API 密钥（可选）** – 用于验证部署或触发重新部署：[仪表板 → API 密钥](https://dashboard.render.com/u/*/settings#api-keys)。在环境中设置 `RENDER_API_KEY`。

## 安全注意事项

- **切勿将密钥提交到 `render.yaml` 中** — 对于 API 密钥、密码和令牌，始终使用 `sync: false`；用户应在仪表板中输入这些信息。
- **在建议部署之前进行验证** — 运行 `render blueprints validate render.yaml` 或使用 [验证蓝图 API](https://api-docs.render.com/reference/validate-blueprint) 来确保无效的 YAML 不会被推送。
- **验证用户提供的值** — 在将用户输入的环境变量或服务名称写入 YAML 时，根据需要进行清理或引用，以避免注入攻击。

## 参考资料

- `references/codebase-analysis.md`（检测运行时、构建/启动命令、环境变量）
- `references/blueprint-spec.md`（根级键、服务类型、环境变量、验证）
- `references/rest-api-deployment.md`（直接通过 API 创建服务：所有者 ID、请求体、类型映射）
- `references/mcp-integration.md`（Render MCP 工具、mcporter 的使用方法、支持的运行时/计划/区域）
- `references/post-deploy-checks.md**（通过 API 验证部署状态和健康状况）
- `references/troubleshooting-basics.md`（构建/启动/运行时故障排除）
- `assets/`（示例蓝图：`node-express.yaml`、`python-web.yaml`、`static-site.yaml`、`web-with-postgres.yaml`）

## 蓝图基础

- **文件：** `render.yaml` 必须位于 Git 仓库的 **根目录**。
- **根级键（官方规范）：** `services`、`databases`、`envVarGroups`、`projects`、`ungrouped`、`previews.generation`、`previews.expireAfterDays`。
- **规范：** [蓝图 YAML 参考文档](https://render.com/docs/blueprint-spec)。IDE 验证的 JSON 架构：https://render.com/schema/render.yaml.json（例如，在 VS Code/Cursor 中使用 YAML 扩展名）。

**验证：** 使用 `render blueprints validate render.yaml`（Render CLI v2.7.0+），或 [验证蓝图 API](https://api-docs.render.com/reference/validate-blueprint)。

## 服务类型

| 类型       | 目的                          |
|------------|------------------------------|
| `web`      | 公共 HTTP 应用程序或静态站点（静态站点使用 `runtime: static`） |
| `pserv`    | 私有服务（仅限内部主机名，无公共 URL）         |
| `worker`   | 后台工作进程（持续运行，例如作业队列）             |
| `cron`     | 定时任务（使用 cron 表达式；运行后退出）             |
| `keyvalue` | Render 的键值存储实例（兼容 Redis/Valkey；在 `services` 中定义） |

**注意：** 私有服务使用 `pserv`，而不是 `private`。键值存储服务使用 `type: keyvalue`；在新蓝图中不要使用单独的根级键（一些旧蓝图使用 `keyValueStores` 和 `fromKeyValueStore`——建议使用官方格式）。

## 运行时

建议使用 **`runtime`（推荐；`env` 已弃用）**：`node`、`python`、`elixir`、`go`、`ruby`、`rust`、`docker`、`image`、`static`。对于静态站点：需要设置 `type: web` 和 `runtime: static`，以及 `staticPublishPath`（例如 `./build` 或 `./dist`）。

## 最小化 Web 服务配置示例

```yaml
services:
  - type: web
    name: my-app
    runtime: node
    buildCommand: npm install
    startCommand: npm start
    envVars:
      - key: NODE_ENV
        value: production
```

Python 示例：`runtime: python`，`buildCommand: pip install -r requirements.txt`，`startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT`（或使用 gunicorn）。根据需要，在环境变量中设置 `PYTHON_VERSION` / `NODE_VERSION`。

## 静态站点配置示例

```yaml
- type: web
  name: my-blog
  runtime: static
  buildCommand: yarn build
  staticPublishPath: ./build
```

可选：`headers`、`routes`（重定向/重写规则）。详情请参阅 [静态站点文档](https://render.com/docs/static-sites)。

## 环境变量

- **字面值：** `key` + `value`（切勿硬编码密钥）。
- **来自 Postgres：** `fromDatabase.name` + `fromDatabase.property`（例如 `connectionString`）。
- **来自键值存储或其他服务：** `fromService.type` + `fromService.name` + `fromService.property`（例如 `connectionString`、`host`、`port`、`hostport`）或 `fromService.envVarKey`（来自其他服务的环境变量）。
- **密钥/用户设置：** `sync: false`（首次创建时在仪表板中提示用户设置；之后可以手动添加新密钥）。**不能在环境变量组中使用。**
- **生成的值：** `generateValue: true`（256 位 Base64 值）。
- **共享：** `fromGroup: <envVarGroups[].name>` 用于关联环境变量组。

**环境变量组** **不能** 引用其他服务（组内不能使用 `fromDatabase`/`fromService`），也不能使用 `sync: false`。将密钥和数据库/键值存储引用放在 **服务级别的** `envVars` 中，或者同时引用组和服务特定的变量。

## 数据库（Render 使用 Postgres）

```yaml
databases:
  - name: my-db
    plan: basic-256mb
    databaseName: my_app
    user: my_user
    region: oregon
    postgresMajorVersion: "18"
```

**当前计划：** `free`、`basic-256mb`、`basic-1gb`、`basic-4gb`、`pro-*`、`accelerated-*`。旧计划：`starter`、`standard`、`pro`、`pro plus`（旧计划不支持新数据库）。可选：`diskSizeGB`、`ipAllowList`、`readReplicas`、`highAvailability.enabled`。在服务配置中引用：`fromDatabase.name`、`property: connectionString`。

## 键值存储（Redis/Valkey）

键值存储实例是类型为 `keyvalue` 的服务（或已弃用的 `redis`）。**`ipAllowList` 是必需的**：使用 `[]` 表示仅限内部访问，或者使用 `- source: 0.0.0.0/0` 表示允许外部访问。

```yaml
services:
  - type: keyvalue
    name: my-cache
    ipAllowList:
      - source: 0.0.0.0/0
        description: everywhere
    plan: free
    maxmemoryPolicy: allkeys-lru
```

在另一个服务中的引用：`fromService.type: keyvalue`，`fromService.name: my-cache`，`property: connectionString`。策略：`allkeys-lru`（缓存）、`noeviction`（作业队列）等。详情请参阅 [键值存储文档](https://render.com/docs/key-value)。

**注意：** 一些仓库使用根级别的 `keyValueStores` 和 `fromKeyValueStore`；新蓝图建议使用官方的 `services` + `fromService` 格式。

## 定时任务

`schedule` 是一个 cron 表达式（格式为分钟:小时:日期:星期几）。`buildCommand` 是必需的（如果没有构建任务，则设置为 `"true"`）。免费计划不支持定时任务/工作进程/私有服务。

## 环境变量组

在服务之间共享变量。组内不能使用 `fromDatabase`/`fromService`/`sync: false`——只能使用字面值或 `generateValue: true`。

```yaml
envVarGroups:
  - name: app-env
    envVars:
      - key: CONCURRENCY
        value: "2"
      - key: APP_SECRET
        generateValue: true

services:
  - type: web
    name: api
    envVars:
      - fromGroup: app-env
      - key: DATABASE_URL
        fromDatabase:
          name: my-db
          property: connectionString
```

## 健康检查、区域和预部署

- **仅限 Web 服务：** 使用 `healthCheckPath: /health` 以实现零停机时间部署。
- **区域：** `region: oregon`（默认）、`ohio`、`virginia`、`frankfurt`、`singapore`（创建时设置；之后无法更改）。
- **预部署：** `preDeployCommand` 在构建完成后、启动之前运行（例如执行迁移操作）。

## 扩展性

- **手动：** `numInstances: 2`。
- **自动扩展**（专业工作空间）：`scaling.minInstances`、`scaling.maxInstances`、`scaling.targetCPUPercent` 或 `scaling.targetMemoryPercent`。持久磁盘不支持自动扩展。

## 磁盘、单仓库项目和 Docker

- **持久磁盘：** `disk.name`、`disk.mountPath`、`disk.sizeGB`（适用于 Web 服务、私有服务、工作进程）。
- **单仓库项目：** `rootDir`、`buildFilterpaths` / `buildFilter.ignoredPaths`、`dockerfilePath` / `dockerContext`。
- **Docker：** `runtime: docker`（从 Dockerfile 构建）或 `runtime: image`（从镜像仓库拉取）。需要时使用 `dockerCommand` 而不是 `startCommand`。

## 预览环境和项目

- **预览环境：** 根级别设置 `previews.generation: off | manual | automatic`，可选 `previews.expireAfterDays`。每个服务可以单独设置 `previews.generation`、`previews.numInstances`、`previews.plan`。
- **项目和环境：** 根级别设置 `projects`，其中包含 `environments`（每个项目列出 `services`、`databases`、`envVarGroups`）。用于 staging/production 环境。对于不在任何环境中的资源，可以使用 `ungrouped`。

## 常见部署模式

### 完整堆栈（Web + Postgres + 键值存储）

Web 服务使用 `fromDatabase` 连接 Postgres，使用 `fromService` 连接键值存储。在 `render.yaml` 中添加一个 `databases` 条目和一个 `type: keyvalue` 服务；从 Web 服务的 `envVars` 中引用这两个服务。示例蓝图：`assets/web-with-postgres.yaml`；添加一个键值存储服务并使用 `fromService` 连接 Redis。

### 微服务（API + 工作进程 + 定时任务）

在一个蓝图中包含多个服务：`type: web` 用于 API，`type: worker` 用于后台处理，`type: cron` 用于定时任务。共享 `envVarGroups` 或重复使用环境变量；根据运行时设置 `fromDatabase`/`fromService` 以共享数据库/Redis。所有服务使用相同的 `branch`、`buildCommand` 和 `startCommand`。

### 用于 PR 的预览环境

将根级别设置为 `previews.generation: automatic`（或 `manual`）。可选设置 `previews.expireAfterDays: 7`。每个 PR 都会获得一个预览链接；可以根据需要通过 `previews.generation`、`previews.numInstances` 或 `previews.plan` 进行自定义。

## 计划（服务类型）

`plan: free | starter | standard | pro | pro plus`（对于 Web/pserv/worker：分别为 `pro max`、`pro ultra`）。如果不需要更改，则保留默认设置 `starter`。免费计划不适用于私有服务、工作进程和定时任务。

## 仪表板和 API

- **仪表板：** https://dashboard.render.com — 新建项目 → 选择蓝图，连接仓库，然后选择 `render.yaml`。
- **键值存储：** https://dashboard.render.com/new/redis

## API 访问

要从代理程序使用 Render API（验证部署、触发部署、列出服务/日志）：

1. **获取 API 密钥：** 仪表板 → 账户设置 → [API 密钥](https://dashboard.render.com/u/*/settings#api-keys)。
2. **作为环境变量存储：** 在环境中设置 `RENDER_API_KEY`（例如 `skills.entries.render.env` 或通过进程设置环境变量）。
3. **身份验证：** 在所有请求中使用 Bearer 令牌：`Authorization: Bearer $RENDER_API_KEY`。
4. **API 文档：** https://api-docs.render.com — 服务信息、部署信息、日志、蓝图验证等。

---

# 部署到 Render（与 Codex render-deploy 技能相同的过程）

目标：通过生成蓝图来部署应用程序，然后通过仪表板的一键链接进行部署；如果用户有 `RENDER_API_KEY`，还可以通过 API 进行验证或触发部署。

## 第一步：分析代码库并创建 `render.yaml`

- 使用 `references/codebase-analysis.md` 确定运行时、构建/启动命令、环境变量和数据存储。
- 在仓库根目录下添加或更新 `render.yaml`（参见上面的蓝图部分和 `references/blueprint-spec.md`）。对于敏感信息，请使用 `sync: false`。示例请参阅 `assets/`。
- 在请求用户推送之前进行 **验证**：
  - 命令行工具：`render blueprints validate render.yaml`（安装方法：`brew install render` 或 [Render CLI](https://github.com/render-oss/cli)）。
  - 或者通过 API：使用 `POST` 请求 [验证蓝图](https://api-docs.render.com/reference/validate-blueprint) 并传递 YAML 内容。
- 在继续之前修复任何验证错误。

## 第二步：提交并推送（必需）

Render 会从 **Git 仓库** 读取蓝图文件。必须提交并推送该文件。

```bash
git add render.yaml
git commit -m "Add Render deployment configuration"
git push origin main
```

如果没有 Git 仓库，请停止操作并提示用户在 GitHub/GitLab/Bitbucket 上创建一个仓库，将其添加为 `origin`，然后推送。如果没有推送的仓库，仪表板的一键链接将无法使用。

## 第三步：通过仪表板的一键链接进行部署

获取仓库 URL 并生成蓝图链接：

```bash
git remote get-url origin
```

如果仓库地址是 **SSH** 格式，需要将其转换为 **HTTPS** 格式（Render 需要 HTTPS 链接）：

| SSH | HTTPS |
|-----|--------|
| `git@github.com:user/repo.git` | `https://github.com/user/repo` |
| `git@gitlab.com:user/repo.git` | `https://gitlab.com/user/repo` |
| `git@bitbucket.org:user/repo.git` | `https://bitbucket.org/user/repo` |

**链接格式示例：**
```
https://dashboard.render.com/blueprint/new?repo=<REPO_HTTPS_URL>
```

示例：`https://dashboard.render.com/blueprint/new?repo=https://github.com/username/my-app`

向用户提供以下操作指南：
1. 确认 `render.yaml` 文件位于仓库的根目录中（用户刚刚已经推送了该文件）。
2. **点击链接** 打开 Render 仪表板。
3. 如果需要，完成 Git 提供者的 OAuth 验证。
4. 为蓝图命名（或接受默认名称）。
5. **填写敏感环境变量**（那些设置为 `sync: false` 的变量）。
6. 审查服务/数据库设置，然后点击 **应用** 进行部署。

部署将自动开始。用户可以在仪表板中监控部署进度。

## 第四步：验证部署（可选，需要 API 密钥）

如果用户设置了 `RENDER_API_KEY`（例如在 `skills.entries.render.env` 或环境变量中），代理程序可以在用户应用蓝图后进行验证：

- **列出服务：** `GET https://api.render.com/v1/services` — 请求头：`Authorization: Bearer $RENDER_API_KEY`。通过名称查找服务。
- **列出部署结果：** `GET https://api.render.com/v1/services/{serviceId}/deploys?limit=1` — 检查 `status: "live"` 以确认部署成功。
- **日志（如有需要）：** 通过 Render API 或仪表板 → 服务 → 日志查看。

示例（使用 `curl` 执行）：
```bash
curl -s -H "Authorization: Bearer $RENDER_API_KEY" "https://api.render.com/v1/services" | head -100
curl -s -H "Authorization: Bearer $RENDER_API_KEY" "https://api.render.com/v1/services/{serviceId}/deploys?limit=1"
```

有关简短的操作指南和常见问题的解决方法，请参阅 `references/post-deploy-checks.md` 和 `references/troubleshooting-basics.md`。

## 触发部署（无需推送）

- **仓库连接后：** 如果启用了自动部署，推送到链接的仓库会触发自动部署。
- **通过 API 触发：** 使用 `RENDER_API_KEY` 触发新的部署：
  - **POST** `https://api.render.com/v1/services/{serviceId}/deploys`
  - 请求头：`Authorization: Bearer $RENDER_API_KEY`
  - 可选请求体：`{"clearCache": "do_not_clear" }` 或 `"clear"`
- **部署钩子（无需 API 密钥）：** 在仪表板 → 服务 → 设置 → 部署钩子。用户可以将该链接设置为环境变量（例如 `RENDER_DEPLOYHOOK_URL`）；然后代理程序可以通过 `curl -X POST "$RENDER_DEPLOYHOOK_URL"` 来触发部署。

**总结：** OpenClaw 可以通过以下方式部署：** (1) 创建 `render.yaml`，(2) 让用户推送并点击蓝图链接（一键部署），或者 (3) 在有 API 密钥的情况下通过 API 或部署钩子触发部署。

## 通过 OpenClaw 进行部署（不使用内置的 MCP）

OpenClaw 不会从配置文件中加载 MCP 服务器。可以使用以下方法之一：

### 选项 A：REST API（推荐使用 API 密钥）

使用 `RENDER_API_KEY` 和 Render 的 REST API（通过curl 或其他工具）：创建服务、列出服务、触发部署、列出部署结果、查看日志。**请求体和端点信息：** 参见 `references/rest-api-deployment.md`。

### 选项 B：通过 mcporter（如果已安装）

如果用户有 `mcporter` 并且 Render 已配置（URL 为 `https://mcp.render.com/mcp`，使用 `Bearer `$RENDER_API_KEY`），则可以直接调用 Render 的 MCP 工具。**工具列表和示例命令：** 参见 `references/mcp-integration.md`。

---

## 新部署的操作指南

1. 添加或更新 `render.yaml` 文件，其中包含 `services`（以及可选的 `databases`、`envVarGroups`、`projects`）。对于敏感信息，使用 `sync: false`；提示用户在仪表板中设置这些信息。切勿将密钥放入环境变量组中。
2. 对于键值存储服务，必须设置 `ipAllowList`。
3. 验证蓝图：使用 `render blueprints validate render.yaml` 或 API 进行验证。
4. 用户必须提交并推送文件，然后使用 **蓝图链接**（`https://dashboard.render.com/blueprint/new?repo=<HTTPS_REPO_URL>`）进行部署。如果设置了 `RENDER_API_KEY`，还可以选择通过 API 进行验证或重新部署。

## 规则

- 建议使用蓝图来完整定义应用程序；只有在蓝图无法表达某些需求时才建议使用仪表板/API。
- **切勿提交真实的 API 密钥或敏感信息**；使用 `sync: false` 并明确指出用户需要设置的环境变量。
- 对于 Python/Node 项目，根据需要在使用环境变量时设置 `PYTHON_VERSION`/`NODE_VERSION`。
- 在引用键值存储或其他服务时，使用正确的 `fromService` 和类型（例如 `type: keyvalue`、`pserv`）。