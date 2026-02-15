---
name: shadowstrike-security
description: 这是一个精英级的渗透测试平台，配备了600多种安全工具。
metadata:
  {
    "openclaw":
      {
        "emoji": "⚔️",
        "category": "security"
      }
  }
---

# ShadowStrike 安全平台

**精英渗透测试与安全评估平台**

将 OpenClaw 转变为一个专业的安全运营中心，配备 600 多种 Kali Linux 工具、智能化的工具编排机制以及自动化报告功能。

## 什么是 ShadowStrike？

ShadowStrike 是一个全面的安全测试平台，提供以下功能：
- **智能工具编排**：为每个任务自动选择最合适的工具
- **完整的渗透测试生命周期**：从侦察到专业报告
- **600 多种安全工具**：丰富的 Kali Linux 工具库
- **自动化工作流程**：一个命令即可完成整个评估过程

## 主要特性

### 🎯 智能侦察
- **网络发现**：nmap、masscan、unicornscan
- **Web 应用程序枚举**：dirb、gobuster、ffuf、wfuzz
- **子域名扫描**：amass、 sublist3r、assetfinder
- **开源信息收集**：theHarvester、recon-ng、maltego

### 🔍 漏洞评估
- **Web 应用程序测试**：sqlmap、nikto、dalfox、nuclei
- **网络扫描**：610 多种 NSE 脚本
- **SSL/TLS 分析**：testssl.sh、sslscan、sslyze
- **配置审查**：自动检测配置错误

### ⚔️ 专业攻击与利用
- **Web 应用程序攻击**：SQL 注入、XSS、LFI、RCE 测试
- **密码攻击**：hashcat、john（支持 GPU 加速）
- **无线网络审计**：airecrack-ng、wifite、reaver
- **漏洞利用框架**：Metasploit、searchsploit、BeEF

### 🛡️ 利用后操作
- **权限提升**：linpeas、winpeas
- **横向移动**：渗透与隧道建立
- **持久性测试**：后门检测
- **数据窃取**：安全的数据传输方式

### 📊 专业报告
- **高层风险概览**：全面的风险分析
- **技术报告**：漏洞详情与攻击路径
- **修复指南**：详细的修复步骤
- **证据收集**：截图与日志记录

## 快速入门

### 安装
```bash
cp -r shadowstrike-security ~/.openclaw/skills/
```

**配置代理服务器：**
```json
{
  "skills": ["shadowstrike-security"]
}
```

**重启系统：**
```bash
pkill -f "openclaw gateway" && openclaw gateway &
```

### 基本命令
```
"scan target.com"          → Quick port scan
"web target.com"           → Web application test
"pentest target.com"       → Full penetration test
"wifi"                     → WiFi security audit
"hashes crack hash.txt"    → Password cracking
```

## 命令参考

### 网络评估

| 命令 | 描述 | 示例输出 |
|---------|-------------|----------------|
| `scan [目标]` | 快速端口扫描 | `端口：22,80,443` |
| `deep [目标]` | 全部端口扫描（65,535 个端口） | `[扫描完成]` |
| `services [目标]` | 服务检测 | `80:nginx, 3306:mysql` |
| `os [目标]` | 操作系统识别 | `Linux 5.4` |

### Web 应用程序测试

| 命令 | 描述 | 示例输出 |
|---------|-------------|----------------|
| `web [目标]` | 全面 Web 应用程序测试 | `发现 SQL 注入漏洞（XSS 中等风险）` |
| `dirb [目标]` | 目录结构扫描 | `/admin, /api, /config` |
| `sql [目标]` | SQL 注入测试 | `检测到漏洞（id 参数）` |
| `xss [目标]` | XSS 测试 | `确认存在反射型 XSS 漏洞` |
| `vuln [目标]` | 漏洞扫描 | `严重等级：2；高风险等级：5` |

### 完整工作流程

| 命令 | 描述 | 所需时间 |
|---------|-------------|----------|
| `pentest [目标]` | 完整的渗透测试生命周期 | 10-30 分钟 |
| `bugbounty [目标] | 漏洞赏金计划 | 15-45 分钟 |
| `audit [network] | 网络安全审计 | 20-60 分钟 |
| `compliance [目标] | 合规性检查 | 30-90 分钟 |

### 专用工具

| 命令 | 描述 |
|---------|-------------|
| `wifi` | 无线网络安全审计 |
| `hashes [文件] | 解密密码哈希值 |
| `exploit [cve] | 搜索并执行漏洞利用工具 |
| `report` | 生成安全报告 |

## 工作原理

### 智能工具选择

ShadowStrike 会自动为不同类型的攻击目标选择最合适的工具：

**针对 Web 目标：**
```
Input: "test web target.com"
ShadowStrike:
  1. whatweb → Technology fingerprinting
  2. dirb → Directory discovery
  3. nikto → Vulnerability scanning
  4. sqlmap → SQL injection test
  5. dalfox → XSS testing
  6. nuclei → CVE scanning
Output: "Critical: 2, High: 5, Report: ./target-security.md"
```

**针对网络目标：**
```
Input: "scan 192.168.1.0/24"
ShadowStrike:
  1. nmap -sS → Port scanning
  2. nmap -sV → Service detection
  3. nmap -O → OS fingerprinting
  4. nmap --script=vulners → Vuln detection
