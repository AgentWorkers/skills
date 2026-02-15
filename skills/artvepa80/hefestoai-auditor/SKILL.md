---
name: hefestoai-auditor
version: "1.2.0"
description: "基于 HefestoAI 的人工智能代码分析工具：支持 17 种编程语言，可执行安全审计、检测代码问题（如“代码异味”）、分析代码复杂性，并提供由机器学习算法优化的改进建议。当用户需要分析代码、进行安全审计、检查代码质量或查找漏洞时，可随时使用该工具。"
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

# HefestoAI 验证器技能

这是一款由 AI 驱动的代码质量监控工具，能够分析 17 种语言的代码，检测其中的安全漏洞、复杂性问题、代码异味以及违反最佳实践的情况。

## 快速入门

### 运行全面审计
```bash
# IMPORTANTE: Cargar environment primero para activar licencia
source /home/user/.hefesto_env 2>/dev/null
hefesto analyze /ruta/absoluta/al/proyecto --severity HIGH --exclude venv,node_modules,.git
```

### 严重性级别
```bash
hefesto analyze /path/to/project --severity CRITICAL   # Solo criticos
hefesto analyze /path/to/project --severity HIGH        # High y Critical
hefesto analyze /path/to/project --severity MEDIUM      # Medium, High, Critical
hefesto analyze /path/to/project --severity LOW         # Todo
```

### 输出格式
```bash
hefesto analyze /path/to/project --output text          # Default, terminal
hefesto analyze /path/to/project --output json          # JSON estructurado
hefesto analyze /path/to/project --output html --save-html report.html  # Reporte HTML
hefesto analyze /path/to/project --quiet                # Solo resumen
```

### 检查状态和版本
```bash
hefesto status
hefesto --version
```

## 建议：使用包装脚本

为了获得可靠的结果，请创建一个包装脚本，确保在每次运行 Hefesto 时都会加载您的许可证：
```bash
#!/bin/bash
# Save as /usr/local/bin/hefesto (replaces direct binary)
source /path/to/.hefesto_env 2>/dev/null
exec /path/to/venv/bin/hefesto "$@"
```

这样无论 Hefesto 以何种方式被调用，都能确保您的许可证处于激活状态。

### 预构建的审计脚本
```bash
# Save as ~/hefesto_tools/run_audit.sh
#!/bin/bash
SEVERITY="${1:-HIGH}"
TARGET="${2:-/path/to/your/project}"
source /path/to/.hefesto_env 2>/dev/null
exec hefesto analyze "$TARGET" --severity "$SEVERITY" --exclude venv,node_modules,.git
```

## 使用方法
```bash
bash ~/hefesto_tools/run_audit.sh              # HIGH severity, default project
bash ~/hefesto_tools/run_audit.sh CRITICAL     # CRITICAL only
bash ~/hefesto_tools/run_audit.sh MEDIUM /other/project  # Custom
```

## 重要提示

- **务必** 使用绝对路径，切勿使用相对路径。
- **务必** 在执行之前加载环境变量（`source /home/user/.hefesto_env`）以激活许可证。
- **务必** 排除 `venv`, `node_modules`, `.git` 目录，以避免因依赖关系导致的误报。
- **仅报告** Hefesto 在输出中显示的问题，切勿自行添加额外的问题。

## 支持的语言（17 种）

**代码语言：** Python, TypeScript, JavaScript, Java, Go, Rust, C#
**DevOps/配置文件：** Dockerfile, Jenkins/Groovy, JSON, Makefile, PowerShell, Shell, SQL, Terraform, TOML, YAML

## 检测内容

### 安全问题
- SQL 注入漏洞
- 硬编码的密钥和 API 密钥
- 命令注入风险
- 不安全的配置

### 代码质量
- 循环复杂度过高（函数过于复杂）
- 深层嵌套（超过 4 层）
- 函数过长（超过 50 行）
- 代码异味和反模式

### DevOps 问题
- Dockerfile：缺少 `USER` 变量，未设置 `HEALTHCHECK`，以 root 权限运行
- Shell 脚本：缺少 `set -euo pipefail` 选项，变量未加引号
- Terraform：缺少标签，使用硬编码值

## 解读结果

HefestoAI 以以下格式输出检测结果：
```
📄 <file>:<line>:<col>
├─ Issue: <description>
├─ Function: <name>
├─ Type: <issue_type>
├─ Severity: CRITICAL | HIGH | MEDIUM | LOW
└─ Suggestion: <fix recommendation>
```

### 严重性等级说明
- **CRITICAL**：循环复杂度 > 20。立即修复。
- **HIGH**：复杂度 10-20，存在深层嵌套或 SQL 注入风险。在当前开发周期内修复。
- **MEDIUM**：存在代码风格问题或需要小幅度改进。根据实际情况进行修复。
- **LOW**：仅提供最佳实践建议。

### 问题类型
- `VERY_HIGH_complexITY`：循环复杂度 > 20
- **HIGH_complexITY**：循环复杂度 10-20
- **DEEP_NESTING**：嵌套层次超过阈值（默认为 4 层）
- **SQL_INJECTION_RISK**：存在通过字符串拼接导致的 SQL 注入风险
- **LONG_FUNCTION**：函数长度超过规定阈值

## 使用技巧

### 排除目录
为了避免误报，请始终排除依赖目录：
```bash
hefesto analyze /path/to/project --severity HIGH --exclude venv,node_modules,.git
```

### CI/CD 防护机制
如果检测到问题，请终止构建过程：
```bash
hefesto analyze /path/to/project --fail-on HIGH --exclude venv
```

### 安装推送前钩子
```bash
hefesto install-hook
```

### 限制输出内容
```bash
hefesto analyze /path/to/project --max-issues 10
```

### 排除特定类型的问题
```bash
hefesto analyze /path/to/project --exclude-types VERY_HIGH_COMPLEXITY,LONG_FUNCTION
```

## 许可证等级

| 许可证等级 | 价格 | 主要功能 |
|------|-------|-------------|
| **FREE** | 每月 USD0 | 静态分析，支持 17 种语言，推送前钩子 |
| **PRO** | 每月 USD8 | 机器学习驱动的语义分析，REST API，BigQuery，自定义规则 |
| **OMEGA** | 每月 USD19 | IRIS 监控，自动关联分析，实时警报，团队仪表盘 |

所有付费等级均提供 **14 天的免费试用期**。

### 升级链接
- **PRO**：https://buy.stripe.com/4gM00i6jE6gV3zE4HseAg0b
- **OMEGA**：https://buy.stripe.com/14A9AS23o20Fgmqb5QeAg0c

### 激活许可证
```bash
export HEFESTO_LICENSE_KEY=<your-key>
hefesto status  # verify tier
```

## 关于我们

HefestoAI 由 **Narapa LLC**（佛罗里达州迈阿密）开发 — Arturo Velasquez (@artvepa)  
GitHub：https://github.com/artvepa80/Agents-Hefesto  
支持邮箱：support@narapallc.com  

> “干净的代码就是安全的代码。”