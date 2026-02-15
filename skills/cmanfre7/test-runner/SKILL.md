# 测试运行器

用于跨语言和框架编写和运行测试。

## 框架选择

| 语言 | 单元测试 | 集成测试 | 端到端测试 |
|----------|-----------|-------------|-----|
| TypeScript/JavaScript | Vitest（推荐），Jest | Supertest | Playwright |
| Python | pytest | pytest + httpx | Playwright |
| Swift | XCTest | XCTest | XCUITest |

## 按框架快速入门

### Vitest（TypeScript / JavaScript）
```bash
npm install -D vitest @testing-library/react @testing-library/jest-dom
```

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config'
export default defineConfig({
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './tests/setup.ts',
  },
})
```

```bash
npx vitest              # Watch mode
npx vitest run          # Single run
npx vitest --coverage   # With coverage
```

### Jest
```bash
npm install -D jest @types/jest ts-jest
```

```bash
npx jest                # Run all
npx jest --watch        # Watch mode
npx jest --coverage     # With coverage
npx jest path/to/test   # Single file
```

### pytest（Python）
```bash
uv pip install pytest pytest-cov pytest-asyncio httpx
```

```bash
pytest                          # Run all
pytest -v                       # Verbose
pytest -x                       # Stop on first failure
pytest --cov=app                # With coverage
pytest tests/test_api.py -k "test_login"  # Specific test
pytest --tb=short               # Short tracebacks
```

### XCTest（Swift）
```bash
swift test                      # Run all tests
swift test --filter MyTests     # Specific test suite
swift test --parallel           # Parallel execution
```

### Playwright（端到端测试）
```bash
npm install -D @playwright/test
npx playwright install
```

```bash
npx playwright test                    # Run all
npx playwright test --headed           # With browser visible
npx playwright test --debug            # Debug mode
npx playwright test --project=chromium # Specific browser
npx playwright show-report             # View HTML report
```

## TDD（测试驱动开发）工作流程

1. **编写失败的测试用例** — 编写描述预期行为的测试用例。
2. **编写最少的代码** — 编写使测试通过的最小代码量。
3. **重构代码** — 在保持测试通过的情况下优化代码结构。

```
┌─────────┐     ┌─────────┐     ┌──────────┐
│  Write   │────▶│  Write  │────▶│ Refactor │──┐
│  Test    │     │  Code   │     │  Code    │  │
│  (Red)   │     │ (Green) │     │          │  │
└─────────┘     └─────────┘     └──────────┘  │
     ▲                                          │
     └──────────────────────────────────────────┘
```

## 测试模式

### Arrange-Act-Assert（排列-执行-断言）
```typescript
test('calculates total with tax', () => {
  // Arrange
  const cart = new Cart([{ price: 100, qty: 2 }]);

  // Act
  const total = cart.totalWithTax(0.08);

  // Assert
  expect(total).toBe(216);
});
```

### 测试异步代码
```typescript
test('fetches user data', async () => {
  const user = await getUser('123');
  expect(user.name).toBe('Colt');
});
```

### 模拟（Mocking）
```typescript
import { vi } from 'vitest';

const mockFetch = vi.fn().mockResolvedValue({
  json: () => Promise.resolve({ id: 1, name: 'Test' }),
});
vi.stubGlobal('fetch', mockFetch);
```

### 测试API接口（Python）
```python
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_get_users():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
```

### 测试React组件
```typescript
import { render, screen, fireEvent } from '@testing-library/react';
import { Button } from './Button';

test('calls onClick when clicked', () => {
  const handleClick = vi.fn();
  render(<Button onClick={handleClick}>Click me</Button>);
  fireEvent.click(screen.getByText('Click me'));
  expect(handleClick).toHaveBeenCalledOnce();
});
```

## 覆盖率相关命令

```bash
# JavaScript/TypeScript
npx vitest --coverage          # Vitest (uses v8 or istanbul)
npx jest --coverage            # Jest

# Python
pytest --cov=app --cov-report=html    # HTML report
pytest --cov=app --cov-report=term    # Terminal output
pytest --cov=app --cov-fail-under=80  # Fail if < 80%

# View HTML coverage report
open coverage/index.html       # macOS
open htmlcov/index.html        # Python
```

## 应该测试的内容

**必须测试的内容：**
- 公共API/导出的函数
- 边缘情况：空输入、null值、边界值
- 错误处理：无效输入、网络故障
- 业务逻辑：计算逻辑、状态转换

**无需测试的内容：**
- 私有的实现细节
- 框架的内部机制（如React的渲染逻辑、Express的路由机制）
- 简单的getter/setter方法
- 第三方库的实现行为