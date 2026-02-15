---
name: obekt-security
description: 针对代码、文件以及代理技能的基本威胁检测与安全分析功能。适用于需要扫描漏洞、验证安全模式、检测恶意行为或审计代码库中的安全问题的场景。
---

# ObekT Security

这是一个用于代码、文件和代理技能的基本威胁检测与安全分析工具包。

**Pro Tier** 提供持续监控和专业报告生成功能，适用于高级安全工作流程。

## 核心功能

### 1. 基于模式的威胁检测
- 扫描代码中的常见漏洞模式（如 SQL 注入、XSS、命令注入）
- 识别硬编码的秘密信息、API 密钥和凭证
- 检测不安全的文件操作和路径遍历风险
- 发现不安全的加密实践

### 2. 安全审计工作流程
- 对代码和应用程序进行基本审查
- 检查身份验证/授权的薄弱环节
- 验证输入处理和清理机制
- 审查 API 端点的安全性

### 3. 恶意模式识别
- 检测混淆的代码模式
- 识别数据泄露尝试
- 扫描可疑的网络请求
- 检查未经授权的加密钱包操作

## 快速入门

### 安装

**Basic Tier（无需依赖）：**
所有核心扫描脚本均支持 Python 3.8 及更高版本的标准库。

**Pro Tier（需要额外依赖）：**
```bash
pip install watchdog  # For continuous monitoring
```

### 扫描代码库中的常见漏洞

```bash
python3 scripts/threat_scan.py --directory /path/to/code --severity medium,high
```

### 检查硬编码的秘密信息

```bash
python3 scripts/secret_scan.py --file path/to/source.py
```

### 审计代理技能

```bash
python3 scripts/skill_audit.py --skill-path /path/to/skill
```

## 威胁检测模式

### 严重性极高的模式
- 使用用户输入直接执行命令（如 exec、eval、os.system）
- 通过字符串连接构建 SQL 查询
- 硬编码的私钥或助记词
- 外部钱包资金流失的尝试
- 无限制的文件上传

### 严重性较高的模式
- 随机数生成机制较弱
- 硬编码的 API 密钥或令牌
- 缺少输入验证
- 不安全的加密算法（如 MD5、SHA1）
- 路径遍历漏洞

### 严重性中等的模式
- 记录敏感数据
- 不安全的 URL 重定向
- 缺少速率限制机制
- 密码策略较弱

## 安全审计检查清单

在审计代码或技能时，请检查以下内容：
- [ ] 无硬编码的秘密信息（密钥、令牌、密码）
- [ ] 输入验证和清理机制
- [ ] 正确的错误处理（无信息泄露）
- [ ] 安全的加密实现
- [ ] 在需要的地方进行了身份验证/授权
- [ ] 最小权限原则得到遵守
- [ ] 无命令注入漏洞
- [ ] 安全的文件操作
- [ ] 安全的网络通信
- [ ] 正确的会话管理

## 使用脚本

### threat_scan.py
扫描目录以检测已知的漏洞模式。

```bash
python3 scripts/threat_scan.py <path> [--severity LEVEL] [--output FORMAT]
```

**选项：**
- `--severity`：按严重性过滤（严重、高、中、低）。默认：全部
- `--output`：输出格式（json、text、markdown）。默认：text
- `--recursive`：递归扫描子目录。默认：true

**示例：**
```bash
# Find critical and high issues in a project
python3 scripts/threat_scan.py ~/project --severity critical,high --output markdown
```

### secret_scan.py
检测硬编码的凭证和秘密信息。

```bash
python3 scripts/secret_scan.py <path> [--patterns PATTERN_FILE]
```

**检测的模式包括：**
- API 密钥（AWS、Google、Stripe 等）
- 私钥（PEM、OpenSSH 格式）
- 数据库连接字符串
- 加密钱包的种子/助记词
- OAuth 令牌

### skill_audit.py
审计代理技能的安全性问题。

```bash
python3 scripts/skill_audit.py <skill-path> [--quick]
```

**检查内容：**
- SKILL.md 文件的结构和完整性
- 文件权限（必需与可选）
- 外部依赖项和命令的安全性
- 网络请求和数据处理方式
- 凭据处理方式

### monitor.py（Pro Tier）
持续安全监控——监视目录变化并自动扫描。

```bash
python3 scripts/monitor.py --path /path/to/project --interval 60
python3 scripts/monitor.py --config monitor.json
```

**功能：**
- 实时监控文件变化
- 在文件修改时自动进行威胁和秘密信息扫描
- 可配置的严重性阈值和扫描间隔
- 发现问题时发送警报通知
- 智能过滤（忽略 .git、node_modules 等文件）

