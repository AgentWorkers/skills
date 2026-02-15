---
name: service-connect
description: 智能外部服务连接编排器，能够自动选择最优的连接方式（MCP → REST API → SDK → CLI → 直接连接）。适用于连接 Supabase、Cloudflare、PostgreSQL、MongoDB、Redis 或 AWS 等服务。该工具遵循“阻力最小”的原则来避免连接问题。
---

# 服务连接编排器

## 🎯 核心原则

**永远不要手动解决连接问题，而是选择最简单的解决方案：**

```
MCP Server → REST API → SDK/Client → CLI → Direct Connection
     ↑                                              ↓
   BEST                                          WORST
```

---

## 🔌 服务连接矩阵

### Supabase

```yaml
Priority:
  1. MCP Server (BEST - bypasses ALL network issues)
  2. REST API via fetch (reliable, works everywhere)
  3. JavaScript Client SDK (good for app code)
  4. CLI (supabase db push) - AVOID for migrations
  5. Direct psql - AVOID (IPv6/pooler issues)

Setup MCP:
  npx @anthropic-ai/claude-code-mcp add supabase
  # Then restart Claude Code

Credential Check (presence only - never display values!):
  grep -qE "SUPABASE_URL|SUPABASE_ANON_KEY|SUPABASE_SERVICE_ROLE" .env && echo "Supabase credentials found"

Direct REST (no MCP needed):
  curl "${SUPABASE_URL}/rest/v1/table" \
    -H "apikey: ${SUPABASE_ANON_KEY}" \
    -H "Authorization: Bearer ${SUPABASE_SERVICE_ROLE_KEY}"

SQL via REST (PostgREST RPC):
  # Create a function in Supabase SQL Editor first, then call via REST
  curl "${SUPABASE_URL}/rest/v1/rpc/function_name" \
    -H "apikey: ${SUPABASE_ANON_KEY}" \
    -d '{"param": "value"}'

Connection Pooler (if direct needed):
  # Use port 6543, NOT 5432
  # Use transaction mode for serverless
  DATABASE_URL="postgresql://postgres.[ref]:[password]@aws-0-[region].pooler.supabase.com:6543/postgres"
```

### Cloudflare（Workers、KV、D1、R2）

```yaml
Priority:
  1. Wrangler CLI with OAuth session (BEST)
  2. REST API with API Token
  3. MCP Server (if available)

Setup:
  # One-time login (opens browser, saves session)
  wrangler login

  # Verify
  wrangler whoami

Credential Check (presence only - never display values!):
  wrangler whoami 2>/dev/null || echo "Not logged in"
  grep -qE "CF_API_TOKEN|CLOUDFLARE_API_TOKEN" .env && echo "Cloudflare token found"

Common Operations:
  # Deploy Worker
  wrangler deploy

  # Set secret (no .env exposure)
  echo "secret_value" | wrangler secret put SECRET_NAME

  # KV operations
  wrangler kv:key put --binding=MY_KV "key" "value"

  # D1 (SQLite) operations
  wrangler d1 execute DB_NAME --command "SELECT * FROM users"

  # R2 (S3-compatible) operations
  wrangler r2 object put BUCKET/key --file=./file.txt
```

### PostgreSQL（直接连接）

```yaml
Priority:
  1. MCP Server (postgres-mcp)
  2. Connection Pooler (PgBouncer, Supabase Pooler)
  3. psql CLI with proper connection string
  4. Direct TCP - AVOID in serverless

Setup MCP:
  npx @anthropic-ai/claude-code-mcp add postgres

  # Config requires DATABASE_URL in environment

Connection String Patterns:
  # Standard
  postgresql://user:password@host:5432/database

  # With SSL (required for most cloud DBs)
  postgresql://user:password@host:5432/database?sslmode=require

  # Supabase Pooler (transaction mode for serverless)
  postgresql://postgres.[ref]:[password]@aws-0-[region].pooler.supabase.com:6543/postgres?pgbouncer=true

Credential Check (presence only - never display values!):
  grep -qE "DATABASE_URL|POSTGRES_|PG_" .env && echo "PostgreSQL credentials found"
```

### MongoDB Atlas

```yaml
Priority:
  1. Atlas Data API (REST-based, no driver needed)
  2. MCP Server
  3. MongoDB Node.js Driver
  4. mongosh CLI

Atlas Data API Setup:
  # Enable in Atlas UI: App Services > Data API
  # Get API Key from Atlas UI

  curl --request POST \
    "${MONGODB_DATA_API_URL}/action/findOne" \
    -H "api-key: ${MONGODB_DATA_API_KEY}" \
    -H "Content-Type: application/json" \
    -d '{
      "dataSource": "Cluster0",
      "database": "mydb",
      "collection": "users",
      "filter": {"email": "test@example.com"}
    }'

Credential Check (presence only - never display values!):
  grep -qE "MONGODB_URI|MONGO_URL|MONGODB_DATA_API" .env && echo "MongoDB credentials found"
```

### Redis / Upstash

```yaml
Priority:
  1. Upstash REST API (BEST - HTTP-based, serverless-friendly)
  2. MCP Server
  3. ioredis client
  4. redis-cli - AVOID (TCP issues in many environments)

Upstash REST:
  # No TCP connection needed!
  curl "${UPSTASH_REDIS_REST_URL}/set/mykey/myvalue" \
    -H "Authorization: Bearer ${UPSTASH_REDIS_REST_TOKEN}"

  curl "${UPSTASH_REDIS_REST_URL}/get/mykey" \
    -H "Authorization: Bearer ${UPSTASH_REDIS_REST_TOKEN}"

Vercel KV (Upstash-backed):
  # Uses same REST pattern
  import { kv } from '@vercel/kv';
  await kv.set('key', 'value');

Credential Check (presence only - never display values!):
  grep -qE "REDIS_URL|UPSTASH_" .env && echo "Redis/Upstash credentials found"
```

