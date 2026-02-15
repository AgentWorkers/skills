---
name: version-aligner
description: 多仓库版本管理策略：同步更新、独立更新、统一管理；遵循semver规范；版本冲突检测。
---

# 版本对齐工具

**专业能力**：多仓库版本对齐、语义化版本控制、版本冲突检测以及兼容性验证。

## 核心功能

### 1. 语义化版本控制（Semver）

**强制执行 Semver 规则**：

**格式**：`MAJOR.MINOR.PATCH[-PRERELEASE][+BUILD]`

**版本升级规则**：
```yaml
MAJOR (1.0.0 → 2.0.0):
  - Breaking changes (incompatible API)
  - Remove features
  - Change behavior of existing features
  Examples:
    - Remove deprecated endpoints
    - Change function signatures
    - Modify data formats

MINOR (1.0.0 → 1.1.0):
  - New features (backward compatible)
  - Add endpoints/functions
  - Deprecate (but don't remove) features
  Examples:
    - Add new API endpoints
    - Add optional parameters
    - New module exports

PATCH (1.0.0 → 1.0.1):
  - Bug fixes (no API changes)
  - Performance improvements
  - Documentation updates
  Examples:
    - Fix null pointer error
    - Optimize database query
    - Update README
```

**预发布标签**：
```yaml
# Alpha: Early development (unstable)
1.0.0-alpha.1, 1.0.0-alpha.2, ...

# Beta: Feature complete (testing)
1.0.0-beta.1, 1.0.0-beta.2, ...

# RC: Release candidate (near production)
1.0.0-rc.1, 1.0.0-rc.2, ...

# Final: Production release
1.0.0
```

### 2. 版本对齐策略

**同步版本控制**（所有仓库使用相同版本）：
```yaml
Strategy: Lockstep
Current State:
  - frontend: v2.5.0
  - backend: v2.5.0
  - api: v2.5.0
  - shared: v2.5.0

Proposed Bump: MAJOR (breaking change in API)
New State:
  - frontend: v3.0.0
  - backend: v3.0.0
  - api: v3.0.0
  - shared: v3.0.0

Rules:
  - ALL repos MUST bump together
  - Use highest bump type (if any repo needs MAJOR, all bump MAJOR)
  - Version always stays in sync
```

**独立版本控制**（每个仓库有自己的版本）：
```yaml
Strategy: Independent
Current State:
  - frontend: v4.2.0
  - backend: v2.8.0
  - api: v3.1.0
  - shared: v1.5.0

Changes:
  - frontend: Bug fix → PATCH bump
  - backend: New feature → MINOR bump
  - api: No changes → No bump
  - shared: Breaking change → MAJOR bump

New State:
  - frontend: v4.2.1 (patch)
  - backend: v2.9.0 (minor)
  - api: v3.1.0 (unchanged)
  - shared: v2.0.0 (major)

Rules:
  - Each repo versions independently
  - Only bump repos with changes
  - Validate compatibility constraints
```

**伞形版本控制**（产品版本 + 服务版本）：
```yaml
Strategy: Umbrella
Product: v5.0.0 (umbrella)

Version Matrix:
  - frontend: v4.2.0
  - backend: v2.8.0
  - api: v3.1.0
  - shared: v1.5.0

Changes for Product v6.0.0:
  - frontend: v4.2.0 → v5.0.0 (major redesign)
  - backend: v2.8.0 → v2.9.0 (new endpoints)
  - api: v3.1.0 → v4.0.0 (breaking changes)
  - shared: v1.5.0 → v1.5.0 (no changes)

New Product: v6.0.0 (umbrella)
  - frontend: v5.0.0
  - backend: v2.9.0
  - api: v4.0.0
  - shared: v1.5.0

Rules:
  - Product version bumps for milestones
  - Services version independently
  - Track matrix in release-strategy.md
```

### 3. 传统提交分析

**分析提交以建议版本升级**：

