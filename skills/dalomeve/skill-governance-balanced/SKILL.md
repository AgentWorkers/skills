# 技能治理

使用此技能通过平衡的治理模型来控制多技能之间的副作用。

## 使用场景

- 安装新技能后（必须通过验收流程才能被视为“可用”状态）
- 每日/定期更新治理状态
- 调整核心技能池以及自动晋升/降级技能
- 路由决策：优先使用核心技能，其次为所有“可用”技能，最后使用备用技能

## 政策规则

- 技能状态模型：`候选` -> `可用` -> `核心` -> `隔离` -> `退役`
- 第三方技能默认为`候选`状态
- 只有“可用”或“核心”状态的技能才能被自动选中
- 如果连续两次执行失败，该技能将被隔离
- 如果某项“核心”技能三天内未被使用，其状态将降级为“可用”
- 核心技能的数量上限为8到14个

## 安全与隐私

- 该技能不涉及任何出站网络请求
- 不会收集任何凭证或上传令牌
- 脚本仅用于读取/写入本地工作区的文件，以维护治理状态和记录
- 每周的清理操作是安全的（仅改变技能状态，不会删除文件）
- 任何超出本地治理范围的操作都必须由操作员明确授权

## 数据来源

- `skill-registry.json`

## 相关脚本

1. 将运行时状态与文件系统数据同步到注册表：
   - `scripts/reconcile-ready.ps1 -Root <workspace>`
2. 对某项技能进行四步验收流程：
   - `scripts/audit-skill.ps1 -Root <workspace> -SkillName <name>`
3. 记录技能使用结果：
   - `scripts/record-skill-usage.ps1 -Root <workspace> -SkillName <name> -Outcome success|failure|blocked`
4. 评估核心技能池的调整以及核心技能数量的动态变化：
   - `scripts/update-core-pool.ps1 -Root <workspace>`
5. 规划执行顺序（核心技能 -> 可用技能 -> 备用技能）：
   - `scripts/route-skill.ps1 -Root <workspace> -TaskText "<text>" -Candidates "a,b,c"`
6. 每周清理过时或缺失的技能：
   - `scripts/weekly-cleanup.ps1 -Root <workspace>`

## 安装新技能的必要步骤

安装新技能后，请按照以下顺序执行操作：

1. 运行 `reconcile-ready.ps1`
2. 运行 `audit-skill.ps1` 对该技能进行验收
3. 确保该技能在 `skill-registry.json` 中的状态为“可用”，才能将其用于自动路由决策