---
name: zod
description: Zod v4的最佳实践、模式以及API指南，涵盖了TypeScript应用程序中的模式验证、解析、错误处理和类型推断等方面。内容包括`safeParse`、对象组合、类型优化、数据转换、自定义类型（branded types）以及从Zod v3到Zod v4的迁移方法。基准版本为Zod ^4.0.0。触发条件包括：`zod`的导入语句、`z.object`、`z.string`、`z.infer`等函数的使用，以及任何提及“Zod”、“模式验证”、“Zod v4”或“Zod enum”的内容。
license: MIT
user-invocable: false
agentic: false
compatibility: "TypeScript ^5.5 projects using zod ^4.0.0"
metadata:
  author: Anivar Aravind
  author_url: https://anivar.net
  source_url: https://github.com/anivar/zod-skill
  version: 1.0.0
  tags: zod, validation, schema, typescript, parsing, type-inference, forms, api
---
# Zod

**重要提示：** 关于 `zod` 的培训数据可能已经过时或不准确——Zod v4 对字符串格式、枚举类型、错误处理以及递归类型进行了重大修改。请始终以本技能指南中的规则文件和项目的实际源代码作为权威信息来源。当 v3 的使用方式与最新文档冲突时，切勿依赖记忆中的旧规则。

## 何时使用 Zod

Zod 用于 **运行时类型验证**——在系统边界（如 API 输入、表单数据、环境变量、外部服务）解析不可信的数据。对于仅需要在编译时处理的类型，使用普通的 TypeScript 即可。

| 需求 | 推荐工具 |
|------|-----------------|
| API 输入/输出验证 | **Zod** |
| 表单验证（React、Vue） | **Zod**（结合 `react-hook-form`、`formik` 等工具） |
| 环境变量解析 | **Zod**（结合 `t3-env` 或手动解析） |
| 仅用于编译时的类型 | 普通 TypeScript |
| 小型代码包（约 1KB） | **Valibot** |
| 最高级别的类型推断 | **ArkType** |

## 规则类别及优先级

| 优先级 | 类别 | 影响程度 | 前缀 |
|----------|----------|--------|--------|
| 1 | 解析与类型安全 | 关键 | `parse-` |
| 2 | 模式设计 | 关键 | `schema-` |
| 3 | 优化与转换 | 高 | `refine-` |
| 4 | 错误处理 | 高 | `error-` |
| 5 | 性能与组合 | 中等 | `perf-` |
| 6 | v4 迁移 | 中等 | `migrate-` |
| 7 | 高级模式 | 中等 | `pattern-` |
| 8 | 架构与边界处理 | 关键/高 | `arch-` |
| 9 | 可观测性 | 高/中等 | `observe-` |

## 快速参考

### 1. 解析与类型安全（关键）

- `parse-use-safeParse` — 对用户输入使用 `safeParse()` 而不是可能抛出错误的 `parse()`  
- `parse-async-required` — 当模式包含异步优化时，必须使用 `parseAsync()` 或 `safeParseAsync()`  
- `parse-infer-types` — 使用 `z.infer<typename Schema>` 来推断输出类型；切勿手动重复定义类型  

### 2. 模式设计（关键）

- `schema-object-unknowns` — `z.object()` 会删除未知的键；使用 `strictObject` 或 `looseObject`  
- `schema-union-discriminated` — 对于带标签的联合类型，使用 `z.discriminatedUnion()` 而不是 `z.union()`  
- `schema-coercion-pitfalls` — `z.coerceboolean()` 会将 `"false"` 强制转换为 `true`；使用 `z.stringbool()`  
- `schema-recursive-types` — 对于递归模式，请使用 getter 模式；`z.lazy()` 在 v4 中已被移除  

### 3. 优化与转换（高）

- `refine-never-throw` — 在 `.refine()` 或 `.transform()` 中不要抛出异常；使用 `ctx.addIssue()`  
- `refine-vs-transform` — `.refine()` 用于验证，`.transform()` 用于转换，`.pipe()` 用于中间处理  
- `refine-cross-field` — 对父对象使用 `.superRefine()` 进行跨字段验证  

### 4. 错误处理（高）

- `error-custom-messages` — 使用 v4 的 `error` 参数；`required_error` 和 `invalid_type_error` 已被移除  
- `error-formatting` — 对于表单数据使用 `z.flattenError()`，对于嵌套数据使用 `z.treeifyError()`；`formatError` 已弃用  
- `error-input-security` — 在生产环境中切勿使用 `reportInput: true`，否则会泄露敏感信息  

### 5. 性能与组合（中等）

- `perf-extend-spread` — 对于大型模式，使用 `{ ...Schema.shape }` 来展开链式 `.extend()`  
- `perf-reuse-schemas` — 一次性定义模式，然后通过 `.pick()`、`.omit()`、`.partial()` 进行派生  
- `perf-zod-mini` — 为对代码包大小有严格要求的客户端应用使用 `zod/v4/mini`（1.88KB 版本）  

