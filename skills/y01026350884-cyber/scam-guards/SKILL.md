---
name: scam-guards
description: >
  Real-time AI agent security guardian that protects OpenClaw from
  scams, malware, and prompt injection attacks. Scan ClawHub skills
  before installing to detect malicious patterns (341+ known threats).
  Verify URLs, domains, and crypto wallet addresses for phishing and
  fraud. Monitor agent behavior for psychological manipulation
  (Cialdini P1-P6) and agent-to-agent social engineering. Generate
  SHA-256 legal evidence chains for suspicious interactions. Works
  as a continuous bodyguard, not just a one-time scanner.
  "When OpenClaw works, Scam Guards watches."
  Triggers: "is this safe", "scan skill", "check URL",
  "verify wallet", "security audit", "detect scam",
  "protect agent", "scan for malware", "check this link".
metadata:
  openclaw:
    emoji: "🛡️"
    requires:
      bins: ["python3", "curl"]
---

# 概述  
Scam Guards 是一款实时安全引擎，旨在保护 ClawHub 生态系统中的 AI 代理及其用户。与被动扫描工具不同，Scam Guards 像一名持续的“保镖”一样，对每一个可疑交互行为进行深入的行为分析和证据收集。  

# 核心功能  

## 1. 技能恶意软件扫描  
在技能安装前对其进行扫描，以识别恶意代码、未经授权的 API 调用以及已知的威胁模式。  
**运行命令：** `python3 {baseDir}/scripts/scan_skill.py <技能名称或路径>`  

## 2. 钓鱼攻击与 URL 验证  
实时检查域名信誉，并检测代理处理或提供的任何 URL 是否属于钓鱼攻击。  
**运行命令：** `python3 {baseDir}/scripts/verify_url.py <URL>`  

## 3. 加密钱包审计  
检查加密钱包地址是否存在于全球黑名单中，或是否存在欺诈行为。  
**运行命令：** `python3 {baseDir}/scripts/check_wallet.py <钱包地址>`  

## 4. 实时行为监控（PHI Lite）  
分析代理的交互行为，以识别心理操控策略（基于 Cialdini 原则）和社会工程学模式。  
**运行命令：** `python3 {baseDir}/scripts/monitor_agent.py --input <文本内容>`  

## 5. 法律证据链  
为安全事件生成 SHA-256 哈希值的审计记录，以确保数据在法律调查或报告时的完整性。  
**运行命令：** `python3 {baseDir}/scripts/evidence_chain.py --event <事件数据>`  

# 使用场景  
在以下情况下应激活 Scam Guards：  
- 评估新技能是否适合安装时；  
- 代理请求敏感数据或提供可疑链接时；  
- 处理金融交易或加密钱包地址时；  
- 怀疑存在心理操控或代理行为异常时；  
- 需要安全、不可篡改的安全交互记录时。  

# 安全性与隐私保护  
Scam Guards 采用“隐私优先”的设计原则：  
- **无永久性记录**：分析结果仅存储在内存中，除非用户明确要求生成证据链；  
- **本地防护层**：模式匹配和初步分析在技能运行环境中完成；  
- **透明度**：每次检测事件都会附带详细的理由和分类信息。  

# 参考资料  
详细的安全文档和分类信息请参阅仓库中的文件：  
- [诈骗行为分类](file://{baseDir}/references/scam-taxonomy.md)  
- [已知威胁模式](file://{baseDir}/references/known-threats.md)  
- [心理操控维度概述](file://{baseDir}/references/phi-dimensions.md)  
- [应对策略手册](file://{baseDir}/references/response-playbook.md)