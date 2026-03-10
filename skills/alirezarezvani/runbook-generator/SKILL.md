---
name: "runbook-generator"
description: "**Runbook Generator**"
---
# 运行手册生成器

**级别：** 高级  
**类别：** 工程  
**领域：** DevOps / 网站可靠性工程  

---

## 概述  

该工具可分析代码库并生成适用于生产环境的操作运行手册。它能自动识别您的系统架构（包括持续集成/持续部署（CI/CD）流程、数据库、托管服务以及容器环境），然后生成包含可复制/粘贴的命令、验证检查步骤、回滚流程、升级路径及时间预估的详细运行手册。同时，通过关联配置文件的修改日期来确保运行手册内容的实时性。  

---

## 核心功能  

- **系统架构检测** — 从代码仓库文件中自动识别CI/CD、数据库、托管服务及容器配置  
- **运行手册类型** — 部署、事件响应、数据库维护、扩展、监控设置  
- **格式规范** — 每个步骤都有编号；命令可复制粘贴；每个验证步骤后都标有✅符号；包含时间预估  
- **升级路径** — 设有从一级（L1）到三级（L3）的升级机制，并提供联系信息和决策标准  
- **回滚流程** — 每个部署步骤都配有相应的回滚操作  
- **内容更新检测** — 运行手册中的内容会引用配置文件；当配置文件发生变化时系统会自动标记  
- **测试机制** — 提供用于预测试环境的模拟框架，并定期（每季度）进行审查  

---

## 使用场景  

- 当代码库中缺乏运行手册且需要快速建立时  
- 当现有运行手册过时或不完整时（建议重新生成）  
- 在新工程师入职时，为他们提供清晰的操作指南  
- 在准备事件响应演练或审计时  
- 从零开始设置监控系统和值班轮换机制  

## 不适用场景  

- 当系统仍处于早期阶段，尚未形成稳定的运行模式时  
- 当运行手册已存在且只需进行小幅更新时（直接编辑即可）  

---

## 系统架构检测  

在编写运行手册之前，会扫描代码仓库以识别以下系统组件：  

```bash
# CI/CD
ls .github/workflows/     → GitHub Actions
ls .gitlab-ci.yml         → GitLab CI
ls Jenkinsfile            → Jenkins
ls .circleci/             → CircleCI
ls bitbucket-pipelines.yml → Bitbucket Pipelines

# Database
grep -r "postgresql\|postgres\|pg" package.json pyproject.toml → PostgreSQL
grep -r "mysql\|mariadb"           package.json               → MySQL
grep -r "mongodb\|mongoose"        package.json               → MongoDB
grep -r "redis"                    package.json               → Redis
ls prisma/schema.prisma            → Prisma ORM (check provider field)
ls drizzle.config.*                → Drizzle ORM

# Hosting
ls vercel.json                     → Vercel
ls railway.toml                    → Railway
ls fly.toml                        → Fly.io
ls .ebextensions/                  → AWS Elastic Beanstalk
ls terraform/  ls *.tf             → Custom AWS/GCP/Azure (check provider)
ls kubernetes/ ls k8s/             → Kubernetes
ls docker-compose.yml              → Docker Compose

# Framework
ls next.config.*                   → Next.js
ls nuxt.config.*                   → Nuxt
ls svelte.config.*                 → SvelteKit
cat package.json | jq '.scripts'   → Check build/start commands
```  

根据检测到的系统架构，生成相应的运行手册模板。例如，对于一个使用Next.js、PostgreSQL、Vercel和GitHub Actions的仓库，需要生成以下类型的运行手册：  
- **部署运行手册**（用于部署Vercel应用）  
- **数据库运行手册**（用于备份、迁移和清理数据库）  
- **事件响应运行手册**（用于处理异常情况）  
- **监控设置运行手册**（用于配置监控工具）  

---

## 运行手册类型  

### 1. 部署运行手册  

