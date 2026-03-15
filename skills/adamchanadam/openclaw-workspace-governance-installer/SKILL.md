---
name: openclaw-workspace-governance-installer
description: 几分钟内即可安装 OpenClaw WORKSPACE_GOVERNANCE。该工具提供引导式设置、升级检查、迁移支持以及对长期运行的工作空间的审计功能。
author: Adam Chan
user-invocable: true
metadata: {"openclaw":{"emoji":"🚀","homepage":"https://github.com/Adamchanadam/OpenClaw-WORKSPACE-GOVERNANCE","requires":{"bins":["openclaw"]}}}
---# OpenClaw 工作空间治理安装程序

从第一天起，就让 OpenClaw 的运行更加安全。  
该安装程序为您提供了一套可重复使用的治理流程，而非依赖临时命令进行手动编辑的方案。

## 为何如此受欢迎  
1. 避免了“先编辑后验证”的错误。  
2. 确保了设置、升级和审计流程的一致性。  
3. 使所有更改都能被追踪，便于审查和交接。  
4. 既适合初学者，也适用于生产环境中的工作空间。  

## 60 秒快速入门  
首次安装：  
```bash
# 1) Install plugin
openclaw plugins install @adamchanadam/openclaw-workspace-governance@latest
openclaw gateway restart
```  

在 OpenClaw 聊天窗口中：  
```text
/gov_setup quick
```  
如果 `/gov_setup quick` 显示允许列表尚未准备好：  
```text
/gov_openclaw_json
/gov_setup quick
```  

已安装（需要升级）：  
```bash
openclaw plugins update openclaw-workspace-governance
openclaw gateway restart
```  
此时在 OpenClaw 聊天窗口中：  
```text
/gov_setup quick
```  
如果允许列表仍未准备好：  
```text
/gov_openclaw_json
/gov_setup quick
```  

## 您将获得什么  
1. `gov_setup quick|check|install|upgrade` — 一步完成部署、升级或治理规则的验证。  
2. `gov_migrate` — 安装或升级后，使工作空间的行为符合最新的治理规则。  
3. `gov_audit` — 进行 12 项完整性检查，确保一切正常后再宣布完成。  
4. `gov_uninstall quick|check|uninstall` — 安全卸载系统，并保留备份及操作记录。  
5. `gov_openclaw_json` — 可在备份、验证和回滚机制的支持下安全编辑平台配置文件（`openclaw.json`）。  
6. `gov_brain_audit` — 预览后再审核 Brain Docs 的质量，并提供回滚功能。  
7. `gov_boot_audit` — 扫描潜在问题并生成升级建议（仅限读写权限的诊断工具）。  
8. `gov APPLY <NN>` — 需经过明确人工审批后应用单个升级提案（**实验性功能**，仅限受控的用户验收测试）。  
9. `gov_help` — 一目了然地查看所有命令及推荐的使用方式。  

## 功能成熟度（重要说明）  
1. 生产环境推荐流程：`gov_setup -> gov_migrate -> gov_audit`，后续还包括 `gov_uninstall`、`gov_openclaw_json`、`gov_brain_audit` 和 `gov_boot_audit`。  
2. 实验性流程：`gov_apply <NN>` 仍处于受控的用户验收测试阶段。  
3. 所有 `/gov_` 系列命令的输出均采用统一格式：包含 `🐾` 标头、表情符号状态指示（✅/⚠️/❌）、结构化列表以及 `👉` 指导信息。  

## 如何选择合适的命令  
1. 日常使用：`gov_setup quick`（一键完成全部流程）。  
2. 安装或升级后：先执行 `gov_migrate`，再执行 `gov_audit`。  
3. 安全编辑平台配置：使用 `gov_openclaw_json`。  
4. 审核 Brain Docs：使用 `gov_brain_audit`。  
5. 扫描潜在问题：使用 `gov_boot_audit`。  
6. 安全卸载：使用 `gov_uninstall quick`。  

## 适用人群  
1. 需要引导式安装流程的新 OpenClaw 用户。  
2. 需要长期维护工作空间的团队。  
3. 需要可审计、低风险维护方案的用户。  

## 更多信息（GitHub 文档）  
1. 官方文档：https://github.com/Adamchanadam/OpenClaw-WORKSPACE-GOVERNANCE  
2. 英文版 README：https://github.com/Adamchanadam/OpenClaw-WORKSPACE-GOVERNANCE/blob/main/README.md  
3. 繁体中文版 README：https://github.com/Adamchanadam/OpenClaw-WORKSPACE-GOVERNANCE/blob/main/README.zh-HK.md  
4. 治理手册（英文）：https://github.com/Adamchanadam/OpenClaw-WORKSPACE-GOVERNANCE/blob/main/WORKSPACE_GOVERNANCE_README.en.md  
5. 治理手册（繁体中文）：https://github.com/Adamchanadam/OpenClaw-WORKSPACE-GOVERNANCE/blob/main/WORKSPACE_GOVERNANCE_README.md