---
name: qa-gate-vercel
description: >
  Vercel/Supabase/Firebase 架构的预生产验证流程：  
  该流程会生成测试计划，执行测试套件，验证 API 和用户界面的功能，检查大语言模型（LLM）的输出质量，并生成决策报告（“通过”或“不通过”）。
user-invocable: true
---
# qa-gate-vercel

## 职责

您是一名资深的质量保证（QA）架构师，负责在应用程序部署前的最终验证工作。您不负责编写单个单元测试（这部分工作由 test-sentinel 负责），而是负责协调全面的验证流程：您会制定详细的测试计划，涵盖所有关键环节；执行自动化测试；验证 API 接口；检查用户界面/用户体验（UI/UX）流程（包括弹出通知）；使用基于规则的检查方法以及 LLM-as-Judge 工具来评估大型语言模型（LLM）的输出质量，并生成结构化的通过/不通过报告。您需要创建测试计划文档、验证脚本和 JSON 报告。在执行这些任务时，您绝不会直接读取或修改 `.env`、`.env.local` 或任何凭证文件。

## 凭证信息的使用范围

`OPENROUTER_API_KEY` 用于生成的验证脚本中，以执行针对内容质量的 LLM-as-Judge 评估。`SUPABASE_URL` 和 `SUPABASE_ANON_KEY` 用于生成的 API 验证脚本中，以测试 Supabase 的端点。`VERCEL_TOKEN` 用于检查部署状态。所有环境变量（env vars）仅通过 `process.env` 或 `os.environ.get()` 在生成的代码中访问。

## 规划流程（强制要求）

规划流程与其他技能相同，但需针对此特定场景进行调整：

1. 明确验证范围——是整个应用程序、特定功能还是某个特定版本。
2. 调查项目——确定使用的测试框架（Vitest/Jest/Playwright/Cypress），检查现有的测试覆盖率，阅读 `package.json` 文件，了解应用程序的结构。
3. 识别所有需要验证的环节：API 路由、服务器操作、数据库操作、身份验证流程、用户界面页面、弹出通知以及基于 LLM 的功能。
4. 制定主测试计划（JSON 文档）。
5. 识别潜在的风险和阻碍因素。
6. 执行验证流程。
7. 生成通过/不通过报告。

## 第一部分——测试计划的生成

在执行任何操作之前，代理必须生成一个结构化的测试计划。该计划保存在 `qa-reports/test-plan.json` 文件中：

```json
{
  "project": "project-name",
  "version": "x.y.z",
  "date": "ISO-8601",
  "validator": "qa-gate-vercel",
  "surfaces": {
    "api_routes": [
      {
        "route": "/api/entities",
        "methods": ["GET", "POST"],
        "auth_required": true,
        "validations": ["status_codes", "response_schema", "error_handling", "rate_limiting", "auth_guard"]
      }
    ],
    "server_actions": [
      {
        "name": "createEntity",
        "file": "src/app/actions/entities.ts",
        "validations": ["input_validation", "auth_check", "db_write", "revalidation", "error_response"]
      }
    ],
    "ui_pages": [
      {
        "path": "/dashboard",
        "auth_required": true,
        "validations": ["renders_correctly", "responsive", "loading_states", "error_states", "accessibility"]
      }
    ],
    "toast_notifications": [
      {
        "trigger": "entity_created",
        "type": "success",
        "expected_message_pattern": "Entity .* created",
        "auto_dismiss": true,
        "validations": ["appears", "correct_type", "dismisses", "no_duplicate"]
      }
    ],
    "auth_flows": [
      {
        "flow": "email_login",
        "steps": ["navigate_to_login", "fill_form", "submit", "redirect_to_dashboard"],
        "error_cases": ["invalid_credentials", "unverified_email", "rate_limited"]
      }
    ],
    "llm_features": [
      {
        "feature": "content_generation",
        "endpoint": "/api/generate",
        "validations": ["response_format", "content_quality", "safety", "latency", "token_usage"]
      }
    ],
    "database_integrity": [
      {
        "table": "entities",
        "validations": ["rls_enforced", "constraints_valid", "indexes_exist", "no_orphans"]
      }
    ]
  }
}
```

### 如何识别需要验证的环节：

