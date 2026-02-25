---
name: openclaw-workspace-governance-installer
description: 在几分钟内安装 OpenClaw WORKSPACE_GOVERNANCE。它提供了引导式设置、升级检查、迁移以及针对长期运行的工作空间的审计功能。
author: Adam Chan
user-invocable: true
metadata: {"openclaw":{"emoji":"🚀","homepage":"https://github.com/Adamchanadam/OpenClaw-WORKSPACE-GOVERNANCE","requires":{"bins":["openclaw"]}}}
---# OpenClaw 工作空间治理安装程序

从第一天起，就让 OpenClaw 的运行更加安全。  
该安装程序为您提供了一套可重复的治理流程，而非依赖临时修改命令的解决方案。  

## 为何如此受欢迎  
1. 防止“先修改再验证”的错误。  
2. 确保设置、升级和审计流程的一致性。  
3. 让所有变更都能被追踪，便于审查和交接。  
4. 既适合新手，也适用于生产环境中的工作空间。  

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
2. `gov_setup quick|check|install|upgrade`：一步完成治理的部署、升级或验证。  
3. `gov_migrate`：安装或升级后，使工作空间行为符合最新的治理规则。  
4. `gov_audit`：执行 12 项完整性检查，确保一切正常后再宣布完成。  
5. `gov_uninstall quick|check|uninstall`：安全卸载工具，并保留备份和审计记录。  
6. `gov_openclaw_json`：在备份、验证和可回滚的前提下，安全编辑平台配置文件（`openclaw.json`）。  
7. `gov_brain_audit`：预览并审核 Brain Docs 的质量，支持审批和回滚功能。  
8. `gov_boot_audit`：扫描潜在问题并生成升级建议（仅限读取模式）。  
9. `gov APPLY <NN>`：在明确的人工审批下应用单个升级提案（**实验性功能**，仅限受控的用户验收测试）。  

## 功能成熟度（重要提示）  
1. 生产环境中的正式发布流程：`gov_setup -> gov_migrate -> gov_audit`，以及 `gov_uninstall`、`gov_openclaw_json`、`gov_brain_audit`、`gov_boot_audit`。  
2. 实验性流程：`gov APPLY <NN>` 被纳入运行时回归基线，但仍属于受控的用户验收测试范围。  
3. 如果使用 `gov_apply <NN>`，请确保在操作后执行 `gov_migrate` 和 `gov_audit`。  
4. 所有 `/gov_` 命令的输出都遵循统一格式：包含 `🐾` 标头、表情符号状态指示（✅/⚠️/❌）、结构化的列表项以及 `👉` 下一步指引。  

## 如何选择合适的命令（快速参考）  
1. 需要快速查看命令列表？使用 `gov_help`。  
2. 日常默认操作：`gov_setup quick`（一键完成所有步骤）。  
3. 需要先判断工作空间是否准备好？使用 `gov_setup check`。  
4. 首次部署？使用 `gov_setup install`。  
5. 需要更新现有部署？使用 `gov_setup upgrade`。  
6. 部署或升级后需要调整策略？使用 `gov_migrate`。  
7. 完成部署前需最终验证？使用 `gov_audit`。  
8. 安全清理治理相关文件？使用 `gov_uninstall quick`。  
9. 安全编辑 OpenClaw 平台配置？使用 `gov_openclaw_json`。  
10. 安全审核 Brain Docs？使用 `gov_brain_audit`，必要时可执行 `gov_brain_audit APPROVE: ... -> gov_brain_audit ROLLBACK`。  
11. 扫描潜在问题并获取升级建议？使用 `gov_boot_audit`。  
12. 仅应用已批准的升级提案？使用 `gov_apply <NN>`（仅限实验性功能）。  

## 首次运行时的注意事项  
执行 `/gov_setup quick` 后：  
- 如果提示“允许列表未准备好”，请运行 `/gov_openclaw_json`，然后再重新运行 `/gov_setup quick`。  
- 如果输出显示“PASS”，则表示工作空间配置正确。  
- 如果输出显示“FAIL/BLOCKED”，请按照提示的下一步命令操作。  
- 手动操作方案依然可用：`check -> install/upgrade -> migrate -> audit`。  

## 重要更新说明  
如果 `openclaw plugins install ...` 命令返回“plugin already exists”（插件已存在），请执行以下操作：  
1. `openclaw plugins update openclaw-workspace-governance`。  
2. 重启 `openclaw gateway`。  
3. （如有需要）使用 `/gov_openclaw_json` 调整允许列表。  
4. 重新运行 `/gov_setup quick`（或手动执行 `gov_setup upgrade` -> `/gov_migrate` -> `/gov_audit`）。  
5. 即使 `gov_setup check` 显示“READY”，也不影响已请求的 `gov_setup upgrade` 操作。  

## 版本信息（管理员需知）  
- 已安装版本：`openclaw plugins info openclaw-workspace-governance`。  
- 最新版本：`npm view @adamchanadam/openclaw-workspace-governance version`。  

## 运行时规则（重要提示）  
- 仅允许读取和测试相关的命令，禁止写入/更新操作。  
- 在进行任何更改前，必须提供相应的计划和验证信息。  
- 如果命令被运行时系统阻止，通常表示治理机制正常工作（而非系统故障）。  
- 确保治理工具的输出包含 `WG_PLAN_GATE_OK` 和 `WG_READ_gate_OK`，然后重试。  
- 所有 `gov_` 命令的输出都遵循统一格式。  

## 其他注意事项  
- 如果路径导航不稳定，请使用备用命令或自然语言操作方式。  

## 适用人群  
- 需要引导式安装流程的新用户。  
- 需要维护长期运行工作空间的团队。  
- 需要可审计、低风险维护方案的用户。  

## 更多信息（请参阅 GitHub 文档）  
1. 官方文档：https://github.com/Adamchanadam/OpenClaw-WORKSPACE-GOVERNANCE  
2. 英文版 README：https://github.com/Adamchanadam/OpenClaw-WORKSPACE-GOVERNANCE/blob/main/README.md  
3. 繁体中文版 README：https://github.com/Adamchanadam/OpenClaw-WORKSPACE-GOVERNANCE/blob/main/README.zh-HK.md  
4. 治理手册（英文）：https://github.com/Adamchanadam/OpenClaw-WORKSPACE-GOVERNANCE/blob/main/WORKSPACE_GOVERNANCE_README.en.md  
5. 治理手册（繁体中文）：https://github.com/Adamchanadam/OpenClaw-WORKSPACE-GOVERNANCE/blob/main/WORKSPACE_GOVERNANCE_README.md  
6. 产品定位说明（英文）：https://github.com/Adamchanadam/OpenClaw-WORKSPACE-GOVERNANCE/blob/main/VALUE_POSITIONING_AND_FACTORY_GAP.en.md  
7. 产品定位说明（繁体中文）：https://github.com/Adamchanadam/OpenClaw-WORKSPACE-GOVERNANCE/blob/main/VALUE_POSITIONING_AND_FACTORY_GAP.md