**提交模式**：
```bash
# MAJOR (breaking change)
feat!: remove legacy authentication
BREAKING CHANGE: Old auth endpoints removed

# MINOR (new feature)
feat: add real-time notifications
feat(api): add WebSocket support

# PATCH (bug fix)
fix: prevent null pointer in user service
fix(ui): correct button alignment
perf: optimize database queries

# No version bump
docs: update README
chore: upgrade dependencies
style: format code
refactor: extract helper function
test: add unit tests
```

**版本升级计算**：
```bash
# Example commit history
git log v2.5.0..HEAD --oneline

feat!: remove deprecated endpoints       # BREAKING
feat: add dark mode toggle               # FEATURE
fix: prevent crash on logout             # BUGFIX
docs: update API documentation           # NO BUMP
chore: upgrade React to v18              # NO BUMP

# Analysis
Breaking changes: 1 → MAJOR bump (v2.5.0 → v3.0.0)
Features: 1 → Overridden by MAJOR
Bug fixes: 1 → Overridden by MAJOR

# Suggested: v2.5.0 → v3.0.0
```

### 4. 版本冲突检测

**检测不兼容的版本**：

**依赖版本冲突**：
```yaml
# Scenario: Two services depend on different versions of shared-lib

service-a:
  package.json: "shared-lib": "^2.0.0"
  Currently using: v2.0.0 ✓

service-b:
  package.json: "shared-lib": "^1.5.0"
  Currently using: v1.8.0 ✗

Conflict:
  - service-a requires shared-lib v2.x (breaking changes)
  - service-b still on shared-lib v1.x (outdated)
  - Cannot release until service-b upgrades

Resolution:
  1. Update service-b to "shared-lib": "^2.0.0"
  2. Test service-b with shared-lib v2.0.0
  3. Release service-b
  4. Then proceed with coordinated release
```

**API 合同版本冲突**：
```yaml
# Scenario: Frontend expects API v3, but backend provides v2

frontend:
  api-client: v3.0.0
  Expects: POST /api/v3/users (new endpoint)

backend:
  Current version: v2.8.0
  Provides: POST /api/v2/users (old endpoint)

Conflict:
  - Frontend expects v3 API
  - Backend hasn't released v3 yet
  - Deployment will fail

Resolution:
  1. Release backend v3.0.0 first (Wave 1)
  2. Verify API v3 endpoints work
  3. Then release frontend v5.0.0 (Wave 2)
```

### 5. 兼容性验证

**验证跨仓库的兼容性**：

**Semver 范围检查**：
```typescript
// Example: Validate service-a can work with shared-lib versions

// service-a/package.json
{
  "dependencies": {
    "shared-lib": "^2.0.0"  // Allows 2.0.0 to <3.0.0
  }
}

// Validation
shared-lib v2.0.0 → Compatible ✓
shared-lib v2.5.0 → Compatible ✓
shared-lib v2.9.9 → Compatible ✓
shared-lib v3.0.0 → Incompatible ✗ (MAJOR change)
```

**API 合同验证**：
```yaml
# OpenAPI spec comparison

api-gateway v2.8.0 (current):
  POST /api/v2/users:
    parameters:
      - name: email (required)
      - name: password (required)

api-gateway v3.0.0 (proposed):
  POST /api/v3/users:
    parameters:
      - name: email (required)
      - name: password (required)
      - name: phoneNumber (optional)  # NEW (backward compatible)

Compatibility:
  - New optional field → Minor version bump (v2.8.0 → v2.9.0) ✗
  - But route changed (/v2 → /v3) → Major version bump (v3.0.0) ✓
  - Verdict: v3.0.0 is correct ✓
```

### 6. 版本矩阵管理

**跟踪伞形发布的版本**：

