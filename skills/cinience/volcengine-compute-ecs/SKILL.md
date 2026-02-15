---
name: volcengine-compute-ecs
description: 管理 Volcengine ECS 实例及相关资源。适用于用户需要查看实例清单、执行生命周期操作、进行故障排除，或使用 ECS 自动化模板的情况。
---

# volcengine-compute-ecs

通过明确的操作范围、干运行（dry-run）式检查以及可审计的输出结果，安全地管理ECS（Elastic Container Service）资源。

## 执行检查清单

1. 确认区域、账户权限范围以及实例筛选条件。
2. 在执行任何修改操作之前，先查询资源清单。
3. 仅使用明确的目标ID来执行生命周期操作（启动/停止/重启）。
4. 返回包含实例ID和状态的操作摘要。

## 安全规则

- 首先优先使用只读命令。
- 按区域和标签对操作进行批量处理。
- 记录操作前的状态和操作后的状态，以便后续回滚。

## 参考资料

- `references/sources.md`