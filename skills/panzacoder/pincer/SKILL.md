---
name: pincer
description: 这是一个以安全为首要目标的代理技能安装封装工具。在安装之前，它会扫描系统中是否存在恶意软件、脚本注入以及可疑行为。建议使用该工具替代 `clawhub install`，以实现更安全的技能管理。
homepage: https://github.com/panzacoder/pincer
metadata:
  openclaw:
    emoji: "🦞"
    requires:
      bins: ["pincer"]
    install:
      - id: symlink
        kind: script
        label: "Install pincer to PATH"
        script: |
          chmod +x "${SKILL_DIR}/scripts/pincer.sh"
          mkdir -p ~/.local/bin
          ln -sf "${SKILL_DIR}/scripts/pincer.sh" ~/.local/bin/pincer
          echo ""
          echo "✅ pincer installed!"
          echo ""
          echo "Make sure ~/.local/bin is in your PATH:"
          echo '  export PATH="$HOME/.local/bin:$PATH"'
          echo ""
          echo "Usage:"
          echo "  pincer install <skill>  # Safe install with scanning"
          echo "  pincer scan <skill>     # Scan without installing"
          echo "  pincer audit            # Scan all installed skills"
          echo ""
---

# pincer 🛡️  
这是一个以安全为首要目标的 `clawhub install` 包装工具。在安装技能之前，它会扫描这些技能是否存在恶意软件、命令注入或可疑行为。  

## 为什么需要它？  
代理技能（agent skills）非常强大——它们本质上就是可执行的代码。ClawHub 生态系统中已经出现过通过看似无害的技能传播恶意软件的案例（参考：[https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub/](https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub/)。pincer 为你的技能安装过程添加了一层额外的安全保障。  

## 安装方法  
```bash
# From ClawHub
clawhub install pincer

# Or manually
chmod +x ./scripts/pincer.sh
ln -sf "$(pwd)/scripts/pincer.sh" ~/.local/bin/pincer
```  

**依赖项：**  
- `clawhub`：用于获取技能信息  
- `uvx`：用于执行 mcp-scan 检查（使用 `brew install uv` 安装）  
- `jq`：用于 JSON 数据解析  

## 使用方法  

### 安全安装  
```bash
# Instead of: clawhub install some-skill
pincer install some-skill

# With specific version
pincer install some-skill@1.2.0
```  

### 不安装直接扫描  
```bash
# Scan a ClawHub skill
pincer scan some-skill

# Scan a local directory
pincer scan ./path/to/skill

# JSON output for automation
pincer scan some-skill --json
```  

### 审计已安装的技能  
```bash
# Quick-scan all installed skills
pincer audit

# JSON output
pincer audit --json
```  

### 管理信任设置  
```bash
# Add trusted publisher (auto-approve clean skills)
pincer trust add steipete

# Remove from trusted
pincer trust remove old-publisher

# Block a publisher or skill
pincer trust block suspicious-dev
pincer trust block malware-skill

# Unblock
pincer trust unblock redeemed-dev

# List all trust settings
pincer trust list
```  

### 查看安装历史  
```bash
# See what you've installed
pincer history

# JSON output
pincer history --json
```  

### 配置选项  
```bash
# Show current config
pincer config show

# Edit in $EDITOR
pincer config edit

# Reset to defaults
pincer config reset
```  

## 检查内容：  

### 通过 mcp-scan（Invariant Labs）进行检测：  
- 命令注入攻击  
- 以自然语言形式存在的恶意代码  
- 工具被篡改（工具中毒）  
- 敏感数据泄露  
- 硬编码的秘密信息  

### 其他常见恶意模式：  
| 模式 | 风险等级 | 描述 |  
|---------|------|-------------|  
| Base64 编码的命令 | 🚨 高风险 | 已加密的 shell 命令  
| 十六进制格式的恶意数据 | 🚨 高风险 | 被混淆的二进制文件  
| `xattr -d quarantine` 命令 | 🚨 高风险 | 用于绕过 macOS 的安全机制（Gatekeeper）  
| `curl \| sh` 命令 | 🚨 高风险 | 通过管道将数据传递给 shell 执行  
| 隐藏的恶意文件 | ⚠️ 中等风险 | 用于隐藏恶意代码  
| 下载后立即执行的脚本 | ⚠️ 中等风险 | 类型为 `chmod +x && ./` 的脚本  
| 动态代码执行（`eval $var`） | ⚠️ 中等风险 | 动态代码的调用  
| 持久化机制（如 cron/launchd 任务） | ⚠️ 中等风险 | 用于长期隐藏恶意行为  