### AWS 服务

```yaml
Priority:
  1. AWS CLI with SSO/profile
  2. AWS SDK with credentials chain
  3. MCP Server (if available)

Setup:
  # Configure SSO (recommended)
  aws configure sso

  # Or use access keys (store in ~/.aws/credentials, NOT .env)
  aws configure

Credential Check (presence only - never display values!):
  aws sts get-caller-identity
  grep -qE "AWS_ACCESS_KEY|AWS_SECRET|AWS_PROFILE" .env ~/.aws/credentials && echo "AWS credentials found"

Common Services:
  # S3
  aws s3 cp file.txt s3://bucket/key

  # Lambda
  aws lambda invoke --function-name MyFunction output.json

  # DynamoDB
  aws dynamodb scan --table-name MyTable

  # Secrets Manager (for app secrets)
  aws secretsmanager get-secret-value --secret-id MySecret
```

### Vercel

```yaml
Priority:
  1. Vercel CLI with OAuth
  2. REST API with token
  3. MCP Server

Setup:
  # One-time login
  vercel login

  # Link project
  vercel link

Credential Check (presence only - never display values!):
  vercel whoami 2>/dev/null || echo "Not logged in"
  grep -q VERCEL_TOKEN .env && echo "Vercel token found"

Common Operations:
  # Deploy
  vercel --prod

  # Environment variables
  vercel env add VARIABLE_NAME production

  # Logs
  vercel logs project-name
```

---

## 🔄 自动检测逻辑

在开始工作时，Claude 应该检查：

```bash
# 1. Check which services are configured
echo "=== Service Detection ==="

# Supabase
if grep -q "SUPABASE_URL" .env 2>/dev/null; then
  echo "✓ Supabase detected"
  echo "  → Use MCP or REST API, avoid direct psql"
fi

# Cloudflare
if wrangler whoami 2>/dev/null | grep -q "email"; then
  echo "✓ Cloudflare/Wrangler authenticated"
elif grep -q "CF_API_TOKEN\|CLOUDFLARE" .env 2>/dev/null; then
  echo "⚠ Cloudflare token found, but wrangler not logged in"
  echo "  → Run: wrangler login"
fi

# PostgreSQL
if grep -q "DATABASE_URL\|POSTGRES" .env 2>/dev/null; then
  echo "✓ PostgreSQL detected"
  # Check for pooler pattern without displaying URL
  if grep -qE "DATABASE_URL=.*(pooler|:6543)" .env 2>/dev/null; then
    echo "  → Using connection pooler (good!)"
  else
    echo "  ⚠ Direct connection - consider pooler for serverless"
  fi
fi

# MongoDB
if grep -q "MONGODB" .env 2>/dev/null; then
  echo "✓ MongoDB detected"
  if grep -q "MONGODB_DATA_API" .env; then
    echo "  → Data API configured (best for serverless)"
  else
    echo "  → Consider enabling Atlas Data API"
  fi
fi

# Redis/Upstash
if grep -q "UPSTASH" .env 2>/dev/null; then
  echo "✓ Upstash Redis detected (REST API available)"
elif grep -q "REDIS_URL" .env 2>/dev/null; then
  echo "✓ Redis detected"
  echo "  → Consider Upstash for REST-based access"
fi

# AWS
if aws sts get-caller-identity 2>/dev/null; then
  echo "✓ AWS CLI authenticated"
fi

# Vercel
if vercel whoami 2>/dev/null; then
  echo "✓ Vercel CLI authenticated"
fi
```

---

## 🛠️ MCP 服务器安装（一次性设置）

**MCP 服务器提供：**
- 直接的 API 访问（无需使用 CLI）
- 自动重试/错误处理
- 跨服务的一致性接口
- 无网络/防火墙问题（基于 HTTP）

---

## 🚨 常见问题及解决方法

### Supabase “连接失败”（IPv6）
```
Problem: supabase db push fails with connection error
Cause: Direct connection uses IPv6, often blocked

Fix: Use REST API or MCP instead
  # Don't use: supabase db push
  # Do use: REST API or Supabase client SDK
```

### Cloudflare “未认证”
```
Problem: wrangler commands fail with auth error
Cause: Session expired or never logged in

Fix:
  wrangler login  # Opens browser, saves OAuth session
  wrangler whoami # Verify
```

### PostgreSQL 需要 SSL 加密
```
Problem: "SSL connection required"
Cause: Cloud DBs require SSL by default

Fix: Add ?sslmode=require to connection string
  DATABASE_URL="postgresql://...?sslmode=require"
```

### MongoDB 驱动程序版本不匹配
```
Problem: Connection fails with driver errors
Cause: Incompatible driver version

Fix: Use Atlas Data API instead (no driver needed)
  # Enable in Atlas: App Services > Data API
```

---

## 📋 飞行前检查清单

在操作外部服务之前，请执行以下步骤：
1. **检查凭据是否存在**：`grep -q SERVICE .env && echo "Found"`
2. **检查 CLI 认证**：`service-cli whoami`
3. **优先使用 MCP/REST**：避免直接连接
4. **使用数据库连接池**：使用端口 6543 而不是 5432
5. **启用数据 API**：对于 MongoDB，使用 Atlas Data API