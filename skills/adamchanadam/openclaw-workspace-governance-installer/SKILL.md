---
name: openclaw-workspace-governance-installer
description: 几分钟内即可安装 OpenClaw WORKSPACE_GOVERNANCE。它提供了引导式设置、升级检查、迁移功能以及针对长期运行的工作空间的审计服务。
author: Adam Chan
user-invocable: true
metadata: {"openclaw":{"emoji":"🚀","homepage":"https://github.com/Adamchanadam/OpenClaw-WORKSPACE-GOVERNANCE","requires":{"bins":["openclaw"]}}}
---# OpenClaw 工作空间治理安装程序

从第一天起，就让 OpenClaw 的操作更加安全。  
该安装程序为您提供了一套可重复使用的治理流程，而非依赖临时提示进行手动编辑的方案。

## 为何如此受欢迎  
1. 防止“先编辑后验证”的错误。  
2. 确保设置、升级和审计流程的一致性。  
3. 让所有变更都能被追踪，便于审查和交接。  
4. 既适合初学者，也适用于生产环境的工作空间。  

## 60 秒快速入门  

**首次安装：**  
```bash  
# 1) 安装插件（仅限首次使用）  
openclaw plugins install @adamchanadam/openclaw-workspace-governance@latest  

# 2) 启用插件  
openclaw plugins enable openclaw-workspace-governance  

# 3) 验证技能配置  
openclaw skills list --eligible  
```  

**在 OpenClaw 聊天窗口中执行：**  
```text  
/gov_setup check  
/gov_setup install  
/gov_audit  
```  

**已安装用户（升级流程：**  
```bash  
# 如果插件已存在，请勿再次运行安装命令  
openclaw plugins update openclaw-workspace-governance  
openclaw gateway restart  
```  

**随后在 OpenClaw 聊天窗口中执行：**  
```text  
/gov_setup check  
/gov_setup upgrade  
/gov_migrate  
/gov_audit  
```  

## 您将获得的功能：  
1. `gov_setup`：支持 `install`、`upgrade` 和 `check` 操作。  
2. `gov_migrate`：用于治理规则的升级。  
3. `gov_audit`：执行 12 项一致性检查。  
4. `gov_apply <NN>`：用于控制 BOOT 提案的提交流程。  
5. `gov_openclaw_json`：用于控制平台配置的更新：  
   - 更新范围：`~/.openclaw/openclaw.json`  
   - 在需要时更新：`~/.openclaw/extensions/`  
   - 不包括 Brain Docs（`USER.md`、`SOUL.md`、`memory/*.md`）或普通工作空间文档。  
6. `gov_brain_audit`：用于 Brain Docs 的风险审核：  
   - 默认为只读预览模式  
   - 需要批准后才能进行差异更新，并提供备份  
   - 只有在存在有效备份的情况下才能回滚。  

## 哪个命令适用于什么场景（快速参考）：  
1. 新建工作空间：`gov_setup install`  
2. 升级现有治理规则：`gov_setup upgrade`  
3. 应用治理规则变更：`gov_migrate`  
4. 验证一致性：`gov_audit`  
5. 提交已批准的 BOOT 提案：`gov APPLY <NN>`  
6. 安全地修改 OpenClaw 平台配置：`gov_openclaw_json`  
7. 安全地审核 Brain Docs：`gov_brain_audit` → `gov_brain_audit APPROVE` → `gov_brain_audit ROLLBACK`（如需回滚）  

## 首次运行时的状态判断：  
执行 `/gov_setup check` 后：  
- 如果显示 “NOT_INSTALLED”，则运行 `/gov_setup install`。  
- 如果显示 “PARTIAL”，则运行 `/gov_setup upgrade`。  
- 如果显示 “READY”，则依次运行 `/gov_migrate` 和 `/gov_audit`。  

## 重要更新规则：  
如果 `openclaw plugins install ...` 报告 “插件已存在”，请执行以下操作：  
1. `openclaw plugins update openclaw-workspace-governance`  
2. `openclaw gateway restart`  
3. 接着运行 `/gov_setup upgrade` → `/gov_migrate` → `/gov_audit`  

**版本检查（操作员端）：**  
- 已安装：`openclaw plugins info openclaw-workspace-governance`  
- 最新版本：`npm view @adamchanadam/openclaw-workspace-governance version`  

**运行时权限控制规则（重要）：**  
1. 仅允许执行读取/测试命令，禁止写入/更新操作。  
2. 执行写入/更新操作前，必须提供相应的计划（PLAN）和验证依据（READ）。  
3. 如果被运行时权限系统阻止，通常表示治理规则生效（而非系统故障）。  
4. 确保治理系统输出中包含 `WG_PLAN_gate_OK` 和 `WG_READ_gate_OK`，然后再重试。  
5. 最终响应格式应为：`STATUS` → `WHY` → `NEXT STEP (Operator)` → `COMMAND TO COPY`。  
6. 如果 `gov_setup upgrade` 仍提示权限问题，先更新插件至最新版本并重启网关，然后重新执行 `/gov_setup check` 和 `gov_setup upgrade`。  

**如果路径导航不稳定，请使用备用命令：**  
```text  
/skill gov_setup check  
/skill gov_setup install  
/skill gov_setup upgrade  
/skill gov_migrate  
/skill gov_audit  
/skill gov APPLY 01  
/skill gov_openclaw_json  
/skill gov_brain_audit  
/skill gov_brain_audit APPROVE: APPLY_ALL_SAFE  
/skill gov_brain_audit ROLLBACK  
```  

**或使用自然语言提示：**  
“请以只读模式运行 `gov_setup`，并获取工作空间的根目录信息、当前状态及下一步操作建议。”  

**适用人群：**  
1. 需要引导式安装流程的新 OpenClaw 用户。  
2. 需要维护长期运行工作空间的团队。  
3. 需要可审计、低风险维护方案的用户。  

**更多信息（GitHub 文档）：**  
1. 主文档：https://github.com/Adamchanadam/OpenClaw-WORKSPACE-GOVERNANCE  
2. 英文版 README：https://github.com/Adamchanadam/OpenClaw-WORKSPACE-GOVERNANCE/blob/main/README.md  
3. 繁体中文版 README：https://github.com/Adamchanadam/OpenClaw-WORKSPACE-GOVERNANCE/blob/main/README.zh-HK.md  
4. 治理手册（英文）：https://github.com/Adamchanadam/OpenClaw-WORKSPACE-GOVERNANCE/blob/main/WORKSPACE_GOVERNANCE_README.en.md