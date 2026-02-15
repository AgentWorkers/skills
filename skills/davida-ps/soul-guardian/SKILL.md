---
name: soul-guardian
version: 0.0.2
description: **漂移检测与基线完整性保护机制：用于代理工作区文件，并支持自动警报功能**
homepage: https://clawsec.prompt.security
metadata: {"openclaw":{"emoji":"👻","category":"security"}}
clawdis:
  emoji: "👻"
  requires:
    bins: [python3]
---

# Soul-Guardian 👻

该工具可保护您的代理核心文件（如 SOUL.md、AGENTS.md 等）免受未经授权的修改，具备自动检测、恢复文件以及向用户发送警报的功能。

## 快速入门（3 个步骤）

### 步骤 1：初始化基线
```bash
cd ~/.openclaw/workspace
python3 skills/soul-guardian/scripts/soul_guardian.py init --actor setup --note "initial baseline"
```

### 步骤 2：启用监控
```bash
python3 skills/soul-guardian/scripts/soul_guardian.py enable-monitoring
```
本部分将指导您如何将监控功能集成到您的工作流程中。

### 步骤 3：添加到 HEARTBEAT.md 文件中（推荐）

建议将以下代码添加到您的 HEARTBEAT.md 文件中，以实现自动监控：
```markdown
## Soul Guardian Check
- Run `python3 skills/soul-guardian/scripts/soul_guardian.py check --actor heartbeat --output-format alert`
- If any output is produced, relay it to the user immediately as a security alert
```

完成这些设置后，Soul-Guardian 将：
- ✅ 检测到对受保护文件的未经授权的修改
- ✅ 自动将 SOUL.md 和 AGENTS.md 恢复到已批准的基线状态
- ✅ 在检测到文件内容发生变化时向您发送警报

---

## 保护文件类型及默认策略

| 文件名 | 监控模式 | 发生变化时的处理方式 |
|------|------|-----------------|
| SOUL.md | 恢复文件 | 自动恢复文件并发送警报 |
| AGENTS.md | 恢复文件 | 自动恢复文件并发送警报 |
| USER.md | 发送警报 | 仅发送警报 |
| TOOLS.md | 发送警报 | 仅发送警报 |
| IDENTITY.md | 发送警报 | 仅发送警报 |
| HEARTBEAT.md | 发送警报 | 仅发送警报 |
| MEMORY.md | 发送警报 | 仅发送警报 |
| memory/*.md | 忽略 | 忽略这些文件 |

## 命令

### 检测文件内容变化（并显示警报）
```bash
python3 skills/soul-guardian/scripts/soul_guardian.py check --output-format alert
```
- 未检测到变化时：不显示任何提示
- 检测到变化时：显示易于阅读的警报信息
- 非常适合与心跳检查（heartbeat check）功能集成使用

### 持续监控模式
```bash
python3 skills/soul-guardian/scripts/soul_guardian.py watch --interval 30
```
该模式会持续运行，每 30 秒检查一次文件内容是否发生变化。

### 批准有意进行的修改
```bash
python3 skills/soul-guardian/scripts/soul_guardian.py approve --file SOUL.md --actor user --note "intentional update"
```

### 查看状态
```bash
python3 skills/soul-guardian/scripts/soul_guardian.py status
```

### 验证审计日志的完整性
```bash
python3 skills/soul-guardian/scripts/soul_guardian.py verify-audit
```

---

## 警报格式

当检测到文件内容发生变化时，使用 `--output-format alert` 选项会生成如下格式的警报信息：
```
==================================================
🚨 SOUL GUARDIAN SECURITY ALERT
==================================================

📄 FILE: SOUL.md
   Mode: restore
   Status: ✅ RESTORED to approved baseline
   Expected hash: abc123def456...
   Found hash:    789xyz000111...
   Diff saved: /path/to/patches/drift.patch

==================================================
Review changes and investigate the source of drift.
If intentional, run: soul_guardian.py approve --file <path>
==================================================
```

该警报信息可直接通过 TUI 或聊天界面发送给用户。

---

## 安全模型

**功能说明：**
- 检测文件系统内容与已批准基线（通过 sha256 哈希值进行比对）之间的差异
- 生成统一的差异报告供审核
- 通过哈希链技术维护审计日志的完整性，防止篡改
- 不会对符号链接进行操作
- 使用原子写操作来确保文件恢复的可靠性

**局限性：**
- 无法确定具体是哪个用户进行了修改（仅记录操作者的元数据）
- 如果攻击者同时控制了工作区和状态目录，该工具将无法提供有效保护
- 不能替代传统的备份机制

**建议：** 将状态目录存储在工作区之外，以提高系统的弹性。

---

## 演示

运行完整的演示流程，查看 Soul-Guardian 的实际效果：
```bash
bash skills/soul-guardian/scripts/demo.sh
```

演示流程包括：
1. 验证文件系统的初始状态（静默检查）
2. 向 SOUL.md 文件中插入恶意内容
3. 运行心跳检查（触发警报）
4. 显示 SOUL.md 文件已被成功恢复

---

## 故障排除

- **出现 “未初始化” 错误**：请先运行 `init` 命令以初始化基线。
- **文件内容持续发生变化**：检查哪些进程正在修改文件，并查看审计日志并进行相应的修复。
- **希望批准某次修改**：在查看修改内容后，运行 `approve --file <路径>` 命令进行批准。