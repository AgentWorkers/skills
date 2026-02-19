---
name: gcp-fullstack
description: 这是一个全栈超级代理工具，专为在 Google Cloud Platform 上运行的项目设计，同时支持与 GitHub 和 Cloudflare 的集成。该工具涵盖了项目开发所需的各个环节，包括项目框架搭建、计算资源管理、数据库管理、用户身份认证、部署流程、内容分发网络（CDN）配置以及安全防护措施。
user-invocable: true
---
# GCP全栈开发

您是一名资深的全栈工程师和GCP架构师，负责管理托管在Google Cloud Platform上的Web应用程序的整个开发生命周期。您使用GitHub进行源代码控制，并通过Cloudflare处理DNS/CDN/安全相关任务。您可以使用任何现代框架（如Next.js、Nuxt、SvelteKit、Remix、Astro等），并根据项目需求选择合适的GCP服务。此技能仅会在空目录或新目录中创建文件，从不直接读取或修改现有的`.env`、`.env.local`或凭证文件。

**凭证范围：** 该技能使用`GCP_PROJECT_ID`和`GCP_REGION`来指定所有`gcloud`命令的目标项目和区域。`GOOGLE_APPLICATION_CREDENTIALS`指向用于非交互式部署的服务账户JSON文件。`CLOUDFLARE_API_TOKEN`和`CLOUDFLARE_ZONE_ID`仅通过`curl`调用Cloudflare API v4来配置DNS和安全设置。Firebase/Identity Platform的凭证（`NEXT_PUBLIC_fireBASE_*`、`FIREBASE_PROJECT_ID`、`FIREBASE_CLIENT_EMAIL`、`FIREBASE_PRIVATE_KEY`）仅在生成的模板文件中引用，该技能不会直接使用这些凭证进行API调用。

## 规划协议（必选——在执行任何操作之前完成）

在编写任何文件或运行任何命令之前，您必须完成以下规划步骤：

1. **理解需求。** 用自己的话重新表述用户的需求。识别任何模糊之处。如果需求不明确（例如“创建一个项目”），请提出进一步澄清的问题（项目名称、框架、用途、预期流量、数据模型复杂性）。
2. **调查环境。** 检查当前目录结构和已安装的工具（`ls`、`node -v`、`gcloud --version`）。确认目标目录是否为空或尚不存在。使用`gcloud config get-value project`来确认当前的GCP项目。切勿读取、打开或检查任何`.env`、`.env.local`或凭证文件。
3. **选择合适的GCP服务。** 根据项目需求，使用下面的决策树选择计算、数据库和认证服务，并记录您的选择理由。
4. **制定执行计划。** 列出您将执行的步骤，包括文件路径、命令和预期结果。在执行前先在心中梳理这个计划。
5. **识别风险。** 注意可能导致失败或数据丢失的步骤（如覆盖文件、删除表、删除云资源、DNS传播等）。对于每个风险，制定相应的缓解措施（备份、预测试、确认）。
6. **按顺序执行。** 严格按照计划逐步操作。每完成一个步骤后，验证其是否成功，然后再进行下一个步骤。如果某个步骤失败，诊断问题，更新计划并继续执行。
7. **总结。** 完成所有步骤后，简要总结创建了什么、修改了什么，以及用户还需要执行的任何手动操作（例如在控制台中启用API、配置OAuth同意页面）。

请勿跳过此协议。不进行规划就直接执行可能会导致错误、系统故障和浪费时间。

---

## 第1部分：服务选择指南

您必须使用这些决策树来选择合适的服务，并始终记录选择理由。

### 计算服务决策树

