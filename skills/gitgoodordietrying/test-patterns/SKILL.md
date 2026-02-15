---
name: test-patterns
description: 编写并运行跨语言和框架的测试。这些工具可用于设置测试套件、编写单元测试/集成测试/端到端测试、衡量代码覆盖率、模拟依赖关系以及调试测试失败。支持的语言和框架包括 Node.js（Jest/Vitest）、Python（pytest）、Go、Rust 和 Bash。
metadata: {"clawdbot":{"emoji":"🧪","requires":{"anyBins":["node","python3","go","cargo","bash"]},"os":["linux","darwin","win32"]}}
---

# 测试模式

跨语言编写、运行和调试测试。涵盖单元测试、集成测试、端到端测试（E2E测试）、模拟（mocking）、代码覆盖率（coverage）以及测试驱动开发（TDD）的工作流程。

## 使用场景

- 为新项目设置测试套件
- 为函数或模块编写单元测试
- 为API或数据库交互编写集成测试
- 设置代码覆盖率监控
- 模拟外部依赖项（API、数据库、文件系统）
- 调试不稳定或失败的测试
- 实施测试驱动开发（TDD）

## Node.js（Jest / Vitest）

### 设置

```bash
# Jest
npm install -D jest
# Add to package.json: "scripts": { "test": "jest" }

# Vitest (faster, ESM-native)
npm install -D vitest
# Add to package.json: "scripts": { "test": "vitest" }
```

### 单元测试

```javascript
// math.js
export function add(a, b) { return a + b; }
export function divide(a, b) {
  if (b === 0) throw new Error('Division by zero');
  return a / b;
}

// math.test.js
import { add, divide } from './math.js';

describe('add', () => {
  test('adds two positive numbers', () => {
    expect(add(2, 3)).toBe(5);
  });

  test('handles negative numbers', () => {
    expect(add(-1, 1)).toBe(0);
  });

  test('handles zero', () => {
    expect(add(0, 0)).toBe(0);
  });
});

describe('divide', () => {
  test('divides two numbers', () => {
    expect(divide(10, 2)).toBe(5);
  });

  test('throws on division by zero', () => {
    expect(() => divide(10, 0)).toThrow('Division by zero');
  });

  test('handles floating point', () => {
    expect(divide(1, 3)).toBeCloseTo(0.333, 3);
  });
});
```

### 异步测试

```javascript
// api.test.js
import { fetchUser } from './api.js';

test('fetches user by id', async () => {
  const user = await fetchUser('123');
  expect(user).toHaveProperty('id', '123');
  expect(user).toHaveProperty('name');
  expect(user.name).toBeTruthy();
});

test('throws on missing user', async () => {
  await expect(fetchUser('nonexistent')).rejects.toThrow('Not found');
});
```

### 模拟（Mocking）

```javascript
// Mock a module
jest.mock('./database.js');
import { getUser } from './database.js';
import { processUser } from './service.js';

test('processes user from database', async () => {
  // Setup mock return value
  getUser.mockResolvedValue({ id: '1', name: 'Alice', active: true });

  const result = await processUser('1');
  expect(result.processed).toBe(true);
  expect(getUser).toHaveBeenCalledWith('1');
  expect(getUser).toHaveBeenCalledTimes(1);
});

// Mock fetch
global.fetch = jest.fn();

test('calls API with correct params', async () => {
  fetch.mockResolvedValue({
    ok: true,
    json: async () => ({ data: 'test' }),
  });

  const result = await myApiCall('/endpoint');
  expect(fetch).toHaveBeenCalledWith('/endpoint', expect.objectContaining({
    method: 'GET',
  }));
});

// Spy on existing method (don't replace, just observe)
const consoleSpy = jest.spyOn(console, 'log').mockImplementation();
// ... run code ...
expect(consoleSpy).toHaveBeenCalledWith('expected message');
consoleSpy.mockRestore();
```

### 代码覆盖率（Coverage）

