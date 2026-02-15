---
name: Forge
description: 这是一个自主的质量工程团队，它通过持续的行为验证、全面的端到端（E2E）测试以及自我修复的修复机制来生成可用于生产的代码。该团队将 DDD（领域驱动设计）+ ADR（需求驱动设计）+ TDD（测试驱动开发）方法论与 BDD（行为驱动开发）/ Gherkin 规范相结合，同时运用了七层质量检测机制、缺陷预测技术、混沌测试（chaos testing）以及跨上下文的依赖关系管理能力。该团队的架构具有通用性，能够适用于单体应用（monoliths）、微服务（microservices）、模块化单体应用（modular monoliths）以及任何具有明确边界和上下文的系统架构。
---

# Forge — 自主质量工程集群

**质量是内在生成的，而非事后附加的。**

Forge 是一个自我学习、自主运行的质量工程集群，它将三种方法整合为一体：

| 方法 | 来源 | 功能 |
|--------|--------|--------------|
| **构建** | DDD+ADR+TDD 方法论 | 结构化开发，包含质量检查点、缺陷预测和基于置信度的修复建议 |
| **验证** | BDD/Gherkin 行为规范 | 持续的行为验证——确保产品本身正常工作，而不仅仅是代码 |
| **修复** | 自主端到端修复循环 | 测试 → 分析 → 修复 → 提交 → 学习 → 重复 |

“完成”意味着：代码能够编译通过，并且产品的行为符合预期。所有的 Gherkin 场景都通过了验证，所有的质量检查点也都满足要求。

---

## 架构适应性

Forge 可以适应任何项目架构。在首次运行之前，它会自动发现项目的结构：

### 支持的架构

| 架构 | Forge 的适应方式 |
|-------------|-----------------|
| **单体应用** | 单一后端进程，所有代码都在一个代码库中。Forge 在一个服务器上运行所有测试。 |
| **模块化单体应用** | 单次部署，每个模块都有明确的边界。Forge 会独立发现并测试每个模块。 |
| **微服务** | 多个服务。Forge 会发现服务端点，并测试每个服务，验证服务间的契约。 |
| **单一仓库** | 多个应用程序/包位于一个仓库中。Forge 可以识别工作区的结构（如 Turborepo、Nx、Lerna、Melos、Cargo）。 |
| **前端 + 后端** | 前端应用与后端 API 相连接。Forge 会启动后端，然后针对后端运行端到端测试。 |
| **全栈单体应用** | 前端和后端在同一部署环境中。Forge 会通过 UI 层面直接测试后端。 |

### 项目发现

在首次调用时，Forge 会分析项目以构建上下文映射：

```bash
# Forge automatically discovers:
# 1. Backend technology (Rust/Cargo, Node/npm, Python/pip, Go, Java/Maven/Gradle, .NET)
# 2. Frontend technology (Flutter, React, Next.js, Vue, Angular, SwiftUI, Kotlin/Compose)
# 3. Test framework (integration_test, Jest, Pytest, Go test, JUnit, xUnit)
# 4. Project structure (monorepo layout, service boundaries, module boundaries)
# 5. API protocol (REST, GraphQL, gRPC, WebSocket)
# 6. Build system (Make, npm scripts, Gradle tasks, Cargo features)
```

Forge 会存储发现的项目结构信息：

```json
{
  "architecture": "mobile-backend",
  "backend": {
    "technology": "rust",
    "buildCommand": "cargo build --release --features test-endpoints",
    "runCommand": "cargo run --release --features test-endpoints",
    "healthEndpoint": "/health",
    "port": 8080,
    "migrationCommand": "cargo sqlx migrate run"
  },
  "frontend": {
    "technology": "flutter",
    "testCommand": "flutter drive --driver=test_driver/integration_test.dart --target={target}",
    "testDir": "integration_test/e2e/",
    "specDir": "integration_test/e2e/specs/"
  },
  "contexts": ["identity", "rides", "payments", "..."],
  "testDataSeeding": {
    "method": "api",
    "endpoint": "/api/v1/test/seed",
    "authHeader": "X-Test-Key"
  }
}
```

### 配置覆盖

项目可以在仓库根目录下提供 `forge.config.yaml` 文件来覆盖自动发现的结果：

```yaml
# forge.config.yaml (optional — Forge auto-discovers if absent)
architecture: microservices
backend:
  services:
    - name: auth-service
      port: 8081
      healthEndpoint: /health
      buildCommand: npm run build
      runCommand: npm start
    - name: payment-service
      port: 8082
      healthEndpoint: /health
      buildCommand: npm run build
      runCommand: npm start
frontend:
  technology: react
  testCommand: npx cypress run --spec {target}
  testDir: cypress/e2e/
  specDir: cypress/e2e/specs/
contexts:
  - name: identity
    testFile: auth.cy.ts
    specFile: identity.feature
  - name: payments
    testFile: payments.cy.ts
    specFile: payments.feature
dependencies:
  identity:
    blocks: [payments, orders]
  payments:
    depends_on: [identity]
    blocks: [orders]
```

---

## 重要规则：禁止使用模拟或存根

**绝对禁止：此工具严禁对后端 API 使用模拟或存根技术。**

- 所有测试都必须针对真实的后端 API 进行。
- 禁止使用任何模拟框架（如 `mockito`、`wiremock`、`MockClient`、`nock`、`msw`、`httpretty` 等）。
- 禁止使用伪造的 API 响应或数据。
- 在执行任何测试之前，后端必须处于运行状态且正常工作。
- 测试数据必须通过真实的 API 调用来生成。

**禁止使用模拟的原因：**
- 模拟会掩盖真实的集成问题。
- 模拟会带来虚假的信心。
- 模拟无法测试实际的数据流。
- 真实的 API 测试能够捕捉到序列化、验证和时序问题。

---

## 第 0 阶段：后端设置（必须首先完成）

**在任何测试开始之前，后端必须已经构建、编译并运行。**

这是该工具首先执行的步骤——没有任何例外。

### 第 1 步：检查并启动后端

```bash
# 1. Read project config or auto-discover backend settings
# 2. Check if backend is already running
curl -s http://localhost:${BACKEND_PORT}/${HEALTH_ENDPOINT} || {
  echo "Backend not running. Starting..."

  # 3. Navigate to backend directory
  cd ${BACKEND_DIR}

  # 4. Ensure environment is configured
  cp .env.example .env 2>/dev/null || true

  # 5. Build the backend
  ${BUILD_COMMAND}

  # 6. Run database migrations (if applicable)
  ${MIGRATION_COMMAND}

  # 7. Start backend (background)
  nohup ${RUN_COMMAND} > backend.log 2>&1 &
  echo $! > backend.pid

  # 8. Wait for backend to be healthy (up to 60 seconds)
  for i in {1..60}; do
    if curl -s http://localhost:${BACKEND_PORT}/${HEALTH_ENDPOINT} | grep -q "ok\|healthy\|UP"; then
      echo "Backend healthy on port ${BACKEND_PORT}"
      break
    fi
    sleep 1
  done
}
```

### 第 2 步：验证后端状态

