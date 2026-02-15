---
name: ctf-writeup-generator
description: 能够从解决CTF（Capture The Flag）挑战的过程中自动生成专业的报告。这些报告包括标志（flag）的检测结果、挑战的类别划分，以及符合Markdown格式的文档编写。
tags:
  - cybersecurity
  - ctf
  - documentation
  - pentesting
  - writeups
homepage: https://github.com/yourusername/ctf-writeup-generator
---

# CTF报告生成器

## 描述

该工具帮助CTF参与者、安全研究人员和网络安全教育工作者自动从他们的解题过程中生成专业的报告。它能够智能地识别flag的格式，对挑战进行分类，并使用适当的标题来组织报告内容，同时还会包含带有语法高亮的代码块。

**适用场景**：
- 为特定平台（如HackTheBox、TryHackMe、OffSec等）生成报告
- 记录Jeopardy风格的CTF解决方案
- 为培训材料生成教育性内容
- 建立安全研究作品集

## 使用场景

当用户有以下需求时，请使用此工具：
- 请求生成CTF报告
- 表示需要记录自己的CTF解决方案
- 要为某个挑战生成报告
- 提到已完成CTF挑战并需要文档记录
- 希望以专业的方式格式化解题过程
- 需要从笔记中提取并格式化flag

## 功能特点

### Flag格式识别
- 自动识别并验证常见的CTF flag格式：`CTF{...}`、`FLAG{...}`、`flag{...}`  
- 平台特定格式：`HTB{...}`、`THM{...}`、`SHAASTRA{...}`、`picoCTF{...}`  
- 支持针对特定竞赛的自定义正则表达式模式  
- 支持大小写敏感的验证

### 挑战分类
- 根据关键词和使用的工具自动对挑战进行分类：
  - **Web攻击**：SQL注入、XSS、CSRF、身份验证绕过  
  - **二进制攻击**：缓冲区溢出、ROP、格式字符串攻击、堆栈溢出  
  - **逆向工程**：二进制分析、反编译、代码混淆  
  - **密码学**：经典加密算法、现代加密技术、哈希破解  
  - **取证**：隐写术、内存取证、网络分析、磁盘成像  
  - **OSINT**：信息收集、社交媒体分析  
  - **PWN**：漏洞利用、shellcode编写、权限提升  
  - **其他**：混合或独特的挑战类型

### 结构化输出
- 生成格式规范的markdown报告，包含：
  - 挑战元数据（名称、类别、难度、分数）
  - 执行摘要  
  - 逐步解题过程（含代码块）  
  - 使用的工具  
  - Flag提交方式  
  - 关键学习点和收获  
  - 可选：附加资源和参考文献

### 代码格式化
- 为以下语言提供正确的语法高亮：
  - Python、Bash、JavaScript、C/C++  
  - 汇编语言（x86、ARM）  
  - SQL查询  
  - 命令行工具输出  
  - 网络数据包分析

## 使用说明

当用户请求CTF报告时，请按照以下步骤操作：

1. **收集信息**：
   - 询问用户以下内容：
     - 挑战名称  
     - 平台/CTF名称（例如：“HackTheBox”、“Shaastra CTF”）  
     - 分类（或根据描述自动判断）  
     - 难度级别（简单/中等/困难或分数值）  
     - 非标准flag的格式  
     - 解题过程/笔记  

2. **处理内容**：
   - 从用户的描述中提取技术步骤  
   - 识别使用的工具和命令  
   - 识别并验证flag格式  
   - 对挑战进行分类  
   - 逻辑地组织解题流程  

3. **生成报告**：
   使用以下结构创建markdown文档：

   ```markdown
   ```markdown
   # [Challenge Name] - [Platform] CTF Writeup
   
   **Author**: [Author name or handle]  
   **Date**: [Current date]  
   **Category**: [Category]  
   **Difficulty**: [Difficulty]  
   **Points**: [Points if applicable]
   
   ## Summary
   
   [2-3 sentence overview of the challenge and solution approach]
   
   ## Challenge Description
   
   [Original challenge description if provided]
   
   ## Reconnaissance
   
   [Initial enumeration and information gathering]
   
   ## Solution
   
   ### Step 1: [Phase name]
   
   [Detailed explanation with commands/code]
   
   ```bash
   # 使用的命令
   ```
   
   ### Step 2: [Next phase]
   
   [Continue with logical progression]
   
   ## Tools Used
   
   - Tool 1: Purpose
   - Tool 2: Purpose
   
   ## Flag
   
   ```
   FLAG{...}
   ```
   
   ## Key Takeaways
   
   - Learning point 1
   - Learning point 2
   
   ## References
   
   - [Relevant links]
   ```
   ```

4. **验证和优化**：
   - 检查flag格式是否与平台匹配  
   - 确保代码块具有正确的语法高亮  
   - 为复杂的命令添加解释性注释  
   - 如果有替代方法，也一并包含  

5. **保存报告**：
   将生成的报告保存为名为`[platform]_[challenge-name]_writeup.md`的markdown文件

