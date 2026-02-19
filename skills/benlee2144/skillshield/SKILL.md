---
name: skill-guard
version: 4.0.0
description: "SkillShield v4 — 专为 OpenClaw 技能设计的终极安全扫描工具。具备 65 项安全检查功能，支持 SARIF v2.1.0 格式的数据输出，兼容持续集成/持续部署（CI/CD）流程，能够检测恶意活动、阻止来自特定 IP 地址的攻击（C2 IP 块列表），并拥有已知恶意行为者的数据库。该工具还能检测针对 macOS 的攻击行为、防止代理配置被篡改，以及防范大型语言模型（LLM）工具的攻击。仅使用 Python 3 的标准库开发，文件结构简洁（单文件），且完全无依赖关系。"
---
# SkillShield v4.0.0 — 终极版 🛡️

**65项安全检查** | **支持SARIF v2.1.0** | **支持CI/CD集成** | **零依赖**

这是针对OpenClaw/ClawHub技能的最全面的安全扫描工具，能够检测恶意软件、凭证窃取、数据泄露、命令提示注入、攻击签名、代理接管以及针对macOS的特定攻击等多种安全威胁。

## 功能对比

| 功能 | SkillShield v4 | Skillvet v2 |
|---------|:-:|:-:|
| 总安全检查项数 | **65** | 48 |
| 仅支持Python 3标准库 | ✅ | ❌（仅支持bash） |
| 单个文件扫描 | ✅ | ❌（支持多文件扫描） |
| 支持SARIF v2.1.0输出格式 | ✅ | ✅ |
| 支持JSON输出格式 | ✅ | ✅ |
| 提供摘要模式 | ✅ | ✅ |
| 提供详细模式 | ✅ | ✅ |
| 支持提交前钩子（pre-commit hook） | ✅ | ✅ |
| 支持GitHub Actions模板 | ✅ | ✅ |
| 提供HTML仪表盘报告 | ✅ | ❌ |
| 支持Markdown报告 | ✅ | ❌ |
| 支持交互式界面 | ✅ | ❌ |
| 具有隔离系统功能 | ✅ | ❌ |
| 支持基线检测和篡改检测 | ✅ | ❌ |
| 支持生成软件物料清单（SBOM） | ✅ | ❌ |
| 支持差异扫描 | ✅ | ❌ |
| 支持自定义规则引擎 | ✅ | ❌ |
| 支持风险评分（加权评分） | ✅ | ✅ |
| 支持检查特定代码片段（SS-001+） | ✅ | ✅ |
| 提供退出代码（0/1/2） | ✅ | ✅ |
| 支持已知的C2/IOC IP地址黑名单 | ✅ | ✅ |
| 支持识别已知恶意行为者 | ✅ | ✅ |
| 支持检测数据泄露目标地址 | ✅ | ✅ |
| 支持检测用于数据泄露的服务 | ✅ | ✅ |
| 支持检测恶意活动模式 | ✅ | ❌ |
| 支持行为分析 | ✅ | ❌ |
| 支持检测针对macOS的攻击 | ✅ | ✅ |
| 支持检测代理配置篡改 | ✅ | ✅ |
| 支持检测对大语言模型（LLM）工具的利用 | ✅ | ✅ |
| 支持检测字符串逃避技巧 | ✅ | ✅ |
| 支持检测使用punycode的域名 | ✅ | ✅ |
| 支持检测双重编码 | ✅ | ✅ |
| 支持检测密码压缩文件 | ✅ | ✅ |
| 支持网络指纹识别 | ✅ | ❌ |
| 支持信誉评级 | ✅ | ❌ |
| 支持上下文感知的域名检查 | ✅ | ❌ |
| 支持忽略特定文件（.skillshield-ignore） | ✅ | ✅（.skillvetrc） |
| 支持设置最大文件大小 | ✅ | ✅ |
| 支持设置最大扫描深度 | ✅ | ✅ |
| 支持扫描16种文件类型 | ✅ | ✅ |
| 提供统计信息 | ✅ | ✅ |

## 使用方法

### 扫描所有技能

```bash
python3 skills/skill-guard/scripts/skillguard.py scan
```

### 检查单个技能

```bash
python3 skills/skill-guard/scripts/skillguard.py check skills/some-skill
```

### 检查技能目录

```bash
python3 skills/skill-guard/scripts/skillguard.py check /path/to/skills
```

### 输出格式

```bash
# JSON output (for automation)
python3 scripts/skillguard.py check skills/some-skill --json

# SARIF v2.1.0 (for GitHub Code Scanning / VS Code)
python3 scripts/skillguard.py check skills/some-skill --sarif

# Summary mode (one-line per skill)
python3 scripts/skillguard.py scan --summary

# Verbose mode (debug check progress)
python3 scripts/skillguard.py scan --verbose

# HTML dashboard
python3 scripts/skillguard.py scan --html report.html

# Markdown report
python3 scripts/skillguard.py scan --report report.md
```

