---
name: testing-patterns
model: standard
category: testing
description: 单元测试、集成测试以及端到端（E2E）测试的实践模式，附带针对特定测试框架的指导建议。当需要“编写测试用例”、“增加测试覆盖率”、“制定测试策略”、“测试某个功能”、“创建测试套件”、“修复频繁出错的测试用例”或“提升测试质量”时，请参考这些指南。
version: 1.0
---

# 测试模式

> **编写能够捕获错误的测试，而不仅仅是通过测试的测试。** — 通过测试覆盖率来建立信心，通过隔离来提高测试效率。

---

## 测试金字塔

| 级别 | 比例 | 速度 | 成本 | 信心 | 覆盖范围 |
|-------|-------|-------|------|------------|-------|
| **单元测试** | 约70% | 毫秒级 | 低 | 低（隔离良好） | 单个函数/类 |
| **集成测试** | 约20% | 秒级 | 中等 | 中等 | 模块边界、API、数据库 |
| **端到端测试** | 约10% | 分钟级 | 高 | 高（模拟实际使用场景） | 完整的用户工作流程 |

> **规则：** 如果你的端到端测试数量超过单元测试数量，那么请反转这个金字塔的结构。

---

## 单元测试模式

### 核心模式

| 模式 | 使用时机 | 结构 |
|---------|------------|-----------|
| **Arrange-Act-Assert** | 所有单元测试的默认结构 | 设置（Setup）、执行（Act）、验证（Assert） |
| **Given-When-Then** | 基于行为驱动的开发（BDD）风格 | 前提条件（Given）、操作（When）、结果（Then） |
| **参数化测试** | 同一逻辑，多种输入 | 数据驱动的测试用例 |
| **快照测试** | UI组件、序列化输出 | 与保存的基线进行比较 |
| **基于属性的测试** | 数学不变量 | 生成随机输入，验证属性是否正确 |

### Arrange-Act-Assert（AAA）

这是每个单元测试的默认结构。将设置、执行和验证明确分开，使测试易于阅读和维护。

```typescript
// Clean AAA structure
test('calculates order total with tax', () => {
  // Arrange
  const items = [{ price: 10, qty: 2 }, { price: 5, qty: 1 }];
  const taxRate = 0.08;

  // Act
  const total = calculateTotal(items, taxRate);

  // Assert
  expect(total).toBe(27.0);
});
```

### 测试替身（Test Doubles）

根据具体情况选择合适的测试替身。每种替身都有其特定的用途。

| 替身类型 | 用途 | 使用时机 | 示例 |
|--------|---------|-------------|---------|
| **存根（Stub）** | 返回预设数据 | 控制间接输入 | `jest.fn().mockReturnValue(42)` |
| **模拟（Mock）** | 验证函数调用 | 确认函数是否被调用 | `expect(mock).toHaveBeenCalledWith('arg')` |
| **间谍（Spy）** | 包装真实实现 | 观察而不替换真实实现 | `jest.spyOn(service, 'save')` |
| **伪造对象（Fake）** | 简化的模拟实现 | 需要模拟真实行为 | 内存数据库、伪造的HTTP服务器 |

```typescript
// Stub — control indirect input
const getUser = jest.fn().mockResolvedValue({ id: 1, name: 'Alice' });

// Spy — observe without replacing
const spy = jest.spyOn(logger, 'warn');
processInvalidInput(data);
expect(spy).toHaveBeenCalledWith('Invalid input received');

// Fake — lightweight substitute
class FakeUserRepo implements UserRepository {
  private users = new Map<string, User>();
  async save(user: User) { this.users.set(user.id, user); }
  async findById(id: string) { return this.users.get(id) ?? null; }
}
```

### 参数化测试

当相同的逻辑需要用多种输入进行验证时，使用参数化测试。这样可以避免重复编写测试代码，并实现全面的测试覆盖。

```typescript
// Vitest/Jest
test.each([
  ['hello', 'HELLO'],
  ['world', 'WORLD'],
  ['', ''],
  ['123abc', '123ABC'],
])('toUpperCase(%s) returns %s', (input, expected) => {
  expect(input.toUpperCase()).toBe(expected);
});
```

