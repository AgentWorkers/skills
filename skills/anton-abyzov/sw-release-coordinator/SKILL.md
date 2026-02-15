---
name: release-coordinator
description: 多仓库发布协调机制——包括依赖关系管理、发布顺序的编排以及跨仓库的验证功能。该机制用于实现多服务之间的同步发布。
---

# 发布协调员

**专业技能**：多仓库发布编排、依赖管理、发布顺序规划以及跨仓库验证。

## 核心能力

### 1. 发布依赖管理

**理解并管理发布顺序**：

**依赖类型**：
```yaml
# Build-time dependencies
shared-lib: v2.0.0
  └─ service-a: v3.1.0 (depends on shared-lib)
  └─ service-b: v2.5.0 (depends on shared-lib)

# Runtime dependencies
auth-service: v1.8.0
  └─ api-gateway: v2.0.0 (calls auth-service)
     └─ frontend: v3.2.0 (calls api-gateway)

# Data schema dependencies
database-migrations: v10
  └─ backend-services: v2.x (requires schema v10)
```

**发布顺序计算**：
1. 构建依赖关系图
2. 通过拓扑排序确定正确的发布顺序
3. 识别循环依赖（错误）
4. 生成发布批次：
   - 第一批：无依赖项（共享库、数据库迁移）
   - 第二批：依赖于第一批（服务A、服务B）
   - 第三批：依赖于第二批（API网关）
   - 第四批：依赖于第三批（前端）

**示例发布计划**：
```markdown
## Release Order for Product v3.0.0

### Wave 1 (Foundations)
- [ ] shared-lib: v2.0.0 → v3.0.0
- [ ] database-migrations: v9 → v10

### Wave 2 (Backend Services)
- [ ] auth-service: v1.8.0 → v2.0.0 (depends: shared-lib v3.0.0)
- [ ] user-service: v1.5.0 → v2.0.0 (depends: shared-lib v3.0.0, schema v10)
- [ ] order-service: v2.1.0 → v3.0.0 (depends: shared-lib v3.0.0, schema v10)

### Wave 3 (API Layer)
- [ ] api-gateway: v2.0.0 → v3.0.0 (depends: auth-service v2.0.0, user-service v2.0.0)

### Wave 4 (Frontend)
- [ ] web-app: v3.2.0 → v4.0.0 (depends: api-gateway v3.0.0)
- [ ] mobile-app: v2.5.0 → v3.0.0 (depends: api-gateway v3.0.0)

**Total Duration**: ~4 hours (waves run sequentially, repos in wave release in parallel)
```

### 2. 协调发布策略

**同步版本控制**（所有仓库使用相同版本）：
```yaml
Product: v3.0.0
Repositories:
  - frontend: v3.0.0
  - backend: v3.0.0
  - api: v3.0.0
  - shared: v3.0.0

Benefits:
  - Simple to understand (one version = one product state)
  - Clear API compatibility
  - Easier rollback (revert entire product)

Challenges:
  - Forces releases even if no changes
  - High coordination overhead
  - All teams must sync

Use When:
  - Tight coupling between repos
  - Small team (all work together)
  - Breaking changes affect all repos
```

**独立版本控制**（每个仓库有自己的版本）：
```yaml
Product: N/A
Repositories:
  - frontend: v4.2.0
  - backend: v2.8.0
  - api: v3.1.0
  - shared: v1.5.0

Benefits:
  - Autonomous teams
  - Release when ready
  - No forced releases

Challenges:
  - Complex compatibility matrix
  - Hard to understand product state
  - Testing combinations expensive

Use When:
  - Loose coupling between repos
  - Large team (independent squads)
  - Frequent releases (daily/weekly)
```

**统一版本控制**（产品版本 + 服务版本）：
```yaml
Product: v5.0.0 (umbrella)
├─ frontend: v4.2.0
├─ backend: v2.8.0
├─ api: v3.1.0
└─ shared: v1.5.0

Benefits:
  - Clear product milestones (v5.0.0 = major release)
  - Internal flexibility (services version independently)
  - Best of both worlds

Challenges:
  - Version matrix tracking
  - Compatibility validation

Use When:
  - Medium/large team
  - Product-level milestones important
  - Services evolve at different rates
```

### 3. 创建发布增量

**创建跨仓库的发布增量**：

**单仓库发布增量**：
```
.specweave/increments/0020-backend-v2-release/
├── spec.md           # What's being released
├── plan.md           # Release execution plan
├── tasks.md          # Release checklist
└── metadata.json     # Repository: backend, target: v2.0.0
```

**多仓库发布增量**：
```
.specweave/increments/0025-product-v3-release/
├── spec.md           # Product release overview
├── plan.md           # Cross-repo orchestration
├── tasks.md          # Multi-repo checklist
└── metadata.json     # Repositories: [frontend, backend, api], umbrella: v3.0.0
```

