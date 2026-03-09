---
name: em-intel
description: **工程经理智能工具：** 该工具可用于跟踪团队绩效、工程师的贡献情况以及项目的整体运行状况，数据来源于 GitLab/GitHub 和 Jira/GitHub Issues。适用于需要晨会简报、每日工作回顾、团队报告、针对特定工程师的提醒、项目健康状况检查或每周新闻通讯的场景。通过分析功能分支，可以将工程师的贡献情况与 Jira 票据关联起来。支持通过 Slack、Telegram 和电子邮件进行信息推送。触发命令包括：/morning-brief、/eod-review、/team-report、"谁参与了 X 项目的开发"、"哪些任务处于停滞状态"、"发送新闻通讯"、"团队绩效分析"。
license: MIT
metadata:
  author: larry.l.fang@gmail.com
  version: "1.0.0"
  tags: engineering-manager,gitlab,github,jira,team-performance,morning-brief,eod-review,newsletter,dora
---
# em-intel — 工程经理智能系统

该系统用于跟踪团队绩效、工程师的贡献情况以及项目的整体状态，数据来源于 GitLab/GitHub 和 Jira/GitHub Issues。

## 快速入门

```bash
# Copy and fill environment variables
cp .env.example .env

# Install dependencies
pip install -r requirements.txt

# Run morning brief
python em_intel.py morning-brief

# Full help
python em_intel.py --help
```

## 命令

| 命令          | 描述                                      |
|---------------|-------------------------------------------|
| `morning-brief`   | 昨天合并的代码、超过 3 天未处理的 PR、未活跃的工程师、停滞的项目（epic） |
| `eod-review`    | 今日的合并操作、贡献者列表、代码开发周期趋势           |
| `team-report [--days N]` | 全部团队绩效报告                         |
| `contributions [--engineer NAME] [--days N]` | 某工程师在指定时间段内的分支到工单的贡献情况       |
| `quiet-engineers` | 3 天内未提交任何合并请求的工程师             |
| `epic-health`    | 停滞且未分配给任何工程师的项目（epic）                   |
| `newsletter [--week]` | 通过配置的渠道发送每周汇总信息                   |

## 配置

将 `EM_CODE_PROVIDER` 设置为 `gitlab` 或 `github`，将 `EM.TickET_PROVIDER` 设置为 `jira` 或 `github_issues`。

支持的消息传递渠道：`telegram`、`slack`、`email` 或 `print`（默认为 `stdout`）。

详细配置选项请参见 `.env.example` 文件。

## 架构

```
em_intel.py          ← CLI entrypoint (argparse)
adapters/            ← Code platform + ticket system adapters
  base.py            ← Abstract base classes & data models
  gitlab_adapter.py  ← GitLab REST API
  github_adapter.py  ← GitHub REST API
  jira_adapter.py    ← Jira REST API
  github_issues_adapter.py ← GitHub Issues as ticket system
core/                ← Business logic
  branch_mapper.py   ← Map branches → tickets → engineers
  team_pulse.py      ← Quiet engineers, MR trends, cycle times
  jira_health.py     ← Stale epics, unassigned tickets, PR age
  newsletter.py      ← Weekly digest generation
  delivery.py        ← Telegram / Slack / Email / Print routing
commands/            ← Command implementations
  morning_brief.py   ← Morning briefing
  eod_review.py      ← End-of-day review
  team_report.py     ← Full team report
  newsletter.py      ← Newsletter generation & delivery
```