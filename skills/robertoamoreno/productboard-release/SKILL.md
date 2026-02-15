---
name: productboard-release
description: 管理 ProductBoard 的发布流程及路线图规划
user-invocable: false
homepage: https://github.com/robertoamoreno/openclaw-productboard
metadata: {"openclaw":{"emoji":"🚀"}}
---

# ProductBoard 发布计划技能

通过组织功能、跟踪进度和更新 ProductBoard 中的状态来规划和管理产品发布。

## 可用工具

- `pb_feature_create` - 为发布创建新功能
- `pb_feature_update` - 更新功能的状态和详细信息
- `pb_feature_list` - 按状态或产品列出功能
- `pb_feature_get` - 获取详细的功能信息
- `pb_product_list` - 列出产品
- `pb_product_hierarchy` - 查看产品结构
- `pb_user_list` - 查找可分配为负责人的用户

## 发布计划工作流程

### 1. 查看当前状态

```
1. pb_product_hierarchy - Understand workspace structure
2. pb_feature_list with status "candidate" - Review feature candidates
3. pb_feature_list with status "in-progress" - Check ongoing work
```

### 2. 对功能进行优先级排序

审查候选功能并更新其状态：

```
pb_feature_update:
  - id: "feature-id"
  - status: "in-progress"  // Move to active development
```

### 3. 分配负责人

查找用户并分配功能负责人：

```
1. pb_user_list - Get available team members
2. pb_feature_update:
   - id: "feature-id"
   - ownerEmail: "developer@company.com"
```

### 4. 设置时间框架

为功能设置计划日期：

```
pb_feature_update:
  - id: "feature-id"
  - startDate: "2024-01-15"
  - endDate: "2024-02-15"
```

### 5. 跟踪进度

监控功能的状态：

```
pb_feature_list with status "in-progress" - Active development
pb_feature_list with status "shipped" - Completed features
```

## 功能状态生命周期

| 状态 | 描述 |
|--------|-------------|
| `new` | 新创建，尚未评估 |
| `candidate` | 正在考虑开发中 |
| `in-progress` | 正在积极开发中 |
| `shipped` | 已发布给客户 |
| `postponed` | 延期到未来的计划中 |
| `archived` | 不再相关 |

## 计划场景

### 断裂期计划

1. 列出候选功能：使用 `pb_feature_list`（状态为“candidate”）
2. 查看每个功能的详细信息：使用 `pb_feature_get`
3. 将选中的功能状态更改为“in-progress”：使用 `pb_feature_update`
4. 分配负责人：使用 `pb_feature_update` 设置 `ownerEmail`
5. 设置断裂期日期：使用 `pb_feature_update` 设置 `startDate/endDate`

### 发布回顾

1. 列出已发布的功能：使用 `pb_feature_list`（状态为“shipped”）
2. 查看关于功能的反馈：使用反馈工具
3. 归档已完成的工作：使用 `pb_feature_update` 将状态更改为“archived”

### 季度计划

1. 查看产品结构：使用 `pb_product_hierarchy`
2. 按产品列出所有活跃的功能
3. 重新评估优先级并更新状态
4. 根据需要创建新功能：使用 `pb_feature_create`

## 组织功能

### 按产品分类

```
pb_feature_create:
  - name: "Feature name"
  - productId: "product-id"
  - status: "candidate"
```

### 按组件分类

```
pb_feature_create:
  - name: "Feature name"
  - componentId: "component-id"
  - status: "candidate"
```

### 作为子功能分类

```
pb_feature_create:
  - name: "Sub-feature name"
  - parentFeatureId: "parent-feature-id"
```

## 最佳实践

1. **使用一致的状态**：系统地推进功能通过生命周期
2. **尽早分配负责人**：明确的责任制有助于提高效率
3. **设置现实的时间框架**：根据计划的变化更新日期
4. **分层组织**：使用产品、组件和子功能进行分类
5. **归档已完成的工作**：通过归档已发布的功能来保持待办事项列表的整洁
6. **定期审查**：使用列表工具来审核功能的状态