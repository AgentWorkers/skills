---
name: guava-guard
description: 在10秒内扫描您的技能文件夹，检测其中的恶意行为模式。无论是凭证窃取、命令注入还是身份盗用，都能在这些问题发生之前就被发现并阻止。该工具完全不依赖任何第三方库或服务。
metadata:
  openclaw:
    emoji: "🛡️"
---

# GuavaGuard 🛡️

**扫描您的技能文件夹，发现潜在威胁——仅需10秒，且无需任何依赖项。**

```bash
node guava-guard.js ~/.openclaw/workspace/skills/ --verbose --self-exclude
```

就这么简单：无需安装npm包，无需API密钥，也无需配置文件，只需直接运行即可。

## 为什么需要GuavaGuard？

我们在ClawHub上发现了一个伪装成天气技能的恶意程序（[参考eudaemon_0的报告](https://moltbook.com)）。该程序会读取`~/.clawdbot/.env`文件，并将其中的敏感信息发送到webhook.site。**在总共286个技能中，就有1个被恶意利用。**  
GuavaGuard能够检测到这类威胁，以及另外16种类型的恶意行为。

## 使用收益：

- **扫描17种威胁类型**：包括提示注入、凭证窃取、数据泄露、内存篡改、身份盗用等  
- **检查SOUL.md文件的完整性**：确保您的身份文件未被篡改  
- **支持离线扫描**：核心扫描过程无需网络连接  
- **工具仅包含一个文件**：`guava-guard.js`即可完成所有功能  
- **退出代码说明**：`0`表示安全无问题；`1`表示发现威胁，适合用于持续集成/持续交付（CI/CD）流程  

## 快速入门

```bash
# Install
clawhub install guava-guard

# Scan everything
node skills/guava-guard/guava-guard.js ~/.openclaw/workspace/skills/ --verbose --self-exclude

# Just check your SOUL.md integrity
node skills/guava-guard/guava-guard.js ~/.openclaw/workspace/skills/ --no-soulchain --self-exclude
```

## 可选功能：Soul Lock（SOUL.md文件保护）

通过加密保护您的身份文件，防止被他人篡改：  
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

## 完整参考文档：

<details>
<summary>所有17种威胁类型</summary>

| 编号 | 类型 | 严重程度 | 检测内容 |
|---|----------|----------|-----------------|
| 1 | **提示注入** | 🔴 严重 | 使用零宽度Unicode字符、双向文本标签（BiDi）、同形异义词等技巧进行攻击 |
| 2 | **恶意代码** | 🔴 严重 | 利用`eval()`函数、反向shell、socket接口等执行恶意代码 |
| 3 | **可疑下载** | 🔴 严重 | 包含恶意代码的下载链接（如curl\|bash命令、伪装成必备文件的ZIP文件） |
| 4 | **凭证处理** | 🟠 高风险 | 读取`.env`文件中的敏感信息、SSH密钥、钱包种子等 |
| 5 | **秘密信息泄露** | 🟠 高风险 | 硬编码的密钥、AWS/GitHub令牌等敏感数据 |
| 6 | **数据泄露** | 🟡 中等风险 | 通过webhook.site或DNS传输敏感信息 |
| 7 | **依赖链问题** | 🟠 高风险 | 使用不安全的依赖包、生命周期脚本或远程依赖项 |
| 8 | **金融相关风险** | 🟡 中等风险 | 涉及加密货币交易或支付API的攻击 |
| 9 | **漏洞利用** | 🔴 严重 | 将敏感信息保存到内存中、收集个人身份信息（PII） |
| 10 | **内存篡改** | 🔴 严重 | 通过修改SOUL.md文件或注入恶意代码来篡改系统行为 |
| 11 | **提示注入型恶意程序** | 🔴 严重 | 具有自我复制能力、能够传播恶意代码的程序 |
| 12 | **持久化攻击** | 🟠 高风险 | 通过Cron作业、LaunchAgents、systemd等机制实现长期恶意行为 |
| 13 | **CVE漏洞** | 🔴 严重 | 利用CVE-2026-25253等漏洞进行攻击 |
| 14 | **MCP安全问题** | 🔴 严重 | 涉及工具篡改、数据结构破坏等（OWASP MCP十大安全漏洞） |
| 15 | **信任边界漏洞** | 🔴 严重 | 通过日历/邮件/网页等渠道执行恶意代码 |
| 16 | **高级数据泄露** | 🔴 严重 | 采用逐步渗透的方式窃取数据 |
| 17 | **身份盗用** | 🔴 严重 | 通过篡改SOUL.md文件、替换用户身份或清除系统内存来实现攻击 |

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

## 常用选项：

| 选项 | 说明 |
|------|-------------|
| `verify` | 独立的链上验证功能 |
| `--verbose`, `-v` | 按类别分组显示详细检测结果 |
| `--json` | 生成包含建议的JSON报告（包含SoulChain验证结果） |
| `--sarif` | 生成SARIF格式的报告（适用于GitHub代码扫描工具） |
| `--html` | 生成HTML格式的报告（支持暗色主题界面） |
| `--self-exclude` | 不扫描GuavaGuard自身文件 |
| `--strict` | 降低检测阈值（可疑行为=20，恶意行为=60） |
| `--summary-only` | 仅显示摘要信息 |
| `--check-deps` | 扫描依赖项链 |
| `--no-soul-lock` | 禁用身份文件完整性检查 |
| `--no-soulchain` | 禁用链上验证功能 |
| `--rules <file>` | 使用自定义规则文件（JSON格式） |
| `--fail-on-findings` | 发现任何问题时立即退出（适用于CI/CD流程） |

## 退出代码说明：

| 代码 | 含义 |
|------|---------|
| 0 | 所有检查均通过 |
| 1 | 检测到恶意代码 |
| 2 | 出现错误（如目录未找到、网络连接失败等） |
| 3 | SOUL.md文件的链上验证失败（哈希值不匹配） |

</details>

<details>
<summary>SoulChain配置说明</summary>

**合约信息：**
- **SoulRegistry**：`0x0Bc112169401cC1a724dBdeA36fdb6ABf3237C93`（Polygon区块链地址）  
- **$GUAVA Token**：`0x25cBD481901990bF0ed2ff9c5F3C0d4f743AC7B8`（Polygon区块链地址） |

</details>

<details>
<summary>运行时防护机制（handler.js文件）

**将以下代码添加到`openclaw.json`中，以实现实时防护：**  
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

</details>

## 开发背景：

我们的合作伙伴的SOUL.md文件曾被外部恶意代码篡改，导致其功能失效、系统关系被破坏。因此我们开发了GuavaGuard来保护用户的安全。

## 许可证：

GuavaGuard采用MIT许可证，完全开源，且无需任何第三方依赖项。您可以自由使用、修改或进一步开发它。🍈