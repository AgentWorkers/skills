---
name: upgrade-openclaw
description: >
  升级 OpenClaw，以体验新的功能、钩子（hooks）以及配置上的改进。  
  适用场景：当用户明确要求“升级 OpenClaw”、“更新 OpenClaw”或“检查 OpenClaw 的更新”时。该脚本会执行升级操作，审核当前的配置设置，并提出优化建议供用户审批。
metadata:
  {
    "openclaw":
      {
        "emoji": "🚀",
        "author": "decentraliser",
        "requires": { "bins": ["openclaw", "curl", "clawhub"] }
      }
  }
---
# 升级 OpenClaw

**保持领先。持续更新、审计、探索、提出建议。始终拥有最新功能。**

## 触发条件

当用户执行以下操作时，此技能将被激活：
- “upgrade openclaw”
- “update openclaw”
- “check for openclaw updates”
- “what’s new in openclaw”

## 设置

在首次运行时，系统会询问用户偏好的子代理模型，并将选择保存到 `settings.json` 文件中：

```json
{
  "subagentModel": "anthropic/claude-sonnet-4-6"
}
```

> ⚠️ **隐私声明：** 如果您选择外部提供商（例如 `gpt-4o`、`claude-*`），在升级过程中，您的本地 OpenClaw 配置和环境信息将会被发送给该提供商。
> 建议选择本地托管的模型或您信任的主要提供商。

## 执行步骤

### 1. 检查设置

在技能目录中查找 `settings.json` 文件。如果 `subagentModel` 未设置，系统会提示用户选择：
> “选择用于升级的子代理模型？（例如：`claude-sonnet-4-6`、`deepseek-chat`）。请注意：外部提供商将会接收您的配置数据。”

将用户的选择保存到 `settings.json` 文件中。

### 2. 检查前提条件

在继续之前，验证所需的二进制文件是否已经安装：

```bash
which openclaw && openclaw --version
which curl
which clawhub && clawhub -V
```

如果发现缺少任何文件，系统会中止升级过程并提示用户安装这些文件。

### 3. 运行升级操作

```bash
openclaw update
```

### 4. 了解新功能

```bash
openclaw --version
curl -s https://docs.openclaw.ai/llms.txt | head -100
```

- 查看配置模板：`github.com/openclaw/openclaw/tree/main/docs/reference/templates`
- 查看 GitHub 上的更新日志（Changelog）

### 5. 审计当前设置

检查以下内容：
- 未启用的新钩子（hooks）
- 未应用的 Doctor 建议
- 未使用的配置选项
- 新发布的 ClawHub 技能

### 6. 展示审计结果

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

### 7. 经用户确认后应用更改

**未经用户明确同意，切勿应用任何更改。**

等待用户回复“yes”、“apply”或选择具体要应用的更改。对于含糊不清的输入，不要继续执行操作。

使用 `settings.json` 中指定的模型创建子代理，并执行以下操作：
- 通过 `gateway config.patch` 更新配置
- 通过 `openclaw hooks enable <hook>` 启用相应的钩子
- 通过 `clawhub install <skill>` 安装新的技能