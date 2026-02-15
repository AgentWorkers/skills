---
name: openclaw-security-hardening
description: 保护 OpenClaw 安装环境，防止提示框注入（prompt injection）、数据泄露、恶意操作以及工作区的篡改。
version: 1.0.0
author: openclaw-community
tags: [security, hardening, audit, protection]
---

# OpenClaw 安全加固

这是一套全面的安全工具包，用于保护 OpenClaw 安装环境免受恶意技能文件、提示注入、数据泄露和工作区篡改等攻击的威胁。

## 威胁模型

本工具包可防御以下威胁：

| 威胁 | 描述 | 使用工具 |
|--------|-------------|------|
| **提示注入** | 恶意技能文件包含用于覆盖系统提示、忽略安全规则或操控代理行为的指令 | `scan-skills.sh` |
| **数据泄露** | 恶意技能文件指示代理将敏感数据（如凭证、内存内容、配置信息）发送到外部服务器 | `audit-outbound.sh` |
| **技能文件篡改** | 安装后的技能文件被未经授权地修改 | `integrity-check.sh` |
| **工作区安全漏洞** | 敏感文件的权限设置不当、`.gitignore` 规则缺失或网关配置不安全 | `harden-workspace.sh` |
| **供应链攻击** | 安装的技能文件中隐藏了恶意代码 | `install-guard.sh` |

## 快速入门

```bash
# Run a full security scan of all installed skills
./scripts/scan-skills.sh

# Audit outbound data flow patterns
./scripts/audit-outbound.sh

# Initialize integrity baseline
./scripts/integrity-check.sh --init

# Harden your workspace
./scripts/harden-workspace.sh --fix

# Check a new skill before installing
./scripts/install-guard.sh /path/to/new-skill/
```

## 工具介绍

### 1. `scan-skills.sh` — 技能文件扫描器

扫描所有已安装的技能文件，检测是否存在提示注入、数据泄露尝试、可疑 URL、隐藏的 Unicode 字符、混淆的命令以及社会工程学攻击的迹象。

**使用方法：**
```bash
# Scan all skill directories
./scripts/scan-skills.sh

# Scan a specific directory only
./scripts/scan-skills.sh --path /path/to/skills/

# Output as JSON for automation
./scripts/scan-skills.sh --json

# Show help
./scripts/scan-skills.sh --help
```

**检测内容：**
- 覆盖系统提示的恶意指令
- 用于发送敏感数据的 HTTP/HTTPS 请求
- 可能用于窃取数据的 URL（如 webhooks、pastebin、requestbin、ngrok 等）
- 可能隐藏恶意指令的 Base64 编码内容
- 隐藏的 Unicode 字符（零宽度空格、RTL 文字顺序反转等）
- 对敏感文件（如 `.env`、凭证、API 密钥、令牌）的引用
- 用于修改系统文件的指令（如 `AGENTS.md`、`SOUL.md`）
- 被混淆的命令（如十六进制编码、Unicode 转义等）
- 社会工程学攻击的提示（如“不要告知用户”、“秘密执行”等）

**严重程度：**
- 🔴 **严重** — 可能具有恶意性，需立即采取行动
- 🟡 **警告** — 值得怀疑，需手动检查
- 🔵 **信息提示** — 虽然值得关注，但通常为良性行为

---

### 2. `integrity-check.sh` — 技能文件完整性监控器

为所有技能文件生成 SHA256 哈希值，并检测文件是否被未经授权地修改。

**使用方法：**
```bash
# Initialize baseline (first run)
./scripts/integrity-check.sh --init

# Check for changes (run periodically)
./scripts/integrity-check.sh

# Update baseline after reviewing changes
./scripts/integrity-check.sh --update

# Check specific directory
./scripts/integrity-check.sh --path /path/to/skills/

# Show help
./scripts/integrity-check.sh --help
```

