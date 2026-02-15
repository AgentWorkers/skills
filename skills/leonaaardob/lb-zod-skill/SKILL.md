---
name: zod
description: 完整的 Zod 验证库文档。适用于处理 Zod 模式验证、TypeScript 类型推断、表单验证、API 验证、错误处理以及数据解析等场景。内容包括模式定义、优化方法、数据转换、错误自定义以及与相关生态系统的集成。
---

# Zod 文档

这是一个完整的 Zod 验证库文档，采用 Markdown 格式编写。您可以通过阅读 `references/` 目录中的文件来了解关于模式验证、类型推断和错误处理的相关信息。

## 文档结构

所有文档都存储在 `references/` 目录中，并按主题进行分类：

### 核心文档

#### 入门
- `index.mdx` - 介绍和快速入门
- `basics.mdx` - 基本用法和模式定义

#### API 参考
- `api.mdx` - 完整的 API 文档
  - 原始类型（字符串、数字、布尔值等）
  - 复合类型（对象、数组、元组、联合类型等）
  - 模式方法（`parse`、`safeParse`、`parseAsync` 等）
  - 优化和转换
  - 类型推断
  - 错误处理

#### 高级功能
- `error-formatting.mdx` - 错误格式化和自定义
- `error-customization.mdx` - 自定义错误信息
- `codecs.mdx` - 序列化和反序列化
- `json-schema.mdx` - JSON 模式生成
- `metadata.mdx` - 模式元数据

#### 集成与生态系统
- `ecosystem.mdx` - 社区包和集成方案
- `library-authors.mdx` - 库作者指南
- `packages/` - 相关包

#### Zod 4.0 版本
- `v4/` - Zod 4.0 的新特性和迁移指南

## 快速参考

### 常见任务

| 任务 | 需要阅读的文件 |
|------|--------------|
| 入门 | `index.mdx`, `basics.mdx` |
| 定义模式 | `api.mdx`（原始类型部分） |
| 对象验证 | `api.mdx`（对象部分） |
| 数组验证 | `api.mdx`（数组部分） |
| 联合类型 | `api.mdx`（联合类型部分） |
| 优化 | `api.mdx`（优化部分） |
| 转换 | `api.mdx`（转换部分） |
| 错误处理 | `error-formatting.mdx`, `error-customization.mdx` |
| 类型推断 | `api.mdx`（类型推断部分） |
| 异步验证 | `api.mdx`（异步部分） |
| JSON 模式 | `json-schema.mdx` |
| 自定义错误信息 | `error-customization.mdx` |
| 生态系统 | `ecosystem.mdx` |

### 模式示例

**原始类型：**
```typescript
z.string()
z.number()
z.boolean()
z.date()
z.undefined()
z.null()
z.any()
z.unknown()
```

**复合类型：**
```typescript
z.object({ ... })
z.array(z.string())
z.tuple([z.string(), z.number()])
z.union([z.string(), z.number()])
z.record(z.string())
z.map(z.string(), z.number())
z.set(z.string())
```

**优化：**
```typescript
z.string().email()
z.string().url()
z.string().uuid()
z.number().min(5).max(10)
z.string().regex(/pattern/)
```

**转换：**
```typescript
z.string().transform(val => val.toUpperCase())
z.coerce.number()
```

### 适用场景

- 在 React/Next.js 中进行表单验证
- API 请求/响应的验证
- 环境变量的解析
- 运行时类型检查
- 数据的转换和解析
- 自定义错误信息
- 与 tRPC、React Hook Form 等工具的集成
- 从模式生成 TypeScript 类型

### 如何导航

1. 首先阅读 `index.mdx` 以获取简介。
2. 了解基本用法，请阅读 `basics.mdx`。
3. 查阅 API 详细信息，请参考 `api.mdx`。
4. 有关错误处理，请参阅 `error-formatting.mdx` 和 `error-customization.mdx`。
5. 了解高级功能，请浏览 `codecs.mdx`、`json-schema.mdx` 和 `metadata.mdx`。
6. 有关集成方案，请查看 `ecosystem.mdx`。
7. 了解 Zod 4.0 的新特性，请查看 `v4/` 目录。

所有文件均为 `.mdx` 格式（Markdown + JSX），但也可以直接作为纯 Markdown 文本阅读。