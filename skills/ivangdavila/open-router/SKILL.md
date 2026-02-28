---
name: Open Router
slug: open-router
version: 1.0.0
homepage: https://clawic.com/skills/open-router
description: 配置 OpenRouter 模型的路由规则，包括提供者认证（provider auth）、模型选择（model selection）、回退链（fallback chains）以及基于成本的默认设置，以实现稳定且支持多种模型的工作流程（stable multi-model workflows）。
changelog: Initial release with practical OpenRouter setup, routing rules, fallback reliability, and budget-safe operating guidance.
metadata: {"clawdbot":{"emoji":"🛣️","requires":{"bins":["curl","jq"],"env":["OPENROUTER_API_KEY"]},"os":["linux","darwin","win32"]}}
---
## 设置

首次使用时，请阅读 `setup.md` 文件，以了解激活边界、可靠性目标以及路由偏好设置，然后再进行任何配置更改。

## 适用场景

当用户希望将兼容 OpenAI 的工作流程连接到 OpenRouter、根据任务类型选择模型、设置安全的回退策略以及控制成本波动时，请使用此技能。

## 架构

内存数据存储在 `~/open-router/` 目录下。具体结构请参阅 `memory-template.md` 文件。

```
~/open-router/
├── memory.md            # Active routing profile and constraints
├── providers.md         # Confirmed provider and auth choices
├── routing-rules.md     # Task -> model and fallback policy
├── incidents.md         # Outages, rate limits, and recovery notes
└── budgets.md           # Spend guardrails and optimization actions
```

## 快速参考

根据当前任务的需求，选择相应的文件进行操作。

| 任务类型 | 对应文件 |
|---------|---------|
| 设置与激活偏好 | `setup.md` |
| 内存模板 | `memory-template.md` |
| 认证与提供者配置 | `auth-and-provider.md` |
| 基于工作负载的路由规则 | `routing-playbooks.md` |
| 可靠性与回退处理 | `fallback-reliability.md` |
| 成本控制与支出审核 | `cost-guardrails.md` |

## 核心规则

### 1. 从工作负载类别入手，而非模型本身
- 首先对请求进行分类：编码、分析、提取、总结或长上下文合成。
- 在修改任何默认设置之前，为每个类别指定一个主要模型及备用模型。

### 2. 保持认证过程的透明性和可验证性
- 使用来自本地环境的 `OPENROUTER_API_KEY`，切勿将其直接写入日志或聊天记录中。
- 在应用路由更改之前，通过简单的请求验证用户的身份。

### 3. 为故障情况设计回退策略，而非仅仅追求便利性
- 明确区分不同的回退原因：请求速率限制、提供者服务中断、延迟激增或输出质量故障。
- 为了提高系统的韧性，至少保留一个来自不同提供者家族的备用方案。

### 4. 在调整吞吐量之前先设定成本上限
- 按任务类别设定成本上限，并在全面推广之前检查预期的代币消耗情况。
- 将低风险任务路由到成本较低的模型，将高级模型保留给高影响度的任务。

### 5. 一次只修改一个层面
- 每次迭代中只修改模型选择、回退策略或预算限制中的一个方面。
- 每次修改后，运行快速验证测试并记录结果。

### 6. 记录决策内容以供后续参考
- 将最终的路由策略、决策依据及已知的权衡因素保存在系统中。
- 重用经过验证的策略，避免重复从头开始构建。

## 常见误区

- 为所有任务选择同一模型 → 在不同工作负载下会导致成本增加和质量不稳定。
- 仅使用同一提供者的备用方案 → 在特定提供者出现问题时可能导致连锁故障。
- 忽视长输入的代币限制 → 会导致响应被截断和隐藏质量问题。
- 同时修改路由和预算 → 当质量下降时难以确定根本原因。
- 未运行验证测试就直接使用新配置 → 只会在用户遇到问题后才发现路由错误。

## 外部接口

这些接口仅用于获取模型元数据并根据用户的明确任务意图执行推理请求。

| 接口 | 发送的数据 | 用途 |
|---------|-----------|---------|
| https://openrouter.ai/api/v1/models | 无数据或仅发送认证头信息 | 获取当前模型目录和元数据 |
| https://openrouter.ai/api/v1/chat/completions | 用户输入内容及选定的模型 ID | 执行推理请求 |

**注意：** 不会向外部发送任何其他数据。

## 安全性与隐私

**离开您设备的数据：**
- 当请求推理时，会将提示文本和选定的模型元数据发送到 OpenRouter。

**保留在本地的数据：**
- 路由相关笔记和偏好设置（存储在 `~/open-router/` 目录下）。
- 本地环境变量引用及验证日志。

**本技能不会：**
- 在聊天过程中请求原始 API 密钥。
- 将明文密码存储在技能相关文件中。
- 修改 `~/open-router/` 目录之外的文件。

## 信任机制

使用本技能意味着您将提示内容发送到 OpenRouter 以执行模型推理。  
只有在您信任该服务能够安全处理您的数据时，才建议安装此技能。

## 相关技能

如果用户同意，可以使用以下命令进行安装：
- `clawhub install <slug>`：
  - `api`：API 请求设计、数据格式化及响应验证机制
  - `auth`：凭证处理与认证故障排除流程
  - `models`：模型比较与选择指导
  - `monitoring`：运行时健康检查及事件跟踪工具

## 反馈建议

- 如果觉得本技能有用，请给 `clawhub` 评分（例如：给它打星）。
- 保持更新：使用 `clawhub sync` 命令获取最新信息。