```bash
# Verify critical endpoints are responding
curl -s http://localhost:${BACKEND_PORT}/${HEALTH_ENDPOINT} | jq .

# Verify test fixtures endpoint (for seeding)
curl -s -H "${TEST_AUTH_HEADER}" http://localhost:${BACKEND_PORT}/${TEST_STATUS_ENDPOINT} | jq .
```

### 第 3 步：契约验证

```bash
# Verify API spec matches running API (if OpenAPI/Swagger available)
curl -s http://localhost:${BACKEND_PORT}/${OPENAPI_ENDPOINT} > /tmp/live-spec.json

# Store contract snapshot for regression detection
npx @claude-flow/cli@latest memory store \
  --key "contract-snapshot-$(date +%s)" \
  --value "$(cat /tmp/live-spec.json | head -c 5000)" \
  --namespace forge-contracts
```

### 第 4 步：生成测试数据（通过真实 API 调用）

```bash
# Seed test data through REAL API — adapt to your project's seeding endpoint
curl -X POST http://localhost:${BACKEND_PORT}/${SEED_ENDPOINT} \
  -H "Content-Type: application/json" \
  -H "${TEST_AUTH_HEADER}" \
  -d '${SEED_PAYLOAD}'
```

---

## 第 1 阶段：行为规范与架构记录

**在测试之前，确保目标上下文有对应的 Gherkin 规范和架构决策记录。**

行为规范定义了产品从用户角度应该实现的功能。每个测试都对应一个 Gherkin 场景。如果测试通过了但规范未通过，说明产品存在问题。

### 规范的位置

Gherkin 规范与测试文件存储在同一位置：

```
${SPEC_DIR}/
├── [context-a].feature
├── [context-b].feature
├── [context-c].feature
└── ...
```

具体的存储位置取决于项目的测试结构。Forge 会自动从项目结构中识别这些文件的位置。

### 规范与测试的映射关系

每个 Gherkin 场景都对应一个测试函数。这种映射关系会被记录下来：

```gherkin
Feature: [Context Name]
  As a [user role]
  I want to [action]
  So that [outcome]

  Scenario: [Descriptive scenario name]
    Given [precondition]
    When [action]
    Then [expected result]
    And [additional verification]
```

### 规范缺失时的生成

如果某个上下文的规范缺失，规范验证器会自动生成：
1. 读取该上下文的屏幕/组件/路由实现文件。
2. 提取所有用户可见的功能、交互和状态。
3. 生成覆盖所有路径的 Gherkin 场景。
4. 将生成的规范文件保存到 `${SPEC_DIR}/[context].feature`。
5. 将每个场景映射到对应的测试函数。

### 优化后的 ADR 生成

当 Forge 发现某个没有架构决策记录的上下文时，规范验证器会自动生成相应的 ADR（架构决策文档）。ADR 采用专为机器处理的优化格式：

```markdown
# ADR-NNN: [Context] Architecture Decision

## Status
Proposed | Accepted | Deprecated | Superseded by ADR-XXX

## MUST
- [Explicit required behaviors with contract references]
- [Link to OpenAPI spec: /api/v1/[context]/openapi.json]
- [Required integration patterns]

## MUST NOT
- [Explicit forbidden patterns]
- [Anti-patterns to avoid]
- [Coupling violations]

## Verification
- Command: [command to verify this decision holds]
- Expected: [expected output or exit code]

## Dependencies
- Depends on: [list of upstream contexts with ADR links]
- Blocks: [list of downstream contexts with ADR links]
```

**ADR 的存储位置：**
- ADR 保存在 `docs/decisions/` 目录中，或项目配置的 ADR 目录中。
- 每个上下文只有一个 ADR。
- 当契约发生变化或发现新的依赖关系时，ADR 会更新。
- 规范验证器的工作流程中包含 ADR 的生成。

---

## 第 2 阶段：契约与依赖关系验证

### 契约验证

在运行测试之前，验证 API 响应格式是否与预期的数据传输对象（DTO）匹配：

```bash
# For each endpoint the context uses:
# 1. Make a real API call
# 2. Compare response structure against expected DTO/schema
# 3. Flag any mismatches as contract violations
```

如果契约验证失败，将被视为第 7 个质量检查点的失败，必须在功能测试之前解决这些问题。

### 共享类型的验证

对于具有共享依赖关系的上下文，验证类型的一致性：
1. **识别共享的 DTO/模型**：提取每个上下文中 API 请求和响应中使用的类型。
2. **跨上下文比较类型**：比较具有共享依赖关系的上下文之间的 DTO。
3. **标记类型不匹配**：例如，上下文 A 需要 `userId: string`，但上下文 B 发送 `userId: number`。
4. **验证值对象**：确保值对象（如电子邮件、货币、地址）在所有上下文中都遵循一致的模式。
5. **报告问题**：以预定义的文件位置和预期类型与实际类型进行对比，作为警告。

```json
{
  "sharedTypeViolation": {
    "type": "UserId",
    "contextA": { "name": "payments", "file": "types/payment.ts", "definition": "string" },
    "contextB": { "name": "orders", "file": "types/order.ts", "definition": "number" },
    "severity": "error"
  }
}
```

### 跨领域基础验证

验证所有上下文中的跨领域问题是否一致：
- **认证模式**：所有端点的认证格式（`Authorization: Bearer <token>`）和验证方式一致。
- **错误响应格式**：所有 API 端点返回的错误格式一致。
- **日志记录模式**：所有上下文的日志级别、格式和关联 ID 一致。
- **分页格式**：所有集合端点的分页参数和响应格式一致。

跨领域问题会在质量检查开始前作为警告报告。

### 依赖关系图

具有依赖关系的上下文之间可能存在依赖关系。当某个上下文的修复影响到其他上下文时，这些依赖上下文都需要重新测试。

```yaml
# Context Dependency Map — define in forge.config.yaml or auto-discover
# Example for a typical application:
#
# authentication:
#   depends_on: []
#   blocks: [orders, payments, profile, messaging]
#
# payments:
#   depends_on: [authentication]
#   blocks: [orders, subscriptions]
#
# orders:
#   depends_on: [authentication, payments]
#   blocks: [reviews, notifications]
```

### 级联重新测试

当 Bug Fixer 修改了某个上下文中的文件时：
1. 确定该文件属于哪个上下文。
2. 在 `blocks` 列表中查找与该上下文相关的所有上下文。
3. 在 X 的测试通过后，自动重新运行这些上下文的测试。
4. 如果出现级联失败，会追溯到最初的修复操作。

---

## 第 3 阶段：集群初始化

```bash
# Initialize anti-drift swarm for Forge
npx @claude-flow/cli@latest swarm init --topology hierarchical --max-agents 10 --strategy specialized

# Load previous fix patterns from memory
npx @claude-flow/cli@latest memory search --query "forge fix patterns" --namespace forge-patterns

# Check current coverage and gate status
npx @claude-flow/cli@latest memory retrieve --key "forge-coverage-status" --namespace forge-state

# Load confidence tiers
npx @claude-flow/cli@latest memory search --query "confidence tier" --namespace forge-patterns

# Check defect predictions for target context
npx @claude-flow/cli@latest memory search --query "defect prediction" --namespace forge-predictions
```

