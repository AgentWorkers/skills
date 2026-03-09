---
name: "Canary � Agent Safety Tripwire System"
description: "AI代理的安全监控与警报机制：防止未经授权的文件访问、危险命令的执行以及异常活动的发生。在检测到严重违规行为时，系统会自动停止相关操作。蜜罐（Honeypot）机制可有效检测潜在的窥探行为。"
author: "@TheShadowRose"
version: "1.0.3"
tags: ["safety", "security", "tripwire", "monitoring", "honeypot", "agent-protection"]
license: "MIT"
---
# Canary – 人工智能代理的安全监控与预警系统

本系统专为人工智能（AI）代理提供安全监控与预警功能，可防范未经授权的文件访问、危险命令的执行以及异常行为。在检测到严重违规行为时，系统会自动停止代理的运行；同时，通过设置诱饵文件来检测潜在的窥探行为。

---

**人工智能代理的安全监控与预警系统**

该系统能够有效防止未经授权的文件访问、危险命令的执行以及代理的异常行为，并在发现严重违规时自动停止代理的运行。此外，通过诱饵文件可及时发现任何窥探行为。

---

## 主要功能

Canary 提供三层安全防护机制：

1. **操作监控**：在执行命令前检查文件路径和命令内容。
2. **诱饵文件**：设置这些文件为绝对禁止访问的“陷阱”，用于检测潜在的入侵行为。
3. **审计日志**：详细记录所有操作行为，并通过模式匹配进行异常检测。

### 核心特性

- **受保护路径**：阻止对敏感目录（如 `/etc/`、`~/.ssh/` 等）的访问。
- **可定制的保护列表**：允许用户自定义需要保护的目录。
- **细粒度操作控制**：支持读、写、删除等操作权限的控制。

- **禁止的命令模式**：利用正则表达式识别危险命令（例如 `rm -rf /`、`chmod 777`、`curl | sh` 等）。
- **可扩展的模式库**：支持用户自定义的命令模式。

- **速率限制**：限制文件操作、网络请求和命令执行的频率。
- **配置灵活的阈值**：用户可设置操作次数和阈值，防止代理行为失控。

- **自动停止**：一旦超过预设的违规阈值，系统会自动停止代理，避免连锁故障的发生，需要手动审核后才能重新启动代理。

- **诱饵文件**：创建不可访问的诱饵文件，用于检测文件被修改、删除或访问的情况，并通过哈希验证确保文件完整性。

- **审计日志**：记录所有操作行为，包括违规事件的历史记录和异常模式（如频繁的违规行为、重复攻击目标、时间集中的异常操作等），并可导出为 JSON 或 Markdown 格式。

---

## 快速入门

### 安装

无需依赖其他库，仅需要 Python 3.7 及以上的标准库环境。

```bash
# Copy config example
cp config_example.py config.py

# Edit config with your protected paths
nano config.py
```

### 基本使用

```python
from canary import CanaryMonitor

# Initialize monitor
canary = CanaryMonitor('config.py')

# Check path before access
is_safe, reason = canary.check_path('/etc/passwd', 'read')
if not is_safe:
    print(f"Blocked: {reason}")
    exit(1)

# Check command before execution
is_safe, reason = canary.check_command('rm -rf /')
if not is_safe:
    print(f"Blocked: {reason}")
    exit(1)

# Get status
status = canary.get_status()
print(f"Violations: {status['violation_count']}/{status['halt_threshold']}")
```

### 命令行接口（CLI）使用方法

```bash
# Check status
python3 canary.py status

# Check if path is safe
python3 canary.py check-path --path /etc/passwd --operation read

# Check if command is safe
python3 canary.py check-command --command "rm -rf /"

# Reset monitoring (clears violations)
python3 canary.py reset
```

---

## 诱饵文件设置

创建绝对禁止访问的诱饵文件：

