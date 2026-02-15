---
name: discord-context
description: 管理 Discord 论坛帖子的上下文信息。将 QMD 内容预先加载到帖子中，以便 AI 能够理解帖子的背景和上下文。
metadata:
 {
   "openclaw": {
     "requires": { "bins": ["curl"] },
     "user-invocable": true
   }
 }
---
# discord-context

该技能用于管理 Discord 论坛帖子的上下文信息，通过预加载 QMD（Q&A Markdown 文件）内容来提升 AI 的上下文感知能力。

## 设置要求

- 需要在 OpenClaw 中配置 Discord 机器人的访问令牌。
- 确保系统中可执行 `curl` 命令。
- OpenClaw 工作空间默认位于 `~/.openclaw/workspace`。

该技能依赖以下目录：
- 缓存目录：`memory/discord-cache/`
- QMD 文件存储路径：`memory/*.md`

## 斜杠命令（Slash Commands）

当用户输入 `/discord-context <args>` 时，系统将按照以下规则进行处理：

### `/discord-context poll`
- 执行轮询脚本并显示结果。
```
Run: node {baseDir}/scripts/discord-context-cli.js poll
```

### `/discord-context context`
- 列出所有已缓存的帖子及其对应的上下文信息。
```
Run: node {baseDir}/scripts/discord-context-cli.js context
```

### `/discord-context context <thread_id>`
- 显示指定帖子的上下文信息。
```
Run: node {baseDir}/scripts/discord-context-cli.js context <thread_id>
```

### `/discord-context link <thread_id> <qmd_name>`
- 将 QMD 文件链接到相应的帖子中。
```
Run: node {baseDir}/scripts/discord-context-cli.js link <thread_id> <qmd_name>
```

### `/discord-context help`
- 显示帮助信息。

## 使用示例

```
/discord-context poll
/discord-context context
/discord-context context 1472595645192867983
/discord-context link 1472595645192867983 skills
```

## 工作原理

1. **轮询**：每 2 小时通过 cron 任务检查 agent-hub 论坛中的新内容，并加载相应的 QMD 文件。
2. **缓存**：将帖子的上下文信息存储在 `memory/discord-cache thread-{id}-context.txt` 文件中。
3. **按需显示**：根据用户请求，将缓存的信息插入到帖子中。

## 帖子与 QMD 文件的映射关系

帖子名称与 QMD 文件的映射关系如下（使用空格分隔的多个部分用破折号 `-` 连接）：
- `Skills` → `memory/skills.md`
- `Mission Control` → `memory/mission-control.md`
- `Philosophy time` → `memory/philosophy-time.md`
- `DOCUMENTATION` → `memory/documentation.md`
- `Nightly Work` → `memory/nightly-work.md`
- `mc-refactor-14022026` → `memory/mc-refactor-14022026.md`

## 实现细节

该技能包含以下组件：
- `scripts/discord-context-cli.js`：主要的命令行接口（CLI）入口文件。
- `scripts/discord-context-poll.sh`：用于执行轮询任务的脚本（由 cron 任务触发）。

缓存目录：`memory/discord-cache/`

## 安装说明

安装完成后，请执行以下操作：
1. 确保您的 Discord 机器人具有访问论坛频道的权限。
2. 如有需要，在轮询脚本中配置论坛频道的 ID。
3. 在 `memory/` 目录下创建与帖子名称对应的 QMD 文件。
4. （可选）设置 cron 任务，使脚本每 2 小时执行一次轮询操作。