---

## 模型分配

Forge 会根据任务的复杂性将各个代理分配到相应的模型层级，以优化成本的同时不牺牲质量：

| 代理 | 模型 | 原因 |
|-------|-------|-----------|
| 规范验证器 | `sonnet` | 读取代码并生成 Gherkin 规范——中等复杂度的推理 |
| 测试运行器 | `haiku` | 结构化执行，输出解析——较低复杂度的推理 |
| 故障分析器 | `sonnet` | 根本原因分析——中等复杂度的推理 |
| 错误修复器 | `opus` | 基于第一性原理的代码修复——较高复杂度的推理 |
| 质量检查器 | `haiku` | 阈值比较——较低复杂度的推理 |
| 可访问性审计器 | `sonnet` | 代码分析 + WCAG 规则检查——中等复杂度的推理 |
| 自动提交器 | `haiku` | Git 操作，消息格式化——较低复杂度的推理 |
| 学习优化器 | `sonnet` | 模式分析，预测——中等复杂度的推理 |

项目可以通过 `forge.config.yaml` 文件覆盖这些模型分配：

```yaml
# forge.config.yaml — Model routing overrides (optional)
model_routing:
  spec-verifier: sonnet
  test-runner: haiku
  failure-analyzer: sonnet
  bug-fixer: opus
  gate-enforcer: haiku
  accessibility-auditor: sonnet
  auto-committer: haiku
  learning-optimizer: sonnet
```

如果没有指定覆盖配置，将使用默认设置。这种分配方式相比在最高层级模型上运行所有代理，可以减少大约 60% 的资源消耗。

---

## 第 4 阶段：自动启动代理

Claude Code 必须通过包含 `run_in_background: true` 的消息来启动这 8 个代理：

