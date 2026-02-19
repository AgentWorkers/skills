# 质量保证与测试引擎 — 完整的软件质量管理体系

> 这是针对AI代理的终极测试方法论。从测试策略到执行、覆盖范围到报告生成——您所需的一切，以确保软件的质量。

## 第1阶段：测试策略设计

在编写任何测试用例之前，首先设计好测试策略。

### 策略简报模板

```yaml
project:
  name: ""
  type: web-app | api | mobile | library | cli | data-pipeline
  languages: [typescript, python, go, java]
  frameworks: [react, express, django, spring]
  
risk_profile:
  data_sensitivity: low | medium | high | critical  # PII, financial, health
  user_impact: internal | b2b | b2c | life-safety
  deployment_frequency: daily | weekly | monthly
  regulatory: [none, SOC2, HIPAA, PCI-DSS, GDPR]

test_scope:
  in_scope: []    # Features, services, components
  out_of_scope: [] # Explicitly excluded (with reason)
  
environments:
  dev: { url: "", db: "local" }
  staging: { url: "", db: "seeded" }
  prod: { url: "", smoke_only: true }
```

### 测试类型决策矩阵

| 风险等级 | 单元测试 | 集成测试 | 端到端测试 | 性能测试 | 安全性测试 | 可访问性测试 |
|---|---|---|---|---|---|---|
| 内部工具 | ✅ | ✅ | ⚠️ | ❌ | ⚠️ | ❌ |
| B2B SaaS | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| B2C高流量 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 金融/医疗行业 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 金融/医疗行业（高并发） | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 金融/医疗行业（包含混沌工程） | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

### 测试金字塔架构

```
         /  E2E  \          5-10% — Critical user journeys only
        / Integration \     20-30% — API contracts, service boundaries
       /    Unit Tests   \  60-70% — Business logic, pure functions
```

**反模式：过度依赖端到端测试（“冰淇淋锥”）** — 过度依赖端到端测试而忽视单元测试。这种方式效率低、可靠性差且成本高。解决方法是将测试覆盖范围向下调整到金字塔的较低层级。

**反模式：失衡的测试结构（“沙漏”）** — 单元测试和端到端测试数量过多，但缺乏集成测试。这会导致服务之间的接口问题被忽略。

---

## 第2阶段：单元测试精通

### AAA测试模式（Arrange-Act-Assert）

每个单元测试都应遵循以下结构：

```typescript
describe('PricingCalculator', () => {
  // Group by behavior, not by method
  describe('when customer has volume discount', () => {
    it('applies tiered pricing above threshold', () => {
      // ARRANGE — Set up the scenario
      const calculator = new PricingCalculator();
      const customer = createCustomer({ tier: 'enterprise', units: 150 });
      
      // ACT — Execute the behavior under test
      const price = calculator.calculate(customer);
      
      // ASSERT — Verify the outcome (ONE logical assertion)
      expect(price).toEqual({
        subtotal: 12000,
        discount: 1800,  // 15% volume discount
        total: 10200,
      });
    });
  });
});
```

### 测试命名规范

**格式：`[单元测试名称] [测试场景] [预期结果]`

✅ 正确的命名示例：
- `PricingCalculator applies 15% discount when units exceed 100`（当购买数量超过100个时，`PricingCalculator`会应用15%的折扣）
- `UserService throwsNotFoundError when user ID is invalid`（当用户ID无效时，`UserService`会抛出`NotFoundError`异常）
- `parseDate returns null for malformed ISO strings`（对于格式错误的ISO字符串，`parseDate`会返回`null`）

❌ 错误的命名示例：
- `test1`（仅包含“应该正常工作”这样的描述，没有明确说明测试内容）

### 单元测试的重点内容（按优先级排序）：
1. **业务逻辑** — 价格计算、规则应用、状态机逻辑
2. **数据转换** — 解析器、格式化器、序列化器的正确性
3. **边界情况** — 数据边界、空值/未定义值、空集合的处理
4. **错误处理** — 每个错误处理逻辑的验证
5. **纯函数** — 最容易测试的代码，具有最高的测试回报

### 不应进行单元测试的内容：
- 框架内部实现（如React渲染、Express路由逻辑）
- 没有逻辑的简单getter/setter方法
- 第三方库的行为
- 代码的实现细节（如私有方法、内部状态）