```python
# pytest
@pytest.mark.parametrize("input,expected", [
    ("hello", "HELLO"),
    ("world", "WORLD"),
    ("", ""),
])
def test_to_upper(input, expected):
    assert input.upper() == expected
```

```go
// Go — table-driven tests (idiomatic)
func TestAdd(t *testing.T) {
    tests := []struct {
        name     string
        a, b     int
        expected int
    }{
        {"positive", 2, 3, 5},
        {"zero", 0, 0, 0},
        {"negative", -1, -2, -3},
    }
    for _, tc := range tests {
        t.Run(tc.name, func(t *testing.T) {
            if got := Add(tc.a, tc.b); got != tc.expected {
                t.Errorf("Add(%d,%d) = %d, want %d", tc.a, tc.b, got, tc.expected)
            }
        })
    }
}
```

---

## 集成测试模式

### 数据库测试策略

| 策略 | 方法 | 权衡 |
|----------|----------|-----------|
| **事务回滚** | 将每个测试包裹在事务中，测试完成后回滚 | 快速，但可能掩盖提交相关的错误 |
| **测试固定数据（Fixtures）** | 在测试套件开始前加载已知数据 | 可预测，但数据库模式变更时容易出问题 |
| **工厂函数（Factory Functions）** | 程序生成数据 | 灵活，但需要更多的设置代码 |
| **测试容器（Test Containers）** | 在Docker中启动真实的数据库 | 更真实，但启动速度较慢 |

```typescript
// Transaction rollback pattern (Prisma)
beforeEach(async () => {
  await prisma.$executeRaw`BEGIN`;
});
afterEach(async () => {
  await prisma.$executeRaw`ROLLBACK`;
});

test('creates user in database', async () => {
  const user = await createUser({ name: 'Alice', email: 'a@b.com' });
  const found = await prisma.user.findUnique({ where: { id: user.id } });
  expect(found?.name).toBe('Alice');
});
```

### API测试

```typescript
// Supertest (Node.js)
import request from 'supertest';
import { app } from '../src/app';

describe('POST /api/users', () => {
  it('creates a user and returns 201', async () => {
    const res = await request(app)
      .post('/api/users')
      .send({ name: 'Alice', email: 'alice@test.com' })
      .expect(201);

    expect(res.body).toMatchObject({
      id: expect.any(String),
      name: 'Alice',
    });
  });

  it('returns 400 for invalid email', async () => {
    await request(app)
      .post('/api/users')
      .send({ name: 'Alice', email: 'not-an-email' })
      .expect(400);
  });
});
```

---

## 模拟的最佳实践

### 模拟系统边界，而不是内部逻辑

基本原则：只在系统边界（外部API、数据库、文件系统）进行模拟，切勿模拟内部业务逻辑。

```typescript
// BAD — mocking internal implementation
jest.mock('./utils/formatDate');  // Breaks on refactor

// GOOD — mocking external boundary
jest.mock('./services/paymentGateway');  // Third-party API is the boundary
```

### 何时模拟，何时不模拟

| 应该模拟 | 不应该模拟 |
|------|-----------|
| HTTP API、外部服务 | 纯函数 |
| 数据库（在单元测试中） | 你的业务逻辑 |
| 文件系统、网络操作 | 数据转换 |
| 时间/日期（如`Date.now()`） | 简单的计算 |
| 环境变量 | 内部类方法 |

### 依赖注入以提高可测试性

通过代码结构设计，使得在测试中可以替换依赖项。这是提高代码可测试性的最有效方法。

```typescript
// Injectable dependencies — easy to test
class OrderService {
  constructor(
    private paymentGateway: PaymentGateway,
    private inventory: InventoryService,
    private notifier: NotificationService,
  ) {}

  async placeOrder(order: Order): Promise<OrderResult> {
    const stock = await this.inventory.check(order.items);
    if (!stock.available) return { status: 'out_of_stock' };

    const payment = await this.paymentGateway.charge(order.total);
    if (!payment.success) return { status: 'payment_failed' };

    await this.notifier.send(order.userId, 'Order confirmed');
    return { status: 'confirmed', id: payment.transactionId };
  }
}

// In tests — inject fakes
const service = new OrderService(
  new FakePaymentGateway(),
  new FakeInventory({ available: true }),
  new FakeNotifier(),
);
```