**spec.md 示例**：
```markdown
# Product v3.0.0 Release

## Release Type
Umbrella (coordinated major version)

## Repositories
- frontend: v3.2.0 → v4.0.0
- backend: v2.5.0 → v3.0.0
- api-gateway: v2.8.0 → v3.0.0
- shared-lib: v1.8.0 → v2.0.0

## Key Changes
- **Breaking**: API v2 → v3 (remove legacy endpoints)
- **Feature**: Real-time notifications (WebSocket)
- **Performance**: 50% faster API response time

## Release Waves
See plan.md for detailed orchestration

## Success Criteria
- [ ] All repos tagged (v3.0.0 umbrella)
- [ ] GitHub releases published
- [ ] Changelogs updated
- [ ] Packages published (NPM/Docker)
- [ ] Deployed to production
- [ ] Smoke tests passing
- [ ] DORA metrics: Lead time <1 day
```

### 4. 发布前验证

**跨仓库验证检查**：

**发布前**：
```bash
# 1. Version Compatibility
✓ shared-lib v2.0.0 compatible with service-a v3.0.0
✓ API contracts match between gateway and services
✗ Database schema v10 required by backend, but only v9 deployed

# 2. CI/CD Status
✓ All tests passing in all repos
✓ No pending code review comments
✗ Staging deployment failed for frontend

# 3. Dependency Versions
✓ All repos use shared-lib v2.0.0
✓ No conflicting dependency versions
✗ service-b still using deprecated shared-lib v1.5.0

# 4. Documentation
✓ CHANGELOG.md updated in all repos
✓ API docs regenerated
✗ Migration guide missing for breaking changes

# 5. Release Notes
✓ All commits since last release analyzed
✓ Breaking changes documented
✗ Missing highlights section
```

**问题报告**：
```markdown
## Pre-Release Validation: BLOCKED ❌

### Blockers (MUST FIX)
1. **Database schema mismatch**:
   - Backend requires schema v10
   - Current production: schema v9
   - Action: Deploy migration v9→v10 first

2. **Frontend staging failure**:
   - Build error: Module 'api-client' not found
   - Cause: API client v3.0.0 not published yet
   - Action: Publish api-client first (Wave 1)

3. **Outdated dependency**:
   - service-b using shared-lib v1.5.0 (deprecated)
   - Required: shared-lib v2.0.0
   - Action: Update service-b, test, then release

### Warnings (Should Fix)
1. Missing migration guide for API v2→v3
2. Incomplete release notes (missing highlights)

### Ready to Release
- auth-service v2.0.0 ✓
- user-service v2.0.0 ✓
- shared-lib v2.0.0 ✓
```

### 5. 发布执行编排

**自动化发布工作流程**：
```bash
# Command
/sw-release:execute 0025-product-v3-release

# Executes:
1. Pre-flight checks (validation)
2. Wave 1: Release shared-lib, database-migrations
   - Wait for CI/CD success
   - Verify package published
3. Wave 2: Release backend services (parallel)
   - auth-service, user-service, order-service
   - Wait for CI/CD success
4. Wave 3: Release api-gateway
   - Wait for CI/CD success
5. Wave 4: Release frontend apps (parallel)
   - web-app, mobile-app
   - Wait for CI/CD success
6. Post-release validation
   - Smoke tests
   - Health checks
   - Monitor for 1 hour
7. Update living docs
   - Sync release-strategy.md
   - Update version matrix
8. Notify stakeholders
   - Slack/email: "Product v3.0.0 released"
   - DORA metrics: Deployment frequency +1
```

### 6. 回滚协调

**多仓库回滚**：
```markdown
## Rollback Plan: Product v3.0.0 → v2.5.0

### Trigger
- Critical bug in api-gateway v3.0.0
- Affected: 20% of API calls failing

### Strategy
Reverse wave order (rollback dependencies first)

### Wave 1 (Rollback Frontend First)
- [ ] web-app: v4.0.0 → v3.2.0
- [ ] mobile-app: v3.0.0 → v2.5.0

### Wave 2 (Rollback API Layer)
- [ ] api-gateway: v3.0.0 → v2.8.0

### Wave 3 (Rollback Backend - Optional)
- [ ] Keep backend services at v3.0.0 (backward compatible)
- [ ] If needed: auth-service v2.0.0 → v1.8.0

### Wave 4 (Rollback Shared - Optional)
- [ ] Keep shared-lib at v2.0.0 (no bugs reported)

**Duration**: ~30 minutes (frontend + gateway only)
**Impact**: Minimal (API compatible with older clients)
```

### 7. 与 SpecWeave 工作流程集成

**发布增量生命周期**：
```bash
# 1. Plan release
/sw:increment "0025-product-v3-release"
# → Creates increment with multi-repo spec

# 2. Coordinate release (this skill activates)
# → Analyzes dependencies
# → Generates release waves
# → Creates validation checklist

# 3. Execute release
/sw:do
# → Runs pre-flight checks
# → Executes wave-by-wave
# → Monitors progress

# 4. Complete release
/sw:done 0025
# → Validates all repos released
# → Updates living docs
# → Syncs to GitHub/Jira/ADO
```

## 何时使用此技能

**请告诉我**：

1. **协调多仓库发布**：
   - “为5个微服务规划发布”
   - “协调后端和前端的发布”
   - “创建跨仓库的发布计划”

