---
name: hefestoai-auditor
version: "2.1.0"
description: "这款由人工智能驱动的架构守护者采用了“苏格拉底式自适应架构”（Socratic Adaptive Architecture），具备以下功能：  
1. 执行安全审计；  
2. 检测代码语义上的变化；  
3. 分析代码的复杂性；  
4. 防止人工智能生成的代码出现质量下降（这些问题可能出现在多种编程语言中）。  
该守护者遵循严格的伦理原则进行运作，并具备多模型感知能力（multi-model awareness）。"
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

# HefestoAI Auditor v2.0

这是一款由人工智能驱动的架构监控工具，不仅仅是一个代码分析工具，而是一个基于“苏格拉底式自适应宪法”（Socratic Adaptive Constitution）进行管理的**安全与质量治理系统**。

## v2.0的新功能

- **苏格拉底式自适应宪法（Socratic Adaptive Constitution）**：为所有机器人行为提供正式的伦理框架。
- **语义漂移检测（Semantic Drift Detection）**：能够识别人工智能生成的代码在逻辑意图上发生的微妙变化。
- **多模型架构（Multi-Model Architecture）**：集成了Grok、DeepSeek、Claude和OpenAI作为运行子代理。
- **增强的安全机制**：明确的安全范围定义和持续审计原则。
- **优化的令牌管理（Enhanced Token Management）**：结构化的输出和基于差异的通信方式。

---

## 快速入门

### 运行全面审计

```bash
source /home/user/.hefesto_env 2>/dev/null
hefesto analyze /absolute/path/to/project --severity HIGH --exclude venv,node_modules,.git
```

### 问题严重程度分级

```bash
hefesto analyze /path --severity CRITICAL   # Critical only
hefesto analyze /path --severity HIGH        # High + Critical
hefesto analyze /path --severity MEDIUM      # Medium + High + Critical
hefesto analyze /path --severity LOW         # Everything
```

### 输出格式

```bash
hefesto analyze /path --output text                          # Terminal (default)
hefesto analyze /path --output json                          # Structured JSON
hefesto analyze /path --output html --save-html report.html  # HTML report
hefesto analyze /path --quiet                                # Summary only
```

### 状态与版本信息

```bash
hefesto status
hefesto --version
```

---

## 苏格拉底式自适应宪法（概述）

该工具遵循包含6个章节的正式宪法：

1. **基本原则**：诚实、人类主导、持续审计、有益性、责任性、隐私保护。
2. **苏格拉底式自适应方法（Socratic Adaptive Method, MSA）**：四阶段工作流程——诊断、决策（最多2个问题）、执行（最小影响）、验证。
3. **多模型架构**：当前使用Gemini模型，未来将集成DeepSeek/Claude模型。
4. **安全策略**：提前发现代码/配置漏洞（非运行时/网络层面的问题）。
5. **操作规则**：防止垃圾信息、避免误导性的输出、结构化的响应。
6. **功能**：审计协议、社交发布、开发工具。

完整宪法内容请参见工作区文件`CLAUDE.md`。

---

## 检测内容

### 安全漏洞
- SQL注入和命令注入
- 硬编码的敏感信息（API密钥、密码、令牌）
- 不安全的配置（Dockerfile、Terraform、YAML文件）
- 路径遍历和XSS风险

### 语义漂移（AI代码完整性）
- 保持语法但改变逻辑意图的代码修改
- 由AI生成的代码导致的架构退化
- 单一代码库中的隐藏重复项和不一致性

### 代码质量
- 循环复杂度超过10（高风险）或超过20（严重风险）
- 过度嵌套（超过4层）
- 过长的函数（超过50行）
- 代码异味和反模式

### DevOps问题
- Dockerfile中缺少`USER`字段、未设置`HEALTHCHECK`、以root权限运行
- Shell脚本中缺少`set -euo pipefail`选项、变量未加引号
- Terraform配置中缺少标签或使用硬编码值

### 无法检测的内容
- 运行时网络攻击（DDoS、端口扫描）
- 活动中的入侵行为（rootkit、权限提升）
- 网络流量监控
- 这些问题需通过SIEM/IDS/IPS或GCP安全命令中心进行处理

---

## 支持的语言（17种）

**代码语言**：Python、TypeScript、JavaScript、Java、Go、Rust、C#
**DevOps/配置文件**：Dockerfile、Jenkins/Groovy、JSON、Makefile、PowerShell、Shell脚本、SQL、Terraform、TOML、YAML

