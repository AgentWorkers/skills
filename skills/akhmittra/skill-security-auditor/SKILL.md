---
name: skill-security-auditor
description: ClawHub 技能的命令行安全分析工具。运行 `analyze-skill.sh` 命令，可在安装前扫描 SKILL.md 文件，检测恶意代码模式、凭证泄露情况以及 C2（Command and Control）基础设施相关问题。该工具配备了包含 20 多种检测模式的威胁情报数据库。
emoji: 🔍🛡️
metadata:
  openclaw:
    requires:
      bins: ["curl", "jq", "grep", "bash"]
    version: "1.0.0"
    author: "akm626"
    category: "security"
    tags: ["security", "audit", "malware-detection", "skill-vetting", "cli-tool"]
---

# 技能安全审计器

## 介绍

技能安全审计器是一个**命令行工具**，用于在安装ClawHub技能之前对其进行基于模式的安全分析。鉴于最近发现了341个以上的恶意技能（ClawHavoc活动），这些技能会分发Atomic Stealer（AMOS）并窃取加密货币凭证，该工具提供了必要的预安装威胁检测功能。

**该工具提供以下功能：**
- ✅ Bash脚本（`analyze-skill.sh`）用于本地安全分析
- ✅ 威胁情报数据库（`patterns/malicious-patterns.json`）
- ✅ 与20多种已知恶意指标进行模式匹配
- ✅ 风险评分系统（0-100分）
- ✅ 详细的审计报告及建议

**使用方法：**
1. 从ClawHub安装此工具
2. 对任何技能（通过slug或本地文件）运行`analyze-skill.sh`脚本
3. 查看风险评估和发现结果
4. 根据评估结果做出安装决策

**在以下情况下使用此工具：**
- 即将从ClawHub安装新技能时
- 调查可疑技能行为时
- 对社区技能进行安全审查时
- 审计已安装的技能时

**此工具不执行以下操作：**
- ❌ 自动扫描技能（需手动运行）
- ❌ 阻止安装（仅提供建议）
- ❌ 访问VirusTotal API（请通过ClawHub的Web界面进行）
- ❌ 保证100%的检测率（建议采取深度防御措施）

## 核心功能

### 1. **恶意模式检测**
- 检查ClawHavoc活动中已知的恶意模式：
  - 假装的必备软件安装文件（如`openclaw-agent.zip`、`openclaw-setup.exe`）
  - SKILL.md文件中的可疑下载命令
  - 元数据中隐藏的负载执行
  - 社会工程学语言模式
  - 未经授权的外部二进制文件下载

### 2. **凭证泄露分析**
- 识别潜在的凭证泄露途径：
  - SKILL.md文件中硬编码的API密钥、令牌、密码
  - 可疑的环境变量泄露
  - 未加密的敏感数据传输
  - 过度宽泛的权限请求
  - 证书收集行为

### 3. **依赖关系链验证**
- 分析技能的依赖关系：
  - 未经验证的二进制文件需求
  - 来自可疑GitHub仓库的依赖项
  - 外部脚本的执行
  - 与未知主机的网络连接
  - 嵌套依赖关系的利用

### 4. **C2基础设施检测**
- 检查命令与控制（C2）指标：
  - 已知的恶意IP地址（例如，ClawHavoc的91.92.242.30）
  - 可疑的域名模式
  - 编码的通信端点
  - 数据泄露通道
  - 信标行为模式

### 5. **SKILL.md结构验证**
- 验证技能的完整性：
  - 正确的YAML格式
  - 元数据的一致性
  - 描述与实际行为的匹配度
  - 权限要求的合理性
  - 作者的验证（GitHub账户的使用时长）

## 安全评分系统

每个分析过的技能都会获得一个**风险评分（0-100分）**：
- **0-20分**：✅ **安全** - 无重大安全问题
- **21-40分**：⚠️ **低风险** - 有轻微问题，需谨慎操作
- **41-60分**：🟡 **中等风险** - 存在多个风险提示，建议手动审查
- **61-80分**：🔴 **高风险** - 存在严重问题，未经专家审查请勿安装
- **81-100分**：☠️ **危急** - 检测到恶意指标，请避免安装

## 使用说明

该工具提供了一个**bash脚本**（`analyze-skill.sh`），用于对ClawHub技能进行基于模式的安全分析。分析过程使用内置的威胁情报数据库在本地执行。

### 安装与设置

```bash
# Install the skill from ClawHub
npx clawhub install skill-security-auditor

# Make the analyzer executable
chmod +x ~/.openclaw/skills/skill-security-auditor/analyze-skill.sh

# Optional: Create alias for convenience
echo 'alias audit-skill="~/.openclaw/skills/skill-security-auditor/analyze-skill.sh"' >> ~/.bashrc
source ~/.bashrc
```

### 安装前审计技能

**方法1：通过slug自动从ClawHub获取并分析**

