---
name: openclaw-model-failover
slug: openclaw-model-failover
description: "OpenClaw插件：自动检测速率限制、配额限制或身份验证失败的情况，并将会话切换到备用的大型语言模型（LLM）。通过修复被固定的会话模型，该插件可以防止出现“API速率限制已达到”的循环错误。"
---
# openclaw-model-failover（OpenClaw插件）

这是一个**OpenClaw网关插件**，而非代理技能。

该插件通过自动切换对话所使用的模型来缓解服务中断情况。当检测到以下问题时，它会执行切换：
- 速率限制/配额耗尽（HTTP 429，RESOURCE_EXHAUSTED）
- 认证/权限失败（例如：OpenAI返回`apiresponses.write`错误）

## 安装

### 选项A：使用ClawHub

```bash
clawhub install openclaw-model-failover
```

### 选项B：从仓库（开发版本）安装

```bash
openclaw plugins install -l ~/.openclaw/workspace/openclaw-model-failover
openclaw gateway restart
```

## 配置

设置模型切换的优先级（示例）：
- Anthropic -> OpenAI -> Google

有关完整的配置信息，请参阅README文件。