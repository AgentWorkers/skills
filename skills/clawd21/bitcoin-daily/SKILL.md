---
name: bitcoin-daily
description: 比特币开发邮件列表及Bitcoin Core代码提交的每日摘要。适用于需要了解近期比特币开发讨论、邮件列表活动、Bitcoin Core代码变更情况时，或用于生成每日总结。数据来源于groups.google.com/g/bitcoindev上的讨论帖以及github.com/bitcoin/bitcoin上的代码提交记录。
metadata: {"clawdbot":{"emoji":"📰"}}
---

# 每日比特币开发动态（📰）

![比特币每日更新](https://files.catbox.moe/v0zvnj.png)

每日汇总比特币开发邮件列表（bitcoindev mailing list）的讨论内容以及比特币核心（Bitcoin Core）的代码提交信息。

*制作于 🤠 德克萨斯州 ❤️ [PlebLab](https://pleblab.dev)*

## 命令

使用以下命令运行脚本：`node ~/workspace/skills/bitcoin-daily/scripts/digest.js <command>`

| 命令 | 描述 |
|---------|-------------|
| `digest [YYYY-MM-DD]` | 获取并汇总指定日期的邮件列表内容（默认为昨日） |
| `archive` | 列出所有已归档的每日汇总报告 |
| `read <YYYY-MM-DD>` | 读取指定日期的每日汇总报告 |

## 输出格式

该脚本会获取原始数据，然后以以下格式为用户生成汇总内容：

**邮件列表：** 每条内容包含：
- **加粗的标题** — 用简洁明了的语言（1-2句话）解释相关内容，并加入一些幽默元素 |
- 相关邮件讨论的链接

**代码提交：** 显示重要的代码合并内容及其对应的Pull Request（PR）链接。

确保汇总内容易于阅读——假设读者对比特币有一定了解，但不是比特币核心项目的贡献者。幽默元素欢迎使用，但无需刻意为之。

## 归档

原始数据会被存档到 `~/workspace/bitcoin-dev-archive/YYYY-MM-DD/` 目录下：
- `mailing-list/*.json` — 每个主题的完整邮件讨论内容 |
- `mailing-list/_index.json` — 邮件讨论的索引文件 |
- `commits.json` — 原始的代码提交数据 |
- `summary.md` — 生成的汇总报告

## 日常调度

通过 Clawdbot 的 cron 任务每天早上自动运行该脚本。脚本会获取数据、进行归档并生成汇总报告，随后由系统发送给用户。

## 数据来源：
- 比特币开发邮件列表：https://groups.google.com/g/bitcoindev |
- 比特币核心项目代码库：https://github.com/bitcoin/bitcoin/commits/master/