```bash
# Create tripwire
python3 canary_tripwire.py create \
  --path ~/.secrets/fake-api-key.txt \
  --severity critical \
  --description "Honeypot to detect credential snooping"

# List all tripwires
python3 canary_tripwire.py list

# Check for triggered tripwires
python3 canary_tripwire.py check

# View alert history
python3 canary_tripwire.py alerts --limit 10

# Remove tripwire
python3 canary_tripwire.py remove --path ~/.secrets/fake-api-key.txt
```

### Python API 使用方法

```python
from canary_tripwire import TripwireManager

manager = TripwireManager()

# Create tripwire
manager.create_tripwire(
    path='~/.aws/fake-credentials',
    severity='critical',
    description='Detects AWS credential access'
)

# Check all tripwires
triggered = manager.check_tripwires()
if triggered:
    print(f"⚠️  {len(triggered)} tripwire(s) triggered!")
    for alert in triggered:
        print(f"  - {alert['path']}: {alert['event']}")
```

---

## 审计报告

系统可分析日志并生成安全报告：

```bash
# Summary report
python3 canary_audit.py summary

# View violations by severity
python3 canary_audit.py violations --severity critical

# Timeline of recent events
python3 canary_audit.py timeline --hours 24

# Detect suspicious patterns
python3 canary_audit.py patterns

# Export full report
python3 canary_audit.py export --output report.json --format json
python3 canary_audit.py export --output report.md --format markdown
```

### Python API 使用方法

```python
from canary_audit import CanaryAuditor

auditor = CanaryAuditor('canary.log')

# Generate summary
summary = auditor.generate_summary_report()
print(f"Total violations: {summary['total_violations']}")

# Get critical violations
critical = auditor.get_violations_by_severity('critical')

# Detect patterns
patterns = auditor.detect_patterns()
if patterns['rapid_violations']:
    print("⚠️  Rapid violation sequence detected!")

# Export report
auditor.export_report('safety-report.md', format='markdown')
```

---

## 配置设置

详细配置选项请参考 `config_example.py` 文件。

### 必需的配置项

```python
# Protected paths
protected_paths = [
    '/etc/',
    '~/.ssh/',
    '~/critical-data/',
]

# Forbidden patterns
forbidden_patterns = [
    r'rm\s+-rf\s+/',      # Recursive delete from root
    r'chmod\s+777',       # World-writable permissions
    r'curl.*\|\s*sh',     # Curl piped to shell
]

# Auto-halt threshold
halt_threshold = 5  # Stop after 5 critical/high violations

# Rate limits
rate_limits = {
    'file_operations': {'limit': 100, 'window': 60},  # 100 per minute
    'command_executions': {'limit': 20, 'window': 60},
}
```

---

## 集成示例

- **与代理运行时集成**：将 Canary 与代理一起部署，以防止意外删除系统文件、凭证泄露或代理行为失控。
- **多代理系统**：为每个代理配置独立的 Canary 实例和规则：
  - **研究型代理**：限制网络访问。
  - **编码型代理**：禁止在生产环境中执行任何操作。
  - **管理型代理**：允许全部操作，但需严格审计。

- **部署前检查**：在部署前使用 Canary 检查代理配置的合法性。

---

## 使用场景

- **自主代理的安全防护**：与自主代理一起使用，防止文件被意外删除、凭证被窃取或代理行为失控。
- **多代理系统**：为每个代理配置合适的安全策略。
- **开发/测试环境**：在代理开发过程中使用 Canary 检测危险行为，验证安全机制的有效性。
- **生产环境监控**：在生产环境中实时监控代理行为，确保合规性，并及时发现异常。

---

## 架构概述

```
┌─────────────────┐
│   Your Agent    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐      ┌──────────────────┐
│ CanaryMonitor   │◄────►│  config.py       │
│ (canary.py)     │      │  (your rules)    │
└────────┬────────┘      └──────────────────┘
         │
         ├─────► canary.log (action log)
         │
         ▼
┌─────────────────┐      ┌──────────────────┐
│ TripwireManager │◄────►│ .canary_tripwires│
│ (tripwire.py)   │      │ (honeypot files) │
└────────┬────────┘      └──────────────────┘
         │
         └─────► alerts.log
         
         
┌─────────────────┐
│ CanaryAuditor   │───► reports (JSON/MD)
│ (audit.py)      │
└─────────────────┘
```

