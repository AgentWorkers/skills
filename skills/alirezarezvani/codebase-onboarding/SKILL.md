---
name: "codebase-onboarding"
description: "代码库入职指南"
---
# 代码库入职指南

**级别：** 高级  
**类别：** 工程  
**领域：** 文档 / 开发者体验  

---

## 概述  
本指南用于分析代码库，并为特定受众生成全面的入职文档。内容包括架构概述、关键文件映射、本地设置指南、常见任务操作手册、调试指南以及代码贡献规范。文档输出格式支持 Markdown、Notion 或 Confluence。  

## 核心功能  
- **架构概述**：技术栈、系统边界、数据流图  
- **关键文件映射**：说明文件的重要性及用途，并附有注释  
- **本地设置指南**：从克隆代码到运行测试的详细步骤  
- **常见开发者任务**：如何添加路由、执行数据迁移、创建组件  
- **调试指南**：常见错误、日志位置及实用查询方法  
- **代码贡献指南**：分支策略、提交流程（PR）及代码规范  
- **针对不同受众的文档内容**：适用于初级开发者、高级工程师或合同工  

---

## 使用场景  
- 新团队成员或合同工的入职培训  
- 项目进行重大重构后（导致现有文档过时）  
- 项目开源前  
- 为服务创建团队维基页面  
- 长假前的自我学习  

---

## 代码库分析命令  
在生成文档之前，请运行以下命令以收集所需信息：  
```bash
# Project overview
cat package.json | jq '{name, version, scripts, dependencies: (.dependencies | keys), devDependencies: (.devDependencies | keys)}'

# Directory structure (top 2 levels)
find . -maxdepth 2 -not -path '*/node_modules/*' -not -path '*/.git/*' -not -path '*/.next/*' | sort | head -60

# Largest files (often core modules)
find src/ -name "*.ts" -not -path "*/test*" -exec wc -l {} + | sort -rn | head -20

# All routes (Next.js App Router)
find app/ -name "route.ts" -o -name "page.tsx" | sort

# All routes (Express)
grep -rn "router\.\(get\|post\|put\|patch\|delete\)" src/routes/ --include="*.ts"

# Recent major changes
git log --oneline --since="90 days ago" | grep -E "feat|refactor|breaking"

# Top contributors
git shortlog -sn --no-merges | head -10

# Test coverage summary
pnpm test:ci --coverage 2>&1 | tail -20
```  

---

## 生成的文档模板  

### README.md（完整模板）  
```markdown
# [Project Name]

> One-sentence description of what this does and who uses it.

[![CI](https://github.com/org/repo/actions/workflows/ci.yml/badge.svg)](https://github.com/org/repo/actions/workflows/ci.yml)
[![Coverage](https://codecov.io/gh/org/repo/branch/main/graph/badge.svg)](https://codecov.io/gh/org/repo)

## What is this?

[2-3 sentences: problem it solves, who uses it, current state]

**Live:** https://myapp.com  
**Staging:** https://staging.myapp.com  
**Docs:** https://docs.myapp.com

---

## Quick Start

### Prerequisites

| Tool | Version | Install |
|------|---------|---------|
| Node.js | 20+ | `nvm install 20` |
| pnpm | 8+ | `npm i -g pnpm` |
| Docker | 24+ | [docker.com](https://docker.com) |
| PostgreSQL | 16+ | via Docker (see below) |

### Setup (5 minutes)

```  
```bash
# 1. 克隆代码库  
git clone https://github.com/org/repo  
cd repo  

# 2. 安装依赖项  
pnpm install  

# 3. 启动基础设施  
docker compose up -d   # 启动 PostgreSQL 和 Redis  

# 4. 配置环境变量  
cp .env.example .env  
# 修改 .env 文件中的参数（可咨询同事或查看 Vault）  

# 5. 设置数据库  
pnpm db:migrate        # 执行数据迁移  
pnpm db:seed           # 可选：加载测试数据  

# 6. 启动开发服务器  
pnpm dev               # 访问地址：http://localhost:3000  

# 7. 验证代码是否正常运行  
pnpm test              # 所有测试应通过  
```  

### 代码示例  
#### 浏览器/移动端应用结构  
```bash
# 浏览器/移动端  
    │  
    ▼  
[Next.js 应用] ←──── [认证：NextAuth]  
    │  
    ├──→ [PostgreSQL]（主数据存储）  
    ├──→ [Redis]（会话存储、任务队列）  
    └──→ [S3]（文件上传）  
```  
#### 后端服务架构  
```bash
# 后端服务架构  
[BullMQ 工作进程] ←── Redis 队列  
    └──→ [外部 API：Stripe, SendGrid]  
```  

