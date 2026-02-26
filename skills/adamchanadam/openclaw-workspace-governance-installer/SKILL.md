---
name: openclaw-workspace-governance-installer
description: 只需几分钟即可安装 OpenClaw WORKSPACE_GOVERNANCE。它提供了引导式设置、升级检查、迁移以及针对长期运行的工作空间的审计功能。
author: Adam Chan
user-invocable: true
metadata: {"openclaw":{"emoji":"🚀","homepage":"https://github.com/Adamchanadam/OpenClaw-WORKSPACE-GOVERNANCE","requires":{"bins":["openclaw"]}}}
---# OpenClaw 工作空间治理安装程序

从第一天起，就让 OpenClaw 的运行更加安全。  
该安装程序为您提供了一套可重复使用的治理流程，而非依赖临时提示进行手动编辑的方案。

## 为何如此受欢迎  
1. 避免了“先编辑后验证”的错误。  
2. 确保了设置、升级和审计流程的一致性。  
3. 使所有更改均可被追踪，便于审查和交接。  
4. 既适合初学者，也适用于生产环境中的工作空间。  

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

## 您将获得的功能  
1. `gov_help`：一目了然地查看所有命令及推荐的入口点。  
2. `gov_setup quick|check|install|upgrade`：一步完成治理环境的部署、升级或验证。  
3. `gov_migrate`：在安装或升级后，使工作空间的行为符合最新的治理规则。  
4. `gov_audit`：执行 12 项完整性检查，确保一切正常后再宣布完成。  
5. `gov_uninstall quick|check|uninstall`：安全地卸载程序，并保留备份及操作记录。  
6. `gov_openclaw_json`：可安全地编辑平台配置文件（`openclaw.json`），同时提供备份、验证和回滚功能。该工具会在修改前扫描本地工作空间文档；若文档不可用，会自动切换到官方文档；若两者均不可用，则会优雅地降级处理。  
7. `gov_brain_audit`：审核并优化 Brain Docs 的质量，支持预览后确认以及回滚功能。  
8. `gov_boot_audit`：扫描潜在问题并生成升级建议（仅限读取权限）。  
9. `gov.apply <NN>`：需要人工明确批准后，才能应用升级提案（**实验性功能**，仅限受控的用户验收测试）。  

## 功能成熟度（重要说明）  
1. 生产环境中的正式部署流程：`gov_setup -> gov_migrate -> gov_audit`，后续还包括 `gov_uninstall`、`gov_openclaw_json`、`gov_brain_audit` 和 `gov_boot_audit`。  
2. 实验性流程：`gov.apply <NN>` 被纳入了运行时回归基线测试，但仍属于受控的用户验收测试范围。  
3. 如果您使用了 `gov.apply <NN>`，请确保在操作完成后执行 `gov_migrate` 和 `gov_audit`。  
4. 所有 `gov_` 命令的输出均采用统一的格式：包含 `🐾` 标头、表情符号状态指示（✅/⚠️/❌）、结构化的列表项以及 `👉` 下一步指引。  

## 如何选择合适的命令（快速参考）  
1. 需要快速查看命令列表？使用 `gov_help`。  
2. 日常默认操作：使用 `gov_setup quick`（一键完成全部流程）。  
3. 需要先判断系统是否准备好使用新功能？使用 `gov_setup check`。  
4. 首次部署时：使用 `gov_setup install`。  
5. 需要更新现有部署环境？使用 `gov_setup upgrade`。  
6. 部署或升级后需要调整策略？使用 `gov_migrate`。  
7. 完成部署前需要最终验证？使用 `gov_audit`。  
8. 需要安全地清理治理相关文件？使用 `gov_uninstall quick`。  
9. 需要安全地编辑 OpenClaw 平台配置？使用 `gov_openclaw_json`。  
10. 需要审核并优化 Brain Docs 的质量？使用 `gov_brain_audit`，必要时可执行 `gov_brain_audit APPROVE` 或 `gov_brain_audit ROLLBACK`。  
11. 需要扫描潜在问题并获取升级建议？使用 `gov_boot_audit`。  
12. 仅限批准后才能应用升级提案？使用 `gov.apply <NN>`（实验性功能）。  

