---
name: afrexai-devops-engine
description: 完整的 DevOps 与平台工程系统：包括持续集成/持续交付（CI/CD）管道、基础设施即代码（Infrastructure as Code）管理、容器编排（Container Orchestration）机制、可观测性（Observability）工具、事件响应（Incident Response）流程，以及站点可靠性工程（Site Reliability Engineering, SRE）最佳实践——适用于所有平台和所有云环境。
metadata: {"clawdbot":{"emoji":"🔧","os":["linux","darwin","win32"]}}
---
# DevOps与平台工程引擎

这是一个完整的系统，用于构建、部署、运营和监控生产环境中的软件。它涵盖了整个DevOps生命周期——不仅仅是持续集成/持续部署（CI/CD），也不仅仅局限于单一云平台。

## 第一阶段：仓库与分支策略

### Git Flow决策矩阵

| 团队规模 | 发布频率 | 策略 | 分支结构 |
|-----------|----------------|----------|----------|
| 1-3人 | 持续集成 | 基于主分支（Trunk-based） | main + 短期功能分支 |
| 4-15人 | 每周/双周 | GitHub Flow | main + 功能分支 + 提交请求（PR） |
| 15人以上 | 定期发布 | Git Flow | main + 开发分支 + 功能分支 + 发布分支 + 紧急修复分支 |
| 受监管的团队 | 经过审核的发布 | Git Flow + 标签（tags） | 上述分支结构 + 签名的标签 + 审计追踪 |

### 分支保护规则（请遵循这些规则）

```yaml
# branch-protection.yml — document your rules
main:
  required_reviews: 2
  dismiss_stale_reviews: true
  require_codeowners: true
  require_status_checks:
    - ci/test
    - ci/lint
    - ci/security
  require_linear_history: true  # No merge commits
  restrict_pushes: true         # Only via PR
  require_signed_commits: false # Enable for regulated

develop:
  required_reviews: 1
  require_status_checks:
    - ci/test
```

### 提交规范

格式：`<类型>(<范围>): <描述>`

类型示例：`feat`（新增功能）、`fix`（修复问题）、`docs`（文档更新）、`style`（代码风格调整）、`refactor`（代码重构）、`perf`（性能优化）、`test`（测试）、`build`（构建）、`ci`（持续集成相关）、`chore`（杂务）

重要提示：涉及重大变更的提交需使用`feat!: remove legacy API`作为前缀，或添加`BREAKING CHANGE: 描述变更内容`的注释。通过`commitlint`和`husky`（Node.js插件）或预提交钩子来强制执行这些规范。

## 第二阶段：CI/CD管道架构

### 管道设计原则

1. **一次构建，到处部署**——相同的构建产物应用于开发、测试和生产环境。
2. **快速失败检测**——优先执行成本最低的检查步骤（代码格式检查、单元测试、集成测试、端到端测试）。
3. **封闭式构建**——构建过程中不依赖外部状态，且可以从提交哈希值（commit SHA）重现构建过程。
4. **构建产物不可修改**——构建完成后不允许修改；使用Git哈希值进行标记。
5. **并行处理独立阶段**——同时执行测试、代码格式检查和安全扫描等步骤。

### 通用管道模板

```yaml
# pipeline-stages.yml — adapt to your CI system
stages:
  # Stage 1: Quality Gate (parallel, <2 min)
  lint:
    run: lint
    parallel: true
    timeout: 2m
  typecheck:
    run: tsc --noEmit
    parallel: true
    timeout: 2m
  security_scan:
    run: trivy, snyk, or semgrep
    parallel: true
    timeout: 3m

  # Stage 2: Test (parallel by type, <10 min)
  unit_tests:
    run: test --unit
    parallel: true
    coverage_threshold: 80%
    timeout: 5m
  integration_tests:
    run: test --integration
    parallel: true
    needs: [database_service]
    timeout: 10m

  # Stage 3: Build (<5 min)
  build:
    needs: [lint, typecheck, unit_tests]
    outputs: [docker_image, release_artifact]
    tag: "${GIT_SHA}"
    cache: [node_modules, .next/cache, target/]

  # Stage 4: Deploy Staging (auto)
  deploy_staging:
    needs: [build]
    environment: staging
    strategy: rolling
    smoke_test: true
    auto: true

  # Stage 5: E2E on Staging (<15 min)
  e2e_tests:
    needs: [deploy_staging]
    timeout: 15m
    retry: 1
    artifacts: [screenshots, videos]

  # Stage 6: Deploy Production (manual gate or auto)
  deploy_prod:
    needs: [e2e_tests]
    environment: production
    strategy: canary  # or blue-green
    approval: required  # manual gate
    rollback_on_failure: true
    monitoring_window: 15m
```

