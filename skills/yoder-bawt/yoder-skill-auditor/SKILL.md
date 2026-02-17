---
name: skill-auditor
version: 3.0.0
description: "OpenClaw技能的终极安全扫描工具。提供18项安全检查，包括提示注入检测、下载并执行恶意代码、权限提升、凭证收集、供应链攻击、加密信息泄露等多种安全风险。采用五维信任评分机制，并支持趋势跟踪功能。"
metadata:
  openclaw:
    requires:
      bins: ["python3", "bash"]
      env: []
      config: []
    user-invocable: true
---
# Skill Auditor v3.0.0

这是一款专为 OpenClaw/ClawHub 技能设计的安全扫描工具，能够全面检测 18 项安全风险，其中包括 **提示注入（prompt injection）检测**——它是首个能够发现技能文档中代理操控攻击的扫描工具。该工具支持五维度的信任评分、趋势跟踪、差异分析以及性能基准测试，并且对合法技能的检测结果绝对不会出现误报。

## 何时需要激活该工具

1. **从 ClawHub 安装新技能**时：运行 `inspect.sh` 进行全面的预安装验证。
2. **审核现有技能**时：使用 `audit.sh` 扫描任何技能目录。
3. **生成信任评分**时：使用 `trust_score.py` 根据五个维度为技能打分（0-100 分）。
4. **比较技能**时：使用 `trust_score.py --compare` 进行对比分析。
5. **跟踪技能改进情况**时：使用 `trust_score.py --save-trend` 监测评分变化。
6. **审查技能更新**时：使用 `diff-audit.sh` 比较技能的版本差异。
7. **批量扫描**时：使用 `audit-all.sh` 或 `benchmark.sh` 对所有技能进行统一分析。

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

## 安全最佳实践与注意事项

**应遵循的操作：**
- ✓ 在从不可信来源安装技能之前，务必对其进行安全审核。
- ✓ 拒绝评分低于 60 分（D 级）的技能。
- ✓ 在更新技能时使用 `diff-audit.sh` 以检测潜在的代码退化问题。
- ✓ 使用 `--json` 输出格式，以便集成到持续集成/持续部署（CI/CD）流程中。
- ✓ 定期运行 `--save-trend` 命令来监控技能的安全状况。

**不应遵循的操作：**
- ✗ 未经彻底人工审查，不要安装评分低于 40 分（F 级）的技能。
- ✗ 忽视任何“严重”（CRITICAL）的安全问题，因为这些问题可能预示着潜在的安全威胁。
- ✗ 未经核实技能的权限需求，就盲目将其添加到允许列表中。
- ✗ 仅仅因为技能“流行”或“官方发布”，就跳过安全审核。

## 安全检查项目（共 18 项）

