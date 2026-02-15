---
name: architecture-decision-records-(adrs)
model: reasoning
---

# 架构决策记录（Architecture Decision Records, ADRs）

## 什么是架构决策记录（ADR）？
架构决策记录是一种轻量级的文档，用于记录重要技术决策的背景、决策过程及其后果。这些记录成为了项目开发过程中各项决策的“制度性记忆”，有助于解释各项设计决策的依据。

## 何时需要编写ADR？
- 在采用新的框架或技术时
- 在不同架构方案之间进行选择时
- 在决定使用何种数据库或基础设施时
- 在定义API设计模式时
- 在做出任何难以撤销或日后难以理解的决策时

## 相关术语：
ADR（Architecture Decision Record）、技术文档、决策日志、MADR（Major Architecture Decision Record）、RFC（Request for Comment）、设计决策、权衡因素

---

## 快速判断：是否需要编写ADR？
| 是否需要编写ADR | 是否可以跳过ADR |
|------------|-------------|
| 采用新的框架/语言 | 进行小版本升级时 |
| 选择数据库技术 | 修复漏洞时 |
| 定义API设计模式 | 提供实现细节时 |
| 决定安全架构 | 进行常规维护时 |
| 选择集成方案 | 修改配置时 |
| 引入重大变更 | 调整代码格式时 |

---

## ADR的生命周期
**已接受的ADR严禁修改**——只能通过编写新的ADR来替换原有的记录。

---

## 模板：
### 模板1：标准模板（直接使用）
```markdown
# ADR-NNNN: [Title]

## Status
[Proposed | Accepted | Deprecated | Superseded by ADR-XXXX]

## Context
[What is the issue? What forces are at play? 2-3 paragraphs max.]

## Decision
We will [decision statement].

## Consequences

### Positive
- [Benefit 1]
- [Benefit 2]

### Negative
- [Drawback 1]
- [Drawback 2]

### Risks
- [Risk and mitigation]

## Related
- ADR-XXXX: [Related decision]
```

### 模板2：详细模板（适用于重大决策）
```markdown
# ADR-0001: Use PostgreSQL as Primary Database

## Status
Accepted

## Context
We need to select a primary database for our e-commerce platform handling:
- ~10,000 concurrent users
- Complex product catalog with hierarchical categories
- Transaction processing for orders and payments
- Full-text search for products

The team has experience with MySQL, PostgreSQL, and MongoDB.

## Decision Drivers
- **Must have** ACID compliance for payment processing
- **Must support** complex queries for reporting  
- **Should support** full-text search to reduce infrastructure
- **Should have** good JSON support for flexible product attributes

## Considered Options

### Option 1: PostgreSQL
**Pros**: ACID compliant, excellent JSONB support, built-in full-text search, PostGIS
**Cons**: Slightly more complex replication than MySQL

### Option 2: MySQL
**Pros**: Familiar to team, simple replication
**Cons**: Weaker JSON support, no built-in full-text search

### Option 3: MongoDB
**Pros**: Flexible schema, native JSON
**Cons**: No ACID for multi-document transactions, team has limited experience

## Decision
We will use **PostgreSQL 15** as our primary database.

## Rationale
PostgreSQL provides the best balance of ACID compliance (essential for e-commerce), 
built-in capabilities (reduces infrastructure), and team familiarity.

## Consequences

### Positive
- Single database handles transactions, search, and geospatial
- Reduced operational complexity
- Strong consistency for financial data

### Negative
- Need PostgreSQL-specific training for team
- Vertical scaling limits may require read replicas

### Risks
- Full-text search may not scale as well as Elasticsearch
- **Mitigation**: Design for potential ES addition if needed

## Implementation Notes
- Use JSONB for flexible product attributes
- Implement connection pooling with PgBouncer
- Set up streaming replication for read replicas

## Related
- ADR-0002: Caching Strategy (Redis)
- ADR-0005: Search Architecture
```

### 模板3：简化模板（适用于较小决策）
```markdown
# ADR-0012: Adopt TypeScript for Frontend

**Status**: Accepted  
**Date**: 2024-01-15  
**Deciders**: @alice, @bob

## Context
React codebase has 50+ components with increasing bugs from prop type mismatches.

## Decision
Adopt TypeScript for all new frontend code. Migrate existing code incrementally.

## Consequences
**Good**: Catch type errors at compile time, better IDE support  
**Bad**: Learning curve, initial slowdown  
**Mitigation**: Training sessions, `allowJs: true` for gradual adoption
```