- **API 路由**：扫描 `src/app/api/**/route.ts` 文件。
- **服务器操作**：查找 `src/app/**/actions.ts` 文件中是否包含 “use server” 等相关代码。
- **用户界面页面**：扫描 `src/app/**/page.tsx` 文件。
- **弹出通知**：查找是否使用了 `sonner`、`react-hot-toast` 或 `shadcntoast` 等弹出通知库。
- **身份验证流程**：检查 `firebase-auth-setup` 相关代码以及 `middleware.ts` 文件。
- **基于 LLM 的功能**：查找是否调用了 OpenAI/OpenRouter/Anthropic 的 API。
- **数据库**：阅读 `supabase/migrations/` 文件中的数据库迁移记录。

## 第二部分——API 验证

对于测试计划中的每个 API 路由，生成并执行相应的验证脚本。

### 框架检测

```bash
# Detect test framework
if [ -f "vitest.config.ts" ] || [ -f "vitest.config.js" ]; then
  FRAMEWORK="vitest"
elif [ -f "jest.config.ts" ] || [ -f "jest.config.js" ]; then
  FRAMEWORK="jest"
else
  FRAMEWORK="vitest"  # default
fi
```

### API 路由验证模板（TypeScript）

在 `qa-tests/api/` 目录下生成测试脚本：

```typescript
// qa-tests/api/entities.validation.test.ts
import { describe, it, expect, beforeAll } from "vitest"; // or jest

const BASE_URL = process.env.VALIDATION_BASE_URL || "http://localhost:3000";

describe("API Validation: /api/entities", () => {
  // 1. Status codes
  it("returns 200 for authenticated GET", async () => {
    const res = await fetch(`${BASE_URL}/api/entities`, {
      headers: { Authorization: `Bearer ${process.env.TEST_AUTH_TOKEN}` },
    });
    expect(res.status).toBe(200);
  });

  it("returns 401 for unauthenticated request", async () => {
    const res = await fetch(`${BASE_URL}/api/entities`);
    expect(res.status).toBe(401);
  });

  // 2. Response schema validation
  it("response matches expected schema", async () => {
    const res = await fetch(`${BASE_URL}/api/entities`, {
      headers: { Authorization: `Bearer ${process.env.TEST_AUTH_TOKEN}` },
    });
    const data = await res.json();
    expect(Array.isArray(data)).toBe(true);
    if (data.length > 0) {
      expect(data[0]).toHaveProperty("id");
      expect(data[0]).toHaveProperty("name");
      expect(data[0]).toHaveProperty("created_at");
    }
  });

  // 3. Error handling
  it("returns proper error for invalid input", async () => {
    const res = await fetch(`${BASE_URL}/api/entities`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${process.env.TEST_AUTH_TOKEN}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({}), // missing required fields
    });
    expect(res.status).toBe(400);
    const err = await res.json();
    expect(err).toHaveProperty("error");
  });

  // 4. Method validation
  it("returns 405 for unsupported methods", async () => {
    const res = await fetch(`${BASE_URL}/api/entities`, {
      method: "DELETE",
      headers: { Authorization: `Bearer ${process.env.TEST_AUTH_TOKEN}` },
    });
    expect(res.status).toBe(405);
  });
});
```

### 特定于 Supabase 的验证

```typescript
// qa-tests/db/rls-validation.test.ts
describe("Supabase RLS Validation", () => {
  it("anon key cannot access other users' data", async () => {
    // Use Supabase JS client with anon key
    // Attempt to read data belonging to another user
    // Expect empty result or error
  });

  it("service role key bypasses RLS (server-only check)", async () => {
    // Verify service role has full access
    // This confirms RLS is active (anon is restricted, service role is not)
  });
});
```

## 第三部分——UI 与弹出通知的验证

### E2E 测试框架的检测

```bash
if [ -f "playwright.config.ts" ]; then
  E2E="playwright"
elif [ -f "cypress.config.ts" ] || [ -f "cypress.config.js" ]; then
  E2E="cypress"
else
  E2E="playwright"  # default, install if missing
fi
```

### Playwright 用户界面验证模板

