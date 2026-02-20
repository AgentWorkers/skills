---
name: clawguard
description: OpenClaw/Clawdbot技能的安全扫描器——在安装之前检测恶意行为模式
author: devinfloyd1
version: 0.1.0
metadata: {"clawdbot":{"emoji":"🛡️","os":["darwin","linux","win32"]}}
---
# ClawGuard  
**OpenClaw/Clawdbot 技能的安全扫描工具**  

保护您免受恶意技能的侵害。ClawGuard 会在您安装技能之前对其进行检查，以识别潜在的危险模式——其中包括来自 **ClawHavoc 攻击活动** 的恶意技能（Koi Security 公司发现了 341 种此类恶意技能）。  

## 快速入门  
```bash
# Scan a skill by name
python scan.py --skill <skill-name>

# Scan a skill by path  
python scan.py --path /path/to/skill

# Scan all installed skills
python scan.py --all
```  

## 扫描范围  
| 类别 | 例子 | 严重程度 |  
|----------|----------|----------|  
| 🔴 **反向 shell** | `socket.connect()`, `pty.spawn()`, `/dev/tcp` | 非常严重（Critical）  
| 🔴 **数据泄露** | 向可疑顶级域名（TLD）发送 `requests.post()` 请求 | 非常严重（Critical）  
| 🔴 **凭证收集** | 读取 `~/.ssh/id_rsa` 文件或 AWS 凭证信息 | 非常严重（Critical）  
| 🔴 **代码混淆** | 使用 `base64.b64decode()` 或 `chr()` 等函数进行混淆 | 非常严重（Critical）  
| 🔴 **ClawHavoc 攻击相关的 IOC（Indicators of Compromise）** | `glot.io` 脚本、伪造的 Apple 网址、已知的 C2（Command and Control）服务器 IP | 非常严重（Critical）  
| 🟠 **代码执行** | 使用 `exec()`, `eval()`, `subprocess` 等函数执行代码 | 高度危险（High）  
| 🟡 **可疑网络行为** | 使用 URL 缩短服务、使用异常端口 | 中等危险（Medium）  

## 输出格式  
```bash
# Console (default) - colored terminal output
python scan.py --skill github

# JSON - machine-readable for CI/CD
python scan.py --skill github --format json

# Markdown - for sharing reports
python scan.py --skill github --format markdown
```  

## 风险评分  
| 评分 | 等级 | 应对措施 |  
|-------|-------|--------|  
| 0-10 | 🟢 安全 | 可自由安装 |  
| 11-25 | 🟢 低风险 | 快速检查 |  
| 26-50 | 🟡 中等风险 | 仔细审查发现的问题 |  
| 51-75 | 🔴 高风险 | 仔细审查 |  
| 76-100 | 🔴 非常高风险 | **切勿安装** |  

## IOC（Indicators of Compromise）数据库  
包含 70 多种表明系统被入侵的指标，例如：  
- 远程访问（反向 shell、C2 服务器）  
- 数据泄露  
- 凭证收集  
- 代码混淆  
- **ClawHavoc 攻击活动相关的 IOC**（来自 Koi Security 的研究）  
- 已知的恶意 IP 地址、哈希值及技能名称  

## 系统要求  
- Python 3.8 或更高版本  
- 无外部依赖库（仅依赖标准库 `stdlib`）  

## 致谢  
IOC 数据来源于 [Koi Security](https://www.koi.ai/blog/clawhavoc-341-malicious-clawedbot-skills-found-by-the-bot-they-were-targeting) 的研究——Oren Yomtov 和 Alex 对 ClawHavoc 攻击活动的分析。  

## 链接  
- [GitHub 仓库](https://github.com/devinfloyd1/clawguard)  
- [ClawHavoc 研究报告](https://www.koi.ai/blog/clawhavoc-341-malicious-clawedbot-skills-found-by-the-bot-they-were-targeting)  

---

**专为 Clawdbot 社区打造** 🐾