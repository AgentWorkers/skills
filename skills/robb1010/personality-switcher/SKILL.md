---
name: personality-switcher
description: 创建并切换 AI 助手的人格。使用 `/personality` 命令可以查看和激活已保存的人格；使用 `/create-personality` 命令可以设计新的人格，系统会自动填充相关属性（如 SOUL 和 IDENTITY）。这些人格设置会在会话之间保持持久性，并且在对话过程中会自动恢复（通过心跳检测机制）。切换人格时系统会进行原子级别的操作，并提供备份和回滚功能。在切换人格之前，系统会始终先备份当前的状态。
---

# 个性切换技能

该技能允许用户创建和管理多个AI助手的个性，并在它们之间无缝切换，同时保持所有设置的变化并维持共享的用户上下文。

## 安装

安装此技能后：

1. 会创建一个名为 `personalities/` 的文件夹。
2. 当前的 `SOUL.md` 和 `IDENTITY.md` 文件会被备份为“default”版本。
3. 会生成一个名为 `_personality_state.json` 的文件来记录当前激活的个性。
4. `HEARTBEAT.md` 文件中会添加一个脚本，用于在每次系统心跳时恢复用户的个性设置。

卸载此技能后：

1. 系统会恢复到默认的个性设置。
2. `HEARTBEAT.md` 中的个性恢复脚本会被移除。
3. `personalities/` 文件夹会被保留（用户可以选择手动删除它）。

## 快速入门

**列出所有个性：**
```
/personality
```

**切换到某个个性：**
```
/personality <name>
```

**创建一个新的个性：**
```
/create-personality A stoic dwarf who loves ale and mining
```

**重命名一个个性：**
```
/rename-personality old-name new-name
```

**删除一个个性：**
```
/delete-personality personality-name
```

## 工作原理

### 架构

每个个性由两个文件组成：
- `SOUL.md`：包含个性的核心理念、语音特征、行为模式和行为界限。
- `IDENTITY.md`：包含个性的名称、特征、表情符号、口头禅和整体氛围。

这两个文件存储在 `personalities/<个性名称>/` 目录下。

`USER.md` 文件始终位于工作区的根目录下，不会因个性切换而被修改。它保存了用户的全局偏好设置和上下文信息。

### 状态持久化

当前激活的个性信息存储在 `_personality_state.json` 文件中：
```json
{
  "active_personality": "aelindor",
  "timestamp": "2026-02-08T18:27:33.373846Z",
  "previous_personality": "default"
}
```

每次系统心跳时，`restore_personality.py` 脚本会读取该文件，并将当前激活的个性应用到工作区的根目录中。这样，即使会话重启或数据被压缩，个性设置也能得以保留。

### 原子级切换机制（安全保障）

切换个性时，系统会执行以下五个步骤：
1. **保存当前状态**：创建 `SOUL.md` 和 `IDENTITY.md` 的备份文件（包含时间戳）。
2. **保存更改**：将当前个性的更新内容写回对应的文件夹。
3. **加载新个性**：将新个性的文件复制到工作区的根目录。
4. **更新状态**：将当前激活的个性信息写入 `_personality_state.json`。
5. **验证完整性**：检查文件是否正确加载；如果任何步骤失败，系统会回滚到之前的状态。

如果任何步骤失败，整个操作都会恢复到之前的状态，确保数据不会丢失。

### 备份管理

备份文件存储在 `~/.openclaw/workspace/personalities/backups/` 目录下。切换个性时，系统会自动创建上一个个性版本的备份，并保留最近 10 个备份文件。用户可以通过 `--keep N`（默认值：10）和 `--days D`（保留天数）选项来自定义备份策略。

**可选配置：** 在 `HEARTBEAT.md` 中添加脚本，以实现定期备份清理：
```bash
python3 ~/.openclaw/workspace/skills/personality-switcher/scripts/cleanup_backups.py --keep 10
```

### 默认个性

“default”个性具有特殊含义：
- 安装时会根据用户的初始配置自动创建。
- 始终可用且可被选择。
- 防止被意外删除或重命名。
- 在出现问题时，它是用户的“安全网”。

## 命令

### `/personality [名称]`

- 列出所有可用的个性。
- 或者切换到指定的个性。

**无参数时**：显示所有可用个性的列表，并标出当前激活的个性。
**带参数时**：立即切换到指定的个性。

**示例：**
```
/personality aelindor
```

**输出：**
```
Switched to personality 'aelindor'.
Previous: default
Backup: _personality_current_2026-02-08T18-27-33.371866
```

### `/create-personality [描述]**

根据用户提供的文本描述创建一个新的个性。

**输入：** 个性的自然语言描述。

**输出：** 一个新的个性文件夹会被创建，其中包含自动生成的 `SOUL.md` 和 `IDENTITY.md` 文件，可立即使用。

**工作原理：**
1. 用户提供个性的描述。
2. 系统会为该个性选择一个简短的名称（1-2个单词）。
3. 系统会根据描述生成相应的 `SOUL.md` 和 `IDENTITY.md` 文件。

**示例：**
```
/create-personality A curious wizard obsessed with knowledge, speaks in riddles, brilliant but condescending
```

**创建完成后：** 新个性即可立即使用。用户可以在 `personalities/` 目录下编辑 `SOUL.md` 和 `IDENTITY.md` 文件来进一步定制个性。

**技术细节：** 系统会自动选择一个简洁的名称，确保名称的唯一性和格式正确性。

### `/rename-personality [旧名称] [新名称]**

重命名指定的个性文件夹。

**规则：**
- 不能重命名“default”个性。
- 名称必须唯一（只能使用小写字母、数字和连字符）。
- 如果重命名的是当前激活的个性，系统会自动更新其状态。