---

## 测试框架快速参考

| 框架 | 语言 | 测试类型 | 测试运行器 | 断言方法 |
|-----------|----------|------|-------------|-----------|
| **Jest** | JavaScript/TypeScript | 单元测试/集成测试 | 内置 | `expect()` |
| **Vitest** | JavaScript/TypeScript | 单元测试/集成测试 | Vite内置 | `expect()`（兼容Jest） |
| **Playwright** | JavaScript/TypeScript/Python | 端到端测试 | 内置 | `expect()` / 定位器（locators） |
| **Cypress** | JavaScript/TypeScript | 端到端测试 | 内置 | `cy.should()` |
| **pytest** | Python | 单元测试/集成测试 | 内置 | `assert` |
| **Go测试** | Go语言 | 单元测试/集成测试 | `go test` | `t.Error()` / `testify` |
| **Rust** | Rust语言 | 单元测试/集成测试 | `cargo test` | `assert!()` / `assert_eq!()` |
| **JUnit 5** | Java/Kotlin | 单元测试/集成测试 | 内置 | `assertEquals()` |
| **RSpec** | Ruby语言 | 单元测试/集成测试 | 内置 | `expect().to` |
| **PHPUnit** | PHP语言 | 单元测试/集成测试 | 内置 | `$this->assert*()` |
| **xUnit** | C#语言 | 单元测试/集成测试 | 内置 | `Assert.Equal()` |

---

## 测试质量检查清单

| 质量标准 | 规则 | 原因 |
|---------|------|-----|
| **确定性** | 相同的输入应始终产生相同的结果 | 不稳定的测试会降低开发者的信心 |
| **隔离性** | 测试之间不应有共享的可变状态 | 依赖顺序的测试可能在持续集成（CI）过程中出问题 |
| **速度** | 单元测试：<10毫秒，集成测试：<1秒，端到端测试：<30秒 | 运行速度慢的测试可能不会被执行 |
| **可读性** | 测试名称应描述测试场景和预期结果 | 测试本身就是文档 |
| **可维护性** | 修改一个功能时，只需修改相应的测试 | 不稳定的测试会阻碍开发进度 |
| **针对性** | 每个测试应只验证一个逻辑点 | 失败能明确指出问题所在 |

> **命名规范：** `test_[单元功能]_[测试场景]_[预期结果)` 或 `should [在条件Y下执行X]`

---

## 测试覆盖策略

### 何时追求不同的测试目标

| 目标 | 适用场景 | 原因 |
|--------|------|-----------|
| **80%以上的代码覆盖率** | 业务逻辑、辅助函数、核心功能 | 高投资回报率——能捕获大多数回归错误 |
| **90%以上的分支覆盖率** | 支付处理、认证、安全关键部分 | 边缘情况需要重点测试 |
| **100%的代码覆盖率** | 几乎不需要——过度覆盖反而会降低效率 | 获取器/设置器的测试会增加不必要的复杂性 |
| **变异测试** | 在达到较高覆盖率后，对关键路径进行测试 | 确保测试能真正捕获错误 |

### 不应测试的内容

| 应避免测试的内容 | 原因 |
|------|--------|
| 由工具生成的代码（如Prisma客户端、protobuf） | 由工具维护的代码 |
| 第三方库的内部实现 | 不属于你的职责范围 |
| 简单的getter/setter方法 | 没有需要验证的逻辑 |
| 配置文件 | 应测试它们配置的行为 |
| 控制台日志/打印语句 | 没有业务价值的副作用 |

---

## 测试组织

```
src/
├── services/
│   ├── order.service.ts
│   └── order.service.test.ts      # Co-located unit tests
├── api/
│   └── routes/
│       └── orders.ts
tests/
├── integration/
│   ├── api/
│   │   └── orders.test.ts         # API integration tests
│   └── db/
│       └── order.repo.test.ts     # DB integration tests
├── e2e/
│   ├── pages/                     # Page objects
│   │   └── checkout.page.ts
│   └── specs/
│       └── checkout.spec.ts       # E2E specs
└── helpers/
    ├── factories.ts               # Test data factories
    └── setup.ts                   # Global test setup
```

