---
name: claimable-postgres
description: 通过 Neon 的 Claimable Postgres (pg.new) 功能，可以即时创建临时性的 PostgreSQL 数据库，无需登录、注册或使用信用卡。该服务支持 REST API、CLI 和 SDK。适用于用户快速搭建 PostgreSQL 环境、生成用于原型开发或测试的临时数据库 URL，或者当用户急需使用数据库时的场景。相关触发词包括：`quick postgres`、`temporary postgres`、`nosignup database`、`no credit card database`、`instant DATABASE_URL`、`npx get-db`、`pg.new`、`pg.new API`、`claimable postgres API`。
  Provision instant temporary Postgres databases via Claimable Postgres by Neon
  (pg.new) with no login, signup, or credit card. Supports REST API, CLI, and
  SDK. Use when users ask for a quick Postgres environment, a throwaway
  DATABASE_URL for prototyping/tests, or "just give me a DB now". Triggers
  include: "quick postgres", "temporary postgres", "no signup database",
  "no credit card database", "instant DATABASE_URL", "npx get-db", "pg.new",
  "pg.new API", "claimable postgres API".
---
# Claimable Postgres

提供即用的Postgres数据库，适用于本地开发、演示、原型设计和测试环境。无需注册账户。数据库将在72小时后过期，除非用户将其关联到Neon账户。

## 快速入门

从JSON响应中解析`connection_string`和`claim_url`，并将`connection_string`写入项目的`.env`文件中，作为`DATABASE_URL`。

