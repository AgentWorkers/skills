---
name: skill-scanner-guard
license: MIT
description: 使用 `cisco-ai-defense/skill-scanner` 为 OpenClaw AgentSkills 添加安全防护机制。该机制适用于以下场景：  
- 在设置或运行技能扫描时（针对路径 `~/.openclaw/skills`）；  
- 为新技能文件夹配置自动扫描/隔离功能；  
- 在安装 ClawHub 之前执行扫描；  
- 生成扫描报告（格式包括 Markdown、JSON 或 SARIF）；  
- 调整安全策略的阈值（例如：将规则设置为“高/严重”级别，允许“中等”级别但触发警告）。
---

# 技能扫描保护机制（Skill Scanner Guard）

**强化 OpenClaw 的技能供应链安全：**
- 使用 `cisco-ai-defense/skill-scanner` 工具扫描技能。
- 仅阻止 **高风险（High）** 或 **关键（Critical）** 等级的技能。
- 允许 **中等（Medium）**、**低风险（Low）** 或 **信息（Info）** 等级的技能通过，但会发出警告。
- 每当 `~/.openclaw/skills` 目录中的技能发生变化时，系统会自动触发扫描。
- 失败的技能会被隔离到 `~/.openclaw/skills-quarantine` 目录中。

## 快速入门

### 安装 skill-scanner（包含仓库和 UV 环境配置）

```bash
cd "$HOME/.openclaw/workspace"
# or wherever you keep repos

git clone https://github.com/cisco-ai-defense/skill-scanner
cd skill-scanner
CC=gcc uv sync --all-extras
```

**注意：** 在使用 `yara-python` 构建工具时，某些环境可能会尝试使用 `gcc-12`；强制设置 `CC=gcc` 可以避免这个问题。

## 工作流程

### 1) 手动扫描所有用户的技能

用户的技能文件存储在：
- `~/.openclaw/skills`

执行命令：
```bash
$HOME/.openclaw/skills/skill-scanner-guard/scripts/scan_openclaw_skills.sh
```

扫描结果会保存在：
- `/home/rev/.openclaw/workspace/skill_scans/`

### 2) 通过扫描机制安装文件夹中的技能（复制/克隆流程）

建议使用封装脚本而非直接复制文件：
```bash
$HOME/.openclaw/skills/skill-scanner-guard/scripts/scan_and_add_skill.sh /path/to/skill-dir
```

**规则：**
- 仅阻止高风险（High）或关键（Critical）等级的技能通过（除非使用 `--force` 参数）。
- 即使只有中等（Medium）或低风险（Low）等级的技能，系统也会进行安装，并会打印警告信息。

### 3) 通过 ClawHub 安装技能（分阶段安装流程）

首先将技能文件安装到临时目录，然后进行扫描；只有通过扫描的技能才会被复制到 `~/.openclaw/skills` 目录中：
```bash
$HOME/.openclaw/skills/skill-scanner-guard/scripts/clawhub_scan_install.sh <slug>
# optionally
$HOME/.openclaw/skills/skill-scanner-guard/scripts/clawhub_scan_install.sh <slug> --version <version>
```

### 4) 自动扫描并在技能发生变化时进行隔离（使用 systemd 用户单元）

相关脚本模板位于 `references/` 目录中：
```bash
mkdir -p ~/.config/systemd/user
cp -a "$HOME/.openclaw/skills/skill-scanner-guard/references/openclaw-skill-scan."* ~/.config/systemd/user/

systemctl --user daemon-reload
systemctl --user enable --now openclaw-skill-scan.path
```

**行为：**
- 任何对 `~/.openclaw/skills/` 目录的修改都会触发 `scripts/auto_scan_user_skills.sh` 脚本的执行。
- 如果检测到高风险（High）或关键（Critical）等级的技能问题，该脚本会将问题技能文件移动到：
  `~/.openclaw/skills-quarantine/<技能名称>-<时间戳>`
- 报告文件会被保存在：
  `/home/rev/.openclaw/workspace/skill_scans/auto/`

### 相关资源

### scripts/ 目录：
- `scan_openclaw_skills.sh`：生成用户技能和捆绑技能的 Markdown 报告。
- `scan_and_add_skill.sh`：扫描指定文件夹中的技能，并仅在允许的情况下进行安装。
- `clawhub_scan_install.sh`：从 ClawHub 下载技能文件，进行扫描后进行安装。
- `auto_scan_user_skills.sh`：自动扫描 `~/.openclaw/skills` 目录中的所有变化，并隔离高风险/关键等级的技能问题。

### references/ 目录：
- `openclaw-skill-scan.path` 和 `openclaw-skill-scan.service`：用于触发 systemd 用户单元的配置文件。