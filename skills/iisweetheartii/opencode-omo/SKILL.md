---
name: opencode-omo
description: 使用 OpenCode 和 Oh-My-OpenCode（基于 Sisyphus、Prometheus、Atlas 的框架）作为编程后端。遵循“Sisyphus 先于其他组件”的工作流程。
homepage: https://github.com/IISweetHeartII/openclaw-skills
metadata: {"openclaw":{"emoji":"🧱","category":"devtools","tags":["opencode","oh-my-opencode","sisyphus","coding"],"requires":{"bins":["opencode","git","clawhub"]}}}
---
# OpenCode + Oh-My-OpenCode 操作指南

本操作指南介绍了如何使用 **OpenCode** 进行规划与编码工作，同时 **Oh-My-OpenCode** 提供了 Sisyphus/Prometheus/Atlas 工作流程来辅助这些任务。

## 核心规则

- 除非特别要求，否则不要在 OpenCode 之外直接编辑代码。
- 对于编码任务，优先使用 Sisyphus 进行任务执行。
- 对于复杂的工作：先使用 Prometheus (`@plan`) 进行规划，然后再使用 Atlas (`/start-work`) 来执行计划。

## 快速命令

### 检查 Oh-My-OpenCode 插件是否已安装

```bash
cat ~/.config/opencode/opencode.json | sed -n '1,120p'
```

你应该能在 `plugin` 列表中看到 `"oh-my-opencode"`。

### 运行一次性编码任务（Sisyphus + ultrawork）

```bash
opencode run --agent sisyphus "ulw <your request>"
```

### 启动交互式 OpenCode（Sisyphus）

```bash
opencode --agent sisyphus
```

在 OpenCode 中：

- 使用 `@plan "..."` 来调用 Prometheus 进行规划。
- 使用 `/start-work` 来让 Atlas 执行规划结果。

## 故障处理

- 如果代理在执行过程中提出问题，请在规划模式（Prometheus）下回答问题，然后重新运行任务。
- 如果需要更确定的结果，可以使用 `ulw` 并提交更具体、更明确的请求来重新执行任务。