有关其他方法（CLI、SDK、Vite插件），请参阅下方的[Which Method?](#which-method)。

## 选择哪种方法？

- **REST API**：返回结构化的JSON数据。除了`curl`之外，无需额外的运行时依赖。当需要可预测的输出和错误处理时，这是首选方法。
- **CLI** (`npx get-db@latest --yes`）：通过一个命令完成数据库的配置并写入`.env`文件。适用于Node.js环境，且用户希望设置过程简单的情况。
- **SDK** (`get-db/sdk`）：在Node.js中通过脚本或编程方式配置数据库。
- **Vite插件** (`vite-plugin-db`）：当`DATABASE_URL`缺失时，会在`vite dev`模式下自动配置数据库。适用于使用Vite项目的用户。
- **浏览器**：用户无法直接使用CLI或API。请访问https://pg.new。

## REST API

**基础URL：** `https://pg.new/api/v1`

### 创建数据库

```bash
curl -s -X POST "https://pg.new/api/v1/database" \
  -H "Content-Type: application/json" \
  -d '{"ref": "agent-skills"}'
```

| 参数 | 是否必填 | 说明 |
|-----------|----------|-------------|
| `ref` | 是 | 用于追踪数据库配置者的标识符。通过此技能配置数据库时，请使用`"agent-skills"`。 |
| `enable_logical_replication` | 否 | 是否启用逻辑复制（默认值：false，启用后无法禁用） |

API返回的`connection_string`是一个池化连接的URL。如需直接连接（非池化连接，例如Prisma迁移），请从主机名中删除`-pooler`。CLI会自动同时生成池化连接和直接连接的URL。

**响应：**

```json
{
  "id": "019beb39-37fb-709d-87ac-7ad6198b89f7",
  "status": "UNCLAIMED",
  "neon_project_id": "gentle-scene-06438508",
  "connection_string": "postgresql://...",
  "claim_url": "https://pg.new/claim/019beb39-...",
  "expires_at": "2026-01-26T14:19:14.580Z",
  "created_at": "2026-01-23T14:19:14.580Z",
  "updated_at": "2026-01-23T14:19:14.580Z"
}
```

### 检查状态

```bash
curl -s "https://pg.new/api/v1/database/{id}"
```

返回相同的响应格式。状态变化顺序为：`UNCLAIMED` -> `CLAIMING` -> `CLAIMED`。数据库被领取后，`connection_string`将变为`null`。

### 错误响应

| 错误条件 | HTTP状态码 | 错误信息 |
|-----------|------|---------|
| `ref`缺失或为空 | 400 | “缺少引用来源” |
| 数据库ID无效 | 400 | “未找到数据库” |
| JSON格式无效 | 500 | “创建数据库失败” |

## CLI

```bash
npx get-db@latest --yes
```

通过一个命令完成数据库的配置，并将连接字符串写入`.env`文件中。始终使用`@latest`和`--yes`选项（跳过可能导致代理程序暂停的交互式提示）。

### 预运行检查

检查目标`.env`文件中是否已存在`DATABASE_URL`（或选定的键）。如果找到该键，CLI将直接退出而不会执行配置操作。

如果键已存在，向用户提供三个选项：
1. 删除或注释掉现有记录，然后重新运行。
2. 使用`--env`选项将配置信息写入其他文件（例如`--env .env.local`）。
3. 使用`--key`选项将配置信息写入不同的变量名下。在继续之前请获取用户的确认。

### 选项

| 选项 | 别名 | 说明 | 默认值 |
|--------|-------|-------------|---------|
| `--yes` | `-y` | 跳过提示，使用默认设置 | `false` |
| `--env` | `-e` | .env文件的路径 | `./.env` |
| `--key` | `-k` | 连接字符串的环境变量名 | `DATABASE_URL` |
| `--prefix` | `-p` | 生成的环境变量前缀 | `PUBLIC_` |
| `--seed` | `-s` | 种子SQL文件的路径 | 无 |
| `--logical-replication` | `-L` | 启用逻辑复制 | `false` |
| `--ref` | `-r` | 引用来源ID（通过此技能配置数据库时使用） | 无 |

其他包管理器：`yarn dlx get-db@latest`、`pnpm dlx get-db@latest`、`bunx get-db@latest`、`deno run -A get-db@latest`。

### 输出

CLI会将配置信息写入目标`.env`文件中：

```
DATABASE_URL=postgresql://...              # pooled (use for application queries)
DATABASE_URL_DIRECT=postgresql://...       # direct (use for migrations, e.g. Prisma)
PUBLIC_POSTGRES_CLAIM_URL=https://pg.new/claim/...
```

## SDK

适用于脚本和编程化的数据库配置流程。

```typescript
import { instantPostgres } from 'get-db';

const { databaseUrl, databaseUrlDirect, claimUrl, claimExpiresAt } = await instantPostgres({
  referrer: 'agent-skills',
  seed: { type: 'sql-script', path: './init.sql' },
});
```

返回`databaseUrl`（池化连接）、`databaseUrlDirect`（直接连接，用于迁移）、`claimUrl`以及`claimExpiresAt`（日期对象）。`referrer`参数是必填项。

## Vite插件

对于Vite项目，如果`DATABASE_URL`缺失，`vite-plugin-db`会在`vite dev`模式下自动配置数据库。使用`npm install -D vite-plugin-db`进行安装。有关配置详情，请参阅[Claimable Postgres文档](https://neon.com/docs/reference/claimable-postgres#vite-plugin)。

## 代理工作流程

### API流程

1. **确认意图**：如果请求不明确，请确认用户是否需要一个临时数据库（无需注册）。如果用户明确要求快速或临时数据库，则跳过此步骤。
2. **配置数据库**：向`https://pg.new/api/v1/database`发送POST请求，请求中包含`{"ref": "agent-skills"}`。
3. **解析响应**：从JSON响应中提取`connection_string`、`claim_url`和`expires_at`。
4. **写入`.env`文件**：将`DATABASE_URL`写入项目的`.env`文件（或用户指定的文件和变量名）。未经确认，请勿覆盖现有配置。
5. **执行种子操作（如需要）**：如果用户提供了种子SQL文件，请在新数据库上执行相应的操作：
   ```bash
   psql "$DATABASE_URL" -f seed.sql
   ```
6. **通知用户**：告知用户连接字符串的存储位置、使用的变量名，并提供领取数据库的URL。提醒用户：数据库现已可用，需在72小时内领取才能永久保留。
7. **可选**：提供简单的连接测试（例如`SELECT 1`）。

### CLI流程

1. **检查`.env`文件**：检查目标`.env`文件中是否存在`DATABASE_URL`（或选定的键）。如果存在，则不执行配置操作。提供删除现有配置的选项（`--env`或`--key`），并获取用户的确认。
2. **确认意图**：如果请求不明确，请确认用户是否需要一个临时数据库。如果用户明确要求快速或临时数据库，则跳过此步骤。
3. **收集用户选项**：除非有特殊要求（例如用户指定了自定义环境文件、种子SQL文件或需要启用逻辑复制），否则使用默认设置。
4. **执行配置**：使用`@latest --yes`执行配置，并确保使用最新版本。始终使用`@latest`以避免使用过时的缓存版本。`--yes`选项会跳过可能导致代理程序暂停的交互式提示。
   ```bash
   npx get-db@latest --yes --ref agent-skills --env .env.local --seed ./schema.sql
   ```
5. **验证**：确认连接字符串已正确写入目标文件。
6. **通知用户**：告知用户连接字符串的存储位置、使用的变量名，以及环境变量中的领取URL。提醒用户：数据库现已可用，需在72小时内领取才能永久保留。
7. **可选**：提供简单的连接测试（例如`SELECT 1`）。

### 输出内容

务必告知用户以下信息：
- 连接字符串的存储位置（例如`.env`文件）。
- 使用的变量名（`DATABASE_URL`或自定义键）。
- 领取数据库的URL（来自`.env`文件或API响应）。
- 未领取的数据库为临时数据库，有效期为72小时。

## 领取数据库

领取数据库是可选操作。即使不领取，数据库也可以立即使用。用户可以通过浏览器打开领取URL进行登录或创建Neon账户来领取数据库。

- **API/SDK**：将创建数据库时的`claim_url`提供给用户。
- **CLI**：使用`npx get-db@latest claim`命令，该命令会从`.env`文件中读取领取URL并自动打开浏览器。

用户无法将数据库配置到与Vercel关联的组织中；他们必须选择另一个Neon组织。

## 默认设置和限制

| 参数 | 默认值 |
|-----------|-------|
| 提供商 | AWS |
| 地区 | us-east-2 |
| 使用的Postgres版本 | 17 |

对于可领取的数据库，地区无法更改。未领取的数据库使用更严格的资源限制。领取数据库后，资源限制将恢复到免费计划的默认值。

| | 未领取状态 | 已领取状态（免费计划） |
|---|-----------|---------------------|
| 存储空间 | 100 MB | 512 MB |
| 数据传输量 | 1 GB | 约5 GB |
| 分支支持 | 不支持 | 支持 |
| 数据库有效期 | 72小时 | 无限制 |

## 自动配置

如果代理程序需要数据库来完成任务（例如“为我构建一个带有真实数据库的待办事项应用”），而用户未提供连接字符串，可以通过API自动配置数据库，并告知用户领取方式（包括领取URL）。

## 安全性和用户体验注意事项

- 请勿覆盖现有的环境变量。配置前请先检查，然后使用`--env`或`--key`选项（CLI），或直接跳过配置操作（API），以避免冲突。
- 在执行可能破坏数据的SQL操作（如`DROP`、`TRUNCATE`、`DELETE`）之前，请先征求用户同意。
- 对于生产环境，请推荐使用标准的Neon数据库配置方式，而非临时数据库。
- 如果用户需要长期使用数据库，请立即让他们领取数据库。

## 注意事项

- 如果用户需要长期使用数据库，请立即让他们领取数据库。
- 在将凭据写入`.env`文件后，请确保该文件被`.gitignore`文件覆盖。如果没有，请提前告知用户。未经确认，请勿修改`.gitignore`文件。