> **规则：** 将单元测试与源代码放在同一目录中。将集成测试和端到端测试放在专门的目录中。

---

## 避免的测试实践

| 避免的测试实践 | 问题 | 解决方法 |
|--------------|---------|-----|
| **测试实现细节** | 重构时测试失败，而非检测实际功能 | 应测试功能及其输出，而非内部实现 |
| **不稳定的测试** | 不稳定的测试结果会影响持续集成（CI） | 移除对时间、顺序或网络的依赖 |
| **测试之间的状态冲突** | 测试之间共享可变状态 | 在`beforeEach`/`setUp`中重置状态 |
| **长时间的等待操作** | 使用`sleep(2000)`会导致测试运行缓慢且不可靠 | 使用显式的等待机制、轮询或事件触发 |
| 复杂的测试设置** | 长达50行的设置代码会降低测试的可读性 | 将复杂的设置逻辑提取到单独的工厂函数中 |
| **无断言的测试** | 测试虽然运行但没有任何验证 | 每个测试都必须有明确的断言或预期结果 |
| **过度模拟** | 模拟所有内容会导致测试失去实际意义 | 只应模拟系统边界 |
| **重复的测试代码** | 重复的测试会导致代码冗余 | 使用参数化测试或辅助函数 |
| **测试框架本身** | 测试库的实现是否正常工作 | 应测试你的代码逻辑，而不是框架 |
| **忽略测试失败** | 使用`skip`、`xit`、`@Disabled`等标记来忽略测试 | 必须修复或删除被忽略的测试 |
| **与数据库的紧密耦合** | 数据库模式变更时测试失败 | 在单元测试中使用模拟数据 |
| **单一的巨大测试用例** | 一个测试用例涵盖多个场景 | 将测试拆分为更具体的、有明确名称的测试 |
| **修复错误后不更新测试** | 修复错误后可能会重新引入问题 | 每个错误修复都应对应相应的测试 |

---

## 绝对不能做的事情

1. **绝不要测试代码的实现细节，而应测试代码的功能** — 测试应验证代码的功能，而不是实现方式。
2. **绝不要在测试中使用`sleep()`** — 应使用显式的等待机制、轮询或自动重试的断言方法。
3. **绝不要在测试之间共享可变状态** — 每个测试都应自行设置和清理状态。
4. **绝不要编写没有断言的测试** — 没有断言的测试无法验证任何内容。
5. **绝不要模拟内部业务逻辑** — 只应在系统边界（如网络、数据库、文件系统）进行模拟。
6. **绝不要在没有关联问题及恢复计划的情况下忽略测试** — 被忽略的测试会逐渐累积，导致测试体系变得混乱。
7. **绝不要让测试套件处于失败状态** — 在继续开发之前，必须修复问题或删除失败的测试。
8. **绝不要将100%的覆盖率作为目标** — 覆盖率只是一个工具，关键路径上的强断言比全局的弱断言更重要。

---

## 总结

| 应该做 | 不应该做 |
|----|-------|
| 测试代码的功能，而不是实现细节 | 模拟所有相关的系统边界 |
| 在修复错误之前先编写测试代码 | 为了加快发布速度而忽略测试 |
| 保持测试的高效率和确定性 | 避免使用`sleep()`或共享状态 |
| 使用工厂函数生成测试数据 | 不要在多个测试中重复设置代码 |
| 只模拟系统边界 | 不要模拟内部函数 |
| 为测试命名时要有描述性 | 测试名称应清晰明了 |
| 在每次推送代码时都运行测试 | 应仅在本地运行测试 |
| 删除或修复被忽略的测试 | 不要让被忽略的测试长期存在 |
| 使用参数化测试来处理不同情况 | 避免重复编写测试代码 |
| 为提高可测试性而注入依赖项 | 不要硬编码依赖关系 |

> **记住：** 测试是安全网——快速、可靠的测试体系能让你放心地进行代码重构，并确保代码的质量。