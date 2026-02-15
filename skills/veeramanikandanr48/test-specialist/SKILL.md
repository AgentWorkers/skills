---
name: test-specialist
description: 此技能适用于编写测试用例、修复漏洞、分析代码中的潜在问题，以及提高 JavaScript/TypeScript 应用程序的测试覆盖率。它可以用于单元测试、集成测试、端到端测试、调试运行时错误、逻辑错误、性能问题、安全漏洞的排查，以及系统的代码分析。
---

# 测试专家

## 概述

运用系统的测试方法和调试技巧来处理 JavaScript/TypeScript 应用程序。该技能提供了全面的测试策略、错误分析框架以及自动化工具，用于识别测试覆盖范围中的遗漏和未测试的代码。

## 核心能力

### 1. 编写测试用例

编写涵盖单元测试、集成测试和端到端测试的全面测试用例。

#### 单元测试方法

使用 AAA 模式（Arrange-Act-Assert）来组织测试：

```typescript
describe('ExpenseCalculator', () => {
  describe('calculateTotal', () => {
    test('sums expense amounts correctly', () => {
      // Arrange
      const expenses = [
        { amount: 100, category: 'food' },
        { amount: 50, category: 'transport' },
        { amount: 25, category: 'entertainment' }
      ];

      // Act
      const total = calculateTotal(expenses);

      // Assert
      expect(total).toBe(175);
    });

    test('handles empty expense list', () => {
      expect(calculateTotal([])).toBe(0);
    });

    test('handles negative amounts', () => {
      const expenses = [
        { amount: 100, category: 'food' },
        { amount: -50, category: 'refund' }
      ];
      expect(calculateTotal(expenses)).toBe(50);
    });
  });
});
```

**关键原则：**
- 每个测试只验证一个功能
- 覆盖正常情况、边界情况和错误条件
- 使用能描述测试场景的描述性测试名称
- 保持测试的独立性和隔离性

#### 集成测试方法

测试组件之间的协作，包括数据库、API 和服务的交互：

```typescript
describe('ExpenseAPI Integration', () => {
  beforeAll(async () => {
    await database.connect(TEST_DB_URL);
  });

  afterAll(async () => {
    await database.disconnect();
  });

  beforeEach(async () => {
    await database.clear();
    await seedTestData();
  });

  test('POST /expenses creates expense and updates total', async () => {
    const response = await request(app)
      .post('/api/expenses')
      .send({
        amount: 50,
        category: 'food',
        description: 'Lunch'
      })
      .expect(201);

    expect(response.body).toMatchObject({
      id: expect.any(Number),
      amount: 50,
      category: 'food'
    });

    // Verify database state
    const total = await getTotalExpenses();
    expect(total).toBe(50);
  });
});
```

#### 端到端测试方法

使用 Playwright 或 Cypress 等工具测试完整的用户工作流程：

```typescript
test('user can track expense from start to finish', async ({ page }) => {
  // Navigate to app
  await page.goto('/');

  // Add new expense
  await page.click('[data-testid="add-expense-btn"]');
  await page.fill('[data-testid="amount"]', '50.00');
  await page.selectOption('[data-testid="category"]', 'food');
  await page.fill('[data-testid="description"]', 'Lunch');
  await page.click('[data-testid="submit"]');

  // Verify expense appears in list
  await expect(page.locator('[data-testid="expense-item"]')).toContainText('Lunch');
  await expect(page.locator('[data-testid="total"]')).toContainText('$50.00');
});
```

### 2. 系统化错误分析

应用结构化的调试方法来识别和修复问题。

#### 五步分析流程

1. **重现问题**：可靠地重现错误
   - 记录触发错误的具体步骤
   - 确定所需的环境/状态
   - 记录预期行为与实际行为

2. **定位问题**：缩小问题范围
   - 逐步排查代码路径
   - 创建最小化的重现场景
   - 移除无关的依赖项

3. **根本原因分析**：确定问题的根本原因
   - 跟踪执行流程
   - 检查假设和前提条件
   - 查看最近的代码更改（使用 git blame）

4. **修复实现**：实施解决方案
   - 先编写失败的测试用例（TDD）
   - 实施修复
   - 验证测试是否通过

5. **验证**：确保修复后的代码质量
   - 运行完整的测试套件
   - 测试边界情况
   - 确认没有出现回归问题

#### 常见错误类型

**竞态条件：**
```typescript
// Test concurrent operations
test('handles concurrent updates correctly', async () => {
  const promises = Array.from({ length: 100 }, () =>
    incrementExpenseCount()
  );

  await Promise.all(promises);
  expect(getExpenseCount()).toBe(100);
});
```