### CI平台快速参考

| 功能 | GitHub Actions | GitLab CI | CircleCI | Jenkins |
|---------|---------------|-----------|----------|---------|
| 配置文件 | `.github/workflows/*.yml` | `.gitlab-ci.yml` | `.circleci/config.yml` | `Jenkinsfile` |
| 并行性 | `jobs.<id>`（自动设置） | `stages` + `parallel` | `workflows` | `parallel`步骤 |
| 缓存策略 | `actions/cache` | `cache:`键 | `save_cache/restore_cache` | Stash/unstash` |
| 机密管理 | 设置 → 机密管理功能 | 设置 → CI/CD → 变量管理 | 项目设置 → 环境变量 | 凭据管理插件 |
| 多环境部署 | `strategy.matrix` | `parallel:matrix` | `workflows`中的`matrix`配置 | 管道中的`matrix`设置 |
| 自托管环境 | `runs-on: self-hosted` | GitLab Runner | `resource_class` | 默认配置 |
| 使用OIDC/无密钥认证 | `permissions: id-token: write` | `id_tokens:` | OIDC认证机制 |
| 缓存策略 | **具体实现方式请参考相应平台文档** |

### GitHub Actions特定模式

```yaml
# Reusable workflow (DRY across repos)
# .github/workflows/reusable-deploy.yml
on:
  workflow_call:
    inputs:
      environment:
        required: true
        type: string
    secrets:
      DEPLOY_KEY:
        required: true

# Caller workflow
jobs:
  deploy:
    uses: ./.github/workflows/reusable-deploy.yml
    with:
      environment: production
    secrets: inherit
```

### GitHub Actions其他相关内容

```yaml
# Path-based triggers (monorepo)
on:
  push:
    paths:
      - 'packages/api/**'
      - 'shared/**'
  # Skip CI for docs-only changes
  pull_request:
    paths-ignore:
      - '**.md'
      - 'docs/**'
```

### GitHub Actions其他相关内容

## 第三阶段：容器化策略

### Dockerfile最佳实践

```dockerfile
# Multi-stage build template
# Stage 1: Build
FROM node:20-alpine AS builder
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --production=false    # Install all deps for build
COPY . .
RUN npm run build

# Stage 2: Production
FROM node:20-alpine AS production
RUN addgroup -g 1001 app && adduser -u 1001 -G app -s /bin/sh -D app
WORKDIR /app
COPY --from=builder --chown=app:app /app/dist ./dist
COPY --from=builder --chown=app:app /app/node_modules ./node_modules
COPY --from=builder --chown=app:app /app/package.json ./

