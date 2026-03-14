---
name: git-toolkit
description: "Git Extras — 一套扩展的 Git 工具集，提供自动化功能以帮助完成 Git 相关任务。当您需要使用 Git Extras 的各种功能时，可以将其纳入您的开发流程中。"
runtime: bash
license: MIT
---
# Git Extras

Git Extras — 一系列扩展的 Git 工具

## 为什么需要这个工具？

- 受到热门开源项目的启发（在 GitHub 上获得了数千个星标）
- 无需安装，可以直接使用系统自带的工具
- 具有实际功能，能够执行真实的 Git 命令并产生相应的输出结果

## 命令列表

运行 `scripts/git_extras.sh <command>` 即可使用以下命令：

- `summary` — 显示仓库的摘要信息（包括提交记录、作者及文件列表）
- `authors` — 按提交记录列出所有作者
- `changelog` — [since] 生成变更日志
- `effort` — [n] 显示提交次数最多的文件
- `fresh-branch` — [n] 从仓库的初始状态创建一个新的分支
- `ignore` — [pattern] 将指定模式添加到 `.gitignore` 文件中
- `undo` — [n] 撤销最近 n 次的提交（仅是软撤销）
- `standup` — [days] 显示过去 [days] 天内自己做了哪些工作（默认为 1 天）
- `stats` — 提供仓库的详细统计信息
- `info` — 显示仓库的版本信息

## 快速入门

```bash
git_extras.sh help
```

---
> **免责声明**：此工具为独立开发的原创作品，与所引用的开源项目无关，也未得到其授权或基于该项目进行开发。任何代码均未被复制。引用该开源项目仅用于提供背景信息。

由 BytesAgain 提供支持 | bytesagain.com | hello@bytesagain.com