---
name: wilma
version: 1.2.0
description: 您可以通过AI代理访问芬兰的Wilma学校系统。通过wilma CLI获取课程表、作业、考试信息、成绩、通知以及最新动态。首先使用`wilma summary --json`命令获取每日概要，或者使用特定命令来查询详细数据。
metadata:
  {
    "openclaw":
      {
        "requires":
          {
            "bins": ["wilma"],
            "configPaths": ["~/.config/wilmai/config.json"],
          },
        "install":
          [
            {
              "id": "node",
              "kind": "node",
              "package": "@wilm-ai/wilma-cli",
              "bins": ["wilma"],
              "label": "Install Wilma CLI (npm)",
            },
          ],
        "credentials":
          {
            "note": "Requires a local Wilma config file (~/.config/wilmai/config.json or $XDG_CONFIG_HOME/wilmai/config.json) created by running the CLI interactively once. This stores Wilma session credentials for accessing student data.",
          },
      },
  }
---
# Wilma 功能简介

## 概述

Wilma 是一个芬兰的学校信息系统，学校和地方政府通过它向家长/监护人发送消息、新闻、考试安排、作业信息以及其他与学生相关的更新内容。

您可以使用 `wilma` 或 `wilmai` 命令行工具（CLI）以非交互式模式获取 Wilma 的数据，供 AI 代理使用。建议使用 `--json` 选项进行输出，并避免交互式提示。

## 快速入门

### 安装
```bash
npm i -g @wilm-ai/wilma-cli
```

1. 确保用户已至少运行过一次交互式 CLI，以创建 `~/.config/wilmai/config.json` 文件。
2. 使用带有 `--json` 选项的非交互式命令来获取数据。

## 核心功能

### 每日简报（从这里开始）
```bash
wilma summary --student <id|name> --json
wilma summary --all-students --json
```
该功能可以一次性返回当天的课程安排、明天的考试信息、最近的作业、最新新闻以及最新的消息。这是向家长提供信息时的最佳起点。

### 课程安排
```bash
wilma schedule list --when today --student <id|name> --json
wilma schedule list --when tomorrow --student <id|name> --json
wilma schedule list --when week --student <id|name> --json
```

### 作业
```bash
wilma homework list --student <id|name> --json
```

### 即将到来的考试
```bash
wilma exams list --student <id|name> --json
```

### 考试成绩
```bash
wilma grades list --student <id|name> --json
```

### 学生列表
```bash
wilma kids list --json
```

### 新闻和消息
```bash
wilma news list --student <id|name> --json
wilma news read <id> --student <id|name> --json
wilma messages list --student <id|name> --folder inbox --json
wilma messages read <id> --student <id|name> --json
```

### 获取所有学生的信息
所有列表命令都支持 `--all-students` 选项：
```bash
wilma summary --all-students --json
wilma homework list --all-students --json
wilma exams list --all-students --json
```

您也可以通过 `--student` 选项指定学生的名称（支持模糊匹配）。

## 注意事项
- 如果未提供 `--student` 选项，CLI 会使用 `~/.config/wilmai/config.json`（或 `$XDG_CONFIG_HOME/wilmai/config.json`）文件中最后选定的学生信息。
- 如果存在多个学生且未设置默认学生，CLI 会显示一个提示性错误并列出所有学生。
- 当账户关联多个学生时，执行读取操作时必须使用 `--student` 选项。
- 如果认证信息过期或 CLI 显示没有保存的配置文件，请重新运行交互式 `wilma` 命令，或使用 `wilma config clear` 重置配置。
- 运行 `wilma update` 命令可更新 CLI 到最新版本。

## 对家长的操作指南

Wilma 中的信息包含紧急事项和一般性通知。在向家长汇总信息时，请优先处理需要家长采取行动的内容：

**应包含的信息**：
- 需要家长采取行动或准备的事项（如填写表格、回复信息、申请权限、携带所需材料）。
- 宣布截止日期或特定时间的要求。
- 说明课程安排的变化或值得注意的事件（如外出活动、主题日、学校停课、考试等）。
- 提及作业、考试或即将到来的截止日期。

**应优先级较低的信息**：
- 仅提供信息性内容，不涉及任何需要采取行动的事项、截止日期或对课程安排的影响。
- 与当前时间段无关的通用公告。

如有疑问，请**包含所有相关信息**，由家长自行判断。建议提供简洁、结构清晰的汇总内容，包括日期和具体信息标识。

## 脚本

可以使用 `scripts/wilma-cli.sh` 脚本作为 CLI 的稳定封装工具。

## 链接
- **GitHub:** https://github.com/aikarjal/wilmai
- **官方网站:** https://wilm.ai