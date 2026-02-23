---
name: solo-pipeline
description: 启动一个自动化的多技能处理流程，该流程会将多个技能串联起来形成一个循环。当用户输入“运行流程”（run pipeline）、“将研究结果自动化处理并提交到产品需求文档（PRD）”（automate research to PRD）、“执行完整流程”（full pipeline）、“进行研究并验证结果”（research and validate）、“构建基础框架”（scaffold to build）或“持续循环执行直至完成”（loop until done）等指令时，应使用此流程。请勿将该流程用于单个技能的处理（应直接使用相应的技能功能）。
license: MIT
metadata:
  author: fortunto2
  version: "1.4.0"
  openclaw:
    emoji: "🔄"
allowed-tools: Bash, Read, Write, AskUserQuestion
argument-hint: "research <idea> | dev <name> <stack> [--feature desc]"
---
# /pipeline

启动一个自动化的多技能流水线。所有阶段之间的技能调用都是自动完成的，无需手动干预。

## 可用的流水线

### 研究流水线
`/pipeline research "AI therapist app"`

执行流程：`/research` -> `/validate`
生成文件：`research.md` -> `prd.md`

### 开发流水线
`/pipeline dev "project-name" "stack"`
`/pipeline dev "project-name" "stack" --feature "user onboarding"`

执行流程：`/scaffold` -> `/setup` -> `/plan` -> `/build`
生成包含工作流程、计划和实现的完整项目文件

## 步骤

### 1. 解析参数

从 `$ARGUMENTS` 中提取以下信息：
- 流水线类型：第一个参数（`research` 或 `dev`）
- 其余参数：传递给启动脚本

如果参数缺失或不明确，请提示用户输入：

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

通过 `AskUserQuestion` 功能向用户确认操作。

### 3. 启动第一个阶段

直接运行流水线中的第一个技能：
- 对于研究流水线：运行 `/research "idea name"`
- 对于开发流水线：运行 `/scaffold project-name stack`

如果配置了 `Stop` 钩子，后续阶段将自动执行；
如果没有 `Stop` 钩子，则需要手动依次执行每个技能。

### 3b. 启动脚本（可选，仅适用于 Claude Code 插件）

如果安装了 `solo-factory` 插件，启动脚本会提供 tmux 仪表板和日志记录功能：

```bash
# Only available with Claude Code plugin — skip if not installed
solo-research.sh "idea name" [--project name]
solo-dev.sh "project-name" "stack" [--feature "desc"]
```

在技能上下文中运行时，可以使用 `--no-dashboard` 选项来禁用仪表板。

### 5. 流水线完成

所有阶段完成后，输出相应的结果：

```
<solo:done/>
```

`Stop` 钩子会检测到这一信号，并清理状态文件。

## 状态文件

状态文件的位置：
- 本地项目：`.solo/pipelines/solo-pipeline-{project}.local.md`
- 全局项目：`~/.solo/pipelines/solo-pipeline-{project}.local.md`
日志文件：`.solo/pipelines/solo-pipeline-{project}.log`

文件格式：YAML 格式，包含阶段列表、`project_root` 和 `log_file` 字段。
`Stop` 钩子在每次会话退出时都会读取该文件。

要手动取消流水线，请删除状态文件 `solo-pipeline-{project}.local.md`。

## 监控

### tmux 仪表板（终端使用）

当从终端启动流水线（未使用 `--no-dashboard` 选项）时，会自动打开 tmux 仪表板：
- 第 0 面板：工作区
- 第 1 面板：日志文件的实时显示（每 2 秒更新一次）
- 第 2 面板：状态信息（实时更新）

### 手动监控

可以使用标准工具监控流水线的进度：

```bash
# Watch log file
tail -f .solo/pipelines/solo-pipeline-<project>.log

# Check pipeline state

# Auto-refresh
watch -n2 -c solo-pipeline-status.sh
```

### 会话重用

重新运行流水线时会复用之前的状态信息，已完成的阶段会自动跳过。
无需关闭或重新创建环境，只需再次运行相同的命令即可。

### 日志格式

```
[22:30:15] START    | my-app | stages: research -> validate | max: 5
[22:30:16] STAGE    | iter 1/5 | stage 1/2: research
[22:30:16] INVOKE   | /research "AI therapist app"
[22:35:42] CHECK    | research | .../research.md -> FOUND
[22:35:42] STAGE    | iter 2/5 | stage 2/2: validate
[22:35:42] INVOKE   | /validate "AI therapist app"
[22:40:10] CHECK    | validate | .../prd.md -> FOUND
[22:40:10] DONE     | All stages complete! Promise detected.
[22:40:10] FINISH   | Duration: 10m
```

## 重要规则

1. **启动流水线前务必确认所有参数**。
2. **不要跳过任何阶段**——`Stop` 钩子会确保流程按顺序执行。
3. **取消操作需删除状态文件**——请告知用户这一操作。
4. **设置最大迭代次数**以防止无限循环（研究流水线默认为 5 次，开发流水线默认为 15 次）。
5. **在 Claude Code 技能上下文中运行时，请使用 `--no-dashboard` 选项**。