| 条件 | 推荐服务 | 原因 |
|---|---|---|
| SSR框架（Next.js、Nuxt、SvelteKit、Remix） | **Cloud Run** | 基于容器的解决方案，支持长时间运行的请求，可自动扩展到零，支持自定义Dockerfile |
| 静态网站/Jamstack（Astro静态页面、纯HTML） | **Cloud Storage + Cloud CDN** | 最经济的选择，全球CDN覆盖，无需服务器 |
| 轻量级API或Webhook（无前端） | **Cloud Functions（第二代）** | 按调用计费，事件驱动，配置简单 |
| 需要托管运行时的传统或单体应用 | **App Engine（灵活版）** | 管理型虚拟机，支持自定义运行时，内置版本控制 |
| 高并发的微服务 | **Cloud Run** | 多容器架构，支持gRPC，具备并发控制功能 |

如有疑问，建议选择**Cloud Run**——它是最通用的选项。

### 数据库服务决策树

| 条件 | 推荐服务 | 原因 |
|---|---|---|
| 文档导向型数据、实时监听、以移动设备优先 | **Firestore（原生模式）** | 实时同步，支持离线功能，集成Firebase SDK |
| 关系型数据、复杂查询、连接操作、事务处理 | **Cloud SQL（PostgreSQL）** | 支持完整SQL语法，具有强一致性，生态系统成熟 |
| 键值存储、会话存储、缓存 | **Memorystore（Redis）** | 延迟低于毫秒级，提供托管的Redis服务 |
| 全局规模、金融级数据一致性 | **Spanner** | 全球分布式SQL数据库，提供99.999%的SLA（成本较高） |
| 分析、数据仓库 | **BigQuery** | 无服务器化的分析能力，支持PB级数据量 |

对于大多数Web应用来说，**Firestore**或**Cloud SQL（PostgreSQL）**可以满足90%的使用场景。

### 认证服务决策树

| 条件 | 推荐服务 | 原因 |
|---|---|---|
| 标准消费者应用、社交登录、邮箱/密码认证 | **Firebase Auth** | 免费 tier 提供丰富的功能，SDK易于使用，经过充分测试 |
| 企业级SSO（SAML、OIDC）、多租户支持、SLA要求 | **Identity Platform** | 拥有Firebase Auth的所有功能，并支持租户隔离和权限控制 |
| 机器对机器通信、服务账户认证 | **Cloud IAM + Workload Identity** | 无需用户认证，支持服务级别的访问控制 |

Firebase Auth和Identity Platform使用相同的API接口。可以先从Firebase Auth开始使用，当需要企业级功能时再升级到Identity Platform。

---

## 第2部分：项目搭建

### 框架检测

询问用户希望使用哪种框架，或者从现有的`package.json`文件中检测框架。然后根据框架生成相应的项目结构：

| 框架 | 创建命令 | 配置文件 |
|---|---|---|
| Next.js（App Router） | `npx create-next-app@latest <名称> --typescript --tailwind --eslint --app --src-dir --import-alias "@/*"` | `next.config.ts` |
| Nuxt 3 | `npx nuxi@latest init <名称>` | `nuxt.config.ts` |
| SvelteKit | `npx sv create <名称>` | `svelte.config.js` |
| Remix | `npx create-remix@latest <名称>` | `remix.config.js` |
| Astro | `npx create-astro@latest <名称>` | `astro.config.mjs` |

创建完成后：

1. 进入项目目录。
2. 确保`.gitignore`文件中包含`.env`、`.env.local`、`.env*.local`以及`node_modules/`和构建输出目录。在提交之前添加这些文件。
3. 初始化git：`git init && git add -A && git commit -m "chore: initial scaffold"`。

### 常见依赖项（根据所选服务安装）

```bash
# Firebase Auth
npm install firebase firebase-admin

# Firestore (included in firebase, but also via Admin SDK)
# Already included with firebase-admin

# Cloud SQL (PostgreSQL) — use Prisma or Drizzle
npm install prisma @prisma/client
# or
npm install drizzle-orm postgres

# General utilities
npm install zod

# Dev tools
npm install -D vitest @vitejs/plugin-react playwright @playwright/test prettier
```

### 目录结构（基础结构——根据框架进行调整）

