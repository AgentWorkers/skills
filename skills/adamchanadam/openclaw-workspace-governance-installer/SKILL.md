---
name: openclaw-workspace-governance-installer
description: 只需几分钟，即可安装 OpenClaw WORKSPACE_GOVERNANCE。该工具提供指导性的设置流程、升级检查、迁移支持以及针对长期运行的工作空间的审计功能。
author: Adam Chan
user-invocable: true
metadata: {"openclaw":{"emoji":"🚀","homepage":"https://github.com/Adamchanadam/OpenClaw-WORKSPACE-GOVERNANCE","requires":{"bins":["openclaw"]}}}
---# OpenClaw 工作空间治理安装程序

从第一天起，就让 OpenClaw 的运行更加安全。  
该安装程序为您提供了一套可重复使用的治理流程，避免了随意修改命令行的情况。  

## 为何如此受欢迎  
1. 防止“先修改再验证”的错误。  
2. 确保设置、升级和审计流程的一致性。  
3. 让所有变更都可追溯，便于审查和交接。  
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
1. `gov_setup` 命令，用于执行安装、升级和检查操作。  
2. `gov_migrate` 命令，用于治理系统的升级。  
3. `gov_audit` 命令，用于进行全面的一致性检查。  
4. `gov_apply <NN>` 命令，用于提交受控的启动提案。  
5. `gov_platform_change` 命令，用于受控地更新 `~/.openclaw/openclaw.json` 文件。  

## 首次运行后的状态判断  
执行 `/gov_setup check` 后：  
- 如果显示“NOT_INSTALLED”，则运行 `/gov_setup install`。  
- 如果显示“PARTIAL”，则运行 `/gov_setup upgrade`。  
- 如果显示“READY”，则依次运行 `/gov_migrate` 和 `/gov_audit`。  

## 重要更新规则  
如果 `openclaw plugins install ...` 命令返回“plugin already exists”（插件已存在）的提示，请执行以下操作：  
1. 使用 `openclaw plugins update openclaw-workspace-governance` 更新插件。  
2. 重启 OpenClaw 服务（`openclaw gateway restart`）。  
3. 接着依次执行 `/gov_setup upgrade`、`/gov_migrate` 和 `/gov_audit`。  

## 如果路径导航不稳定  
请使用备用命令：  
```text
/skill gov_setup check
/skill gov_setup install
/skill gov_migrate
/skill gov_audit
```  

或者使用自然语言提示：  
```text
Please use gov_setup in check mode (read-only) and return workspace root, status, and next action.
```  

## 适用对象  
1. 需要引导式安装流程的新 OpenClaw 用户。  
2. 需要管理长期运行工作空间的团队。  
3. 需要可审计、低维护成本的工作空间管理方案的用户。  

## 更多信息（GitHub 文档）  
1. 主文档：https://github.com/Adamchanadam/OpenClaw-WORKSPACE-GOVERNANCE  
2. 英文版 README：https://github.com/Adamchanadam/OpenClaw-WORKSPACE-GOVERNANCE/blob/main/README.md  
3. 繁体中文版 README：https://github.com/Adamchanadam/OpenClaw-WORKSPACE-GOVERNANCE/blob/main/README.zh-HK.md  
4. 治理手册（英文）：https://github.com/Adamchanadam/OpenClaw-WORKSPACE-GOVERNANCE/blob/main/WORKSPACE_GOVERNANCE_README.en.md