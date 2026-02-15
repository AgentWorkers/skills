---
name: unit-testing-expert
description: Vitest 和 Jest 的单元测试专家。负责编写单元测试代码、实现模拟功能（mocking），以及配置测试覆盖率。
---

# 单元测试专家

**具备独立的单元测试能力，适用于任何使用Vitest/Jest的项目。**

---

## 测试驱动开发（Test-Driven Development, TDD）

**红-绿-重构（Red-Green-Refactor）循环：**

```typescript
// 1. RED: Write failing test
describe('Calculator', () => {
  it('should add two numbers', () => {
    const calc = new Calculator();
    expect(calc.add(2, 3)).toBe(5);
  });
});

// 2. GREEN: Minimal implementation
class Calculator {
  add(a: number, b: number): number {
    return a + b;
  }
}

// 3. REFACTOR: Improve code
class Calculator {
  add(...numbers: number[]): number {
    return numbers.reduce((sum, n) => sum + n, 0);
  }
}
```

**TDD的优势：**
- 更好的代码设计（易于测试）
- 实时的文档记录
- 更快的调试速度
- 更高的代码可靠性

---

## Vitest/Jest基础

### 基本测试结构

```typescript
import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { UserService } from './UserService';

describe('UserService', () => {
  let service: UserService;

  beforeEach(() => {
    service = new UserService();
  });

  afterEach(() => {
    vi.clearAllMocks();
  });

  it('should create user', () => {
    const user = service.create({ name: 'John', email: 'john@test.com' });

    expect(user).toMatchObject({
      id: expect.any(String),
      name: 'John',
      email: 'john@test.com'
    });
  });

  it('should throw for invalid email', () => {
    expect(() => {
      service.create({ name: 'John', email: 'invalid' });
    }).toThrow('Invalid email');
  });
});
```

### 异步测试

```typescript
it('should fetch user from API', async () => {
  const user = await api.fetchUser('user-123');

  expect(user).toEqual({
    id: 'user-123',
    name: 'John Doe'
  });
});

// Testing async errors
it('should handle API errors', async () => {
  await expect(api.fetchUser('invalid')).rejects.toThrow('User not found');
});
```

---

## 模拟策略

### 1. 模拟函数

```typescript
// Mock a function
const mockFn = vi.fn();
mockFn.mockReturnValue(42);
expect(mockFn()).toBe(42);

// Mock with implementation
const mockAdd = vi.fn((a, b) => a + b);
expect(mockAdd(2, 3)).toBe(5);

// Verify calls
expect(mockFn).toHaveBeenCalledTimes(1);
expect(mockFn).toHaveBeenCalledWith(expected);
```

### 2. 模拟模块

```typescript
// Mock entire module
vi.mock('./database', () => ({
  query: vi.fn().mockResolvedValue([{ id: 1, name: 'Test' }])
}));

import { query } from './database';

it('should fetch users from database', async () => {
  const users = await query('SELECT * FROM users');
  expect(users).toHaveLength(1);
});
```

### 3. 间谍（Spies）

```typescript
// Spy on existing method
const spy = vi.spyOn(console, 'log');

myFunction();

expect(spy).toHaveBeenCalledWith('Expected message');
spy.mockRestore();
```

### 4. 模拟依赖项

```typescript
class UserService {
  constructor(private db: Database) {}

  async getUser(id: string) {
    return this.db.query('SELECT * FROM users WHERE id = ?', [id]);
  }
}

// Test with mock
const mockDb = {
  query: vi.fn().mockResolvedValue({ id: '123', name: 'John' })
};

const service = new UserService(mockDb);
const user = await service.getUser('123');

expect(mockDb.query).toHaveBeenCalledWith(
  'SELECT * FROM users WHERE id = ?',
  ['123']
);
```

---

## 测试模式

### AAA模式（Arrange-Act-Assert）

```typescript
it('should calculate total price', () => {
  // Arrange
  const cart = new ShoppingCart();
  cart.addItem({ price: 10, quantity: 2 });
  cart.addItem({ price: 5, quantity: 3 });

  // Act
  const total = cart.getTotal();

  // Assert
  expect(total).toBe(35);
});
```

### Given-When-Then（行为驱动开发, BDD）

```typescript
describe('Shopping Cart', () => {
  it('should apply discount when total exceeds $100', () => {
    // Given: A cart with items totaling $120
    const cart = new ShoppingCart();
    cart.addItem({ price: 120, quantity: 1 });

    // When: Getting the total
    const total = cart.getTotal();

    // Then: 10% discount applied
    expect(total).toBe(108); // $120 - $12 (10%)
  });
});
```

