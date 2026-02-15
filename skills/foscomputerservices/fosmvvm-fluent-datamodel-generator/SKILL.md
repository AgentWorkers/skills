---
name: fosmvvm-fluent-datamodel-generator
description: 为 FOSMVVM 的服务器端持久化生成流畅的数据模型（Fluent DataModels）。为基于数据库的实体生成模型框架（scaffolds）、数据迁移脚本（migrations）以及测试用例（tests）。
homepage: https://github.com/foscomputerservices/FOSUtilities
metadata: {"clawdbot": {"emoji": "🗄️", "os": ["darwin", "linux"]}}
---
# FOSMVVM Fluent 数据模型生成器

该工具用于根据 FOSMVVM 架构生成用于服务器端持久化的 Fluent 数据模型。

> **依赖项：** 本技能依赖于 [fosmvvm-fields-generator](../fosmvvm-fields-generator/SKILL.md) 来生成字段层（包括协议、消息和 YAML 数据结构）。在生成基于表单的模型之前，请先运行该工具。

## 使用范围说明

本技能专门用于处理 **Fluent** 持久化层（通常应用于 Vapor 服务器应用程序中）。

**在以下情况下请停止使用并询问用户：**
- 项目不使用 Fluent 持久化框架；
- 目标平台仅为 iOS，且使用 CoreData、SwiftData 或 Realm 作为数据存储方案；
- 用户提到了非 Fluent 持久化框架；
- 你不确定项目是否使用 Fluent 持久化层。

**判断项目是否使用 Fluent 的依据：**
- `Package.swift` 文件中是否导入了 `fluent`、`fluent-postgres-driver`、`fluent-sqlite-driver` 等库；
- 现有模型中是否使用了 `@ID`、`@Field`、`@Parent`、`@Children`、`@Siblings` 等属性装饰器；
- 项目中是否存在 `Migrations/` 目录以及相关的迁移脚本；
- 项目导入的库中是否包含 `FluentKit` 或 `Fluent`。

如果项目未使用 Fluent，请告知用户：“此技能用于生成服务器端持久化的 Fluent 数据模型。您的项目似乎不使用 Fluent 持久化框架，您希望如何继续？”

---

## 使用场景

- 用户需要创建新的模型/实体/表；
- 用户希望为某些数据类型（如用户、想法、文档等）添加数据库支持；
- 用户需要对某个新实体进行 CRUD 操作；
- 需要为新的实体创建持久化层。

## 架构背景

在 FOSMVVM 中，**Model** 是核心组件，负责数据的读取和写入操作。

有关完整架构信息，请参阅 [FOSMVVMArchitecture.md](../../docs/FOSMVVMArchitecture.md) 或 [OpenClaw 参考文档](../references/FOSMVVMArchitecture.md)。

### 架构中的数据模型

```
                    ┌─────────────────────────────────────┐
                    │         Fluent DataModel            │
                    │    (implements Model + Fields)      │
                    │                                     │
                    │  • All fields (system + user)       │
                    │  • Relationships (@Parent, etc.)    │
                    │  • Timestamps, audit fields         │
                    │  • Persistence logic                │
                    └──────────────┬──────────────────────┘
                                   │
              ┌────────────────────┼────────────────────────┐
              │                    │                        │
              ▼                    ▼                        ▼
    ┌─────────────────┐  ┌─────────────────┐    ┌─────────────────┐
    │ ViewModelFactory│  │  CreateRequest  │    │  UpdateRequest  │
    │   (projector)   │  │   RequestBody   │    │   RequestBody   │
    │                 │  │                 │    │                 │
    │ → ViewModel     │  │ → persists to   │    │ → updates       │
    │   (projection)  │  │   DataModel     │    │   DataModel     │
    └─────────────────┘  └─────────────────┘    └─────────────────┘
```

### 字段（Fields）与数据模型（DataModel）的区别

- **字段协议（Fields Protocol）**：表示用户通过表单输入的数据（可编辑的部分）；
  - 包括用户输入的内容、验证规则、标签和占位符；
  - 不包含关联关系或系统自动分配的字段。
- **数据模型（DataModel）**：表示完整的实体结构（包含系统自动分配的字段，如 `createdBy`、`timestamp`）；
  - 包含所有字段及关联关系（`@Parent`、`@Children`、`@Siblings`）；
  - 支持 Fluent 的属性装饰器及迁移逻辑。

**并非所有实体都需要字段：**
- 会话相关的数据（如用户认证信息）：仅使用数据模型；
- 审计记录：由系统自动生成，仅使用数据模型；
- 用于连接不同表的中间表：仅使用数据模型。

---

## 文件结构

每个基于表单的模型都需要在多个目标平台上生成相应的文件：