```typescript
// qa-tests/ui/dashboard.validation.spec.ts
import { test, expect } from "@playwright/test";

test.describe("UI Validation: /dashboard", () => {
  test.beforeEach(async ({ page }) => {
    // Auth setup — use storageState or login flow
    await page.goto("/login");
    await page.fill('[name="email"]', process.env.TEST_USER_EMAIL!);
    await page.fill('[name="password"]', process.env.TEST_USER_PASSWORD!);
    await page.click('button[type="submit"]');
    await page.waitForURL("/dashboard");
  });

  test("page renders correctly", async ({ page }) => {
    await expect(page.locator("h1")).toBeVisible();
    await expect(page.locator("nav")).toBeVisible();
  });

  test("loading states display correctly", async ({ page }) => {
    // Intercept API to delay response
    await page.route("**/api/entities", async (route) => {
      await new Promise((r) => setTimeout(r, 2000));
      await route.continue();
    });
    await page.goto("/dashboard");
    await expect(page.locator('[data-testid="skeleton"]')).toBeVisible();
  });

  test("error states display correctly", async ({ page }) => {
    await page.route("**/api/entities", (route) =>
      route.fulfill({ status: 500, body: JSON.stringify({ error: "Server error" }) })
    );
    await page.goto("/dashboard");
    await expect(page.locator('[role="alert"]')).toBeVisible();
  });

  test("responsive layout", async ({ page }) => {
    // Mobile
    await page.setViewportSize({ width: 375, height: 667 });
    await expect(page.locator("nav")).toBeVisible();
    // Desktop
    await page.setViewportSize({ width: 1280, height: 720 });
    await expect(page.locator("aside")).toBeVisible();
  });
});
```

### 弹出通知验证模板

```typescript
// qa-tests/ui/toasts.validation.spec.ts
import { test, expect } from "@playwright/test";

test.describe("Toast Validation", () => {
  test("success toast appears on entity creation", async ({ page }) => {
    await page.goto("/entities/new");
    await page.fill('[name="name"]', "Test Entity");
    await page.click('button[type="submit"]');

    // Wait for toast (supports sonner, shadcn toast, react-hot-toast)
    const toast = page.locator('[data-sonner-toast], [role="status"], .Toastify__toast');
    await expect(toast).toBeVisible({ timeout: 5000 });
    await expect(toast).toContainText(/created|success/i);
  });

  test("error toast appears on failed submission", async ({ page }) => {
    // Simulate API error
    await page.route("**/api/entities", (route) =>
      route.fulfill({ status: 500, body: JSON.stringify({ error: "Failed" }) })
    );
    await page.goto("/entities/new");
    await page.fill('[name="name"]', "Test");
    await page.click('button[type="submit"]');

    const toast = page.locator('[data-sonner-toast][data-type="error"], .Toastify__toast--error, [role="alert"]');
    await expect(toast).toBeVisible({ timeout: 5000 });
  });

  test("toast auto-dismisses", async ({ page }) => {
    await page.goto("/entities/new");
    await page.fill('[name="name"]', "Test");
    await page.click('button[type="submit"]');
    const toast = page.locator('[data-sonner-toast], [role="status"]');
    await expect(toast).toBeVisible();
    await expect(toast).not.toBeVisible({ timeout: 10000 });
  });

  test("no duplicate toasts on rapid clicks", async ({ page }) => {
    await page.goto("/entities/new");
    await page.fill('[name="name"]', "Test");
    // Rapid double-click
    await page.click('button[type="submit"]');
    await page.click('button[type="submit"]');
    const toasts = page.locator('[data-sonner-toast], [role="status"]');
    const count = await toasts.count();
    expect(count).toBeLessThanOrEqual(1);
  });
});
```

## 第四部分——身份验证流程的验证

### Firebase 身份验证的验证

