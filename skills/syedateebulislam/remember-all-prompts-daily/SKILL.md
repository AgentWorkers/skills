---
name: remember-all-prompts-daily
description: 在令牌压缩周期中，通过提取并按日期顺序存档所有提示信息来保持对话的连续性。当令牌使用率达到95%（压缩前）或新冲刺开始时，系统会自动触发会话历史的导出操作；在会话重新启动时，系统会导入这些存档的摘要内容以恢复对话的上下文。
---

# 每日自动保存所有对话记录

该功能通过在新会话开始时自动归档会话历史记录，并在会话压缩前将其恢复，从而确保对话的连续性。

## 工作原理

### 1. **触发归档（当令牌使用量达到95%时）**
- 当令牌使用量接近95%时：
  - 运行 `export_prompts.py` 命令以提取当前会话的历史记录。
  - 将所有提示和回复按照时间戳进行格式化。
  - 将这些记录按日期顺序添加到 `memory/remember-all-prompts-daily.md` 文件中。
  - 标记归档点，以便后续进行会话压缩。

### 2. **触发新会话（当令牌使用量降至1%时）**
- 当新会话开始时（令牌使用量降至1%），系统会：
  - 检查 `memory/remember-all-prompts-daily.md` 文件是否存在。
  - 读取最新的会话记录。
  - 将这些记录作为“之前的对话摘要”重新引入新会话中，以恢复对话上下文。
  - 会话会从上一次结束的地方无缝继续。

### 3. **每日文件结构**
```
# Remember All Prompts Daily

## [DATE: 2026-01-26]

### Session 1 (09:00 - 09:47)
[All prompts and responses from session]

### Session 2 (10:15 - 11:30)
[All prompts and responses from session]
```

## 脚本

### `scripts/export_prompts.py`
从当前会话中提取所有提示和回复，并将它们归档。

**使用方法：**
```bash
python scripts/export_prompts.py
```

**功能说明：**
- 使用 `sessions_history()` 函数获取当前会话中的所有消息。
- 将消息按照时间戳和消息ID进行格式化。
- 将格式化后的内容添加到 `memory/remember-all-prompts-daily.md` 文件中。
- 包含元数据（如令牌数量、会话持续时间等）。

### `scripts/ingest_prompts.py`
在会话开始时读取归档文件，并将其作为对话上下文重新引入会话中。

**使用方法：**
```bash
python scripts/ingest_prompts.py
```

**功能说明：**
- 读取 `memory/remember-all-prompts-daily.md` 文件（如果存在）。
- 提取最新的会话记录。
- 返回格式化的摘要内容，以便在新会话中使用。

## 集成

### 心跳检测
将相关代码添加到 `HEARTBEAT.md` 文件中，以监控令牌使用情况：
```
Check token usage - if >95%, export session history
```

### 定时任务（可选）
为了实现自动触发，可以设置定时任务：
```bash
# Check token at regular intervals
clawdbot cron add --text "Check token usage and export if needed" --schedule "*/15 * * * *"
```

## 示例流程

**会话1：**
1. 正常聊天。
2. 令牌使用量达到95%。
3. `export_prompts.py` 自动运行，将所有对话记录归档到每日文件中。
4. 会话被压缩。

**会话2（新会话）：**
1. 令牌使用量降至1%。
2. `ingest_prompts.py` 读取归档文件。
3. 系统会显示：“这是我们昨天讨论的内容……”
4. 对话上下文得到恢复，会话继续进行。

## 手动操作

### 立即导出会话记录
```bash
python skills/remember-all-prompts-daily/scripts/export_prompts.py
```

### 查看今日的归档记录
```bash
cat memory/remember-all-prompts-daily.md | tail -100
```

### 重新引入上一次的会话记录
```bash
python skills/remember-all-prompts-daily/scripts/ingest_prompts.py
```

## 令牌使用监控
可以通过以下方式监控令牌使用情况：
```bash
session_status  # Shows current token usage %
```

当令牌使用量接近95%时，系统会自动触发归档操作；您也可以手动执行导出操作。

## 注意事项

- 该功能仅在主会话中运行（即与 Ateeb 的直接聊天过程中）。
- 该功能尊重用户隐私，仅存储您的实际对话内容。
- 每日文件会在午夜自动更新（每个日期对应一条记录）。
- 您也可以随时手动触发归档操作。