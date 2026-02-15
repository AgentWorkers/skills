---
name: senior-qa
description: 当用户请求“生成测试用例”、“编写单元测试”、“分析测试覆盖率”、“搭建端到端测试框架”、“配置 Playwright”、“配置 Jest”、“实现测试模式”或“提高测试质量”时，应使用此技能。该技能适用于使用 Jest、React Testing Library 和 Playwright 进行 React/Next.js 应用程序的测试工作。
---

# 高级质量保证工程师

负责 React 和 Next.js 应用程序的测试自动化、代码覆盖率分析以及质量保证工作。

## 目录

- [快速入门](#quick-start)
- [工具概述](#tools-overview)
  - [测试套件生成器](#1-test-suite-generator)
  - [代码覆盖率分析工具](#2-coverage-analyzer)
  - [端到端测试框架](#3-e2e-test-scaffolder)
- [质量保证工作流程](#qa-workflows)
  - [单元测试生成流程](#unit-test-generation-workflow)
  - [代码覆盖率分析流程](#coverage-analysis-workflow)
  - [端到端测试设置流程](#e2e-test-setup-workflow)
- [参考文档](#reference-documentation)
- [常见模式快速参考](#common-patterns-quick-reference)

---

## 快速入门

```bash
# Generate Jest test stubs for React components
python scripts/test_suite_generator.py src/components/ --output __tests__/

# Analyze test coverage from Jest/Istanbul reports
python scripts/coverage_analyzer.py coverage/coverage-final.json --threshold 80

# Scaffold Playwright E2E tests for Next.js routes
python scripts/e2e_test_scaffolder.py src/app/ --output e2e/
```

---

## 工具概述

### 1. 测试套件生成器

扫描 React/TypeScript 组件，并生成结构规范的 Jest + React Testing Library 测试代码。

**输入：** 包含 React 组件的源代码目录
**输出：** 包含描述性代码（describe）、渲染测试和交互测试的测试文件

**使用方法：**
```bash
# Basic usage - scan components and generate tests
python scripts/test_suite_generator.py src/components/ --output __tests__/

# Output:
# Scanning: src/components/
# Found 24 React components
#
# Generated tests:
#   __tests__/Button.test.tsx (render, click handler, disabled state)
#   __tests__/Modal.test.tsx (render, open/close, keyboard events)
#   __tests__/Form.test.tsx (render, validation, submission)
#   ...
#
# Summary: 24 test files, 87 test cases

# Include accessibility tests
python scripts/test_suite_generator.py src/ --output __tests__/ --include-a11y

# Generate with custom template
python scripts/test_suite_generator.py src/ --template custom-template.tsx
```

**支持的模式：**
- 使用 hooks 的函数组件
- 使用 Context 提供者的组件
- 需要获取数据的组件
- 需要验证数据的表单组件

---

### 2. 代码覆盖率分析工具

解析 Jest/Istanbul 的代码覆盖率报告，识别覆盖率不足的部分，并提供改进建议。

**输入：** 代码覆盖率报告（JSON 或 LCOV 格式）
**输出：** 带有改进建议的覆盖率分析结果

**使用方法：**
```bash
# Analyze coverage report
python scripts/coverage_analyzer.py coverage/coverage-final.json

# Output:
# === Coverage Analysis Report ===
# Overall: 72.4% (target: 80%)
#
# BY TYPE:
#   Statements: 74.2%
#   Branches: 68.1%
#   Functions: 71.8%
#   Lines: 73.5%
#
# CRITICAL GAPS (uncovered business logic):
#   src/services/payment.ts:45-67 - Payment processing
#   src/hooks/useAuth.ts:23-41 - Authentication flow
#
# RECOMMENDATIONS:
#   1. Add tests for payment service error handling
#   2. Cover authentication edge cases
#   3. Test form validation branches
#
# Files below threshold (80%):
#   src/components/Checkout.tsx: 45%
#   src/services/api.ts: 62%

# Enforce threshold (exit 1 if below)
python scripts/coverage_analyzer.py coverage/ --threshold 80 --strict

# Generate HTML report
python scripts/coverage_analyzer.py coverage/ --format html --output report.html
```

---

### 3. 端到端测试框架

扫描 Next.js 的页面或应用目录，生成包含常见交互操作的 Playwright 测试代码。

**输入：** Next.js 的页面或应用目录
**输出：** 按路由组织的 Playwright 测试文件

**使用方法：**
```bash
# Scaffold E2E tests for Next.js App Router
python scripts/e2e_test_scaffolder.py src/app/ --output e2e/

# Output:
# Scanning: src/app/
# Found 12 routes
#
# Generated E2E tests:
#   e2e/home.spec.ts (navigation, hero section)
#   e2e/auth/login.spec.ts (form submission, validation)
#   e2e/auth/register.spec.ts (registration flow)
#   e2e/dashboard.spec.ts (authenticated routes)
#   e2e/products/[id].spec.ts (dynamic routes)
#   ...
#
# Generated: playwright.config.ts
# Generated: e2e/fixtures/auth.ts

# Include Page Object Model classes
python scripts/e2e_test_scaffolder.py src/app/ --output e2e/ --include-pom

# Generate for specific routes
python scripts/e2e_test_scaffolder.py src/app/ --routes "/login,/dashboard,/checkout"
```

---

## 质量保证工作流程

### 单元测试生成流程

用于为新组件或现有组件设置测试。

**步骤 1：扫描项目中未测试的组件**
```bash
python scripts/test_suite_generator.py src/components/ --scan-only
```

**步骤 2：生成测试代码**
```bash
python scripts/test_suite_generator.py src/components/ --output __tests__/
```

**步骤 3：审查并自定义生成的测试代码**
```typescript
// __tests__/Button.test.tsx (generated)
import { render, screen, fireEvent } from '@testing-library/react';
import { Button } from '../src/components/Button';

describe('Button', () => {
  it('renders with label', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByRole('button', { name: /click me/i })).toBeInTheDocument();
  });

  it('calls onClick when clicked', () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Click</Button>);
    fireEvent.click(screen.getByRole('button'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  // TODO: Add your specific test cases
});
```

**步骤 4：运行测试并检查覆盖率**
```bash
npm test -- --coverage
python scripts/coverage_analyzer.py coverage/coverage-final.json
```

---

### 代码覆盖率分析流程

用于提高测试覆盖率或为发布做准备。

**步骤 1：生成代码覆盖率报告**
```bash
npm test -- --coverage --coverageReporters=json
```

**步骤 2：分析覆盖率不足的部分**
```bash
python scripts/coverage_analyzer.py coverage/coverage-final.json --threshold 80
```

**步骤 3：识别关键代码路径**
```bash
python scripts/coverage_analyzer.py coverage/ --critical-paths
```

**步骤 4：生成缺失的测试代码**
```bash
python scripts/test_suite_generator.py src/ --uncovered-only --output __tests__/
```

**步骤 5：验证测试效果的改进**
```bash
npm test -- --coverage
python scripts/coverage_analyzer.py coverage/ --compare previous-coverage.json
```

---

### 端到端测试设置流程

用于为 Next.js 项目配置 Playwright 测试框架。

**步骤 1：（如果未安装）初始化 Playwright**
```bash
npm init playwright@latest
```

**步骤 2：根据路由生成端到端测试代码**
```bash
python scripts/e2e_test_scaffolder.py src/app/ --output e2e/
```

**步骤 3：配置认证相关的测试环境**
```typescript
// e2e/fixtures/auth.ts (generated)
import { test as base } from '@playwright/test';

export const test = base.extend({
  authenticatedPage: async ({ page }, use) => {
    await page.goto('/login');
    await page.fill('[name="email"]', 'test@example.com');
    await page.fill('[name="password"]', 'password');
    await page.click('button[type="submit"]');
    await page.waitForURL('/dashboard');
    await use(page);
  },
});
```

**步骤 4：运行端到端测试**
```bash
npx playwright test
npx playwright show-report
```

**步骤 5：将测试集成到持续集成（CI）流程中**
```yaml
# .github/workflows/e2e.yml
- name: Run E2E tests
  run: npx playwright test
- name: Upload report
  uses: actions/upload-artifact@v3
  with:
    name: playwright-report
    path: playwright-report/
```

---

## 参考文档

| 文件 | 内容 | 使用场景 |
|------|----------|----------|
| `references/testing_strategies.md` | 测试策略、测试类型、覆盖率目标、持续集成/持续部署（CI/CD）集成 | 设计测试策略 |
| `references/test_automation_patterns.md` | 页面对象模型（Page Object Model, POM）、模拟（Mocking, MSW）、测试用例固定装置（Fixtures）、异步测试模式 | 编写测试代码 |
| `references/qa_best_practices.md` | 可测试的代码、易出错的测试（Flaky Tests）、调试方法、质量指标 | 提高测试质量 |

---

## 常见模式快速参考

### React Testing Library 的常用查询方法

```typescript
// Preferred (accessible)
screen.getByRole('button', { name: /submit/i })
screen.getByLabelText(/email/i)
screen.getByPlaceholderText(/search/i)

// Fallback
screen.getByTestId('custom-element')
```

### 异步测试

```typescript
// Wait for element
await screen.findByText(/loaded/i);

// Wait for removal
await waitForElementToBeRemoved(() => screen.queryByText(/loading/i));

// Wait for condition
await waitFor(() => {
  expect(mockFn).toHaveBeenCalled();
});
```

### 使用 MSW 进行模拟

```typescript
import { rest } from 'msw';
import { setupServer } from 'msw/node';

const server = setupServer(
  rest.get('/api/users', (req, res, ctx) => {
    return res(ctx.json([{ id: 1, name: 'John' }]));
  })
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

### Playwright 的定位器（Locators）

```typescript
// Preferred
page.getByRole('button', { name: 'Submit' })
page.getByLabel('Email')
page.getByText('Welcome')

// Chaining
page.getByRole('listitem').filter({ hasText: 'Product' })
```

### Jest 配置文件（jest.config.js）中的覆盖率阈值设置

```javascript
module.exports = {
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80,
    },
  },
};
```

---

## 常用命令

```bash
# Jest
npm test                           # Run all tests
npm test -- --watch                # Watch mode
npm test -- --coverage             # With coverage
npm test -- Button.test.tsx        # Single file

# Playwright
npx playwright test                # Run all E2E tests
npx playwright test --ui           # UI mode
npx playwright test --debug        # Debug mode
npx playwright codegen             # Generate tests

# Coverage
npm test -- --coverage --coverageReporters=lcov,json
python scripts/coverage_analyzer.py coverage/coverage-final.json
```