USER app
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD wget -qO- http://localhost:3000/health || exit 1
CMD ["node", "dist/index.js"]
```

### 图像大小优化建议

- 使用alpine或distroless基础镜像。
- 采用多阶段构建方式（将依赖项打包到单独的镜像中）。
- 使用`.dockerignore`文件排除不必要的文件（如`.git`、`node_modules`、`.md`文件以及测试和文档文件）。
- 合并多个`RUN`命令以减少镜像层数。
- 在构建过程中清理包管理器的缓存（例如：`rm -rf /var/cache/apk/*`）。
- 确保生产环境不包含开发阶段的依赖项。
- 固定基础镜像的哈希值（例如：`FROM node:20-alpine@sha256:abc123...`）。

### 容器安全扫描

```bash
# Trivy (recommended — free, fast)
trivy image myapp:latest --severity HIGH,CRITICAL
trivy fs . --security-checks vuln,secret,config

# Scan in CI before push
# Fail pipeline if CRITICAL vulnerabilities found
trivy image --exit-code 1 --severity CRITICAL myapp:${GIT_SHA}
```

### 本地开发环境下的Docker Compose配置

```yaml
# docker-compose.yml — local development stack
services:
  app:
    build:
      context: .
      target: builder  # Use build stage for hot reload
    volumes:
      - .:/app
      - /app/node_modules  # Don't override node_modules
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=postgres://user:pass@db:5432/app
      - REDIS_URL=redis://cache:6379
    depends_on:
      db:
        condition: service_healthy

  db:
    image: postgres:16-alpine
    volumes:
      - pgdata:/var/lib/postgresql/data
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: app
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user"]
      interval: 5s
      timeout: 3s
      retries: 5

  cache:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  pgdata:
```

## 第四阶段：基础设施即代码（Infrastructure as Code, IaC）

### IaC工具选择矩阵

| 工具 | 适用场景 | 数据存储方式 | 编程语言 | 学习曲线 |
|------|----------|-------|----------|----------------|
| Terraform/OpenTofu | 多云环境，与云平台无关 | 使用远程存储（如S3、GCS） | HCL（Terraform配置语言） | 中等难度 |
| Pulumi | 适合喜欢编写实际代码的开发者 | 使用远程存储 | 使用 TypeScript/Python/Go语言 | 学习难度较低（如果自己编写配置脚本的话） |
| AWS CDK | 仅适用于AWS环境 | 使用CloudFormation | 使用 TypeScript/Python语言 | 中等难度 |
| Ansible | 用于配置管理和服务器设置 | 无状态存储 | 使用YAML语言 | 学习难度较低 |
| Helm | 用于Kubernetes部署 | 支持Tiller/OCI（Kubernetes操作框架） | 使用YAML和Go模板 | 中等难度 |

### Terraform项目结构建议

```
infrastructure/
├── modules/                    # Reusable components
│   ├── vpc/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── ecs-service/
│   └── rds/
├── environments/
│   ├── dev/
│   │   ├── main.tf            # Calls modules with dev params
│   │   ├── terraform.tfvars
│   │   └── backend.tf         # Dev state bucket
│   ├── staging/
│   └── prod/
├── .terraform-version          # Pin terraform version
└── .tflint.hcl
```

### Terraform安全使用规则

1. **始终在应用更改前进行规划**——仔细审查每个变更。
2. **使用锁定机制管理远程状态数据**——例如使用S3和DynamoDB或GCS，并设置锁定机制。
3. **不要将敏感信息（如数据库密码）存储在Git仓库中**。
4. **在管理资源之前先导入现有资源**——避免重复创建资源。
5. **对关键资源（如数据库、S3存储桶）使用`prevent_destroy`选项进行保护**。
6. **为所有资源添加标签**——例如`environment`、`team`、`cost-center`、`managed-by: terraform`等。
7. 在CI过程中使用`terraform fmt`工具保持配置格式的一致性。

### 环境发布流程建议

```
                    ┌──────────────────┐
  terraform plan ──►│  Review in PR    │
                    └────────┬─────────┘
                             │ merge
                    ┌────────▼─────────┐
  auto-apply ──────►│  Dev             │──► smoke tests
                    └────────┬─────────┘
                             │ promote
                    ┌────────▼─────────┐
  manual approve ──►│  Staging         │──► integration tests
                    └────────┬─────────┘
                             │ promote (manual gate)
                    ┌────────▼─────────┐
  manual approve ──►│  Production      │──► monitoring window
                    └──────────────────┘
```

## 第五阶段：Kubernetes操作

### Kubernetes资源模板

```yaml
# deployment.yml — production-ready template
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
  labels:
    app: myapp
    version: "1.0.0"
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0    # Zero-downtime
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
      containers:
        - name: myapp
          image: myregistry/myapp:abc123  # Git SHA tag
          ports:
            - containerPort: 3000
          resources:
            requests:
              cpu: 100m
              memory: 128Mi
            limits:
              cpu: 500m
              memory: 512Mi
          livenessProbe:
            httpGet:
              path: /health
              port: 3000
            initialDelaySeconds: 10
            periodSeconds: 10
            failureThreshold: 3
          readinessProbe:
            httpGet:
              path: /ready
              port: 3000
            initialDelaySeconds: 5
            periodSeconds: 5
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: myapp-secrets
                  key: database-url
      topologySpreadConstraints:
        - maxSkew: 1
          topologyKey: topology.kubernetes.io/zone
          whenUnsatisfiable: DoNotSchedule
```

### Helm图表配置建议

- 在`values.yaml`文件中设置合理的默认值（以便快速配置）。
- 明确资源请求和限制。
- 定义健康检查/就绪检查机制。
- 设置PodDisruptionBudget参数（例如`minAvailable: 1`表示允许1%的故障率，`maxUnavailable: 25%`表示允许25%的故障率）。
- 配置网络策略（例如`deny all`表示拒绝所有流量，`allow specific`表示仅允许特定流量）。
- 使用`ServiceAccount`进行身份验证（非默认设置）。
- 通过`external-secrets-operator`或`sealed-secrets`机制管理机密信息。
- 在CI过程中使用`helm lint`和`helm template`进行代码检查。
- 在`NOTES.txt`文件中记录部署后的操作指南。

### kubectl基本操作指南

```bash
# Debugging
kubectl get pods -l app=myapp -o wide          # Pod status + node
kubectl describe pod <pod>                      # Events, conditions
kubectl logs <pod> --tail=100 -f               # Stream logs
kubectl logs <pod> --previous                   # Crashed container logs
kubectl exec -it <pod> -- /bin/sh              # Shell into pod
kubectl top pods -l app=myapp                  # Resource usage

# Rollouts
kubectl rollout status deployment/myapp        # Watch rollout
kubectl rollout history deployment/myapp       # Revision history
kubectl rollout undo deployment/myapp          # Rollback to previous
kubectl rollout undo deployment/myapp --to-revision=3  # Specific

# Scaling
kubectl scale deployment/myapp --replicas=5    # Manual scale
kubectl autoscale deployment/myapp --min=3 --max=10 --cpu-percent=70

# Context management
kubectl config get-contexts                     # List clusters
kubectl config use-context prod-cluster         # Switch
kubectl config set-context --current --namespace=myapp  # Set namespace
```

## 第六阶段：部署策略

### 部署策略选择矩阵

| 部署策略 | 风险 | 部署速度 | 回滚能力 | 成本 | 适用场景 |
|----------|------|-------|----------|------|----------|
| 滚动部署（Rolling） | 风险较低 | 部署速度快 | 回滚速度较慢 | 适用于标准部署场景 |
| 蓝绿部署（Blue-Green） | 风险较低 | 部署速度快 | 可立即切换到新版本 | 适用于关键服务，要求零停机时间 |
| 瓜牛部署（Canary） | 风险极低 | 部署速度快 | 可立即切换到新版本 | 适用于高流量、风险较高的场景 |
| 特性开关（Feature Flag） | 风险极低 | 部署速度快 | 可立即切换 | 适用于逐步推广新特性或进行A/B测试 |
| 重新创建部署（Recreate） | 风险较高 | 部署速度快 | 回滚速度慢 | 适用于需要重建资源的场景（如状态化应用） |

### 瓜牛部署工作流程

当部署出现问题时：
1. **立即采取措施**：将流量从新版本路由到旧版本。
2. **如果使用滚动部署**：使用`kubectl rollout undo`命令撤销部署或重新部署之前的版本。
3. **检查**：数据库迁移是否向后兼容？
4. **验证**：回滚操作是否成功？检查错误率和系统性能。
5. **沟通**：在#incidents通道中报告问题，并更新状态页面。
6. **调查**：在找到根本原因之前不要重新部署。

### 数据库迁移安全注意事项

```
RULE: Migrations must be backward-compatible with the PREVIOUS version.
      (Because during rolling deploy, both versions run simultaneously)

Safe migration pattern:
  v1: Add new column (nullable, with default)
  v2: Backfill data, start writing to new column
  v3: Make new column required, stop writing old column
  v4: Drop old column (after v3 is fully deployed)

NEVER in one deploy:
  ❌ Rename column
  ❌ Change column type
  ❌ Drop column still read by current version
  ❌ Add NOT NULL without default
```

## 第七阶段：监控与可观测性

### 监控与可观测性工具组合

| 工具 | 功能 | 优先级 |
|--------|------|-------|
| **指标（Metrics）** | 随时间变化的数值数据 | Prometheus、Datadog、CloudWatch | 首选工具 |
| **日志（Logs）** | 事件记录 | ELK、Loki、CloudWatch Logs | 重要工具 |
| **追踪（Traces）** | 服务间的请求流程 | Jaeger、Tempo、X-Ray、Honeycomb | 高级工具 |
| **性能分析（Profiling）** | CPU/内存使用情况分析 | Pyroscope、Parca | 可选工具（针对性能优化需求） |

### 需要跟踪的关键指标

```yaml
# RED Method (request-driven services)
rate:     # Requests per second
errors:   # Failed requests per second
duration: # Latency distribution (p50, p95, p99)

# USE Method (infrastructure/resources)
utilization:  # % of resource in use (CPU, memory, disk)
saturation:   # Queue depth, pending work
errors:       # Resource errors (OOM, disk full)

# Business Metrics (most important!)
signups_per_hour:
checkout_completion_rate:
api_calls_by_customer:
revenue_per_minute:
```

### 警报规则设置建议

```yaml
# alerting-rules.yml
alerts:
  # Symptom-based (good — tells you users are impacted)
  - name: HighErrorRate
    condition: "error_rate_5xx > 1% for 5m"
    severity: critical
    runbook: docs/runbooks/high-error-rate.md
    notify: [pagerduty, slack-incidents]

  - name: HighLatency
    condition: "p99_latency > 2s for 5m"
    severity: warning
    runbook: docs/runbooks/high-latency.md
    notify: [slack-incidents]

  # Cause-based (supplementary — helps diagnose)
  - name: PodCrashLooping
    condition: "pod_restart_count increase > 3 in 10m"
    severity: warning
    notify: [slack-platform]

  - name: DiskSpaceWarning
    condition: "disk_usage > 80%"
    severity: warning
    notify: [slack-platform]

  - name: CertificateExpiring
    condition: "cert_expiry_days < 14"
    severity: warning
    notify: [slack-platform]

# Alert rules:
# 1. Every alert must have a runbook link
# 2. Every alert must be actionable (if you can't do anything, remove it)
# 3. Critical = wake someone up. Warning = check next business day.
# 4. Review alerts monthly — archive unused, tune noisy ones
```

### 结构化日志记录标准

**日志级别说明：**
- `error`：表示系统出现故障，需要立即处理。
- `warn`：表示出现意外情况，但系统已处理（例如重试成功或使用了备用方案）。
- `info`：表示业务相关事件（例如订单放置、用户注册、部署开始等）。
- `debug`：表示技术细节（例如查询执行结果、缓存命中/未命中等）——在生产环境中通常关闭这些日志。

### 仪表板设计建议

每个服务的仪表板都应包含必要的监控指标。

```
Row 1: Traffic Overview
  - Request rate (per endpoint)
  - Error rate (4xx, 5xx separate)
  - Active users / connections

Row 2: Performance
  - p50, p95, p99 latency
  - Throughput
  - Apdex score

Row 3: Resources
  - CPU utilization (per pod/instance)
  - Memory usage (vs limit)
  - Disk I/O / Network I/O

Row 4: Business
  - Revenue per minute (if applicable)
  - Conversion funnel
  - Queue depth / processing lag

Row 5: Dependencies
  - Database query latency + connection pool
  - External API latency + error rate
  - Cache hit rate
```

## 第八阶段：事件响应机制

### 事件严重程度分级

| 严重程度 | 定义 | 响应时间 | 示例 |
|-------|-----------|---------------|---------|
| SEV-1 | 服务完全中断，影响收入 | 15分钟 | 网站瘫痪，支付功能失效 |
| SEV-2 | 主要功能故障，但有临时解决方案 | 30分钟 | 搜索功能失效，页面加载缓慢 |
| SEV-3 | 较小功能故障，影响较小 | 4小时 | 管理面板出现错误，非关键API故障 |
| SEV-4 | 仅影响外观或用户体验 | 下一个开发周期处理 | 文本格式错误，UI界面有小问题 |

### 事件处理工作流程

```
1. DETECT (automated or reported)
   → Alert fires / user reports issue
   → Create incident channel: #inc-YYYY-MM-DD-description

2. TRIAGE (first 5 minutes)
   → Assign Incident Commander (IC)
   → Determine severity level
   → Post initial assessment in channel
   → Update status page (if customer-facing)

3. MITIGATE (focus on stopping the bleeding)
   → Can we rollback? → Do it
   → Can we scale up? → Do it
   → Can we feature-flag disable? → Do it
   → DON'T debug root cause yet — restore service first

4. RESOLVE
   → Confirm service restored (metrics, customer reports)
   → Communicate resolution to stakeholders
   → Update status page

5. POST-MORTEM (within 48 hours)
   → Blameless — focus on systems, not people
   → Timeline of events
   → Root cause analysis (5 Whys)
   → Action items with owners and deadlines
   → Share with team
```

### 事件事后分析模板

```markdown
# Incident Post-Mortem: [Title]

**Date:** YYYY-MM-DD
**Duration:** Xh Ym
**Severity:** SEV-X
**Incident Commander:** [name]
**Author:** [name]

## Summary
[1-2 sentence summary of what happened and impact]

## Impact
- Users affected: [number/percentage]
- Revenue impact: [if applicable]
- Duration: [start to full resolution]

## Timeline (all times UTC)
| Time | Event |
|------|-------|
| 14:00 | Deploy v2.3.1 begins |
| 14:05 | Error rate spikes to 15% |
| 14:07 | Alert fires, IC paged |
| 14:12 | Rollback initiated |
| 14:15 | Service restored |

## Root Cause
[Technical explanation — what actually broke and why]

## Contributing Factors
- [Factor 1 — e.g., migration not tested with production data volume]
- [Factor 2 — e.g., canary deployment not configured for this service]

## What Went Well
- [Fast detection — alert fired within 2 minutes]
- [Clear runbook — IC knew rollback procedure]

## What Went Wrong
- [No canary — went straight to 100% rollout]
- [Migration was not backward-compatible]

## Action Items
| Action | Owner | Due | Priority |
|--------|-------|-----|----------|
| Add canary to deployment | @engineer | YYYY-MM-DD | P1 |
| Add migration backward-compat check | @engineer | YYYY-MM-DD | P1 |
| Update runbook for this service | @sre | YYYY-MM-DD | P2 |

## Lessons Learned
[Key takeaways for the team]
```

### 紧急情况下的应对最佳实践

```yaml
on_call:
  rotation: weekly
  handoff: Monday 10:00 (overlap 1h with previous)
  escalation:
    - primary: respond within 15 min
    - secondary: auto-page if no ack in 15 min
    - manager: auto-page if no ack in 30 min

  expectations:
    - Laptop + internet within reach
    - Respond to page within 15 minutes
    - Follow runbook first, improvise second
    - Escalate early — "I don't know" is fine
    - Update incident channel every 15 min during active incident

  wellness:
    - No more than 1 week in 4 on-call
    - Comp time after major incidents
    - Toil budget: <30% of on-call time should be toil
    - Quarterly review: are we paging too much?
```

## 第九阶段：安全加固措施

### CI管道中的安全检查

```yaml
security_gates:
  # Pre-commit
  - tool: gitleaks / trufflehog
    what: Secret detection in code
    block: true

  # Build
  - tool: semgrep / CodeQL
    what: Static analysis (SAST)
    block: critical findings

  - tool: npm audit / pip audit / cargo audit
    what: Dependency vulnerabilities (SCA)
    block: critical/high

  # Container
  - tool: trivy / grype
    what: Image vulnerability scan
    block: critical

  - tool: hadolint
    what: Dockerfile best practices
    block: error level

  # Deploy
  - tool: checkov / tfsec
    what: IaC security scan
    block: high findings

  # Runtime
  - tool: falco / sysdig
    what: Runtime anomaly detection
    alert: true
```

### 机密信息管理策略

| 方法 | 安全性 | 复杂性 | 适用场景 |
|--------|----------|------------|----------|
| CI/CD过程中的环境变量管理 | 基础安全措施 | 适用于小型团队和非关键场景 |
| AWS Secrets Manager / GCP Secret Manager | 高级安全措施 | 适用于复杂环境或对安全性要求较高的场景 |
| HashiCorp Vault | 最高级安全措施 | 适用于多云环境或对合规性要求严格的应用 |
| SOPS + git | 良好的安全实践 | 适用于GitOps工作流程 |

**安全建议：**
- 至少每90天更新一次机密信息。
- 不同环境（开发环境、测试环境、生产环境）使用不同的机密信息。
- 审计所有对机密信息的访问行为。
- 在CI输出中隐藏机密信息。
- 尽可能使用OIDC/无密钥认证机制（避免使用长期有效的令牌）。

### 网络安全基本要求

```
1. Default deny all — explicitly allow what's needed
2. TLS everywhere — including internal service-to-service
3. No public IPs on internal services — use load balancers / API gateways
4. WAF on public endpoints — OWASP Top 10 rules minimum
5. Rate limiting on all APIs — prevent abuse and DDoS
6. DNS for service discovery — never hardcode IPs
7. VPN or zero-trust for admin access — no SSH from internet
8. Network policies in K8s — pods can't talk to everything
9. Egress control — services should only reach what they need
10. Certificate auto-renewal — cert-manager or ACM
```

## 第十阶段：运维最佳实践（SRE）

### SLO（Service Level Objective）框架

```yaml
# Define SLOs for every user-facing service
service: checkout-api
slos:
  availability:
    target: 99.95%        # 4.38 hours downtime/year
    window: 30d rolling
    measurement: "successful_requests / total_requests"

  latency:
    target: 99%           # 99% of requests under threshold
    threshold: 500ms      # p99 < 500ms
    window: 30d rolling

  freshness:
    target: 99.9%         # Data updated within SLA
    threshold: 5m
    window: 30d rolling

error_budget:
  monthly_budget: 0.05%   # ~21.6 minutes
  burn_rate_alert:
    fast: 14.4x           # Budget consumed in 1 hour → page
    slow: 3x              # Budget consumed in 10 hours → ticket
  policy:
    budget_exhausted:
      - freeze non-critical deploys
      - redirect eng effort to reliability
      - review in weekly SRE sync
```

### 降低运维工作量的方法

```
Toil = manual, repetitive, automatable, reactive, no lasting value

Track toil:
  - Log manual interventions for 2 weeks
  - Categorize: deployment, scaling, cert renewal, data fixes, permissions
  - Prioritize: frequency × time × frustration

Target: <30% of engineering time on toil
If toil > 50%: stop feature work, automate the top 3 toil items

Common toil automation:
  Manual deploys         → CI/CD pipeline
  Certificate renewal    → cert-manager / ACM
  Scaling up/down        → HPA / auto-scaling groups
  Permission requests    → Self-service IAM with approval
  Data fixes             → Admin API / scripts
  Dependency updates     → Renovate / Dependabot
  Flaky test management  → Auto-quarantine + ticket
```

### 容量规划建议

```yaml
capacity_review:
  frequency: monthly
  inputs:
    - current_utilization: "CPU, memory, disk, network per service"
    - growth_rate: "request rate trend over 90 days"
    - planned_events: "launches, marketing campaigns, seasonal peaks"
    - headroom_target: 30%  # Don't run above 70% sustained

  formula:
    needed_capacity: "current_usage × (1 + growth_rate) × (1 + headroom)"
    lead_time: "14 days for cloud, 60+ days for hardware"

  actions:
    - "If utilization > 70%: plan scaling within 2 weeks"
    - "If utilization > 85%: emergency scaling NOW"
    - "If utilization < 30%: rightsize down (save money)"
```

## 第十一阶段：成本优化

### 云服务成本管理

### 云服务成本管理规则

```
1. Right-size first — most instances are overprovisioned
   Check: actual CPU/memory usage vs provisioned (CloudWatch, Datadog)
   Action: downsize to next tier that maintains 70% headroom

2. Reserved capacity for baseline — spot/preemptible for burst
   Pattern: 60% reserved + 30% on-demand + 10% spot
   Savings: 40-70% on reserved vs on-demand

3. Auto-scale to zero when possible
   - Dev/staging environments: scale down nights + weekends
   - Serverless for bursty workloads (Lambda, Cloud Functions)

4. Delete zombie resources monthly
   - Unattached EBS volumes
   - Old snapshots (>90 days, not tagged for retention)
   - Unused load balancers
   - Orphaned Elastic IPs

5. Storage tiering
   - Hot: SSD (frequently accessed)
   - Warm: HDD (monthly access)
   - Cold: S3 Glacier / Archive (yearly access)
   - Auto-lifecycle policies on S3 buckets

6. Tag everything — untagged = untracked = wasted
   Required tags: environment, team, service, cost-center
   Weekly report: cost by tag, highlight untagged resources
```

### 月度成本审查模板

```markdown
## Cloud Cost Review — [Month YYYY]

### Summary
- Total spend: $X,XXX (vs budget: $X,XXX)
- MoM change: +X% ($XXX)
- Top 3 cost drivers: [service1, service2, service3]

### By Service
| Service | Cost | % of Total | MoM Change | Action |
|---------|------|-----------|------------|--------|
| EKS | $XXX | XX% | +X% | Right-size node group |
| RDS | $XXX | XX% | 0% | Consider reserved |
| S3 | $XXX | XX% | +X% | Add lifecycle rules |

### Optimization Actions Taken
- [Action 1]: Saved $XXX/mo
- [Action 2]: Saved $XXX/mo

### Next Month Actions
- [ ] [Action with estimated savings]
```

### DevOps成熟度评估

评估团队的DevOps成熟度（每个维度评分1-5分）：

| 维度 | 1（初步阶段） | 3（基本完善） | 5（高度优化） |
|--------|-----------|-------------|----------------|
| **CI/CD** | 手动部署 | 自动化管道，但需要人工审核 | 完全自动化部署，支持快速切换到新版本（<15分钟） |
| **基础设施即代码（IaC）** | 通过点击操作管理配置 | 部分使用Terraform，需要手动调整 | 100%自动化部署，具备自动恢复机制 |
| **监控** | 发生问题时才进行检查 | 通过仪表板和基本警报进行监控 | 设定服务水平目标（SLOs），具备自动恢复机制 |
| **事件响应** | 依赖紧急响应机制和SSH远程登录 | 有完善的事件处理流程和值班制度 | 进行事后分析，采用混沌工程（chaos engineering） |
| **安全性** | 定期进行安全审计 | 使用CI扫描工具和机密信息管理工具 | 采用预防性安全措施 |

**评分说明：**
- 6-12分：处于基础阶段，需要重点提升CI/CD和基本监控能力。
- 13-20分：正在发展中，需要引入基础设施即代码（IaC）和事件响应机制。
- 21-26分：已经较为成熟，具备SRE最佳实践和成本管理能力。
- 27-30分：处于高级阶段，注重混沌工程和提升开发者的工作体验。

### 常用命令示例

- “为我的Node.js项目设置CI/CD流程。”
- “为我的Python API创建一个Dockerfile。”
- “为使用RDS的ECS服务编写Terraform配置。”
- “为我的服务设计一个监控仪表板。”
- “帮我分析昨天的系统故障。”
- “评估我的Kubernetes部署是否具备生产环境所需的准备就绪状态。”
- “我应该选择哪种部署策略？”
- “帮我设置警报规则。”
- “为数据库故障制定事件响应流程。”
- “审计我的云服务成本并提出优化建议。”
- “评估我们的DevOps成熟度。”
- “为我们的CI管道配置机密信息管理机制。”