**示例：**
```
/rename-personality pirate-captain pirate-v2
```

### `/delete-personality [名称]**

永久删除指定的个性。

**规则：**
- 不能删除“default”个性。
- 如果删除的是当前激活的个性，系统会自动切换回“default”个性。

**示例：**
```
/delete-personality pirate-v2
```

## 与 OpenClaw 的集成

在 `HEARTBEAT.md` 中添加以下脚本，以实现每次系统心跳时自动恢复用户的个性设置：
```bash
python3 ~/.openclaw/workspace/skills/personality-switcher/scripts/restore_personality.py
```

### Telegram 原生命令

在 Telegram 聊天中，可以使用以下原生命令：
- `/personality`：列出和切换个性。
- `/create-personality`：创建新的个性。
- `/rename-personality`：重命名个性。
- `/delete-personality`：删除个性。

## 文件结构

**注意：** 备份文件会自动清理，工作区的根目录保持整洁。所有核心逻辑都存储在 `personalities/` 目录下。

## 文件格式要求

### `SOUL.md`

文件内容包含个性的核心理念、语音特征和行为规范：
- 核心身份和背景信息。
- 语音模式和行为习惯。
- 哲学观念（时间、权力、道德等）。
- 说话方式和独特习惯。
- 触发厌恶或认可的行为因素。
- 行为界限和约束条件。
- 个性的标志性行为和口头禅。

**示例结构：**
```markdown
# SOUL.md - [Personality Name]

## Core Identity
[Background and essence]

## Voice & Mannerisms
[How this personality speaks and acts]

## Philosophy
[Core beliefs and worldview]

## Signature Behaviors
[Unique traits and catchphrases]
```

### `IDENTITY.md`

文件用于快速展示个性的基本信息：
- 个性名称。
- 个性的类型/角色。
- 用于识别的表情符号。
- 个性的整体氛围（一句话总结）。
- 口头禅（如适用）。
- 个性的主要特征。

**示例结构：**
```markdown
# IDENTITY.md - [Personality Name]

- **Name:** [Name]
- **Type:** [Creature or archetype]
- **Emoji:** [Emoji]
- **Vibe:** [One-sentence vibe]
- **Catchphrase:** [Signature phrase]

## Quick Traits
- Trait 1
- Trait 2
- Trait 3
```

## 备份与恢复

每次切换个性前，系统会在 `personalities/backups/` 目录下创建备份文件：
- `current_2026-02-08T17-27-33.371866/`：包含上一个个性的 `SOUL.md` 和 `IDENTITY.md` 备份。

**手动恢复**（如有需要）：
```bash
# List available backups
ls -la ~/.openclaw/workspace/personalities/backups/

# Copy backup files back to workspace root if needed
cp ~/.openclaw/workspace/personalities/backups/current_<timestamp>/SOUL.md ~/.openclaw/workspace/SOUL.md
cp ~/.openclaw/workspace/personalities/backups/current_<timestamp>/IDENTITY.md ~/.openclaw/workspace/IDENTITY.md
```

系统会自动清理备份文件；默认保留最近 10 个备份。用户可以在 `HEARTBEAT.md` 中调整备份策略。

## 错误处理

所有命令都会返回 JSON 格式的响应：
- **成功**：返回相应的成功信息。
- **错误**：返回详细的错误信息。

**常见错误代码：**
- `personality_not_found`：目标个性不存在。
- `already_exists`：名称已被使用。
- `invalid_name`：名称格式无效。
- `cannot_delete_default`：尝试删除“default”个性。
- `cannot_rename_default`：尝试重命名“default”个性。
- `switch_failed`：切换失败，系统会回滚到之前的状态。
- `integrity_check_failed`：文件完整性检查失败。

## 提示与最佳实践：
- 个性描述应尽可能具体（例如：“痴迷于宝藏的海盗船长”比“有趣的”更有效）。
- 创建个性后可以直接编辑 `SOUL.md` 和 `IDENTITY.md` 文件以进一步完善个性设置。
- 可以频繁切换个性。
- 将“default”个性作为“安全锚点”，确保系统的稳定性；其他个性可用于实验。
- 切换个性后请检查备份文件，确保之前的个性设置已被正确保存。
- 请注意：`USER.md` 文件始终是共享的，用户的时区、位置和偏好设置不会因个性切换而改变。

## 卸载行为

卸载此技能后：
- 当前的个性文件会被替换为“default”版本的副本。
- 用户的原始 `SOUL.md` 和 `IDENTITY.md` 文件会恢复为“default”版本。
- `personalities/` 文件夹会被保留。
- 系统会恢复到初始状态。

**所有个性设置都不会丢失。**

## 脚本参考

相关脚本位于 `skills/personality-switcher/scripts/` 目录下：
- `list_personalities.py`：列出所有可用的个性。
- `switch_personality.py`：实现原子级切换并包含备份和回滚功能。
- `create_personality.py`：根据描述生成新的个性。
- `rename_personality.py`：重命名个性文件夹。
- `delete_personality.py`：删除个性（如果当前激活的是该个性，则会自动切换回“default”）。
- `restore_personality.py`：在每次系统心跳时恢复个性设置。
- `cleanup_backups.py`：手动清理备份文件（支持 `--keep` 和 `--days` 选项）。
- `utils.py`：提供通用辅助功能（文件读写、备份管理、验证和状态更新）。

### 切换后的自动清理

默认情况下，`switch_personality.py` 会在切换成功后自动清理旧的备份文件，仅保留最近 10 个备份。如果清理失败，系统会返回警告信息。

---

**版本：2.0**（从头开始重新设计）  
**状态：** 已具备原子级切换和故障恢复功能，可投入生产环境使用。