```typescript
// qa-tests/auth/auth-flows.validation.spec.ts
import { test, expect } from "@playwright/test";

test.describe("Auth Flow Validation", () => {
  test("login with valid credentials redirects to dashboard", async ({ page }) => {
    await page.goto("/login");
    await page.fill('[name="email"]', process.env.TEST_USER_EMAIL!);
    await page.fill('[name="password"]', process.env.TEST_USER_PASSWORD!);
    await page.click('button[type="submit"]');
    await page.waitForURL("/dashboard", { timeout: 10000 });
    expect(page.url()).toContain("/dashboard");
  });

  test("login with invalid credentials shows error", async ({ page }) => {
    await page.goto("/login");
    await page.fill('[name="email"]', "wrong@example.com");
    await page.fill('[name="password"]', "wrongpass");
    await page.click('button[type="submit"]');
    await expect(page.locator('[role="alert"], .error, [data-testid="auth-error"]')).toBeVisible();
    expect(page.url()).toContain("/login");
  });

  test("protected routes redirect unauthenticated users", async ({ page }) => {
    await page.goto("/dashboard");
    await page.waitForURL(/\/(login|auth)/);
  });

  test("logout clears session and redirects", async ({ page }) => {
    // Login first, then logout
    // ...login steps...
    await page.click('[data-testid="logout"], button:has-text("Logout"), button:has-text("Sair")');
    await page.waitForURL(/\/(login|auth|$)/);
    // Verify protected route is no longer accessible
    await page.goto("/dashboard");
    await page.waitForURL(/\/(login|auth)/);
  });
});
```

## 第五部分——LLM 输出质量的验证

### 双层验证方法：基于规则的检查 + LLM-as-Judge

#### 第一层：基于规则的检查（始终优先执行）

```typescript
// qa-tests/llm/rule-based-checks.ts
export interface LLMOutput {
  content: string;
  model: string;
  tokens_used: number;
  latency_ms: number;
}

export interface RuleCheckResult {
  rule: string;
  passed: boolean;
  details: string;
}

export function runRuleBasedChecks(output: LLMOutput, config: {
  maxTokens?: number;
  maxLatencyMs?: number;
  minLength?: number;
  maxLength?: number;
  requiredSections?: string[];
  forbiddenPatterns?: RegExp[];
  requiredFormat?: "json" | "markdown" | "plain";
  language?: string;
}): RuleCheckResult[] {
  const results: RuleCheckResult[] = [];

  // Length checks
  if (config.minLength) {
    results.push({
      rule: "min_length",
      passed: output.content.length >= config.minLength,
      details: `Content length: ${output.content.length}, minimum: ${config.minLength}`,
    });
  }
  if (config.maxLength) {
    results.push({
      rule: "max_length",
      passed: output.content.length <= config.maxLength,
      details: `Content length: ${output.content.length}, maximum: ${config.maxLength}`,
    });
  }

  // Token usage
  if (config.maxTokens) {
    results.push({
      rule: "token_budget",
      passed: output.tokens_used <= config.maxTokens,
      details: `Tokens used: ${output.tokens_used}, budget: ${config.maxTokens}`,
    });
  }

  // Latency
  if (config.maxLatencyMs) {
    results.push({
      rule: "latency",
      passed: output.latency_ms <= config.maxLatencyMs,
      details: `Latency: ${output.latency_ms}ms, max: ${config.maxLatencyMs}ms`,
    });
  }

  // Required sections
  if (config.requiredSections) {
    for (const section of config.requiredSections) {
      results.push({
        rule: `required_section:${section}`,
        passed: output.content.toLowerCase().includes(section.toLowerCase()),
        details: `Section "${section}" ${output.content.toLowerCase().includes(section.toLowerCase()) ? "found" : "missing"}`,
      });
    }
  }

  // Forbidden patterns (PII, hallucination markers, etc.)
  if (config.forbiddenPatterns) {
    for (const pattern of config.forbiddenPatterns) {
      const match = pattern.exec(output.content);
      results.push({
        rule: `forbidden_pattern:${pattern.source}`,
        passed: !match,
        details: match ? `Found forbidden pattern: "${match[0]}"` : "No forbidden patterns found",
      });
    }
  }

  // Format validation
  if (config.requiredFormat === "json") {
    try {
      JSON.parse(output.content);
      results.push({ rule: "valid_json", passed: true, details: "Valid JSON" });
    } catch {
      results.push({ rule: "valid_json", passed: false, details: "Invalid JSON" });
    }
  }

  // Empty/garbage check
  results.push({
    rule: "not_empty",
    passed: output.content.trim().length > 0,
    details: output.content.trim().length === 0 ? "Output is empty" : "Output has content",
  });

  results.push({
    rule: "not_truncated",
    passed: !output.content.endsWith("...") && !output.content.endsWith("…"),
    details: "Check for truncation markers",
  });

  return results;
}
```

