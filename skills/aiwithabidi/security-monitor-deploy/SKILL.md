---
name: security-monitor
description: Comprehensive security audit for OpenClaw deployments. Checks Docker port bindings, SSH config, openclaw.json settings, file permissions, exposed services, and firewall rules. Scores your deployment 0-100 with actionable recommendations. Use for security hardening and compliance checks.
homepage: https://www.agxntsix.ai
license: MIT
compatibility: Docker, OpenClaw gateway, Linux
metadata: {"openclaw": {"emoji": "\ud83d\udee1\ufe0f", "requires": {"bins": ["docker"]}, "homepage": "https://www.agxntsix.ai"}}
---

# 安全监控器 🛡️  
**针对 OpenClaw 部署的全面安全审计工具。**  

该工具会扫描您的 Docker 配置、SSH 设置、防火墙规则、OpenClaw 配置以及文件权限，并生成一个安全评分（0-100 分），同时提供可操作的改进建议。  

## 快速入门  
```bash
# Run full audit
bash {baseDir}/scripts/security_audit.sh

# JSON output
bash {baseDir}/scripts/security_audit.sh --json

# Specific checks only
bash {baseDir}/scripts/security_audit.sh --check docker
bash {baseDir}/scripts/security_audit.sh --check ssh
bash {baseDir}/scripts/security_audit.sh --check config
bash {baseDir}/scripts/security_audit.sh --check files
bash {baseDir}/scripts/security_audit.sh --check network
```  

## 审计内容  

### OpenClaw 配置（25 分）  
- `allowInsecureAuth` 必须设置为 `false`  
- `dmPolicy` 不能设置为“开放”或“允许所有连接”（allow-all）  
- 端口绑定必须使用 `127.0.0.1`  
- API 密钥不能硬编码在配置文件中  
- 模型的权限设置必须安全  

### Docker 安全（25 分）  
- 所有端口绑定都必须使用 `127.0.0.1`（而非 `0.0.0.0`）  
- 除非必要，否则禁止使用特权容器  
- 配置正确的 Docker 套接字权限  
- 设置合理的容器资源限制  
- 除非确实需要，否则禁止使用 `--net=host` 选项  

### SSH 配置（20 分）  
- 禁用 root 用户登录（`PermitRootLogin no`）  
- 仅支持基于密钥的认证方式  
- 使用非标准端口（可加分）  
- 必须启用 Fail2ban 或类似的安全机制  

### 网络与服务（15 分）  
- 无不必要的公开端口  
- 防火墙（如 ufw/iptables）处于启用状态  
- 只有预期的服务在运行  
- 配置了 HTTPS/TLS 安全传输  

### 文件权限（15 分）  
- `openclaw.json` 文件不能被全局用户读取  
- SSH 密钥的权限设置正确（600 模式）  
-.env 文件不能被全局用户读取  
- 配置正确的 Docker 套接字权限  
- /tmp 目录中不存在敏感文件  

## 评分标准  

| 评分 | 等级 | 含义 |  
|-------|--------|---------|  
| 90-100 | 🟢 | 非常优秀 | 可以直接用于生产环境  
| 70-89 | 🟡 | 需要少量改进  
| 50-69 | 🟠 | 存在一些问题，需要处理  
| 0-49 | 🔴 | 需立即采取行动  

## 输出示例  
```
═══ Security Audit Report ═══
Date: 2026-02-15 00:30:00

[CONFIG] ✅ allowInsecureAuth: false
[CONFIG] ✅ dmPolicy: allowlist
[CONFIG] ✅ Ports bound to 127.0.0.1
[DOCKER] ✅ All containers bind to 127.0.0.1
[DOCKER] ⚠️  No resource limits on openclaw container
[SSH]    ✅ Root login disabled
[SSH]    ✅ Password auth disabled
[NET]    ✅ UFW active
[FILES]  ✅ Config file permissions OK

Score: 92/100 — 🟢 Excellent
Issues: 1 warning

Recommendations:
  1. Add resource limits to Docker containers
```  

## 致谢  
该工具由 [M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) 和 [agxntsix.ai](https://www.agxntsix.ai) 开发。  
更多信息请访问：[YouTube](https://youtube.com/@aiwithabidi) | [GitHub](https://github.com/aiwithabidi)  
本工具属于 **AgxntSix Skill Suite** 的一部分，专为 OpenClaw 代理设计。  

📅 **需要帮助为您的企业配置 OpenClaw 吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)