**空/未定义值错误：**
```typescript
// Test null safety
test.each([null, undefined, '', 0, false])
  ('handles invalid input: %p', (input) => {
    expect(() => processExpense(input)).toThrow('Invalid expense');
  });
```

**数值错误：**
```typescript
// Test boundaries explicitly
describe('pagination', () => {
  test('handles empty list', () => {
    expect(paginate([], 1, 10)).toEqual([]);
  });

  test('handles single item', () => {
    expect(paginate([item], 1, 10)).toEqual([item]);
  });

  test('handles last page with partial items', () => {
    const items = Array.from({ length: 25 }, (_, i) => i);
    expect(paginate(items, 3, 10)).toHaveLength(5);
  });
});
```

### 3. 主动识别潜在问题

在问题变成错误之前主动发现它们。

#### 安全漏洞

测试常见的安全问题：

```typescript
describe('security', () => {
  test('prevents SQL injection', async () => {
    const malicious = "'; DROP TABLE expenses; --";
    await expect(
      searchExpenses(malicious)
    ).resolves.not.toThrow();
  });

  test('sanitizes XSS in descriptions', () => {
    const xss = '<script>alert("xss")</script>';
    const expense = createExpense({ description: xss });
    expect(expense.description).not.toContain('<script>');
  });

  test('requires authentication for expense operations', async () => {
    await request(app)
      .post('/api/expenses')
      .send({ amount: 50 })
      .expect(401);
  });
});
```

#### 性能问题

测试性能问题：

```typescript
test('processes large expense list efficiently', () => {
  const largeList = Array.from({ length: 10000 }, (_, i) => ({
    amount: i,
    category: 'test'
  }));

  const start = performance.now();
  const total = calculateTotal(largeList);
  const duration = performance.now() - start;

  expect(duration).toBeLessThan(100); // Should complete in <100ms
  expect(total).toBe(49995000);
});
```

#### 逻辑错误

使用参数化测试来捕获边界情况：

```typescript
test.each([
  // [input, expected, description]
  [[10, 20, 30], 60, 'normal positive values'],
  [[0, 0, 0], 0, 'all zeros'],
  [[-10, 20, -5], 5, 'mixed positive and negative'],
  [[0.1, 0.2], 0.3, 'decimal precision'],
  [[Number.MAX_SAFE_INTEGER], Number.MAX_SAFE_INTEGER, 'large numbers'],
])('calculateTotal(%p) = %p (%s)', (amounts, expected, description) => {
  const expenses = amounts.map(amount => ({ amount, category: 'test' }));
  expect(calculateTotal(expenses)).toBeCloseTo(expected);
});
```

### 4. 测试覆盖范围分析

使用自动化工具来识别测试覆盖范围中的遗漏。

#### 查找未测试的代码

运行提供的脚本来识别没有测试的源文件：

```bash
python3 scripts/find_untested_code.py src
```

该脚本将：
- 扫描源代码目录中的所有文件
- 识别缺少相应测试文件的文件
- 按类型（组件、服务、工具等）对未测试的文件进行分类
- 优先处理需要测试的文件

**解释：**
- **API/服务**：高优先级 - 测试业务逻辑和数据操作
- **模型**：高优先级 - 测试数据验证和转换
- **钩子**：中等优先级 - 测试状态相关的行为
- **组件**：中等优先级 - 测试复杂的 UI 逻辑
- **工具**：低优先级 - 根据需要测试复杂的功能

#### 分析覆盖范围报告

在生成测试覆盖报告后运行该脚本：

```bash
# Generate coverage (using Jest example)
npm test -- --coverage

# Analyze coverage gaps
python3 scripts/analyze_coverage.py coverage/coverage-final.json
```

该脚本会识别：
- 覆盖率低于阈值的文件（默认为 80%）
- 语句、分支和函数的覆盖率
- 需要优先改进的文件

**覆盖目标：**
- 关键路径：90% 以上的覆盖率
- 业务逻辑：85% 以上的覆盖率
- UI 组件：75% 以上的覆盖率
- 工具：70% 以上的覆盖率

### 5. 测试维护和质量

确保测试代码具有价值且易于维护。

#### 测试代码质量原则

**DRY（不要重复自己）：**
```typescript
// Extract common setup
function createTestExpense(overrides = {}) {
  return {
    amount: 50,
    category: 'food',
    description: 'Test expense',
    date: new Date('2024-01-01'),
    ...overrides
  };
}

test('filters by category', () => {
  const expenses = [
    createTestExpense({ category: 'food' }),
    createTestExpense({ category: 'transport' }),
  ];
  // ...
});
```

