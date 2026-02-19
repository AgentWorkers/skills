---
name: gov_apply
description: 使用引导式应用工具（guided apply runner），根据编号来应用已批准的 BOOT 升级项。
user-invocable: true
metadata: {"openclaw":{"emoji":"🧩"}}
---# /gov_apply <NN>

## 输入参数
- `<NN>` 必须是一个两位数的项目编号，例如 `01`。

## 功能
执行以下操作：
- `prompts/governance/APPLY_UPGRADE_FROM_BOOT.md`

## 硬性契约（Hard Contract）规则：
1. 如果 `<NN>` 缺失或无效，停止执行并请求用户输入一个两位数的项目编号。
2. 如果缺少 `BOOT` 菜单的相关信息，停止执行并请求用户提供最新的 `BOOT` 菜单内容。
3. 仅应用已批准的项目。
4. 应用完成后，根据应用流程的要求执行迁移/审计操作。
5. 在应用过程中，对于与 OpenClaw 系统相关的功能请求，需对照本地技能文档以及 `https://docs.openclaw.ai` 进行验证；
   - 对于那些依赖于最新版本的信息，还需验证官方发布的文档（`https://github.com/openclaw/openclaw/releases`）。
   - 如果无法完成验证，应报告问题并说明下一步需要检查的内容；切勿自行推断结果。
6. 对于那些依赖于当前日期/时间的功能请求，首先需要验证运行时的时间环境（会话状态）。
7. 使用运行时的 `<workspace-root>` 目录结构；不要假设目录路径是固定的。

## 备用方案（Fallback Strategy）：
- 如果 `/gov_apply` 命令不可用或名称冲突，可以使用以下命令代替：
  - `/skill gov_apply <NN>`