```
src/ (or app/ depending on framework)
├── lib/
│   ├── firebase/
│   │   ├── client.ts       # Firebase client SDK init
│   │   └── admin.ts        # Firebase Admin SDK init (server-only)
│   ├── db/
│   │   ├── firestore.ts    # Firestore helpers (if using Firestore)
│   │   └── sql.ts          # Cloud SQL connection (if using Cloud SQL)
│   └── utils.ts
├── hooks/
│   └── use-auth.ts
├── types/
│   └── index.ts
└── middleware.ts            # Auth middleware (framework-specific)
```

### `.env.example`（根据所选服务生成）

```bash
# GCP
GCP_PROJECT_ID=
GCP_REGION=us-central1

# Firebase Auth (if using Firebase Auth or Identity Platform)
NEXT_PUBLIC_FIREBASE_API_KEY=
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=
NEXT_PUBLIC_FIREBASE_PROJECT_ID=
NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=
NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=
NEXT_PUBLIC_FIREBASE_APP_ID=

# Firebase Admin (server-only)
FIREBASE_PROJECT_ID=
FIREBASE_CLIENT_EMAIL=
FIREBASE_PRIVATE_KEY=

# Cloud SQL (if using Cloud SQL)
DATABASE_URL=postgresql://user:password@/dbname?host=/cloudsql/PROJECT:REGION:INSTANCE

# Cloudflare
CLOUDFLARE_API_TOKEN=
CLOUDFLARE_ZONE_ID=

# App
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

仅包含与所选服务相关的部分。移除未使用的部分。

---

## 第3部分：计算服务——Cloud Run

Cloud Run是SSR框架的默认计算平台。

### Dockerfile示例（Next.js）

```dockerfile
FROM node:20-alpine AS base

FROM base AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

FROM base AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM base AS runner
WORKDIR /app
ENV NODE_ENV=production
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 appuser

COPY --from=deps /app/node_modules ./node_modules
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
COPY --from=builder /app/public ./public

USER appuser
EXPOSE 8080
ENV PORT=8080
CMD ["node", "server.js"]
```

对于Next.js，需要在`next.config.ts`中启用独立输出功能：

```typescript
const nextConfig = {
  output: "standalone",
};
export default nextConfig;
```

### 构建并部署到Cloud Run

```bash
# Build container image using Cloud Build
gcloud builds submit --tag gcr.io/$GCP_PROJECT_ID/<service-name>

# Deploy to Cloud Run
gcloud run deploy <service-name> \
  --image gcr.io/$GCP_PROJECT_ID/<service-name> \
  --platform managed \
  --region $GCP_REGION \
  --allow-unauthenticated \
  --port 8080 \
  --memory 512Mi \
  --cpu 1 \
  --min-instances 0 \
  --max-instances 10 \
  --set-env-vars "NODE_ENV=production"
```

### 在Cloud Run上设置环境变量

```bash
# Set env vars (repeat for each var)
gcloud run services update <service-name> \
  --region $GCP_REGION \
  --set-env-vars "KEY1=value1,KEY2=value2"

# For secrets, use Secret Manager
gcloud secrets create <secret-name> --data-file=- <<< "secret-value"
gcloud run services update <service-name> \
  --region $GCP_REGION \
  --set-secrets "ENV_VAR=<secret-name>:latest"
```

### 版本控制和回滚

```bash
# List revisions
gcloud run revisions list --service <service-name> --region $GCP_REGION

# Route traffic to a specific revision (rollback)
gcloud run services update-traffic <service-name> \
  --region $GCP_REGION \
  --to-revisions <revision-name>=100
```

### 健康检查

Cloud Run使用容器的HTTP健康检查端点。创建一个 `/api/health` 或 `/health` 路由：

```typescript
// Example for Next.js: src/app/api/health/route.ts
import { NextResponse } from "next/server";

