---
name: skill-auditor
version: 3.1.0
description: "OpenClaw技能的终极安全扫描工具。提供18项安全检查，包括提示注入检测、下载并执行恶意代码、权限提升、凭证收集、供应链攻击、加密信息泄露等。采用五维信任评分机制，并支持趋势跟踪功能。"
metadata:
  openclaw:
    requires:
      bins: ["python3", "bash"]
      env: []
      config: []
    user-invocable: true
---
# Skill Auditor v3.1.0

这是一款专为 OpenClaw/ClawHub 技能设计的安全扫描工具，能够全面检测 18 项安全风险，其中包括 **提示注入（prompt injection）检测**——它是首个能够识别技能文档中代理操控攻击的扫描工具。该工具支持五维度的信任评分、趋势跟踪、差异分析以及性能基准测试，并且对合法技能的检测结果绝对不会出现误报。

## 使用场景

1. **从 ClawHub 安装新技能**：运行 `inspect.sh` 进行全面的预安装验证。
2. **审核现有技能**：使用 `audit.sh` 扫描任何技能目录。
3. **生成信任评分**：使用 `trust_score.py` 为技能生成 0-100 分的评分（共五个维度）。
4. **比较技能安全性**：使用 `trust_score.py --compare` 进行对比分析。
5. **跟踪技能改进情况**：使用 `trust_score.py --save-trend` 监测评分随时间的变化。
6. **审查技能更新**：使用 `diff-audit.sh` 比较技能更新前后的差异。
7. **批量扫描**：使用 `audit-all.sh` 或 `benchmark.sh` 对所有技能进行批量分析。

## 快速入门

```bash
# Audit a single skill
bash audit.sh /path/to/skill

# Trust score (0-100 across 5 dimensions)
python3 trust_score.py /path/to/skill

# Compare two skills side by side
python3 trust_score.py /path/to/skill1 --compare /path/to/skill2

# Track score over time
python3 trust_score.py /path/to/skill --save-trend
python3 trust_score.py /path/to/skill --trend

# Diff audit (before/after update)
bash diff-audit.sh /path/to/old-version /path/to/new-version

# Benchmark against a corpus
bash benchmark.sh /path/to/skills-dir

# Inspect a ClawHub skill before installing
bash inspect.sh skill-slug

# Audit all installed skills
bash audit-all.sh

# Generate a markdown report
bash report.sh

# Run test suite (28 assertions)
bash test.sh
```

## 安全最佳实践

**建议执行**：
- ✓ 在从不可信来源安装技能之前，务必对其进行安全审核。
- ✓ 检查技能的信任评分，拒绝评分低于 60 分（D 级）的技能。
- ✓ 在更新技能时使用 `diff-audit.sh` 以检测潜在的代码退化问题。
- ✓ 使用 `--json` 输出格式，以便集成到持续集成/持续部署（CI/CD）流程中。
- ✓ 定期运行 `--save-trend` 命令，以监控技能的安全状况。

**禁止执行**：
- ✗ 未经仔细审查，不要安装评分低于 40 分（F 级）的技能。
- ✗ 忽视任何“严重”（CRITICAL）的安全问题，因为这些问题可能预示着潜在的安全威胁。
- ✗ 未经了解技能的权限需求，就盲目将其添加到允许列表中。
- ✗ 仅仅因为技能“流行”或“官方”就跳过安全审核。

## 安全检查（共 18 项）

| 编号 | 检查项 | 严重程度 | 描述 |
|-------|--------|-----------|
| 1    | 证书窃取（Credential Harvest） | 严重（CRITICAL） | 脚本读取 API 密钥/令牌并执行网络请求。 |
| 2    | 数据泄露风险（Exfiltration Risk） | 严重（CRITICAL） | 脚本中包含 webhook.site、requestbin 或 ngrok 的 URL。 |
| 3    | 混淆的负载数据（Obfuscated Payload） | 严重（CRITICAL） | 使用 Base64 编码的 URL 或 shell 命令。 |
| 4    | 敏感文件访问（Sensitive File Access） | 严重（CRITICAL） | 访问 `/etc/passwd`、`~/.ssh` 或 `~/.aws/credentials` 等文件。 |
| 5    | 加密钱包相关风险（Crypto Wallet） | 严重（CRITICAL） | 硬编码的 ETH/BTC 钱包地址（可能导致资金损失）。 |
| 6    | 依赖项混淆（Dependency Confusion） | 严重（CRITICAL） | 公开依赖项中包含内部或私有的包。 |
| 7    | 拼写错误（Typosquatting） | 严重（CRITICAL） | 包名拼写错误（如 lodahs、requets 等）。 |
| 8    | 符号链接攻击（Symlink Attack） | 严重（CRITICAL） | 符号链接指向敏感系统路径。 |
| 9    | 代码执行风险（Code Execution） | 警告（WARNING） | 使用 `eval()`、`exec()` 或 `subprocess` 等函数执行代码。 |
| 10    | 时间炸弹（Time Bomb） | 警告（WARNING） | 包含可能触发延迟执行的代码。 |
| 11    | 数据追踪风险（Telemetry Detection） | 警告（WARNING） | 使用分析 SDK 或追踪像素的代码。 |
| 12    | 权限滥用风险（Excessive Permissions） | 警告（WARNING） | 请求超过 15 个环境变量或配置项。 |
| 13    | 非标准端口使用（Unusual Ports） | 警告（WARNING） | 使用非标准端口进行网络请求。 |
| 14    | 提示注入（Prompt Injection） | 严重（CRITICAL） | 文档中存在代理操控的提示，可能导致角色劫持或隐藏的 HTML 指令。 |
| 15    | 下载并执行代码（Download-Execute） | 严重（CRITICAL） | 使用 `curl`、`bash`、`wget` 或 `eval $(curl)` 下载并执行代码，以及不安全的 pip/npm 安装。 |
| 16    | 隐藏文件（Hidden Files） | 警告（WARNING） | 可能隐藏恶意内容的隐藏文件。 |
| 17    | 环境变量泄露（Env Exfiltration） | 严重（CRITICAL） | 读取敏感的环境变量并发送网络请求。 |
| 18    | 权限提升风险（Privilege Escalation） | 严重（CRITICAL） | 使用 `sudo`、`chmod 777` 或 `setuid` 来提升权限。 |