## 首次运行时的注意事项  
执行 `gov_setup quick` 后：  
- 如果输出提示“允许列表尚未准备就绪”，请运行 `gov_openclaw_json`，然后再重新运行 `gov_setup quick`。  
- 如果输出显示“PASS”，则表示系统配置已正确。  
- 如果输出显示“FAIL/BLOCKED”，请按照提示的下一步命令操作。  
- 手动操作方案仍然可用：`check -> install/upgrade -> migrate -> audit`。  

## 重要更新说明  
如果 `openclaw plugins install ...` 命令返回“插件已存在”的提示，请执行以下操作：  
1. `openclaw plugins update openclaw-workspace-governance`。  
2. `openclaw gateway restart`。  
3. （如需调整允许列表，请使用 `gov_openclaw_json`）。  
4. 再次执行 `gov_setup quick`（或手动执行 `gov_setup upgrade` -> `gov_migrate` -> `gov_audit`）。  
5. 即使 `gov_setup check` 显示“READY”，也不会取消正在进行的 `gov_setup upgrade` 操作。  

## 版本检查（操作员侧）  
- 已安装的版本：`openclaw plugins info openclaw-workspace-governance`。  
- 最新版本：`npm view @adamchanadam/openclaw-workspace-governance version`。  

## 运行时权限控制规则（重要说明）  
1. 仅允许执行读取权限相关的诊断和测试命令，不应被阻止。  
2. **常规写入操作**（如技能配置、项目配置、代码文件）：系统会发出警告提示，但不会直接阻止写入。  
3. **高风险写入操作**（如 Brain Docs、`openclaw.json`、`_control/*` 文件或治理相关配置文件）：第一次尝试时会发出警告提示；若多次尝试仍无法写入，则会直接阻止。  
4. 如果被运行时权限系统阻止，通常说明治理机制正常工作（而非系统故障）。请提供操作计划及已读取的文件列表，然后重试。  
5. 如果被阻止超过三次，请使用 `gov_brain_audit force-accept` 来解除所有权限限制（同时保留审计记录）。  
6. 所有 `gov_` 命令的输出均遵循统一的格式：包含 `🐾` 标头、表情符号状态提示（✅/⚠️/❌）、结构化的列表项以及 `👉` 下一步指引。  
7. 默认情况下，工具的访问权限需要通过 `gov_*` 命令明确指定（或使用 `/skill gov_`）。  

## 如果路径导航不稳定  
请使用备用命令：  
```text
/skill gov_setup check
/skill gov_setup install
/skill gov_setup upgrade
/skill gov_migrate
/skill gov_audit
/skill gov_uninstall quick
/skill gov_openclaw_json
/skill gov_brain_audit
/skill gov_brain_audit APPROVE: APPLY_ALL_SAFE
/skill gov_brain_audit ROLLBACK
/skill gov_boot_audit
# Experimental only:
/skill gov_apply 01
```  
或使用自然语言进行操作：  
```text
Please use gov_setup in check mode (read-only) and return workspace root, status, and next action.
```  

## 适用人群  
- 需要引导式安装流程的新 OpenClaw 用户。  
- 需要维护长期运行的工作空间的团队。  
- 需要确保系统配置可被审计、且变化较小的用户。  

## 了解更多信息（GitHub 文档）  
1. 主要文档：https://github.com/Adamchanadam/OpenClaw-WORKSPACE-GOVERNANCE  
2. 英文版 README：https://github.com/Adamchanadam/OpenClaw-WORKSPACE-GOVERNANCE/blob/main/README.md  
3. 繁体中文版 README：https://github.com/Adamchanadam/OpenClaw-WORKSPACE-GOVERNANCE/blob/main/README.zh-HK.md  
4. 治理手册（英文）：https://github.com/Adamchanadam/OpenClaw-WORKSPACE-GOVERNANCE/blob/main/WORKSPACE_GOVERNANCE_README.en.md  
5. 治理手册（繁体中文）：https://github.com/Adamchanadam/OpenClaw-WORKSPACE-GOVERNANCE/blob/main/WORKSPACE_GOVERNANCE_README.md  
6. 产品定位说明（英文）：https://github.com/Adamchanadam/OpenClaw-WORKSPACE-GOVERNANCE/blob/main/VALUE_POSITIONING_AND_FACTORY_gap.en.md  
7. 产品定位说明（繁体中文）：https://github.com/Adamchanadam/OpenClaw-WORKSPACE-GOVERNANCE/blob/main/VALUE_POSITIONING_AND_FACTORY_GAP.md