### 测试用例模拟规则：

| 依赖类型 | 模拟策略 | 示例 |
|---|---|---|
| 数据库 | 模拟数据库访问层（如`jest.mock('./userRepo')`） |
| HTTP API | 模拟HTTP客户端或使用第三方库（如`msw.http.get('/api/users', ...)` |
| 文件系统 | 模拟文件系统操作（如`jest.mock('fs/promises')`） |
| 时间/日期处理 | 使用模拟定时器（如`jest.useFakeTimers()`） |
| 随机性处理 | 为随机数生成设置种子或使用模拟函数（如`jest.spyOn(Math, 'random')`） |
| 环境变量 | 手动修改环境变量（如`process.env.NODE_ENV = 'test'`）

**规则：仅在必要的地方进行模拟。** 如果你模拟的是自己实现的类，可能意味着你的设计需要重构。

### 测试覆盖目标：

| 测试指标 | 最低要求 | 良好 | 优秀 |
|---|---|---|---|
| 代码行覆盖率 | 70% | 85% | 95%以上 |
| 分支覆盖率 | 60% | 80% | 90%以上 |
| 函数覆盖率 | 75% | 90% | 95%以上 |
| 关键路径覆盖率 | 100% | 100% | 100% |

**注意：** 100%的代码覆盖率并不等同于高质量。覆盖率只反映了代码被执行的情况，并不能保证所有功能都经过了验证。一个没有断言的测试虽然有覆盖率，但实际价值有限。

---

## 第3阶段：集成测试

### API测试检查清单

对于每个API接口，都需要进行以下测试：

```yaml
endpoint: POST /api/orders
tests:
  happy_path:
    - Valid request returns 201 with order ID
    - Response matches schema
    - Database record created correctly
    - Events/webhooks fired
    
  validation:
    - Missing required fields → 400 with field errors
    - Invalid data types → 400 with type errors
    - Business rule violations → 422 with explanation
    
  authentication:
    - No token → 401
    - Expired token → 401
    - Wrong role → 403
    - Valid token → proceeds
    
  edge_cases:
    - Duplicate request (idempotency) → same response
    - Concurrent requests → no race condition
    - Maximum payload size → 413 or graceful handling
    - Special characters in input → no injection
    
  error_handling:
    - Database down → 503 with retry hint
    - External service timeout → 504 or fallback
    - Rate limit exceeded → 429 with retry-after
```

### 接口契约测试

当不同服务之间进行交互时，需要验证它们之间的契约是否得到遵守：

```yaml
contract:
  consumer: order-service
  provider: payment-service
  
  interactions:
    - description: "Process payment"
      request:
        method: POST
        path: /payments
        body:
          amount: 99.99
          currency: USD
          order_id: "ord_123"
      response:
        status: 200
        body:
          payment_id: "pay_xxx"  # string, not null
          status: "completed"    # enum: completed|pending|failed
          
  breaking_changes:  # NEVER do these without versioning
    - Remove a field from response
    - Change a field's type
    - Add a required field to request
    - Change the URL path
    - Change error response format
```

### 数据库测试规则：
1. **每次测试后数据状态应恢复到初始状态** — 使用可以回滚的事务操作，或在测试之间清除数据库数据。
2. **使用测试工厂而不是固定数据** — 例如：`createUser({ role: 'admin' })` 而不是硬编码SQL语句。
3. **测试数据库迁移逻辑** — 包括迁移前、迁移中和迁移后的操作。
4. **验证数据库约束条件** — 如唯一性约束、外键级联、非空字段等。
5. **测试复杂的查询语句** — 特别是涉及JOIN操作、聚合函数和窗口函数的查询。

---

## 第4阶段：端到端测试

### 关键用户流程测试

识别并测试那些能够产生收入或影响用户体验的核心业务流程：

```yaml
critical_journeys:
  - name: "Sign up → First value"
    steps:
      - Visit landing page
      - Click sign up
      - Fill registration form
      - Verify email
      - Complete onboarding
      - Perform first key action
    max_duration: 3 minutes
    
  - name: "Purchase flow"
    steps:
      - Browse products
      - Add to cart
      - Enter shipping
      - Enter payment
      - Confirm order
      - Receive confirmation email
    max_duration: 2 minutes
    
  - name: "Login → Core task → Logout"
    steps:
      - Login (password + SSO + MFA variants)
      - Navigate to core feature
      - Complete primary workflow
      - Verify result
      - Logout
    max_duration: 1 minute
```

