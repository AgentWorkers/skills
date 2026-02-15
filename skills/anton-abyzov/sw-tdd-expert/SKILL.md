---
name: tdd-expert
description: **测试驱动开发（Test-Driven Development, TDD）专家**  
在实施测试驱动开发（TDD）工作流程、红-绿-重构（red-green-refactor）模式，或优先编写测试代码时，可依赖该专家的专业知识。
---

# 驱动测试开发（TDD）专家

**适用于任何用户项目的独立TDD专业知识。**

---

## TDD循环：红-绿-重构

### 1. 红色阶段（RED）：编写失败的测试用例

**目标**：通过一个失败的测试用例来定义预期的行为

```typescript
import { describe, it, expect } from 'vitest';
import { Calculator } from './Calculator';

describe('Calculator', () => {
  it('should add two numbers', () => {
    const calculator = new Calculator();
    expect(calculator.add(2, 3)).toBe(5); // WILL FAIL - Calculator doesn't exist
  });
});
```

**红色阶段检查清单**：
- [ ] 测试用例仅描述一个具体的行为
- [ ] 测试用例因正确的原因而失败（而非语法错误）
- [ ] 测试用例的名称清晰易懂
- [ ] 预期的行为明确无误

### 2. 绿色阶段（GREEN）：实现最小功能

**目标**：编写最简短的代码以使测试通过

```typescript
// Calculator.ts
export class Calculator {
  add(a: number, b: number): number {
    return a + b; // Minimal implementation
  }
}
```

**绿色阶段检查清单**：
- [ ] 测试用例通过
- [ ] 代码尽可能简洁
- [ ] 避免过早优化
- [ ] 不添加额外的功能

### 3. 重构阶段（REFactor）：改进代码设计

**目标**：在不改变代码行为的情况下提升代码质量

```typescript
// Refactor: Support variable arguments
export class Calculator {
  add(...numbers: number[]): number {
    return numbers.reduce((sum, n) => sum + n, 0);
  }
}

// Tests still pass!
```

**重构阶段检查清单**：
- [ ] 所有测试用例仍然通过
- [ ] 代码更易阅读
- [ ] 删除重复代码
- [ ] 采用更好的设计模式

---

## TDD的优势

**设计方面的优势**：
- 强制代码模块化、易于测试
- 可及早发现设计问题
- 有助于遵循SOLID设计原则
- 促进简洁的解决方案

**质量方面的优势**：
- 100%的代码覆盖率（这是TDD的基本要求）
- 测试用例记录了代码的行为
- 提供了防止回归问题的保障
- 编译速度更快

**生产力方面的优势**：
- 减少调试时间
- 有信心进行代码重构
- 迭代周期更短
- 需求更加明确

---

## 行为驱动开发（BDD）

**基于自然语言的TDD扩展**

### 给定-当-然后（Given-When-Then）模式

```typescript
describe('Shopping Cart', () => {
  it('should apply 10% discount when total exceeds $100', () => {
    // Given: A cart with $120 worth of items
    const cart = new ShoppingCart();
    cart.addItem({ price: 120, quantity: 1 });

    // When: Getting the total
    const total = cart.getTotal();

    // Then: 10% discount applied
    expect(total).toBe(108); // $120 - $12 (10%)
  });
});
```

**BDD的优势**：
- 非开发人员也能理解测试用例
- 业务需求更加清晰
- 有助于改善与利益相关者的沟通
- 提供可执行的规范

---

## TDD模式

### 模式1：测试用例列表

在编码之前，列出所有需要的测试用例：

```markdown
Calculator Tests:
- [ ] add two positive numbers
- [ ] add negative numbers
- [ ] add zero
- [ ] add multiple numbers
- [ ] multiply two numbers
- [ ] divide two numbers
- [ ] divide by zero (error)
```

逐一实现这些测试用例。

### 模式2：先假设计划，再逐步完善

**步骤**：
- 先使用硬编码的返回值进行测试
- 之后逐步将代码泛化

```typescript
// Test 1: add(2, 3) = 5
add(a, b) { return 5; } // Hardcoded!

// Test 2: add(5, 7) = 12
add(a, b) { return a + b; } // Generalized
```

### 模式3：三角测量法（Triangulation）

**步骤**：
- 使用多个测试用例来推动代码的泛化

```typescript
// Test 1
expect(fizzbuzz(3)).toBe('Fizz');

// Test 2
expect(fizzbuzz(5)).toBe('Buzz');

// Test 3
expect(fizzbuzz(15)).toBe('FizzBuzz');

// Forces complete implementation
```

### 模式4：测试数据生成器

