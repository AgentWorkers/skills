# 技能治理

使用该机制通过平衡的治理模型来管理多技能之间的相互影响（即技能之间的副作用）。

## 使用场景

- 安装新技能后（新技能必须通过验收流程才能被视为“可用”）
- 每日/定期更新技能状态
- 调整核心技能池以及自动晋升/降级技能
- 决定执行顺序：优先使用核心技能，其次为其他可用技能，最后使用备用技能

## 政策规则

- 技能状态：`候选` -> `可用` -> `核心` -> `隔离` -> `退役`
- 第三方技能默认为`候选`状态
- 只有处于`可用`或`核心`状态的技能才能被自动选中
- 如果连续两次执行失败，该技能将被置于`隔离`状态
- 如果某项核心技能连续三天未被使用，其状态将降级为`可用`状态
- 核心技能的数量上限为8到14个

## 数据来源

- `skill-registry.json`（技能注册表）

## 相关脚本

1. 将运行时状态与文件系统中的信息同步到注册表：
   - `scripts/reconcile-ready.ps1 -Root <workspace>`
2. 对特定技能进行四步验收流程：
   - `scripts/audit-skill.ps1 -Root <workspace> -SkillName <name>`
3. 记录技能使用结果：
   - `scripts/record-skill-usage.ps1 -Root <workspace> -SkillName <name> -Outcome success|failure|blocked`
4. 评估核心技能池的调整情况以及核心技能的数量上限：
   - `scripts/update-core-pool.ps1 -Root <workspace>`
5. 规定执行顺序（核心技能 -> 可用技能 -> 备用技能）：
   - `scripts/route-skill.ps1 -Root <workspace> -TaskText "<text>" -Candidates "a,b,c"`
6. 每周清理不再使用的或缺失的技能：
   - `scripts/weekly-cleanup.ps1 -Root <workspace>`

## 安装新技能后的必经流程

1. 运行 `reconcile-ready.ps1`
2. 运行 `audit-skill.ps1` 对新安装的技能进行验收
3. 确保该技能在 `skill-registry.json` 中的状态为 `ready`，才能将其纳入自动执行流程