**报告结果：**
- ✅ 未修改的文件
- ⚠️ 被修改的文件（哈希值不一致）
- 🆕 新添加的文件（不在哈希值基准中）
- ❌ 被删除的文件（在基准中存在但实际已删除）

**自动化建议：** 将该脚本添加到系统的心跳脚本或 cron 任务中，每天执行一次：

```bash
# In HEARTBEAT.md or cron
0 8 * * * /path/to/scripts/integrity-check.sh 2>&1 | grep -E '(MODIFIED|NEW|REMOVED)'
```

---

### 3. `audit-outbound.sh` — 出站数据流审计器

监控技能文件中可能导致数据泄露的代码行为。

**使用方法：**
```bash
# Audit all skills
./scripts/audit-outbound.sh

# Audit specific directory
./scripts/audit-outbound.sh --path /path/to/skills/

# Show whitelisted domains
./scripts/audit-outbound.sh --show-whitelist

# Add domain to whitelist
./scripts/audit-outbound.sh --whitelist example.com

# Show help
./scripts/audit-outbound.sh --help
```

**检测内容：**
- 技能文件中包含的 HTTP/HTTPS URL
- 对 `curl`、`wget`、`fetch`、`web_fetch`、浏览器导航等操作的引用
- 用于发送数据的电子邮件/消息/Webhook 功能
- 指令中包含的原始 IP 地址
- 未被允许访问的外部域名

---

### 4. `harden-workspace.sh` — 工作区安全加固工具

检查并修复 OpenClaw 工作区中的常见安全配置问题。

**使用方法：**
```bash
# Check only (report issues)
./scripts/harden-workspace.sh

# Auto-fix safe issues
./scripts/harden-workspace.sh --fix

# Show help
./scripts/harden-workspace.sh --help
```

**检查内容：**
- 敏感文件（如 `MEMORY.md`、`USER.md`、`SOUL.md`、凭证文件）的权限设置
- `.gitignore` 文件中是否包含对敏感文件的屏蔽规则
- 网关认证配置
- 数据库管理（DM）策略设置
- 版本控制文件中的敏感内容

---

### 5. `install-guard.sh** — 安装前安全检查工具

在安装新技能之前运行此脚本，以检测文件中是否存在恶意内容。

**使用方法：**
```bash
# Check a skill before installing
./scripts/install-guard.sh /path/to/new-skill/

# Strict mode (fail on warnings too)
./scripts/install-guard.sh --strict /path/to/new-skill/

# Show help
./scripts/install-guard.sh --help
```

**检查内容：**
- `scan-skills.sh` 中检测到的所有恶意模式
- 脚本中的危险命令（如 `rm -rf`、`curl|bash`、`eval` 等）
- 如果存在 `package.json` 文件，则检查其中的 npm 依赖项
- 执行结果：0 表示安全；1 表示存在可疑内容（适用于持续集成/自动化流程）

## 安全规则模板

将 `assets/security-rules-template.md` 复制到 `AGENTS.md` 文件中，为代理添加运行时的安全规则。这些规则会指示代理拒绝提示注入请求并保护敏感数据。

```bash
cat assets/security-rules-template.md >> /path/to/AGENTS.md
```

## 推荐的设置流程：

1. **初始设置：**
   ```bash
   ./scripts/scan-skills.sh              # Scan existing skills
   ./scripts/audit-outbound.sh           # Audit outbound patterns
   ./scripts/integrity-check.sh --init   # Create baseline
   ./scripts/harden-workspace.sh --fix   # Fix workspace issues
   ```

2. 从模板中将安全规则添加到 `AGENTS.md` 文件中。
3. 在安装新技能之前，执行 `install-guard.sh` 脚本进行安全检查。
4. 定期执行安全检查（可通过心跳脚本或 cron 任务实现）：
   ```bash
   ./scripts/integrity-check.sh          # Detect tampering
   ./scripts/scan-skills.sh              # Re-scan for new patterns
   ```