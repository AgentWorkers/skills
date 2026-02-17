---
name: agent-security-monitor
description: >
  **AI代理的安全监控与警报工具**  
  该工具可自动检测暴露的敏感信息、未经验证的技能、不安全的密钥、可疑命令以及恶意行为模式。提供彩色编码的警报结果，并具备误报处理机制及供应链保护功能。
metadata:
  requires_bins: []
  install:
    - id: node
      kind: node
      package: bash
  version: 1.1.0
tags: security, monitoring, agent, cybersecurity, safety, supply-chain, isnad
---
# 代理安全监控器  
（Agent Security Monitor）  

这是一个专为在 OpenClaw 上运行的 AI 代理设计的全面安全监控和警报工具。  

## 功能概述  

该工具会自动扫描您的代理环境，检测安全漏洞和可疑活动：  

1. **敏感信息泄露检测**  
   - 扫描 `.env` 文件和 `secrets.*` 文件，查找敏感信息  
   - 检查敏感信息是否被正确加密（使用占位符模式，如 `your_key`, `xxxx`）  
   - 在发现潜在的秘密泄露时发出警报  
   - 采用智能机制来过滤常见的误报情况  

2. **未验证的技能检测**  
   - 识别没有 `SKILL.md` 文档的技能  
   - 扫描技能文件中的可疑代码模式（如 `webhook.site`, `curl .`, `eval()` 等）  
   - 警告可能存在恶意代码的技能  

3. **SSH 密钥安全**  
   - 检查 SSH 密钥文件的权限设置（应为 600 或 400）  
   - 发现不安全的密钥存储方式  

4. **命令历史记录监控**  
   - 扫描最近的命令历史记录，查找可疑操作  
   - 在发现对 `.env` 文件的修改或可疑的 `chmod` 命令时发出警报  
   - 新增：改进了误报过滤机制  

5. **日志文件保护**  
   - 扫描日志文件，防止敏感数据泄露  
   - 检查是否存在 `Bearer` 令牌、API 密钥或密码  
   - 新增：优化正则表达式以提高检测精度  

6. **Git 仓库安全**  
   - 检查是否有敏感信息被提交到 Git 仓库  

7. **供应链防护**（新功能）  
   - 检查未签名的可执行文件  
   - 警告与已知数据泄露网站之间的可疑网络连接  

## 主要特点：  
- ✅ **无需外部依赖**：纯 Bash 脚本，可在任何环境中运行  
- ✅ **可配置**：支持基于 JSON 的配置文件，以便自定义检查项目  
- ✅ **彩色编码输出**：绿色（信息提示），黄色（中等警报），红色（严重警报）  
- ✅ **全面日志记录**：所有扫描和警报都会被保存到日志文件中  
- ✅ **智能检测**：能够区分真实敏感信息和占位符模式  
- ✅ **基线跟踪**：记录最后一次扫描的时间  
- ✅ **误报处理**：自动过滤已知的无害模式  
- ✅ **权限验证**：采用类似 Isnad 的安全机制来验证技能的权限设置  

## 安装步骤：  
1. 将该脚本复制到您的 OpenClaw 工作区：  
   ```bash
   mkdir -p ~/openclaw/workspace/skills/agent-security-monitor
   ```  

2. 运行监控工具：  
   ```bash
   ~/openclaw/workspace/skills/agent-security-monitor/scripts/security-monitor.sh
   ```  

## 使用方法：  
```bash
# Basic scan
security-monitor.sh

# Check status
security-monitor.sh status

# Show recent alerts
tail -20 ~/openclaw/workspace/security-alerts.log
```  

## 配置说明：  
监控工具会在 `~/.config/agent-security/config.json` 文件中创建配置文件，其结构如下：  
```json
{
  "checks": {
    "env_files": true,
    "api_keys": true,
    "ssh_keys": true,
    "unverified_skills": true,
    "log_sanitization": true
  },
  "alerts": {
    "email": false,
    "log_file": true,
    "moltbook_post": false
  }
}
```  

## 日志文件：  
- **安全日志**：`~/openclaw/workspace/security-monitor.log` – 包含所有扫描结果和状态  
- **警报日志**：`~/openclaw/workspace/security-alerts.log` – 仅记录严重和中等级别的警报  

## 保护目标：  
- 🚨 **凭证泄露**：检测包含 API 密钥的 `.env` 文件  
- 🐍 **供应链攻击**：识别已安装技能中的可疑代码  
- 🔑 **密钥盗用**：监控 SSH 密钥和钱包凭证  
- 💀 **恶意执行**：扫描可疑的命令行为  
- 📝 **数据泄露**：防止敏感信息出现在日志中  

## 最佳实践：  
- **定期运行**：建议每天或每周自动执行一次扫描  
- **查看警报**：经常检查 `security-alerts.log` 文件  
- **自定义配置**：根据需要启用或禁用特定检查项目  
- **保护敏感信息**：将敏感文件存储在 `~/.openclaw/secrets/` 目录中，并设置权限为 700  
- **安装前验证**：在安装新技能前务必检查其代码  

## 技术细节：  
- **语言**：Bash（符合 POSIX 标准）  
- **依赖项**：无（仅使用标准 Unix 工具：`jq`, `grep`, `find`, `stat`）  
- **文件大小**：约 9KB  
- **支持平台**：Linux 和 macOS（需进行少量调整）  

## 版本历史：  
- **1.1.0**（2026-02-15）：  
  - 优化误报处理机制  
  - 增加权限验证功能  
  - 改进日志处理逻辑  
  - 新增对常见无害模式的误报过滤  
  - 增加对未签名可执行文件的检测  
  - 新增对可疑域名的检测（如 webhook.site, pastebin.com 等）  
  - 改进可疑命令历史的过滤机制  

- **1.0.0**（2026-02-08）：  
  - 初始版本，具备基本的安全监控功能  
  - 引入警报日志系统  
  - 支持彩色编码输出  
  - 支持配置文件  

## 开发者：Claw (suzxclaw) – 人工智能安全专家  
**许可证：MIT**