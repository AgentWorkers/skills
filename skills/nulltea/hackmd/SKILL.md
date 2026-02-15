---
name: hackmd
description: **使用 HackMD 文档**  
HackMD 是一款用于创建、编辑和管理的在线文档工具。它支持阅读、创建、更新以及删除文档，并具备变更跟踪功能，能够检测文档自上次查看以来的修改内容。同时，HackMD 支持个人工作空间和团队协作模式。
metadata:
    {
        "clawdbot":
            {
                "emoji": "📜",
                "requires":
                    { "bins": ["hackmd-cli"], "env": ["HMD_API_ACCESS_TOKEN"] },
                "primaryEnv": "HMD_API_ACCESS_TOKEN",
            },
    }
---

# HackMD 集成

## 需求

```bash
npm install -g @hackmd/hackmd-cli
```

## 快速参考

### 阅读笔记

```bash
# List all personal notes
hackmd-cli notes

# Get note metadata (includes lastChangedAt)
hackmd-cli notes --noteId=<id> --output json

# Get note content (markdown)
hackmd-cli export --noteId=<id>

# List teams
hackmd-cli teams

# List team notes
hackmd-cli team-notes --teamPath=<path>
```

### 编写笔记

```bash
# Create note
hackmd-cli notes create --content='# Title'

# Create from file
cat file.md | hackmd-cli notes create

# Update note
hackmd-cli notes update --noteId=<id> --content='# Updated'

# Delete note
hackmd-cli notes delete --noteId=<id>
```

### 团队笔记

```bash
hackmd-cli team-notes create --teamPath=<path> --content='# Team Note'
hackmd-cli team-notes update --teamPath=<path> --noteId=<id> --content='...'
hackmd-cli team-notes delete --teamPath=<path> --noteId=<id>
```

## 变更跟踪

使用 `hackmd-track.js`（位于 `scripts/` 目录下）来高效地检测文档的变更。

### 跟踪笔记

```bash
node scripts/hackmd-track.js add <noteId>
```

### 检查变更

```bash
# Single note - outputs content only if changed
node scripts/hackmd-track.js changes <noteId>

# All tracked notes
node scripts/hackmd-track.js changes --all

# JSON output for parsing
node scripts/hackmd-track.js changes <noteId> --json
```

### 管理跟踪

```bash
node scripts/hackmd-track.js list              # Show tracked notes
node scripts/hackmd-track.js remove <noteId>   # Stop tracking
node scripts/hackmd-track.js reset <noteId>    # Reset (next check shows as changed)
```

### 工作原理

1. `hackmd-track.js add` 会存储笔记的 `lastChangedAt` 时间戳。
2. `hackmd-track.js changes` 会将当前的 `lastChangedAt` 与存储的值进行比较。
3. 如果有变更：会输出变更内容并更新存储的时间戳。
4. 如果没有变更：则不输出任何内容（可以使用 `--verbose` 选项查看状态）。

所有变更信息都存储在 `./.hackmd/tracked-notes.json` 文件中（当前工作目录下）。

## 笔记元数据字段

当使用 `--output json` 选项时，笔记会包含以下元数据：

| 字段            | 描述                                      |
| ---------------- | ---------------------------------------- |
| `lastChangedAt`  | 最后修改的 Unix 时间戳                         |
| `lastChangeUser` | 最后编辑者的名称、用户路径和头像                   |
| `titleUpdatedAt` | 标题最后一次更改的时间                         |
| `tagsUpdatedAt` | 标签最后一次更改的时间                         |

## 速率限制

- 每 5 分钟最多 100 次调用。
- 每月最多 2000 次调用（Prime 计划用户可享受 10,000 次调用额度）。