---
name: obsidian-conversation-backup
description: Obsidian的自动对话备份系统，支持增量快照、每小时的数据统计以及格式化的Markdown聊天记录。该系统可用于设置对话存档，防止因“/new”命令导致的数据丢失，并帮助您以规范的格式（包括颜色标注、时间戳、多段文本支持等）整理Obsidian中的聊天历史记录。
---

# Obsidian 聊天记录备份

该工具会自动将 Clawdbot 的聊天记录备份到 Obsidian 中，并保持美观的聊天样式格式。通过每小时生成增量快照，有效防止因 `/new` 命令重置而导致的数据丢失。

## 主要功能

- **增量备份**：仅备份新消息（避免重复备份）
- **聊天格式**：采用 Obsidian 的格式化方式，支持表情符号、时间戳以及多段文本
- **按小时分类**：将聊天记录按小时整理，便于查阅
- **零成本**：仅使用 shell 脚本，无需调用大型语言模型（LLM）
- **智能过滤**：跳过空消息和系统通知

## 快速设置

### 安装

```bash
# Extract the skill (if downloaded as .skill file)
unzip obsidian-conversation-backup.skill
cd obsidian-conversation-backup

# Run installer (interactive)
chmod +x install.sh
./install.sh
```

安装程序会询问以下信息：
- Obsidian 存储目录的路径
- 会话文件所在的目录
- 用于跟踪状态的文件位置

**或手动设置：**
1. 将 `config.example` 复制到 `config` 文件中
2. 根据实际情况修改 `config` 文件中的路径
3. 使脚本可执行：`chmod +x scripts/*.sh`

### 启用自动备份

将以下命令添加到 crontab 中，以实现每小时自动备份：

```bash
crontab -e

# Add this line (runs every hour at :00)
0 * * * * /path/to/obsidian-conversation-backup/scripts/monitor_and_save.sh
```

### 自定义聊天显示样式（可选）

编辑 `scripts/format_message_v2.jq` 文件，可以更改：
- 用户的表情符号（默认：🐉）
- 助理的表情符号（默认：🦞）
- 信息标记的类型（默认：用户消息使用 `[!quote]`，辅助消息使用 `[!check]`）

## 使用方法

### 自动增量备份

配置完成后，系统将自动执行以下操作：
- 每小时检查是否有新消息（消息长度至少为 10 行）
- 如果有新消息，生成增量快照并保存到 `YYYY-MM-DD-HHmm-incremental.md` 文件中
- 如果没有新消息，则跳过备份

**示例输出：**
```
2026-01-20-1500-incremental.md (messages from last save to now)
2026-01-20-1600-incremental.md (new messages since 15:00)
2026-01-20-1700-incremental.md (new messages since 16:00)
```

**数据保护**：最多丢失 1 小时的聊天记录

### 按需生成完整快照

可以随时生成完整的聊天记录备份：

```bash
scripts/save_full_snapshot.sh [topic-name]
```

**示例：**
```bash
scripts/save_full_snapshot.sh important-decisions
scripts/save_full_snapshot.sh bug-fix-discussion
scripts/save_full_snapshot.sh  # uses "full-conversation" as default
```

### 按小时分类的聊天记录

将聊天记录按小时整理，便于查阅：

```bash
scripts/create_hourly_snapshots.sh YYYY-MM-DD
```

**示例：**
```bash
scripts/create_hourly_snapshots.sh 2026-01-20
```

**输出结果：**
```
2026-01-20-1500-hourly.md (15:00-15:59 messages)
2026-01-20-1600-hourly.md (16:00-16:59 messages)
2026-01-20-1700-hourly.md (17:00-17:59 messages)
```

**用途**：用于每日结束时整理聊天记录，方便后续查阅

## 聊天格式

聊天记录以彩色文本的形式显示在 Obsidian 中：
- **用户消息**（蓝色 `[!quote]` 标签）：
```
> [!quote] 🐉 User · 15:30
> This is my message
```

- **辅助消息**（绿色 `[!check]` 标签）：
```
> [!check] 🦞 Zoidbot · 15:31  
> This is the response
```

**特点：**
- 时间戳（格式为 HH:MM）
- 支持多段文本（使用 `<br><br>` 分段）
- 每行前都会加上 `>` 符号
- 空消息会被过滤掉
- 系统通知不会被包含在备份中

## 令牌使用监控

`monitor_and_save.sh` 脚本还会监控令牌的使用情况：
- 当令牌使用量达到 800k（80%）时，会发送警告：**“建议尽快使用 /new 命令”**
- 当令牌使用量达到 900k（90%）时，会发送紧急警告：**“立即使用 /new 命令”**