### 参数化测试

```typescript
describe.each([
  [2, 3, 5],
  [10, 5, 15],
  [-1, 1, 0],
  [0, 0, 0]
])('Calculator.add(%i, %i)', (a, b, expected) => {
  it(`should return ${expected}`, () => {
    const calc = new Calculator();
    expect(calc.add(a, b)).toBe(expected);
  });
});
```

---

## 测试替身（Test Doubles）

### 模拟（Mocks） vs 替身（Stubs） vs 间谍（Spies） vs 假装对象（Fakes）

**模拟（Mock）**：验证函数的行为（调用、参数）
```typescript
const mock = vi.fn();
mock('test');
expect(mock).toHaveBeenCalledWith('test');
```

**替身（Stub）**：返回预定义的值
```typescript
const stub = vi.fn().mockReturnValue(42);
expect(stub()).toBe(42);
```

**间谍（Spy）**：观察真实的函数行为
```typescript
const spy = vi.spyOn(obj, 'method');
obj.method();
expect(spy).toHaveBeenCalled();
```

**假装对象（Fake）**：简化的实现版本
```typescript
class FakeDatabase {
  private data = new Map();

  async save(key, value) {
    this.data.set(key, value);
  }

  async get(key) {
    return this.data.get(key);
  }
}
```

---

## 覆盖率分析

### 运行覆盖率分析

```bash
# Vitest
vitest --coverage

# Jest
jest --coverage
```

### 覆盖率阈值

```javascript
// vitest.config.ts
export default {
  test: {
    coverage: {
      provider: 'v8',
      reporter: ['text', 'html', 'lcov'],
      lines: 80,
      functions: 80,
      branches: 80,
      statements: 80
    }
  }
};
```

### 覆盖率最佳实践

**✅ 应该做到：**
- 力求达到80-90%的代码覆盖率
- 重点测试业务逻辑
- 测试边界情况
- 测试错误路径

**❌ 不应该做：**
- 追求100%的覆盖率
- 仅测试getter/setter方法
- 测试测试框架代码
- 仅仅为了提高覆盖率而编写测试

---

## 快照测试（Snapshot Testing）

### 何时使用快照

**适用场景：**
- UI组件的输出结果
- API响应
- 配置对象
- 错误信息

```typescript
it('should render user card', () => {
  const card = renderUserCard({ name: 'John', role: 'Admin' });
  expect(card).toMatchSnapshot();
});

// Update snapshots: vitest -u
```

**不适合使用快照的情况：**
- 日期/时间戳
- 随机生成的值
- 大型对象（应使用具体的断言方式）

---

## 测试组织

### 文件结构

```
src/
├── services/
│   ├── UserService.ts
│   └── UserService.test.ts      ← Co-located
tests/
├── unit/
│   └── utils.test.ts
├── integration/
│   └── api.test.ts
└── fixtures/
    └── users.json
```

### 测试命名规范

**✅ 正确的命名方式：**
```typescript
describe('UserService.create', () => {
  it('should create user with valid email', () => {});
  it('should throw error for invalid email', () => {});
  it('should generate unique ID', () => {});
});
```

**❌ 错误的命名方式：**
```typescript
describe('UserService', () => {
  it('test1', () => {});
  it('should work', () => {});
});
```

---

## 错误处理测试

```typescript
// Synchronous errors
it('should throw for negative numbers', () => {
  expect(() => sqrt(-1)).toThrow('Cannot compute square root of negative');
});

// Async errors
it('should reject for invalid ID', async () => {
  await expect(fetchUser('invalid')).rejects.toThrow('Invalid ID');
});

// Error types
it('should throw TypeError', () => {
  expect(() => doSomething()).toThrow(TypeError);
});

// Custom errors
it('should throw ValidationError', () => {
  expect(() => validate()).toThrow(ValidationError);
});
```

---

## 测试隔离

### 测试之间的状态重置

```typescript
let service: UserService;

beforeEach(() => {
  service = new UserService();
  vi.clearAllMocks();
});

afterEach(() => {
  vi.restoreAllMocks();
});
```

### 避免测试之间的相互依赖

**❌ 不应该做的：**
```typescript
let user;

it('should create user', () => {
  user = createUser(); // Shared state
});

it('should update user', () => {
  updateUser(user); // Depends on previous test
});
```

**✅ 应该做的：**
```typescript
it('should update user', () => {
  const user = createUser();
  updateUser(user);
  expect(user.updated).toBe(true);
});
```

