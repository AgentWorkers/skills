---
name: upgrade-openclaw
description: >
  **升级 OpenClaw：全面发现新功能、配置选项、钩子（hooks）及改进之处**  
  **适用场景：** 当用户请求“升级 OpenClaw”、“更新 OpenClaw”、“检查 OpenClaw 的更新内容”或询问“OpenClaw 的新功能”时使用。  
  **操作流程：**  
  1. 执行升级操作；  
  2. 将更新日志（changelog）与已启用的通道/插件（channels/plugins）进行对比；  
  3. 分析配置模式（config schema）的差异；  
  4. 审查现有的钩子（hooks）及系统提供的优化建议（doctor recommendations）；  
  5. 在正式应用升级之前，将所有检测结果呈现给用户以获取确认。
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

更新、对比差异、审核变更内容并提出相应的操作建议。确保没有遗漏任何新功能。

## 设置

首次运行时，请检查该技能目录下的 `settings.json` 文件。如果 `subagentModel` 未被设置，请询问：

> “要升级哪些子代理模型？（例如：`claude-sonnet-4-6`、`deepseek-chat`）。注意：外部提供者将会收到配置数据。”

将设置保存到 `settings.json` 文件中：
```json
{ "subagentModel": "anthropic/claude-sonnet-4-6" }
```

## 操作步骤

### 1. 记录升级前的状态

在开始任何操作之前，请先记录当前的状态：
```bash
PRE_VERSION=$(openclaw --version | grep -oP '\d{4}\.\d+\.\d+')
echo "$PRE_VERSION"
```

保存 `PRE_VERSION` — 这个版本号用于在步骤 3 中生成变更日志的差异对比。

### 2. 运行更新

```bash
openclaw update
```

如果工作目录中的代码有未提交的更改，请先使用 `git stash` 存储这些更改：
```bash
cd "$(openclaw --version 2>&1 | grep -oP '(?<=\().*?(?=\))' || echo ~/openclaw)" 
git stash --include-untracked -m "pre-update stash" && openclaw update
```

记录新版本号：
```bash
POST_VERSION=$(openclaw --version | grep -oP '\d{4}\.\d+\.\d+')
```

如果 `PRE_VERSION` 等于 `POST_VERSION`，则显示 “已更新” 并直接跳到步骤 5（仅进行审核）。

### 3. 提取变更日志中的差异内容

更新后，变更日志会保存在本地 `~/openclaw/CHANGELOG.md` 文件中。版本号由 `## YYYY.x.x` 标签分隔。

从变更日志中提取新旧版本之间的差异内容：
```bash
awk "/^## $POST_VERSION/,/^## $PRE_VERSION/" ~/openclaw/CHANGELOG.md
```

然后根据当前配置环境对这些差异内容进行 **筛选**：

1. 通过 `gateway config.get` 获取当前启用的频道/插件列表。
2. 从变更日志中保留以下内容的条目：
   - 已启用的频道（例如：Telegram、Discord、Feishu 等，除非这些频道被禁用）。
   - 与核心代理、网关、定时任务、工具、内存或安全相关的更改（始终重要）。
   - 如果启用了 ACP（Agent Configuration Protocol），则保留与 ACP、会话或子代理相关的更改。
   - 会导致系统故障的更改（始终重要）。
3. **忽略** 与已禁用的频道、iOS/macOS 应用程序或未使用的平台相关的更改。
4. 将保留的条目分类为：功能更新、修复问题、安全改进或会导致系统故障的更改。

### 4. 配置模式差异分析

获取当前的配置模式和最新的配置信息：

- 配置模式：`gateway config.schema`
- 当前配置：`gateway config.get`

系统地对比两者：

1. 递归地遍历配置模式的属性结构。
2. 检查每个配置键路径是否存在于当前配置中。
3. **新增或被移除的选项**：指的是配置模式中存在但在当前配置中不存在的键（默认值合理的键除外）。
4. 重点关注那些设置非默认值后能带来实际效果的字段。
5. 将变更日志中新增的字段标记为 “本版本的新功能”。

将对比结果以表格形式呈现：
```
| Config Path | Type | Default | Description | New? |
```

### 5. 审核当前配置环境

```bash
openclaw hooks list --json
openclaw doctor --non-interactive
clawhub update --all --dry-run 2>&1
```

收集以下信息：
- **可用的钩子（hooks）**：所有可用但未被启用的钩子。
- **系统诊断工具（Doctor）**：所有生成的警告和建议。
- **ClawHub 的更新内容**：所有可用的更新信息。

### 6. 提交综合报告

报告的结构应如下所示：
```markdown
## 🔍 Post-Upgrade Report: {PRE_VERSION} → {POST_VERSION}

### 🆕 New Features (Relevant to Your Setup)
- [Feature]: What it does, why it matters for you
  - Config: `path.to.setting` (if applicable)

### 🔧 Notable Fixes
- [Fix]: What was broken, now fixed

### 🔐 Security Updates
- [Security]: What was patched

### ⚠️ Breaking Changes
- [Breaking]: What changed, migration needed

### 📋 New Config Options Available
| Config Path | Type | Default | Why Enable |
|-------------|------|---------|------------|

### 🪝 Hooks Status
- [hook]: enabled/available/new

### 🏥 Doctor Recommendations
- [Item]: severity + action

### 📦 Skill Updates Available
- [skill]: current → available version

---
**Apply these improvements?** Reply with:
- "yes" / "all" — apply everything
- "select" — I'll list numbered items to pick from
- specific items by name
```

**重要提示**：请不要提交内容过于简略的报告。所有通过步骤 3 的筛选的变更日志条目都必须包含在内；步骤 4 中新增的配置选项也必须全部列出；步骤 5 中发现的任何问题也必须被反映出来。用户触发此技能的目的是为了全面了解所有变更情况。

### 7. 经过用户批准后应用更改

**未经用户明确批准，切勿应用任何更改。**

获得批准后，通过以下方式应用更改：
- 配置更改：`gateway config.patch`
- 启用钩子：`openclaw hooks enable <hook>`
- 安装技能：`clawhub install <skill>`

应用更改后，请恢复之前使用 `git stash` 保存的未提交更改：
```bash
cd ~/openclaw && git stash list | grep -q "pre-update stash" && git stash pop
```

### 8. 保存状态

将升级后的状态信息写入该技能目录下的 `state.json` 文件中：
```json
{
  "lastUpgrade": {
    "from": "2026.3.2",
    "to": "2026.3.3",
    "timestamp": "2026-03-05T06:50:00Z",
    "featuresProposed": ["telegram-streaming", "pdf-tool", ...],
    "featuresApplied": ["telegram-streaming", ...],
    "doctorApplied": ["entrypoint-fix", ...]
  }
}
```

这样可以避免在重复运行时重复提出相同的升级请求，并方便用户查询 “自上次升级以来发生了哪些变化”。