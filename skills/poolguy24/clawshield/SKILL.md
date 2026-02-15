---
name: clawshield
display_name: ClawShield
version: 1.1.0
description: "OpenClaw安全审计工具及提示注入检测器：用于扫描网关、漏洞、定时任务（cron）以及特定脚本模式（PI patterns）。适用于提升安装过程的安全性，防止潜在的安全风险。"
category: security
author: Jeffrey Coleman (smallbizailab79@gmail.com)
price: 9.99
inputs: []
outputs:
  - JSON report printed to stdout
---

# ClawShield

## 目的  
审计本地 OpenClaw 安装环境的安全状况及常见的提示注入（prompt-injection）攻击迹象，并生成 JSON 报告以供审查和警报使用。

## 工作流程  
1. **启动面板服务器**：启动面板服务器并展示用户界面。  
2. **用户配置**：修改 `config.yaml` 文件（设置扫描频率、警报规则和敏感度）。  
3. **定时任务设置**：使用 Cron 任务定期执行 `scripts/audit.sh` 脚本。  
4. **报告与警报**：查看 JSON 输出结果；若发现提示注入攻击或异常开放的端口，立即发出警报。  

## 使用方法  
### 通过面板界面进行审计（推荐）  
```bash
node scripts/panel-server.js
```  
启动面板服务器后，可以通过以下地址访问用户界面：  
`http://localhost:8133`  
（菜单选项包括：扫描、设置、日志等。）  

### 通过命令行进行配置  
```bash
node scripts/config.js get
node scripts/config.js set Scan_freq daily alerts telegram sensitivity high
```  

### 通过命令行执行审计  
```bash
bash scripts/audit.sh > report.json
```  

## 注意事项  
- 仅扫描本地系统，不会发起任何超出 `localhost` 范围的网络请求。  
- 面板服务器运行在本地，会将最新的审计报告保存在 `logs/last-report.json` 文件中。  
- `config.yaml` 的默认配置为：  
  - `Scan_freq=daily`（每日扫描）  
  - `alerts=telegram`（通过 Telegram 发送警报）  
  - `sensitivity=high`（高敏感度设置）  
- 适用于常规安全检查及预防突发安全事件。  

联系人：Jeffrey Coleman  
邮箱：smallbizailab79@gmail.com  
服务范围：定制审计服务/企业级解决方案。