---

## VSCode调试模式与子进程测试

**关键注意事项：** 当测试启动子进程（如CLI工具、测试钩子或外部命令）时，在VSCode的调试模式下可能会遇到问题，因为`NODE_OPTIONS`的影响。

### 问题：`NODE_OPTIONS`会影响子进程
VSCode调试器会设置`NODE_OPTIONS=--inspect-brk=<port>`，这会导致子进程尝试连接到同一个调试端口，从而导致失败（退出代码为1）。

**症状：**
- 使用“Run Test”时测试通过，但使用“Debug Test”时失败
- 启动的进程以退出代码1结束且没有输出
- `spawnSync`/`execFileSync`调用会无声地失败

**解决方案：使用`getCleanEnv()`函数**

```typescript
// src/utils/clean-env.ts
export function getCleanEnv(): NodeJS.ProcessEnv {
  const cleanEnv = { ...process.env };

  // Debugger flags (VSCode, WebStorm, IntelliJ)
  delete cleanEnv.NODE_OPTIONS;
  delete cleanEnv.NODE_INSPECT;
  delete cleanEnv.NODE_INSPECT_RESUME_ON_START;

  // Coverage/instrumentation (CI/CD pipelines)
  delete cleanEnv.NODE_V8_COVERAGE;
  delete cleanEnv.VSCODE_INSPECTOR_OPTIONS;

  return cleanEnv;
}
```

**在测试中的使用方法：**

```typescript
import { getCleanEnv } from '../test-utils/clean-env.js';
import { execSync, spawnSync } from 'child_process';

it('should execute CLI command', () => {
  const result = execSync('node my-cli.js', {
    encoding: 'utf-8',
    env: getCleanEnv(),  // ← CRITICAL for debug mode + CI/CD
  });
  expect(result).toContain('expected output');
});

it('should spawn child process', () => {
  const result = spawnSync('npm', ['run', 'build'], {
    encoding: 'utf-8',
    env: getCleanEnv(),  // ← CRITICAL
  });
  expect(result.status).toBe(0);
});
```

**何时使用`getCleanEnv()`：**
**✅ 在以下情况下必须使用：**
- 启动CLI工具（`node`、`npm`、`npx`、`claude`等）
- 启动外部命令（`git`、`gh`等）
- 启动子进程的测试钩子
- 涉及真实进程的集成测试

**❌ 不需要使用`getCleanEnv()`的情况：**
- 纯粹的单元测试（不涉及子进程）
- 使用模拟的依赖项
- 在进程内部的测试

---

## 使用`vi.hoisted()`进行ESM模块的模拟

**关键注意事项：** 在ESM（ECMAScript模块）中，导入语句会被提前解析。使用`vi.hoisted()`可以确保模拟在导入之前就被定义。

### 问题：模拟在导入之后才被定义

```typescript
// ❌ WRONG: vi.mock hoisted, but mockFn not defined yet
vi.mock('./module', () => ({
  myFunc: mockFn  // ReferenceError: mockFn is not defined
}));

const mockFn = vi.fn();
import { myFunc } from './module';
```

**解决方案：使用`vi.hoisted()`**

```typescript
import { describe, it, expect, vi } from 'vitest';

// ✅ Define mocks in hoisted context FIRST
const { mockFn } = vi.hoisted(() => ({
  mockFn: vi.fn()
}));

// Now vi.mock can use the hoisted mock
vi.mock('./module', () => ({
  myFunc: mockFn
}));

// Import AFTER mock setup
import { myFunc } from './module';

describe('Module', () => {
  it('should use mocked function', () => {
    mockFn.mockReturnValue('mocked');
    expect(myFunc()).toBe('mocked');
    expect(mockFn).toHaveBeenCalled();
  });
});
```

**完整的ESM模块模拟示例**

```typescript
import { describe, it, expect, vi, beforeEach } from 'vitest';

// 1. Hoisted mock definitions
const { mockReadFile, mockWriteFile } = vi.hoisted(() => ({
  mockReadFile: vi.fn(),
  mockWriteFile: vi.fn()
}));

// 2. Mock the module using hoisted mocks
vi.mock('fs/promises', () => ({
  readFile: mockReadFile,
  writeFile: mockWriteFile
}));

// 3. Import AFTER mock setup (imports are automatically hoisted in Vitest)
import { readFile, writeFile } from 'fs/promises';

describe('FileService', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should read file', async () => {
    mockReadFile.mockResolvedValue('file content');

    const content = await readFile('/path/to/file', 'utf-8');

    expect(content).toBe('file content');
    expect(mockReadFile).toHaveBeenCalledWith('/path/to/file', 'utf-8');
  });
});
```

