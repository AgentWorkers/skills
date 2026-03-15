---
name: lyrics
version: 1.0.0
author: BytesAgain
license: MIT-0
tags: [lyrics, tool, utility]
---

# 歌词工具包

歌词工具包（Lyrics Toolkit）是一款辅助歌曲创作的工具，提供功能包括：韵律检测、音节计数、诗句结构分析、副歌模式生成以及歌词格式导出等。

## 命令

| 命令          | 描述                                      |
|---------------|---------------------------------------------|
| `lyrics run`     | 执行主功能                         |
| `lyrics list`    | 显示所有可用命令列表                   |
| `lyrics add <item>`  | 添加新的歌词条目                     |
| `lyrics status`   | 显示当前工具包的状态                   |
| `lyrics export <format>` | 以指定格式导出歌词数据                   |
| `lyrics help`    | 显示使用帮助                         |

## 使用方法

```bash
# Show help
lyrics help

# Quick start
lyrics run
```

## 示例

- 使用 `lyrics help` 命令可查看所有可用命令的详细信息。
- 所有歌词数据存储在 `~/.local/share/lyrics/` 目录下。

---
*由 BytesAgain 提供支持 | bytesagain.com*

## 输出结果

工具包的输出结果会直接显示在标准输出（stdout）中。若需保存输出内容，可使用命令 `lyrics run > output.txt`。

## 配置设置

可以通过设置环境变量 `LYRICS_DIR` 来更改数据存储目录。默认目录为 `~/.local/share/lyrics/`。