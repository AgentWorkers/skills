---
name: cancel
description: 通过 `/cancel` 命令，可以根据运行 ID (`run-id`) 取消正在进行的交互式调度任务。当用户需要立即停止调度任务或 Ralph-Loop 任务时，可以使用此命令。
---
运行 `{baseDir}/scripts/run_cancel.sh` 命令，并传入用户提供的参数。

## 命令格式

- 命令格式：`/cancel <run-id>`
- 也支持：`/cancel <project>/<run-id>`

## 本地配置

- 可选的环境文件：`${OPENCLAW_DISPATCH_ENV:-<workspace>/skills/dispatch.env.local}`
- 支持从 `OpenClaw` 的 `skills.entries.cancel.env` 文件中读取配置信息
- 该脚本是独立运行的（无需依赖其他外部组件）

## 安全性说明

- 仅从 `dispatch.env.local` 文件中读取经过键值对格式化处理的允许访问的环境变量（不直接读取文件内容）。
- 仅将 tmux 相关的操作（如按键输入）发送到根据本地元数据确定的会话中。
- 更新会话的元数据（状态设置为 `cancelled`，退出代码设置为 `130`）。

## 动作流程

1. 将 `run-id` 解析为对应的运行结果目录。
2. 向该 tmux 会话发送 `/ralph-loop:cancel-ralph` 命令。
3. 通过发送 `/exit` 命令强制终止 tmux 会话。
4. 返回操作是否成功或详细的错误信息。