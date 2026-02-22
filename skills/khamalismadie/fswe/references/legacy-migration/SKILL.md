# 旧代码迁移

## “Strangler Pattern”（绞杀者模式）

```
Before:                    After:
┌─────────────┐           ┌─────────────┐
│  PHP        │           │   New TS    │
│  Monolith   │           │   Service   │
└─────────────┘           └─────────────┘
      ↑                         ↑
      │     ┌─────────────┐      │
      ├────►│   Facade   │◄─────┤
      │     │  (Gateway) │      │
      │     └─────────────┘      │
      │            ↑            │
      │            │            │
      └────────────┴────────────┘
```

## 逐步提取功能（Incremental Feature Extraction）

```typescript
// New service imports from legacy via API
// Once feature is migrated, point to new service

// Phase 1: API Gateway routes to PHP
router.get('/users', proxyToLegacy)

// Phase 2: Extract to new service
router.get('/users', userController.findAll)

// Phase 3: Remove legacy dependency
// DELETE /users from PHP
```

## 风险评估（Risk Mapping）

| 功能        | 复杂度      | 风险等级    | 迁移顺序       |
|------------|-----------|----------|-------------|
| 认证系统（Auth）   | 高        | 关键级别    | 第一步         |
| 用户资料系统（User Profile） | 中等        | 中等级别    | 第二步         |
| 仪表盘系统（Dashboard） | 低        | 低级别      | 第三步         |
| 旧版报告系统（Legacy Reports） | 高        | 低级别      | 最后一步       |

## 检查清单（Checklist）

- [ ] 审查旧代码库
- [ ] 映射代码依赖关系
- [ ] 确定功能的边界范围
- [ ] 实现“绞杀者模式”（Strangler Pattern）的封装层
- [ ] 逐个提取功能
- [ ] 并行运行新旧系统
- [ ] 逐步完成迁移过程