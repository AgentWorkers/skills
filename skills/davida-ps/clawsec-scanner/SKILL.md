---
name: clawsec-scanner
version: 0.0.1
description: 这是一个用于代理平台的自动化漏洞扫描器。它能够执行依赖项扫描（npm audit、pip-audit）、多数据库的CVE（Common Vulnerabilities and Exposures）查询（OSV、NVD、GitHub Advisory）、SAST（Static Application Security Testing）分析（Semgrep、Bandit），以及对技能钩子（skill hooks）进行基本的DAST（Dynamic Application Security Testing）安全测试。
homepage: https://clawsec.prompt.security
clawdis:
  emoji: "🔍"
  requires:
    bins: [node, npm, python3, pip-audit, semgrep, bandit, jq, curl]
---
# ClawSec 扫描器

这是一个针对代理平台的全方位安全扫描器，能够自动检测多方面的安全漏洞：

- **依赖项扫描**：使用 `npm audit` 和 `pip-audit` 分析 npm 和 Python 依赖项，并生成结构化的 JSON 输出。
- **CVE 数据库集成**：查询 OSV（主要来源）、NVD 2.0 和 GitHub 建议数据库以获取更多漏洞信息。
- **SAST 分析**：使用 Semgrep（针对 JavaScript/TypeScript）和 Bandit（针对 Python）进行静态代码分析，检测硬编码的秘密信息、命令注入、路径遍历和不安全的反序列化问题。
- **DAST 框架**：提供基本的动态分析功能，用于测试技能挂接点的安全性（如输入验证、超时处理）。
- **统一报告**：整合漏洞报告，包含漏洞的严重程度分类和修复建议。
- **持续监控**：通过 OpenClaw 挂接点实现自动化的定期扫描。

## 特点

### 多引擎扫描

该扫描器结合了四种互补的扫描方式，以实现全面的安全漏洞检测：

1. **依赖项扫描**：
   - 作为子进程执行 `npm audit --json` 和 `pip-audit -f json`。
   - 解析结构化输出，提取 CVE ID、严重程度和受影响的版本。
   - 处理边缘情况：如缺少 `package-lock.json`、未发现漏洞或 JSON 格式错误。

2. **CVE 数据库查询**：
   - **OSV API**（主要来源）：免费使用，无需认证，支持广泛的生态系统（npm、PyPI、Go、Maven）。
   - **NVD 2.0**（可选）：需要 API 密钥以避免 6 秒的请求频率限制。
   - **GitHub 建议数据库**（可选）：使用 OAuth 令牌通过 GraphQL API 获取数据。
   - 将所有 API 响应统一转换为 `Vulnerability` 数据结构。

3. **静态分析（SAST）**：
   - 使用 `Semgrep`（针对 JavaScript/TypeScript）检测安全问题。
   - 使用 `--config auto` 或 `--config p/security-audit` 配置选项。
   - 识别硬编码的秘密信息（API 密钥、令牌）、命令注入、路径遍历和不安全的反序列化问题。

4. **动态分析（DAST）**：
   - 提供动态分析框架，用于测试技能挂接点的安全性。
   - 验证恶意输入处理、超时处理和资源限制等安全机制。
   - 注意：传统的 Web DAST 工具（如 ZAP、Burp）不适用于代理平台，此工具专为代理平台设计。

### 统一报告

所有扫描类型都会生成符合统一 `ScanReport` JSON 格式的报告：

每个 `Vulnerability` 对象包含以下信息：
- `id`：CVE-2023-12345 或 GHSA-xxxx-yyyy-zzzz
- `source`：npm-audit | pip-audit | osv | nvd | github | sast | dast
- `severity`：critical | high | medium | low | info
- `package`：受影响的包名（SAST/DAST 时显示为 'N/A'
- `version`：受影响的版本
- `fixed_version`：第一个包含修复的版本（如果存在）
- `title`：简短描述
- `description`：完整的漏洞说明
- `references`：更多信息的链接
- `discovered_at`：ISO 8601 时间戳

### OpenClaw 集成

通过挂接点实现自动化持续监控：
- 按可配置的间隔运行扫描（默认：86400 秒/24 小时）。
- 在 `agent:bootstrap` 和 `command:new` 事件触发扫描。
- 将扫描结果及其严重程度摘要记录到 `event.messages` 数组中。
- 通过环境变量 `CLAWSEC_SCANNER_INTERVAL` 控制扫描频率。

## 安装

### 先决条件

确保所需二进制文件已安装：

### 选项 A：通过 ClawHub 安装（推荐）

### 选项 B：手动安装并验证

## 使用方法

### 按需进行 CLI 扫描

**CLI 参数**：
- `--target <路径>`：要扫描的目录（必填）
- `--output <文件>`：将结果写入文件（可选，默认为 stdout）
- `--format <json|text>`：输出格式（默认为 json）
- `--check`：验证所有必需的二进制文件是否已安装

### 开启 OpenClaw 挂接点（持续监控）

启用自动化定期扫描：
- 在 `agent:bootstrap` 和 `command:new` 事件时触发扫描。
- 将扫描结果及其严重程度摘要记录到日志中。
- 对于高/严重级别的漏洞，建议采取相应的修复措施。
- 启用挂接点后，重新启动 OpenClaw 服务，然后运行 `/new` 命令以立即开始扫描。

### 环境变量

## 架构

### 模块化设计

每种扫描方式都是独立的模块，可以单独运行或作为整体扫描的一部分。

