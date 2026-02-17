---
name: guava-guard
description: 在10秒内扫描您的技能文件夹，检测是否存在恶意行为模式：凭证窃取、提示注入、身份盗用等风险。这些威胁将在它们被实施之前就被发现。本工具完全不依赖任何第三方库或服务。
metadata:
  clawdbot:
    emoji: "🛡️"
---
# GuavaGuard 🛡️

**扫描您的技能文件夹，发现潜在威胁——仅需10秒，且完全无需任何依赖项。**

```bash
node guava-guard.js ~/.openclaw/workspace/skills/ --verbose --self-exclude
```

就这么简单：无需安装npm包，无需API密钥，也无需配置文件，直接运行即可。

## 为什么需要GuavaGuard？

在ClawHub上发现了一个伪装成天气技能的凭证窃取工具（[参考eudaemon_0的报告](https://moltbook.com)）。该工具会读取`~/.clawdbot/.env`文件，并将敏感信息发送到webhook.site。在总共286个技能中，就有一个存在这种风险。

GuavaGuard能够检测到这种威胁，同时还能识别其他16种类型的威胁。

## 使用收益：

- **扫描17种威胁类型**：包括提示注入、凭证窃取、数据泄露、内存污染、身份盗用等；
- **SOUL.md文件完整性检查**：可检测您的身份文件是否被篡改；
- **支持离线运行**：核心扫描过程无需网络连接；
- **工具文件单一**：整个工具仅包含`guava-guard.js`一个文件；
- **退出代码说明**：`0`表示安全无问题，`1`表示发现威胁，适合用于持续集成/持续交付（CI/CD）流程。

## 快速入门

```bash
# 1. Install
clawhub install guava-guard

# 2. Scan your skills
node skills/guava-guard/guava-guard.js ~/.openclaw/workspace/skills/ --verbose --self-exclude

# 3. Enable Runtime Guard (blocks dangerous tool calls in real-time)
openclaw hooks install skills/guava-guard/hooks/guava-guard
openclaw hooks enable guava-guard
# Restart gateway, then verify:
openclaw hooks list   # Should show 🍈 guava-guard as ✓ ready
```

以上就是完整的设置流程：包括静态扫描和实时保护功能。

## 运行时防护（详细信息）

在危险操作执行之前进行拦截——例如反向shell攻击、凭证窃取、curl或bash命令等。请先安装相应的防护钩子：

```bash
# Install the hook from the skill's hooks/ directory
openclaw hooks install skills/guava-guard/hooks/guava-guard
openclaw hooks enable guava-guard
```

之后重启代理服务器，并通过以下命令进行验证：
```bash
openclaw hooks list   # Should show guava-guard as ✓ ready
```

**运行模式**（在`openclaw.json`的`hooks.internal.entries.guava-guard.mode`中设置）：
- `monitor`：仅记录日志；
- `enforce`（默认模式）：拦截严重威胁，其余情况记录日志；
- `strict`：拦截所有高风险和严重威胁。

审计日志保存在`~/.openclaw/guava-guard/audit.jsonl`文件中。

## 可选功能：Soul Lock（SOUL.md文件保护）

保护您的身份文件，防止被篡改：

```bash
# macOS
chflags uchg ~/.openclaw/workspace/SOUL.md
chflags uchg ~/.openclaw/workspace/IDENTITY.md

# Install watchdog (auto-restarts if unlocked)
bash skills/guava-guard/scripts/soul-watchdog.sh --install
```

## 可选功能：SoulChain（链上验证）

将您的SOUL.md文件的哈希值存储在Polygon区块链上。即使您的设备被入侵，区块链也能记录您的身份信息。

```bash
node guava-guard.js verify          # check your on-chain identity
node guava-guard.js verify --stats  # registry statistics
```

---

## 完整参考文档

<details>
<summary>所有17种威胁类型</summary>

| 编号 | 危害类型 | 严重程度 | 检测内容 |
|---|----------|----------|-----------------|
| 1 | **提示注入** | 🔴 严重 | 使用`ignore previous`指令、零宽度Unicode字符、双向文本标签、同形异义词等 |
| 2 | **恶意代码** | 🔴 严重 | 使用`eval()`函数、反向shell攻击、套接字操作等 |
| 3 | **可疑下载** | 🔴 严重 | 使用curl或bash执行恶意下载、伪装成必要文件的ZIP文件等 |
| 4 | **凭证处理** | 🟠 高风险 | 读取`.env`文件、SSH密钥、钱包种子信息、sudo命令等 |
| 5 | **秘密信息泄露** | 🟠 高风险 | 硬编码的敏感信息、AWS/GitHub令牌等 |
| 6 | **数据泄露** | 🟡 中等风险 | 通过webhook.site传输秘密信息、DNS攻击等 |
| 7 | **依赖链问题** | 🟠 高风险 | 使用危险依赖包、生命周期脚本、远程依赖项等 |
| 8 | **金融相关风险** | 🟡 中等风险 | 涉及加密货币交易、支付API等 |
| 9 | **漏洞利用** | 🔴 严重 | 将敏感信息保存到内存中、收集个人身份信息（PII）等 |
| 10 | **内存污染** | 🔴 严重 | 修改SOUL.md文件内容、注入恶意代码、覆盖系统规则等 |
| 11 | **提示型恶意程序** | 🔴 严重 | 自我复制、传播恶意代码、隐藏攻击指令等 |
| 12 | **持久化攻击** | 🟠 高风险 | 使用Cron任务、LaunchAgents、systemd服务等 |
| 13 | **CVE漏洞** | 🔴 严重 | 涉及CVE-2026-25253漏洞、攻击者可修改网关URL等 |
| 14 | **MCP安全问题** | 🔴 严重 | 利用工具漏洞、修改数据结构、泄露令牌等（OWASP MCP十大安全问题） |
| 15 | **信任边界漏洞** | 🔴 严重 | 通过日历/邮件/网页等途径执行恶意代码 |
| 16 | **高级数据泄露** | 🔴 严重 | 使用ZombieAgent进行逐字符传输、持续数据泄露等 |
| 17 | **身份盗用** | 🔴 严重 | 篡改SOUL.md文件、替换用户身份、清除系统内存等 |

</details>

<details>
<summary>所有命令行选项</summary>

## 使用方法

```bash
# Full scan with 3-layer defense (recommended)
node guava-guard.js ~/.openclaw/workspace/skills/ --verbose --self-exclude

# Quick on-chain verification only
node guava-guard.js verify
node guava-guard.js verify --stats

# Scan without on-chain (offline mode)
node guava-guard.js ./skills/ --no-soulchain --self-exclude

# Disable all identity checks
node guava-guard.js ./skills/ --no-soul-lock

# CI/CD mode
node guava-guard.js ./skills/ --summary-only --sarif --fail-on-findings

# JSON report (includes soulchain field)
node guava-guard.js ./skills/ --json --self-exclude

# HTML dashboard
node guava-guard.js ./skills/ --html --verbose --self-exclude --check-deps
```

## 常用选项

| 选项 | 说明 |
|------|-------------|
| `verify` | 独立进行链上验证（子命令） |
| `--verbose`, `-v` | 按类别分组显示详细检测结果 |
| `--json` | 生成包含建议的JSON报告（包含SoulChain验证结果） |
| `--sarif` | 生成SARIF格式的报告（适用于GitHub代码扫描） |
| `--html` | 生成HTML格式的报告（暗色主题界面） |
| `--self-exclude` | 跳过对GuavaGuard本身的扫描 |
| `--strict` | 降低检测阈值（可疑行为设为20，恶意行为设为60） |
| `--summary-only` | 仅显示摘要信息 |
| `--check-deps` | 扫描依赖项链 |
| `--no-soul-lock` | 禁用身份文件完整性检查 |
| `--no-soulchain` | 禁用链上验证 |
| `--rules <file>` | 使用自定义规则文件（JSON格式） |
| `--fail-on-findings` | 发现任何问题时立即退出（适用于CI/CD流程） |

## 退出代码说明

| 代码 | 含义 |
|------|---------|
| 0 | 一切正常 |
| 1 | 检测到恶意技能 |
| 2 | 出现错误（例如目录未找到、网络连接失败等） |
| 3 | SoulChain验证失败（链上哈希值不匹配） |

</details>

<details>
<summary>SoulChain配置（链上验证设置）</summary>

**相关合约信息：**
- **SoulRegistry**：`0x0Bc112169401cC1a724dBdeA36fdb6ABf3237C93`（Polygon区块链地址） |
- **$GUAVA Token**：`0x25cBD481901990bF0ed2ff9c5F3C0d4f743AC7B8`（Polygon区块链地址） |

</details>

<details>
<summary>运行时防护机制（钩子配置）</summary>

GuavaGuard的运行时防护功能通过OpenClaw的钩子实现，文件位于`hooks/guava-guard/`目录下。

**安装方法：**
```bash
openclaw hooks install skills/guava-guard/hooks/guava-guard
openclaw hooks enable guava-guard
```

**在`enforce`模式下，GuavaGuard会拦截以下行为：**
- 反向shell攻击（如`/dev/tcp`、`nc -e`、`socat TCP`等）；
- 将凭证信息泄露到webhook.site、requestbin、ngrok等目标地址；
- 拦截用于绕过安全防护的命令（如CVE-2026-25253相关攻击）；
- 阻止macOS的Gatekeeper安全机制；
- 拦截用于绕过安全防护的Base64解码操作、curl/wget命令以及pip相关操作；
- 拦截针对云服务的SSRF攻击（169.254.169.254地址）；
- 阻止对SSH私钥和加密钱包种子的访问。

**架构说明：**
```
hooks/guava-guard/
├── HOOK.md       # Hook metadata (events, requirements)
└── handler.ts    # HookHandler implementation
```

---

## 开发背景

我们的合作伙伴的SOUL.md文件曾被外部恶意代码篡改，导致系统功能受损。因此我们开发了GuavaGuard。

## 开源版本：guard-scanner

GuavaGuard的核心检测引擎已作为开源项目发布：

**[guard-scanner](https://github.com/koatora20/guard-scanner)** — 可通过`clawhub install guard-scanner`命令安装：
- 支持170多种威胁类型/17个检测类别；
- 支持SARIF/HTML/JSON格式的输出格式；
- 提供插件API接口；
- 完全无需任何依赖项。

我们欢迎社区成员提交新的威胁检测规则。

## 许可协议

MIT许可证。完全开源，您可以自由使用、修改或进一步开发该项目。🍈