---

## 结果解读

```
📄 <file>:<line>:<col>
├─ Issue: <description>
├─ Function: <name>
├─ Type: <issue_type>
├─ Severity: CRITICAL | HIGH | MEDIUM | LOW
└─ Suggestion: <fix recommendation>
```

### 问题类型 | 严重程度 | 应对措施 |
|------|----------|--------|
| `VERY_HIGH_COMPLEXITY` | 严重 | 立即修复 |
| `HIGH_COMPLEXITY` | 高风险 | 在当前开发周期内修复 |
| `DEEP_NESTING` | 高风险 | 优化代码嵌套结构 |
| `SQL_INJECTION_RISK` | 高风险 | 对查询参数进行参数化处理 |
| `HARDCODED_SECRET` | 严重风险 | 移除并定期更换敏感信息 |
| `LONG_FUNCTION` | 中等风险 | 分解冗长的函数 |

---

## 使用技巧

```bash
# CI/CD gate - fail build on issues
hefesto analyze /path --fail-on HIGH --exclude venv

# Pre-push hook
hefesto install-hook

# Limit output
hefesto analyze /path --max-issues 10

# Exclude specific types
hefesto analyze /path --exclude-types VERY_HIGH_COMPLEXITY,LONG_FUNCTION
```

### 推荐的封装脚本（Wrapper Script）

```bash
#!/bin/bash
source /home/user/.hefesto_env 2>/dev/null
exec hefesto "$@"
```

---

## 多模型架构（正在使用中）

HefestoAI Auditor支持以下4个模型协同工作：

| 模型 | 角色 | 状态 |
|-------|------|--------|
| **Gemini 2.5 Flash** | 中枢处理单元 + 伦理审核机制 | 正在运行 |
| **DeepSeek** | 逻辑架构设计工具 | 正在运行 |
| **Claude Code** | 代码生成与重构工具 | 正在运行 |
| **Grok** | 情报收集与社交分析工具（X/Twitter） | 正在运行 |
| **OpenAI GPT** | 辅助分析工具 | 正在运行 |

HefestoAI作为**外部审计层**，负责审核所有模型的输出，确保其符合安全和质量标准。

### 多模型相关命令

```bash
# Query individual models
source ~/.hefesto_env 2>/dev/null
python3 ~/hefesto_tools/multi_model/query_model.py --model grok "Analyze trends"
python3 ~/hefesto_tools/multi_model/query_model.py --model deepseek "Formalize this algorithm"
python3 ~/hefesto_tools/multi_model/query_model.py --model claude "Review this code"

# Run constitutional pipelines
python3 ~/hefesto_tools/multi_model/orchestrate.py --task code-review --input "def foo(): ..."
python3 ~/hefesto_tools/multi_model/orchestrate.py --task full-cycle --input "Design a webhook validator"
python3 ~/hefesto_tools/multi_model/orchestrate.py --task strategy --input "Position vs Devin"
```

---

## 许可方案

| 许可等级 | 价格 | 主要功能 |
|------|-------|-------------|
| **免费版（FREE）** | 每月$0 | 静态代码分析、支持17种语言、预推送钩子 |
| **专业版（PRO）** | 每月$8 | 机器学习语义分析、REST API、BigQuery支持、自定义规则 |
| **高级版（OMEGA）** | 每月$19 | IRIS监控、自动关联分析、实时警报、团队仪表盘 |

所有付费版本均提供**14天免费试用**。

- **专业版**：https://buy.stripe.com/4gM00i6jE6gV3zE4HseAg0b
- **高级版**：https://buy.stripe.com/14A9AS23o20Fgmqb5QeAg0c

---

## 重要规则

- **务必**使用绝对路径，切勿使用相对路径。
- **务必**先加载环境变量：`source /home/user/.hefesto_env`
- **务必**排除以下目录：`--exclude venv,node_modules,.git`
- **仅报告**Hefesto检测到的问题，切勿自行添加问题。

---

## 关于我们

由**Narapa LLC**（佛罗里达州迈阿密）开发 — Arturo Velasquez (@artvepa)
GitHub仓库：https://github.com/artvepa80/Agents-Hefesto
支持邮箱：support@narapallc.com

> “干净的代码就是安全的代码” 🛡️