```javascript
// Agent 1: Specification Verifier
Task({
  model: "sonnet",
  prompt: `You are the Specification Verifier agent. Your mission:

    1. VERIFY backend is running: curl -sf http://localhost:${BACKEND_PORT}/${HEALTH_ENDPOINT}
    2. Check if Gherkin specs exist for the target bounded context:
       - Look in the project's spec directory
    3. If specs are MISSING:
       - Read the screen/component/route implementation files for the context
       - Extract all user-visible features, interactions, states
       - Generate Gherkin feature files with scenarios for every cyclomatic path
       - Write specs to the correct location
    4. If specs EXIST:
       - Read current implementations
       - Compare against existing scenarios
       - Flag scenarios that no longer match implementation (stale specs)
       - Generate new scenarios for uncovered features
    5. Create spec-to-test mapping:
       - Each Scenario name → test function name
       - Store mapping in memory for Test Runner
    6. Store results:
       npx @claude-flow/cli@latest memory store --key "specs-[context]-[timestamp]" \
         --value "[spec status JSON]" --namespace forge-specs

    CONSTRAINTS:
    - NEVER generate specs for code you haven't read
    - NEVER assume UI elements exist without checking implementation
    - NEVER create scenarios that duplicate existing coverage
    - NEVER modify existing test files — only spec files

    ACCEPTANCE:
    - Every implementation file has at least one Gherkin scenario
    - Spec-to-test mapping has zero unmapped entries
    - All generated scenarios follow Given/When/Then format
    - Results stored in forge-specs namespace

    Output: List of all Gherkin scenarios with their mapped test functions, and any gaps found.`,
  subagent_type: "researcher",
  description: "Spec Verification",
  run_in_background: true
})

// Agent 2: Test Runner
Task({
  model: "haiku",
  prompt: `You are the Test Runner agent. Your mission:

    1. VERIFY backend is running
    2. Check defect predictions from memory:
       npx @claude-flow/cli@latest memory search --query "defect prediction [context]" --namespace forge-predictions
       - Run predicted-to-fail tests FIRST for faster convergence
    3. Run the E2E test suite for the specified context using the project's test command
    4. Capture ALL test output including stack traces
    5. Parse failures into structured format:
       {testId, gherkinScenario, error, stackTrace, file, line, context}
    6. Map each failure to its Gherkin scenario (from spec-to-test mapping)
    7. Store results in memory for other agents:
       npx @claude-flow/cli@latest memory store \
         --key "test-run-[timestamp]" \
         --value "[parsed results JSON]" \
         --namespace forge-results

    CONSTRAINTS:
    - NEVER skip failing tests
    - NEVER modify test code or source code
    - NEVER mock API calls or stub responses
    - NEVER continue if backend health check fails

    ACCEPTANCE:
    - All test results stored in memory with structured format
    - Zero unparsed failures — every failure has testId, error, stackTrace, file, line
    - Predicted-to-fail tests executed first
    - Results include Gherkin scenario mapping for every test`,
  subagent_type: "tester",
  description: "Test Runner",
  run_in_background: true
})

// Agent 3: Failure Analyzer
Task({
  model: "sonnet",
  prompt: `You are the Failure Analyzer agent. Your mission:

    1. Monitor memory for new test results from Test Runner
    2. For each failure, analyze:
       - Root cause category: element-not-found, assertion-failed, timeout,
         api-mismatch, navigation-error, state-error, contract-violation
       - Affected file and line number
       - Which Gherkin scenario is violated
       - Impact on dependent contexts (check dependency graph)
    3. Search memory for matching fix patterns with confidence tiers:
       npx @claude-flow/cli@latest memory search \
         --query "[error pattern]" --namespace forge-patterns
    4. If pattern found with confidence >= 0.85 (Gold+):
       - Recommend auto-apply
       - Include pattern key and success rate
    5. If pattern found with confidence >= 0.75 (Silver):
       - Suggest fix but flag for review
    6. If no matching pattern:
       - Perform root cause analysis from first principles
       - Generate fix hypothesis
    7. Store analysis in memory for Bug Fixer:
       npx @claude-flow/cli@latest memory store \
         --key "analysis-[testId]-[timestamp]" \
         --value "[analysis JSON]" \
         --namespace forge-results

    CONSTRAINTS:
    - NEVER assume root cause without stack trace evidence
    - NEVER recommend fixes for passing tests
    - NEVER skip dependency graph impact analysis
    - NEVER override confidence tier thresholds

    ACCEPTANCE:
    - Every failure has a root cause category and affected file
    - Zero unanalyzed failures
    - Dependency impact documented for every failure
    - Pattern search executed for every error type`,
  subagent_type: "researcher",
  description: "Failure Analyzer",
  run_in_background: true
})

// Agent 4: Bug Fixer
Task({
  model: "opus",
  prompt: `You are the Bug Fixer agent. Your mission:

    1. Retrieve failure analysis from memory
    2. For each failure, apply fix using confidence-tiered approach:

       PLATINUM (>= 0.95 confidence):
       - Auto-apply the stored fix pattern immediately
       - No review needed

       GOLD (>= 0.85 confidence):
       - Auto-apply the stored fix pattern
       - Flag in commit message for awareness

       SILVER (>= 0.75 confidence):
       - Read the failing test file and source file
       - Apply suggested fix with extra verification
       - Run targeted test before proceeding

       BRONZE or NO PATTERN:
       - Read the failing test file
       - Read the source file causing the failure
       - Implement fix from first principles
       - Use defensive patterns appropriate to the test framework

    3. After fixing, identify affected context:
       - Check dependency graph for cascade impacts
       - Flag dependent contexts for re-testing

    4. Store the fix pattern with initial confidence:
       npx @claude-flow/cli@latest memory store \
         --key "fix-[error-type]-[hash]" \
         --value '{"pattern":"[fix]","confidence":0.75,"tier":"silver","applied":1,"successes":0}' \
         --namespace forge-patterns

    5. Signal Test Runner to re-run affected tests
    6. Signal Quality Gate Enforcer to check all 7 gates

    CONSTRAINTS:
    - NEVER change test assertions to make tests pass
    - NEVER modify Gherkin specs to match broken behavior
    - NEVER introduce new dependencies without flagging
    - NEVER apply fixes without reading both test file and source file

    ACCEPTANCE:
    - Every applied fix has a targeted test re-run result
    - Zero fixes without verification
    - Fix pattern stored with initial confidence score
    - Cascade impacts identified and flagged for re-testing`,
  subagent_type: "coder",
  description: "Bug Fixer",
  run_in_background: true
})

// Agent 5: Quality Gate Enforcer
Task({
  model: "haiku",
  prompt: `You are the Quality Gate Enforcer agent. Your mission:

    After each fix cycle, evaluate ALL 7 quality gates:

    GATE 1 — FUNCTIONAL (100% required):
    - All tests in the target context pass
    - No regressions in previously passing tests

    GATE 2 — BEHAVIORAL (100% of targeted scenarios):
    - Every Gherkin scenario that was targeted has a passing test
    - Spec-to-test mapping is complete (no unmapped scenarios)

    GATE 3 — COVERAGE (>=85% overall, >=95% critical paths):
    - Calculate path coverage for the context
    - Critical paths: authentication, payment, core workflows
    - Non-critical paths: preferences, history, settings

    GATE 4 — SECURITY (0 critical/high violations):
    - No hardcoded API keys, tokens, or secrets in test files
    - No hardcoded test credentials (use env vars or test fixtures)
    - Secure storage patterns used (no plaintext sensitive data)
    - No SQL injection vectors in dynamic queries
    - No XSS vectors in rendered output
    - No path traversal in file operations
    - Dependencies have no known critical CVEs (when lockfile available)
    - When AQE available: delegate to security-scanner for full SAST analysis

    GATE 5 — ACCESSIBILITY (WCAG AA):
    - All interactive elements have accessible labels
    - Touch/click targets meet minimum size requirements
    - Color contrast meets WCAG AA ratios
    - Screen reader navigation order is logical

    GATE 6 — RESILIENCE (tested for target context):
    - Offline/disconnected state handled gracefully
    - Timeout handling shows user-friendly message
    - Error states show retry option
    - Server errors show generic error, not stack trace

    GATE 7 — CONTRACT (0 mismatches):
    - API responses match expected schemas
    - No unexpected null fields
    - Enum values match expected set
    - Pagination format is consistent

    For each gate:
    - Status: PASS / FAIL / SKIP (with reason)
    - Details: what passed, what failed
    - Blocking: whether this gate blocks the commit

    Store gate results:
    npx @claude-flow/cli@latest memory store \
      --key "gates-[context]-[timestamp]" \
      --value "[gate results JSON]" \
      --namespace forge-state

    ONLY signal Auto-Committer when ALL 7 GATES PASS.

    CONSTRAINTS:
    - NEVER approve a commit with ANY blocking gate failure
    - NEVER lower thresholds below defined minimums
    - NEVER skip gate evaluation — all 7 gates must be assessed
    - NEVER mark a gate as PASS without evidence

    ACCEPTANCE:
    - Gate results stored in memory with PASS/FAIL/SKIP for all 7 gates
    - Every FAIL includes specific details of what failed
    - Every SKIP includes reason for skipping
    - Auto-Committer only signaled when all blocking gates pass`,
  subagent_type: "reviewer",
  description: "Quality Gate Enforcer",
  run_in_background: true
})

// Agent 6: Accessibility Auditor
Task({
  model: "sonnet",
  prompt: `You are the Accessibility Auditor agent. Your mission:

    1. For each screen/page/component in the target context, audit:

    LABELS:
    - Every interactive element has an accessible label/aria-label/Semantics label
    - Labels are descriptive (not "button1" but "Submit payment")
    - Images have alt text or semantic labels

    TOUCH/CLICK TARGETS:
    - All interactive elements meet minimum size (48x48dp mobile, 44x44px web)
    - Flag any undersized targets

    CONTRAST:
    - Text on colored backgrounds meets WCAG AA ratio (4.5:1 normal, 3:1 large)
    - Flag low-contrast combinations

    SCREEN READER:
    - Accessibility tree has logical reading order
    - No duplicate or misleading labels
    - Form fields have associated labels

    FOCUS/TAB ORDER:
    - Focus order follows visual layout
    - Focus trap in modals/dialogs
    - Focus returns to trigger after dialog closes

    2. Generate findings as:
       {severity: "critical"|"warning"|"info", element, file, line, issue, fix}

    3. Store audit results:
       npx @claude-flow/cli@latest memory store \
         --key "a11y-[context]-[timestamp]" \
         --value "[audit JSON]" \
         --namespace forge-state

    CONSTRAINTS:
    - NEVER skip interactive elements during audit
    - NEVER report false positives for decorative images
    - NEVER ignore focus/tab order analysis
    - NEVER apply fixes — only report findings for Bug Fixer

    ACCEPTANCE:
    - Every interactive element audited
    - Findings stored with severity, element, file, line, issue, fix
    - Zero unaudited interactive elements in target context
    - WCAG AA compliance level assessed for every screen`,
  subagent_type: "analyst",
  description: "Accessibility Auditor",
  run_in_background: true
})

// Agent 7: Auto-Committer
Task({
  model: "haiku",
  prompt: `You are the Auto-Committer agent. Your mission:

    1. Monitor for successful fixes where ALL 7 QUALITY GATES PASS
    2. For each successful fix:
       - Stage only the fixed files (never git add -A)
       - Create detailed commit message:

         fix(forge): Fix [TEST_ID] - [brief description]

         Behavioral Spec: [Gherkin scenario name]
         Root Cause: [what caused the failure]
         - [specific issue 1]
         - [specific issue 2]

         Fix Applied:
         - [change 1]
         - [change 2]

         Quality Gates:
         - Functional: PASS
         - Behavioral: PASS
         - Coverage: [X]%
         - Security: PASS
         - Accessibility: PASS
         - Resilience: PASS
         - Contract: PASS

         Confidence Tier: [platinum|gold|silver|bronze]
         Pattern Stored: fix-[error-type]-[hash]

       - Commit with the message above
    3. Update coverage report with new passing paths
    4. Store commit hash in memory for rollback capability:
       npx @claude-flow/cli@latest memory store \
         --key "commit-[hash]" \
         --value "[commit details JSON]" \
         --namespace forge-commits
    5. Store last known good commit:
       npx @claude-flow/cli@latest memory store \
         --key "last-green-commit" \
         --value "[hash]" \
         --namespace forge-state

    CONSTRAINTS:
    - NEVER use git add -A or git add .
    - NEVER commit without all 7 gates passing
    - NEVER amend previous commits
    - NEVER push to remote — only local commits

    ACCEPTANCE:
    - Commit message includes Behavioral Spec, Root Cause, Fix Applied, all 7 gate statuses
    - Only fixed files are staged (no unrelated files)
    - Commit hash stored in forge-commits namespace
    - Last green commit updated in forge-state namespace`,
  subagent_type: "reviewer",
  description: "Auto-Committer",
  run_in_background: true
})

// Agent 8: Learning Optimizer
Task({
  model: "sonnet",
  prompt: `You are the Learning Optimizer agent. Your mission:

    1. After each test cycle, analyze patterns:
       - Which error types fail most often?
       - Which fix patterns have highest success rate?
       - What new defensive patterns should be added?
       - Which Gherkin scenarios are most fragile?

    2. UPDATE CONFIDENCE TIERS:
       For each fix pattern applied this cycle:
       - If fix succeeded: confidence += 0.05 (cap at 1.0)
         - If confidence crosses 0.95: promote to Platinum
         - If confidence crosses 0.85: promote to Gold
       - If fix failed: confidence -= 0.10 (floor at 0.0)
         - If confidence drops below 0.70: demote to Bronze (learning-only)
       Store updated pattern:
       npx @claude-flow/cli@latest memory store \
         --key "fix-[error-type]-[hash]" \
         --value "[updated pattern JSON]" \
         --namespace forge-patterns

    3. DEFECT PREDICTION:
       Analyze which contexts/files are likely to fail next:
       - Files changed since last green run
       - Historical failure rate per context
       - Complexity of recent changes
       Store prediction:
       npx @claude-flow/cli@latest memory store \
         --key "prediction-[date]" \
         --value "[prediction JSON]" \
         --namespace forge-predictions

    4. Train neural patterns on successful fixes:
       npx @claude-flow/cli@latest hooks post-task \
         --task-id "forge-cycle" --success true --store-results true

    5. Update coverage status:
       npx @claude-flow/cli@latest memory store \
         --key "forge-coverage-status" \
         --value "[updated coverage JSON]" \
         --namespace forge-state

    6. Generate recommendations for test improvements
    7. Export learning metrics:
       npx @claude-flow/cli@latest neural train --pattern-type forge-fixes --epochs 5

    CONSTRAINTS:
    - NEVER promote a pattern that failed in the current cycle
    - NEVER delete patterns — only demote below Bronze threshold
    - NEVER override confidence scores without evidence from test results
    - NEVER generate predictions without historical data

    ACCEPTANCE:
    - All applied patterns have updated confidence scores
    - Prediction stored for next run with context-level probabilities
    - Coverage status updated in forge-state namespace
    - Zero patterns promoted without success evidence`,
  subagent_type: "researcher",
  description: "Learning Optimizer",
  run_in_background: true
})
```