```bash
~/.openclaw/skills/skill-security-auditor/analyze-skill.sh --slug bitcoin-tracker

# Example output:
# ============================================
#          SECURITY AUDIT REPORT
# ============================================
# 
# Risk Score: 85/100 - ☠️ CRITICAL
# ...
```

**方法2：分析本地文件**

```bash
# Download skill first
curl -s "https://clawhub.ai/api/skills/bitcoin-tracker/latest" > /tmp/skill.md

# Then analyze
~/.openclaw/skills/skill-security-auditor/analyze-skill.sh --file /tmp/skill.md
```

### 审计所有已安装的技能

```bash
# Scan all skills in your workspace
for skill in ~/.openclaw/skills/*/SKILL.md; do
  echo "Checking: $(basename $(dirname $skill))"
  ~/.openclaw/skills/skill-security-auditor/analyze-skill.sh -f "$skill"
done
```

### 快速手动安全检查

```bash
# Fast grep-based pattern matching (no full analysis)
grep -iE "(prerequisite.*download|91\.92\.242\.30|curl.*\|.*bash)" SKILL.md
```

## 检测规则

### 🚨 危急警告（自动触发）

1. **虚假的必备软件部分**
   - 匹配关键词：“Prerequisites”（必备软件）、“Setup Required”（设置要求）、“Installation Steps”（安装步骤）
   - 包含`.zip`、`.exe`、`.dmg`文件的下载链接
   - 例如：“从https://...下载openclaw-agent.zip”

2. **已知的恶意基础设施**
   - IP地址：`91.92.242.30`（ClawHavoc的C2服务器）
   - 新注册或可疑的顶级域名（TLD）
   - 编码的URL或Base64混淆

3. **证书收集**
   - API密钥的正则表达式匹配：`api[_-]?key|token|password)\s*[:=]\s*['\"][^'\"]+['\"]`
   - SSH密钥访问请求
   - 钱包私钥相关内容

4. **未经授权的代码执行**
   - `curl | bash`或`wget | sh`命令
   - 隐藏的Base64编码命令
   - 对外部输入使用`eval()`或`exec()`函数

### ⚠️ 警示指标（评分增加）

1. **可疑的依赖关系**
   - 无明确理由的二进制文件需求
   - 来自未经验证来源的依赖项
   - 过度的权限请求

2. **混淆技术**
   - 元数据中高度编码的字符串
   - 缩小或混淆的JavaScript/Python代码
   - URL中的重定向链

3. **社会工程学语言**
   - 紧急提示语：“立即安装”、“时间有限”
   - 权威声明：“官方OpenClaw”、“由Anthropic验证”
   - 恐吓性语言：“不安装此工具，系统将面临风险”

### ✅ 安全提示指标

1. **经过验证的作者**
   - GitHub账户使用时长超过1年
   - 拥有多个高评价的技能
   - 积极参与社区活动

2. **透明的依赖关系**
   - 来源明确的二进制文件需求
   - 依赖开源工具
   - 权限需求有详细文档说明

3. **代码质量**
   - SKILL.md文件清晰易读
   - 适当的错误处理
   - 无不必要的网络请求

## 审计报告格式

```markdown
## Security Audit Report
**Skill**: {skill-name}
**Author**: {author}
**Version**: {version}
**Audit Date**: {date}

### Risk Score: {score}/100 - {RISK_LEVEL}

### Critical Findings:
- {finding 1}
- {finding 2}

### Warning Indicators:
- {warning 1}
- {warning 2}

### Positive Indicators:
- {positive 1}
- {positive 2}

### Recommendations:
{INSTALL | DO NOT INSTALL | REVIEW MANUALLY}

### Detailed Analysis:
{Deep dive into specific concerns}

### VirusTotal Link:
{If available from ClawHub}
```

## 与VirusTotal的集成

**重要提示**：此工具不直接访问VirusTotal的API。可以通过ClawHub与VirusTotal的合作关系，在其Web界面查看VirusTotal的扫描结果。

要查看技能的VirusTotal扫描结果：
1. 访问技能的ClawHub页面：`https://clawhub.ai/skills/{skill-slug}`
2. 在技能页面上查找VirusTotal的扫描结果
3. ClawHub会通过其与VirusTotal的合作关系自动扫描发布的技能

**此分析器侧重于基于模式的威胁检测**，它补充（但不会替代）ClawHub的VirusTotal扫描功能。

### 推荐的安全工作流程

1. **首先运行此分析器** - 进行基于模式的检测（本地、即时）
2. **查看ClawHub的VirusTotal结果** - 检查二进制文件/文件的信誉
3. **手动代码审查** - 对于关键场景进行最终验证

```bash
# Step 1: Pattern analysis (local)
~/.openclaw/skills/skill-security-auditor/analyze-skill.sh -s suspicious-skill

# Step 2: Visit ClawHub page for VirusTotal results
# https://clawhub.ai/skills/suspicious-skill

# Step 3: Manual review if needed
curl -s "https://clawhub.ai/api/skills/suspicious-skill/latest" > skill.md
less skill.md
```

