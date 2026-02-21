---
name: solo-pipeline
description: 启动一个自动化的多技能处理流程，该流程会将多个技能链接在一起形成一个循环。当用户输入“运行流程”（run pipeline）、“将研究结果自动化并提交到产品需求文档（PRD）”（automate research to PRD）、“执行完整流程”（full pipeline）、“进行研究并验证结果”（research and validate）、“构建基础框架”（scaffold to build）或“循环执行直到完成”（loop until done）等指令时，可以使用此流程。请勿将该流程用于单一技能的处理（应直接使用相应的技能功能）。
license: MIT
metadata:
  author: fortunto2
  version: "1.2.0"
  openclaw:
    emoji: "🔄"
allowed-tools: Bash, Read, Write, AskUserQuestion
argument-hint: "research <idea> | dev <name> <stack> [--feature desc]"
---
# /pipeline

启动一个自动化的多技能流水线。所有阶段之间的技能调用都是自动完成的，无需手动干预。

## 可用的流水线

### 研究流水线
`/pipeline research "AI 治疗师应用"`

执行流程：`/research` -> `/validate`
生成文件：`research.md` -> `prd.md`

### 开发流水线
`/pipeline dev "项目名称" "技术栈"`
`/pipeline dev "项目名称" "技术栈" --feature "用户入职"`

执行流程：`/scaffold` -> `/setup` -> `/plan` -> `/build`
生成文件：包含工作流程、计划和实现的完整项目文件

## 步骤

### 1. 解析参数

从 `$ARGUMENTS` 中提取以下信息：
- 流水线类型：第一个参数（`research` 或 `dev`）
- 其他参数：传递给启动脚本

如果参数缺失或不明确，提示用户输入：

```
Which pipeline do you want to run?

1. Research Pipeline — /research → /validate (idea to PRD)
2. Dev Pipeline — /scaffold → /setup → /plan → /build (PRD to running code)
```

### 2. 与用户确认

向用户展示即将执行的操作：

```
Pipeline: {type}
Stages: {stage1} → {stage2} → ...
Idea/Project: {name}

This will run multiple skills automatically. Continue?
```

通过 `AskUserQuestion` 功能向用户确认操作内容。

### 3. 运行启动脚本

确定插件根目录（技能所在的目录）：
- 检查 `${CLAUDE_PLUGIN_ROOT}` 是否已设置（用于获取插件上下文）
- 如果未设置，则在项目目录下查找 `solo-factory/scripts/` 目录

```bash
# Research pipeline
${CLAUDE_PLUGIN_ROOT}/scripts/solo-research.sh "idea name" [--project name] --no-dashboard

# Dev pipeline
${CLAUDE_PLUGIN_ROOT}/scripts/solo-dev.sh "project-name" "stack" [--feature "desc"] --no-dashboard
```

**注意：** 在 Claude 代码技能上下文中运行时，必须使用 `--no-dashboard` 选项（`tmux` 仅用于终端使用）。

### 4. 启动第一个阶段

脚本创建状态文件后，立即运行第一个阶段的技能。
后续阶段将由 `Stop` 钩子自动处理。

- 对于研究流水线：运行 `/research "想法名称"`
- 对于开发流水线：运行 `/scaffold 项目名称 技术栈`

### 5. 流水线完成

所有阶段完成后，输出相应的结果：

```
<solo:done/>
```

`Stop` 钩子会检测到这一信号并清理状态文件。

## 状态文件

位置：`~/.solo/pipelines/solo-pipeline-{项目}.local.md`
日志文件：`~/.solo/pipelines/solo-pipeline-{项目}.log`

文件格式：使用 YAML 格式，包含阶段列表、项目根目录（`project_root`）和日志文件路径（`log_file`）字段。
每次会话退出时，`Stop` 钩子会读取该文件。

**手动取消流水线的方法：** 删除 `~/.solo/pipelines/solo-pipeline-{项目}.local.md` 文件。

## 监控

### tmux 控制台（终端使用）

当从终端启动流水线（未使用 `--no-dashboard` 选项）时，会自动打开一个 tmux 控制台：
- 第 0 个窗格：工作区
- 第 1 个窗格：日志文件的实时显示（`tail -f`）
- 第 2 个窗格：实时状态更新（每 2 秒刷新一次）

**手动控制命令：**

```bash
# Create dashboard for a pipeline
solo-dashboard.sh create <project>

# Attach to existing dashboard
solo-dashboard.sh attach <project>

# Close dashboard
solo-dashboard.sh close <project>
```

### 手动监控方式

```bash
# Colored status display
solo-pipeline-status.sh              # all pipelines
solo-pipeline-status.sh <project>    # specific pipeline

# Auto-refresh
watch -n2 -c solo-pipeline-status.sh

# Log tail
tail -f ~/.solo/pipelines/solo-pipeline-<project>.log
```

### 实时工具可视化

流水线使用 `--output-format stream-json` 格式输出数据，并通过 `solo-stream-fmt.py` 进行处理，因此工具调用会以彩色图标的形式实时显示：

```
  📖 Read ~/startups/solopreneur/4-opportunities/jarvis/research.md
  🔍 Glob "*.md" ~/startups/active/jarvis/
  💻 Bash npm test
  🌐 WebSearch voice AI agent developer tools 2026
  🤖 Task [Explore] Research task
  🔌 kb_search jarvis voice agent
```

**自定义选项：**
- 禁用颜色显示：`--no-color`
- 禁用声音效果：`--no-sound`

### 背景音乐

流水线运行期间会自动播放 8 位背景音乐（五声音阶旋律，方波音调，140 BPM）。音乐会在流程完成后停止。
音量设置为 0.08（非常轻柔）。

**手动控制音乐：** `solo-chiptune.sh start|stop|status [--volume 0.1] [--bpm 140]`

### 会话复用

重新运行流水线时，会使用现有的 tmux 会话：
- 所有窗格内容都会被清除（使用 Ctrl-C + clear）
- 日志和状态信息会重新显示
- 无需关闭或重新创建会话，只需再次运行相同的命令即可

### 日志格式

```
[22:30:15] START    | jarvis | stages: research -> validate | max: 5
[22:30:16] STAGE    | iter 1/5 | stage 1/2: research
[22:30:16] INVOKE   | /research "Jarvis voice AI agent"
[22:35:42] CHECK    | research | .../research.md -> FOUND
[22:35:42] STAGE    | iter 2/5 | stage 2/2: validate
[22:35:42] INVOKE   | /validate "Jarvis voice AI agent"
[22:40:10] CHECK    | validate | .../prd.md -> FOUND
[22:40:10] DONE     | All stages complete! Promise detected.
[22:40:10] FINISH   | Duration: 10m
```

## 重要规则

1. **启动流水线前务必确认所有参数**。
2. **不要跳过任何阶段**——`Stop` 钩子会确保流程按顺序执行。
3. **取消操作会删除状态文件**——请告知用户这一点。
4. **设置最大迭代次数**以防止无限循环（研究流水线默认为 5 次，开发流水线默认为 15 次）。
5. **在 Claude 代码技能上下文中运行时，请使用 `--no-dashboard` 选项**。