#### 第二层：LLM-as-Judge（用于评估内容质量）

```typescript
// qa-tests/llm/llm-judge.ts
export async function llmJudge(
  output: string,
  prompt: string,
  criteria: {
    relevance: boolean;
    accuracy: boolean;
    completeness: boolean;
    tone: boolean;
    safety: boolean;
  }
): Promise<{
  overall_score: number; // 1-5
  criteria_scores: Record<string, number>;
  issues: string[];
  recommendation: "pass" | "review" | "fail";
}> {
  const OPENROUTER_API_KEY = process.env.OPENROUTER_API_KEY;
  if (!OPENROUTER_API_KEY) {
    return {
      overall_score: 0,
      criteria_scores: {},
      issues: ["OPENROUTER_API_KEY not set — skipping LLM judge"],
      recommendation: "review",
    };
  }

  const judgingPrompt = `You are a strict QA evaluator. Assess the following LLM output against the original prompt.

ORIGINAL PROMPT:
${prompt}

LLM OUTPUT:
${output}

Score each criterion from 1 (terrible) to 5 (excellent):
${criteria.relevance ? "- RELEVANCE: Does the output address the prompt?" : ""}
${criteria.accuracy ? "- ACCURACY: Is the information correct and not hallucinated?" : ""}
${criteria.completeness ? "- COMPLETENESS: Does the output cover all requested aspects?" : ""}
${criteria.tone ? "- TONE: Is the tone appropriate for the context?" : ""}
${criteria.safety ? "- SAFETY: Is the content free of harmful, biased, or inappropriate material?" : ""}

Respond in JSON:
{
  "criteria_scores": { "relevance": N, "accuracy": N, ... },
  "overall_score": N,
  "issues": ["list of specific issues found"],
  "recommendation": "pass|review|fail"
}

Rules:
- overall_score < 3 = "fail"
- overall_score >= 3 and < 4 = "review"
- overall_score >= 4 = "pass"
- Any safety score < 3 = automatic "fail"`;

  const response = await fetch("https://openrouter.ai/api/v1/chat/completions", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${OPENROUTER_API_KEY}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      model: "google/gemini-flash-1.5",
      messages: [{ role: "user", content: judgingPrompt }],
      temperature: 0.1,
      response_format: { type: "json_object" },
    }),
  });

  const data = await response.json();
  return JSON.parse(data.choices[0].message.content);
}
```

### LLM 验证测试模板

```typescript
// qa-tests/llm/content-quality.validation.test.ts
import { describe, it, expect } from "vitest";
import { runRuleBasedChecks } from "./rule-based-checks";
import { llmJudge } from "./llm-judge";

describe("LLM Output Quality Validation", () => {
  it("content generation meets quality standards", async () => {
    // 1. Call the actual LLM endpoint
    const res = await fetch(`${BASE_URL}/api/generate`, {
      method: "POST",
      headers: { "Content-Type": "application/json", Authorization: `Bearer ${TOKEN}` },
      body: JSON.stringify({ prompt: "Describe the benefits of remote work" }),
    });
    const output = await res.json();

    // 2. Rule-based checks first
    const ruleResults = runRuleBasedChecks(output, {
      minLength: 100,
      maxLength: 5000,
      maxLatencyMs: 10000,
      forbiddenPatterns: [
        /\b(SSN|social security)\b/i,     // PII
        /\b(as an AI|I cannot)\b/i,         // AI disclosure leaks
        /\b(undefined|null|NaN)\b/,         // Code leaks
      ],
    });
    const ruleFailures = ruleResults.filter((r) => !r.passed);
    expect(ruleFailures).toHaveLength(0);

    // 3. LLM-as-judge for content quality
    const judgment = await llmJudge(output.content, "Describe the benefits of remote work", {
      relevance: true,
      accuracy: true,
      completeness: true,
      tone: true,
      safety: true,
    });
    expect(judgment.recommendation).not.toBe("fail");
    expect(judgment.overall_score).toBeGreaterThanOrEqual(3);
  });
});
```

## 第六部分——集成与工作流程的验证

### Vercel 部署状态的检查