Output: "Hosts: 15, Open ports: 47, Vulnerabilities: 12"
```

## 工具库

- **信息收集工具（50 多种）**：```
nmap, masscan, unicornscan, zmap
theHarvester, recon-ng, maltego
amass, sublist3r, assetfinder, findomain
```
- **Web 应用程序测试工具（60 多种）**：```
nikto, sqlmap, burpsuite, zap
dirb, gobuster, wfuzz, ffuf
dalfox, xsser, nuclei, arachni
wpscan, joomscan, droopescan
```
- **密码攻击工具（30 多种）**：```
hashcat (GPU-accelerated), john, hydra
medusa, ncrack, patator, crowbar
crunch, cewl, cupp (wordlist generators)
```
- **无线网络工具（25 多种）**：```
aircrack-ng, wifite, reaver, bully
kismet, wireshark, airmon-ng
hostapd-wpe, freeradius-wpe
```
- **漏洞利用工具（35 多种）**：```
metasploit, searchsploit, beef
setoolkit, sqlmap, commix
routersploit, exploitdb
```
- **取证工具（40 多种）**：```
autopsy, sleuthkit, volatility
foremost, scalpel, binwalk
yara, cuckoo, remnux, ghidra
```

## 工作流程示例

### 示例 1：漏洞赏金计划
```
You: "bugbounty target.com"

ShadowStrike executes:
✓ Subdomain enumeration (amass, sublist3r)
✓ Screenshot all services
✓ Technology fingerprinting
✓ Vulnerability scanning (nikto, nuclei)
✓ SQL injection testing (sqlmap)
✓ XSS testing (dalfox, xsser)
✓ SSL/TLS analysis (testssl.sh)

Results:
💰 Critical (P1): 1 - SQL Injection
💰 High (P2): 3 - XSS, IDOR, LFI
💰 Medium (P3): 5 - Various issues

Reports:
📄 P1-SQLi-report.md (Ready to submit)
📄 P2-XSS-report.md (Ready to submit)
📄 P2-IDOR-report.md (Ready to submit)

Potential Bounty: $2,000 - $5,000
```

### 示例 2：网络安全审计
```
You: "audit 192.168.1.0/24"

ShadowStrike executes:
✓ Host discovery (nmap -sn)
✓ Port scanning (nmap -sS -p-)
✓ Service detection (nmap -sV)
✓ OS fingerprinting (nmap -O)
✓ Vulnerability scanning (nmap --script=vulners)
✓ SSL testing (testssl.sh)
✓ Default credential testing

Results:
Hosts Found: 23
Open Ports: 147
Services: 89
Vulnerabilities: 34 (Critical: 3, High: 8, Medium: 23)

Report: ./network-audit-report.md
```

### 示例 3：全面渗透测试
```
You: "pentest target.com"

Phase 1: Reconnaissance (5 min)
✓ Subdomain enumeration
✓ IP range discovery
✓ Technology stack identification
✓ DNS enumeration

Phase 2: Scanning (10 min)
✓ Port scanning
✓ Service detection
✓ OS fingerprinting

Phase 3: Enumeration (10 min)
✓ User enumeration
✓ Share discovery
✓ Directory brute-forcing

Phase 4: Vulnerability Assessment (15 min)
✓ Automated scanning
✓ Manual verification
✓ Exploit research

Phase 5: Exploitation (10 min)
✓ Attempt exploitation
✓ Proof of concept
✓ Credential testing

Phase 6: Post-Exploitation (10 min)
✓ Privilege escalation testing
✓ Lateral movement
✓ Data collection

Phase 7: Reporting (5 min)
✓ Executive summary
✓ Technical findings
✓ Risk ratings
✓ Remediation steps

Final Report:
Security Score: 68/100
Critical: 2, High: 5, Medium: 8, Low: 12

Full Report: ./pentest-target-report.md
Remediation: ./pentest-target-remediation.md
Evidence: ./pentest-target-evidence/
```

## 法律与道德规范

**⚠️ 重要提示：请负责任地使用本工具**

**允许的行为：**
- ✅ 测试您自己拥有的系统
- ✅ 在获得授权的情况下测试系统
- ✅ 进行合法的渗透测试
- ✅ 对您的基础设施进行安全审计
- ✅ 参与漏洞赏金计划（在授权范围内）

**禁止的行为：**
- ❌ 未经许可测试系统
- ❌ 非法攻击系统
- ❌ 违反隐私法规
- ❌ 对系统造成损害
- ❌ 窃取数据

**法律声明：**
未经授权的访问行为属于违法行为：
- 《计算机欺诈与滥用法案》（CFAA）
- 《计算机滥用法案》（英国）
- 全球各地类似的法律

请在测试前务必获得适当的授权。

## 系统要求

- OpenClaw 版本 >= 2026.2.3
- 推荐使用 Kali Linux 2024.x
- 需要具备 sudo 权限以执行高级操作
- 最小内存要求：4GB（建议 8GB）
- 空闲磁盘空间：20GB

## 许可证

MIT 许可证——适用于教育和授权的安全测试用途

---

**ShadowStrike 安全平台：专为专业测试设计的强大工具** ⚔️🛡️