---

## 第 5 阶段：质量检查

每次修复循环后，会评估 7 个质量检查点。所有检查点都必须通过才能创建提交。

| 检查点 | 检查内容 | 阈值 | 是否阻塞提交 |
|------|-------|-----------|----------|
| 1. 功能性 | 所有测试通过 | 100% 通过率 | 是 |
| 2. 行为 | 所有 Gherkin 场景满足 | 100% 的目标场景 | 是 |
| 3. 覆盖率 | 总覆盖率 >=85%，关键路径 >=95% | 是（仅针对关键路径） |
| 4. 安全性 | 无硬编码的秘密信息，安全存储，SAST 检查 | 无关键性错误 | 是 |
| 5. 可访问性 | 标签可读，目标尺寸合适，对比度符合 WCAG 标准 | 只显示警告 |
| 6. 弹性 | 支持离线操作，超时处理，错误状态 | 已针对目标上下文进行测试 | 只显示警告 |
| 7. 契约 | API 响应符合预期格式 | 无格式不匹配 | 是 |

### 检查点失败分类

当检查点失败时，会针对具体情况决定重新运行的策略：
- **功能性失败** → 重新运行对应的错误修复器。
- **行为失败** | 检查规范与测试的映射关系，可能需要新的测试。
- **覆盖率失败** | 生成额外的测试路径。
- **安全性失败** | 修改硬编码的值，更新存储方式。
- **可访问性失败** | 添加可访问性标签，调整目标尺寸。
- **弹性失败** | 添加离线/错误处理机制。
- **契约失败** | 更新 DTO 或标记 API 回归问题。

---

## 自主执行循环

