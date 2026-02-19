# claw-shell-kali

始终使用 TMUX 会话 `claw`。

## 目的

- 在 TMUX 会话 `claw` 内运行 shell 命令
- 绝不操作其他任何会话
- 将输出结果发送回代理

## 接口

### 工具：`claw_shell_run`

**输入参数：**

- `command`（字符串，必填）：要在会话 `claw` 内运行的 shell 命令

**执行流程：**

1. 连接到 tmux 会话 `claw`（如果会话不存在，则创建它：`tmux new -s claw -d`）。
2. 发送命令并按下 Enter 键。
3. 捕获该命令的执行结果（即会话中的输出）。
4. 将捕获到的输出结果发送回代理。

## 安全性注意事项

- **禁止执行的命令：**
  - `sudo`
  - `rm`（未经明确用户授权的情况下）
  - `reboot`、`shutdown` 或其他可能对系统造成破坏的命令
- **如果命令包含上述任何内容：**
  - 在执行前需要用户确认。

## 示例

- **安全操作：**
  - `ls -la`
  - `bird read https://x.com/...`
  - `git status`

- **危险操作（执行前需确认）：**
  - `rm -rf ...`
  - `docker system prune -a`
  - `chmod -R ...`