#### 路由处理函数示例  
```typescript
// app/api/my-resource/route.ts  
import { NextRequest, NextResponse } from 'next/server';  
import { auth } from '@/lib/auth';  
import { db } from '@/db/client';  

export async function GET(req: NextRequest) {  
  const session = await auth();  
  if (!session) {  
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });  
  }  
  const data = await db.query.myResource.findMany({ where: (r, { eq }) => eq(r.userId, session.user.id });  
  return NextResponse.json({ data });  
}  
```  

#### 测试文件示例  
```bash
# 添加测试用例  
touch tests/api/my-resource.test.ts  
```  

#### 数据库迁移示例  
```bash
# 生成数据库迁移脚本  
pnpm generate:openapi  
# 查看并执行迁移命令  
cat drizzle/migrations/0001_my_change.sql  
pnpm db:migrate  
# 回滚操作（手动执行）  
psql $DATABASE_URL -f scripts/rollback_0001.sql  
```  

#### 代码模板示例  
```bash
# 创建邮件发送功能  
# 创建模板文件  
touch emails/my-email.tsx  
# 预览邮件发送效果  
pnpm email:preview  
# 发送邮件  
import { sendEmail } from '@/lib/email';  
await sendEmail({ to: user.email, subject: '邮件主题', template: 'my-email', props: { name: "用户名" });  
```  

#### 工作队列示例  
```typescript
// 工作队列实现  
import { Queue, Worker } from 'bullmq';  
import { redis } from '@/lib/redis';  

export const myJobQueue = new Queue('my-job', { connection: redis });  
export const myJobWorker = new Worker('my-job', async (job) {  
  // 处理任务  
});  
// 将任务加入队列  
await myJobQueue.add('process', { userId, data });  
```  

#### 确认环境变量  
```bash
# 确认 .env 文件中包含数据库连接信息  
cat .env | grep DATABASE_URL  
# 如果 PostgreSQL 未运行，启动它  
docker compose up -d postgres  
```  

#### 其他检查命令  
```bash
# 检查用户是否存在  
# 用户是否重复注册  
Run: SELECT * FROM users WHERE email = 'test@example.com';  
```  
# 设置 JWT 令牌有效期  
# 更新 .env 文件中的令牌过期时间  
JWT_EXPIRES_IN=30d  

# 检查系统时间同步  
date && docker exec postgres date  
```  
#### 日常维护命令  
```bash
# 检查终端输出  
# 检查数据库连接  
psql $DATABASE_URL -c "SELECT 1";  
# 检查 Redis 连接  
redis-cli ping;  
# 查看日志  
pnpm dev 2>&1 | grep -E "error|Error|ERROR";  
```  

#### 数据库优化建议  
```bash
# 分析查询性能  
SELECT query, mean_exec_time, calls, total_exec_time  
FROM pg_stat_statements  
ORDER BY mean_exec_time DESC;  
```  
```  
#### 解码 JWT  
```bash
# 解码 JWT  
echo "YOUR_JWT" | cut -d. -f2 | base64 -d | jq .  
```  

---

## 针对不同受众的说明  
### 初级开发者  
- 从 `src/lib/auth.ts` 开始学习认证机制  
- 阅读 `tests/api/` 中的测试用例  
- 修改 `src/db/schema.ts` 前请先咨询他人  
- 使用 `pnpm db:seed` 生成真实的本地数据  

### 高级工程师/技术负责人  
- 架构决策记录在 `docs/adr/` 中  
- 性能测试结果在 `tests/benchmarks/baseline.json` 中  
- 安全策略在 `src/db/rls.sql` 中  
- 扩展性相关说明在 `docs/scaling.md` 中  

### 合同工  
- 仅处理 `src/features/` 目录下的代码  
- 禁止直接推送代码到 `main` 分支  
- 所有外部 API 调用需通过 `src/lib/` 中的封装层  
- 每日记录任务耗时  

---

## 文档输出格式  
详情请参阅 `references/output-format-templates.md`  

## 常见问题  
- **文档编写后不再更新**：将文档更新添加到 PR 提交清单中  
- **缺少本地设置步骤**：每季度在全新环境中测试设置流程  
- **调试信息缺失**：调试指南对新员工至关重要  
- **内容过于复杂**：合同工只需了解具体任务，无需深入了解架构  
- **缺少截图**：UI 流程需要截图  
- **忽略原因说明**：应说明决策的依据  

---

## 最佳实践  
1. **简化设置流程**：确保设置步骤不超过 10 分钟；如有困难，先优化设置而非修改文档  
2. **测试文档**：让新员工实际操作文档，及时修复问题  
3 **链接参考资料**：引用相关决策记录、问题跟踪和外部文档  
4 **同步更新**：在提交代码时同时更新文档  
5 **标注版本变更**：明确说明最近版本的变化  
6 **以实践操作为主**：提供具体命令指导（而非抽象描述）