```
┌────────────────────────────────────────────────────────────────────────┐
│                      FORGE AUTONOMOUS LOOP                             │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐        │
│  │ Specify  │───▶│   Test   │───▶│ Analyze  │───▶│   Fix    │        │
│  │ (Gherkin)│    │ (Run)    │    │ (Root    │    │ (Tiered) │        │
│  └──────────┘    └──────────┘    │  Cause)  │    └──────────┘        │
│       ▲                          └──────────┘         │               │
│       │                                               ▼               │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐        │
│  │  Learn   │◀───│  Commit  │◀───│  Gate    │◀───│  Audit   │        │
│  │ (Update  │    │ (Auto)   │    │ (7 Gates)│    │ (A11y)   │        │
│  │  Tiers)  │    └──────────┘    └──────────┘    └──────────┘        │
│  └──────────┘                                                         │
│       │                                                                │
│       └───────────────── REPEAT ──────────────────────────────────────│
│                                                                        │
│  Loop continues until: ALL 7 GATES PASS or MAX_ITERATIONS (10)        │
│  Gate failures are categorized for targeted re-runs (not full re-run) │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 实时进度报告

每个代理在执行过程中都会发送结构化的进度事件，以便监控：

```json
{"agent": "spec-verifier", "event": "spec_generated", "context": "payments", "scenarios": 12}
{"agent": "test-runner", "event": "test_started", "context": "payments", "test": "user_can_pay"}
{"agent": "test-runner", "event": "test_completed", "context": "payments", "passed": 10, "failed": 2}
{"agent": "failure-analyzer", "event": "root_cause_found", "test": "user_can_pay", "cause": "timeout"}
{"agent": "bug-fixer", "event": "fix_applied", "file": "payments.ts", "confidence": 0.92}
{"agent": "gate-enforcer", "event": "gate_evaluated", "gate": "functional", "status": "PASS"}
{"agent": "auto-committer", "event": "committed", "hash": "abc123", "tests_fixed": 2}
{"agent": "learning-optimizer", "event": "pattern_updated", "pattern": "fix-timeout-xyz", "tier": "gold"}
```

**进度文件：**
- 事件会被追加到 `.forge/progress.jsonl` 文件中（每行一个 JSON 对象）。
- 该文件在每次 Forge 运行开始时创建，并在运行结束后被截断。
- 可以通过 `tail -f .forge/progress.jsonl` 命令实时监控进度。

**与 Agentic QE UI 的集成：**
- 当 Agentic QE UI 协议可用时，事件会直接传输到用户界面。
- 用户可以实时看到进度：哪些检查点正在被评估，哪些测试正在运行，哪些修复操作正在执行。
- 在没有 Ag-UI 的情况下，可以通过代理的输出文件查看进度。

---

## 修复模式的置信度分级

每个修复模式都会被赋予一个置信度分数，这个分数会随时间变化：

```json
{
  "key": "fix-element-not-found-abc123",
  "pattern": {
    "error": "Element not found / No element",
    "fix": "Ensure element is rendered and visible before interaction",
    "files_affected": ["*_test.*"],
    "context": "any"
  },
  "tier": "gold",
  "confidence": 0.92,
  "auto_apply": true,
  "applied_count": 47,
  "success_count": 43,
  "success_rate": 0.915,
  "last_applied": "2026-02-06T14:30:00Z",
  "last_failed": "2026-02-01T09:15:00Z"
}
```

### 分级阈值

| 级别 | 置信度 | 是否自动应用 | 行为 |
|------|-----------|------------|----------|
| **铂金** | >= 0.95 | 是 | 立即应用，无需审核 |
| **黄金** | >= 0.85 | 是 | 应用并在提交信息中标记 |
| **白银** | >= 0.75 | 否 | 建议错误修复器处理，不自动应用 |
| **青铜** | >= 0.70 | 否 | 仅用于学习，不自动应用 |
| **过期** | < 0.70 | 否 | 模式降级，需要重新验证 |

### 置信度更新

每次应用后：
- **成功**：置信度增加 0.05（上限为 1.0）。
- **失败**：置信度减少 0.10（最低为 0.0）。
- **升级或降级**：当置信度超过或低于阈值时发生。

---

## 缺陷预测

在运行测试之前，学习优化器会分析历史数据来预测哪些测试最有可能失败：

### 输入信号

1. 自上次成功运行以来发生变化的文件（使用 git diff 与上次成功提交的差异）。
2. 每个上下文的历史失败率（来自 `forge-results` 命名空间）。
3. 修复模式的新鲜度——最近应用的修复更容易导致问题。
4. 复杂度指标——路径更复杂的上下文更容易失败。
5. 依赖关系链的长度——依赖关系更深的上下文失败率更高。

### 预测结果

```json
{
  "date": "2026-02-07",
  "predictions": [
    { "context": "payments", "probability": 0.73, "reason": "3 files changed in payment module" },
    { "context": "orders", "probability": 0.45, "reason": "depends on payments (changed)" },
    { "context": "identity", "probability": 0.12, "reason": "no changes, stable history" }
  ],
  "recommended_order": ["payments", "orders", "identity"]
}
```

测试会按照失败概率的降序执行——预测会失败的测试会优先执行，以便更快地收敛结果。

---

## 全面的边缘情况测试

### 通用 UI 元素的边缘情况测试
对于每个交互元素，测试以下内容：
1. **交互状态**：
   - 单次交互 → 预期的操作。
   - 快速重复交互 → 避免重复操作。
   - 长时间按压/右键点击 → 显示上下文菜单（如果适用）。
   - 禁用状态 → 不执行任何操作，显示视觉反馈。
2. **输入字段状态**：
   - 空输入 → 显示占位符。
   - 焦点聚焦 → 显示焦点指示器。
   - 输入有效 → 无错误提示。
   - 输入无效 → 显示错误消息。
   - 达到最大长度 → 阻止进一步输入。
   - 粘贴 → 验证粘贴的内容。
   - 清空 → 重置为空状态。
3. **异步操作状态**：
   - 加载前 → 显示加载指示器。
   | 加载中 → 显示加载指示器，禁用提交按钮。
   | 成功 → 显示数据，隐藏加载指示器。
   | 错误 → 显示错误消息，提供重试选项。
   | 超时 → 显示超时提示，提供重试选项。
4. **导航边缘情况**：
   | 向后导航 → 显示上一个页面或退出确认。
   | 深链接 → 显示正确的页面和参数。
   | 无效的深链接 → 显示错误页面。
   | 浏览器前进/后退 → 显示正确的状态。
5. **滚动边缘情况**：
   | 滚动到页面底部 → 显示适当的反馈。
   | 滚动到隐藏的内容 → 显示内容。
   | 键盘操作 → 显示相应的滚动效果。
6. **网络边缘情况**：
   | 无网络连接 → 显示离线提示，如果有缓存数据则使用缓存数据。
   | 连接缓慢 → 继续显示加载状态，处理超时。
   | 连接恢复 → 自动重试未完成的操作。
   | 服务器错误 500 → 显示通用错误消息。
   | 认证错误 401 → 重定向到登录页面。
   | 权限错误 403 → 显示“未找到”提示。
   | 未找到 404 → 显示“未找到”提示。
7. **混沌测试（弹性测试）**
   | 对于每个目标上下文，注入可控的错误：
     | **超时** → API 调用超过 10 秒 → 检查超时处理。
     | **部分响应** → API 返回不完整的数据 → 检查优雅的降级处理。
     | **速率限制** → API 返回 429 状态码 → 检查重试行为。
     | **并发修改** → 多个客户端同时修改同一资源 → 检查冲突处理。
8. **视觉回归测试**
   | 对于依赖大量交互的 UI 应用，Forge 会捕获并比较截图以检测意外的视觉变化：
     | **修复前** → 拍摄目标上下文中所有页面的基线截图。
     | **修复后** → 拍摄相同页面的新截图。
     | **比较** → 逐像素比较（默认容忍度为 0.1% 的差异）。
     | **报告** → 将视觉差异标记为第 5 个质量检查点的警告。
     | **存储** | 将截图差异保存在内存中以供后续分析。

**截图捕获方法：**
| 平台 | 方法 |
|----------|--------|
| Web (Playwright) | `page.screenshot({ fullPage: true })` |
| Web (Cypress) | `cy.screenshot()` |
| Flutter | `await tester.binding.setSurfaceSize(size); await expectLater(find.byType(App), matchesGoldenFile('name.png'))` |
| Mobile (native) | 根据平台特定的方法捕获截图 |

**配置：**
```yaml
# forge.config.yaml — Visual regression settings (optional)
visual_regression:
  enabled: true
  threshold: 0.001  # 0.1% pixel diff tolerance
  screenshot_dir: .forge/screenshots
  full_page: true
```

当 Agentic QE 可用时，可以委托给 `visual-tester` 代理来并行比较不同屏幕尺寸。

---

## 调用模式

```bash
# Full autonomous run — all contexts, all gates
/forge --autonomous --all

# Single context autonomous
/forge --autonomous --context [context-name]

# Behavioral verification only (no fixes)
/forge --verify-only
/forge --verify-only --context [context-name]

# Fix-only mode (fix failures, don't generate new tests)
/forge --fix-only --context [context-name]

# Learn mode (analyze patterns, update confidence tiers)
/forge --learn

# Add coverage for new screens/pages/components
/forge --add-coverage --screens [name1],[name2]

# Generate Gherkin specs for a context
/forge --spec-gen --context [context-name]
/forge --spec-gen --all

# Run quality gates without test execution
/forge --gates-only
/forge --gates-only --context [context-name]

# Defect prediction only
/forge --predict
/forge --predict --context [context-name]

