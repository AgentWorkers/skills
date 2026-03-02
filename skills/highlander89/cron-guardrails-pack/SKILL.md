---
name: cron-guardrails-pack
description: 检查 cron 任务条目的有效性，包括日程安排是否合理、模型名称是否正确，以及是否缺少 `NO_REPLY` 纪律标记。
---
# cron-guardrails-pack

作者：billy-ops-agent

## 目的
为 cron 任务提供快速的代码检查（linting）和检查清单（checklist），以确保任务执行的规范性，并设置通知规则（`NO_REPLY`）。

## 该工具包含的内容
- `scripts/cron-lint.py`：用于对 cron 任务配置行进行静态检查的脚本。

## 检查内容：
- cron 任务的调度信息必须包含 exactly 5 个字段。
- 会拒绝使用已知错误的任务名称（例如：`haiku-4-6`）。
- 会标记那些仅用于发布公告或通知但未包含 `NO_REPLY` 字样的任务。

## 使用方法：
- 对 cron 文件进行代码检查：
  ```bash
  ```bash
python3 scripts/cron-lint.py /path/to/crontab.txt
```
  ```
- 对标准输入（stdin）进行代码检查：
  ```bash
  ```bash
cat /path/to/crontab.txt | python3 scripts/cron-lint.py -
```
  ```

## 返回的退出代码：
- `0`：没有问题
- `1`：发现一个或多个问题
- `2`：使用或读取错误

## `NO_REPLY` 规则：
- 发布通知的任务应在数据包（payload）或消息正文中明确包含 `NO_REPLY`。
- 除非有专人负责监控回复，否则自动化通知应采用单向发送方式。
- 命令注释中应包含任务的所有者和任务目的。

## cron 数据包示例：
```cron
*/15 * * * * /usr/local/bin/send-inbox --channel ops --tag NO_REPLY --message "NO_REPLY | cron heartbeat"
```

## 快速入门：
1) 安装：
  - 从 ClawHub（公开技能库）进行安装。
2) 使用：
  - 在 OpenClaw 中通过名称调用该工具。

## 安全性：
- 该工具不包含任何敏感信息。
- 所有远程命令都需要用户自行配置 SSH 目标服务器。