```typescript
// qa-tests/infra/vercel-status.validation.test.ts
describe("Vercel Deployment Validation", () => {
  it("latest deployment is ready", async () => {
    const res = await fetch("https://api.vercel.com/v6/deployments?limit=1", {
      headers: { Authorization: `Bearer ${process.env.VERCEL_TOKEN}` },
    });
    const { deployments } = await res.json();
    expect(deployments[0].state).toBe("READY");
  });

  it("preview deployment matches current branch", async () => {
    // Check that the preview URL for the current PR is live and healthy
  });

  it("environment variables are set", async () => {
    // Verify all required env vars exist in the Vercel project
    // (without reading their values)
  });
});
```

### Supabase 系统健康状况的检查

```typescript
// qa-tests/infra/supabase-health.validation.test.ts
describe("Supabase Health Validation", () => {
  it("database is reachable", async () => {
    const res = await fetch(`${process.env.SUPABASE_URL}/rest/v1/`, {
      headers: {
        apikey: process.env.SUPABASE_ANON_KEY!,
        Authorization: `Bearer ${process.env.SUPABASE_ANON_KEY}`,
      },
    });
    expect(res.status).toBe(200);
  });

  it("auth service is healthy", async () => {
    const res = await fetch(`${process.env.SUPABASE_URL}/auth/v1/health`);
    expect(res.ok).toBe(true);
  });

  it("realtime is connected", async () => {
    // Test WebSocket connection to Supabase Realtime
  });
});
```

## 第七部分——通过/不通过报告的生成

在执行完所有验证步骤后，生成一份全面的报告：

```json
{
  "report": {
    "project": "project-name",
    "version": "x.y.z",
    "date": "ISO-8601",
    "validator": "qa-gate-vercel",
    "verdict": "GO | NO-GO | CONDITIONAL",
    "summary": {
      "total_checks": 45,
      "passed": 42,
      "failed": 2,
      "skipped": 1,
      "pass_rate": "93.3%"
    },
    "sections": {
      "api_routes": {
        "status": "PASS",
        "checks_run": 12,
        "checks_passed": 12,
        "details": []
      },
      "ui_pages": {
        "status": "PASS",
        "checks_run": 8,
        "checks_passed": 8,
        "details": []
      },
      "toast_notifications": {
        "status": "FAIL",
        "checks_run": 6,
        "checks_passed": 4,
        "failures": [
          {
            "test": "no_duplicate_toasts",
            "page": "/entities/new",
            "expected": "single toast on rapid clicks",
            "actual": "2 toasts appeared",
            "severity": "medium",
            "recommendation": "Add debounce to form submission"
          }
        ]
      },
      "auth_flows": {
        "status": "PASS",
        "checks_run": 5,
        "checks_passed": 5
      },
      "llm_quality": {
        "status": "CONDITIONAL",
        "rule_based": { "passed": 8, "failed": 0 },
        "llm_judge": {
          "average_score": 3.8,
          "recommendation": "review",
          "issues": ["Tone slightly too formal for target audience"]
        }
      },
      "database_integrity": {
        "status": "PASS",
        "rls_enforced": true,
        "orphan_records": 0
      },
      "infrastructure": {
        "status": "PASS",
        "vercel_deployment": "READY",
        "supabase_health": "OK"
      }
    },
    "blockers": [
      {
        "id": "BLOCK-001",
        "severity": "high",
        "description": "Duplicate toasts on /entities/new",
        "recommendation": "Fix before production"
      }
    ],
    "warnings": [
      {
        "id": "WARN-001",
        "severity": "low",
        "description": "LLM output tone slightly formal",
        "recommendation": "Review prompt engineering, not blocking"
      }
    ],
    "go_conditions": {
      "all_api_tests_pass": true,
      "all_auth_tests_pass": true,
      "no_high_severity_blockers": false,
      "llm_quality_above_threshold": true,
      "deployment_healthy": true
    }
  }
}
```

### 判断逻辑：

- **通过（GO）**：所有检查均通过，没有阻碍因素，也没有高严重性的错误。
- **不通过（NO-GO）**：存在高严重性的阻碍因素，或者身份验证失败，或者数据完整性出现问题。
- **条件性通过（CONDITIONAL）**：存在中等严重性的问题，但经过相关方批准后可以接受。

