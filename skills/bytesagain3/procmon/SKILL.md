---
name: ProcMon
description: "进程监控与管理工具。可列出正在运行的进程及其资源使用情况，按名称搜索进程，实时监控特定进程的CPU和内存使用情况，向进程发送信号，以及查看进程树结构。让系统进程管理变得更加简单。"
version: "1.0.0"
author: "BytesAgain"
tags: ["process","monitor","manager","kill","system","admin","top","htop"]
categories: ["System Tools", "Developer Tools"]
---# ProcMon
用于监控和管理进程。可以查找、监视和控制正在运行的进程。
## 命令
- `list [filter]` — 列出进程（可选的名称过滤条件）
- `top [n]` — 按CPU使用率排序的前N个进程
- `mem [n]` — 按内存使用率排序的前N个进程
- `watch <pid>` — 长期监视指定的进程
- `tree` — 显示进程树结构
- `find <name>` — 按名称查找进程
- `signal <pid> <signal>` — 向指定进程发送信号
## 使用示例
```bash
procmon list python
procmon top 10
procmon find nginx
procmon watch 1234
procmon tree
```
---
技术支持：BytesAgain | bytesagain.com

## 使用场景
- 作为更大自动化流程的一部分
- 当需要从命令行快速执行ProcMon操作时

## 输出结果
输出结果会显示在标准输出（stdout）中。可以通过 `procmon run > output.txt` 将输出重定向到文件中。

## 配置
可以通过设置 `PROCMON_DIR` 环境变量来更改数据目录。默认目录为：`~/.local/share/procmon/`