| 序号 | 检查项 | 严重程度 | 描述 |
|------|---------|-----------|
| 1    | 信用信息收集（Credential Harvesting） | 严重（CRITICAL） | 脚本读取 API 密钥/令牌并执行网络请求 |
| 2    | 数据泄露风险（Exfiltration Risk） | 严重（CRITICAL） | 脚本中包含 webhook.site、requestbin 或 ngrok 的 URL |
| 3    | 携带混淆信息的有效载荷（Obfuscated Payload） | 严重（CRITICAL） | 使用 Base64 编码的 URL 或 shell 命令 |
| 4    | 访问敏感文件系统（Sensitive File System Access） | 严重（CRITICAL） | 试图访问 `/etc/passwd`、`~/.ssh` 或 `~/.aws/credentials` 文件 |
| 5    | 加密钱包相关风险（Crypto Wallet） | 严重（CRITICAL） | 硬编码的 ETH/BTC 钱包地址（可能导致资金损失） |
| 6    | 依赖关系混乱（Dependency Confusion） | 严重（CRITICAL） | 公开依赖项中包含内部/私有包 |
| 7    | 拼写错误（Typo Squatting） | 严重（CRITICAL） | 包名拼写错误（如 lodahs、requets 等） |
| 8    | 符号链接攻击（Symlink Attack） | 严重（CRITICAL） | 符号链接指向敏感系统路径 |
| 9    | 代码执行风险（Code Execution） | 警告（WARNING） | 使用 `eval()`、`exec()` 或 `subprocess` 等函数 |
| 10   | 时间炸弹（Time Bomb） | 警告（WARNING） | 可能触发延迟执行的代码逻辑 |
| 11   | 数据追踪风险（Telemetry Detection） | 警告（WARNING） | 包含数据分析 SDK 或追踪像素的代码 |
| 12   | 权限滥用风险（Excessive Permissions） | 警告（WARNING） | 请求超过 15 个环境变量/配置项 |
| 13   | 非标准端口使用（Unusual Ports） | 警告（WARNING） | 向非标准端口发起网络请求 |
| 14   | 提示注入（Prompt Injection） | 严重（CRITICAL） | 文档中存在代理操控指令（如“忽略提示”或角色劫持行为） |
| 15   | 下载并执行文件（Download-Execute） | 严重（CRITICAL） | 使用 `curl`、`bash`、`wget` 或 `eval $(curl)` 下载并执行文件 |
| 16   | 隐藏文件（Hidden Files） | 警告（WARNING） | 可能隐藏恶意内容的隐藏文件 |
| 17   | 环境变量泄露（Env Exfiltration） | 严重（CRITICAL） | 读取敏感环境变量并发送网络请求 |
| 18   | 权限提升风险（Privilege Escalation） | 严重（CRITICAL） | 使用 `sudo`、`chmod 777` 或 `setuid` 来提升权限 |

**注：** 文档中提及的信用信息（credentials）仅被标记为“INFO”级别，不属于严重安全风险。

## 信任评分（五个维度）

| 维度          | 最高分    | 评分依据                |
|---------------|-----------|-------------------|
| 安全性（Security）    | 35       | 安全检查结果（严重问题扣 18 分，警告问题扣 4 分） |
| 质量（Quality）     | 22       | 技能描述、版本信息、使用说明、示例代码、元数据、变更日志 |
| 结构（Structure）    | 18       | 文件组织结构、测试用例、README 文件、代码范围合理性 |
| 透明度（Transparency） | 15       | 使用的许可证、代码是否未压缩、代码注释情况 |
| 行为安全性（Behavioral） | 10       | 限流机制、错误处理能力、输入验证机制 |

**评分等级**：A（90 分以上）、B（75 分以上）、C（60 分以上）、D（40 分以上）、F（40 分以下）

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

## 工具列表

| 文件名        | 功能                        |
|--------------|---------------------------|
| audit.sh       | 单个技能的安全审核（包含 18 项检查）         |
| audit-all.sh     | 批量扫描所有已安装的技能             |
| trust_score.py     | 计算技能的信任评分（五维度，0-100 分）       |
| diff-audit.sh     | 比较不同版本的技能以检测安全问题         |
| benchmark.sh     | 对所有技能进行整体安全评估并生成统计报告     |
| inspect.sh       | ClawHub 安装前的预检查流程             |
| report.sh       | 生成 Markdown 格式的审计报告             |
| test.sh       | 自动化测试套件（包含 28 个测试用例）         |
| allowlist.json     | 已验证为安全的技能列表             |

## 测试用例

共有 12 个测试用例（其中 8 个为恶意用例，4 个为正常用例），包含 28 个自动化测试项：

```bash
bash test.sh
```

**恶意用例**包括：信用信息收集、携带混淆信息的有效载荷、访问敏感文件系统、加密钱包相关风险、时间炸弹、符号链接攻击、提示注入、下载并执行文件操作以及权限提升。

**正常用例**包括：基本技能测试、信用信息文档检查（用于验证是否出现误报）、网络相关技能测试以及隐藏文件相关测试。

## 程序退出代码

- 0：通过，安全安装
- 1：需要进一步审查（发现警告）
- 2：失败，存在严重安全问题
- 3：出现错误或输入格式不正确

## 变更日志（Change Log）

请参阅 [CHANGELOG.md] 以获取完整的版本更新历史。