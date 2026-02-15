---
name: service-layer-architecture
model: standard
description: 控制器-服务-查询（Controller-Service-Query, C-S-Q）分层API架构，支持数据增强（data enrichment）和并行数据获取（parallel data fetching）功能。该架构适用于构建REST API或GraphQL解析器（GraphQL resolvers），能够实现职责的清晰分离（clean separation of concerns）。该架构涵盖了API架构（API architecture）、服务层（service layer）、控制器模式（controller pattern）、数据增强机制以及REST API的相关组件。
---

# 服务层架构

采用清晰、高效的API设计，合理划分职责，并实现并行数据获取功能。

---

## 使用场景

- 构建需要处理复杂数据聚合的REST API
- 需要从多个数据源获取数据的GraphQL解析器
- 任何需要将多个查询的结果合并在一起的API
- 需要可测试、易于维护的代码的系统

---

## 三层架构

```
┌─────────────────────────────────────────────────────┐
│  Controllers   │  HTTP handling, validation        │
├─────────────────────────────────────────────────────┤
│  Services      │  Business logic, data enrichment  │
├─────────────────────────────────────────────────────┤
│  Queries       │  Database access, raw data fetch  │
└─────────────────────────────────────────────────────┘
```

---

## 第一层：控制器（仅处理HTTP请求）

```typescript
// controllers/Entity.ts
import { getEntity, getEntities } from "../services/Entity";

const router = new Router();

router.get("/entity/:entityId", async (ctx) => {
  const { entityId } = ctx.params;

  if (!entityId) {
    ctx.status = 400;
    ctx.body = { error: "Invalid entity ID" };
    return;
  }

  const entity = await getEntity(entityId);
  
  if (!entity) {
    ctx.status = 404;
    ctx.body = { error: "Entity not found" };
    return;
  }
  
  ctx.status = 200;
  ctx.body = entity;
});
```

---

## 第二层：服务层（业务逻辑）

```typescript
// services/Entity.ts
import { queries } from "@common";

export const getEntityData = async (entity: RawEntity): Promise<EnrichedEntity> => {
  // Parallel fetch all related data
  const [metadata, score, activity, location] = await Promise.all([
    queries.getMetadata(),
    queries.getLatestScore(entity.id),
    queries.getActivity(entity.id),
    queries.getLocation(entity.slotId),
  ]);

  // Transform and combine
  return {
    ...entity,
    bonded: entity.bonded / Math.pow(10, metadata.decimals),
    total: score?.total ?? 0,
    location: location?.city,
    activity: {
      activeCount: activity?.active?.length ?? 0,
      inactiveCount: activity?.inactive?.length ?? 0,
    },
  };
};

export const getEntity = async (entityId: string): Promise<EnrichedEntity | null> => {
  const entity = await queries.getEntityById(entityId);
  if (!entity) return null;
  return getEntityData(entity);
};

export const getEntities = async (): Promise<EnrichedEntity[]> => {
  const all = await queries.allEntities();
  const enriched = await Promise.all(all.map(getEntityData));
  return enriched.sort((a, b) => b.total - a.total);
};
```

---

## 第三层：查询层（数据库访问）

```typescript
// queries/Entities.ts
import { EntityModel } from "../models";

export const allEntities = async () => {
  return EntityModel.find({}).lean();  // Always use .lean()
};

export const getEntityById = async (id: string) => {
  return EntityModel.findOne({ id }).lean();
};

export const validEntities = async () => {
  return EntityModel.find({ valid: true }).lean();
};
```

---

## 并行数据获取

```typescript
// BAD: Sequential (slow)
const metadata = await queries.getMetadata();
const score = await queries.getScore(id);
const location = await queries.getLocation(id);
// Time: sum of all queries

// GOOD: Parallel (fast)
const [metadata, score, location] = await Promise.all([
  queries.getMetadata(),
  queries.getScore(id),
  queries.getLocation(id),
]);
// Time: max of all queries
```

---

## 各层的职责

| 任务 | 所在层 |
|------|-------|
| 解析请求参数 | 控制器 |
| 验证输入数据 | 控制器 |
| 设置HTTP状态码 | 控制器 |
| 合并多个查询结果 | 服务层 |
| 转换数据 | 服务层 |
| 对结果进行排序/过滤 | 服务层 |
| 执行数据库查询 | 查询层 |

---

## 相关技能

- **相关技术：** [postgres-job-queue](../postgres-job-queue/) — 后台任务处理
- **相关技术：** [realtime/websocket-hub-patterns](../../realtime/websocket-hub-patterns/) — 服务端的实时更新机制

---

## 绝对不要做的事情

- **绝对不要将数据库查询放在控制器中** — 这会违反职责分离原则
- **绝对不要将HTTP相关的逻辑放在服务层中** — 服务层应该具有通用性
- **绝对不要顺序地获取相关数据** — 应使用`Promise.all`来实现并行处理
- **绝对不要在读取数据时省略`.lean()`方法** — 这可以提升5到10倍的执行速度
- **绝对不要直接展示原始的数据库错误信息** — 应将错误信息转换为用户友好的格式