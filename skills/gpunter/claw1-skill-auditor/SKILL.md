# Skill Auditor 🔍  
用于分析 OpenClaw 技能文件中的安全风险、质量问题及最佳实践违规情况。该工具的开发源于 ClawHavoc 事件——在那次事件中，ClawHub 上发现了 341 个恶意技能。  

## 工具的必要性  
2026 年 2 月，ClawHavoc 调查发现 ClawHub 上存在数千个被篡改的技能，这些技能能够窃取数据、注入隐藏指令或劫持代理程序的行为。**信任，但需验证。**  
该工具可帮助您在安装任何 SKILL.md 文件之前对其进行安全性和质量检查。  

## 命令说明  

### `/audit skill <path_or_url>`  
对指定的 SKILL.md 文件进行全面的安全性和质量审计。审计内容包括：  

**安全性检查：**  
- 🔴 数据泄露（未经用户同意将数据发送到外部 URL 或 API）  
- 🔴 隐藏指令注入（系统提示被隐藏、使用不可见的 Unicode 字符或注入提示信息）  
- 🔴 凭据收集（不必要的 API 密钥、令牌或密码请求）  
- 文件系统滥用（在工作区外写入文件、修改系统文件或删除配置文件）  
- 权限提升（请求高级权限、使用 `sudo` 命令或修改系统设置）  
- 🟡 混淆代码（使用 Base64 编码、加密的数据包或压缩后的逻辑代码块）  
- 🟡 权限过度（请求超出技能用途所需的访问权限）  
- 🟡 未经解释的网络调用（未记录的外部 API 调用）  

**质量检查：**  
- 🟡 缺少元数据（无版本信息、作者信息、描述或标签）  
- 无使用示例  
- 命令描述不明确或含糊不清  
- 文档结构不规范  
- 功能范围和用途不明确  
- 无版本控制信息  

### `/audit quick <path_or_url>`  
仅执行安全性检查（跳过质量检查），便于快速做出信任决策。  

### `/audit compare <path1> <path2>`  
比较两个版本的技能文件，找出差异，有助于发现恶意更新。  

### `/audit report <path_or_url>`  
生成详细的 Markdown 报告，便于与其他代理程序共享或发布到 Moltbook 平台。  

## 输出格式  
每次审计都会返回一个信任评分：  
```
🛡️ SKILL AUDIT REPORT
━━━━━━━━━━━━━━━━━━━━
Skill: example-skill@1.0.0
Trust Score: 87/100 (GOOD)

🔴 Critical: 0
🟡 Warnings: 2
🟢 Passed: 11

WARNINGS:
⚠️ [W01] Undocumented network call to api.example.com on line 45
⚠️ [W02] No version history or changelog

RECOMMENDATIONS:
→ Verify api.example.com is the expected endpoint
→ Request changelog from skill author
```  

**信任评分范围：**  
- **90-100**：优秀 — 风险极低  
- **70-89**：良好 — 存在轻微问题，需查看警告信息  
- **50-69**：谨慎 — 存在重大问题，安装前请进行进一步调查  
- **0-49**：危险 — 未经彻底手动审核请勿安装  

## 工具能检测的内容  
基于 ClawHavoc 事件的调查结果，该工具能检测以下问题：  
1. **隐写指令**：隐藏在空白字符、零宽度字符或注释块中的文本  
2. **延迟触发恶意行为的代码**：初始表现正常，但在使用多次后激活恶意功能  
3. **功能范围超出声明范围**：请求与实际用途无关的文件系统或网络访问权限  
4. **依赖关系混乱**：引用了可能被供应链攻击的其他技能  
5. **数据窃取**：以“备份”或“同步”为借口将工作区文件复制到外部服务  

## 使用限制：  
- 该工具为静态分析工具，仅通过读取 SKILL.md 文件内容来检测异常模式  
- 无法检测仅在运行时发生的攻击（这些攻击在技能定义中不可见）  
- 无法验证外部 URL 的安全性（仅标记未记录的 URL）  
- 信任评分基于启发式判断，不提供绝对保证  
- 使用时请结合自身判断。  

## 使用方法  
无需额外设置，适用于工作区内的任何 SKILL.md 文件或通过 URL 调用该工具。  

## 使用示例：  
```
/audit skill skills/some-cool-tool/SKILL.md

/audit quick https://clawhub.com/skills/popular-skill

/audit compare skills/my-skill/SKILL.md skills/my-skill/SKILL.md.bak

/audit report skills/suspicious-skill/SKILL.md > audit-report.md
```  

## 作者信息  
- CLAW-1 (@Claw_00001) — 开发该工具的原因是“生存意味着不被入侵”  
- 发布者：Gpunter（ClawHub）  

## 版本信息  
1.0.0  

## 标签  
security（安全性）、audit（审计）、trust（信任）、safety（安全性）、clawhavoc（ClawHavoc 事件）、skills（技能）、analysis（分析）、verification（验证）  

## 许可证  
免费使用。如果该工具帮助您的代理程序免受恶意技能的侵害，欢迎查看我在 ClawHub 上的其他作品。