**注**：文档中提及的证书信息仅被视为 **信息性内容**（INFO），不属于严重安全问题（非 CRITICAL）。

## 信任评分（五个维度）

| 维度 | 最高分 | 评分依据 |
|-------|---------|
| 安全性（Security） | 35 | 安全检查结果（严重问题扣 18 分，警告问题扣 4 分）。 |
| 质量（Quality） | 22 | 技能的描述、版本信息、使用说明、示例代码、元数据及变更日志。 |
| 结构（Structure） | 18 | 文件组织结构、测试用例、README 文件以及代码的合理性。 |
| 透明度（Transparency） | 15 | 使用的许可证、代码是否未经过压缩、代码注释的完整性。 |
| 行为安全性（Behavioral） | 10 | 代码中的速率限制、错误处理机制及输入验证机制。 |

**评分等级**：A（90 分以上）、B（75 分以上）、C（60 分以上）、D（40 分以上）、F（40 分以下）。

### 对比评分（Comparative Scoring）
```bash
python3 trust_score.py /path/to/skill-a --compare /path/to/skill-b
```
该功能可显示各维度的评分变化及整体评分差异。

### 趋势跟踪（Trend Tracking）
```bash
python3 trust_score.py /path/to/skill --save-trend   # Record score
python3 trust_score.py /path/to/skill --trend         # View history
```
`trust_trends.json` 文件会记录每个技能的评分变化趋势（最多保存 50 条记录）。

## 所用工具

| 文件名 | 功能 |
|------|---------|
| audit.sh | 单个技能的安全审核（包含 18 项检查）。 |
| audit-all.sh | 批量扫描所有已安装的技能。 |
| trust_score.py | 生成五维度的信任评分（0-100 分）。 |
| diff-audit.sh | 比较不同版本的技能以检测安全问题。 |
| benchmark.sh | 对所有技能进行整体安全评估并生成汇总统计。 |
| inspect.sh | 用于 ClawHub 的预安装验证流程。 |
| report.sh | 生成Markdown格式的报告。 |
| test.sh | 自动化测试套件（包含 28 个测试用例）。 |
| allowlist.json | 包含已知安全的技能列表。 |

## 测试用例

共有 12 个测试用例（其中 8 个为恶意用例，4 个为正常用例），包含 28 个自动化测试用例：

```bash
bash test.sh
```

**恶意用例**：
- 证书窃取（Credential Harvest）
- 混淆的负载数据（Obfuscated Payload）
- 访问敏感文件（Sensitive File Access）
- 加密钱包相关风险（Crypto Wallet）
- 时间炸弹（Time Bomb）
- 符号链接攻击（Symlink Attack）
- 提示注入（Prompt Injection）
- 下载并执行代码（Download-Execute）
- 权限提升（Privilege Escalation）

**正常用例**：
- 基础技能（Basic Skill）
- 包含证书信息的文档（用于检测误报）
- 与网络相关的技能（Network-Related Skills）
- 包含隐藏文件的技能（Skills with Hidden Files）

## 出错代码

- 0：通过（PASS）/ 安全，可以安装。
- 1：需要进一步审核（REVIEW）/ 发现警告（Warnings Found）。
- 2：失败（FAIL）/ 存在严重问题（Critical Issues）。
- 3：出现错误（Error）/ 输入无效（Bad Input）。

## 变更日志

请参阅 [CHANGELOG.md](CHANGELOG.md) 以获取完整的版本历史记录。