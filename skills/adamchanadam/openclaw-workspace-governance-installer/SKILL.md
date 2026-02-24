---
name: openclaw-workspace-governance-installer
description: 只需几分钟即可安装 OpenClaw WORKSPACE_GOVERNANCE。该工具提供引导式设置、升级检查、迁移支持以及针对长期运行的工作空间的审计功能。
author: Adam Chan
user-invocable: true
metadata: {"openclaw":{"emoji":"🚀","homepage":"https://github.com/Adamchanadam/OpenClaw-WORKSPACE-GOVERNANCE","requires":{"bins":["openclaw"]}}}
---# OpenClaw 工作空间治理安装程序

从第一天起，就让 OpenClaw 的运行更加安全。  
该安装程序为您提供了一套可重复的治理流程，而非依赖临时手动编辑的解决方案。

## 为什么这个工具如此受欢迎？  
1. 避免了“先编辑后验证”的错误。  
2. 确保了设置、升级和审计流程的一致性。  
3. 使所有变更都能被追踪，便于审查和交接。  
4. 既适合初学者，也适用于生产环境。  

## 60 秒快速入门  
首次安装：  
```bash
# 1) Install plugin (first time only)
openclaw plugins install @adamchanadam/openclaw-workspace-governance@latest

# 2) Enable plugin
openclaw plugins enable openclaw-workspace-governance

# 3) Verify skills
openclaw skills list --eligible
```  

在 OpenClaw 聊天窗口中：  
```text
/gov_help
/gov_setup quick
# if quick output says allowlist is not ready (for example plugins.allow needs alignment):
/gov_openclaw_json
/gov_setup quick
# manual fallback (step-by-step):
/gov_setup install
prompts/governance/OpenClaw_INIT_BOOTSTRAP_WORKSPACE_GOVERNANCE.md
# if this workspace was already active before first governance adoption:
/gov_migrate
/gov_audit
```  

已安装的用户（升级流程）：  
```bash
# Do NOT run install again if plugin already exists
openclaw plugins update openclaw-workspace-governance
openclaw gateway restart
```  

随后在 OpenClaw 聊天窗口中：  
```text
/gov_setup quick
# if quick output says allowlist is not ready (for example plugins.allow needs alignment):
/gov_openclaw_json
/gov_setup quick
/gov_setup upgrade
/gov_migrate
/gov_audit
# manual fallback:
/gov_setup upgrade
/gov_migrate
/gov_audit
```  

## 您将获得什么？  
1. `gov_help`：一目了然地查看所有命令及推荐的入口点。  
2. `gov_setup quick|check|install|upgrade`：一步完成治理配置的部署、升级或验证。  
3. `gov_migrate`：在安装或升级后，使工作空间行为符合最新的治理规则。  
4. `gov_audit`：执行 12 项完整性检查，确保一切正常后再宣布完成。  
5. `gov_openclaw_json`：安全地编辑平台配置文件（`openclaw.json`），同时提供备份、验证和回滚功能。  
6. `gov_brain_audit`：审核并优化 Brain Docs 的质量，支持预览后批准及回滚操作。  
7. `gov_boot_audit`：扫描潜在问题并生成升级建议（仅限读写模式）。  
8. `gov_uninstall quick|check|uninstall`：安全地卸载程序，并保留所有备份和审计记录。  
9. `gov_apply <NN>`：在明确的人工审核下应用升级提案（**实验性功能**，仅限受控的用户验收测试）。  

## 功能成熟度（重要说明）  
1. 生产环境推荐流程：`gov_setup -> gov_migrate -> gov_audit`，并配合 `gov_openclaw_json`、`gov_brain_audit`、`gov_boot_audit` 和 `gov_uninstall` 使用。  
2. 实验性流程：`gov APPLY <NN>` 被纳入运行时回归测试的基准范围，但仍属于受控的用户验收测试。  
3. 如果使用 `gov APPLY <NN>`，请确保在操作完成后执行 `gov_migrate` 和 `gov_audit`。  
4. 所有 `gov_*` 命令的输出均采用统一格式：包含 `🐾` 标头、表情符号状态指示（✅/⚠️/❌）、结构化的列表项以及 `👉` 下一步指引。  