**版本矩阵文档**：
```markdown
# Product Version Matrix

## v6.0.0 (Latest - 2025-01-15)
- frontend: v5.0.0
- backend: v2.9.0
- api-gateway: v4.0.0
- auth-service: v2.1.0
- user-service: v2.0.0
- order-service: v3.2.0
- shared-lib: v2.0.0
- database-schema: v12

## v5.0.0 (Previous - 2024-12-10)
- frontend: v4.2.0
- backend: v2.8.0
- api-gateway: v3.1.0
- auth-service: v2.0.0
- user-service: v1.8.0
- order-service: v3.1.0
- shared-lib: v1.5.0
- database-schema: v11

## Compatibility Matrix

| Product | Frontend | Backend | API Gateway | Shared Lib | Schema |
|---------|----------|---------|-------------|------------|--------|
| v6.0.0  | v5.0.0   | v2.9.0  | v4.0.0      | v2.0.0     | v12    |
| v5.0.0  | v4.2.0   | v2.8.0  | v3.1.0      | v1.5.0     | v11    |
| v4.0.0  | v3.5.0   | v2.5.0  | v2.8.0      | v1.2.0     | v10    |

## Breaking Changes

### v6.0.0
- API Gateway v3 → v4: Removed legacy /v2 endpoints
- Shared Lib v1 → v2: Changed authentication interface
- Schema v11 → v12: Added user_metadata table

### v5.0.0
- Frontend v4 → v5: React 16 → 18 (requires Node.js 18+)
- User Service v1 → v2: Changed user creation API
```

### 7. 自动化版本升级

**建议并执行版本升级**：

**交互式版本升级**：
```bash
# Command
/sw-release:align

# Interactive prompts
? Which repositories to align?
  ◉ frontend (v4.2.0)
  ◉ backend (v2.8.0)
  ◉ api-gateway (v3.1.0)
  ◯ shared-lib (v2.0.0) - no changes

? Alignment strategy?
  ◯ Lockstep (all repos same version)
  ◉ Independent (bump changed repos only)
  ◯ Umbrella (product milestone)

# Analysis
Analyzing conventional commits since last release...

frontend (v4.2.0):
  - 12 commits since v4.2.0
  - Breaking changes: 1
  - Features: 3
  - Bug fixes: 5
  Suggested: v5.0.0 (MAJOR)

backend (v2.8.0):
  - 8 commits since v2.8.0
  - Features: 2
  - Bug fixes: 3
  Suggested: v2.9.0 (MINOR)

api-gateway (v3.1.0):
  - 15 commits since v3.1.0
  - Breaking changes: 2
  - Features: 4
  Suggested: v4.0.0 (MAJOR)

? Confirm version bumps?
  ◉ frontend: v4.2.0 → v5.0.0
  ◉ backend: v2.8.0 → v2.9.0
  ◉ api-gateway: v3.1.0 → v4.0.0

[Yes / No / Edit]
```

**自动化执行**：
```bash
# Updates package.json
npm version major  # frontend
npm version minor  # backend
npm version major  # api-gateway

# Creates git tags
git tag v5.0.0 (frontend)
git tag v2.9.0 (backend)
git tag v4.0.0 (api-gateway)

# Updates CHANGELOG.md
# - Extracts commits since last tag
# - Groups by type (breaking, features, fixes)
# - Generates markdown

# Updates version matrix
# - Adds new product version row
# - Links to service versions
# - Documents breaking changes
```

## 适用场景

**请使用此工具进行以下操作**：

1. **对齐多个仓库的版本**：
   - “对齐所有微服务的版本”
   - “在发布前同步版本”
   - “我们应该将版本升级到哪个版本？”

2. **检测版本冲突**：
   - “检查版本冲突”
   - “验证跨仓库的兼容性”
   - “我们的依赖关系是否对齐？”

3. **建议版本升级**：
   - “我们应该将版本升级到哪个版本？”
   - “分析提交以确定是否需要升级”
   - “从提交记录中计算 Semver 版本”

4. **管理版本矩阵**：
   - “更新版本矩阵”
   - “显示兼容性矩阵”
   - **跟踪伞形发布的版本历史**

5. **验证兼容性**：
   - “前端 v5.0.0 能与后端 v2.8.0 兼容吗？”
   - “检查 API 合同的兼容性”
   - **验证依赖关系的版本范围”

## 最佳实践

**Semver 规范**：
- 严禁跳过版本号（例如，从 v1.0.0 直接升级到 v1.2.0，而应升级到 v1.1.0）
- 使用预发布标签进行测试（如 v1.0.0-rc.1）
- 清晰记录破坏性变更