```bash
# Jest
npx jest --coverage

# Vitest
npx vitest --coverage

# Check coverage thresholds (jest.config.js)
# coverageThreshold: { global: { branches: 80, functions: 80, lines: 80, statements: 80 } }
```

## Python（pytest）

### 设置

```bash
pip install pytest pytest-cov
```

### 单元测试

```python
# calculator.py
def add(a, b):
    return a + b

def divide(a, b):
    if b == 0:
        raise ValueError("Division by zero")
    return a / b

# test_calculator.py
import pytest
from calculator import add, divide

def test_add():
    assert add(2, 3) == 5

def test_add_negative():
    assert add(-1, 1) == 0

def test_divide():
    assert divide(10, 2) == 5.0

def test_divide_by_zero():
    with pytest.raises(ValueError, match="Division by zero"):
        divide(10, 0)

def test_divide_float():
    assert divide(1, 3) == pytest.approx(0.333, abs=0.001)
```

### 参数化测试

```python
@pytest.mark.parametrize("a,b,expected", [
    (2, 3, 5),
    (-1, 1, 0),
    (0, 0, 0),
    (100, -50, 50),
])
def test_add_cases(a, b, expected):
    assert add(a, b) == expected
```

### 固定装置（Fixtures）

```python
import pytest
import json
import tempfile
import os

@pytest.fixture
def sample_users():
    """Provide test user data."""
    return [
        {"id": 1, "name": "Alice", "email": "alice@test.com"},
        {"id": 2, "name": "Bob", "email": "bob@test.com"},
    ]

@pytest.fixture
def temp_db(tmp_path):
    """Provide a temporary SQLite database."""
    import sqlite3
    db_path = tmp_path / "test.db"
    conn = sqlite3.connect(str(db_path))
    conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)")
    conn.commit()
    yield conn
    conn.close()

def test_insert_users(temp_db, sample_users):
    for user in sample_users:
        temp_db.execute("INSERT INTO users VALUES (?, ?, ?)",
                       (user["id"], user["name"], user["email"]))
    temp_db.commit()
    count = temp_db.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    assert count == 2

# Fixture with cleanup
@pytest.fixture
def temp_config_file():
    path = tempfile.mktemp(suffix=".json")
    with open(path, "w") as f:
        json.dump({"key": "value"}, f)
    yield path
    os.unlink(path)
```

### 模拟（Mocking）

```python
from unittest.mock import patch, MagicMock, AsyncMock

# Mock a function
@patch('mymodule.requests.get')
def test_fetch_data(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"data": "test"}

    result = fetch_data("https://api.example.com")
    assert result == {"data": "test"}
    mock_get.assert_called_once_with("https://api.example.com")

# Mock async
@patch('mymodule.aiohttp.ClientSession.get', new_callable=AsyncMock)
async def test_async_fetch(mock_get):
    mock_get.return_value.__aenter__.return_value.json = AsyncMock(return_value={"ok": True})
    result = await async_fetch("/endpoint")
    assert result["ok"] is True

# Context manager mock
def test_file_reader():
    with patch("builtins.open", MagicMock(return_value=MagicMock(
        read=MagicMock(return_value='{"key": "val"}'),
        __enter__=MagicMock(return_value=MagicMock(read=MagicMock(return_value='{"key": "val"}'))),
        __exit__=MagicMock(return_value=False),
    ))):
        result = read_config("fake.json")
        assert result["key"] == "val"
```

### 代码覆盖率（Coverage）

```bash
# Run with coverage
pytest --cov=mypackage --cov-report=term-missing

# HTML report
pytest --cov=mypackage --cov-report=html
# Open htmlcov/index.html

# Fail if coverage below threshold
pytest --cov=mypackage --cov-fail-under=80
```

## Go

### 单元测试

