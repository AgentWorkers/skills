---
name: openclaw-skill-scanner
description: >
  **OpenClaw AgentSkills的安全防护机制**  
  在安装过程中，该安全机制会使用 `cisco-ai-defense/skill-scanner` 工具对文件夹中的技能文件以及 ClawHub 中的技能进行扫描。该机制支持手动扫描、分阶段安装，并可通过 `systemd` 系统自动隔离高风险技能文件。
binaries:
  - uv
  - npx
  - git
  - systemctl
env:
  - OPENCLAW_STATE_DIR
  - OPENCLAW_WORKSPACE_DIR
---
# 技能扫描保护机制（Skill Scanner Guard）

**强化 OpenClaw 的技能供应链安全：**
- 使用 `cisco-ai-defense/skill-scanner` 工具扫描技能。
- 仅阻止 **高风险（High）** 或 **关键（Critical）** 等级的技能。
- 允许 **中等风险（Medium）**、**低风险（Low）** 或 **信息提示（Info）** 等级的技能通过，但会发出警告。
- 当 `~/.openclaw/skills` 目录中的技能发生变化时，自动触发扫描。
- 将检测为有问题的技能隔离到 `~/.openclaw/skills-quarantine` 目录中。

## 快速入门

### 安装 skill-scanner（包含仓库和 UV 环境配置）

```bash
cd "$HOME/.openclaw/workspace"
# or wherever you keep repos

git clone https://github.com/cisco-ai-defense/skill-scanner
cd skill-scanner
CC=gcc uv sync --all-extras
```

**注意：** 在使用 `yara-python` 构建工具时，某些环境可能会尝试使用 `gcc-12`；强制设置 `CC=gcc` 可以避免此问题。

## 工作流程

### 1) 手动扫描所有用户的技能

用户的技能文件存储在：
- `~/.openclaw/skills`

**执行命令：**
```bash
$HOME/.openclaw/skills/skill-scanner-guard/scripts/scan_openclaw_skills.sh
```

**扫描结果输出到：**
- `/home/rev/.openclaw/workspace/skill_scans/`

### 2) 通过扫描机制安装文件夹中的技能（使用复制/克隆方式）

**建议使用封装脚本而非直接复制：**
```bash
$HOME/.openclaw/skills/skill-scanner-guard/scripts/scan_and_add_skill.sh /path/to/skill-dir
```

**策略：**
- 仅阻止 **高风险（High）** 或 **关键（Critical）** 等级的技能通过（除非使用 `--force` 参数）。
- 即使只有中等风险（Medium）或低风险（Low）的技能，也会进行安装，但会打印警告信息。

### 3) 从 ClawHub 安装技能（采用分阶段安装方式）

**步骤：**
- 先将技能文件安装到临时目录中，然后进行扫描；
- 仅当扫描结果符合要求时，才将技能文件复制到 `~/.openclaw/skills` 目录中。

### 4) 自动扫描并处理变更（通过 systemd 用户单元实现）

**步骤：**
- 安装相应的 systemd 用户单元（模板文件位于 `references/` 目录中）：
```bash
mkdir -p ~/.config/systemd/user
cp -a "$HOME/.openclaw/skills/skill-scanner-guard/references/openclaw-skill-scan."* ~/.config/systemd/user/

systemctl --user daemon-reload
systemctl --user enable --now openclaw-skill-scan.path
```

**行为：**
- 任何对 `~/.openclaw/skills/` 目录的更改都会触发 `scripts/auto_scan_user_skills.sh` 脚本。
- 如果检测到高风险（High）或关键（Critical）级别的问题，脚本会将有问题的技能文件移动到：
  `~/.openclaw/skills-quarantine/<技能名称>-<时间戳>`
- 扫描结果会记录到：
  `/home/rev/.openclaw/workspace/skill_scans/auto/`

**检查结果：**
```bash
systemctl --user status openclaw-skill-scan.path
journalctl --user -u openclaw-skill-scan.service -n 100 --no-pager
ls -la ~/.openclaw/skills-quarantine
```

## 配置文件及工具包内容

### 工具包中的文件：
- `scan_openclaw_skills.sh`：生成用户技能及系统自带技能的 Markdown 报告。
- `scan_and_add_skill.sh`：扫描指定文件夹中的技能，并仅在符合条件时进行安装。
- `clawhub_scan_install.sh`：从 ClawHub 下载技能文件，进行扫描后进行安装。
- `auto_scan_user_skills.sh`：自动扫描 `~/.openclaw/skills` 目录中的所有变化，并将高风险/关键问题的技能隔离。

### 参考文件：
- `openclaw-skill-scan.path` 和 `openclaw-skill-scan.service`：用于触发 systemd 用户单元的配置文件。