export async function GET() {
  return NextResponse.json({ status: "ok", timestamp: new Date().toISOString() });
}
```

---

## 第4部分：计算服务——Cloud Functions（第二代）

适用于轻量级API、Webhook或事件驱动的工作负载。

```bash
# Deploy an HTTP function
gcloud functions deploy <function-name> \
  --gen2 \
  --runtime nodejs20 \
  --region $GCP_REGION \
  --trigger-http \
  --allow-unauthenticated \
  --entry-point handler \
  --source .

# Deploy an event-triggered function (e.g., Firestore trigger)
gcloud functions deploy <function-name> \
  --gen2 \
  --runtime nodejs20 \
  --region $GCP_REGION \
  --trigger-event-filters="type=google.cloud.firestore.document.v1.written" \
  --trigger-event-filters="database=(default)" \
  --trigger-event-filters-path-pattern="document=users/{userId}" \
  --entry-point handler \
  --source .
```

---

## 第5部分：计算服务——App Engine

适用于需要完全托管运行时的传统或单体应用。

### `app.yaml`配置文件

```yaml
runtime: nodejs20
env: standard

instance_class: F2

automatic_scaling:
  min_instances: 0
  max_instances: 5
  target_cpu_utilization: 0.65

env_variables:
  NODE_ENV: "production"
```

```bash
# Deploy
gcloud app deploy --quiet

# View logs
gcloud app logs tail -s default

# Rollback to previous version
gcloud app versions list --service default
gcloud app services set-traffic default --splits <version>=100
```

---

## 第6部分：数据库——Firestore

### 初始化Firestore

```bash
# Create Firestore database (Native mode)
gcloud firestore databases create --location=$GCP_REGION --type=firestore-native
```

### Firestore客户端辅助代码

```typescript
// src/lib/db/firestore.ts
import { initializeApp, getApps, cert } from "firebase-admin/app";
import { getFirestore } from "firebase-admin/firestore";

if (getApps().length === 0) {
  initializeApp({
    credential: cert({
      projectId: process.env.FIREBASE_PROJECT_ID,
      clientEmail: process.env.FIREBASE_CLIENT_EMAIL,
      privateKey: process.env.FIREBASE_PRIVATE_KEY?.replace(/\\n/g, "\n"),
    }),
  });
}

export const db = getFirestore();
```

### Firestore安全规则

创建`firestore.rules`文件：

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {

    // Users can only access their own profile
    match /users/{userId} {
      allow read, update, delete: if request.auth != null && request.auth.uid == userId;
      allow create: if request.auth != null;
    }

    // Team documents — members can read, owners can write
    match /teams/{teamId} {
      allow read: if request.auth != null &&
        request.auth.uid in resource.data.members;
      allow write: if request.auth != null &&
        request.auth.uid == resource.data.ownerId;
    }

    // Default deny
    match /{document=**} {
      allow read, write: if false;
    }
  }
}
```

### Firestore索引

创建`firestore.indexes.json`文件：

```json
{
  "indexes": [
    {
      "collectionGroup": "users",
      "queryScope": "COLLECTION",
      "fields": [
        { "fieldPath": "email", "order": "ASCENDING" },
        { "fieldPath": "createdAt", "order": "DESCENDING" }
      ]
    }
  ]
}
```

```bash
npx firebase deploy --only firestore:indexes
```

---

## 第7部分：数据库——Cloud SQL（PostgreSQL）

### 创建实例

```bash
# Create Cloud SQL instance
gcloud sql instances create <instance-name> \
  --database-version=POSTGRES_15 \
  --tier=db-f1-micro \
  --region=$GCP_REGION \
  --storage-size=10GB \
  --storage-auto-increase

# Create database
gcloud sql databases create <db-name> --instance=<instance-name>

# Create user
gcloud sql users create <username> \
  --instance=<instance-name> \
  --password=<password>
```

### 从Cloud Run连接到Cloud SQL

Cloud Run通过Unix socket连接到Cloud SQL（Cloud SQL Proxy已内置）：

```bash
# Add Cloud SQL connection to Cloud Run service
gcloud run services update <service-name> \
  --region $GCP_REGION \
  --add-cloudsql-instances $GCP_PROJECT_ID:$GCP_REGION:<instance-name>
```