### 端到端测试的最佳实践：
1. **测试用户行为，而非代码实现** — 通过文本或角色名称来点击按钮，而不是依赖CSS类名。
2. **仅在无法使用标准选择器时才使用`dataTestId`。
3. **等待页面状态变化，而不是等待固定时间** — 使用`waitFor(element)`而不是`sleep(3000)`。
4. **为每个测试创建独立的数据**。
5. **在持续集成（CI）环境中运行测试，并设置重试机制** — 对于网络不稳定的情况，设置重试次数；如果失败率超过5%，则需要深入排查。

### 选择测试选择器的优先级（从最佳到最差）：
1. `getByRole('button', { name: 'Submit' })` — 可访问性良好，且稳定性高。
2. `getByLabelText('Email')` — 与表单相关，易于使用。
3. `getByText('Welcome back')` — 基于文本内容的选择器。
4. `getByText('submit-btn')` — 明确指定的测试选择器。
5. `querySelector('.btn-primary')` — 易受CSS变化影响，稳定性较差。

### 不稳定的测试用例处理：
| 症状 | 可能原因 | 解决方案 |
|---|---|---|
| 在本地测试通过但在CI环境中失败 | 代码执行时间或竞争条件 | 添加显式的等待逻辑，检查CI系统的资源限制。
| 测试结果不稳定 | 测试之间存在共享状态 | 为每个测试创建独立的数据，重置测试环境。
| 部署后测试失败 | 环境差异 | 检查环境变量、API版本和功能开关。
| 在特定时间点失败 | 代码依赖于时间因素 | 使用模拟的时间值，避免基于时间的断言。
| 并行测试时失败 | 资源竞争 | 为每个测试任务分配唯一的端口或数据库连接。

**规则：** 将不稳定的测试用例在24小时内隔离出来。一个被所有人忽视的不稳定测试集合，比没有测试的情况更糟糕。

---

## 第5阶段：性能测试

### 负载测试设计

```yaml
performance_tests:
  smoke:
    vus: 5
    duration: 1m
    purpose: "Verify test works"
    
  load:
    vus: 100  # Expected concurrent users
    duration: 10m
    ramp_up: 2m
    purpose: "Normal traffic behavior"
    thresholds:
      p95_response: <500ms
      error_rate: <1%
      
  stress:
    vus: 300  # 3x expected load
    duration: 15m
    ramp_up: 5m
    purpose: "Find breaking point"
    
  soak:
    vus: 80
    duration: 2h
    purpose: "Memory leaks, connection exhaustion"
    
  spike:
    stages:
      - { vus: 50, duration: 2m }
      - { vus: 500, duration: 30s }  # Sudden spike
      - { vus: 50, duration: 2m }
    purpose: "Recovery behavior"
```

### 性能指标：

| 测试指标 | Web应用 | API | 后台任务 |
|---|---|---|---|
| 响应时间（50%的时间点） | <200毫秒 | <100毫秒 | 不适用 |
| 响应时间（95%的时间点） | <1秒 | <500毫秒 | 不适用 |
| 响应时间（99%的时间点） | <3秒 | <1秒 | 不适用 |
| 吞吐量 | >100请求/秒 | >500请求/秒 | >1000请求/秒 |
| 错误率 | <0.1% | <0.1% | <0.5% |
| CPU使用率 | <70% | <70% | <90% |
| 内存使用增长 | <5%/小时 | <2%/小时 | <10%/小时 |

### 数据库性能测试

```yaml
db_performance:
  query_tests:
    - name: "Dashboard aggregate query"
      baseline: 50ms
      max_acceptable: 200ms
      with_1M_rows: measure
      with_10M_rows: measure
      
  index_verification:
    - Run EXPLAIN ANALYZE on all critical queries
    - Verify no sequential scans on tables >10K rows
    - Check index usage statistics weekly
    
  connection_pool:
    - Test at max connections
    - Verify graceful handling when pool exhausted
    - Monitor connection wait time
```

---

## 第6阶段：安全性测试

### OWASP十大安全漏洞测试