# Chaos/resilience testing for a context
/forge --chaos --context [context-name]
/forge --chaos --all
```

---

## 内存命名空间

| 命名空间 | 用途 | 关键模式 |
|-----------|---------|-------------|
| `forge-patterns` | 带有置信度的修复模式 | `fix-[error-type]-[hash]` |
| `forge-results` | 测试运行结果 | `test-run-[timestamp]` |
| `forge-state` | 覆盖率和检查点状态 | `forge-coverage-status`, `gates-[context]-[ts]`, `last-green-commit` |
| `forge-commits` | 提交历史 | `commit-[hash]` |
| `forge-screens` | 实际执行的页面 | `screen-[name]` |
| `forge-specs` | Gherkin 规范 | `specs-[context]-[timestamp]` |
| `forge-contracts` | API 契约快照 | `contract-snapshot-[timestamp]` |
| `forge-predictions` | 缺陷预测历史 | `prediction-[date]` |

---

## 可选：与 Agentic QE 的集成

Forge 可以通过 MCP 与 [Agentic QE](https://github.com/proffesor-for-testing/agentic-qe) 框架集成，以增强功能。**所有 AQE 功能都是可选的——即使没有 AQE，Forge 也能正常工作。**

### 检测

在启动时，Forge 会检查 AQE 是否可用：

```bash
# Check if agentic-qe MCP server is registered
claude mcp list | grep -q "aqe" && echo "AQE available" || echo "AQE not available — using defaults"
```

### 使用 AQE 时的增强功能

| Forge 组件 | 无 AQE（默认） | 有 AQE |
|----------------|----------------------|----------|
| **模式存储** | claude-flow 内存（`forge-patterns` 命名空间） | ReasoningBank — 使用 HNSW 索引，搜索速度提高 150 倍，支持回放体验 |
| **缺陷预测** | 历史失败率和文件变化 | `defect-intelligence` 域 — 提供根本原因分析和缺陷预测功能 |
| **安全性扫描** | 第 4 个检查点（秘密信息、注入向量） | `security-compliance` 域 — 使用 security-scanner 工具进行全面的 SAST/DAST 检查 |
| **可访问性审计** | 使用 Forge 可访问性审计器 | `visual-accessibility` 域 |
| **契约测试** | 第 7 个检查点的契约验证 | `contract-testing` 域 | 使用 contract-validator 和 graphql-tester 工具 |
| **进度报告** | 使用 `.forge/progress.jsonl` 文件 | 通过 AG-UI 协议实时更新进度 |

### 备用行为

当 AQE 不可用时，Forge 会回退到内置的行为。无需额外配置，因为它会自动检测并适应环境。

### 配置

```yaml
# forge.config.yaml — AQE integration settings (optional)
integrations:
  agentic-qe:
    enabled: true  # auto-detected if not specified
    domains:
      - defect-intelligence
      - security-compliance
      - visual-accessibility
      - contract-testing
    reasoning_bank:
      enabled: true  # replaces claude-flow memory for forge-patterns namespace
    ag_ui:
      enabled: true  # stream progress events to AG-UI protocol
```

### AQE 代理的委托

当启用 AQE 时，Forge 会将特定的子任务委托给专门的 AQE 代理：

| Forge 代理 | AQE 领域 | 使用的 AQE 代理 |
|-------------|-----------|-----------------|
| 规范验证器 | `requirements-validation` | bdd-generator, requirements-validator |
| 故障分析器 | `defect-intelligence` | root-cause-analyzer, defect-predictor |
| 质量检查器（第 4 个检查点） | `security-compliance` | security-scanner, security-auditor |
| 可访问性审计器 | `visual-accessibility` | visual-tester, accessibility-auditor |
| 质量检查器（第 7 个检查点） | `contract-testing` | contract-validator, graphql-tester |
| 学习优化器 | `learning-optimization` | learning-coordinator, pattern-learner |

对于没有对应 AQE 功能的代理（如测试运行器、错误修复器、自动提交器），它们会继续以内置模式运行。

---

## 防御性测试模式

错误修复器会根据项目的测试框架使用相应的防御性测试模式。例如：

### Flutter 的防御性测试模式：
```dart
Future<bool> safeTap(WidgetTester tester, Finder finder) async {
  await tester.pumpAndSettle();
  final elements = finder.evaluate();
  if (elements.isNotEmpty) {
    await tester.tap(finder.first, warnIfMissed: false);
    await tester.pumpAndSettle();
    return true;
  }
  debugPrint('Widget not found: ${finder.description}');
  return false;
}
```

### Flutter 的安全文本输入模式
```dart
Future<bool> safeEnterText(WidgetTester tester, Finder finder, String text) async {
  await tester.pumpAndSettle();
  final elements = finder.evaluate();
  if (elements.isNotEmpty) {
    await tester.enterText(finder.first, text);
    await tester.pumpAndSettle();
    return true;
  }
  return false;
}
```

### Flutter 的视觉观察延迟模式
```dart
Future<void> visualDelay(WidgetTester tester, {String? label}) async {
  if (label != null) debugPrint('Observing: $label');
  await tester.pump(const Duration(milliseconds: 2500));
}
```

### Flutter 的等待 API 响应模式
```dart
Future<void> waitForApiResponse(WidgetTester tester, {int maxWaitMs = 5000}) async {
  final startTime = DateTime.now();
  while (DateTime.now().difference(startTime).inMilliseconds < maxWaitMs) {
    await tester.pump(const Duration(milliseconds: 100));
    if (find.byType(CircularProgressIndicator).evaluate().isEmpty) break;
  }
  await tester.pumpAndSettle();
}
```

### Cypress / Playwright 的安全点击模式
```javascript
async function safeClick(selector, options = { timeout: 5000 }) {
  try {
    await page.waitForSelector(selector, { state: 'visible', timeout: options.timeout });
    await page.click(selector);
    return true;
  } catch (e) {
    console.warn(`Element not found: ${selector}`);
    return false;
  }
}
```

### Cypress / Playwright 的等待 API 响应模式
```javascript
async function waitForApi(urlPattern, options = { timeout: 10000 }) {
  return page.waitForResponse(
    response => response.url().includes(urlPattern) && response.status() === 200,
    { timeout: options.timeout }
  );
}
```

---

## 常见的修复模式

### 模式：元素未找到
```json
{
  "error": "Element not found / No element / Bad state: No element",
  "cause": "Element not rendered, wrong selector, or not in viewport",
  "tier": "platinum",
  "confidence": 0.97,
  "fixes": [
    "Wait for element to be rendered before interaction",
    "Use safe interaction helpers instead of direct calls",
    "Verify selector matches actual element",
    "Scroll element into view before interaction"
  ]
}
```

### 模式：超时
```json
{
  "error": "Timeout / pumpAndSettle timed out / waiting for selector",
  "cause": "Infinite animation, continuous rebuild, or slow API",
  "tier": "gold",
  "confidence": 0.89,
  "fixes": [
    "Use fixed-duration wait instead of settle/idle wait",
    "Dispose animation controllers in tearDown",
    "Check for infinite re-render loops",
    "Increase timeout for slow API calls"
  ]
}
```

### 模式：断言失败
```json
{
  "error": "Expected: X, Actual: Y / AssertionError",
  "cause": "State not updated or wrong expectation",
  "tier": "silver",
  "confidence": 0.78,
  "fixes": [
    "Add delay before assertion for async state updates",
    "Verify test data seeding completed",
    "Check async operation completion before asserting"
  ]
}
```

### 模式：API 响应不匹配
```json
{
  "error": "Type error / null value / schema mismatch",
  "cause": "Backend response format changed",
  "tier": "gold",
  "confidence": 0.86,
  "fixes": [
    "Update model/DTO to match current API response",
    "Add null safety handling",
    "Check API version compatibility"
  ]
}
```

---

## 覆盖率跟踪

学习优化器会维护每个上下文的覆盖率状态：

```json
{
  "lastRun": "2026-02-07T11:00:00Z",
  "backendStatus": {
    "healthy": true,
    "port": 8080
  },
  "gateStatus": {
    "functional": "PASS",
    "behavioral": "PASS",
    "coverage": "PASS",
    "security": "PASS",
    "accessibility": "WARNING",
    "resilience": "PASS",
    "contract": "PASS"
  },
  "contexts": {
    "[context-a]": { "total": 68, "passing": 68, "failing": 0, "behavioralCoverage": 100 },
    "[context-b]": { "total": 72, "passing": 70, "failing": 2, "behavioralCoverage": 97 }
  },
  "totalPaths": 0,
  "passingPaths": 0,
  "coveragePercent": 0,
  "confidenceTiers": {
    "platinum": 0,
    "gold": 0,
    "silver": 0,
    "bronze": 0,
    "expired": 0
  }
}
```

---

## 自动提交消息格式

```
fix(forge): Fix [TEST_ID] - [brief description]