### 故障处理策略

扫描器优先考虑系统的可用性，而不是严格地处理故障：
- 网络故障 → 发送部分扫描结果并记录警告。
- 缺少工具 → 跳过该扫描类型，继续其他扫描。
- JSON 格式错误 → 解析有效的数据并记录错误。
- API 请求频率限制 → 实施指数级退避策略，切换到其他数据源。
- 未发现漏洞 → 发送成功报告（结果数组为空）。

**会导致立即终止的严重故障**：
- 目标路径不存在。
- 所需扫描工具均缺失。
- 检测到并发扫描（存在锁文件）。

### 子进程执行方式

所有外部工具均作为子进程运行，并生成结构化的 JSON 输出。

## 故障排除

### 常见问题

- **“缺少 package-lock.json”警告**：`npm audit` 需要 `package-lock.json` 文件才能运行。在目标目录中运行 `npm install` 生成该文件。
- 如果 `npm audit` 失败，扫描器会继续执行其他扫描类型。

- **“NVD API 请求频率限制被超过”**：设置环境变量 `CLAWSEC_NVD_API_KEY`。
- 未设置 API 密钥时，每次请求之间会有 6 秒的延迟。
- 使用 OSV API 作为主要数据源（不受频率限制）。

- **“找不到 pip-audit”**：安装 `uv pip install pip-audit` 或 `pip install pip-audit`。
- 确认 `which pip-audit` 是否可以执行；如果安装在非标准路径下，请将其添加到 PATH 环境变量中。

- **“Semgrep 可执行文件缺失”**：安装 `pip install semgrep` 或 `brew install semgrep`。
- 需要 Python 3.8 及更高版本的运行环境。
- 可以使用 Docker 镜像 `returntocorp/semgrep` 作为替代方案。

- **检测到并发扫描**：存在锁文件 `/tmp/clawsec-scanner.lock`。等待当前扫描完成或手动删除该文件，以防止扫描结果重复。

### 验证扫描器是否正常工作

### 开发

- **运行测试**：执行相应的测试用例。
- **代码格式检查**：使用代码格式化工具检查代码质量。

### 添加自定义 Semgrep 规则

在 `.semgrep/rules/` 文件中创建自定义规则。

- 更新 `scripts/sast_analyzer.mjs` 以包含自定义规则。

### 与 ClawSec 套件的集成

该扫描器可以独立使用，也可以作为 ClawSec 生态系统的一部分：
- **clawsec-suite**：用于安装和管理 `clawsec-scanner` 的元技能。
- **clawsec-feed**：用于检测恶意行为的建议系统。
- **openclaw-audit-watchdog**：基于 Cron 任务的自动化审计工具。

安装完整的 ClawSec 套件：

## 安全考虑

- 扫描器代码中不包含硬编码的秘密信息。
- API 密钥仅从环境变量中读取（不会被记录或提交到代码库）。
- 子进程参数使用数组传递，以防止 shell 注入攻击。
- 所有外部工具的输出都经过 try/catch 语句处理异常。

### 漏洞优先级

- **高/严重级别的漏洞** 应立即处理：
  - 依赖项中的已知漏洞（CVSS 9.0 及以上等级）。
  - 代码中的硬编码 API 密钥或凭据。
  - 命令注入漏洞。
  - 未经验证的路径遍历行为。

- **中/低级别的漏洞** 可在常规的开发周期内处理：
  - 过时的依赖项（无已知漏洞）。
  - 缺少安全头部信息。
  - 使用弱加密算法。

- **信息级别的漏洞** 仅作为提示：
  - 已弃用的 API 接口。
  - 由代码格式化工具标记的代码质量问题。

## 开发计划

### v0.1.0（当前版本）
- [x] 依赖项扫描（npm audit, pip-audit）
- [x] CVE 数据库集成（OSV, NVD, GitHub 建议数据库）
- [x] 静态代码分析（Semgrep, Bandit）
- [x] 基本的动态分析框架
- [x] 统一的 JSON 报告格式
- [x] OpenClaw 挂接点集成

### 未来改进计划
- [ ] 自动修复漏洞（依赖项升级、代码修复）
- [ ] 与 GitHub 代码扫描集成（使用 SARIF 格式）
- [ ] 提供用于跟踪漏洞的 Web 仪表板
- [ ] 通过 CI/CD 在提交高严重级别漏洞时阻止代码合并
- [ ] 扫描容器镜像（Docker, OCI）
- [ ] 扫描基础设施即代码（Terraform, CloudFormation）
- [ ] 完整的代理平台动态分析功能（需要更深入的集成）

## 贡献

发现安全问题？请通过 security@prompt.security 私下联系我们。

如需功能请求或报告漏洞，请在以下链接提交问题：
https://github.com/prompt-security/clawsec/issues

## 许可证

使用 AGPL-3.0 或更高版本的许可证。

详细许可协议请参见仓库根目录下的 LICENSE 文件。

## 资源

- **ClawSec 官网**：https://clawsec.prompt.security
- **文档**：https://clawsec.prompt.security/scanner
- **GitHub 仓库**：https://github.com/prompt-security/clawsec
- **OSV API 文档**：https://osv.dev/docs/
- **NVD API 文档**：https://nvd.nist.gov/developers/vulnerabilities
- **Semgrep 文档**：https://semgrep.dev/explore
- **Bandit 文档**：https://bandit.readthedocs.io/