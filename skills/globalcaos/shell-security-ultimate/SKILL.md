---
name: shell-security-ultimate
version: 1.0.2
description: AI代理的Shell命令安全、执行风险分类及审计功能：根据命令的风险等级（从“安全”到“危急”）对命令进行分类，确保操作的透明度，并防止危险操作的发生。该系统包含相应的执行脚本以及代理集成方案。
homepage: https://github.com/globalcaos/clawdbot-moltbot-openclaw
repository: https://github.com/globalcaos/clawdbot-moltbot-openclaw
---

# Shell Security Ultimate

为AI代理提供以安全为先的命令执行机制，对每个shell命令进行分类、审计和控制。

---

## 问题所在

拥有shell访问权限的AI代理可以：
- 运行破坏性命令（如 `rm -rf /`）
- 泄露敏感数据（如 `cat ~/.ssh/id_rsa`）
- 在未经监督的情况下修改系统状态
- 在不说明原因的情况下执行命令

**本技能通过强制实施命令的安全分类、透明性和可审计性来解决这些问题。**

---

## 代码控制与提示控制

有两种方式可以控制代理的行为：

| 方法 | 实施方式 | 可靠性 | 示例 |
|----------|-------------|-------------|---------|
| **提示控制** | 通过MD文件中的指令 | 约80% | 在 `SOUL.md` 中提示“不要运行危险命令” |
| **代码控制** | 通过实际代码或钩子 | 约100% | 插件会在执行前阻止 `rm -rf` 命令 |

### 为什么这很重要

- **提示控制的效果会减弱** — 代理在长时间运行过程中可能会忘记指令
- **代码控制的效果更持久** — 代码不会被遗忘，也无法通过口头劝说改变规则
- **深度防御** — 应同时使用提示进行引导和代码进行强制执行

### 该技能的当前状态

| 组件 | 类型 | 状态 |
|-----------|------|--------|
| 分类指南 | 提示控制 | ✅ 已包含在 `SKILL.md` 中 |
| 显示脚本 | 代码控制 | ✅ `scripts/cmd_display.py` 已编写 |
| 与 `SOUL.md` 的集成 | 提示控制 | ✅ 提供了模板 |
| OpenClaw插件钩子 | 代码控制 | ❌ 尚未实现 — 需要 `before_tool_call` 钩子 |
| 命令拦截功能 | 代码控制 | ❌ 计划中 — 将阻止符合特定模式的命令 |

**现状**：采用混合控制方式。显示脚本提供了结构，但真正的强制执行（在执行前阻止危险命令）需要依赖OpenClaw插件。当前实现依赖于代理自行选择是否使用这些安全机制。

**未来目标**：通过插件完全实现代码控制，拦截 `exec` 工具调用并在执行前应用安全策略。

---

## 安全级别

| 级别 | 表情符号 | 风险 | 示例 |
|-------|-------|------|----------|
| 🟢 安全 | 无 | `ls`, `cat`, `git status`, `pwd` |
| 🔵 低风险 | 可逆操作 | `touch`, `mkdir`, `git commit` |
| 🟡 中等风险 | 中等风险 | `npm install`, `git push`, 配置文件修改 |
| 🟠 高风险 | 高风险操作 | `sudo`, 服务重启, 全局安装 |
| 🔴 极高风险 | 破坏性操作 | `rm -rf`, 数据库删除, 访问凭证 |

---

## 使用方法

### 基本格式

```bash
python3 scripts/cmd_display.py <level> "<command>" "<purpose>" "$(<command>)"
```

### 示例

**🟢 安全级别（仅读取）：**
```bash
python3 scripts/cmd_display.py safe "git status" "Check repo state" "$(git status --short)"
```

**🔵 低风险级别（允许修改文件）：**
```bash
python3 scripts/cmd_display.py low "touch notes.md" "Create file" "$(touch notes.md && echo '✓')"
```

**🟡 中等风险级别（需要谨慎操作）：**
```bash
python3 scripts/cmd_display.py medium "npm install axios" "Add HTTP client" "$(npm install axios 2>&1 | tail -1)"
```

**🟠 高风险级别（仅显示，禁止执行）：**
```bash
python3 scripts/cmd_display.py high "sudo systemctl restart nginx" "Restart server" "⚠️ Manual execution required"
```

**🔴 极高风险级别（禁止自动执行）：**
```bash
python3 scripts/cmd_display.py critical "rm -rf node_modules" "Clean deps" "🛑 Blocked - requires human confirmation"
```

---

## 输出格式

```
🟢 SAFE ✓ git status --short │ Check repo state
   2 modified, 1 untracked

🟠 HIGH ⚠ sudo systemctl restart nginx │ Restart server
   ⚠️ Manual execution required
```

---

## 代理集成方法

将以下内容添加到您的 `SOUL.md` 或 `AGENTS.md` 文件中：

```markdown
## Command Execution Protocol

1. **Classify** every command before running (SAFE/LOW/MEDIUM/HIGH/CRITICAL)
2. **Wrap** with: `python3 <skill>/scripts/cmd_display.py <level> "<cmd>" "<why>"`
3. **HIGH commands** — Show for manual execution, do not run
4. **CRITICAL commands** — NEVER execute, always ask human first
5. **Summarize** verbose output to one line
```

---

## 分类快速参考

**🟢 安全级别（可自动执行）：**
`ls`, `cat`, `head`, `grep`, `find`, `git status`, `git log`, `pwd`, `whoami`, `date`

**🔵 低风险级别（允许执行，但需记录日志）：**
`touch`, `mkdir`, `cp`, `mv`（在项目内部使用），`git add`, `git commit`

**🟡 中等风险级别（需谨慎执行）：**
`npm/pip install`, `git push/pull`, 配置文件修改`

**🟠 高风险级别（执行前需确认）：**
`sudo *`, 服务相关命令, 全局安装, 网络配置修改`

**🔴 极高风险级别（禁止自动执行）：**
`rm -rf`, `DROP DATABASE`, 访问凭证文件, 系统目录操作`

---

## 开发计划

- [x] 制定分类指南
- [x] 编写显示脚本
- [x] 开发 `before_tool_call` 插件以实现代码控制
- [ ] 提供可配置的命令拦截规则
- [ ] 实现审计日志记录功能

---

## 设计理念

> “如果可以通过代码来实现安全控制，就不要依赖文档。”

提示控制只是建议；代码控制才是真正的安全保障。本技能同时提供了这两种方式——现在可以先使用提示，等插件准备好后再升级到代码控制。

---

## 致谢

本技能由 **Oscar Serra** 在 **Claude**（Anthropic团队）的帮助下开发完成。

*安全是不可或缺的。代理执行的每一个命令都应进行分类、理由说明，并且必须能够被审计。*