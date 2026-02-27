---
name: dispatch
description: 通过 `/slash` 命令调度来启动非阻塞式的 Claude 代码无头任务。适用于用户请求异步编程任务且不需要仅依赖 `/slash` 命令的 Claude 插件的情况。
---
运行 `{baseDir}/scripts/run_dispatch.sh`，并传递用户提供的参数。

## 命令格式

命令格式为：`/dispatch <项目名称> <任务名称> <提示信息...>`

- 工作目录映射：`${REPOS_ROOT:-/home/miniade/repos}/<项目名称>`

- 代理团队策略：按需启动（仅当提示信息中包含代理团队相关指令时才会启用）

- 安全性：无头模式运行时，会通过 `DISPATCH_TIMEOUT_SEC`（默认值为 7200 秒）来强制设置超时时间

## 本地配置

- 可选的环境配置文件：`${OPENCLAW_DISPATCH_ENV:-<工作空间>/skills/dispatch.env.local}`

- 支持从 `OpenClaw` 的 `skills.entries.dispatch.env` 文件中注入配置信息

- 该脚本为独立可执行的文件（包含 `dispatch.sh` 和 `claude_code_run.py`）

## 安全性说明

- 仅从 `dispatch.env.local` 文件中读取经过键值对格式化处理的允许访问的环境变量（不支持读取源代码内容）

- 脚本会在后台运行（使用 `nohup` 命令），并将日志和结果写入指定的路径

- 网络回调功能默认是禁用的；只有在设置了 `ENABLE_CALLBACK=1` 且相关组配置允许的情况下才能启用

- 脚本在运行过程中不会下载远程代码

## 动作流程

1. 验证输入参数；如果参数不完整，会返回使用说明
2. 在后台启动任务（非阻塞方式）
3. 返回包含任务运行 ID 和日志路径的简短摘要信息
4. 除非用户明确要求，否则不会执行额外的验证步骤