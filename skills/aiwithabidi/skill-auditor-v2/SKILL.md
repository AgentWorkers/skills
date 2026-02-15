---
name: skill-auditor
version: 2.0.0
description: >
  Security scanner for OpenClaw skills. Detects malicious code, obfuscated payloads,
  prompt injection, social engineering, typosquatting, and data exfiltration before
  installation. Features 0-100 numeric risk scoring, MITRE ATT&CK mappings, base64/hex
  deobfuscation, IoC database, whitelist system, and SHA256 file inventory. Use before
  installing any third-party skill. Triggers: audit skill, check security, scan skill,
  is this skill safe, security review, quarantine.
license: MIT
compatibility:
  openclaw: ">=0.10"
metadata:
  openclaw:
    requires:
      bins: ["python3"]
---

# Skill Auditor v2.0 🔍🛡️  
一款专为 OpenClaw/ClawHub 技能设计的全面安全扫描工具，将静态分析、反混淆技术和威胁情报整合到一个 Python 工具中。  

## 使用场景  
- 在从 ClawHub 安装任何第三方技能之前  
- 在审查技能更新时，检查是否存在安全漏洞  
- 在发布自己的技能之前进行安全审计  
- 当有人询问“这个技能安全吗？”或要求进行安全审计时  

## 快速入门  
### 审计本地技能目录  
```bash
python3 {baseDir}/scripts/audit_skill.py /path/to/skill --human
```  

### 按技能名称（slug）审计 ClawHub 中的技能  
```bash
python3 {baseDir}/scripts/audit_skill.py --slug skill-name --human
```  

### 隔离流程（包含审计提示及安装建议）  
```bash
bash {baseDir}/scripts/quarantine.sh /path/to/skill
bash {baseDir}/scripts/quarantine.sh --slug skill-name
```  

### 用于程序化处理的 JSON 输出  
```bash
python3 {baseDir}/scripts/audit_skill.py /path/to/skill --json
```  

## 评分系统  
| 分数 | 等级 | 处理建议 |  
|-------|-------|--------|  
| 0–20 | ✅ 安全 | 可自动安装 |  
| 21–40 | 🟢 低风险 | 请谨慎使用 |  
| 41–60 | 🟡 中等风险 | 需要人工审核 |  
| 61–80 | 🟠 高风险 | 需要专家评估 |  
| 81–100 | 🔴 极高风险 | 绝对不要安装 |  

**退出代码说明**：  
`0` = 安全（分数 ≤ 20）  
`1` = 需要审核（分数 21–60）  
`2` = 危险（分数 > 60）  

## 检测层次  
### 第一层：静态模式分析  
- 使用正则表达式进行 10 多种扫描  
- 检查 shell 命令执行、网络请求、文件系统访问、文件系统逃逸行为  
- 检测提示注入、数据泄露、加密钱包访问  
- 检测动态导入、浏览器凭证窃取、虚假依赖项  

### 第二层：反混淆  
- 提取并解码 Base64 字符串，重新扫描解码后的内容  
- 解码十六进制转义序列，再次进行扫描  
- 发现隐藏命令或编码载荷中的 C2（命令与控制）IP  

### 第三层：威胁情报  
- 利用 IoC（Indicators of Compromise）数据库识别已知恶意 IP 和域名  
- 检测社会工程学攻击（如虚假授权、恐吓策略）  
- 为每个检测结果关联 MITRE ATT&CK 分类  
- 安全的二进制文件/域名会降低评分  

### 其他检查  
- 使用 SHA256 校验文件完整性  
- 检测包名中的拼写错误（通过莱文斯坦距离算法）  
- 检查 SKILL.md 文件中是否存在零宽度字符  
- 降低评论中安全漏洞的评分（评论中的问题会被降级处理）  
- 分析权限范围（该技能需要使用哪些工具）  

## IoC 数据库  
威胁信息存储在 `references/ioc-database.json` 文件中。新威胁出现时会自动更新该文件。扫描器在运行时自动加载该文件。  

## 参考资料  
- `references/ioc-database.json` — 结构化的威胁数据（IP、域名、模式）  
- `references/known-patterns.md` — 人类可读的威胁文档  
- `references/prompt-injection-patterns.md` — 提示注入模式参考  

## 开发者信息  
由 [M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) 和 [agxntsix.ai](https://www.agxntsix.ai) 开发  
[YouTube](https://youtube.com/@aiwithabidi) | [GitHub](https://github.com/aiwithabidi)  
该工具是 **AgxntSix Skill Suite** 的一部分，专为 OpenClaw 代理设计。  

📅 **需要帮助为您的企业配置 OpenClaw 吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)  

本工具基于 [skill-auditor-pro](https://clawhub.ai/skills/skill-auditor-pro)（由 sypsyp97 开发）和 [skill-security-auditor](https://clawhub.ai/skills/skill-security-auditor)（由 akm626 开发）合并而成。