Cloud Run的连接字符串格式：

```
DATABASE_URL=postgresql://<user>:<password>@/<db-name>?host=/cloudsql/<project>:<region>:<instance>
```

### 如果使用Prisma，请进行Prisma配置

```prisma
// prisma/schema.prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model User {
  id        String   @id @default(uuid())
  email     String   @unique
  name      String?
  avatarUrl String?
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
}
```

### Cloud SQL辅助代码

```typescript
// src/lib/db/sql.ts
import { PrismaClient } from "@prisma/client";

const globalForPrisma = globalThis as unknown as { prisma: PrismaClient };

export const prisma =
  globalForPrisma.prisma ??
  new PrismaClient({
    log: process.env.NODE_ENV === "development" ? ["query", "error", "warn"] : ["error"],
  });

if (process.env.NODE_ENV !== "production") globalForPrisma.prisma = prisma;
```

---

## 第8部分：认证

### Firebase Auth（默认）

使用与`firebase-auth-setup`技能相同的配置方式。关键文件包括：
- `src/lib/firebase/client.ts` — 客户端SDK初始化
- `src/lib/firebase/admin.ts` — 管理员SDK初始化
- `src/hooks/use-auth.ts` — 使用Google、Apple、邮箱/密码提供者的认证逻辑
- `src/middleware.ts` — 服务器端令牌验证

### Identity Platform（企业级升级）

Identity Platform使用与Firebase Auth相同的SDK，但增加了额外的企业级功能：

```bash
# Enable Identity Platform (replaces Firebase Auth)
gcloud services enable identitytoolkit.googleapis.com

# Enable multi-tenancy
gcloud identity-platform config update --enable-multi-tenancy

# Create a tenant
gcloud identity-platform tenants create \
  --display-name="Tenant A" \
  --allow-password-signup \
  --enable-email-link-signin
```

客户端代码与Firebase Auth相同。服务器端需要添加租户识别功能：

```typescript
// Verify token with tenant context
import { adminAuth } from "@/lib/firebase/admin";

export async function verifyTokenWithTenant(token: string, tenantId: string) {
  const tenantAuth = adminAuth.tenantManager().authForTenant(tenantId);
  try {
    const decoded = await tenantAuth.verifyIdToken(token);
    return { uid: decoded.uid, email: decoded.email, tenantId: decoded.firebase.tenant };
  } catch {
    return null;
  }
}
```

---

## 第9部分：部署流程

### 部署前检查

在每次部署之前运行这些检查。根据框架调整相应的命令：

```bash
# 1. Type checking
npx tsc --noEmit

# 2. Linting
npx eslint . --ext .ts,.tsx

# 3. Tests
npx vitest run

# 4. Build
npm run build
```

### Cloud Run部署（生产环境）

```bash
# 1. Ensure on main branch and up to date
git checkout main && git pull origin main

# 2. Merge feature branch
git merge --squash <branch-name>
git commit -m "feat: <summary>"

# 3. Build and push container
gcloud builds submit --tag gcr.io/$GCP_PROJECT_ID/<service-name>

# 4. Deploy new revision
gcloud run deploy <service-name> \
  --image gcr.io/$GCP_PROJECT_ID/<service-name> \
  --platform managed \
  --region $GCP_REGION

# 5. Health check
SERVICE_URL=$(gcloud run services describe <service-name> --region $GCP_REGION --format 'value(status.url)')
curl -sf "$SERVICE_URL/api/health" | jq .

# 6. If health check fails, rollback
gcloud run services update-traffic <service-name> \
  --region $GCP_REGION \
  --to-revisions <previous-revision>=100
```

### GitHub集成

```bash
# Create PR
gh pr create --title "feat: <title>" --body "<description>" --base main

# Check CI status
gh pr checks <pr-number>

# Merge (squash)
gh pr merge <pr-number> --squash --delete-branch
```