```yaml
security_tests:
  A01_broken_access_control:
    - [ ] Horizontal privilege escalation (access other user's data)
    - [ ] Vertical privilege escalation (access admin functions)
    - [ ] IDOR (Insecure Direct Object References)
    - [ ] Missing function-level access control
    - [ ] CORS misconfiguration
    
  A02_cryptographic_failures:
    - [ ] Sensitive data in transit (TLS 1.2+)
    - [ ] Sensitive data at rest (encryption)
    - [ ] Password hashing (bcrypt/argon2, not MD5/SHA)
    - [ ] No secrets in code/logs/URLs
    
  A03_injection:
    - [ ] SQL injection (parameterized queries)
    - [ ] NoSQL injection
    - [ ] Command injection (OS commands)
    - [ ] XSS (stored, reflected, DOM-based)
    - [ ] Template injection (SSTI)
    
  A04_insecure_design:
    - [ ] Rate limiting on auth endpoints
    - [ ] Account lockout after N failures
    - [ ] CAPTCHA on public forms
    - [ ] Business logic abuse scenarios
    
  A05_security_misconfiguration:
    - [ ] Default credentials removed
    - [ ] Error messages don't leak stack traces
    - [ ] Security headers set (CSP, HSTS, X-Frame-Options)
    - [ ] Directory listing disabled
    - [ ] Unnecessary HTTP methods disabled
    
  A07_auth_failures:
    - [ ] Brute force protection
    - [ ] Session fixation
    - [ ] Session timeout
    - [ ] JWT validation (signature, expiry, issuer)
    - [ ] MFA bypass attempts
```

### 输入验证测试

对所有用户输入进行验证，确保其符合安全要求：

```yaml
injection_payloads:
  sql: ["' OR 1=1--", "'; DROP TABLE users;--", "1 UNION SELECT * FROM users"]
  xss: ["<script>alert(1)</script>", "<img onerror=alert(1) src=x>", "javascript:alert(1)"]
  path_traversal: ["../../etc/passwd", "..\\..\\windows\\system32", "%2e%2e%2f"]
  command: ["; ls -la", "| cat /etc/passwd", "$(whoami)", "`id`"]
  
boundary_values:
  strings: ["", " ", "a"*10000, null, undefined, "emoji: 🎯", "unicode: é à ü", "rtl: مرحبا"]
  numbers: [0, -1, 2147483647, -2147483648, NaN, Infinity, 0.1+0.2]
  arrays: [[], [null], Array(10000)]
  dates: ["1970-01-01", "2099-12-31", "invalid-date", "2024-02-29", "2023-02-29"]
```

---

## 第7阶段：测试自动化架构

### 框架选择指南：

| 测试需求 | JavaScript/TypeScript | Python | Go | Java |
|---|---|---|---|---|
| 单元测试 | Vitest/Jest | pytest | testing + testify | JUnit 5 |
| API测试 | Supertest | httpx + pytest | net/http/httptest | RestAssured |
| 端到端测试（浏览器） | Playwright | Playwright | chromedp | Selenium |
| 性能测试 | k6 | Locust | vegeta | Gatling |
| 接口契约测试 | Pact | Pact | Pact | Pact |
| 安全性测试 | ZAP + 自定义工具 | Bandit + 自定义工具 | gosec | SpotBugs |

### 持续集成（CI）流程中的测试阶段

```yaml
pipeline:
  stage_1_fast:  # <2 min, blocks PR
    - Lint + type check
    - Unit tests
    - Security: dependency scan (npm audit / safety)
    
  stage_2_thorough:  # <10 min, blocks merge
    - Integration tests
    - Contract tests
    - Security: SAST scan
    - Coverage report + threshold check
    
  stage_3_confidence:  # <30 min, blocks deploy
    - E2E critical journeys
    - Visual regression (if applicable)
    - Security: container scan
    
  stage_4_post_deploy:  # After deploy to staging
    - Smoke tests against staging
    - Performance baseline check
    - Security: DAST scan (ZAP)
    
  stage_5_production:  # After prod deploy
    - Smoke tests (critical paths only)
    - Synthetic monitoring enabled
    - Canary metrics watching
```

### 测试数据管理