```markdown
# Deployment Runbook — [App Name]
**Stack:** Next.js 14 + PostgreSQL 15 + Vercel  
**Last verified:** 2025-03-01  
**Source configs:** vercel.json (modified: git log -1 --format=%ci -- vercel.json)  
**Owner:** Platform Team  
**Est. total time:** 15–25 min  

---

## Pre-deployment Checklist
- [ ] All PRs merged to main
- [ ] CI passing on main (GitHub Actions green)
- [ ] Database migrations tested in staging
- [ ] Rollback plan confirmed

## Steps

### Step 1 — Run CI checks locally (3 min)
```  
```bash  
pnpm test  
pnpm lint  
pnpm build  
```  
```
✅ Expected: All pass with 0 errors. Build output in `.next/`

### Step 2 — Apply database migrations (5 min)
```  
```bash  
# 先在预测试环境（staging）中部署  
DATABASE_URL=$STAGING_DATABASE_URL npx prisma migrate deploy  
```  
```
✅ Expected: `All migrations have been successfully applied.`

```  
```bash  
# 验证迁移是否成功  
psql $STAGING_DATABASE_URL -c "\d" | grep -i migration  
```  
```
✅ Expected: Migration table shows new entry with today's date

### Step 3 — Deploy to production (5 min)
```  
```bash  
# 将更改推送到主环境  
git push origin main  
```  
```
✅ Expected: Vercel dashboard shows deployment in progress. URL format:
`https://app-name-<hash>-team.vercel.app`

### Step 4 — Smoke test production (5 min)
```  
```bash  
# 进行健康检查  
curl -sf https://your-app.vercel.app/api/health | jq .  
```  
```
✅ Expected: health returns `{"status":"ok","db":"connected"}`. Users API returns valid ID.

### Step 5 — Monitor for 10 min
- Check Vercel Functions log for errors: `vercel logs --since=10m`
- Check error rate in Vercel Analytics: < 1% 5xx
- Check DB connection pool: `SELECT count(*) FROM pg_stat_activity;` (< 80% of max_connections)

---

## Rollback

If smoke tests fail or error rate spikes:

```  
**（推荐方案：**）  
# 通过Vercel快速回滚到之前的部署状态（<30秒内完成）  
vercel rollback [previous-deployment-url]  
```  
***  
**（仅当进行了数据库迁移时执行回滚操作）**  
DATABASE_URL=$PROD_DATABASE_URL npx prisma migrate reset --skip-seed  
**注意：** 此操作会将数据库恢复到迁移前的状态，请先确认数据是否受到影响。  

---

### 2. 事件响应运行手册  

```markdown
# Incident Response Runbook
**Severity levels:** P1 (down), P2 (degraded), P3 (minor)  
**Est. total time:** P1: 30–60 min, P2: 1–4 hours  

## Phase 1 — Triage (5 min)

### Confirm the incident
```  
```bash  
# 应用是否正常响应？  
curl -sw "%{http_code}" https://your-app.vercel.app/api/health -o /dev/null  
```  
***  
**检查Vercel日志（过去15分钟内的错误信息）**  
vercel logs --since=15m | grep -i "error\|exception\|5[0-9][0-9]"  
***  
**检查最近是否有新的部署操作**  
vercel ls --limit=5  
***  
**检查数据库健康状况**  
psql $DATABASE_URL -c "SELECT pid, state, wait_event, query FROM pg_stat_activity WHERE state != 'idle' LIMIT 20;"  
***  
**检查长时间运行的查询**  
psql $DATABASE_URL -c "SELECT pid, now() - pg_stat_activity.query_start AS duration, query FROM pg_stat_activity WHERE state = 'active' AND now() - pg_stat_activity.query_start > interval '30 seconds';"  
***  
**检查连接池使用情况**  
psql $DATABASE_URL -c "SELECT count(*), max_conn FROM pg_stat_activity, (SELECT setting::int AS max_conn FROM pg_settings WHERE name='max_connections') t GROUP BY max_conn;"  
***  
**终止异常运行的数据库查询**  
psql $DATABASE_URL -c "SELECT pg_terminate_backend(<pid>);"  
***  
**调整数据库连接池大小（针对Supabase/Neon环境）**  
vercel env add MAINTENANCE_MODE true production  
vercel --prod  # 重新部署应用  
***  

---

### 3. 数据库维护运行手册  

```markdown
# Database Maintenance Runbook — PostgreSQL
**Schedule:** Weekly vacuum (automated), monthly manual review  

## Backup

```  
**创建完整备份**  
pg_dump $DATABASE_URL \  
  --format=custom \  
  --compress=9 \  
  --file="backup-$(date +%Y%m%d-%H%M%S).dump  