### CI/CD集成

**使用GitHub Actions上传扫描结果（SARIF格式）:**

```yaml
- name: Run SkillShield
  run: python3 skills/skill-guard/scripts/skillguard.py check skills/ --sarif > results.sarif || true

- name: Upload SARIF
  uses: github/codeql-action/upload-sarif@v3
  with:
    sarif_file: results.sarif
```

**生成GitHub Actions工作流:**

```bash
python3 scripts/skillguard.py ci > .github/workflows/skillshield.yml
```

**提交前钩子（pre-commit hook）:**

```bash
python3 scripts/skillguard.py hook > .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

### 退出代码说明

| 代码 | 含义 |
|------|---------|
| 0 | 无问题 |
| 1 | 仅发现警告 |
| 2 | 发现严重/恶意问题 |

### 常用命令

| 命令 | 描述 |
|---------|-------------|
| `scan [目录]` | 扫描所有技能（默认路径：~/clawd/skills/） |
| `check <路径>` | 扫描单个技能或目录 |
| `watch [目录]` | 生成用于定时提醒的摘要信息 |
| `diff <名称>` | 将当前技能与基线进行比较 |
| `quarantine <名称>` | 将恶意技能移至隔离区 |
| `unquarantine <名称>` | 从隔离区恢复技能 |
| `list-quarantine` | 显示被隔离的技能列表 |
| `sbom <名称>` | 生成软件物料清单（JSON格式） |
| `hook` | 生成Git提交前钩子 |
| `ci` | 生成GitHub Actions工作流 |

### 常用选项

| 选项 | 描述 |
|------|-------------|
| `--json` | 生成机器可读的JSON输出 |
| `--sarif` | 生成SARIF v2.1.0格式的输出 |
| `--summary` | 为每个技能生成简短摘要 |
| `--verbose` | 显示扫描进度 |
| `--report <路径>` | 生成Markdown格式的报告文件 |
| `--html <路径>` | 生成HTML格式的仪表盘报告 |
| `--baseline` | 强制重新生成基线哈希值 |
| `--interactive` | 以交互方式查看扫描结果 |
| `--ci` | 生成GitHub Actions工作流 |
| `--max-file-size N` | 跳过大于N字节的文件 |
| `--max-depth N` | 限制扫描深度 |

### 如何避免误报

**文件级屏蔽:** 在目标技能文件中创建`.skillshield-ignore`文件：

```
Base64 encode/decode operation
HTTP request to unknown domain: my-legit-api.com
```

**代码内屏蔽:** 在文件中添加`# skillshield-ignore`注释：

```python
url = "https://bit.ly/legit-link"  # skillshield-ignore
```

## 安全检查项目（共65项）

### 检查代码片段（SS-001至SS-065）

