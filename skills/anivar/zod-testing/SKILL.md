---
name: zod-testing
description: >
  使用 Jest 和 Vitest 对 Zod 模型进行测试的技巧。内容包括模型正确性测试、模拟数据的生成、错误断言方式、与 API 处理程序及表单的集成测试、使用 `z.toJSONSchema()` 进行的快照测试，以及基于属性的测试。基准版本：Zod 4.0.0。触发条件包括：包含 Zod 模型的测试文件、`zod-schema-faker` 的导入语句，以及任何提及“test schema”、“schema test”、“zod mock”、“zod test”或模型测试相关内容的代码。
  （Note: The translation has been adjusted to fit the Chinese language context and grammar rules. Some terms have been simplified for clarity, such as “zod-schema-faker” being translated as “zod-schema-faker” instead of “zod-schema-faker import”.）
license: MIT
user-invocable: false
agentic: false
compatibility: "zod ^4.0.0, Jest or Vitest, TypeScript ^5.5"
metadata:
  author: Anivar Aravind
  author_url: https://anivar.net
  source_url: https://github.com/anivar/zod-testing
  version: 1.0.0
  tags: zod, testing, jest, vitest, mock-data, property-testing, schema-validation
---
# Zod模式测试指南

**重要提示：** 关于Zod模式测试的培训资料可能已经过时——Zod v4更改了错误格式，移除了`z.nativeEnum()`方法，并引入了`z.toJSONSchema()`等新API。请始终以本文档和项目的实际源代码作为参考依据。

## 测试优先级

1. **模式正确性**：该模式能否接受有效数据并拒绝无效数据？
2. **错误信息**：模式是否能够生成正确的错误信息和错误代码？
3. **集成性**：该模式能否与API处理器、表单、数据库层正确配合使用？
4. **边缘情况**：边界值、可选字段/可空字段的组合、空输入等。

## 核心模式

```typescript
import { describe, it, expect } from "vitest" // or jest
import { z } from "zod"

const UserSchema = z.object({
  name: z.string().min(1),
  email: z.email(),
  age: z.number().min(0).max(150),
})

describe("UserSchema", () => {
  it("accepts valid data", () => {
    const result = UserSchema.safeParse({
      name: "Alice",
      email: "alice@example.com",
      age: 30,
    })
    expect(result.success).toBe(true)
  })

  it("rejects missing required fields", () => {
    const result = UserSchema.safeParse({})
    expect(result.success).toBe(false)
    if (!result.success) {
      const flat = z.flattenError(result.error)
      expect(flat.fieldErrors.name).toBeDefined()
      expect(flat.fieldErrors.email).toBeDefined()
    }
  })

  it("rejects invalid email", () => {
    const result = UserSchema.safeParse({
      name: "Alice",
      email: "not-an-email",
      age: 30,
    })
    expect(result.success).toBe(false)
  })

  it("rejects negative age", () => {
    const result = UserSchema.safeParse({
      name: "Alice",
      email: "alice@example.com",
      age: -1,
    })
    expect(result.success).toBe(false)
  })
})
```

## 测试方法

| 方法 | 目的 | 适用场景 |
|----------|---------|----------|
| `safeParse()`结果检查 | 检查模式正确性 | 测试时始终使用`safeParse()`方法 |
| `z.flattenError()`断言 | 错误信息测试 | 验证特定字段的错误情况 |
| `z.toJSONSchema()`快照 | 模式结构测试 | 检测意外的模式变更 |
| 伪造数据生成 | 测试用例创建 | 需要有效或随机化的测试数据 |
| 基于属性的测试 | 模糊测试 | 模式必须能够处理任意有效的输入 |
| 结构测试 | 确保模式仅在边界条件下被正确导入 |
| 变化检测 | 回归测试 | 通过JSON模式快照捕捉意外的模式变更 |

## 模式正确性测试

### 测试时始终使用`safeParse()`

```typescript
// GOOD: test doesn't crash — asserts on result
const result = schema.safeParse(invalidData)
expect(result.success).toBe(false)

// BAD: test crashes instead of failing
expect(() => schema.parse(invalidData)).toThrow()
// If schema changes and starts accepting, this still passes
```

### 同时测试有效数据和无效数据

```typescript
describe("EmailSchema", () => {
  const valid = ["user@example.com", "a@b.co", "user+tag@domain.org"]
  const invalid = ["", "not-email", "@missing.com", "user@", "user @space.com"]

  it.each(valid)("accepts %s", (email) => {
    expect(z.email().safeParse(email).success).toBe(true)
  })

  it.each(invalid)("rejects %s", (email) => {
    expect(z.email().safeParse(email).success).toBe(false)
  })
})
```

### 测试边界值

```typescript
const AgeSchema = z.number().min(0).max(150)

it("accepts minimum boundary", () => {
  expect(AgeSchema.safeParse(0).success).toBe(true)
})

it("accepts maximum boundary", () => {
  expect(AgeSchema.safeParse(150).success).toBe(true)
})

it("rejects below minimum", () => {
  expect(AgeSchema.safeParse(-1).success).toBe(false)
})

it("rejects above maximum", () => {
  expect(AgeSchema.safeParse(151).success).toBe(false)
})
```

