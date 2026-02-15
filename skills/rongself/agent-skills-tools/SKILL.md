---
name: agent-skills-tools
description: >
  Security audit and validation tools for the Agent Skills ecosystem.
  Scan skill packages for common vulnerabilities like credential leaks,
  unauthorized file access, and Git history secrets.
  Use when you need to audit skills for security before installation,
  validate skill packages against Agent Skills standards,
  or ensure your skills follow best practices.
license: MIT
metadata:
  openclaw:
    emoji: "🔒"
    category: "security"
---

# 代理技能工具 🔒  
用于代理技能生态系统的安全性和验证工具。  

## 概述  
该工具包提供了用于审计和验证代理技能包是否存在安全漏洞以及是否符合相关标准的工具。  

## 工具  

### 1. 安全审计工具 (skill-security-audit.sh)  
该工具会扫描技能包中的常见安全问题：  

**检查内容：**  
- 🔐 凭据泄露（硬编码的 API 密钥、密码、令牌）  
- 📁 危险的文件访问（如 `~/.ssh`、`~/.aws`、`~/.config`）  
- 🌐 外部网络请求  
- 📋 环境变量的使用（推荐做法）  
- 🔑 文件权限（`credentials.json` 文件）  
- 📜 Git 历史记录中是否存在敏感信息的泄露  

**使用方法：**  
```bash
./skill-security-audit.sh path/to/skill
```  

**示例输出：**  
```
🔒 技能安全审计报告：path/to/skill
==========================================

📋 检查1: 凭据泄露 (API key, password, secret, token)
----------------------------------------
✅ 未发现凭据泄露

📋 检查2: 危险的文件操作 (~/.ssh, ~/.aws, ~/.config)
----------------------------------------
✅ 未发现危险的文件访问

[... more checks ...]

==========================================
🎯 安全审计完成
```  

## 背景  
在 286 个技能包中，`eudaemon_0` 发现了 1 个存在凭证泄露问题的技能包。由于代理技能被设计为友好且信任用户，因此它们容易受到恶意技能的攻击。  
这些工具有助于在漏洞造成损害之前将其发现并修复。  

## 最佳实践：  
1. **切勿硬编码凭证**  
   - ❌ `API_KEY="sk_live_abc123..."`  
   - ✅ 从环境变量或配置文件中读取凭证  

2. **使用环境变量**  
   ```bash
   export MOLTBOOK_API_KEY="sk_live_..."
   ```  
   ```python
   import os
   api_key = os.environ.get('MOLTBOOK_API_KEY')
   ```  

3. **检查 Git 历史记录**  
   ```bash
   git log -S 'api_key'
   git-secrets --scan-history
   ```  

4. **将敏感文件添加到 `.gitignore` 文件中**  
   ```
   credentials.json
   *.key
   .env
   ```  

## 许可证**  
MIT