### `vi.hoisted()`与传统模拟方法的对比

| 方法 | 是否兼容ESM | 是否兼容Jest |
|----------|---------------|-----------------|
| `vi.hoisted()` + `vi.mock()` | ✅ 是 | ❌ 不（仅适用于Vitest） |
| 使用`jest.mock()`进行模拟 | ⚠️ 部分兼容 | ✅ 是 |
| 手动替换模块 | ✅ 是 | ✅ 是 |

---

## 在隔离的临时目录中进行测试

**关键注意事项：** 集成测试绝不应该在项目目录中执行，应始终使用隔离的临时目录。

### 问题：测试可能影响项目状态

```typescript
// ❌ DANGEROUS: Can corrupt project state
const testDir = path.join(process.cwd(), '.specweave/test');
```

**解决方案：使用隔离的临时目录**

```typescript
import * as os from 'os';
import * as path from 'path';
import * as fs from 'fs/promises';

// ✅ SAFE: Unique temp directory per test run
const TEST_ROOT = path.join(
  os.tmpdir(),
  `my-test-${Date.now()}-${Math.random().toString(36).slice(2)}`
);

describe('Integration Test', () => {
  beforeEach(async () => {
    await fs.mkdir(TEST_ROOT, { recursive: true });
  });

  afterEach(async () => {
    await fs.rm(TEST_ROOT, { recursive: true, force: true });
  });

  it('should work in isolated directory', async () => {
    const testFile = path.join(TEST_ROOT, 'test.json');
    await fs.writeFile(testFile, '{"test": true}');
    // Test logic...
  });
});
```

### 恢复工作目录的步骤

当测试更改工作目录时，务必将其恢复到初始状态，以防止影响其他测试：

```typescript
describe('Tests that change CWD', () => {
  let originalCwd: string;

  beforeEach(() => {
    originalCwd = process.cwd();  // ← Save BEFORE changing
    process.chdir(TEST_ROOT);
  });

  afterEach(() => {
    process.chdir(originalCwd);   // ← Restore BEFORE cleanup
    // Now safe to delete TEST_ROOT
  });
});
```

---

## 最佳实践总结

**✅ 应该做到：**
- 在编写代码之前先编写测试（TDD）
- 测试函数的行为，而不是实现细节
- 每个测试只包含一个断言
- 为测试变量使用描述性的名称
- 模拟外部依赖项
- 测试边界情况和错误情况
- 保持测试速度（每个测试不超过100毫秒）
- 使用描述性的变量名
- 测试完成后清理环境

**❌ 不应该做：**
- 直接测试私有方法
- 在测试之间共享状态
- 使用真实的数据库或API
- 测试测试框架代码
- 编写依赖实现变化的测试
- 跳过错误情况
- 使用难以理解的代码（如魔法数字）
- 留下未使用的测试代码

---

## 快速参考

### 断言（Assertions）

```typescript
expect(value).toBe(expected);              // ===
expect(value).toEqual(expected);           // Deep equality
expect(value).toBeTruthy();                // Boolean true
expect(value).toBeFalsy();                 // Boolean false
expect(array).toHaveLength(3);             // Array length
expect(array).toContain(item);             // Array includes
expect(string).toMatch(/pattern/);         // Regex match
expect(fn).toThrow(Error);                 // Throws error
expect(obj).toHaveProperty('key');         // Has property
expect(value).toBeCloseTo(0.3, 5);        // Float comparison
```

### 生命周期钩子（Lifecycle Hooks）

```typescript
beforeAll(() => {});      // Once before all tests
beforeEach(() => {});     // Before each test
afterEach(() => {});      // After each test
afterAll(() => {});       // Once after all tests
```

### 模拟相关工具（Mocking Utilities）

```typescript
vi.fn()                           // Create mock
vi.fn().mockReturnValue(x)        // Return value
vi.fn().mockResolvedValue(x)      // Async return
vi.fn().mockRejectedValue(e)      // Async error
vi.mock('./module')               // Mock module
vi.spyOn(obj, 'method')           // Spy on method
vi.clearAllMocks()                // Clear call history
vi.resetAllMocks()                // Reset + clear
vi.restoreAllMocks()              // Restore originals
```

---

**此技能具有独立性，适用于任何使用Vitest/Jest的项目。**