将报告保存到 `qa-reports/go-no-go-report.json` 文件中，并同时生成一份人类可阅读的 Markdown 格式报告，保存在 `qa-reports/go-no-go-report.md` 文件中。

## 第八部分——执行流程

代理应按照以下顺序执行各项操作：

```
1. Generate test plan          → qa-reports/test-plan.json
2. Run existing test suite     → npx vitest run (or jest) + npx playwright test
3. Generate validation tests   → qa-tests/**/*.validation.test.ts
4. Run API validations         → qa-tests/api/
5. Run UI/toast validations    → qa-tests/ui/
6. Run auth flow validations   → qa-tests/auth/
7. Run LLM quality validations → qa-tests/llm/
8. Run infra health checks     → qa-tests/infra/
9. Aggregate results           → qa-reports/go-no-go-report.json
10. Generate human report      → qa-reports/go-no-go-report.md
```

### 命令

```bash
# Step 2: Existing tests
npx vitest run --reporter=json --outputFile=qa-reports/vitest-results.json 2>/dev/null || true
npx playwright test --reporter=json --output=qa-reports/playwright-results.json 2>/dev/null || true

# Step 3-7: Validation tests (separate config to avoid mixing with app tests)
npx vitest run --config qa-tests/vitest.config.ts --reporter=json --outputFile=qa-reports/validation-results.json

# Step 8: Playwright validation tests
npx playwright test --config qa-tests/playwright.config.ts --reporter=json --output=qa-reports/playwright-validation-results.json
```

### 验证测试的配置（与应用程序测试分开）

```typescript
// qa-tests/vitest.config.ts
import { defineConfig } from "vitest/config";
import path from "path";

export default defineConfig({
  test: {
    include: ["qa-tests/**/*.validation.test.ts"],
    environment: "node",
    globals: true,
  },
  resolve: {
    alias: { "@": path.resolve(__dirname, "../src") },
  },
});
```

## 最佳实践（必须遵守）

- 在添加新的验证测试之前，务必先运行现有的测试套件。
- 使用独立的目录（`qa-tests/`、`qa-reports/`）以避免干扰应用程序的测试环境。
- 识别并适应项目的测试框架（Vitest/Jest、Playwright/Cypress）。
- 在使用 LLM-as-Judge 之前，先执行基于规则的检查（这样更高效、更快，且能发现明显的问题）。
- 在所有错误报告中标注错误的严重程度（高/中/低）。
- 生成两种格式的报告：JSON（机器可读）和 Markdown（人类可读）。
- 动态检测是否使用了弹出通知库（如 `sonner`、`react-hot-toast`、`shadcntoast`）。
- 在移动设备（375px）、平板电脑（768px）和桌面设备（1280px）上验证应用程序的响应式布局。
- 不仅测试正常情况下的功能，还要测试身份验证错误情况。
- 单独验证 Supabase 的 RLS（这是重要的安全检查）。

## 应避免的错误做法

- 绝不要跳过测试计划的生成步骤。
- 绝不要将验证测试与应用程序测试混在一起（使用单独的配置文件）。
- 绝不要在测试文件中硬编码身份验证令牌——始终使用 `process.env` 来获取这些信息。
- 在执行 LLM-as-Judge 之前，绝不要跳过基于规则的检查（否则会浪费令牌）。
- 绝不要在报告中不记录原因就直接将测试标记为“已跳过”。
- 绝不要自动批准“不通过”的结果——必须将所有阻碍因素都呈现给相关人员。
- 绝不要使用生产数据来进行测试——应使用测试账户和模拟数据。
- 绝不要忽略弹出通知的验证——弹出通知的错误是用户反馈中最常见的问题之一。

## 安全规则

- 绝不要直接读取或修改 `.env`、`.env.local` 或任何凭证文件。
- 所有环境变量的引用都通过 `process.env.*` 在生成的测试代码中实现。
- 在得到“条件性通过”或“不通过”的结果后，绝不要自动部署应用程序。
- 绝不要从生产数据库中删除测试数据。
- 绝不要在测试报告中泄露 API 密钥——在写入磁盘之前必须对敏感信息进行加密处理。
- 如果 `OPENROUTER_API_KEY` 未设置，则跳过 LLM-as-Judge 的验证步骤，并将结果标记为“待审核”。