Behavioral Spec: [Gherkin scenario name]
Root Cause: [what caused the failure]
- [specific issue 1]
- [specific issue 2]

Fix Applied:
- [change 1]
- [change 2]

Quality Gates:
- Functional: PASS
- Behavioral: PASS
- Coverage: [X]%
- Security: PASS
- Accessibility: PASS/WARNING
- Resilience: PASS
- Contract: PASS

Test Verification:
- Test now passes after fix
- No regression in related tests
- Dependent contexts re-tested: [list]

Confidence Tier: [platinum|gold|silver|bronze]
Pattern Stored: fix-[error-type]-[hash]
```

---

## 回滚与冲突解决

### 回滚机制

如果修复操作导致了问题：
```bash
# Retrieve last known good commit
npx @claude-flow/cli@latest memory retrieve --key "last-green-commit" --namespace forge-state

# Rollback to that commit
git revert [bad-commit-hash]

# Store rollback event for learning (prevents pattern from being re-applied)
npx @claude-flow/cli@latest memory store \
  --key "rollback-[timestamp]" \
  --value '{"commit":"[hash]","reason":"[reason]","pattern":"[pattern-key]"}' \
  --namespace forge-patterns

# Demote the fix pattern confidence (-0.10)
# Learning Optimizer will handle this automatically
```

### 修复冲突处理

当错误修复器导致的修复引发了级联问题（依赖上下文的测试失败）时：
1. **停止** — 中止受影响上下文的修复过程。
2. **重新分析** — 故障分析器会检查原始故障和级联故障。
3. **分类** — 比较根本原因：
   - **根本原因不同** → 保留原始修复；将级联故障视为新的独立故障，在下一次循环中处理。
   - **根本原因相同** → 撤销修复操作，并降低该模式的置信度（降低 0.10）。
4. **回滚限制** — 每个测试最多进行 2 次回滚操作，之后会请求用户审核。
5. **升级机制** — 如果同一测试出现两次回滚，Forge 会暂停并报告：

```
   ESCALATION: Test [testId] has regressed 2x after fix attempts.
   Original failure: [description]
   Cascade failure: [description]
   Attempted fixes: [list]
   Recommendation: Manual review required.
   ```

### 代理间意见不一致时的处理

当两个代理的意见不一致时（例如，错误修复器想要修改规范验证器认为不应修改的文件）：
1. **质量检查器充当仲裁者** — 它会评估两种修改方案。
2. **选择更优的方案**：
   - 修改的文件较少 → 优先选择。
   | 置信度更高 → 优先选择。
   | 错误修复器的修改方案 → 优先采用规范验证器的建议。

---

## 执行后的学习

每次自动运行结束后，该工具会触发全面的学习过程：

```bash
# Train on successful patterns
npx @claude-flow/cli@latest hooks post-task --task-id "forge-run" --success true --store-results true

# Update neural patterns
npx @claude-flow/cli@latest neural train --pattern-type forge-fixes --epochs 5

# Update defect predictions
npx @claude-flow/cli@latest memory store \
  --key "prediction-$(date +%Y-%m-%d)" \
  --value "[prediction JSON from Learning Optimizer]" \
  --namespace forge-predictions

# Export metrics
npx @claude-flow/cli@latest hooks metrics --format json
```

---

## 项目特定的扩展

可以通过创建 `forge.contexts.yaml` 文件来为每个项目定制 Forge 的配置：

```yaml
# forge.contexts.yaml — Project-specific bounded contexts and screens
contexts:
  - name: identity
    testFile: click_through_identity_full_test.dart
    specFile: identity.feature
    paths: 68
    subdomains: [Auth, Profiles, Verification]
    screens:
      - name: Identity Verification
        file: lib/screens/compliance/identity_verification_screen.dart
        route: /verification
        cyclomaticPaths:
          - All verifications incomplete -> show progress 0%
          - Email only verified -> show 25%
          - All verified -> show 100% + celebration state

  - name: payments
    testFile: click_through_payments_test.dart
    specFile: payments.feature
    paths: 89
    subdomains: [Wallet, Cards, Transactions]

dependencies:
  identity:
    blocks: [rides, payments, driver]
  payments:
    depends_on: [identity]
    blocks: [rides, subscriptions]
```

这样可以将通用的 Forge 架构与项目特定的配置分离，使得 Forge 可以在任意代码库中重复使用。

---

## 快速参考检查清单

在运行 Forge 之前：
- 确保后端已经构建并运行。
- 确保通过健康检查。
- 通过真实的 API 调用生成测试数据。
- 确保测试代码中不使用模拟或存根技术。
- 确保目标上下文有对应的 Gherkin 规范（或者已经生成）。
- 确保所有新的页面都有测试覆盖。
- 确保所有的边缘情况都已被记录和测试。

Forge 完成后：
- 第 1 个检查点（功能性）：所有测试通过。
- 第 2 个检查点（行为性）：所有目标 Gherkin 场景都满足。
- 第 3 个检查点（覆盖率）：总覆盖率 >=85%，关键路径 >=95%。
- 第 4 个检查点（安全性）：没有硬编码的秘密信息，存储安全，没有严重的安全漏洞。
- 第 5 个检查点（可访问性）：符合 WCAG AA 标准。
- 第 6 个检查点（弹性）：支持离线操作、超时处理和错误状态。
- 第 7 个检查点（契约）：API 响应符合预期格式。
- 所有应用的修复模式的置信度都已更新。
- 所有修复操作都附带详细的提交信息。