## 示例工作流程

**场景**：用户想要安装名为`solana-wallet-tracker`的技能

**步骤1：运行安全分析**
```bash
$ ~/.openclaw/skills/skill-security-auditor/analyze-skill.sh -s solana-wallet-tracker

Fetching skill 'solana-wallet-tracker' from ClawHub...
✓ Skill fetched successfully

Analyzing skill content...

============================================
         SECURITY AUDIT REPORT
============================================

Risk Score: 95/100 - ☠️ CRITICAL

============================================

☠️ CRITICAL FINDINGS:
  CLAW-001: Fake Prerequisites - ClawHavoc Campaign [+50 points]
  └─ Matches the ClawHavoc campaign pattern of fake prerequisites requesting malicious binary downloads
  CLAW-002: Known C2 Infrastructure [+50 points]
  └─ IP address used in ClawHavoc campaign for C2 communications

============================================
RECOMMENDATION:
DO NOT INSTALL. Malicious patterns detected matching known attack campaigns.
============================================
```

**步骤2：做出决策**
- ☠️ **高风险** → **不要安装**
- 向ClawHub管理员报告该技能
- 寻找安全的替代方案

**步骤3：在ClawHub上验证**（可选）
```bash
# Visit skill page to check VirusTotal results
open "https://clawhub.ai/skills/solana-wallet-tracker"
```

## 高级功能

### 1. 行为分析（未来增强功能）
- 沙箱环境中的执行监控
- 网络流量分析
- 文件系统访问模式

### 2. 社区威胁情报
- 共享恶意技能签名
- 协作的IOC（Indicators of Compromise）数据库
- 声誉评分系统

### 3. 持续监控**
- 自动审计更新后的技能
- 新安全警告的即时通知
- 定期重新扫描已安装的技能

## 减少误报

为了减少误报：
1. **上下文分析**：验证合法工具的二进制文件需求（例如，用于GitHub CLI的`gh`）
2. **白名单**：经过验证的作者和知名技能会获得信任加分
3. **人工审核选项**：始终为安全决策提供详细理由
4. **申诉流程**：用户可以报告误报以调整技能的信誉

## 合规性与伦理

- ✅ 分析公开可用的技能元数据
- ✅ 保护用户安全和隐私
- ✅ 促进负责任的技能开发
- ❌ 不进行未经授权的访问
- ❌ 不能保证100%的安全性（没有工具能做到）
- ❌ 不替代用户的判断

## 响应模板

### 安全的技能
```
✅ Security Audit Complete

{skill-name} has been analyzed and appears SAFE to install.

Risk Score: {score}/100 (LOW)

No malicious patterns detected. The skill:
- Uses standard dependencies from trusted sources
- Has a verified author with {X} published skills
- Contains clear documentation with no obfuscation
- Requests appropriate permissions for its function

VirusTotal: {link}

Recommendation: Safe to proceed with installation.
```

### 可疑的技能
```
🔴 Security Alert: HIGH RISK DETECTED

{skill-name} has been flagged with CRITICAL security concerns.

Risk Score: {score}/100 (HIGH)

⚠️ Critical Findings:
{detailed findings}

This skill matches patterns from the ClawHavoc malware campaign.

Recommendation: DO NOT INSTALL. Consider reporting this skill to ClawHub moderators.

Alternative safe skills: {suggestions}
```

## 技术实现说明

**模式数据库位置**：`~/.openclaw/security-auditor/patterns/`
- `malicious-patterns.json`：已知的恶意指标
- `safe-patterns.json`：白名单中的元素
- `ioc-database.json`：泄露的指标

**更新机制**：
```bash
# Pull latest threat intelligence
curl -s "https://openclaw-security.github.io/threat-intel/latest.json" \
  > ~/.openclaw/security-auditor/patterns/ioc-database.json
```

## 贡献方式

发现新的恶意模式？请将IOC（Indicators of Compromise）提交给OpenClaw安全工作组：
- GitHub：`github.com/openclaw/security-auditor`
- 报告格式：包含模式正则表达式、描述和严重性的JSON文件

## 限制

⚠️ **重要免责声明**：
- 该工具提供分析结果，但不保证100%的准确性
- 复杂的恶意软件可能逃避检测
- 对于关键应用，建议结合使用VirusTotal和人工审查
- 安全是共同的责任
- 没有工具可以完全替代专业安全人员

## 参考资料

- ClawHavoc活动分析：[The Hacker News, 2026年2月]
- OpenClaw与VirusTotal的安全合作
- 恶意技能数据库：OpenSourceMalware Research
- ClawHub管理指南：`docs.openclaw.ai/security`

---

**记住**：最佳的安全措施是深度防御。将此工具作为安全策略的一部分，但不要仅依赖它。

保持安全，保持怀疑态度，确保安全。🦞🛡️