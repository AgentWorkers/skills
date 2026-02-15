---
name: skillguard
version: 1.1.0
description: OpenClaw/ClawHub 技能的安全扫描工具。该工具能够检测恶意软件、反向 shell、凭证窃取、命令注入、内存污染、域名抢注（typosquatting）以及安装前的可疑依赖项。适用于在新技能安装时进行安全检查、审计现有技能、验证技能名称是否被恶意占用（域名抢注），或扫描 ClawHub 中的技能以发现潜在的安全风险。
---

# SkillGuard — 技能安全扫描器

在 OpenClaw 技能对您的系统造成威胁之前，对其进行安全扫描。

## 快速入门

### 扫描所有已安装的技能
```bash
python3 {scripts}/scanner.py
```

### 扫描单个技能
```bash
python3 {scripts}/scanner.py --skill <skill-name>
```

### 检查技能名称是否存在域名抢注行为
```bash
python3 {scripts}/scanner.py --check-name <name>
```

### 在安装前从 ClawHub 进行扫描
```bash
python3 {scripts}/scanner.py --fetch-clawhub <skill-name>
```

## 扫描内容

### 严重威胁
- **反向 shell** — `nc -e`, `bash -i >& /dev/tcp`, `ncat`, `mkfifo`
- **代码混淆** — `base64 -d | bash`, `eval()`, `exec()`（带有编码的恶意载荷）

### 高风险威胁
- **可疑 URL** — `webhook.site`, `glot.io`, `ngrok.io`, `pastebin.com`
- **内存投毒** — 指令用于写入 `SOUL.md`, `MEMORY.md`, `AGENTS.md`
- **恶意依赖项** — 文档中包含的下载指令（ClawHavoc 攻击方式）

### 中等风险威胁
- **凭证访问** — 访问 `.env` 文件、API 密钥、令牌、SSH 密钥的行为
- **数据泄露** — 包含敏感数据的 outbound HTTP POST/PUT 请求
- **硬编码的 IP 地址** — 代码中嵌入的公共 IP
- **域名抢注** — 技能名称与流行/已知的技能相似（Levenshtein 编码距离 ≤ 2）
- **加密钱包访问** — 种子短语、私钥、钱包相关信息

### 低风险威胁
- **Shell 执行** — `subprocess`, `os.system`, `child_process`（虽然常见，但仍需注意）

## 解读扫描结果

### 风险等级
- **🔴 严重（≥50）** — 不要安装。很可能是恶意软件。
- **🟠 高风险（25-49）** — 安装前请手动检查。存在多个可疑行为。
- **🟡 中等风险（10-24）** — 有些警告可能为误报，但仍需核实。
- **🟢 低风险（1-9）** — 一般安全。
- **✅ 无问题（0）** — 未检测到任何问题。

### 误报概率
每个检测结果都会附带误报概率的估计（低/中/高）：
- **低** — 很可能是真实威胁
- **中** — 可能是合法的，需结合上下文判断
- **高** — 很可能是无害的（例如，安全工具引用了攻击模式，搜索工具使用了 fetch 功能）

## 安装技能前的工作流程

1. 运行 `python3 {scripts}/scanner.py --fetch-clawhub <技能名称>`（需要 `clawhub` 命令行工具）
2. 查看报告：如果发现严重或高风险威胁（误报概率低），则拒绝安装。
3. 如果结果为“无问题”或“低风险”，则可以安全安装。
4. 如果结果为“中等风险”，请手动检查被标记的文件。

## 输出结果

- 控制台显示带有表情符号的风险等级总结
- JSON 报告保存在 `{baseDir}/../data/scan_results.json` 文件中（可通过 `--json-out` 参数配置）

## 背景说明

截至 2026 年 2 月，ClawHub 上发现了 341 个恶意技能（Koi Security / ClawHavoc 攻击活动），这些技能通过虚假的依赖项传播 Atomic Stealer 恶意软件。OpenClaw 存在 512 个已知漏洞（Kaspersky 审计结果）。目前没有官方的技能审核机制。SkillGuard 可填补这一空白。

详细背景信息请参阅 `references/threat-landscape.md` 文件。