**步骤**：
- 为复杂的对象创建测试辅助工具

```typescript
class UserBuilder {
  private user = { name: 'Test', email: 'test@example.com', role: 'user' };

  withName(name: string) {
    this.user.name = name;
    return this;
  }

  withRole(role: string) {
    this.user.role = role;
    return this;
  }

  build() {
    return this.user;
  }
}

// Usage
const admin = new UserBuilder().withRole('admin').build();
```

---

## 自信地进行重构

**TDD的安全保障**

### 重构类型

**1. 提取方法（Extract Method）**：
```typescript
// Before
function processOrder(order) {
  const total = order.items.reduce((sum, item) => sum + item.price, 0);
  const tax = total * 0.1;
  return total + tax;
}

// After (refactored with test safety)
function calculateTotal(items) {
  return items.reduce((sum, item) => sum + item.price, 0);
}

function calculateTax(total) {
  return total * 0.1;
}

function processOrder(order) {
  const total = calculateTotal(order.items);
  const tax = calculateTax(total);
  return total + tax;
}
```

**2. 删除重复代码（Remove Duplication）**：
```typescript
// Tests force you to see duplication
it('should validate email', () => {
  expect(validateEmail('test@example.com')).toBe(true);
  expect(validateEmail('invalid')).toBe(false);
});

it('should validate phone', () => {
  expect(validatePhone('+1-555-0100')).toBe(true);
  expect(validatePhone('invalid')).toBe(false);
});

// Extract common validation pattern
```

### 重构工作流程

```
1. All tests GREEN? → Continue
2. Identify code smell
3. Make small refactoring
4. Run tests → GREEN? → Continue
5. Repeat until satisfied
6. Commit
```

---

## TDD的常见误区

### ❌ 测试实现细节
**误区**：不应该在测试中关注代码的具体实现细节

```typescript
// BAD: Testing private method
it('should call _validateEmail internally', () => {
  spyOn(service, '_validateEmail');
  service.createUser({ email: 'test@example.com' });
  expect(service._validateEmail).toHaveBeenCalled();
});

// GOOD: Testing behavior
it('should reject invalid email', () => {
  expect(() => service.createUser({ email: 'invalid' }))
    .toThrow('Invalid email');
});
```

### ❌ 在代码编写完成后才编写测试用例
**误区**：应该先编写测试用例，再编写代码

### ❌ 过长的测试用例
**误区**：测试用例不应超过20行

### ❌ 跳过重构阶段
**误区**：重构是TDD流程中的重要环节

---

## 基于模拟的TDD（Mock-Driven TDD）

**在处理外部依赖时**

### 策略1：依赖注入（Dependency Injection）
**步骤**：
- 使用依赖注入来模拟外部依赖

### 策略2：基于接口的模拟（Interface-Based Mocking）
**步骤**：
- 通过接口来模拟外部组件

---

## 通过TDD实践SOLID设计原则

**TDD自然地引导我们遵循SOLID设计原则**

### 单一职责原则（Single Responsibility Principle, SRP）：
**示例**：测试可以帮助我们发现类职责过重的情况

```typescript
// Many tests for one class? Split it!
describe('UserManager', () => {
  // 20+ tests here → Too many responsibilities
});

// Refactor to multiple classes
describe('UserCreator', () => { /* 5 tests */ });
describe('UserValidator', () => { /* 5 tests */ });
describe('UserNotifier', () => { /* 5 tests */ });
```

### 开闭原则（Open-Closed Principle, OCP）：
**示例**：测试使得代码易于扩展

```typescript
// Testable, extensible design
interface PaymentProcessor {
  process(amount: number): Promise<void>;
}

class StripeProcessor implements PaymentProcessor { }
class PayPalProcessor implements PaymentProcessor { }
```

### 依赖倒置原则（Dependency Inversion Principle, DIP）：
**示例**：TDD要求我们使用依赖注入来管理依赖关系

---

## 快速参考

### TDD工作流程
```
1. Write test (RED) → Fails ✅
2. Minimal code (GREEN) → Passes ✅
3. Refactor → Still passes ✅
4. Repeat
```

### 测试用例的常见问题：
- 测试用例过长（超过20行）
- 同时包含多个断言（超过3个）
- 测试用例关注实现细节
- 测试用例名称不明确
- 测试执行时间过长（超过100毫秒）
- 测试用例不稳定（容易出错）

### 何时使用TDD：
- 新功能的开发
- 修复错误（先编写测试用例）
- 代码重构
- 复杂逻辑的处理
- 公共API的实现

**注意**：TDD适用于任何用户项目，是不可或缺的开发技能。