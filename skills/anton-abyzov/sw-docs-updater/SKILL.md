---
name: docs-updater
description: 这是一个实时更新的文档管理系统，能够将代码实现的进度同步到产品文档中。在任务完成后更新文档、将文档状态从“草稿”更改为“已发布”，或确保文档内容始终反映当前的代码实现状态时，可以使用该系统。
---

# 文档更新器

根据实现进度更新产品文档（.specweave/docs/）。

## 使用场景

- 当 `tasks.md` 中指定了文档更新需求时
- 特性实现完成后
- 用户请求“更新文档”或“同步文档”
- 在关闭增量版本后，确保文档内容与实际情况一致

## 功能介绍

1. **读取任务需求**：理解 `tasks.md` 中记录的实现内容
2. **更新文档内容**：根据实际实现情况修改 `.specweave/docs/` 文件
3. **状态跟踪**：将文档部分的标记从 `[DRAFT]` 更改为 `[COMPLETE]`
4. **维护双向链接**：保持文档与增量版本之间的链接关系
5. **格式适配**：确保文档格式与现有结构（如 features/ 或 modules/）保持一致

## 工作流程

```
1. Read tasks.md � Find documentation tasks
2. Read implementation � Understand what changed
3. Update docs � Add real code examples, endpoints, configs
4. Mark complete � Change [DRAFT] to [COMPLETE]
5. Verify links � Ensure increment � doc references work
```

## 示例

**`tasks.md` 的内容：**
```markdown
**Documentation Updates**:
- [ ] .specweave/docs/features/payment.md [DRAFT]
- [ ] .specweave/docs/api/payments.md [DRAFT]
```

**文档更新器的工作流程：**
1. 读取与支付功能相关的实现代码
2. 使用实际的代码示例更新 `payment.md` 文件
3. 根据代码中发现的真实 API 端点更新 API 文档
4. 将文档状态更改为 `[COMPLETE]`

## 集成方式

- **被调用方**：`spec-generator`、任务完成触发器
- **更新目标**：`.specweave/docs/**/*.md` 文件
- **读取的数据**：`tasks.md`、实现代码

## 最佳实践

- 在特性任务完成后运行该工具，而非在任务进行过程中
- 确认文档链接的有效性（使用相对路径）
- 保持示例代码与实际代码的一致性
- 避免过度编写文档——专注于用户真正需要的内容