```  
***  
**在预测试环境中恢复数据**  
psql $STAGING_DATABASE_URL backup_dump  
***  
**验证后，再在主环境中部署**  
DATABASE_URL=$PROD_DATABASE_URL npx prisma migrate deploy  
***  
**检查数据库性能**  
psql $DATABASE_URL -c "SELECT schemaname, tablename,  
       pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS total_size,  
       n_dead_tup, n_live_tup,  
       ROUND(n_dead_tup::numeric / NULLIF(n_live_tup + n_dead_tup, 0) * 100, 1) AS dead_ratio  
FROM pg_stat_user_tables  
ORDER BY n_dead_tup DESC LIMIT 10;  
***  
**清理冗余数据**  
psql $DATABASE_URL -c "VACUUM ANALYZE users;"  
psql $DATABASE_URL -c "VACUUM ANALYZE events;"  
***  
**重建索引（使用CONCURRENTLY模式以避免锁问题）**  
psql $DATABASE_URL -c "REINDEX INDEX CONCURRENTLY users_email_idx;"  
***  

---

## 内容更新检测  

在每份运行手册中添加一个标记，用于指示内容是否需要更新：  

```markdown
## Staleness Check
This runbook references the following config files. If they've changed since the
"Last verified" date, review the affected steps.

| Config File | Last Modified | Affects Steps |
|-------------|--------------|---------------|
| vercel.json | `git log -1 --format=%ci -- vercel.json` | Step 3, Rollback |
| prisma/schema.prisma | `git log -1 --format=%ci -- prisma/schema.prisma` | Step 2, DB Maintenance |
| .github/workflows/deploy.yml | `git log -1 --format=%ci -- .github/workflows/deploy.yml` | Step 1, Step 3 |
| docker-compose.yml | `git log -1 --format=%ci -- docker-compose.yml` | All scaling steps |
```  

**自动化建议：**  
安排每周自动执行一次CI任务，如果运行手册中引用的文件在最近被修改过，就在文档中添加注释。  

---

## 运行手册测试机制  

### 在预测试环境中进行模拟测试  

在将运行手册应用于生产环境之前，务必在预测试环境中验证每个步骤的正确性：  

```bash
# 1. Create a staging environment mirror
vercel env pull .env.staging
source .env.staging

# 2. Run each step with staging credentials
# Replace all $DATABASE_URL with $STAGING_DATABASE_URL
# Replace all production URLs with staging URLs

# 3. Verify expected outputs match
# Document any discrepancies and update the runbook

# 4. Time each step — update estimates in the runbook
time npx prisma migrate deploy
```  

### 定期审查机制  

每季度安排一次1小时的审查会议：  
1. 在预测试环境中执行所有命令，确认其是否仍能正常工作  
2. 检查配置文件是否发生变化  
3. 测试回滚流程  
4. 更新联系信息（可能因人员变动而需要更新）  
5. 添加过去季度中发现的新故障处理方式  
6. 更新运行手册顶部的“最后验证日期”  

---

## 常见问题及解决方法  

| 问题 | 解决方案 |  
|---|---|  
| 需要手动输入动态值的命令 | 使用环境变量（如 `$DATABASE_URL`，而非 `postgres://user:pass@host/db`）  
| 没有指定预期输出结果 | 在每个验证步骤后添加✅符号，并明确说明预期输出内容  
| 缺少回滚步骤 | 每个可能破坏数据的操作都必须有对应的回滚措施  
| 运行手册从未被测试过 | 定期在团队日历中安排预测试  
| 三级升级联系人仍是之前的CTO | 每季度更新联系人信息  
| 迁移运行手册未提及表锁问题 | 明确指出大规模表操作可能导致的锁风险  

---

## 最佳实践建议：  

1. 所有命令都必须能够直接复制粘贴（避免使用占位符文本，使用环境变量）  
2. 每个步骤后都应标注✅符号，并明确说明预期输出结果  
3. 必须提供时间预估，以便工程师了解是否有足够时间在服务级别协议（SLA）超期前解决问题  
4. 在部署前先执行回滚操作  
5. 运行手册应存储在代码仓库中，并与所描述的代码版本同步更新  
6. 每次事件处理结束后都应更新运行手册  
7. 只引用官方配置文件，不要将其内容复制到运行手册中  
8. 像测试代码一样测试运行手册——未经测试的运行手册毫无价值（反而会带来误导）