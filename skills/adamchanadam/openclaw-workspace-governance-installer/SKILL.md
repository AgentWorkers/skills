---
name: openclaw-workspace-governance-installer
description: 只需几分钟即可安装 OpenClaw WORKSPACE_GOVERNANCE。它提供引导式设置、升级检查、迁移支持以及针对长期运行的工作空间的审计功能。
author: Adam Chan
user-invocable: true
metadata: {"openclaw":{"emoji":"🚀","homepage":"https://github.com/Adamchanadam/OpenClaw-WORKSPACE-GOVERNANCE","requires":{"bins":["openclaw"]}}}
---# OpenClaw 工作空间治理安装程序

从第一天起，就确保 OpenClaw 的运行更加安全。  
该安装程序为您提供了一套可重复使用的治理流程，避免了随意修改配置的麻烦。  

## 为何如此受欢迎  
1. 防止“先修改后验证”的错误。  
2. 确保设置、升级和审计流程的一致性。  
3. 让所有变更都可追溯，便于审查和交接。  
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
/gov_setup check
/gov_setup install
/gov_audit
```  

已安装用户（升级流程）：  
```bash
# Do NOT run install again if plugin already exists
openclaw plugins update openclaw-workspace-governance
openclaw gateway restart
```  

之后在 OpenClaw 聊天窗口中：  
```text
/gov_setup check
/gov_setup upgrade
/gov_migrate
/gov_audit
```  

## 您将获得什么  
1. `gov_setup`：包含 `install`、`upgrade` 和 `check` 命令。  
2. `gov_migrate`：用于治理结构的升级。  
3. `gov_audit`：用于进行全面的一致性检查。  
4. `gov_apply <NN>`：用于提交受控制的 BOOT 提案。  
5. `gov_platform_change`：用于控制平台控制平面的更新：  
   - 更新范围：`~/.openclaw/openclaw.json`  
   - 在必要时也会更新：`~/.openclaw/extensions/`  
   - 不会修改 Brain Docs（`USER.md`、`SOUL.md`、`memory/*.md`）或普通工作空间文档。  

## 如何选择合适的命令（快速参考）  
1. 新建工作空间：`gov_setup install`  
2. 升级现有治理配置：`gov_setup upgrade`  
3. 应用治理规则变更：`gov_migrate`  
4. 检查一致性（只读模式）：`gov_audit`  
5. 提交已批准的 BOOT 提案：`gov APPLY <NN>`  
6. 安全地修改 OpenClaw 平台配置：`gov_platform_change`  

## 首次运行后的状态检查  
执行 `/gov_setup check` 后：  
1. 如果显示 “NOT_INSTALLED”，则运行 `/gov_setup install`。  
2. 如果显示 “PARTIAL”，则运行 `/gov_setup upgrade`。  
3. 如果显示 “READY”，则依次运行 `/gov_migrate` 和 `/gov_audit`。  

## 重要更新规则  
如果 `openclaw plugins install ...` 命令返回 “plugin already exists” 的提示，请执行以下操作：  
1. 使用 `openclaw plugins update openclaw-workspace-governance`。  
2. 重启 OpenClaw 的网关服务（`openclaw gateway restart`）。  
3. 接着依次执行 `/gov_setup upgrade`、`gov_migrate` 和 `/gov_audit`。  

## 运行时权限控制规则（非常重要）  
1. 仅允许执行读-only 的诊断/测试命令，这些命令不应被阻止。  
2. 执行写入/更新/保存操作的命令前，必须提供相应的计划（PLAN）和读取权限（READ）证明。  
3. 如果命令被运行时权限系统阻止，请在治理结果中包含 `WG_PLAN_GATE_OK` 和 `WG_READ_gate_OK`，然后重试。  

## 如果路径导航不稳定  
请使用备用命令：  
```text
/skill gov_setup check
/skill gov_setup install
/skill gov_setup upgrade
/skill gov_migrate
/skill gov_audit
/skill gov_apply 01
/skill gov_platform_change
```  

或者使用自然语言提示：  
```text
Please use gov_setup in check mode (read-only) and return workspace root, status, and next action.
```  

## 适用对象  
1. 需要引导式安装流程的新 OpenClaw 用户。  
2. 需要维护长期运行工作空间的团队。  
3. 需要可审计、低错误率维护环境的用户。  

## 了解更多信息（GitHub 文档）  
1. 主要文档：https://github.com/Adamchanadam/OpenClaw-WORKSPACE-GOVERNANCE  
2. 英文版 README：https://github.com/Adamchanadam/OpenClaw-WORKSPACE-GOVERNANCE/blob/main/README.md  
3. 繁体中文版 README：https://github.com/Adamchanadam/OpenClaw-WORKSPACE-GOVERNANCE/blob/main/README.zh-HK.md  
4. 治理手册（英文）：https://github.com/Adamchanadam/OpenClaw-WORKSPACE-GOVERNANCE/blob/main/WORKSPACE_GOVERNANCE_README.en.md