## 如何选择合适的命令（快速参考）  
1. 需要快速查看命令列表？使用 `gov_help`。  
2. 日常默认操作：`gov_setup quick`（一键完成全部流程）。  
3. 需要先判断系统是否准备好升级？使用 `gov_setup check`。  
4. 首次部署？使用 `gov_setup install`。  
5. 需要更新现有配置？使用 `gov_setup upgrade`。  
6. 部署或升级后需要调整策略？使用 `gov_migrate`。  
7. 完成部署后需要最终验证？使用 `gov_audit`。  
8. 仅应用已批准的升级提案？使用 `gov APPLY <NN>`（仅限实验性功能）。  
9. 安全编辑 OpenClaw 平台配置？使用 `gov_openclaw_json`。  
10. 安全审核并优化 Brain Docs？使用 `gov_brain_audit`，必要时可执行 `gov_brain_audit APPROVE` 和 `gov_brain_audit ROLLBACK`。  
11. 安全清理治理相关文件？使用 `gov_uninstall quick`。  
12. 扫描潜在问题并获取升级建议？使用 `gov_boot_audit`。  

## 首次运行时的注意事项  
执行 `gov_setup quick` 后：  
- 如果输出提示“允许列表尚未准备就绪”，请运行 `gov_openclaw_json`，然后再重新运行 `gov_setup quick`。  
- 如果输出结果为“PASS”，则表示系统配置已正确。  
- 如果输出结果为“FAIL/BLOCKED”，请按照提示的下一步命令操作。  
- 手动操作方案仍然可用：`check -> install/upgrade -> migrate -> audit`。  

## 重要更新规则  
如果 `openclaw plugins install ...` 命令提示“插件已存在”，请执行以下操作：  
1. `openclaw plugins update openclaw-workspace-governance`。  
2. 重启 OpenClaw Gateway。  
3. （如有必要）使用 `gov_setup check` 校验允许列表。  
4. 重新运行 `gov_setup quick`（或手动执行 `gov_setup upgrade` -> `gov_migrate` -> `gov_audit`）。  
5. 即使 `gov_setup check` 显示“READY”，也不应取消正在进行的 `gov_setup upgrade` 操作。  

## 版本检查（操作员端）  
- 已安装的版本：`openclaw plugins info openclaw-workspace-governance`。  
- 最新版本：`npm view @adamchanadam/openclaw-workspace-governance version`。  

## 运行时权限控制（重要说明）  
1. 仅允许执行读写模式的诊断和测试命令。  
2. 执行写入、更新或保存操作的命令前，必须提供相应的权限（`PLAN` 和 `READ` 权限）。  
3. 如果被运行时权限系统阻止，通常意味着治理机制正常工作（而非系统故障）。  
4. 确保治理工具的输出包含 `WG_PLAN_gate_OK` 和 `WG_READ_gate_OK` 状态信息，然后重试操作。  
5. 所有 `gov_*` 命令的输出均遵循统一格式。  

## 如果命令路径出现问题  
可以使用备用命令：  
```text
/skill gov_setup check
/skill gov_setup install
/skill gov_setup upgrade
/skill gov_migrate
/skill gov_audit
# Experimental only:
/skill gov_apply 01
/skill gov_openclaw_json
/skill gov_brain_audit
/skill gov_brain_audit APPROVE: APPLY_ALL_SAFE
/skill gov_brain_audit ROLLBACK
/skill gov_boot_audit
```  
或使用自然语言界面：  
```text
Please use gov_setup in check mode (read-only) and return workspace root, status, and next action.
```  

## 适用人群  
- 需要引导式安装流程的新用户。  
- 需要维护长期运行的工作空间的团队。  
- 需要可审计、低风险维护环境的用户。  

## 更多信息（GitHub 文档）：  
1. 官方文档：https://github.com/Adamchanadam/OpenClaw-WORKSPACE-GOVERNANCE  
2. 英文版 README：https://github.com/Adamchanadam/OpenClaw-WORKSPACE-GOVERNANCE/blob/main/README.md  
3. 繁体中文版 README：https://github.com/Adamchanadam/OpenClaw-WORKSPACE-GOVERNANCE/blob/main/README.zh-HK.md  
4. 治理手册（英文）：https://github.com/Adamchanadam/OpenClaw-WORKSPACE-GOVERNANCE/blob/main/WORKSPACE_GOVERNANCE_README.en.md  
5. 治理手册（繁体中文）：https://github.com/Adamchanadam/OpenClaw-WORKSPACE-GOVERNANCE/blob/main/WORKSPACE_GOVERNANCE_README.md  
6. 产品定位说明（英文）：https://github.com/Adamchanadam/OpenClaw-WORKSPACE-GOVERNANCE/blob/main/VALUE_POSITIONING_AND_FACTORY_GAP.en.md  
7. 产品定位说明（繁体中文）：https://github.com/Adamchanadam/OpenClaw-WORKSPACE-GOVERNANCE/blob/main/VALUE_POSITIONING_AND_FACTORY_GAP.md