**选项：**
- `--path`：要监控的目录
- `--interval`：同一路径的扫描间隔（秒）
- `--severity`：报告的严重性级别
- `--alert`：发现问题时触发警报
- `--config`：JSON 配置文件

### generate_report.py（Pro Tier）
生成专业的安全审计报告。

```bash
python3 scripts/generate_report.py --scan-dir /path/to/project --output report.md
python3 scripts/generate_report.py --input scan_results.json --format html
```

**功能：**
- 多种输出格式：Markdown、HTML、JSON
- 带有严重性评估的执行摘要
- 详细的发现结果及代码片段
- 优先级排序的建议
- 适合客户使用的格式

**选项：**
- `--scan-dir`：要扫描的目录（重新扫描）
- `--input`：包含现有扫描结果的 JSON 文件
- `--output`：输出文件路径
- `--format`：markdown、html 或 json
- `--severity`：包含的严重性级别

## Pro Tier 功能

### 4. 持续监控
**新功能** - 为开发工作流程提供实时安全监控

在开发过程中自动监控代码库中的安全漏洞。

```bash
python3 scripts/monitor.py --path /path/to/project --interval 60
```

**功能：**
- 实时监控目录中的文件变化
- 在文件修改时自动触发安全扫描
- 可配置的扫描间隔和严重性阈值
- 发现问题时发送警报通知（支持 Webhook）
- 智能地跳过临时文件和目录

**配置：**
```json
{
  "paths": ["./project"],
  "min_scan_interval": 30,
  "severity": "high,critical",
  "alert_on_issues": true,
  "recursive": true,
  "filters": {
    "include_extensions": [".py", ".js", ".ts", ".java", ".go", ".rs"],
    "exclude_dirs": [".git", "__pycache__", "node_modules", ".venv"]
  },
  "alert_config": {
    "webhook_url": "https://your-webhook-endpoint"
  }
}
```

### 5. 专业报告生成
**新功能** - 生成适合客户使用的审计报告

生成多种格式的专业安全审计报告，可用于交付给客户或作为合规性文档。

```bash
# Generate report from fresh scan
python3 scripts/generate_report.py --scan-dir /path/to/project --output report.md

# Generate HTML report
python3 scripts/generate_report.py --scan-dir /path/to/project --output report.html --format html

# Generate from existing scan results
python3 scripts/generate_report.py --input scan_results.json --output client_report.md
```

**功能：**
- 多种输出格式：Markdown、HTML、JSON
- 专业的格式展示，带有严重性颜色编码
- 带有整体严重性评估的执行摘要
- 详细的发现结果及代码片段
- 按严重性优先排序的建议
- 适合客户使用的报告格式

**报告内容：**
- 带有整体严重性的执行摘要
- 严重性分级表
- 详细的威胁发现结果及代码片段
- 秘密/凭证泄露报告
- 优先级排序的建议
- 时间戳和元数据

## 参考文档

有关详细的威胁模式和修复指南：
- 请参阅 [VULNERABILITY_PATTERNS.md](references/VULNERABILITY_PATTERNS.md) 以获取完整的模式目录
- 请参阅 [REMEDIATION_GUIDE.md](references/REMEDIATION_GUIDE.md) 以获取问题修复方法
- 请参阅 [CHECKLIST.md](references/CHECKLIST.md) 以获取全面的审计检查清单
- 请参阅 [CRYPTO_SECURITY.md](references/CRYPTO_SECURITY.md) 以获取区块链相关的模式信息

## 定价层级

### Free Tier
- 基于模式的威胁检测
- 秘密信息扫描
- 基本技能审计
- 手动扫描执行

### Pro Tier（每月 $5）
- 全部 Free Tier 功能
- **持续监控守护进程**，提供实时警报
- **专业报告生成**（Markdown、HTML、JSON）
- 适合客户使用的审计报告
- 优先级支持

### Enterprise Tier（每月 $50）
- 全部 Pro Tier 功能
- 私有技能审计
- 自定义模式规则
- 团队协作功能
- Webhook 集成

*注：所有层级均为独立运行，无需云账户。*

## 与其他工具的集成

此工具可与以下工具良好配合使用：
- **skill-creator**：在开发过程中验证技能的安全性
- **clawcast**：审计钱包交易的安全性
- **auth-auditor**：补充身份验证流程的安全性

## 限制

该工具提供基于模式的**基本**威胁检测功能。它不能替代：
- 专家的手动安全审查
- 动态应用程序安全测试（DAST）
- 渗透测试
- 静态分析工具（如 SonarQube、CodeQL）

请将其作为第一道防线使用，而非替代全面的安全部署。