2. **管理发布依赖**：
   - “我们应该按什么顺序发布仓库？”
   - “哪些服务依赖于共享库？”
   - “计算发布批次”

3. **进行发布前验证**：
   - “检查我们是否准备好发布”
   - “验证跨仓库的兼容性”
   - “运行预发布检查”

4. **执行协调发布**：
   - “发布产品v3.0.0”
   - “执行统一版本发布”
   - “按批次部署”

5. **规划回滚**：
   - “为v3.0.0创建回滚计划”
   - “如果前端失败该如何回滚？”
   - “反转发布顺序”

## 最佳实践

**依赖管理**：
- 在 `release-strategy.md` 中记录依赖关系
- 自动检测依赖关系（`package.json`、导入项）
- 固定共享库的版本（避免版本浮动）

**发布窗口**：
- 在流量较低的时段安排发布
- 预留回滚时间（发布持续时间的两倍）
- 通知发布期间的禁用时段（节假日、周末）

**验证步骤**：
- 绝不跳过预发布检查（尽早发现问题）
- 自动化验证（CI/CD 流程）
- 生产环境的手动审批步骤

**沟通**：
- 在发布前一天通知所有团队
- 发布过程中实时更新状态
- 发布后总结（DORA指标、问题）

## 集成点

**发布策略顾问**：
- 阅读 `release-strategy.md` 以了解发布策略
- 根据策略类型调整协调方式
- 根据问题提出改进建议

**版本对齐器**：
- 使用版本对齐规则
- 确保各仓库之间的兼容性
- 验证 semver 规则

**RC 管理员**：
- 协调 RC 发布（预生产阶段）
- 在生产前验证 RC
- 将 RC 提升为最终版本

**动态文档**：
- 记录发布历史
- 更新版本矩阵
- 提供 GitHub 发布链接

## 示例工作流程

### 微服务协调发布
```bash
# 1. User initiates release
/sw:increment "0030-product-v4-release"

# 2. Coordinator analyzes
# - 8 microservices detected
# - Dependency graph: shared-lib → services → gateway → frontend
# - Release strategy: Umbrella versioning

# 3. Generates plan
# - Wave 1: shared-lib v3.0.0, database-migrations v15
# - Wave 2: 6 backend services (parallel)
# - Wave 3: api-gateway v4.0.0
# - Wave 4: web + mobile apps (parallel)

# 4. Pre-flight validation
# - All tests passing ✓
# - No blocking dependencies ✓
# - Changelogs updated ✓
# - Ready to release ✓

# 5. Execute release
/sw:do
# - Wave 1 released (15 min)
# - Wave 2 released (20 min, parallel)
# - Wave 3 released (10 min)
# - Wave 4 released (25 min, parallel)
# Total: 70 minutes

# 6. Post-release
# - All smoke tests passing ✓
# - DORA metrics updated ✓
# - Stakeholders notified ✓
# - Living docs synced ✓
```

### 单仓库发布（Lerna）
```bash
# 1. User initiates release
/sw:increment "0035-monorepo-v2-release"

# 2. Coordinator analyzes
# - Lerna monorepo (12 packages)
# - Independent versioning
# - Changes detected in 4 packages

# 3. Generates plan
# - @myapp/shared: v1.5.0 → v1.6.0 (patch)
# - @myapp/api-client: v2.0.0 → v2.1.0 (minor)
# - @myapp/web: v3.2.0 → v3.3.0 (minor)
# - @myapp/mobile: v2.8.0 → v2.8.1 (patch)

# 4. Dependency order
# - shared → api-client → (web, mobile)

# 5. Execute release
npx lerna publish --conventional-commits
# - Shared released first
# - API client released second
# - Web and mobile released in parallel
```

## 命令集成

支持的发布命令：
- `/sw-release:coordinate <increment>` - 规划多仓库发布
- `/sw-release:validate <increment>` - 运行预发布检查
- `/sw-release:execute <increment>` - 执行协调发布
- `/sw-release:rollback <increment>` - 回滚协调发布

## 所需工具

**必备工具**：
- Git（版本标签）
- SpecWeave 核心组件（发布增量生命周期管理）
- 发布策略文档

**可选工具**：
- GitHub CLI (`gh`) - GitHub 发布管理
- NPM (`npm`) - NPM 包检测
- Docker (`docker`) - 容器镜像检测
- Kubernetes (`kubectl`) - 部署验证

**输出结果**

**创建/更新**：
- 发布增量文件（`spec.md`、`plan.md`、`tasks.md`）
- 发布批次文档
- 预发布验证报告
- 回滚计划
- 动态文档中的发布历史记录

**提供内容**：
- 依赖关系图可视化
- 发布顺序（拓扑排序）
- 预发布验证状态
- 实时发布进度
- 发布后指标

---

**记住**：对于多仓库架构来说，发布协调至关重要。务必：
- 在发布前了解依赖关系
- 验证跨仓库的兼容性
- 按批次执行发布（切勿一次性全部发布）
- 准备好回滚计划
- 发布后至少监控一小时

**目标**：实现跨多个仓库的安全、可预测且可重复的协调发布。