**清晰的测试数据：**
```typescript
// Bad: Magic numbers
expect(calculateDiscount(100, 0.15)).toBe(85);

// Good: Named constants
const ORIGINAL_PRICE = 100;
const DISCOUNT_RATE = 0.15;
const EXPECTED_PRICE = 85;
expect(calculateDiscount(ORIGINAL_PRICE, DISCOUNT_RATE)).toBe(EXPECTED_PRICE);
```

**避免测试之间的依赖**：
```typescript
// Bad: Tests depend on execution order
let sharedState;
test('test 1', () => {
  sharedState = { value: 1 };
});
test('test 2', () => {
  expect(sharedState.value).toBe(1); // Depends on test 1
});

// Good: Independent tests
test('test 1', () => {
  const state = { value: 1 };
  expect(state.value).toBe(1);
});
test('test 2', () => {
  const state = { value: 1 };
  expect(state.value).toBe(1);
});
```

## 工作流程决策树

按照以下决策树来确定测试方法：

1. **添加新功能？**
   - 是 → 先编写测试用例（TDD）
     - 编写失败的测试用例
     - 实现功能
     - 验证测试是否通过
     - 重构代码
   - 否 → 转到步骤 2

2. **修复错误？**
   - 是 → 应用错误分析流程
     - 重现错误
     - 编写失败的测试用例
     - 修复代码
     - 验证测试是否通过
   - 否 → 转到步骤 3

3. **提高测试覆盖范围？**
   - 是 → 使用覆盖范围工具
     - 运行 `find_untested_code.py` 来识别遗漏的测试用例
     - 运行 `analyze_coverage.py` 分析覆盖报告
     - 优先处理关键路径
     - 为未测试的代码编写测试用例
   - 否 → 转到步骤 4

4. **分析代码质量？**
   - 是 → 进行系统化审查
     - 检查安全漏洞
     - 测试边界情况和错误处理
     - 验证性能
     - 审查错误处理机制

## 测试框架和工具

### 推荐的工具栈

**单元/集成测试：**
- 使用 Jest 或 Vitest 作为测试运行器
- 用于 React 组件的测试库
- 使用 Supertest 进行 API 测试
- 使用 MSW（Mock Service Worker）进行 API 模拟

**端到端测试：**
- 使用 Playwright 或 Cypress
- 使用 Page Object Model 模式

**覆盖范围分析：**
- 使用 Istanbul（内置在 Jest/Vitest 中）
- 以 JSON 格式生成覆盖范围报告

### 运行测试

```bash
# Run all tests
npm test

# Run with coverage
npm test -- --coverage

# Run specific test file
npm test -- ExpenseCalculator.test.ts

# Run in watch mode
npm test -- --watch

# Run E2E tests
npm run test:e2e
```

## 参考文档

有关详细的测试模式和技术，请参考：

- `references/testing_patterns.md` - 全面的测试模式、最佳实践和代码示例
- `references/bug_analysis.md` - 深入的错误分析框架、常见错误类型和调试技巧

这些参考文档包含了丰富的示例和高级技术。在以下情况下请查阅它们：
- 处理复杂的测试场景时
- 需要特定模式的实现时
- 调试异常问题时
- 寻求特定情况下的最佳实践时

## 脚本

### analyze_coverage.py

分析 Jest/Istanbul 的覆盖范围报告以识别覆盖范围中的遗漏：

```bash
python3 scripts/analyze_coverage.py [coverage-file]
```

如果未指定，该脚本会自动查找常见的覆盖范围文件位置。

**输出：**
- 覆盖率低于阈值的文件
- 语句、分支和函数的覆盖率
- 需要优先改进的文件

### find_untested_code.py

查找没有测试文件的源代码：

```bash
python3 scripts/find_untested_code.py [src-dir] [--pattern test|spec]
```

**输出：**
- 源文件和测试文件的总数
- 测试文件的覆盖率
- 按类型（API、服务、组件等）分类的未测试文件
- 改进的优先级建议

## 最佳实践总结

1. **添加新功能时**：先编写测试用例（TDD）
2. **测试行为，而不是实现** - 测试用例应能在重构后仍然有效
3. **保持测试的独立性** - 测试之间不应有共享的状态
4. **使用描述性名称** - 测试名称应能清晰地描述测试场景
5. **覆盖边界情况** - 包括空值、空对象、边界值和错误条件
6. **模拟外部依赖** - 测试应快速且可靠
7. **保持高覆盖率** - 关键代码的覆盖率应达到 80% 以上
8. **立即修复失败的测试** - 绝不要提交有错误的测试代码
9. **重构测试代码** - 保持与生产代码相同的质量标准
10. **使用工具** - 自动化覆盖范围分析和问题识别