## 文件结构

```
scripts/
├── monitor_and_save.sh           # Hourly incremental backup + token monitoring
├── save_full_snapshot.sh         # On-demand full conversation save
├── create_hourly_snapshots.sh    # Organize by clock hour
└── format_message_v2.jq          # Chat formatting logic
```

## 配置

### 跟踪状态文件

系统使用隐藏文件来记录备份状态：

```bash
/root/clawd/.last_save_line_count       # For token monitoring
/root/clawd/.last_snapshot_timestamp    # For incremental saves
/root/clawd/.token_warning_sent         # For warning deduplication
```

**注意：**请勿删除这些文件，否则增量备份可能会重复备份相同的内容

### 会话文件位置

默认位置：`/root/.clawdbot/agents/main/sessions/*.jsonl`

如果会话文件位于其他位置，请在每个脚本中更新 `SESSION_FILE` 的路径。

## 故障排除

### 无法生成快照

1. 检查 crontab 是否正在运行：`crontab -l`
2. 确保脚本具有执行权限：`chmod +x scripts/*.sh`
3. 查看日志以获取错误信息

### 消息格式问题

- 确保 `format_message_v2.jq` 文件中包含以下代码：`gsub("\n\n"; "<br><br:")`
- 检查所有消息行是否都以 `>` 开头
- 确保已安装 `jq` 工具：`jq --version`

### 快照中存在重复内容

- 删除跟踪文件，然后让系统重新开始备份：
  ```bash
  rm /root/clawd/.last_snapshot_timestamp
  ```

### 显示空聊天框

- 更新 `format_message_v2.jq` 文件以过滤空消息
- 确保脚本中包含 `if ($text_content | length) > 0` 条件判断

## 所需软件

- **jq**：用于解析 JSON 数据（使用 `apt-get install jq` 安装）
- **crontab**：用于自动备份
- **Obsidian 存储目录**：用于保存备份文件

## 高级定制

### 更改备份频率

编辑 crontab 配置文件：

```bash
# Every 2 hours
0 */2 * * * /path/to/monitor_and_save.sh

# Every 30 minutes
*/30 * * * * /path/to/monitor_and_save.sh

# Specific times only (9am, 12pm, 6pm, 9pm)
0 9,12,18,21 * * * /path/to/monitor_and_save.sh
```

### 调整最小消息长度阈值

修改 `monitor_and_save.sh` 文件：

```bash
# Change from 10 to 5 messages minimum
if [[ $new_lines -lt 5 ]]; then
```

### 增加更多信息标记样式

Obsidian 的信息标记类型：
- `[!quote]` - 蓝色
- `[!check]` - 绿色
- `[!note]` - 青色
- `[!tip]` - 紫色
- `[!warning]` - 橙色
- `[!danger]` - 红色

### 自定义 Telegram 通知

编辑 `monitor_and_save.sh` 文件以更改警告内容或添加自定义通知。

## 最佳实践

1. **每天结束时生成按小时分类的聊天记录**：主要用于整理聊天记录，而非仅仅作为备份
2. **持续运行增量备份**：作为数据安全的保障
3. **设置完成后手动测试脚本**：先手动运行脚本以验证输出结果
4. **备份跟踪文件**：在备份文件中包含 `last_snapshot_timestamp` 以记录备份时间
5. **使用有意义的文件名**：为完整备份文件起有意义的名称

## 示例工作流程

**日常操作：**
1. 每小时自动执行增量备份（无需额外操作）
2. 每天结束时：运行 `scripts/create_hourly_snapshots.sh 2026-01-20`
3. 在 Obsidian 中查看按小时分类的聊天记录
4. 如有需要，可删除旧的增量备份文件（已按小时分类的聊天记录会覆盖旧文件）

**在执行 `/new` 命令前：**
1. 可选：运行 `scripts/save_full_snapshot.sh before-reset`
2. 安全地执行 `/new` 命令（聊天记录已备份）
3. 继续聊天，系统会自动恢复增量备份

## 与 Clawdbot 的集成

该工具可与以下功能集成：
- **HEARTBEAT.md**：自动监控令牌使用情况
- **MEMORY.md**：聊天记录存档系统
- **Telegram 集成**：接收警告通知
- **任何 Obsidian 存储目录**：支持与现有的 Obsidian 存储目录配合使用

## 致谢

该工具由 Clawdbot 社区开发，旨在提供可靠的聊天记录备份功能以及美观的 Obsidian 格式化体验。