**依赖管理**：
- 固定主要版本号（例如，使用 “^2.0.0” 而不是 “*”）
- 定期更新依赖关系（避免版本差异）
- 在升级前测试兼容性

**版本矩阵**：
- 每次产品发布后更新版本矩阵
- 将版本矩阵链接到破坏性变更的文档
- 跟踪版本淘汰的时间线

**自动化**：
- 使用传统的提交格式（支持自动化分析）
- 自动生成变更日志
- 在持续集成/持续部署（CI/CD）过程中验证版本

## 集成点

**发布策略顾问**：
- 从 `release-strategy.md` 文件中读取版本对齐策略
- 适应同步版本控制、独立版本控制或伞形版本控制的场景

**发布协调员**：
- 提供版本升级建议
- 在发布前验证兼容性
- 发布后更新版本矩阵

**预发布版本管理员**：
- 管理预发布版本标签
- 将预发布版本推进到最终版本
- 跟踪预发布版本的变更历史

**旧系统分析工具**：
- 检测现有的版本模式
- 提取当前的版本矩阵
- 建议改进版本对齐方式

## 示例工作流程

### 独立版本控制
```bash
# 1. Analyze changes
/sw-release:align

# 2. Review suggested bumps
Frontend v4.2.0 → v5.0.0 (breaking changes)
Backend v2.8.0 → v2.9.0 (new features)
API v3.1.0 → v3.1.1 (bug fixes only)

# 3. Validate compatibility
✓ Frontend v5.0.0 compatible with Backend v2.8.0+
✓ Backend v2.9.0 compatible with API v3.1.0+
✗ Shared-lib v1.5.0 outdated (requires v2.0.0)

# 4. Fix blocking issues
Update Backend to use shared-lib v2.0.0

# 5. Execute version bumps
✓ All versions aligned
✓ Tags created
✓ Changelogs updated
```

### 伞形版本控制
```bash
# 1. Create product release
/sw:increment "0040-product-v6-release"

# 2. Analyze component versions
Current umbrella: v5.0.0
Proposed: v6.0.0 (major milestone)

# 3. Review version matrix
Frontend: v4.2.0 → v5.0.0 (redesign)
Backend: v2.8.0 → v2.9.0 (new API)
API: v3.1.0 → v4.0.0 (breaking changes)
Shared: v1.5.0 → v2.0.0 (breaking changes)

# 4. Validate umbrella bump
Breaking changes detected → MAJOR bump correct ✓
Product v5.0.0 → v6.0.0 ✓

# 5. Update version matrix
.specweave/docs/internal/delivery/version-matrix.md updated ✓
```

## 命令集成

支持以下发布命令：
- `/sw-release:align` – 交互式版本对齐
- `/sw-release:validate-versions` – 检查兼容性
- `/sw-release:bump <仓库> <类型>` – 升级特定仓库的版本
- `/sw-release:matrix` – 显示版本矩阵

## 所需工具

**必备**：
- Git（用于版本标签管理）
- Semver 库（用于版本解析）
- SpecWeave 核心组件（用于生成文档）

**可选**：
- NPM（`npm version`）– 自动化版本升级
- 传统提交格式（用于提交分析）
- GitHub CLI（`gh release`）– 用于生成发布说明

## 输出结果

**创建/更新**：
- `package.json`（包含版本信息）
- Git 标签（如 v1.0.0、v2.0.0 等）
- `CHANGELOG.md`（发布说明）
- `.specweave/docs/internal/delivery/version-matrix.md`（版本矩阵文档）
- 发布策略文档

**提供**：
- 版本升级建议
- 兼容性验证报告
- 版本冲突检测结果
- 依赖关系图
- 版本历史记录

---

**请记住**：对于多仓库架构来说，版本对齐至关重要。务必：
- 严格遵循语义化版本控制规则
- 在发布前验证兼容性
- 清晰记录破坏性变更
- 定期更新版本矩阵
- 在可能的情况下实现自动化（使用传统的提交格式和 Semver 规范）

**目标**：确保所有仓库的版本控制一致、可预测，并提供明确的兼容性保障。