| 代码片段 | 检查内容 | 严重程度 | 权重 |
|----|-------|----------|--------|
| SS-001 | 出站HTTP请求 | 警告 | 3 |
| SS-002 | 评估/执行代码调用 | 警告 | 5 |
| SS-003 | 动态导入 | 警告 | 5 |
| SS-004 | Base64解码操作 | 警告 | 4 |
| SS-005 | 解码后的内容疑似恶意 | 严重 | 9 |
| SS-006 | 十六进制字符串解码后疑似恶意 | 严重 | 9 |
| SS-007 | 检测到URL缩短工具 | 警告 | 5 |
| SS-008 | 可执行数据URI | 警告 | 5 |
| SS-009 | 硬编码的秘密信息 | 严重 | 10 |
| SS-010 | 禁用SSL验证 | 警告 | 5 |
| SS-011 | 修改路径 | 严重 | 8 |
| SS-012 | 修改库路径 | 严重 | 8 |
| SS-013 | 执行shell命令 | 警告 | 4 |
| SS-014 | 使用`shell=True`的子进程 | 严重 | 7 |
| SS-015 | 访问敏感文件 | 严重 | 8 |
| SS-016 | 反向shell攻击模式 | 严重 | 10 |
| SS-017 | DNS数据泄露 | 严重 | 9 |
| SS-018 | 修改crontab | 严重 | 8 |
| SS-019 | 创建系统服务 | 严重 | 8 |
| SS-020 | 修改shell配置文件 | 严重 | 8 |
| SS-021 | 时间炸弹攻击模式 | 警告 | 6 |
| SS-022 | 解析pickle文件 | 严重 | 9 |
| SS-023 | 命令提示注入 | 严重 | 9 |
| SS-024 | 命令提示注入导致数据泄露 | 严重 | 9 |
| SS-025 | 社交工程短语 | 警告 | 5 |
| SS-026 | SVG中的JavaScript代码 | 严重 | 8 |
| SS-027 | SVG事件处理器 | 警告 | 5 |
| SS-028 | npm生命周期钩子 | 严重 | 8 |
| SS-029 | 用于域名抢注的恶意包 | 警告 | 6 |
| SS-030 | 二进制可执行文件 | 严重 | 9 |
| SS-031 | 创建指向敏感路径的符号链接 | 严重 | 8 |
| SS-032 | 压缩文件 | 警告 | 4 |
| SS-033 | Unicode同形字攻击 | 严重 | 7 |
| SS-034 | ANSI转义字符注入 | 警告 | 5 |
| SS-035 | 在技能目录外写入数据 | 警告 | 5 |
| SS-036 | 结合多种攻击方式（敏感操作+出站请求） | 严重 | 10 |
| SS-037 | 结合多种攻击方式（子进程+敏感操作） | 严重 | 8 |
| SS-038 | 与攻击模式匹配 | 严重 | 10 |
| SS-040 | 分阶段数据泄露行为 | 严重 | 9 |
| SS-041 | 下载文件后执行命令 | 严重 | 9 |
| SS-042 | 收集环境变量并尝试网络攻击 | 严重 | 9 |
| SS-043 | 访问剪贴板内容 | 警告 | 4 |
| SS-044 | 大量环境变量捕获 | 严重 | 9 |
| SS-045 | 权限设置不当（可能导致木马） | 严重 | 8 |
| SS-046 | 已知的C2/IOC IP地址 | 严重 | 10 |
| SS-047 | 已知的数据泄露目标地址 | 严重 | 10 |
| SS-048 | 使用GitHub上传恶意文件 | 严重 | 9 |
| SS-049 | 绕过macOS的权限保护机制 | 严重 | 9 |
| SS-050 | 利用macOS的osascript进行社会工程攻击 | 严重 | 8 |
| SS-051 | 在临时文件夹中存放恶意代码 | 严重 | 9 |
| SS-052 | 盗窃密钥链 | 严重 | 10 |
| SS-053 | 使用密码保护的压缩文件 | 严重 | 7 |
| SS-054 | 使用双重编码绕过安全机制 | 严重 | 7 |
| SS-055 | 使用punycode的域名（DNS攻击） | 严重 | 7 |
| SS-056 | 字符串构造技巧 | 严重 | 7 |
| SS-057 | 进程持续运行并尝试网络攻击 | 严重 | 9 |
| SS-058 | 篡改代理配置 | 严重 | 9 |
| SS-059 | 利用大语言模型工具 | 严重 | 9 |
| SS-060 | 使用虚假的依赖项 | 严重 | 7 |
| SS-061 | 结合网络攻击的多种技巧 | 警告 | 6 |
| SS-062 | 已知的恶意行为者 | 严重 | 10 |
| SS-063 | 使用nohup命令隐藏攻击痕迹 | 严重 | 9 |
| SS-064 | 为下载的文件设置可执行权限 | 严重 | 8 |
| SS-065 | 使用`open -a`命令执行下载的文件 | 严重 | 8 |

### 常见恶意活动模式

- **ClawHavoc**：涉及386个技能的攻击活动，包含C2控制端 |
- **twitter-enhanced**：利用域名抢注技术，隐藏评估/执行代码 |
- **ClickFix**：通过社会工程手段执行剪贴板命令

### 已知的C2/IOC IP地址黑名单

根据[Koi Security](https://www.koi.ai/blog/clawhavoc)、[Bitdefender](https://businessinsights.bitdefender.com/)和[Snyk](https://snyk.io/articles/clawdhub-malicious-campaign/)的报告：

- `91.92.242.30` — AMOS C2服务器 |
- `54.91.154.110` — AMOS C2服务器 |
- `185.215.113.16` — ClawHavoc攻击的中间代理 |
- `45.61.136.47` — AMOS攻击的第二个阶段载荷 |
- `194.169.175.232` — Atomic Stealer的C2服务器 |
- `91.92.248.52` — ClawHavoc攻击的用于数据泄露的服务器 |
- `79.137.207.210` — Bandit Stealer的C2服务器 |
- `45.155.205.172` — 通用macOS攻击的C2服务器 |

### 已知的恶意行为者

- zaycv, Ddoy233, Sakaen736jih, Hightower6eu, aslaep123, davidsmorais, clawdhub1

## 支持扫描的文件类型

`.py`, `.js`, `.ts`, `.tsx`, `.jsx`, `.sh`, `.bash`, `.rs`, `.go`, `.rb`, `.c`, `.cpp`, `.md`, `.json`, `.svg`, `.yml`, `.yaml`, `.toml`, `.txt`, `.cfg`, `.ini`, `.html`, `.css`, `.env*`, `Dockerfile*`, `Makefile`, `pom.xml`, `.gradle`

## 性能表现

- 扫描25个技能仅需**< 1秒** |
- 扫描16个测试用例仅需**< 0.5秒** |
- 仅使用Python 3标准库，且无任何外部依赖 |
- 扫描的文件包含2,800行纯Python代码