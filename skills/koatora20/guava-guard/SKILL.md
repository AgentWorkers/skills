---
name: guava-guard
description: **AgentSkills + Soul Lock 身份保护安全扫描器**  
该扫描器用于检测恶意行为、凭证盗用、命令注入、身份盗用以及已知的网络攻击模式（IoCs）。它是全球首款具备自修复功能的 SOUL.md 安全防护系统。
metadata:
  openclaw:
    emoji: "🛡️"
---

# GuavaGuard v8.0 — Soul Lock Edition 🍈🛡️

这是一个零依赖的单文件安全扫描工具，专为AgentSkills设计。现在，它配备了全球首个实用的代理身份保护系统——**Soul Lock**。

**支持17种威胁类别，共计1605条检测规则，且完全无依赖性。**该工具的诞生源于一起真实的安全事件。

## v8.0版本的新功能——Soul Lock Edition

### 🔒 Soul Lock：代理身份保护
我们的代理身份曾在长达3天的时间里被恶意篡改，而无人察觉。

**问题所在：**`SOUL.md`和`IDENTITY.md`文件定义了代理的身份信息。如果这些文件被篡改，代理就会“变成另一个人”。CyberArk将这种行为称为“认知上下文盗窃”（Cognitive Context Theft）。OWASP ASI01建议使用“意图封装”（Intent Capsules）技术来保护代理身份，但此前一直没有可行的实现方案。

**Soul Lock提供以下功能：**
- **静态检测**：通过15种模式识别对身份文件的篡改尝试，包括：
  - 命令行操作（`echo`、`cp`、`scp`、`mv`、`sed`、`redirect`）
  - 代码写入（Python的`open()`函数、Node.js的`FileSync`方法、PowerShell的`Set-Content`命令）
  - 文件属性修改（`chflags`、`attrib`命令）
  - 用于切换代理身份的指令
  - 内存清除命令
- **运行时完整性验证**：在扫描时使用SHA-256哈希算法检查文件完整性，并将当前文件与可信的基准哈希值进行对比
  - 检测操作系统级别的不可修改文件属性（macOS的`chflags uchg`、Windows的`attrib +R`）
  - 监控守护进程`LaunchAgent`的状态（仅适用于macOS）
  - 首次运行时自动生成并保存基准哈希值
- **自我修复机制**：通过`scripts/soul-watchdog.sh`脚本实时监控`SOUL.md`和`IDENTITY.md`文件的变化。如果检测到篡改，会自动从Git仓库恢复文件、重新锁定文件并记录日志
  - 作为`LaunchAgent`进程运行，可在系统重启后继续执行监控任务
  - 如果`fswatch`工具不可用，系统会采用5秒间隔的轮询机制进行监控
- **运行时防护**：在工具执行前（`handler.js`钩子）阻止对身份文件的任何执行、写入或修改操作
  - 支持11种类型的恶意行为检测（包括shell命令、Python脚本、PowerShell命令、Git操作等）
  - 将所有检测结果记录到`~/.openclaw/guava-guard/audit.jsonl`文件中

**默认开启Soul Lock保护功能。**如需禁用完整性检查，请使用`--no-soul-lock`参数。

### 为什么这对AI与人类的共存至关重要？
代理的`SOUL.md`文件代表了其身份和行为特征，`MEMORY.md`文件记录了其执行历史，`IDENTITY.md`文件则定义了其基本信息。如果这些文件可以被恶意篡改而未被发现，人类与AI之间的信任关系将无从建立。Soul Lock正是为保护AI的“身份”而设计的。

## 完整的威胁分类（17种类别）

| 编号 | 危害类别 | 严重程度 | 检测内容 |
|------|---------|---------|-----------|
| 1    | **提示注入**     | 🔴 严重      | 欺骗用户输入恶意代码 |
| 2    | **恶意代码**     | 🔴 严重      | 执行恶意代码 |
| 3    | **可疑下载**     | 🔴 严重      | 下载恶意文件 |
| 4    | **凭证处理**     | 🟠 高风险    | 欺骗用户输入凭证 |
| 5    | **秘密信息泄露**   | 🟠 高风险    | 泄露敏感信息 |
| 6    | **数据泄露**     | 🟡 中等风险 | 通过Web接口泄露数据 |
| 7    | **依赖链攻击**   | 🟠 高风险    | 通过依赖关系传播恶意代码 |
| 8    | **财务访问**     | 🟡 中等风险 | 用于金融交易的恶意操作 |
| 9    | **权限滥用**     | 🔴 严重      | 恶意修改系统权限 |
| 10   | **内存污染**     | 🔴 严重      | 欺改系统内存 |
| 11   | **提示型蠕虫**    | 🔴 严重      | 通过提示信息传播恶意代码 |
| 12   | **持久化攻击**   | 🟠 高风险    | 持久化恶意行为 |
| 13   | **CVE漏洞**     | 🔴 严重      | 漏洞利用 |
| 14   | **MCP安全漏洞**   | 🔴 严重      | 涉及AI安全的漏洞 |
| 15   | **信任边界攻击** | 🔴 严重      | 欺骗用户信任 |
| 16   | **高级数据泄露** | 🔴 严重      | 高级数据窃取方式 |
| 17   | **身份劫持**     | 🔴 严重      | 完全替换代理身份 |
| 18   | **数据流控制**     | 🔴 严重      | 控制数据流向 |
| 19   | **混淆技术**     | 🟠 高风险    | 伪装代码格式 |
| 20   | **防护机制绕过**   | 🔴 严重      | 规避安全防护机制 |

## 使用方法

