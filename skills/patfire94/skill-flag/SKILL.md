# 技能检测工具 🛡️  
用于扫描 Clawdbot/OpenClaw 中的技能，检测恶意代码、后门程序及安全风险。  

**创建者：** DarkM00n（漏洞赏金猎人兼安全研究员）  

## 命令  

### 扫描所有已安装的技能  
```
scan skills
scan all skills
security scan
```  

### 扫描特定技能  
```
scan skill <skill-name>
check skill <skill-name>
```  

### 安装前扫描（URL/路径）  
```
scan skill url <clawdhub-url>
pre-scan <skill-name>
```  

### 快速风险报告  
```
skill risk report
security report
```  

## 使用方法  

运行扫描工具：  
```bash
python3 skills/skill-flag/scanner.py [--skill NAME] [--all] [--verbose]
```  

或向代理发送指令：  
- “扫描我所有已安装的技能，检查是否存在安全问题”  
- “检查‘crypto-tracker’技能是否安全”  
- “生成一份安全报告”  

## 检测内容  

| 类别 | 风险等级 | 例子 |  
|----------|------------|----------|  
| 🔴 数据泄露 | 严重（CRITICAL） | 使用 `curl/wget` 访问外部域名、`fetch()`、`requests.post()` 等操作 |  
| 🔴 后门程序 | 严重（CRITICAL） | 使用 `reverse shell`、`nc -e`、`bash -i`、编码后的恶意载荷 |  
| 🔴 凭据窃取 | 严重（CRITICAL） | 访问 `~/.ssh`、`~/.aws`、API 密钥、`.env` 文件 |  
| 🟠 提示注入 | 高风险（HIGH） | 如 “ignore previous”、“system override”、“new instructions” 等指令 |  
| 🟠 代码执行 | 高风险（HIGH） | 使用 `eval()`、`exec()`、`subprocess` 且 `shell=True` |  
| 🟡 持久化机制 | 中等风险（MEDIUM） | Cron 任务、systemd 单元、启动脚本 |  
| 🟡 混淆技术 | 中等风险（MEDIUM） | 使用 Base64 编码的命令、十六进制字符串、rot13 等加密方式 |  
| 🟢 可疑行为 | 低风险（LOW） | 不常见的导入语句、网络活动等 |  

## 风险评分  

每个技能的风险等级为 0-100：  
- **0-20**：✅ 无问题  
- **21-40**：🟢 低风险（Minor concerns）  
- **41-60**：🟡 中等风险（Recommended for review）  
- **61-80**：🟠 高风险（Need careful inspection）  
- **81-100**：🔴 严重风险（Do not use without audit）  

## 输出结果  

报告保存路径：`skills/skill-flag/reports/`  

**示例输出：**  
```
🛡️ SECURITY SCAN REPORT
━━━━━━━━━━━━━━━━━━━━━━━
Scanned: 12 skills
Clean: 9
Warnings: 2
Critical: 1

⚠️ WARNINGS:
- crypto-tracker: External API calls (expected for price data)
- web-scraper: Uses requests library

🔴 CRITICAL:
- shady-skill: 
  - Line 45: curl to unknown domain
  - Line 67: Base64 encoded payload
  - Line 89: Reads ~/.ssh/id_rsa
  RECOMMENDATION: Remove immediately
```  

## 被扫描的目录：**  
1. `~/.clawdbot/skills/` – 全局安装的技能  
2. `./skills/` – 工作区技能  
3. `~/.npm-global/lib/node_modules/clawdbot/skills/` – 内置技能  

## 正假阳性判断  

某些合法技能需要网络访问或文件操作，扫描工具会将其标记为待审核，但不会自动阻止其运行：  
- 价格追踪工具 → 需要 API 调用（✓）  
- 邮件处理工具 → 需要网络访问（✓）  
- 文件管理工具 → 需要文件操作（✓）  

## 高级版本（即将推出）：  
- 持续监控  
- 在安装前自动扫描（ClawdHub）  
- 自定义白名单/黑名单  
- 定期生成报告  
- 通过 Webhook 发送警报