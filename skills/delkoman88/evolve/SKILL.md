---
name: evolve
description: OpenClaw的本地DevOps/自主开发能力（具备安全防护机制的持续进化循环）。
metadata: { "openclaw": { "emoji": "🧬" } }
---

# evolve

这是一个用于 OpenClaw 的本地 DevOps/自主管理技能（local DevOps/autonomy skill）。

该技能提供了一个安全的“进化循环”控制器（evolution loop controller），其功能包括：
- 备份当前状态（snapshot the current status）
- 生成候选方案（generate candidates）
- 测试候选方案（test candidates）
- 将候选方案提升为可用技能（promote candidates to active skills）
- 支持回滚操作（support rollback）

## 命令

- `evolve plan`：制定进化计划
- `evolve generate <slug>`：生成新的技能方案
- `evolve test <slug>`：测试候选方案
- `evolve promote <slug>`：将候选方案提升为可用技能
- `evolve rollback <slug>`：执行回滚操作

## 注意事项

该技能的所有功能都由一个本地控制器脚本（`evolvectl.sh`）负责处理。您可以通过设置 `EVOLVECTL` 变量来指定该脚本的实际路径。