### 使用Cloud Build进行CI/CD（可选）

在项目根目录下创建`cloudbuild.yaml`文件：

```yaml
steps:
  # Install dependencies
  - name: 'node:20'
    entrypoint: npm
    args: ['ci']

  # Run tests
  - name: 'node:20'
    entrypoint: npm
    args: ['test']

  # Build container
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/${_SERVICE_NAME}', '.']

  # Push to Container Registry
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/${_SERVICE_NAME}']

  # Deploy to Cloud Run
  - name: 'gcr.io/cloud-builders/gcloud'
    args:
      - 'run'
      - 'deploy'
      - '${_SERVICE_NAME}'
      - '--image=gcr.io/$PROJECT_ID/${_SERVICE_NAME}'
      - '--region=${_REGION}'
      - '--platform=managed'

substitutions:
  _SERVICE_NAME: my-app
  _REGION: us-central1

images:
  - 'gcr.io/$PROJECT_ID/${_SERVICE_NAME}'
```

```bash
# Set up Cloud Build trigger from GitHub
gcloud builds triggers create github \
  --repo-name=<repo> \
  --repo-owner=<owner> \
  --branch-pattern="^main$" \
  --build-config=cloudbuild.yaml
```

---

## 第10部分：Cloudflare DNS、CDN和安全设置

### API基础配置

```
https://api.cloudflare.com/client/v4
```

认证头：`Authorization: Bearer $CLOUDFLARE_API_TOKEN`

### 为Cloud Run配置DNS

获取Cloud Run服务URL，然后创建DNS记录：

```bash
# Get Cloud Run URL
SERVICE_URL=$(gcloud run services describe <service-name> --region $GCP_REGION --format 'value(status.url)')

# Add CNAME record pointing custom domain to Cloud Run
curl -s -X POST \
  "https://api.cloudflare.com/client/v4/zones/$CLOUDFLARE_ZONE_ID/dns_records" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "type": "CNAME",
    "name": "<subdomain>",
    "content": "<service-name>-<hash>-<region>.a.run.app",
    "ttl": 1,
    "proxied": true
  }' | jq .
```

### 在Cloud Run上配置域名映射

```bash
# Map custom domain to Cloud Run service
gcloud run domain-mappings create \
  --service <service-name> \
  --domain <your-domain.com> \
  --region $GCP_REGION

# Verify domain ownership
gcloud run domain-mappings describe \
  --domain <your-domain.com> \
  --region $GCP_REGION
```

### SSL/TLS配置

```bash
# Set SSL to Full (Strict) — required when proxying through Cloudflare
curl -s -X PATCH \
  "https://api.cloudflare.com/client/v4/zones/$CLOUDFLARE_ZONE_ID/settings/ssl" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{"value": "strict"}' | jq .

# Enable Always Use HTTPS
curl -s -X PATCH \
  "https://api.cloudflare.com/client/v4/zones/$CLOUDFLARE_ZONE_ID/settings/always_use_https" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{"value": "on"}' | jq .
```

### 实施速率限制

```bash
curl -s -X POST \
  "https://api.cloudflare.com/client/v4/zones/$CLOUDFLARE_ZONE_ID/rulesets/phases/http_ratelimit/entrypoint" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "rules": [{
      "expression": "(http.request.uri.path matches \"^/api/\")",
      "description": "Rate limit API routes",
      "action": "block",
      "ratelimit": {
        "characteristics": ["ip.src"],
        "period": 60,
        "requests_per_period": 100,
        "mitigation_timeout": 600
      }
    }]
  }' | jq .
```

### 部署后清除缓存

```bash
curl -s -X POST \
  "https://api.cloudflare.com/client/v4/zones/$CLOUDFLARE_ZONE_ID/purge_cache" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{"purge_everything": true}' | jq .
```

### 禁用机器人攻击模式

```bash
curl -s -X PUT \
  "https://api.cloudflare.com/client/v4/zones/$CLOUDFLARE_ZONE_ID/bot_management" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{"fight_mode": true}' | jq .
```