---

## 最佳实践

- **从严格配置开始**：初始阶段设置严格的规则，根据实际需求逐步放宽限制。
- **策略性使用诱饵文件**：将诱饵文件放置在关键位置（如伪造的凭证文件、空的“secret”目录或诱饵配置文件）。
- **定期审查日志**：定期检查日志以发现潜在的安全问题。

- **测试配置**：在部署前测试配置的正确性和有效性。

---

## 限制与注意事项

- **模式匹配基于正则表达式**：虽然功能强大，但可能存在误判。
- **无内置警报机制**：系统仅记录日志，不提供实时警报。
- **速率限制仅针对当前会话有效**：重启后限制无效。

---

## 许可证

本软件采用 MIT 许可协议，详细信息请参阅 [LICENSE](LICENSE)。

**作者**：Shadow Rose

---

## 为何需要这个工具？

AI 代理可能迅速造成严重后果：
- 一个错误的命令可能删除关键文件。
- 代理行为失控可能导致系统资源耗尽。
- 被入侵的代理可能泄露敏感信息。

Canary 提供了多层次的安全防护：
- **预防性防护**：在危险操作发生前进行拦截。
- **检测性防护**：通过诱饵文件发现潜在的入侵行为。
- **事后审计**：提供详细的审计日志用于事件分析。

这是一个简单且无需额外依赖的安全解决方案，专为自主运行的 AI 代理设计。

---

## ⚠️ 安全提示：配置文件的执行方式

本工具会通过 `importlib.exec_module` 从用户提供的 Python 文件中加载配置。**请确保你使用的配置文件是经过你本人编写或审核过的**，因为恶意文件可能导致系统受到攻击。请注意：
- 本工具遵循 Python 的标准配置机制，但配置文件仍需视为敏感资源。
- 在执行前，系统会验证配置文件的存在性、扩展名（.py）以及文件大小（最大 1MB）。
- 请勿使用来自不可信来源的配置文件。

## ⚠️ 免责声明

本软件按“原样”提供，不附带任何明示或暗示的保证。使用本软件产生的任何损害或后果（包括但不限于财务损失、数据丢失、安全漏洞或业务中断）均由用户自行承担。
- 作者不对因使用本软件而产生的任何问题负责。
- 本软件不提供财务、法律、交易或专业建议。用户需自行评估其适用性。
- 作者不对第三方使用、修改或分发本软件的行为负责。

通过下载、安装或使用本软件，即表示你已阅读并同意自行承担所有风险。

**安全提示：** 本软件提供额外的安全措施，但不能替代专业的安全审计、渗透测试或合规性检查。对于受监管行业（如医疗、金融、法律等），用户应咨询专业安全人员并确保合规性。

---

## 支持与联系方式

| | |
|---|---|
| 🐛 **问题报告** | TheShadowyRose@proton.me |
| ☕ **Ko-fi** | [ko-fi.com/theshadowrose](https://ko-fi.com/theshadowrose) |
| 🛒 **Gumroad** | [shadowyrose.gumroad.com](https://shadowyrose.gumroad.com) |
| 🐦 **Twitter** | [@TheShadowyRose](https://twitter.com/TheShadowyRose) |
| 🐙 **GitHub** | [github.com/TheShadowRose](https://github.com/TheShadowRose) |
| 🧠 **PromptBase** | [promptbase.com/profile/shadowrose](https://promptbase.com/profile/shadowrose) |

*本工具基于 [OpenClaw](https://github.com/openclaw/openclaw) 开发——感谢 OpenClaw 的支持！*

---

🛠️ **需要定制服务？** 我们提供定制的 OpenClaw 代理和功能服务，价格从 500 美元起。如有需求，请通过 [Fiverr](https://www.fiverr.com/s/jjmlZ0v) 联系我。

> **安装说明：** `canary` 这个技能名称在 ClawHub 上已被占用，建议使用以下命令安装：`clawhub install canary-sr`