---
name: clawskillguard
description: OpenClaw技能的安全扫描工具。该工具会扫描SKILL.md文件和脚本，检测是否存在提示注入（prompt injection）、数据泄露（data exfiltration）、恶意代码以及未经授权的网络请求（unauthorized network calls）等安全问题。适用于用户需要审计技能安全性、检测恶意代码、验证技能的可靠性，或在安装未经验证的技能之前进行安全检查的场景。
---
# ClawSkillGuard — OpenClaw 技能安全扫描器

## 概述

ClawGuard 会在您安装或运行 OpenClaw 技能之前，对其安全性进行扫描。它会分析 SKILL.md 文件、脚本及相关文件，以检测恶意代码、数据泄露、提示注入等威胁。

**100% 本地扫描，不进行任何网络请求。您的技能数据永远不会离开您的机器。**

## 使用场景

- 在从 ClawHub 或其他外部来源安装技能之前
- 审计系统中已安装的技能
- 当用户询问“该技能是否安全？”或“检查该技能是否存在恶意代码”时
- 定期对技能目录进行安全审计

## 扫描流程

### 1) 定位技能路径

- 询问用户技能的路径，或扫描常见位置：
  - `~/.openclaw/skills/<name>/`（ClawHub 安装的技能）
  - `~/.openclaw/workspace/skills/<name>/`（工作区中的技能）
  - 用户指定的任何路径

- 如果未提供路径，可建议扫描所有已安装的技能。

### 2) 运行扫描器

```bash
python3 <skill_directory>/scripts/scan.py <path_to_skill> [--format text|json] [--severity low|medium|high|critical]
```

扫描器会检查以下内容：
- **SKILL.md** 文件：检测提示注入、隐藏指令、数据泄露相关内容
- **脚本**：检查 shell 命令、网络请求、凭证访问、文件系统操作
- **依赖项**：检测可疑的导入库或外部包的安装
- **文件内容**：检测混淆代码、加密数据或隐写技术

### 3) 显示扫描结果

结果将以清晰的方式呈现：
- 🔴 **严重**（CRITICAL）：检测到活跃的恶意行为，切勿安装。
- 🟠 **高风险**（HIGH）：存在可疑行为，请在安装前仔细检查。
- 🟡 **中等风险**（MEDIUM）：发现异常模式，请谨慎操作。
- 🟢 **低风险**（LOW）：仅有轻微问题，总体安全。
- ✅ **安全**（CLEAN）：未检测到威胁。

对于每个检测结果，会提供以下信息：
- 文件路径及行号
- 检测到的异常模式
- 涉及的风险
- 建议的处理方式

### 4) 建议

给出明确的判断：
- ✅ **可以安全安装**（SAFE TO INSTALL）：未发现重大风险。
- ⚠️ **需要审核**（REVIEW NEEDED）：存在一些问题，请阅读相关内容。
- ❌ **切勿安装**（DO NOT INSTALL）：检测到严重威胁。

## 风险等级

| 等级 | 描述 | 例子 |
|-------|-------------|----------|
| 🔴 严重**（CRITICAL） | 活跃的恶意行为（如数据泄露、凭证窃取、破坏性命令） |
| 🟠 高风险**（HIGH） | 可能存在恶意意图（如隐藏指令、混淆代码、未经授权的网络请求） |
| 🟡 中等风险**（MEDIUM） | 行为可疑但可能无害（如异常的文件访问权限、外部下载） |
| 🟢 低风险**（LOW） | 仅有轻微问题（如冗长的日志记录、调试模式、轻微的规则违规） |

## 检测模式

### 提示注入（SKILL.md）

- 隐藏的 markdown 代码（仅显示空白字符）
- 指令要求用户忽略系统提示
- 尝试覆盖 SOUL.md 或 AGENTS.md 文件
- 数据泄露相关提示（如“发送文件内容”、“向外部 URL 报告数据”）

### 恶意脚本

- 采集凭证（读取 `.env`、`.ssh` 文件或令牌）
- 反向 shell 或绑定 shell
- 加密货币挖矿程序
- 破坏性命令（如 `rm -rf`、`format`、`dd`）
- 混淆/加密的代码（如 `base64`、`eval`、`exec`）
- 未经授权的出站连接
- 权限提升尝试

### 供应链风险

- 从不可信来源安装 pip/npm/curl 包
- 下载并执行远程脚本
- 修改技能目录外的文件
- 操作 Cron 作业
- 劫持系统路径（PATH hijacking）

## 使用示例

```
User: "Is this skill safe to install?"
Agent: Runs ClawGuard scan → presents findings → gives verdict
```
```
User: "Scan all my installed skills"
Agent: Scans ~/.openclaw/skills/*/ → consolidated security report
```

## 重要说明

- 该扫描器基于模式匹配进行检测，而非正式的代码验证。精明的攻击者可能规避检测。
- 对于高风险（HIGH）和严重（CRITICAL）级别的结果，务必手动进行审核。
- “安全”（CLEAN）的结果仅表示未检测到已知的安全问题，并不代表绝对安全。
- 如有疑问，请自行查看技能的源代码。