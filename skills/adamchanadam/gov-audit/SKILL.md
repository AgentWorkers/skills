---
name: gov_audit
description: 运行 post-bootstrap 或 post-migration 治理审计。
user-invocable: true
metadata: {"openclaw":{"emoji":"✅"}}
---# /gov_audit

## 目的
在系统启动（bootstrap）、迁移或应用更新后，执行治理完整性检查。

## 必须执行的检查
1. 运行 `_control/REGRESSION_CHECK.md` 中的清单，其中的分母固定为 12/12。
2. 核实治理框架（governance framework）的一致性，以确保符合当前的迁移基线要求。
3. 显示明确的通过/失败（PASS/FAIL）结果；如果有任何检查项未通过，则需要采取相应的补救措施。
4. 验证路径兼容性：
   - 治理框架内容必须使用运行时的 `<workspace-root>` 语义。
   - 在修改后的治理框架内容中，不得包含硬编码的 `~/.openclaw/workspace` 假设。
5. 验证系统信息的准确性：
   - OpenClaw 的系统声明必须引用 `https://docs.openclaw.ai` 作为信息来源。
   - 最新的、版本敏感的 OpenClaw 声明还必须引用 `https://github.com/openclaw/openclaw/releases` 作为信息来源。
   - 日期/时间声明必须包含运行时的当前时间信息（会话状态）。
6. 如果运行过程中涉及平台控制平面的更改，需验证以下内容：
   - 备份路径是否存在于 `archive/_platform_backup_<ts>/...` 下。
   - 是否有运行前后的关键信息摘录。
   - 更改是否通过 `gov_platform_change` 路径（或等效的文档化备用路径）执行。

## 持久化
- 当当前的治理流程需要持久化审计结果时，将审计结果写入 `_runs/` 文件夹中。
- 当添加新的运行报告时，确保 `_control/WORKSPACE_INDEX.md` 文件得到更新。

## 备用方案
- 如果 `/gov_audit` 命令不可用或名称冲突，可以使用以下命令：
  - `/skill gov_audit`