### 模板4：简短声明模板（一行总结）
```markdown
# ADR-0015: API Gateway Selection

In the context of **building a microservices architecture**,
facing **the need for centralized API management and rate limiting**,
we decided for **Kong Gateway**
and against **AWS API Gateway and custom Nginx**,
to achieve **vendor independence and plugin extensibility**,
accepting that **we need to manage Kong infrastructure ourselves**.
```

### 模板5：弃用说明模板
```markdown
# ADR-0020: Deprecate MongoDB in Favor of PostgreSQL

## Status
Accepted (Supersedes ADR-0003)

## Context
ADR-0003 (2021) chose MongoDB for user profiles. Since then:
- MongoDB transactions remain problematic for our use case
- Our schema has stabilized and rarely changes
- Maintaining two databases increases operational burden

## Decision
Deprecate MongoDB and migrate user profiles to PostgreSQL.

## Migration Plan
1. **Week 1-2**: Create PostgreSQL schema, enable dual-write
2. **Week 3-4**: Backfill historical data, validate consistency
3. **Week 5**: Switch reads to PostgreSQL
4. **Week 6**: Remove MongoDB writes, decommission

## Lessons Learned
- Schema flexibility benefits were overestimated
- Operational cost of multiple databases was underestimated
```

---

## 目录结构：
```
docs/
└── adr/
    ├── README.md              # Index and guidelines
    ├── template.md            # Team's ADR template
    ├── 0001-use-postgresql.md
    ├── 0002-caching-strategy.md
    ├── 0003-mongodb-user-profiles.md  # [DEPRECATED]
    └── 0020-deprecate-mongodb.md      # Supersedes 0003
```

### ADR索引（README.md）
```markdown
# Architecture Decision Records

| ADR | Title | Status | Date |
|-----|-------|--------|------|
| [0001](0001-use-postgresql.md) | Use PostgreSQL | Accepted | 2024-01-10 |
| [0002](0002-caching-strategy.md) | Caching with Redis | Accepted | 2024-01-12 |
| [0003](0003-mongodb-user-profiles.md) | MongoDB for Profiles | Deprecated | 2023-06-15 |
| [0020](0020-deprecate-mongodb.md) | Deprecate MongoDB | Accepted | 2024-01-15 |

## Creating a New ADR
1. Copy `template.md` to `NNNN-title-with-dashes.md`
2. Fill in template, submit PR for review
3. Update this index after approval
```

---

## 工具：adr-tools
```bash
# Install
brew install adr-tools

# Initialize
adr init docs/adr

# Create new ADR
adr new "Use PostgreSQL as Primary Database"

# Supersede an ADR
adr new -s 3 "Deprecate MongoDB in Favor of PostgreSQL"

# Generate index
adr generate toc > docs/adr/README.md
```

---

## 审查 checklist：
在提交ADR之前：
- [ ] 文档清晰地解释了问题的背景
- [ ] 已考虑了所有可行的选项
- [ ] 充分、客观地分析了各选项的优缺点
- [ ] 记录了决策的所有后果（正面和负面影响）

在审查过程中：
- [ ] 至少有2位资深工程师参与审查
- [ ] 已与受影响的团队进行了沟通
- [ ] 已考虑了安全方面的影响
- [ ] 已评估了决策的可撤销性

在ADR被接受后：
- [ ] 更新了ADR索引
- [ ] 通知了相关团队
- [ ] 创建了相应的实施任务单

---

**注意事项**：
- **严禁修改已接受的ADR**：只能通过编写新的ADR来替换原有记录。
- **不要省略决策背景**：未来的读者需要了解决策的依据。
- **不要隐瞒失败的决定**：即使决策被否决，它们也是宝贵的学习资源。
- **表述要具体**：决策和后果都必须明确。
- **不要忽略实施细节**：ADR的作用在于指导后续的实施工作。
- **避免过度冗长**：文档长度应控制在1-2页以内。
- **及时编写**：应在实施开始之前完成文档的编写。