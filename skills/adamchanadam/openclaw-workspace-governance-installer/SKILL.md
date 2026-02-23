---
name: openclaw-workspace-governance-installer
description: 只需几分钟，即可安装 OpenClaw WORKSPACE_GOVERNANCE。它提供了设置指导、升级检查、迁移支持以及针对长期运行的工作空间的审计功能。
author: Adam Chan
user-invocable: true
metadata: {"openclaw":{"emoji":"🚀","homepage":"https://github.com/Adamchanadam/OpenClaw-WORKSPACE-GOVERNANCE","requires":{"bins":["openclaw"]}}}
---# OpenClaw 工作空间治理安装程序

从第一天起，就让 OpenClaw 的操作更加安全。  
该安装程序为您提供了一套可重复使用的治理流程，而非依赖临时提示进行手动编辑的方案。

## 为何如此受欢迎  
1. 避免了“先编辑再验证”的错误。  
2. 确保了设置、升级和审计流程的一致性。  
3. 使所有变更都能被追踪，便于审查和交接。  
4. 既适合新手，也适用于生产环境中的工作空间。  

## 60 秒快速入门  
首次安装：  
```bash  
# 1) 安装插件（仅限首次）  
openclaw plugins install @adamchanadam/openclaw-workspace-governance@latest  

# 2) 启用插件  
openclaw plugins enable openclaw-workspace-governance  

# 3) 检查技能配置  
openclaw skills list --eligible  
```  

