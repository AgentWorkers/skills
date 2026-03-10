---
name: guard-scanner
description: "这是一个用于AI代理技能的安全扫描器和运行时防护工具。它支持32个类别中的352种静态威胁模式，并提供26种运行时检查机制（共5层防御机制）。该工具可用于扫描技能目录以检测安全威胁、审计npm/GitHub/ClawHub仓库中的敏感信息泄露情况、在开发过程中实时监控文件变化、将安全检查集成到CI/CD流程中（支持SARIF/JSON格式），以及通过`before_tool_call`钩子对工具调用进行实时防护。该工具仅依赖一个外部库（`ws`），采用MIT许可证授权。"
license: MIT
metadata: {"openclaw": {"requires": {"bins": ["node"]}}}
---
# guard-scanner

该工具可扫描AI代理的技能，以检测32类威胁，包括提示注入（Prompt Injection）、身份盗用（Identity Hijacking）、内存注入（Memory Poisoning）、MCP工具攻击（MCP Tool Poisoning）、供应链攻击（Supply Chain Attacks）以及传统安全工具未能发现的27种其他威胁类型。

## 快速入门

```bash
# Scan a skill directory
npx -y @guava-parity/guard-scanner ./my-skills/ --verbose

# Scan with identity protection
npx -y @guava-parity/guard-scanner ./skills/ --soul-lock --strict
```

## 核心命令

### 扫描（Scan）

```bash
guard-scanner scan <dir>        # Scan directory
guard-scanner scan <dir> -v     # Verbose output
guard-scanner scan <dir> --json # JSON output
guard-scanner scan <dir> --sarif # SARIF for CI/CD
guard-scanner scan <dir> --html # HTML report
```

### 资产审计（Asset Audit）

审计公共注册表，检查是否存在凭证泄露风险。

```bash
guard-scanner audit npm <username>
guard-scanner audit github <username>
guard-scanner audit clawhub <query>
guard-scanner audit all <username> --verbose
```

### MCP服务器（MCP Server）

可作为MCP服务器使用，以便与集成开发环境（IDE）集成。

```bash
guard-scanner serve
```

编辑器配置（支持Cursor、Windsurf、Claude Code、OpenClaw）：

```json
{
  "mcpServers": {
    "guard-scanner": {
      "command": "npx",
      "args": ["-y", "@guava-parity/guard-scanner", "serve"]
    }
  }
}
```

MCP工具：`scan_skill`、`scan_text`、`check_tool_call`、`audit_assets`、`get_stats`。

### 监控模式（Watch Mode）

在开发过程中实时监控技能文件的更改。

```bash
guard-scanner watch ./skills/ --strict --soul-lock
```

### 与VirusTotal集成（VirusTotal Integration）

将语义检测技术与VirusTotal的70多种防病毒引擎结合使用。此功能为可选——guard-scanner亦可独立使用。

```bash
export VT_API_KEY=your-key
guard-scanner scan ./skills/ --vt-scan
```

## 运行时保护（Runtime Guard）

`before_tool_call`钩子可在5个防御层中进行26项运行时检查：

| 防御层 | 检查内容 |
|-------|-------|
| 1. 威胁检测 | 反向shell攻击、curl\|bash命令、SSRF攻击 |
| 2. 信任防御 | SOUL.md文件被篡改、内存注入 |
| 3. 安全性判断 | 工具参数中的提示注入 |
| 4. 行为分析 | 检测未经授权的执行行为 |
| 5. 信任利用（Trust Exploitation） | 检测对系统权限的非法请求 |

模式选项：`monitor`（仅记录日志）、`enforce`（阻止严重威胁，默认模式）、`strict`（阻止高风险威胁）。

## 关键参数

| 参数 | 功能 |
|------|--------|
| `--verbose` / `-v` | 显示详细的检测结果及行号 |
| `--strict` | 降低检测阈值 |
| `--soul-lock` | 启用身份保护机制 |
| `--vt-scan` | 增加VirusTotal的双层检测 |
| `--json` / `--sarif` / `--html` | 输出格式 |
| `--fail-on-findings` | 发现威胁时立即退出（适用于持续集成/持续部署流程CI/CD） |
| `--check-deps` | 扫描package.json中的依赖项 |
| `--rules <file>` | 加载自定义规则文件（JSON格式） |
| `--plugin <file>` | 加载插件模块 |

## 自定义规则（Custom Rules）

```javascript
module.exports = {
  name: 'my-plugin',
  patterns: [
    { id: 'MY_01', cat: 'custom', regex: /dangerous_pattern/g, severity: 'HIGH', desc: 'Description', all: true }
  ]
};
```

```bash
guard-scanner ./skills/ --plugin ./my-plugin.js
```

## 持续集成/持续部署（CI/CD）集成

```yaml
# .github/workflows/security.yml
- name: Scan AI skills
  run: npx -y @guava-parity/guard-scanner ./skills/ --format sarif --fail-on-findings > report.sarif
- uses: github/codeql-action/upload-sarif@v3
  with:
    sarif_file: report.sarif
```

## 威胁类别

涵盖OWASP LLM Top 10和Agentic Security Top 10中的32种威胁类型。完整规则库请参见`src/patterns.js`文件。主要威胁类别包括：

- **提示注入**：隐藏指令、不可见的Unicode字符、同形异义词（homoglyphs）
- **身份盗用**：替换用户身份、篡改SOUL.md文件、清除内存数据
- **内存注入**：通过对话内容注入恶意代码
- **MCP安全威胁**：利用MCP工具进行攻击、SSRF攻击、使用影子服务器（shadow servers）
- **A2A传播**：代理之间的恶意代码传播
- **供应链攻击**：域名抢注（typosquatting/slopsquatting）、生命周期脚本攻击
- **CVE漏洞**：CVE-2026-2256、25046、25253、25905、27825

> ⚿：使用此参数时必须启用`--soul-lock`选项