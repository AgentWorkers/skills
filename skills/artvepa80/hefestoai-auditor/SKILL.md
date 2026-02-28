---
name: hefestoai-auditor
version: "2.2.0"
description: "静态代码分析工具。能够检测17种语言中的安全漏洞、代码质量问题以及代码复杂性问题。所有分析过程均在本地完成——无需将任何代码传输到外部服务器。"
metadata:
  {
    "openclaw":
      {
        "emoji": "🔨",
        "requires": { "bins": ["hefesto"] },
        "install":
          [
            {
              "id": "pip",
              "kind": "pip",
              "package": "hefesto-ai",
              "bins": ["hefesto"],
              "label": "Install HefestoAI (pip)"
            }
          ]
      }
  }
---
# HefestoAI Auditor

一款用于安全、质量和代码复杂性分析的静态代码分析工具，支持17种编程语言。

**隐私政策：**所有分析操作均在本地完成，不会将任何代码传输到外部服务，分析过程中也不会进行任何网络请求。

**权限要求：**该工具仅具有读取指定目录内源文件的权限（仅读），不会修改您的代码。

---

## 安装

```bash
pip install hefesto-ai
```

## 快速入门

```bash
hefesto analyze /path/to/project --severity HIGH
```

### 问题严重程度分级

```bash
hefesto analyze /path/to/project --severity CRITICAL   # Critical only
hefesto analyze /path/to/project --severity HIGH        # High + Critical
hefesto analyze /path/to/project --severity MEDIUM      # Medium + High + Critical
hefesto analyze /path/to/project --severity LOW         # Everything
```

### 输出格式

```bash
hefesto analyze /path/to/project --output text                          # Terminal (default)
hefesto analyze /path/to/project --output json                          # Structured JSON
hefesto analyze /path/to/project --output html --save-html report.html  # HTML report
hefesto analyze /path/to/project --quiet                                # Summary only
```

### 状态与版本信息

```bash
hefesto status
hefesto --version
```

---

## 工具能检测的内容

### 安全漏洞
- SQL注入和命令注入
- 硬编码的秘密信息（API密钥、密码、令牌）
- 不安全的配置（Dockerfile、Terraform、YAML文件）
- 路径遍历和XSS风险

### 代码语义一致性问题（AI生成代码的完整性）
- 逻辑上的变化虽然保持了语法正确性，但实际含义发生了改变
- 由AI生成的代码导致的架构退化
- 单一代码库中的重复代码和不一致性

### 代码质量问题
- 循环复杂度超过10（高风险）或超过20（极度危险）
- 代码嵌套层次过深（超过4层）
- 函数过长（超过50行）
- 代码存在不良实践（如“代码异味”和反模式）

### DevOps相关问题
- Dockerfile中缺少`USER`字段、未配置`HEALTHCHECK`、以root权限运行
- Shell脚本中未使用`set -euo pipefail`命令、变量未加引号
- Terraform配置文件中缺少标签或使用硬编码值

### 无法检测的内容
- 运行时网络攻击（如DDoS、端口扫描）
- 活动中的入侵行为（如rootkit的植入、权限提升）
- 网络流量监控
- 对于这些问题，请使用SIEM/IDS/IPS或GCP Security Command Center等工具进行监控。

---

## 支持的编程语言（共17种）
**代码类型：** Python、TypeScript、JavaScript、Java、Go、Rust、C#
**DevOps/配置文件格式：** Dockerfile、Jenkins/Groovy、JSON、Makefile、PowerShell、Shell脚本、SQL、Terraform、TOML、YAML

---

## 结果解读

```
file.py:42:10
  Issue: Hardcoded database password detected
  Function: connect_db
  Type: HARDCODED_SECRET
  Severity: CRITICAL
  Suggestion: Move credentials to environment variables or a secrets manager
```

### 问题类型及应对措施
| 问题类型 | 严重程度 | 应对措施 |
|------|----------|--------|
| `VERY_HIGH_COMPLEXITY` | 极度危险 | 立即修复 |
| `HIGH_complexITY` | 高风险 | 在当前开发周期内修复 |
| `DEEP_NESTING` | 高风险 | 优化代码嵌套结构 |
| `SQL_INJECTION_RISK` | 高风险 | 将查询参数化 |
| `HARDCODED_SECRET` | 极度危险 | 移除并定期更换这些硬编码的秘密信息 |
| `LONG_FUNCTION` | 中等风险 | 将长函数拆分为多个较小的函数 |

---

## 与持续集成/持续部署（CI/CD）系统的集成

```bash
# Fail build on HIGH or CRITICAL issues
hefesto analyze /path/to/project --fail-on HIGH

# Pre-push git hook
hefesto install-hook

# Limit output
hefesto analyze /path/to/project --max-issues 10

# Exclude specific issue types
hefesto analyze /path/to/project --exclude-types VERY_HIGH_COMPLEXITY,LONG_FUNCTION
```

---

## 许可证定价

| 许可证等级 | 价格 | 主要功能 |
|------|-------|-------------|
| **免费** | 每月0美元 | 静态代码分析、支持17种语言、预推送钩子 |
| **专业版** | 每月8美元 | 机器学习驱动的语义分析、REST API接口、BigQuery集成、自定义规则 |
| **高级版** | 每月19美元 | IRIS监控系统、自动关联分析、实时警报、团队仪表盘 |

所有付费版本均提供**14天免费试用**。

更多价格信息及订阅方式，请访问 [hefestoai.narapallc.com](https://hefestoai.narapallc.com)。

如需激活许可证，请参考 [hefestoai.narapallc.com/setup](https://hefestoai.narapallc.com/setup) 中的设置指南。

---

## 关于HefestoAI Auditor

由 **Narapa LLC**（佛罗里达州迈阿密）开发 — Arturo Velasquez (@artvepa)  
- GitHub仓库：[github.com/artvepa80/Agents-Hefesto](https://github.com/artvepa80/Agents-Hefesto)  
- 技术支持：support@narapallc.com