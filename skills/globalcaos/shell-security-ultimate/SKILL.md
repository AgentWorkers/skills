---
name: shell-security-ultimate
version: 1.0.2
description: "在 OpenClaw 代理执行 shell 命令之前，根据风险等级（从“安全”到“危急”）对它们进行分类。采用颜色编码来显示结果，确保操作的透明度，并记录审计日志。这样可以防止危险操作的发生、避免敏感信息的泄露以及未经授权的网络访问。提供相应的执行脚本和集成方案。"
homepage: https://github.com/globalcaos/clawdbot-moltbot-openclaw
repository: https://github.com/globalcaos/clawdbot-moltbot-openclaw
---

# Shell Security Ultimate

为AI代理提供以安全为首要目标的命令执行机制，对每个shell命令进行分类、审计和控制。

---

## 问题所在

拥有shell访问权限的AI代理可以：
- 运行破坏性命令（如 `rm -rf /`）
- 泄露敏感数据（如 `cat ~/.ssh/id_rsa`）
- 在未经监督的情况下修改系统状态
- 在不说明原因的情况下执行命令

**本技能通过** 对每个命令实施安全分类、透明性和可审计性来解决这些问题。

---

## 编码控制与提示控制

有两种方式来控制代理的行为：

| 方法 | 实施方式 | 可靠性 | 示例 |
|----------|-------------|-------------|---------|
| **提示控制** | 在MD文件中提供指令 | 约80% | 在 `SOUL.md` 中提示“不要运行危险命令” |
| **编码控制** | 通过实际代码/钩子来实现 | 约100% | 一个插件会在执行前阻止 `rm -rf` 命令 |

### 为什么这很重要

- **提示控制的效果会减弱** — 代理在长时间运行过程中可能会忘记指令
- **编码控制的效果更持久** — 代码不会被遗忘，也无法通过言语改变规则
- **深度防御** — 应同时使用提示进行指导，并通过代码来强制执行规则

### 该技能的当前状态

| 组件 | 类型 | 状态 |
|-----------|------|--------|
| 分类指南 | 提示控制 | ✅ 已包含在 `SKILL.md` 中 |
| 显示脚本 | 编码实现 | ✅ `scripts/cmd_display.py` 已编写 |
| 与 `SOUL.md` 的集成 | 提示控制 | ✅ 提供了模板 |
| OpenClaw插件钩子 | 编码实现 | ❌ 尚未完成 — 需要 `before_tool_call` 钩子 |
| 命令拦截功能 | 编码实现 | ❌ 计划中 — 将阻止符合特定模式的命令 |

**现状**：采用混合控制方式。显示脚本提供了结构，但真正的强制执行（在执行前阻止危险命令）需要依赖OpenClaw插件。当前实现依赖于代理自行选择是否使用这些安全机制。

**未来方向**：通过插件完全实现编码控制，该插件会在执行前拦截 `exec` 命令并应用安全策略。

---

## 安全等级

| 等级 | 表情符号 | 风险 | 示例 |
|-------|-------|------|----------|
| 🟢 安全 | 无 | `ls`, `cat`, `git status`, `pwd` |
| 🔵 低风险 | 可逆操作 | `touch`, `mkdir`, `git commit` |
| 🟡 中等风险 | 中等风险 | `npm install`, `git push`, 配置文件修改 |
| 🟠 高风险 | 高风险操作 | `sudo`, 服务重启, 全局安装 |
| 🔴 致命风险 | 破坏性操作 | `rm -rf`, 数据库删除, 访问凭证 |

---

## 使用方法

### 基本格式

```bash
python3 scripts/cmd_display.py <level> "<command>" "<purpose>" "$(<command>)"
```

### 示例

**🟢 安全级（仅读取）：**
```bash
python3 scripts/cmd_display.py safe "git status" "Check repo state" "$(git status --short)"
```

**🔵 低风险（可执行，需记录日志）：**
```bash
python3 scripts/cmd_display.py low "touch notes.md" "Create file" "$(touch notes.md && echo '✓')"
```

**🟡 中等风险（需谨慎执行）：**
```bash
python3 scripts/cmd_display.py medium "npm install axios" "Add HTTP client" "$(npm install axios 2>&1 | tail -1)"
```

**🟠 高风险（仅显示，禁止执行）：**
```bash
python3 scripts/cmd_display.py high "sudo systemctl restart nginx" "Restart server" "⚠️ Manual execution required"
```

**🔴 致命风险（严禁自动执行）：**
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

将相关内容添加到 `SOUL.md` 或 `AGENTS.md` 文件中：

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

**🟢 安全级（可自动执行）：**
`ls`, `cat`, `head`, `grep`, `find`, `git status`, `git log`, `pwd`, `whoami`, `date`

**🔵 低风险（可执行，需记录日志）：**
`touch`, `mkdir`, `cp`, `mv`（在项目范围内），`git add`, `git commit`

**🟡 中等风险（需谨慎执行）：**
`npm/pip install`, `git push/pull`, 配置文件修改`

**🟠 高风险（仅显示，需询问用户）：**
`sudo *`, 服务相关命令, 全局安装, 网络配置修改`

**🔴 致命风险（严禁自动执行）：**
`rm -rf`, `DROP DATABASE`, 访问凭证文件, 系统目录操作`

---

## 发展计划

- [x] 制定分类指南
- [x] 编写显示脚本
- [x] 开发 `before_tool_call` 钩子的OpenClaw插件
- [ ] 提供可配置的命令拦截规则
- [ ] 实现审计日志的持久化存储

---

## 设计理念

> “如果可以用代码来实现安全控制，就不要依赖文档。”

提示控制只是建议；编码控制才是真正的强制措施。本技能同时提供了这两种方式——现在可以使用提示，等到插件准备好后，再升级到编码控制。

---

## 致谢

由 **Oscar Serra** 在 **Claude**（Anthropic团队）的帮助下开发。

*安全是不可或缺的。代理执行的每个命令都应进行分类、合理说明，并且可以被审计。*