### 其他检测内容：  
- 发布者的信誉（可信列表）  
- 技能的下载次数  
- 技能的发布时间  
- 是否在黑名单中  

### 二进制文件检测：  
- 检查是否存在捆绑的可执行文件  
- 支持检测 Mach-O、ELF、PE32 格式的二进制文件  

## 风险等级：  
| 等级 | 含义 | 处理方式 |  
|-------|---------|--------|  
| ✅ **安全** | 无问题 | 如果来自可信发布者，则自动批准安装 |  
| ⚠️ **警告** | 存在潜在风险 | 提示用户确认是否继续安装 |  
| 🚨 **危险** | 发现可疑行为 | 立即阻止安装（可通过 `--force` 参数覆盖） |  
| ☠️ **恶意软件** | 已确认为恶意软件 | 立即阻止安装（无法覆盖） |  
| ⛔ **被列入黑名单** | 该技能已被列入黑名单 | 禁止安装（无法覆盖） |  

## 配置文件：  
`~/.config/pincer/config.json`  

```json
{
  "trustedPublishers": ["openclaw", "steipete", "invariantlabs-ai"],
  "blockedPublishers": [],
  "blockedSkills": [],
  "autoApprove": "clean",
  "logInstalls": true,
  "minDownloads": 0,
  "minAgeDays": 0
}
```  

| 配置项 | 描述 |  
|-----|-------------|  
| `trustedPublishers` | 允许自动批准的发布者列表 |  
| `blockedPublishers` | 始终禁止的发布者列表 |  
| `blockedSkills` | 始终禁止的技能列表 |  
| `autoApprove` | `"clean"`：自动批准来自可信发布者的安全技能；`"never"`：始终要求用户确认 |  
| `logInstalls` | 将安装记录写入日志文件 |  
| `minDownloads` | 如果技能下载次数低于指定阈值，则发出警告 |  
| `minAgeDays` | 如果技能发布时间超过指定天数，则发出警告 |  

## 使用示例：  
- **安全安装**  
```
$ pincer install bird
🛡️ pincer v1.0.0

  → Fetching bird from ClawHub...
  Publisher: steipete (trusted)
  Stats: 7363 downloads · 27 ★ · created 1 month ago

🛡️ pincer Scanning bird...

  → Running mcp-scan...
  ✅ mcp-scan: passed
  → Checking for suspicious patterns...
  ✅ Pattern check: passed
  → Checking external URLs...
  ✅ URL check: passed
  → Checking for bundled binaries...
  ✅ Binary check: passed

Risk Assessment:
  ✅ CLEAN — No issues detected

  → Auto-approved (clean + trusted config).
  → Installing bird...
  ✅ Installed successfully!
```  
- **阻止危险技能**  
```
$ pincer install sketchy-tool
🛡️ pincer v1.0.0

  → Fetching sketchy-tool from ClawHub...
  Publisher: newaccount (unknown)
  Stats: 12 downloads · 0 ★ · created 2 days ago

🛡️ pincer Scanning sketchy-tool...

  → Running mcp-scan...
  🚨 mcp-scan: high-risk warnings
  → Checking for suspicious patterns...
  🚨 Pattern check: suspicious patterns found
    • curl/wget piped to shell
    • macOS quarantine removal (xattr)
  → Checking external URLs...
  ⚠️ URL check: external URLs found
    • http://sketchy-domain.xyz/install
  → Checking for bundled binaries...
  ✅ Binary check: passed

Risk Assessment:
  🚨 DANGER — Suspicious patterns detected
    • mcp-scan: high-risk patterns detected
    • curl/wget piped to shell
    • macOS quarantine removal (xattr)

  ☠️ Install blocked. Use --force to override (not recommended).
```  

## 致谢：  
- [mcp-scan](https://github.com/invariantlabs-ai/mcp-scan)：提供核心的安全扫描功能（由 Invariant Labs 开发）  
- [1Password Security Research](https://1password.com/blog/from-magic-to-malware-how-openclaws-agent-skills-become-an-attack-surface)：启发该工具的威胁分析报告  
- [Snyk ToxicSkills Report](https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub/)：对生态系统威胁的深入研究  

## 许可证：  
MIT 许可证  

**请务必保持安全。** 🛡️