## 错误断言方法

### 断言特定字段的错误

```typescript
it("shows correct error for invalid email", () => {
  const result = UserSchema.safeParse({ name: "Alice", email: "bad", age: 30 })
  expect(result.success).toBe(false)
  if (!result.success) {
    const flat = z.flattenError(result.error)
    expect(flat.fieldErrors.email).toBeDefined()
    expect(flat.fieldErrors.email![0]).toContain("email")
  }
})
```

### 断言错误代码

```typescript
it("produces correct error code", () => {
  const result = z.number().safeParse("not a number")
  expect(result.success).toBe(false)
  if (!result.success) {
    expect(result.error.issues[0].code).toBe("invalid_type")
  }
})
```

### 断言自定义错误信息

```typescript
const Schema = z.string({ error: "Name is required" }).min(1, "Name cannot be empty")

it("shows custom error for missing field", () => {
  const result = Schema.safeParse(undefined)
  expect(result.success).toBe(false)
  if (!result.success) {
    expect(result.error.issues[0].message).toBe("Name is required")
  }
})
```

## 伪造数据生成

### 使用`zod-schema-faker`库

```typescript
import { install, fake } from "zod-schema-faker"
import { z } from "zod"

install(z) // call once in test setup

const UserSchema = z.object({
  name: z.string().min(1),
  email: z.email(),
  age: z.number().min(0).max(150),
})

it("schema accepts generated data", () => {
  const mockUser = fake(UserSchema)
  expect(UserSchema.safeParse(mockUser).success).toBe(true)
})
```

### 为确定性测试生成固定种子数据

```typescript
import { seed, fake } from "zod-schema-faker"

beforeEach(() => {
  seed(12345) // deterministic output
})

it("generates consistent mock data", () => {
  const user = fake(UserSchema)
  expect(user.name).toBeDefined()
})
```

## 使用JSON模式进行快照测试

```typescript
it("schema shape has not changed", () => {
  const jsonSchema = z.toJSONSchema(UserSchema)
  expect(jsonSchema).toMatchSnapshot()
})
```

这种方法可以在代码审查过程中捕捉到意外的模式变更。快照显示了Zod模式的JSON表示形式。

## 集成测试

### API处理器测试

```typescript
it("API rejects invalid request body", async () => {
  const response = await request(app)
    .post("/api/users")
    .send({ name: "", email: "invalid" })
    .expect(400)

  expect(response.body.errors).toBeDefined()
  expect(response.body.errors.fieldErrors.email).toBeDefined()
})
```

### 表单验证测试

```typescript
it("form shows validation errors", () => {
  const result = FormSchema.safeParse(formData)
  if (!result.success) {
    const errors = z.flattenError(result.error)
    // Pass errors to form library
    expect(errors.fieldErrors).toHaveProperty("email")
  }
})
```

## 基于属性的测试

```typescript
import fc from "fast-check"
import { fake } from "zod-schema-faker"

it("schema always accepts its own generated data", () => {
  fc.assert(
    fc.property(fc.constant(null), () => {
      const data = fake(UserSchema)
      expect(UserSchema.safeParse(data).success).toBe(true)
    }),
    { numRuns: 100 }
  )
})
```

## 规则

1. **测试时始终使用`safeParse()`** — 使用`safeParse()`可以避免测试失败。
2. **同时测试有效数据和无效数据** — 不要只测试正常情况。
3. **测试边界值** — 对于数值类型，测试最小值、最大值以及它们的相邻值。
4. **测试可选字段/可空字段的组合** — 包括`undefined`、`null`和缺少键的情况。
5. **断言特定字段的错误** — 使用`z.flattenError()`来检查哪些字段出现了错误。
6. **不要测试模式的内部逻辑** — 只测试解析结果，而不是模式的结构或定义。
7. **使用`z.toJSONSchema()`快照** — 检测意外的模式变更。
8. **为测试生成随机数据** — 随机化的测试结果可能不稳定。
9. **分别测试输入验证和输出转换**。
10. **不要在断言中重复模式逻辑** — 测试行为，而不是实现细节。

## 避免的错误做法

请参阅[references/anti-patterns.md](references/anti-patterns.md)，了解以下错误做法的示例：

- 测试模式的内部逻辑而非其行为。
- 不测试错误情况。
- 在测试中使用`parse()`方法（这会导致测试崩溃而非失败）。
- 不测试边界值。
- 硬编码伪造数据而非动态生成数据。
- 使用原始的`ZodError`对象进行快照测试，而不是格式化后的输出。
- 不在边界条件下进行测试（模式测试通过，但处理器无法验证数据）。
- 不进行快照回归测试（模式变更可能未被发现）。
- 只测试模式的结构而不关注错误信息的表现。
- 没有设置变化检测机制（模式变更可能未被及时发现）。

## 参考资料

- [API参考](references/api-reference.md) — 测试模式、断言辅助工具、伪造数据生成方法。
- [避免的错误做法](references/anti-patterns.md) — 常见的测试错误及避免方法。