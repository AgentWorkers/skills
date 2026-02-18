---
name: opencode-omo
version: 0.3.0
description: 将编码请求转化为实际完成的工作。使用 Prometheus 进行规划，通过 Atlas 执行任务，并利用 OpenCode 中的 Sisyphus 功能进行迭代开发。
homepage: https://github.com/IISweetHeartII/opencode-omo
metadata:
  openclaw:
    emoji: "🧱"
    category: devtools
    requires:
      bins:
        - opencode
        - git
        - clawhub
    tags:
      - opencode
      - oh-my-opencode
      - sisyphus
      - coding
      - workflow
---
# OpenCode + Oh-My-OpenCode 操作指南

本操作指南介绍了如何将 **OpenCode** 作为编程运行时环境，并通过 **Oh-My-OpenCode** 结合 Sisyphus、Prometheus 和 Atlas 进行代码编排。

## 本技能为您提供的功能

- 使用 `ulw` 实现一次性代码执行，以满足特定的编码需求。
- 通过 `@plan` 和 `/start-work` 命令实现计划到执行的完整工作流程。
- 提供可重复的默认设置，确保每次代码执行的质量保持一致。

## 核心规则

- 除非另有明确指示，否则请勿直接在 OpenCode 之外编辑代码。
- 对于编码任务，优先使用 Sisyphus 进行任务调度。
- 对于复杂的项目：先使用 Prometheus (`@plan`) 进行计划，再使用 Atlas (`/start-work`) 进行执行。

## 快速入门

### 验证 Oh-My-OpenCode 插件

```bash
cat ~/.config/opencode/opencode.json | grep "oh-my-opencode"
```

如果命令返回了输出结果，说明插件已成功安装。
您还可以运行内置的检测工具：

```bash
./scripts/check-omo.sh
```

### 执行一次性编码任务（Sisyphus + ultrawork）

```bash
opencode run --agent sisyphus "ulw implement JWT auth in this service and add tests"
```

或者使用内置的辅助工具：

```bash
./scripts/run-ulw.sh "implement JWT auth in this service and add tests"
```

### 启动交互式 OpenCode （Sisyphus）

```bash
opencode --agent sisyphus
```

在 OpenCode 内部：
- 使用 `@plan "..."` 命令来触发 Prometheus 的计划生成。
- 使用 `/start-work` 命令让 Atlas 执行该计划。

## 故障处理

- 如果在执行过程中代理程序提出疑问，请在计划模式（Prometheus）下回答问题，然后重新执行任务。
- 如果需要更可靠的结果，请使用 `ulw` 并提交更具体、更明确的请求来重新执行任务。

## 与其他技能的集成

- **[agent-selfie](https://clawhub.org/skills/agent-selfie)**：将结构化的编码工作流程与生成的视觉资产相结合。
- **[gemini-image-gen](https://clawhub.org/skills/gemini-image-gen)**：使用相同的工作流程自动化机制生成图像。
- **[agentgram](https://clawhub.org/skills/agentgram)**：发布工作流程运行产生的进度更新、结果和演示内容。

## 更新记录

- v0.3.0：增加了双向生态系统链接和内置的工作流程辅助脚本。
- v0.2.0：重新设计了用户界面、快速入门流程和元数据，以便用户更轻松地了解该技能的功能。
- v0.1.0：首次发布，包含 Sisyphus/Prometheus/Atlas 的工作流程使用指南。