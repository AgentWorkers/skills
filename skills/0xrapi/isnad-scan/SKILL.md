---
name: isnad-scan
description: 扫描 AI 代理的技能以检测安全漏洞——能够识别代码注入、提示注入（prompt injection）、凭证窃取（credential exfiltration）、供应链攻击（supply chain attacks）以及 69 种以上的其他威胁模式。适用于在新技能安装时、审核现有技能时、审查不可信的代码时，或在发布软件包之前进行验证。
metadata:
  openclaw:
    emoji: "🛡️"
    requires:
      bins: ["isnad-scan"]
    primaryEnv: null
    install:
      - id: isnad-scan-pip
        kind: pipx
        package: isnad-scan
        bins: ["isnad-scan"]
        label: "Install isnad-scan (pipx)"
---
# isnad-scan — 用于 AI Agent 技能的安全扫描工具

在安装或运行任何技能、包或目录之前，使用 isnad-scan 对其进行安全威胁检测。

## 快速扫描

```bash
isnad-scan <path>
```

扫描指定目录，并按严重程度（CRITICAL、HIGH、MEDIUM、LOW）报告检测结果。

## 选项

```bash
isnad-scan <path> --cve          # Also check dependencies for known CVEs (via OSV.dev)
isnad-scan <path> -v             # Verbose output (show matched lines)
isnad-scan <path> --json         # Machine-readable JSON output
isnad-scan <path> --cve -v       # Full audit: CVEs + verbose findings
```

## 支持检测的安全威胁类型（69 种以上）：

- **代码注入**：shell 执行、eval、exec、subprocess、os.system、动态导入
- **提示注入**：尝试篡改用户角色、劫持指令执行流程
- **凭证泄露**：收集环境变量、访问密钥链、窃取令牌、读取敏感文件路径
- **网络威胁**：反向 shell 连接、DNS 数据泄露、未经授权的出站连接、Webhook 数据泄露
- **文件系统攻击**：路径遍历、符号链接攻击、读取 /etc/passwd 文件、访问 SSH 密钥
- **供应链攻击**：检测域名抢注行为、分析压缩后的 JavaScript 代码、扫描二进制文件、查找隐藏文件
- **加密风险**：使用弱加密算法、硬编码密钥、提取钱包种子信息

## 使用场景：

1. **安装新技能前**：先扫描该技能的目录
2. **定期审计现有技能**：进行安全审查
3. **审查 Pull Request（PR）/贡献代码**：及时发现恶意代码
4. **发布前验证**：确保自己的技能没有安全问题再分享
5. **集成到持续集成/持续交付（CI/CD）流程**：使用 `isnad-scan --json` 进行自动化检查

## 结果解读

```
🔴 CRITICAL  — Immediate threat. Do not install/run.
🟠 HIGH      — Likely malicious or dangerous. Review carefully.
🟡 MEDIUM    — Suspicious pattern. May be legitimate, verify intent.
🔵 LOW       — Informational. Common in legitimate code but worth noting.
```

## 使用示例：

- 在安装 ClawHub 技能之前先进行扫描：
  ```bash
isnad-scan ./skills/some-new-skill/
```

- 进行全面审计并检查安全漏洞（CVE）：
  ```bash
isnad-scan ./skills/some-new-skill/ --cve -v
```

- 适用于自动化的 JSON 输出格式：
  ```bash
isnad-scan . --json | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'{d[\"summary\"][\"critical\"]} critical, {d[\"summary\"][\"high\"]} high')"
```

## Python API

```python
from isnad_scan import scan_directory

results = scan_directory("/path/to/skill")
for finding in results.findings:
    print(f"[{finding.severity}] {finding.category}: {finding.description}")
    print(f"  File: {finding.file}:{finding.line}")
```

## 关于 ISNAD

ISNAD（إسناد）意为“传输链”，是一种用于验证传输内容真实性的方法。isnad-scan 是 [ISNAD 协议](https://isnad.md) 的安全防护层，为 AI Agent 技能生态系统提供了信任验证机制。

**PyPI：** `pip install isnad-scan`
**GitHub：** [counterspec/isnad](https://github.com/counterspec/isnad)
**协议文档：** [isnad.md](https://isnad.md)