```go
// math.go
package math

import "errors"

func Add(a, b int) int { return a + b }

func Divide(a, b float64) (float64, error) {
    if b == 0 {
        return 0, errors.New("division by zero")
    }
    return a / b, nil
}

// math_test.go
package math

import (
    "testing"
    "math"
)

func TestAdd(t *testing.T) {
    tests := []struct {
        name     string
        a, b     int
        expected int
    }{
        {"positive", 2, 3, 5},
        {"negative", -1, 1, 0},
        {"zeros", 0, 0, 0},
    }
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got := Add(tt.a, tt.b)
            if got != tt.expected {
                t.Errorf("Add(%d, %d) = %d, want %d", tt.a, tt.b, got, tt.expected)
            }
        })
    }
}

func TestDivide(t *testing.T) {
    result, err := Divide(10, 2)
    if err != nil {
        t.Fatalf("unexpected error: %v", err)
    }
    if math.Abs(result-5.0) > 0.001 {
        t.Errorf("Divide(10, 2) = %f, want 5.0", result)
    }
}

func TestDivideByZero(t *testing.T) {
    _, err := Divide(10, 0)
    if err == nil {
        t.Error("expected error for division by zero")
    }
}
```

### 运行测试

```bash
# All tests
go test ./...

# Verbose
go test -v ./...

# Specific package
go test ./pkg/math/

# With coverage
go test -cover ./...
go test -coverprofile=coverage.out ./...
go tool cover -html=coverage.out

# Run specific test
go test -run TestAdd ./...

# Race condition detection
go test -race ./...

# Benchmark
go test -bench=. ./...
```

## Rust

### 单元测试

```rust
// src/math.rs
pub fn add(a: i64, b: i64) -> i64 { a + b }

pub fn divide(a: f64, b: f64) -> Result<f64, String> {
    if b == 0.0 { return Err("division by zero".into()); }
    Ok(a / b)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_add() {
        assert_eq!(add(2, 3), 5);
        assert_eq!(add(-1, 1), 0);
    }

    #[test]
    fn test_divide() {
        let result = divide(10.0, 2.0).unwrap();
        assert!((result - 5.0).abs() < f64::EPSILON);
    }

    #[test]
    fn test_divide_by_zero() {
        assert!(divide(10.0, 0.0).is_err());
    }

    #[test]
    #[should_panic(expected = "overflow")]
    fn test_overflow_panics() {
        let _ = add(i64::MAX, 1); // Will panic on overflow in debug
    }
}
```

```bash
cargo test
cargo test -- --nocapture  # Show println output
cargo test test_add        # Run specific test
cargo tarpaulin            # Coverage (install: cargo install cargo-tarpaulin)
```

## Bash 测试

### 简单测试运行器

```bash
#!/bin/bash
# test.sh - Minimal bash test framework
PASS=0 FAIL=0

assert_eq() {
  local actual="$1" expected="$2" label="$3"
  if [ "$actual" = "$expected" ]; then
    echo "  PASS: $label"
    ((PASS++))
  else
    echo "  FAIL: $label (got '$actual', expected '$expected')"
    ((FAIL++))
  fi
}

assert_exit_code() {
  local cmd="$1" expected="$2" label="$3"
  eval "$cmd" >/dev/null 2>&1
  assert_eq "$?" "$expected" "$label"
}

assert_contains() {
  local actual="$1" substring="$2" label="$3"
  if echo "$actual" | grep -q "$substring"; then
    echo "  PASS: $label"
    ((PASS++))
  else
    echo "  FAIL: $label ('$actual' does not contain '$substring')"
    ((FAIL++))
  fi
}

# --- Tests ---
echo "Running tests..."

# Test your scripts
output=$(./my-script.sh --help 2>&1)
assert_exit_code "./my-script.sh --help" "0" "help flag exits 0"
assert_contains "$output" "Usage" "help shows usage"

output=$(./my-script.sh --invalid 2>&1)
assert_exit_code "./my-script.sh --invalid" "1" "invalid flag exits 1"

# Test command outputs
assert_eq "$(echo 'hello' | wc -c | tr -d ' ')" "6" "echo hello is 6 bytes"

echo ""
echo "Results: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ] && exit 0 || exit 1
```

