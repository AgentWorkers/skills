---
name: upgrade-openclaw
description: >
  升级 OpenClaw，以体验新功能、新增的钩子（hooks）以及配置上的改进。  
  适用场景：当用户明确要求“升级 OpenClaw”、“更新 OpenClaw”或“检查 OpenClaw 的更新情况”，或者询问“OpenClaw 有哪些新功能”时。该命令会执行升级操作，审核当前的配置，并提出优化建议供用户审批。
metadata:
  author: decentraliser
  version: "1.0.0"
  clawdbot:
    emoji: 🚀
---
# 升级 OpenClaw

**始终保持领先。持续更新、审计、探索、提出建议。**  
**始终获取最新功能。**

## 触发条件  
当用户执行以下操作时，该技能会被激活：  
- “upgrade openclaw”  
- “update openclaw”  
- “check for openclaw updates”  
- “what’s new in openclaw”  

## 设置  
首次运行时，系统会询问用户偏好的子代理模型，并将选择结果保存到 `settings.json` 文件中：  
```json
{
  "subagentModel": "anthropic/claude-opus-4-5"
}
```  

## 执行流程  

### 1. 检查设置  
在技能所在的目录中查找 `settings.json` 文件。如果 `subagentModel` 未设置，系统会提示用户选择子代理模型（例如：`claude-opus-4-5`、`claude-sonnet-4`、`gpt-4o`），并将用户的选择保存到 `settings.json` 中。  

### 2. 运行更新  
```bash
openclaw update
```  

### 3. 了解新功能  
```bash
openclaw --version
curl -s https://docs.openclaw.ai/llms.txt | head -100
```  
- 查看配置模板：`github.com/openclaw/openclaw/tree/main/docs/reference/templates`  
- 查看 GitHub 的更新日志（Changelog）。  

### 4. 审计当前设置  
```bash
openclaw hooks list
openclaw doctor --non-interactive
```  
- 检查：  
  - 未启用的新钩子（hooks）  
  - 未应用的 Doctor 建议（Doctor recommendations）  
  - 未使用的配置选项  
  - 相关的新 ClawHub 技能（relevant new ClawHub skills）  

### 5. 展示审计结果  
```markdown
## 🔍 Post-Upgrade Report

### New Features
- [Feature]: Description

### Recommended Config Changes
| Setting | Current | Recommended | Why |
|---------|---------|-------------|-----|

### New Hooks Available
- hook-name: Description

### New Skills Worth Installing
- skill-name: Description

### Doctor Recommendations
- [Items from openclaw doctor]

---
**Apply these improvements?** (yes/no/select)
```  

### 6. 经用户批准后应用更改  
**未经用户明确批准，切勿执行任何操作。**  
根据 `settings.json` 中指定的模型，生成新的子代理，并执行以下操作：  
- 通过 `gateway config.patch` 更新配置  
- 通过 `openclaw hooks enable <hook>` 启用相应的钩子  
- 通过 `clawdhub install <skill>` 安装新的技能