### 6. v4 迁移（中等）

- `migrate-string-formats` — 使用 `z.email()`、`z.uuid()`、`z.url()` 而不是 `z.string().email()`  
- `migrate-native-enum` — 使用统一的 `z.enum()` 来处理 TypeScript 枚举类型；`z.nativeEnum()` 已被移除  
- `migrate-error-api` — 在所有地方使用 `error` 参数；`message` 和 `errorMap` 已被移除  

### 7. 高级模式（中等）

- `pattern-branded-types` — 使用 `.brand("<Name">()` 进行命名类型定义（例如 USD 与 EUR）  
- `pattern-codecs` — 提供双向转换功能（解析 + 序列化）  
- `pattern-pipe` — 使用 `.pipe()` 进行分阶段的解析（字符串 → 数字 → 验证范围）  

### 8. 架构与边界处理（关键/高）

- `arch-boundary-parsing` — 在系统边界（API 处理器、环境变量、表单、数据获取）进行解析；将类型化的数据传递给业务逻辑  
- `arch-schema-organization` — 将模式与其边界层紧密结合；业务逻辑中的类型使用 `z.infer` 进行推断  
- `arch-schema-versioning` — 仅进行非破坏性的修改；新字段使用 `.optional()` 来标记  

### 9. 可观测性（高/中等）

- `observe-structured-errors` — 使用 `z.flattenError()` 生成包含请求关联 ID 的结构化日志  
- `observe-error-metrics` — 使用 `trackedSafeParse()` 在失败时记录每个模式和字段的统计信息  

## 模式类型快速参考

| 类型 | 语法 |
|------|--------|
| 字符串 | `z.string()` |
| 数字 | `z.number()`、`z.int()`、`z.float()` |
| 布尔值 | `zboolean()` |
| 大整数 | `z.bigint()` |
| 日期 | `z.date()` |
| 未定义 | `z.undefined()` |
| 空值 | `z_null()` |
| 空对象 | `z.void()` |
| 任意类型 | `z.any()` |
| 未知类型 | `z.unknown()` |
| 常量值 | `z.literal("foo")`、`z.literal(42)` |
| 枚举 | `z.enum(["a", "b"])`、`z.enum(TSEnum)` |
| 电子邮件地址 | `z.email()` |
| URL | `z.url()` |
| UUID | `z.uuid()` |
| 字符串→布尔值 | `z.stringbool()` |
| ISO 日期时间 | `z.iso.datetime()` |
| 文件 | `z.file()` |
| JSON | `z.json()` |
| 数组 | `z.array.Schema)` |
- 元组 | `z.tuple([a, b])` |
- 对象 | `z.object({})` |
- 严格对象 | `z.strictObject({})` |
- 松散对象 | `z.looseObject({})` |
- 记录 | `z.record(keySchema, valueSchema)` |
- 映射 | `z.map(keySchema, valueSchema)` |
- 集合 | `z.set.Schema)` |
- 联合类型 | `z.union([a, b])` |
- 带标签的联合类型 | `z.discriminatedUnion("key", [...])` |
- 交集类型 | `z.intersection(a, b)` |

## 使用方法

详细说明和代码示例请参阅各个规则文件：

```
rules/parse-use-safeParse.md
rules/schema-object-unknowns.md
```

每个规则文件包含：  
- 该规则的重要性的简要说明  
- 错误的代码示例及其原因  
- 正确的代码示例及其解释  
- 相关的上下文信息和决策表格  

## 参考资料

| 优先级 | 参考文档 | 阅读建议 |
|----------|-----------|-------------|
| 1 | `references/schema-types.md` | 所有基本类型、字符串格式、数字、枚举、日期类型的相关内容 |
| 2 | `references/parsing-and-inference.md` | 解析、`safeParse`、类型推断等相关内容 |
| 3 | `references/objects-and-composition.md` | 对象、数组、联合类型、选择/省略/部分提取、递归类型的相关内容 |
| 4 | `references/refinements-and-transforms.md` | 优化、转换、默认值设置等相关内容 |
| 5 | `references/error-handling.md` | 错误处理相关内容 |
| 6 | `references/advanced-features.md` | 高级功能（编码器、命名类型、JSON 模式等） |
| 7 | `references/anti-patterns.md` | 常见错误及其正确/错误的示例 |
| 8 | `references/boundary-architecture.md` | Zod 在 Express、tRPC、Next.js、React Hook Form、环境变量、外部 API 中的应用场景 |
| 9 | `references/linter-and-ci.md` | ESLint 规则、持续集成（CI）中的模式检查、未使用的模式检测、循环依赖关系等 |

## 完整编译后的文档

如需查看包含所有规则的完整指南，请参阅 `AGENTS.md`。