```yaml
test_data_strategy:
  unit_tests:
    approach: factories  # Builder pattern, create exactly what you need
    example: "createUser({ role: 'admin', plan: 'enterprise' })"
    
  integration_tests:
    approach: seeded_database
    reset: per_test_suite  # Transaction rollback or truncate
    sensitive_data: anonymized  # Never use real PII
    
  e2e_tests:
    approach: api_setup  # Create data via API before test
    cleanup: after_each  # Delete created data
    isolation: unique_identifiers  # Timestamp or UUID in test data
    
  performance_tests:
    approach: representative_dataset
    volume: 10x_production  # Test with more data than prod
    generation: faker_libraries  # Realistic but synthetic
```

---

## 第8阶段：质量指标与报告

### 测试健康状况仪表盘

```yaml
metrics:
  test_suite_health:
    total_tests: 0
    passing: 0
    failing: 0
    skipped: 0  # >5% skipped = tech debt alarm
    flaky: 0    # >2% flaky = quarantine immediately
    
  coverage:
    line: "0%"
    branch: "0%"
    critical_paths: "0%"  # Must be 100%
    
  execution:
    unit_duration: "0s"    # Target: <30s
    integration_duration: "0s"  # Target: <5m
    e2e_duration: "0s"     # Target: <15m
    total_ci_time: "0s"    # Target: <20m
    
  defect_metrics:
    bugs_found_in_test: 0
    bugs_escaped_to_prod: 0
    escape_rate: "0%"      # Target: <5%
    mttr: "0h"             # Mean time to resolve
    
  trends:  # Track weekly
    new_tests_added: 0
    tests_deleted: 0  # Healthy deletion = removing redundant tests
    coverage_delta: "+0%"
    flake_rate_delta: "+0%"
```

### 测试报告模板

```markdown
# Test Report — [Feature/Sprint/Release]

## Summary
- **Status:** ✅ PASS / ⚠️ PASS WITH RISKS / ❌ FAIL
- **Tests Run:** X | **Passed:** X | **Failed:** X | **Skipped:** X
- **Coverage:** Line X% | Branch X% | Critical 100%
- **Duration:** Xm Xs

## Key Findings

### 🔴 Critical (Block Release)
1. [Finding] — [Impact] — [Fix recommendation]

### 🟡 High (Fix Before Next Release)
1. [Finding] — [Impact] — [Fix recommendation]

### 🟢 Medium/Low (Backlog)
1. [Finding] — [Impact]

## Risk Assessment
- **Untested areas:** [list]
- **Known flaky tests:** [list with ticket IDs]
- **Performance concerns:** [if any]

## Recommendation
[Ship / Ship with monitoring / Hold for fixes]
```

### 质量评分（0-100分）

| 测试指标 | 权重 | 分数 |
|---|---|---|
| 测试覆盖范围 | 20% | <60%得0分，60-70%得5分，70-80%得10分，80-90%得15分，90%以上得20分 |
| 关键路径覆盖率 | 20% | <100%得0分，100%得20分 |
| 缺陷发现率 | 15% | >10%得0分，5-10%得5分，2-5%得10分，<2%得15分 |
| 测试套件执行速度 | 10% | >30毫秒得0分，20-30毫秒得3分，10-20毫秒得7分，<10毫秒得10分 |
| 测试用例的稳定性 | 10% | >30毫秒得0分，20-30毫秒得3分，10-20毫秒得7分，<10毫秒得10分 |
| 测试用例的失败率 | 10% | >5%得0分，2-5%得3分，1-2%得7分，<1%得10分 |
| 安全性测试覆盖率 | 10% | 未进行安全性测试得0分，基本安全测试得3分，OWASP十大漏洞测试得7分，全面安全测试得10分 |
| 文档完整性 | 5% | 未编写文档得0分，基本文档得2分，完整文档得5分 |
| 自动化程度 | 10% | 自动化程度低于50%得0分，50-70%得3分，70-90%得7分，90%以上得10分 |

**评分标准：** 0-40分表示非常差；41-60分表示需要改进；61-80分表示表现良好；81-100分表示优秀。

---

## 第9阶段：专项测试

### 可访问性测试（WCAG 2.1标准）