在 OpenClaw 聊天界面中：  
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
# 如果插件已存在，请勿再次运行安装命令  
openclaw plugins update openclaw-workspace-governance  
openclaw gateway restart  
```  

在 OpenClaw 聊天界面中：  
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

## 您将获得的功能：  
1. `gov_help`：提供一次性命令列表及一键操作建议。  
2. `gov_setup`：支持“快速设置”、“安装”、“升级”和“检查”功能。  
3. `gov_migrate`：用于治理系统的升级。  
4. `gov_audit`：执行全面的系统一致性检查。  
5. `gov APPLY <NN>`：用于控制性的系统启动（BOOT）提案申请（仅限实验性使用，需经过严格测试）。  
6. `gov_openclaw_json`：用于控制平台控制平面的更新：  
   - 更新范围：`~/.openclaw/openclaw.json`  
   - 在必要时也可更新 `~/.openclaw/extensions/` 目录下的文件  
   - 不适用于 Brain Docs（`USER.md`、`SOUL.md`、`memory/*.md`）或普通工作空间文档。  
7. `gov_brain_audit`：用于对 Brain Docs 进行风险审查：  
   - 默认为只读预览模式  
   - 需要批准后才能进行差异备份  
   - 仅在使用已批准的备份时才能回滚。  
8. `gov_uninstall quick|check|uninstall`：在卸载软件包前安全清理工作空间配置。  

## 功能成熟度（重要说明）  
1. 生产环境中的推荐流程：`gov_setup -> gov_migrate -> gov_audit`，同时使用 `gov_openclaw_json`、`gov_brain_audit` 和 `gov_uninstall`。  
2. 实验性流程：`gov APPLY <NN>` 被纳入运行时回归测试的基准范围，但仍属于受控的测试阶段。  
3. 如果使用了 `gov APPLY <NN>`，请务必通过 `gov_migrate` 和 `gov_audit` 完成整个流程。  

## 如何选择合适的命令（快速参考）：  
1. 需要快速查看命令列表？使用 `gov_help`。  
2. 日常操作：使用 `gov_setup quick`（一键完成所有步骤）。  
3. 需要先评估系统是否准备好部署？使用 `gov_setup check`。  
4. 首次部署：使用 `gov_setup install`。  
5. 更新现有部署配置：使用 `gov_setup upgrade`。  
6. 部署或更新后需核对政策一致性？使用 `gov_migrate`。  
7. 部署完成前的最终验证：使用 `gov_audit`。  
8. 仅应用已批准的 BOOT 提案？使用 `gov_apply <NN>`（仅限实验性使用）。  
9. 安全修改 OpenClaw 平台配置？使用 `gov_openclaw_json`。  
10. 安全审查 Brain Docs？使用 `gov_brain_audit`，必要时可执行 `gov_brain_audit APPROVE: ... -> gov_brain_audit ROLLBACK`。  
11. 安全清理工作空间治理相关文件？使用 `gov_uninstall quick`。  

## 首次运行时的注意事项：  
执行 `gov_setup quick` 后：  
- 如果提示“允许列表尚未准备就绪”，请运行 `gov_openclaw_json`，然后再重新运行 `gov_setup quick`。  
- 如果输出显示“通过”，则表示系统配置已正确。  
- 如果输出显示“失败/被阻止”，请按照提示执行后续操作。  
- 如需手动恢复，可依次执行 `check`、`install`、`upgrade` 和 `audit` 命令。  

## 重要更新规则：  
如果 `openclaw plugins install ...` 返回“插件已存在”的提示，请执行以下操作：  
1. `openclaw plugins update openclaw-workspace-governance`。  
2. `openclaw gateway restart`。  
3. （如需调整允许列表）执行 `gov_openclaw_json`。  
4. 然后执行 `gov_setup quick`（或手动执行 `gov_setup upgrade` → `gov_migrate` → `gov_audit`）。  
5. 即使 `gov_setup check` 显示“准备就绪”，也不影响正在进行的 `gov_setup upgrade` 流程。  

## 版本信息（供管理员参考）：  
- 已安装插件：`openclaw plugins info openclaw-workspace-governance`  
- 最新版本：`npm view @adamchanadam/openclaw-workspace-governance version`  

## 运行时权限控制（重要说明）：  
1. 仅允许执行只读的诊断和测试命令。  
2. 执行写入、更新或保存操作的命令前，必须提供相应的计划（PLAN）和读取权限（READ）验证。  
3. 如果被运行时权限系统阻止，通常说明治理机制正常工作（而非系统故障）。  
4. 确保治理系统输出中包含 `WG_PLAN_gate_OK` 和 `WG_READ_gate_OK`，然后再重试。  
5. 最终的输出格式应为：`STATUS` → `WHY` → `NEXT STEP (Operator)` → `COMMAND TO COPY`。  
6. 如果 `gov_setup upgrade` 仍提示权限问题，请将插件更新至最新版本并重启 gateway，然后重新执行 `gov_setup check` 和 `gov_setup upgrade`。  
7. 该工具支持根目录的访问控制：治理插件工具需要明确指定操作意图（例如 `/gov_*`）。  

## 如果路径导航不稳定，请使用备用命令：  
```text  
/skill gov_setup check  
/skill gov_setup install  
/skill gov_setup upgrade  
/skill gov_migrate  
/skill gov_audit  
# 仅限实验性使用：  
/skill gov APPLY 01  
/skill gov_openclaw_json  
/skill gov_brain_audit  
/skill gov_brain_audit APPROVE: APPLY_ALL_SAFE  
/skill gov_brain_audit ROLLBACK  
```  

或者使用自然语言提示：  
“请以只读模式使用 `gov_setup`，并获取工作空间的根目录信息、当前状态及下一步操作建议。”  

## 适用人群：  
1. 需要引导式安装流程的新 OpenClaw 用户。  
2. 需要维护长期运行的工作空间的团队。  
3. 需要可审计、低风险维护环境的用户。  

## 更多信息（GitHub 文档）：  
1. 主文档：https://github.com/Adamchanadam/OpenClaw-WORKSPACE-GOVERNANCE  
2. 英文版 README：https://github.com/Adamchanadam/OpenClaw-WORKSPACE-GOVERNANCE/blob/main/README.md  
3. 繁体中文版 README：https://github.com/Adamchanadam/OpenClaw-WORKSPACE-GOVERNANCE/blob/main/README.zh-HK.md  
4. 治理手册（英文）：https://github.com/Adamchanadam/OpenClaw-WORKSPACE-GOVERNANCE/blob/main/WORKSPACE_GOVERNANCE_README.en.md  
5. 治理手册（繁体中文）：https://github.com/Adamchanadam/OpenClaw-WORKSPACE-GOVERNANCE/blob/main/WORKSPACE_GOVERNANCE_README.md  
6. 产品定位说明（英文）：https://github.com/Adamchanadam/OpenClaw-WORKSPACE-GOVERNANCE/blob/main/VALUE_POSITIONING_AND_FACTORY_GAP.en.md  
7. 产品定位说明（繁体中文）：https://github.com/Adamchanadam/OpenClaw-WORKSPACE-GOVERNANCE/blob/main/VALUE_POSITIONING_AND_FACTORY_gap.md