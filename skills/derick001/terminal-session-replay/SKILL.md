---
name: terminal-session-replay
description: 记录并回放终端会话，以便于调试、编写文档或与团队成员分享操作步骤。
version: 1.0.0
author: skill-factory
metadata:
  openclaw:
    requires:
      bins:
        - python3
        - script
---
# 终端会话回放工具

## 功能介绍

这是一个用于记录、回放和导出终端会话的命令行工具（CLI）。它可以捕获命令、输出内容以及执行时间，以便后续查看、生成文档或与团队成员共享。该工具通过简化标准 `script` 命令的接口并添加额外功能来提升使用体验。

**主要功能：**
- **记录会话**：使用简单命令开始记录终端会话。
- **回放会话**：以原始执行时间顺序回放已录制的会话。
- **导出为 Markdown**：将会话内容转换为可读的文档格式。
- **会话管理**：列出、查看和删除已录制的会话。
- **元数据支持**：为会话添加标题、描述和标签。
- **时间控制**：调整回放速度或跳过时间信息以加快查看速度。

## 使用方法

### 记录会话：
```bash
./scripts/main.py record --output session1
```

### 回放会话：
```bash
./scripts/main.py replay --input session1
```

### 导出为 Markdown：
```bash
./scripts/main.py export --input session1 --output session1.md
```

### 列出已录制的会话：
```bash
./scripts/main.py list
```

### 完整命令参考：
```bash
./scripts/main.py help
```

## 命令列表

- `record`：开始记录终端会话
  - `--output`：会话名称（默认：基于时间戳的文件名）
  - `--title`：会话标题（用于元数据）
  - `--desc`：会话描述
  - `--tags`：用逗号分隔的标签

- `replay`：回放已录制的会话
  - `--input`：要回放的会话名称
  - `--speed`：回放速度（默认：1.0）
  - `--no-timing`：跳过时间信息，立即显示内容

- `export`：将会话内容导出为 Markdown 文件
  - `--input`：要导出的会话名称
  - `--output`：输出 Markdown 文件的路径（默认：`session_name.md`）
  - `--include-timing`：在导出的文件中包含时间信息

- `list`：列出所有已录制的会话
  - `--filter-tags`：按标签过滤会话

- `info`：显示会话的元数据
  - `--input`：会话名称

- `delete`：删除指定的会话
  - `--input`：要删除的会话名称

## 输出路径

默认情况下，会话文件存储在 `~/.terminal-sessions/` 目录下：
- `session_name.typescript`：原始终端记录内容（`script` 命令的输出）
- `session_nametiming`：用于回放的时间数据
- `session_name.meta.json`：元数据（标题、描述、标签、时间戳）

**导出示例：**
```markdown
# Terminal Session: Setting up Project

**Recorded:** 2026-03-11 10:30:00  
**Duration:** 2 minutes 15 seconds

```bash
$ git clone https://github.com/example/project
Cloning into 'project'...
remote: Enumerating objects: 100, done.
remote: Counting objects: 100% (100/100), done.
remote: Compressing objects: 100% (80/80), done.
remote: Total 100 (delta 20), reused 80 (delta 15), pack-reused 0
Receiving objects: 100% (100/100), 1.5 MiB | 3.5 MiB/s, done.
Resolving deltas: 100% (20/20), done.
$ cd project
$ npm install
...
```

## Limitations

- Requires `script` command (available on Linux/macOS, not on Windows without WSL/Cygwin)
- Cannot record GUI applications or mouse interactions
- Very fast terminal output may not be captured perfectly
- Sessions can be large if recording for long periods
- Color and formatting may not be preserved in markdown export
- Requires terminal with proper support for script command

## Examples

Record a debugging session:
```bash
./scripts/main.py record --output debug-session --title "Debugging API issue" --tags "debug,api"
# ... 在终端中执行操作 ...
exit  # 或使用 Ctrl+D 结束记录
```

Replay at 2x speed:
```bash
./scripts/main.py replay --input debug-session --speed 2.0
```

Export for documentation:
```bash
./scripts/main.py export --input debug-session --output DEBUGGING.md
```

## 安装说明

`script` 命令通常已预装在 Linux 和 macOS 系统上。在 Windows 上，可以使用 WSL 或 Cygwin 来运行该工具。

该工具会在 `~/.terminal-sessions/` 目录下创建用于存储会话文件的文件夹。