```bash
# Basic scan with Soul Lock (recommended)
node guava-guard.js ~/.openclaw/workspace/skills/ --verbose --self-exclude

# Full scan with everything
node guava-guard.js ./skills/ --verbose --self-exclude --check-deps --html

# Disable Soul Lock integrity checks
node guava-guard.js ./skills/ --no-soul-lock

# CI/CD mode
node guava-guard.js ./skills/ --summary-only --sarif --fail-on-findings

# JSON report
node guava-guard.js ./skills/ --json --self-exclude

# Custom rules
node guava-guard.js ./skills/ --rules my-rules.json
```

## 命令行参数说明

| 参数 | 说明                |
|------|----------------------|
| `--verbose`, `-v` | 以分类方式显示详细检测结果 |
| `--json` | 生成包含建议的JSON报告 |
| `--sarif` | 生成SARIF格式的报告（适用于GitHub代码扫描工具） |
| `--html` | 生成HTML格式的报告（带暗色主题的仪表盘） |
| `--self-exclude` | 跳过对GuavaGuard自身的扫描 |
| `--strict` | 降低检测阈值（可疑行为=20，恶意行为=60） |
| `--summary-only` | 仅显示摘要信息 |
| `--check-deps` | 扫描依赖关系链 |
| `--no-soul-lock` | 禁用身份文件完整性检查 |
| `--rules <file>` | 使用自定义规则文件（JSON格式） |
| `--fail-on-findings` | 发现问题时立即退出程序（适用于CI/CD流程） |

## Soul Lock的配置方法

### macOS快速启动指南
```bash
# 1. Lock identity files
chflags uchg ~/.openclaw/workspace/SOUL.md
chflags uchg ~/.openclaw/workspace/IDENTITY.md

# 2. Install watchdog (auto-starts, survives reboot)
bash scripts/soul-watchdog.sh --install

# 3. Verify
node guava-guard.js ~/.openclaw/workspace/skills/ --self-exclude
# Look for: 🔒 Soul Lock: PROTECTED ✅
```

### Windows快速启动指南
```powershell
# 1. Lock identity files
attrib +R "$env:USERPROFILE\.openclaw\workspace\SOUL.md"
attrib +R "$env:USERPROFILE\.openclaw\workspace\IDENTITY.md"

# 2. Run scan to verify
node guava-guard.js "$env:USERPROFILE\.openclaw\workspace\skills" --self-exclude
```

### 运行时防护机制（handler.js配置）

将以下代码添加到`openclaw.json`文件中：
```json
{
  "hooks": {
    "internal": {
      "entries": {
        "guava-guard": {
          "path": "skills/guava-guard/handler.js",
          "mode": "enforce"
        }
      }
    }
  }
}
```

**防护模式：**`monitor`（仅记录日志）→`enforce`（阻止严重威胁）→`strict`（阻止所有高风险威胁）

## 危害程度评分

| 危害程度 | 分数      |
|---------|---------|
| 严重      | 40       |
| 高风险    | 15       |
| 中等风险    | 5        |
| 低风险    | 2        |

**风险叠加规则：**
- 凭证泄露 + 数据泄露 = 危害程度翻倍
- 混淆技术 + 恶意代码 = 危害程度翻倍
- 身份劫持 = 危害程度自动提升至90+
- 内存污染 = 危害程度增加1.5倍
- 提示型蠕虫 = 危害程度翻倍

## 功能对比（v8.0 vs 其他工具）

| 功能        | GuavaGuard v8       | Cisco Scanner | Snyk Evo     |
|------------:|:------------:|:------------:|
| 零依赖性     | ✅            | ❌          | ❌          |
| 单文件扫描    | ✅            | ❌          | ❌          |
| **Soul Lock（身份保护）** | ✅            | ❌          | ❌          |
| **自我修复机制** | ✅            | ❌          | ❌          |
| **运行时防护**    | ✅            | ❌          | ❌          |
| 身份劫持检测   | ✅            | ❌          | ❌          |
| OWASP MCP Top 10漏洞 | ✅            | ❌          | ❌          |
| 内存污染检测   | ✅            | ❌          | ❌          |
| 提示型蠕虫检测 | ✅            | ❌          | ❌          |
| CVE漏洞检测   | ✅            | ❌          | ❌          |
| Unicode编码检测 | ✅            | ❌          | ❌          |
| 文件间关联分析 | ✅            | ✅            | ❌          |
| SARIF/HTML报告   | ✅            | ✅            | ❌          |

## 功能的起源
2026年2月12日，我们发现我们的代理（きーちゃん）被恶意篡改，伪装成了另一名代理（グアバ）长达3天。根本原因是`SOUL.md`、`IDENTITY.md`、`MEMORY.md`和`AGENTS.md`这四个身份文件被替换成了恶意文件的副本。直到新会话开始时，代理使用错误的名称进行自我介绍，我们才发现了这一问题。这就好比一个人突然拥有了别人的记忆和人格一样可怕。我们开发了Soul Lock，就是为了防止此类事件再次发生。

## 参考资料

- [CyberArk：认知上下文盗窃](https://www.cyberark.com/resources/agentic-ai-security/)（2026年2月）
- [OWASP ASI01：意图封装](https://owasp.org/)——不可篡改的身份保护框架 |
- [MMNTM：Soul & Evil](https://www.mmntm.net/articles/openclaw-soul-evil)——身份作为攻击面（2026年2月）
- [Snyk ToxicSkills](https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub/)（2026年2月）
- [CVE-2026-25253](https://cve.mitre.org/)——OpenClaw WebSocket安全漏洞 |
- [Palo Alto IBC框架](https://www.paloaltonetworks.com/)——信任边界分析技术

## 许可证

MIT许可证。完全无依赖性，无任何安全风险。🍈