---
name: wilma
version: 1.4.1
description: 您可以通过 AI 代理访问芬兰的 Wilma 学校系统。通过 `wilma CLI` 获取课程安排、作业、考试信息、成绩、通知以及最新动态。只需执行 `wilma summary --json` 命令，即可获得每日全面的学校信息；如需查看特定数据，可使用相应的命令进行查询。
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
# Wilma 技能

## 概述

Wilma 是一个芬兰的学校信息系统，学校和地方政府使用它来与家长/监护人共享消息、新闻、考试安排、作业以及其他与学生相关的更新信息。

您可以使用 `wilma` 或 `wilmai` 命令行工具（CLI）以非交互模式获取 Wilma 的数据，供 AI 代理使用。建议使用 `--json` 选项输出结果，并避免交互式提示。

## 快速入门

### 安装
```bash
npm i -g @wilm-ai/wilma-cli
```

1. 确保用户已经至少运行过一次交互式 CLI，以创建 `~/.config/wilmai/config.json` 文件。
2. 使用带有 `--json` 选项的非交互式命令来获取数据。

## 核心任务

### 每日简报（从这里开始）
```bash
wilma summary --student <id|name> --json
wilma summary --all-students --json
```
该命令可以一次性返回当天的和明天的课程安排、即将到来的考试、最近的作业、最新新闻以及最新的消息。这是为家长提供的最佳信息汇总起点。

### 课程安排
```bash
wilma schedule list --when today --student <id|name> --json
wilma schedule list --when tomorrow --student <id|name> --json
wilma schedule list --when week --student <id|name> --json
wilma schedule list --date 2026-03-10 --student <id|name> --json
wilma schedule list --weekday thu --student <id|name> --json
```
`--weekday` 选项也支持芬兰语的缩写形式：`ma`、`ti`、`ke`、`to`、`pe`、`la`、`su`。请使用 `--date` 或 `--weekday` 之一，不要同时使用两者。

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

### 获取所有学生的数据
所有列表命令都支持 `--all-students` 选项：
```bash
wilma summary --all-students --json
wilma homework list --all-students --json
wilma exams list --all-students --json
```

您也可以通过提供学生的名字片段来查询特定学生（支持模糊匹配）。

## 多因素认证（MFA）

如果 Wilma 账户启用了多因素认证（MFA）/一次性密码（TOTP）：

**交互式设置（推荐）：** 以交互模式运行 `wilma`。当检测到 MFA 时，选择“保存 TOTP 密码以实现自动登录”，然后粘贴您的 TOTP 密码或 `otpauth://` URI。未来的登录将自动完成身份验证。

**非交互式设置（一次性使用）：** 直接提供 TOTP 密码：
```bash
wilma schedule list --totp-secret <base32-key> --student "Stella" --json
wilma schedule list --totp-secret 'otpauth://totp/...' --student "Stella" --json
```
如果 TOTP 密码已经通过交互式设置保存过，则不需要使用 `--totp-secret` 选项——CLI 会从存储的配置中自动完成身份验证。

## 注意事项
- 如果未提供 `--student` 选项，CLI 会使用 `~/.config/wilmai/config.json`（或 `$XDG_CONFIG_HOME/wilmai/config.json`）文件中指定的最后一名学生。
- 如果存在多名学生且未设置默认学生，CLI 会显示一条包含所有学生名单的错误提示。
- 当账户关联多名学生时，执行读取操作时必须使用 `--student` 选项。
- 如果身份验证信息过期或 CLI 显示没有保存的配置文件，请重新以交互模式运行 `wilma`，或使用 `wilma config clear` 重置配置。
- 运行 `wilma update` 命令以更新 CLI 到最新版本。

## 行动指南（针对家长）

Wilma 中的信息包含紧急事项和一般性信息。在为家长总结信息时，请优先处理需要采取行动的事项：

**应包含的信息**：
- 需要家长采取行动或准备的事项（如填写表格、回复请求、获取许可、准备所需材料）。
- 宣布截止日期或特定时间的要求。
- 描述课程安排的变化或值得注意的事件（如外出旅行、主题日、学校停课、考试等）。
- 提及作业、考试或即将到来的截止日期。

**应省略的信息**：
- 仅提供信息但不需要家长采取任何行动、没有截止日期或对课程安排没有影响的内容。
- 与当前时间段无关的通用性公告。

如有疑问，**尽量包含所有信息**，由家长自行判断。建议提供简洁、结构清晰的总结，包括日期和具体信息来源。

## 脚本

可以使用 `scripts/wilma-cli.sh` 脚本来创建一个稳定的 CLI 使用封装层。

## 链接
- **GitHub：** https://github.com/aikarjal/wilmai
- **官方网站：** https://wilm.ai