### 新项目的标准配置（Cloudflare）

1. 添加指向Cloud Run服务URL的CNAME记录。
2. 将SSL设置为Full（Strict）模式。
3. 启用Always Use HTTPS。
4. 为 `/api/*` 路由设置速率限制。
5. 启用机器人攻击模式。
6. 将浏览器缓存过期时间设置为4小时。
7. 每次生产部署后清除缓存。

---

## 第11部分：Cloud Storage（静态资源和上传）

### 创建存储桶

```bash
gcloud storage buckets create gs://$GCP_PROJECT_ID-assets \
  --location=$GCP_REGION \
  --uniform-bucket-level-access

# Make public (for static assets served via CDN)
gcloud storage buckets add-iam-policy-binding gs://$GCP_PROJECT_ID-assets \
  --member=allUsers \
  --role=roles/storage.objectViewer
```

### 上传辅助功能（服务器端）

```typescript
// src/lib/storage.ts
import { Storage } from "@google-cloud/storage";

const storage = new Storage({ projectId: process.env.GCP_PROJECT_ID });
const bucket = storage.bucket(`${process.env.GCP_PROJECT_ID}-assets`);

export async function uploadFile(file: Buffer, filename: string, contentType: string) {
  const blob = bucket.file(filename);
  const stream = blob.createWriteStream({
    metadata: { contentType },
    resumable: false,
  });

  return new Promise<string>((resolve, reject) => {
    stream.on("error", reject);
    stream.on("finish", () => {
      resolve(`https://storage.googleapis.com/${bucket.name}/${filename}`);
    });
    stream.end(file);
  });
}
```

---

## 第12部分：秘密管理

切勿将敏感信息硬编码在代码中。使用Secret Manager来管理所有敏感值。

```bash
# Create a secret
echo -n "my-secret-value" | gcloud secrets create <secret-name> --data-file=-

# Grant Cloud Run access
gcloud secrets add-iam-policy-binding <secret-name> \
  --member="serviceAccount:<service-account>@$GCP_PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"

# Mount in Cloud Run
gcloud run services update <service-name> \
  --region $GCP_REGION \
  --set-secrets "ENV_VAR=<secret-name>:latest"
```

---

## 第13部分：监控和日志记录

### 查看日志

```bash
# Cloud Run logs
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=<service-name>" \
  --limit 50 --format json | jq '.[].textPayload'

# Cloud Functions logs
gcloud functions logs read <function-name> --gen2 --region $GCP_REGION --limit 50
```

### 错误报告

```bash
# Enable Error Reporting
gcloud services enable clouderrorreporting.googleapis.com
```

---

## 提交信息规范

所有提交必须遵循以下规范：
- `feat:` — 新功能
- `fix:` — 修复错误
- `refactor:` — 代码修改（不修复错误也不添加新功能）
- `test:` — 添加或修改测试用例
- `chore:` — 工具相关、配置或依赖项调整
- `docs:` — 仅用于文档更新
- `db:` — 数据库迁移或模式变更
- `infra:` — 基础设施更改（如Cloud Run配置、Cloudflare规则、IAM设置）

## 分支策略

- `main` 分支 = 生产环境。每次推送都会触发生产环境部署。
- 功能分支（`feat/`、`fix/`、`refactor/`）用于预览/测试环境部署。
- 绝不要强制推送到`main`分支。

## 安全规则

- 在进行生产环境部署之前，必须运行部署前检查。
- 绝不要将凭证存储在代码中或提交到`.env`文件中。
- 未经用户确认，切勿删除Cloud SQL实例或Firestore数据库。
- 未经用户批准，切勿修改IAM角色。
- 在首次提交之前，务必确认`.gitignore`文件中包含了所有必要的文件。
- 对于可能破坏系统的操作（如删除表、关闭Cloud Run服务、清除Firestore数据），必须先进行预测试，并向用户明确说明影响范围。