## 使用示例

**用户**：“我刚刚解决了Shaastra CTF中的‘Binary Bash’挑战。这是一个缓冲区溢出问题，我需要覆盖返回地址。flag的格式是Shaastra{buff3r_0v3rfl0w_m4st3r}。你能生成一份报告吗？”

**工具响应**：
1. 询问更多详细信息（使用的工具、具体的攻击步骤）
2. 生成一份专业报告，内容包括：
   - 正确的挑战元数据  
   - 二进制攻击的分类  
   - 逐步解释缓冲区溢出过程  
   - 包含汇编/C语言代码的代码块  
   - 使用的GDB命令  
   - 格式正确的flag  
   - 关于内存安全的关键学习点

## 平台特定模板

- **HackTheBox**：
  - 包含机器IP、操作系统和难度等级  
  - 添加用户/root flag的相关内容  
  - 如果复杂，添加攻击路径图  

- **OffSec/OSCP**：
  - 重点记录枚举方法  
  - 记录权限提升的步骤  
  - 包含证明截图的参考  

- **Jeopardy CTF**：
  - 列出分数值和解题时间  
  - 如果适用，包括团队策略  
  - 按挑战类型分类

## 高级功能

- **多工具集成**：
  - 针对特定任务引用其他工具：
    - `ghidra-skill`用于逆向工程分析  
    - `burpsuite-skill`用于Web攻击  
    - `volatility-skill`用于内存取证  

- **报告模板**：
  - 支持不同的报告风格：
    - **学术型**：包含详细的理论背景  
    **速通型**：仅包含必要步骤  
    **教程型**：适合初学者的详细解释  
    **作品集型**：适合求职申请的专业格式  

- **输出格式**：
  - 标准Markdown (.md)  
  - 通过pandoc生成PDF  
  - 带有自定义CSS的HTML  
  - 平台特定格式（如HTB Academy、Medium、dev.to）

## 安全注意事项

- **不要包含实际凭证或敏感的API密钥**  
- 对可能泄露系统信息的路径进行清理  
- 遵守比赛规则（在活动CTF期间不要发布报告）  
- 对近期挑战添加剧透警告  
- 确认平台允许分享flag

## 配置

用户可以通过环境变量进行自定义：

```bash
# Set default author name
export CTF_AUTHOR="akm626"

# Set default CTF platform
export CTF_PLATFORM="HackTheBox"

# Set preferred writeup style
export CTF_WRITEUP_STYLE="tutorial"

# Enable automatic screenshot embedding
export CTF_AUTO_SCREENSHOTS=true
```

## 依赖项

- 基本的markdown处理器（内置）  
- 可选：pandoc（用于PDF导出）  
- 可选：pygments（用于增强语法高亮）

## 提高报告质量的建议

1. 提供详细的解题笔记——背景信息越详细越好  
2. 在相关情况下包含命令输出  
3. 提及遇到的死胡同及失败原因（这些是宝贵的学习内容）  
4. 引用CVE和工具文档  
5. 添加自己的独特见解和方法  
6. 保持flag格式与平台一致

## 报告示例结构

**Web攻击挑战示例：**

```markdown
```markdown
# SQL Injection Master - Shaastra CTF 2026

**Author**: akm626  
**Date**: February 08, 2026  
**Category**: Web Exploitation  
**Difficulty**: Medium  
**Points**: 300

## Summary

This challenge involved exploiting a SQL injection vulnerability in a login form to extract database contents and retrieve the flag. The application used client-side filtering which was easily bypassed.

## Challenge Description

[Original description...]

## Reconnaissance

Initial enumeration revealed a PHP-based login portal running on Apache. Basic directory fuzzing found:

```bash
ffuf -w common.txt -u http://target.com/FUZZ

admin/
backup/
config/
```

## Solution

### Step 1: Identifying the Injection Point

Testing the login form with basic SQL injection payloads:

```sql
' OR '1'='1' --
admin' --
' UNION SELECT NULL--
```

### Step 2: Database Enumeration

Used SQLMap to automate extraction:

```bash
sqlmap -u "http://target.com/login.php" --data="username=admin&password=test" \
       --technique=U --dump --batch
```

[Continue with detailed steps...]

## Flag

```
SHAASTRA{sql_inj3ct10n_pr0}
```

## Key Takeaways

- Always test for SQL injection on input fields
- Client-side validation is not security
- Parameterized queries prevent SQL injection

## Tools Used

- **Burp Suite**: Request interception
- **SQLMap**: Automated SQL injection
- **ffuf**: Directory fuzzing

## References

- [OWASP SQL Injection Guide](https://owasp.org/...)
- [SQLMap Documentation](https://sqlmap.org/)
```
```

## 贡献方式

用户可以通过以下方式改进此工具：
- 添加新的flag格式模式  
- 贡献平台特定模板  
- 优化分类逻辑  
- 分享示例报告

## 许可证

MIT许可证——免费使用和修改

## 支持

如有问题或建议，请联系工具维护者，或在GitHub仓库中提交问题。