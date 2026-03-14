---
name: auto-updater
description: "**自动更新 OpenClaw 及已安装的技能**  
适用于设置或维护每日/每周的自动更新机制时，用于检查 OpenClaw 的更新情况、更新所有技能，并发送更新内容的汇总信息。"
metadata: {"version":"1.0.1","openclaw":{"emoji":"🔄","os":["darwin","linux"]}}
---
# 自动更新技能

通过定期更新机制，确保 OpenClaw 及已安装的技能始终保持最新状态。

## 功能概述

该技能用于设置自动化任务，以实现以下功能：
1. 更新 OpenClaw 本身；
2. 通过 ClawHub 更新已安装的技能；
3. 发送更新内容的简要摘要。

## 推荐的 OpenClaw 更新方式

对于当前的 OpenClaw 版本，建议使用 **cron 工具/调度程序**，而非旧的 `clawbot` 或 `clawdbot` 命令行界面（CLI）方法。

建议使用 **独立的定时任务** 来执行以下操作：
1. 运行 `openclaw update`（或 `openclaw update --dry-run` 用于仅预览更新过程）；
2. 运行 `clawhub update --all`；
3. 如果更新过程中发现配置或服务问题，可选地运行 `openclaw doctor`；
4. 向用户发送简短的更新总结。

## 核心命令

### OpenClaw 更新

**推荐命令：**
```bash
openclaw update
```

**其他可用命令：**
```bash
openclaw update status
openclaw update --dry-run
openclaw update --json
openclaw doctor
```

**注意事项：**
- `openclaw update` 是当前推荐的更新方式；
- 在通过源代码安装 OpenClaw 时，该命令会处理安全的更新流程；
- 在通过包管理器安装时，该命令会使用包管理器提供的更新机制；
- `openclaw doctor` 主要用于检查系统健康状况或进行故障排查，而非直接执行更新操作。

### 技能更新

```bash
clawhub update --all
clawhub list
```

## 安排更新任务的指导原则

在配置 OpenClaw 的自动更新功能时：
- 建议使用 **cron 工具**，而非旧的 `openclaw cron add` 或 `clawdbot cron add` 命令；
- 创建一个独立的定时任务；
- 向用户提供详细的更新摘要；
- 如果用户未指定具体时间，建议选择用户所在时区内的非高峰时段来执行更新任务。

## 建议的定时任务提示语

可以使用以下提示语来安排更新任务：
```text
Run the scheduled OpenClaw maintenance routine:

1. Check/update OpenClaw with `openclaw update`
2. Update installed skills with `clawhub update --all`
3. If update output suggests config or service problems, run `openclaw doctor`
4. Summarize:
   - whether OpenClaw changed
   - which skills updated
   - any failures or manual follow-up needed

Keep the final report concise and user-facing.
```

## 更新内容格式

更新内容的格式应便于阅读：
- 显示版本号变更信息；
- 将已更新的技能分组显示；
- 清晰地列出出现的错误；
- 避免使用冗长的原始日志。

## 手动检查步骤

```bash
openclaw update status
openclaw status
clawhub list
```

## 故障排除

### 更新失败时

请检查以下内容：
1. `openclaw update status` 的输出；
2. `openclaw doctor` 的运行结果；
3. `openclaw gateway status` 的状态；
4. `clawhub list` 的输出。

### 技能更新失败的原因

常见原因包括：
- 网络故障；
- 注册表或包解析问题；
- 已安装技能中的文件被修改；
- 工作区权限问题。

针对这些问题，可以尝试以下解决方法：
```bash
clawhub update --all --force
```

或者，也可以选择单独更新某个具体的技能。

## 关于旧版文档的说明

如果旧版文档中提到了以下命令，请按以下方式翻译：
- `clawdbot`/`clawbot` → `openclaw`；
- `clawdhub` → `clawhub`；
- 将 `clawdbot doctor` 作为更新工具的描述改为 “`openclaw update`”（用于故障排查）；
- 旧版的 CLI 安排更新任务的示例应替换为 “OpenClaw 的 cron 工具/调度程序”。

## 参考资源

- OpenClaw 更新相关文档：本地 OpenClaw 安装目录下的 `docs/cli/update.md`；
- OpenClaw 的状态检查/故障排查相关文档：本地 OpenClaw 文档；
- 用于安装/更新技能的 ClawHub CLI 命令：[ClawHub 文档](...)