```
── fosmvvm-fields-generator ──────────────────────────────────
{ViewModelsTarget}/                  (shared protocol layer)
  FieldModels/
    {Model}Fields.swift              ← Protocol + Enum + Validation
    {Model}FieldsMessages.swift      ← Localization message struct

{ResourcesPath}/                     (localization resources)
  FieldModels/
    {Model}FieldsMessages.yml        ← YAML localization strings

── fosmvvm-fluent-datamodel-generator (this skill) ───────────
{WebServerTarget}/                   (server implementation)
  DataModels/
    {Model}.swift                    ← Fluent model (implements protocol)
  Migrations/
    {Model}+Schema.swift             ← Table creation migration
    {Model}+Seed.swift               ← Seed data migration

Tests/
  {ViewModelsTarget}Tests/
    FieldModels/
      {Model}FieldsTests.swift       ← Unit tests

database.swift                       ← Register migrations
```

---

## 使用方法

**调用方式：**
`/fosmvvm-fluent-datamodel-generator`

**前提条件：**
- 通过交流明确了解模型的结构；
- 如果模型基于表单生成，需先使用 `fosmvvm-fields-generator` 创建字段协议；
- 确定模型中的关联关系及系统自动分配的字段；
- 确认项目使用 Fluent 作为持久化框架。

**工作流程：**
本技能用于基于 Fluent 框架实现服务器端数据持久化。对于基于表单的模型，需先运行 `fosmvvm-fields-generator` 生成字段协议。该工具会自动根据交流内容生成相应的文件结构，无需手动提供文件路径或额外信息。

## 实现逻辑

- **模型类型识别**：根据用户交流内容判断模型的用途（用户数据、系统记录、审计日志等）；
- **关联关系分析**：根据已有信息分析模型中的关联关系类型（一对一、多对多关系）；
- **字段分类**：区分用户可编辑的字段、系统自动分配的字段以及计算出的关联关系。

### 文件生成顺序

- 如果模型基于表单生成（已存在字段协议）：
  1. 先使用 `fosmvvm-fields-generator` 创建字段层；
  2. 生成引用字段协议的数据模型；
  3. 执行数据库模式迁移；
  4. 生成初始数据（seed data）；
  5. 进行测试；
  6. 注册迁移脚本。

- 如果模型仅由系统生成（无需字段协议）：
  1. 直接生成数据模型结构；
  2. 执行数据库模式迁移；
  3. （如需要）生成初始数据；
  4. 进行测试；
  5. 注册迁移脚本。

### 设计验证

在生成数据模型之前，工具会进行以下验证：
- 确认模型是否需要表单输入；
- 检查关联关系的实现方式（多对多关系使用中间表，外键使用 `@Parent`）；
- 确保关联关系的命名清晰易懂；
- 确保用户可编辑的字段与系统自动分配的字段分开存储。

### 信息来源

工具的信息来源包括：
- 之前的交流内容（模型需求和关联关系）；
- `Fields Protocol` 的具体内容；
- 项目代码库中的数据库模式；
- 项目中的现有迁移脚本。

---

## 文件模板

完整的文件模板请参阅 [reference.md](reference.md)。

---

## 关键设计模式

### Fluent 数据模型（Fluent DataModel）

```swift
import FluentKit
import FOSFoundation
import FOSMVVM
import FOSMVVMVapor
import Foundation

final class {Model}: DataModel, {Model}Fields, Hashable, @unchecked Sendable {
    static let schema = "{models}"  // snake_case plural

    @ID(key: .id) var id: ModelIdType?

    // Fields from protocol
    @Field(key: "field_name") var fieldName: FieldType

    // Validation messages
    let {model}ValidationMessages: {Model}FieldsMessages

    // Timestamps
    @Timestamp(key: "created_at", on: .create) var createdAt: Date?
    @Timestamp(key: "updated_at", on: .update) var updatedAt: Date?

    // CRITICAL: Initialize validationMessages FIRST
    init() {
        self.{model}ValidationMessages = .init()
    }

    init(id: ModelIdType? = nil, fieldName: FieldType) {
        self.{model}ValidationMessages = .init()  // FIRST!
        self.id = id
        self.fieldName = fieldName
    }
}
```

### 关联关系（Associated Types Pattern）

**设计原则：** 使用 **关联类型（Associated Types）** 可避免代码中的“存在性类型（Existential Types）”。在使用关联类型之前，请务必思考是否有更合适的替代方案。

对于必须存在的关联关系，应在协议中明确指定关联类型：

```swift
public protocol IdeaFields: ValidatableModel, Codable, Sendable {
    associatedtype User: UserFields

    var createdBy: User { get set }
}
```

在 Fluent 数据模型中，`@Parent` 属性直接表示关联关系：

```swift
final class Idea: DataModel, IdeaFields, Hashable, @unchecked Sendable {
    @Parent(key: "created_by") var createdBy: User
    // No computed property needed - @Parent satisfies the associated type directly
}
```

