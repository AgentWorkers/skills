---
name: write-tests
description: 生成测试用例以实现覆盖目标
metadata: {"openclaw":{"requires":{"bins":["git"]}}}
user-invocable: true
---
# 编写测试代码

为指定的代码生成测试用例，以实现预定的覆盖率目标。

## 功能说明

1. 读取目标文件。
2. 分析需要测试的函数和类。
3. 识别边缘情况和错误场景。
4. 生成完整的测试文件。
5. 遵循项目的测试规范。

## 使用方法

```
/write-tests <path> [coverage]
```

**参数：**
- `path`（必填）：需要生成测试代码的文件或目录路径。
- `coverage`（可选）：目标覆盖率（默认值：80%）。

## 输出结果

生成的测试文件将遵循项目的约定：
- 对于 TypeScript，文件名为 `*.test.ts`。
- 对于 JavaScript，文件名为 `*.test.js`。
- 对于 Python，文件名为 `test_*.py`。

## 测试覆盖率

| 覆盖率 | 描述 |
|----------|-------------|
| 80% | 标准覆盖率（默认值） |
| 90% | 关键代码的高覆盖率 |
| 100% | 完全覆盖（包括边缘情况） |

## 测试内容

- **导出的函数**：所有公共函数。
- **类**：构造函数、公共方法。
- **边缘情况**：`null`、`undefined`、空值、边界值。
- **错误场景**：异常处理、验证错误。
- **异步代码**：Promise 的解析/拒绝。

## 测试结构（TypeScript/Jest）

```typescript
describe('FunctionName', () => {
  beforeEach(() => {
    // Setup
  });

  it('should handle normal input', () => {
    // Arrange
    // Act
    // Assert
  });

  it('should handle edge case', () => {
    // Test edge case
  });

  it('should throw error for invalid input', () => {
    expect(() => fn(invalid)).toThrow();
  });
});
```

## 示例

```
/write-tests src/utils/validator.ts 90
```

**输出结果：**
```
Generating tests for src/utils/validator.ts
Target coverage: 90%

Analyzing functions:
- validateEmail() - 3 test cases
- validatePassword() - 5 test cases
- validateUsername() - 4 test cases

Generated: src/utils/validator.test.ts

Test Summary:
- 12 test cases generated
- Estimated coverage: 92%

Run tests with: npm run test src/utils/validator.test.ts
```

## 测试规范

该工具遵循项目的测试规范：
- 对于 JavaScript/TypeScript，使用 Jest 进行测试。
- 对于 Python，使用 Pytest 进行测试。
- 如果可用，会使用现有的模拟工厂（mock factories）。
- 测试遵循 AAA 模式（Arrange、Act、Assert）。

## 下一步操作

生成测试代码后，使用相应的测试运行器执行它们：
- 对于 Jest，运行 `npm run test`。
- 对于 Python，运行 `pytest`。