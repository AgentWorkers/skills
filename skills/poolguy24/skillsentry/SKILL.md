---
name: skillsentry
display_name: SkillSentry
version: 1.1.0
description: "OpenClaw安全审计工具及提示注入检测器：用于扫描网关漏洞、定时任务（cron）中的安全隐患以及特定代码模式（如PI patterns）。该工具专为确保安装过程的安全性而设计，能有效防止恶意行为的发生。"
category: security
author: Jeffrey Coleman (smallbizailab79@gmail.com)
price: 9.99
inputs: []
outputs:
  - JSON report printed to stdout
---

# SkillSentry

## 目的
审计本地 OpenClaw 安装环境的安全状况，检测常见的命令提示符注入（prompt-injection）攻击迹象，并生成 JSON 格式的报告以供审查和报警使用。

## 工作流程
1. **启动面板服务器**：启动 SkillSentry 的面板服务器并展示用户界面。
2. **用户配置**：修改 `config.yaml` 文件（设置扫描频率、报警规则和敏感度参数）。
3. **定时任务设置**：使用 Cron 任务定期执行 `scripts/audit.sh` 脚本。
4. **报告与报警**：查看 JSON 格式的审计结果；如果检测到命令提示符注入攻击或异常开放的端口，立即发出警报。

## 使用方法
### 通过面板界面使用（推荐）
```bash
node scripts/panel-server.js
```
启动面板服务器并访问用户界面：
- `canvas.present` → `http://localhost:8133` （路径：扫描 → 设置 → 日志）

### 通过命令行界面配置
```bash
node scripts/config.js get
node scripts/config.js set Scan_freq daily alerts telegram sensitivity high
```

### 通过命令行界面执行审计
```bash
bash scripts/audit.sh > report.json
```

## 注意事项
- 仅支持本地扫描，不会发起任何超出本地主机的网络请求。
- 面板服务器运行在本地，并将最新的审计报告保存在 `logs/last-report.json` 文件中。
- `config.yaml` 的默认配置为：`Scan_freq=daily`（每日扫描）、`alerts=telegram`（通过 Telegram 发送报警）、`sensitivity=high`（高敏感度）。
- 适用于常规的安全检查以及预防突发安全事件。

联系人：Jeffrey Coleman | smallbizailab79@gmail.com | 提供定制化的审计服务/企业级解决方案。