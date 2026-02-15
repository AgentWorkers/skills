---
name: molt-security-auditor-v3
description: "**Bulletproof Creds/Ports/Configs/Vulns Scan + Safe Auto-Fix V3.100% Secure – No Injection/Lockout/Exfiltration.**  
适用于主机审计（笔记本电脑、树莓派、虚拟私有服务器）。  

**功能特点：**  
1. **全面的安全扫描**：检测账号凭证、网络端口配置及系统漏洞。  
2. **自动修复机制**：发现安全问题后，立即进行自动修复，确保系统100%安全。  
3. **无风险操作**：完全避免注入攻击、账户锁定或数据泄露等风险。  
4. **兼容多种设备**：支持笔记本电脑、树莓派和虚拟私有服务器等设备。  

**主要优势：**  
- **高效安全**：快速准确地识别潜在风险。  
- **自动修复**：减少人工干预，提升系统安全性。  
- **无风险使用**：确保用户操作过程中的安全性。  

**适用场景：**  
- **企业安全审计**  
- **系统维护**  
- **远程管理**  

**立即使用！**  
bulletproofcreds/ports/configs/vulns_scan_v3 是一款功能强大的安全工具，能有效保护您的系统和数据安全。"
---

# Molt Security Auditor V3（防篡改版）

提供扫描与修复功能（预览/验证模式）。所有操作均经过严格编码，确保安全性，不存在恶意路径的风险。

## 快速使用指南
```bash
node scripts/audit.js --full     # Scan → security-report-v3.json
node scripts/audit.js --fix      # Guided fixes
node scripts/audit.js --auto     # Preview → Run + verify
node scripts/rollback.js         # Atomic revert
```

## 扫描功能：
- **凭证检查**：仅通过哈希值进行匹配（如 `sk-*, api_key`）——每100个文件检查1MB的数据量。
- **端口检测**：使用 `netstat`, `ss`, `lsof` 命令检测开放的端口。
- **配置审核**：检查 SSH 密码、root 用户权限以及 `sudo` 权限的设置。
- **漏洞检测**：通过 `npm audit` 和 `openclaw update` 功能识别系统漏洞。

## V3 版本的安全特性：
- **不可篡改的命令执行**：所有命令均被硬编码到白名单中，防止注入攻击。
- **互斥锁机制**：命令执行后锁定5分钟，确保并发安全性。
- **数据备份**：生成只读备份文件，并通过 SHA 算法进行验证。
- **执行超时设置**：命令执行时间限制为5-10秒。
- **跨平台支持**：兼容 Windows、Linux 和 Mac 系统。
- **执行前后对比**：执行前后会对比系统状态，确保操作的正确性。
- **回滚机制**：通过 `backup/*.bak` 文件实现一键恢复。

**报告生成**：生成 `security-report-v3.json` 格式的安全报告（采用安全的 JSON 格式）。

该工具已适配生产环境使用，同时兼容 ClawdHub V3 平台。