在数据库模式中，关联关系的定义如下：
`.field("created_by", .uuid, .required, .references(User.schema, "id", onDelete: .cascade))`

**使用场景：**
- **关联类型（Associated Type）**：用于表示必须存在的关联关系（例如 `User Fields`）；
- **可选关联类型（Optional Associated Type）**：不推荐使用；对于可选的外键，可以使用 `ModelIdType?`；
- **普通 `ModelIdType`**：用于表示可选的外键或外部系统引用。

### 迁移脚本（Migrations）

- 数据库模式迁移文件名格式为 `"{Model.schema}-initial"`；
- 初始化数据迁移文件名格式为 `"{Model.schema}-seed"`；
- 初始化操作会考虑运行环境（调试、测试、生产环境）；
- 初始化操作是幂等的（`guard count() == 0`）。

### PostgreSQL 特性下的 SQL 编写

对于 PostgreSQL 的特殊特性（如 `tsvector`、`LTREE` 等），请使用 `SQLKit`：

```swift
import Fluent
import SQLKit  // Required for raw SQL

// In prepare():
guard let sql = database as? any SQLDatabase else { return }

let schema = Model.schema
try await sql.raw(SQLQueryString("ALTER TABLE \(unsafeRaw: schema) ADD COLUMN search_vector tsvector")).run()
```

**注意事项：**
- 必须导入 `SQLKit`（而不仅仅是 `Fluent`）；
- 在 SQL 语句中，使用 `database as? any SQLDatabase` 进行类型转换；
- 使用 `SQLQueryString` 和 `\(unsafeRaw:)` 来处理数据库特有的字段。

### 测试

- 使用 `@Suite` 注解为测试方法命名；
- 测试方法需遵循 `LocalizableTestCase` 标准；
- 测试所有表单字段；
- 使用 `@Test(arguments:)` 方法进行验证；
- 为包含关联关系的模型创建专门的测试结构。

### 命名规范

| 类型 | 命名规则 | 举例 |
|---------|------------|---------|
| 模型类 | 使用 PascalCase 单数形式 | `User`、`Idea` |
| 表名 | 使用 snake_case 复数形式 | `users`、`ideas` |
| 字段名 | 使用 snake_case | `created_at`、`user_id` |
- 枚举值 | 使用 camelCase | `searchLanguage`、`inProgress` |
- 枚举的原始值 | 使用 snake_case | `"search_language"`、`in_progress"` |
- 协议名称 | 使用 `{Model}Fields` | `UserFields`、`IdeaFields` |
- 消息结构 | 使用 `{Model}FieldsMessages` | `UserFieldsMessages` |

## 常见字段类型

| Swift 类型 | Fluent 类型 | 数据库类型 |
|------------|-------------|----------|
| `String` | `.string` | `VARCHAR/TEXT` |
| `Int` | `.int` | `INTEGER` |
| `Bool` | `.bool` | `BOOLEAN` |
| `Date` | `.datetime` | `TIMESTAMPTZ` |
| `UUID` | `.uuid` | `UUID` |
| `[UUID]` | `.array(of: .uuid)` | `UUID[]` |
| 自定义枚举 | `.string` | `VARCHAR`（以原始字符串形式存储） |
| `JSONB` | `.json` | `JSONB` |

---

**相关资源**

- [FOSMVVMArchitecture.md](../../docs/FOSMVVMArchitecture.md)：完整的 FOSMVVM 架构文档；
- [fosmvvm-fields-generator](../fosmvvm-fields-generator/SKILL.md)：用于表单验证的字段生成工具；
- [fosmvvm-viewmodel-generator](../fosmvvm-viewmodel-generator/SKILL.md)：用于从数据模型生成视图模型的工具；
- [reference.md](reference.md)：包含所有文件模板的参考文档。

---

## 版本历史

| 版本 | 更新日期 | 主要变更 |
|---------|------|---------|
| 1.0 | 2025-12-23 | 基于 SystemConfig 模式初步实现该技能；|
| 1.1 | 2025-12-23 | 添加了关联关系相关的设计模式、初始化顺序和依赖项列表；|
| 1.2 | 2025-12-23 | 优化了关联类型的处理方式、SQL 编写规则和测试结构；|
| 1.3 | 2025-12-24 | 将字段生成逻辑分离到独立的 `fields-generator` 工具中；|
| 2.0 | 2025-12-26 | 重新命名技能名称为 `fosmvvm-fluent-datamodel-generator`，优化了使用范围判断逻辑，使其适用于 FOSMVVM 的通用架构；|
| 2.1 | 2026-01-24 | 采用基于上下文的信息处理方式，不再依赖文件路径或用户输入，直接根据交流内容生成文件结构。