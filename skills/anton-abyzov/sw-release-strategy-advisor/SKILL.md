---
name: release-strategy-advisor
description: 发布策略顾问：能够识别代码库中的“旧代码”模式（如特定标签、持续集成/持续部署（CI/CD）流程、变更日志等），并根据应用程序的架构推荐合适的版本管理策略。该工具会生成名为 `release-strategy.md` 的文档文件。
---

# 释放策略顾问

**专业领域**：发布管理策略设计、版本对齐、旧代码库（brownfield）的发布模式检测，以及发布流程的动态文档编制。

## 核心能力

### 1. 旧代码库发布模式检测

**分析现有项目以检测发布模式**：

**Git 分析**：
- 版本标签（如 v1.0.0、v2.1.0-rc.1 等）
- 标签格式（语义版本控制、基于日期的版本控制、自定义标签）
- 发布分支（如 release/*、hotfix/*）
- 标签的发布频率和节奏

**持续集成/持续部署（CI/CD）检测**：
- GitHub Actions 工作流（`.github/workflows/release.yml`）
- GitLab CI（`.gitlab-ci.yml`）
- Jenkins 管道（`Jenkinsfile`）
- CircleCI 配置（`.circleci/config.yml`）
- Azure Pipelines（`azure-pipelines.yml`）

**包管理器**：
- NPM：`package.json`（版本信息、发布脚本）
- Python：`setup.py`、`pyproject.toml`
- Java：`pom.xml`、`build.gradle`
- Go：`go.mod`
- Ruby：`*.gemspec`
- Rust：`Cargo.toml`

**单代码库工具**：
- Lerna（`lerna.json`）
- Nx（`nx.json`、`workspace.json`）
- Turborepo（`turbo.json`）
- Yarn Workspaces（`package.json`）
- 变更集（`.changeset/config.json`）

**发布自动化**：
- 语义版本控制（`.releaserc`、`release.config.js`）
- 标准版本控制（`.versionrc`）
- 传统的变更日志格式
- 自定义发布脚本

### 2. 策略建议

**根据以下因素建议最佳策略**：

**项目架构**：
- 单个代码库 → 简单的语义版本控制策略
- 多个代码库（2-5 个） → 协调发布或独立发布
- 多个代码库（5 个以上） → 总体版本控制
- 单代码库 → 基于工作区的版本控制
- 微服务 → 服务级别的版本控制

**团队规模**：
- 小团队（1-5 人） → 简单的手动发布
- 中等团队（5-20 人） → 半自动化发布
- 大团队（20 人以上） → 完全自动化发布

**部署频率**：
- 低频率（<1/月） → 手动发布
- 中等频率（1-4/月） → 半自动化发布
- 高频率（每日/每周） → 自动化的 CI/CD
- 持续部署 → 基于主干分支的发布 + 特性开关

**依赖关系**：
- 无依赖关系 → 独立发布
- 耦合度低 → 独立发布但需要协调
- 耦合度高 → 协调发布
- 共享库 → 总体版本控制

### 3. 发布策略类型

**单代码库策略**：
```markdown
## Simple Semver
- One repository, one version
- Manual or automated bumps (patch/minor/major)
- GitHub releases + NPM/PyPI publish
- CHANGELOG.md maintenance
- Example: SpecWeave itself
```

**多代码库策略**：
```markdown
## Coordinated Releases
- All repos share same version
- Release together (v1.0.0 across all)
- Synchronized CI/CD
- Example: Microservices with tight coupling

## Independent Releases
- Each repo has own version
- Release independently
- Example: service-a v2.1.0, service-b v1.5.0

## Umbrella Versioning
- Product version (v3.0.0) spans multiple repos
- Internal service versions tracked separately
- Example: "Product v3.0.0" contains:
  - frontend v2.5.0
  - backend v1.8.0
  - api v2.1.0
```

**单代码库策略**：
```markdown
## Workspace-Based
- Lerna/Nx/Turborepo manage versions
- Independent package versions
- Changesets for semantic release
- Example: Babel, Jest

## Fixed Versioning
- All packages share same version
- Lerna --fixed mode
- Example: Angular packages
```

**微服务策略**：
```markdown
## Service-Level Versioning
- Each service has own semantic version
- API contract versioning separate
- Rolling releases (deploy services independently)

## Coordinated Major Releases
- Independent minor/patch versions
- Coordinated major versions (breaking changes)
- Example: v2.x (service-a v2.3.0, service-b v2.1.0)
```

### 4. 发布候选版本（RC）管理

**RC 发布模式**：

**预发布标签**：
- `v1.0.0-rc.1` → `v1.0.0`（最终版本）
- `v2.0.0-beta.1` → `v2.0.0-rc.1` → `v2.0.0`
- `v3.0.0-alpha.1` → `v3.0.0-beta.1` → `v3.0.0-rc.1` → `v3.0.0`

**基于渠道的发布**：
- 稳定版（生产环境）
- 测试版（预发布阶段）
- 预览版（早期采用者）
- 金丝雀版（仅接收 1% 的流量，启用特性开关）

**基于环境的发布**：
- 开发环境 → 测试环境（RC） → 生产环境（最终版本）
- 特性分支 → RC 分支 → 主分支

**RC 发布流程**：
1. 创建 RC 版本（例如 `v1.0.0-rc.1`）
2. 部署到测试/测试渠道
3. 进行测试和修复错误（创建 rc.2、rc.3 等）
4. 验证完成后，将 RC 版本升级为最终版本 `v1.0.0`
5. 部署到生产环境

### 5. 动态文档编制

**生成 `release-strategy.md` 文件**：
- **跨项目适用**：适用于整个系统
  ```
.specweave/docs/internal/delivery/release-strategy.md
```

- **项目特定**：适用于多个项目的情况
  ```
.specweave/docs/internal/projects/{project-id}/delivery/release-strategy.md
```

**文档结构**：
```markdown
# Release Strategy: {Product/Project Name}

## Current Strategy
- Type: Single-repo / Multi-repo / Monorepo / Microservices
- Versioning: Semantic / Date-based / Custom
- Alignment: Lockstep / Independent / Umbrella
- RC Process: Pre-release tags / Channels / Feature flags

## Repositories
- Repo A: {purpose, current version, release frequency}
- Repo B: {purpose, current version, release frequency}

## Version Alignment
- Major: Coordinated (breaking changes)
- Minor: Independent (new features)
- Patch: Independent (bug fixes)

## Release Candidate Workflow
1. Create RC tag: v1.0.0-rc.1
2. Deploy to staging
3. Testing phase (1 week)
4. Promote to production: v1.0.0

## CI/CD Integration
- GitHub Actions: .github/workflows/release.yml
- Automated: npm publish, Docker push, Deploy to K8s
- Manual gates: QA approval, stakeholder sign-off

## Changelog Management
- Tool: Conventional Changelog / Keep a Changelog
- Format: CHANGELOG.md (root or per-package)
- Automation: semantic-release / standard-version

## Hotfix Strategy
- Branch: hotfix/* from production tag
- Version: Patch bump (v1.0.1)
- Process: Fast-track testing, immediate deploy

## Release Checklist
- [ ] All tests passing
- [ ] Changelog updated
- [ ] Version bumped
- [ ] Git tag created
- [ ] GitHub release published
- [ ] Package published (NPM/PyPI/Docker)
- [ ] Deployment successful
- [ ] Documentation updated

## Metrics & Monitoring
- DORA Metrics: Deployment frequency, lead time, MTTR, change failure rate
- Release cadence: {weekly / bi-weekly / monthly}
- Hotfix frequency: {target <5% of releases}

## Decision History
- 2025-01-15: Adopted umbrella versioning (ADR-023)
- 2025-02-01: Introduced RC workflow (ADR-025)
- 2025-03-10: Migrated to semantic-release (ADR-028)
```

### 6. 与旧代码库分析工具的集成

**旧代码库分析工具运行时自动检测策略**：
```bash
# Brownfield analyzer detects:
# 1. Repository structure (single/multi/monorepo)
# 2. Existing version tags
# 3. CI/CD configurations
# 4. Package manager configs
# 5. Release automation tools

# Then invokes release-strategy-advisor:
# - Analyze detected patterns
# - Classify release strategy
# - Document findings in release-strategy.md
# - Suggest improvements if needed
```

**检测输出示例**：
```markdown
## Detected Release Strategy

**Type**: Multi-repo Independent Releases

**Evidence**:
- 3 repositories detected:
  - frontend: v2.5.0 (last release: 2025-01-10)
  - backend: v1.8.0 (last release: 2025-01-08)
  - shared: v1.2.0 (last release: 2024-12-15)

- Version alignment: None (independent)
- Release frequency: Weekly (frontend), Bi-weekly (backend), Monthly (shared)
- CI/CD: GitHub Actions with semantic-release
- Changelog: Conventional Changelog (auto-generated)

**Recommendations**:
1. Consider umbrella versioning for product releases
2. Add RC workflow for major versions
3. Align major versions for better API compatibility
```

## 适用场景

**请咨询我以下问题**：

1. **分析现有发布策略**：
   - “我们的当前发布策略是什么？”
   - “检测我们的版本控制模式”
   - “分析我们在各个代码库中的发布方式”

2. **建议最佳策略**：
   - “我们应该采用哪种发布策略？”
   - “我们的微服务应该如何进行版本控制？”
   - “我们应该采用协调发布还是独立发布？”

3. **创建发布文档**：
   - “记录我们的发布流程”
   - “生成 `release-strategy.md` 文件”
   - “明确我们的版本控制方法”

4. **规划多代码库的发布**：
   - “如何协调 5 个代码库的发布？”
   - “我们应该对齐版本吗？”
   “最适合我们的 RC 发布流程是什么？”

5. **与旧代码库分析工具的集成**：
   - “了解我们现有的发布流程”
   **我们使用哪些发布工具？**
   **将当前的部署流程与分析工具进行映射**

## 最佳实践

**版本对齐**：
- 对于紧密耦合的服务，使用同步发布策略（共享重大变更）
- 对于耦合度低的服务，使用独立发布策略（团队自主决策）
- 对于包含多个独立模块的产品，使用总体版本控制策略

**RC 发布流程**：
- 对于重大版本（涉及重大变更），始终使用 RC 发布流程
- 如果有关键特性，也可以为次要版本使用 RC 发布流程
- 除非风险较高，否则对于修复性更新（hotfix），可以跳过 RC 发布流程

**变更日志管理**：
- 自动生成变更日志（遵循传统提交规范）
- 对于重大版本，手动整理变更日志并突出关键特性
- 链接到 GitHub 问题/拉取请求（PR）以便追踪

**发布频率**：
- 高风险变更：RC → 测试环境 → 生产环境（1-2 周）
- 低风险变更：直接发布到生产环境（每日/每周）
- 在速度和稳定性之间取得平衡（遵循 DORA 指标）

## 集成点

**旧代码库分析工具**：
- 自动检测现有发布模式
- 将数据提供给发布策略顾问
- 生成基础文档

**动态文档**：
- 将策略存储在 `delivery/` 目录中
- 随着策略的变更进行更新
- 提供决策所需的文档链接

**多项目环境**：
- 每个项目采用不同的发布策略
- 实现跨项目的发布协调
- 共享发布模板

**增量发布周期**：
- 发布增量覆盖多个代码库
- 协调规划与执行
- 自动更新动态文档

## 示例工作流程

### 单代码库项目（SpecWeave）
```bash
# 1. User asks for release strategy
"What release strategy should SpecWeave use?"

# 2. Advisor analyzes:
# - Single repo (GitHub: anton-abyzov/specweave)
# - NPM package
# - GitHub Actions for releases
# - Existing semver tags

# 3. Recommends:
# - Simple semver strategy
# - Automated releases via GitHub Actions
# - CHANGELOG.md maintenance
# - RC for major versions only

# 4. Creates:
# .specweave/docs/internal/delivery/release-strategy.md
```

### 多代码库微服务
```bash
# 1. User asks for strategy
"How should we release our 5 microservices?"

# 2. Advisor analyzes:
# - 5 repos detected (user-service, order-service, ...)
# - Tight coupling (shared API contracts)
# - High deployment frequency (daily)

# 3. Recommends:
# - Umbrella versioning (product v1.0.0)
# - Independent service versions (service-a v2.3.0)
# - RC workflow for product major versions
# - Rolling releases for services

# 4. Creates:
# .specweave/docs/internal/delivery/release-strategy.md
# - Umbrella version matrix
# - Service version independence
# - RC workflow for product releases
```

### 单代码库（Lerna/Nx）
```bash
# 1. User asks for strategy
"How to version our Lerna monorepo?"

# 2. Advisor analyzes:
# - Monorepo with 12 packages
# - Lerna detected (lerna.json)
# - Changesets for versioning
# - Independent package releases

# 3. Recommends:
# - Independent versioning (Lerna independent mode)
# - Changesets for semantic release
# - Automated changelogs per package
# - Fixed versioning for core packages

# 4. Creates:
# .specweave/docs/internal/delivery/release-strategy.md
# - Lerna configuration explanation
# - Changesets workflow
# - Package grouping strategy
```

## 命令集成

支持以下发布管理命令：
- `/sw-release:init` - 分析并推荐发布策略
- `/sw-release:align` - 协调各个代码库的版本
- `/sw-release:rc` - 创建发布候选版本
- `/sw-release:publish` - 执行发布操作

**依赖项**

**必需依赖**：
- Git（用于版本标签分析）
- SpecWeave 核心组件（用于动态文档集成）

**可选依赖（用于检测）**：
- GitHub CLI（`gh`）- 用于检测 GitHub 仓库的发布信息
- NPM（`npm`）- 用于检测 NPM 包
- Python（`python`）- 用于检测 Python 包
- Lerna（`lerna`）- 用于检测单代码库项目
- Nx（`nx`）- 用于检测 Nx 工作区配置

**输出结果**

- 生成/更新以下文件：
- `.specweave/docs/internal/delivery/release-strategy.md`（跨项目通用文档）
- `.specweave/docs/internal/projects/{id}/delivery/release-strategy.md`（项目特定文档）

**提供内容**：
- 当前策略分析结果
- 建议的改进措施
- RC 发布流程模板
- CI/CD 集成指南
- 版本对齐矩阵
- 发布检查清单

---

**请记住**：发布策略是一个动态更新的文档。在以下情况下需要更新它：
- 项目架构发生变化（新增代码库、新服务）
- 团队规模发生变化
- 部署频率发生变化
- 使用的工具发生变化（新的 CI/CD 工具、单代码库工具）
- 从发布过程中获得的经验教训

**目标**：建立一个清晰、有文档记录且可重复的发布流程，以适应团队和产品的不断发展。