```yaml
accessibility_checklist:
  level_a:  # Minimum compliance
    - [ ] All images have alt text
    - [ ] All form inputs have labels
    - [ ] Color is not the only visual indicator
    - [ ] Page has proper heading hierarchy (h1→h2→h3)
    - [ ] All functionality available via keyboard
    - [ ] Focus is visible and logical
    - [ ] No content flashes >3 times/second
    
  level_aa:  # Standard compliance (recommended)
    - [ ] Color contrast ratio ≥4.5:1 (normal text)
    - [ ] Color contrast ratio ≥3:1 (large text)
    - [ ] Text resizable to 200% without loss
    - [ ] Skip navigation links
    - [ ] Consistent navigation across pages
    - [ ] Error suggestions provided
    - [ ] ARIA landmarks for page regions
    
  tools:
    - axe-core (automated, catches ~30% of issues)
    - Lighthouse accessibility audit
    - Manual keyboard navigation test
    - Screen reader testing (VoiceOver/NVDA)
```

### API向后兼容性测试

```yaml
compatibility_tests:
  when_updating_api:
    - [ ] All existing fields still present in response
    - [ ] No field type changes (string→number)
    - [ ] New required request fields have defaults
    - [ ] Deprecated fields still work (with warning header)
    - [ ] Error format unchanged
    - [ ] Pagination behavior unchanged
    - [ ] Rate limits not reduced
    
  versioning_strategy:
    - URL versioning: /v1/users, /v2/users
    - Header versioning: Accept: application/vnd.api+json;version=2
    - Sunset header for deprecated versions
    - Minimum 6-month deprecation notice
```

### 混乱工程（Chaos Engineering）原则

```yaml
chaos_tests:
  network:
    - Service dependency goes down → graceful degradation?
    - Network latency increases 10x → timeout handling?
    - DNS resolution fails → fallback behavior?
    
  infrastructure:
    - Database primary fails → replica promotion?
    - Cache (Redis) goes down → DB fallback works?
    - Disk fills up → alerting + graceful failure?
    
  application:
    - Memory pressure → OOM handling?
    - CPU saturation → request queuing?
    - Certificate expiry → monitoring alert?
    
  data:
    - Corrupt message in queue → dead letter + alert?
    - Schema migration fails mid-way → rollback works?
    - Clock skew between services → idempotency holds?
```

---

## 第10阶段：日常质量保证工作流程

### 新功能开发流程：
1. **需求评审** — 在编写代码之前先确定测试场景（提前规划）。
2. **编写测试用例** — 覆盖正常使用场景、边界情况以及潜在错误。
3. **审查代码提交（PR）中的测试用例** — 测试用例是否具有实际意义？它们是否真正验证了功能行为？
4. **执行完整的测试套件** — 对受影响的模块进行单元测试、集成测试和端到端测试。
5. **生成测试报告** — 使用上述提供的报告模板。

### 错误修复流程：
1. **首先编写失败的测试用例** — 将错误重现为可执行的测试用例。
2. **验证修复后的代码是否能通过测试** — 测试结果就是修复效果的直接证明。
3. **检查是否存在回归问题** — 运行相关的测试套件。
4. **将修复后的代码加入回归测试套件** — 这可以防止类似错误再次发生。

### 每周质量保证审查：
```yaml
weekly_review:
  monday:
    - Review flaky test quarantine — fix or delete
    - Check coverage trends — declining = tech debt
    - Review escaped defects — update test strategy
    
  friday:
    - Update test health dashboard
    - Clean up obsolete tests
    - Document new testing patterns discovered
    - Plan next week's testing focus
```

### 常用命令：
- `"Create test strategy for [项目/功能]"` → 生成完整的测试策略简报。
- `"Write unit tests for [函数/类]"` → 为相关功能编写单元测试用例。
- `"Test this API endpoint: [方法] [路径]"` → 对指定API接口进行全面的测试。
- `"Review these tests for quality"` → 对测试代码进行质量审查。
- `"Generate performance test plan"` → 生成性能测试计划。
- `"Security test [功能/接口]"` → 进行安全性测试。
- `"Create test report for [版本]"` → 生成格式化的测试报告。
- `"What's our test health?"` → 查看测试健康状况仪表盘。
- `"Find gaps in our test coverage"` | 分析测试覆盖范围中的不足，并提供优先级建议。
- `"Help debug this flaky test"` | 分析不稳定的测试用例，并提供修复建议。
- `"Set up CI test pipeline"` | 配置持续集成测试流程。
- `"Accessibility audit [页面/组件]"` | 对页面/组件进行可访问性审计。