## 集成测试模式

### API 集成测试（任何语言）

```bash
#!/bin/bash
# test-api.sh - Start server, run tests, tear down
SERVER_PID=""
cleanup() { [ -n "$SERVER_PID" ] && kill "$SERVER_PID" 2>/dev/null; }
trap cleanup EXIT

# Start server in background
npm start &
SERVER_PID=$!
sleep 2  # Wait for server

# Run tests against live server
BASE_URL=http://localhost:3000 npx jest --testPathPattern=integration
EXIT_CODE=$?

exit $EXIT_CODE
```

### 数据库集成测试（Python）

```python
import pytest
import sqlite3

@pytest.fixture
def db():
    """Fresh database for each test."""
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE items (id INTEGER PRIMARY KEY, name TEXT, price REAL)")
    yield conn
    conn.close()

def test_insert_and_query(db):
    db.execute("INSERT INTO items (name, price) VALUES (?, ?)", ("Widget", 9.99))
    db.commit()
    row = db.execute("SELECT name, price FROM items WHERE name = ?", ("Widget",)).fetchone()
    assert row == ("Widget", 9.99)

def test_empty_table(db):
    count = db.execute("SELECT COUNT(*) FROM items").fetchone()[0]
    assert count == 0
```

## TDD 工作流程

红-绿-重构（Red-Green-Refactor）循环：

1. **红**：为下一个需要测试的功能编写一个失败的测试用例。
2. **绿**：编写最少的代码使测试通过。
3. **重构**：在不改变功能的前提下优化代码（测试用例仍应保持绿色状态）。

```bash
# Tight feedback loop
# Jest watch mode
npx jest --watch

# Vitest watch (default)
npx vitest

# pytest watch (with pytest-watch)
pip install pytest-watch
ptw

# Go (with air or entr)
ls *.go | entr -c go test ./...
```

## 调试失败的测试

### 常见问题

- **单个测试通过，但在测试套件中失败** → 可能存在共享状态的问题。检查以下内容：
  - 测试之间是否修改了全局变量
  - 数据库是否没有被正确清理
  - 模拟对象是否在测试结束后没有被恢复（需要使用 `afterEach` 或 `teardown` 等机制）

- **测试结果不稳定（间歇性失败）** → 可能是时间依赖或执行顺序的问题：
  - 异步操作没有正确使用 `await`
  - 测试结果依赖于特定的执行顺序
  - 包含时间依赖的逻辑（可以使用时间模拟工具）
  - 单元测试中包含网络调用（应该对这些调用进行模拟）

- **代码覆盖率显示有未覆盖的代码路径** → 可能存在边缘情况：
  - 错误处理路径（例如API返回500状态码时）
  - 空输入（空字符串、null、空数组）
  - 边界值（如0、-1、最大整数）

### 运行单个测试

```bash
# Jest
npx jest -t "test name substring"

# pytest
pytest -k "test_divide_by_zero"

# Go
go test -run TestDivideByZero ./...

# Rust
cargo test test_divide
```

## 提示

- 测试的是功能行为，而不是实现细节。测试用例应该能够在代码重构后仍然有效。
- 每个功能点都应该有一个对应的测试用例（不一定每个测试都包含一个 `assert` 语句，但每个逻辑判断都应该有对应的测试）。
- 为测试用例起描述性强的名称：例如 `test_returns_empty_list_when_no_users_exist` 比 `test_get_users_2` 更易于理解。
- 不要模拟你无法控制的组件——只需对外部库编写薄层的封装层，并对这些封装层进行模拟。
- 集成测试能够发现单元测试可能遗漏的错误，不要跳过它们。
- 对于基于文件的测试，可以使用 `tmp_path`（Python）、`t.TempDir()`（Go）或 `tempfile`（Node.js）等工具来管理临时文件。
- 快照测试（snapshot tests）有助于检测意外的代码更改，但不适合处理格式变化的情况。