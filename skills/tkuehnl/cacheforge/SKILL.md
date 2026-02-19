---
name: cacheforge
version: 1.0.0
description: CacheForge 的核心功能包括：为与 OpenAI 兼容的令牌优化网关提供初始设置（bootstrap onboarding）、运维支持（ops）以及性能统计（stats）服务。通过使用 CacheForge，您可以将大型语言模型（LLM）的使用成本降低多达 30%（具体效果因服务提供商和工作负载而异）。
author: CacheForge
license: MIT
homepage: https://app.anvil-ai.io
user-invocable: true
tags:
  - cacheforge
  - ai-agents
  - token-optimization
  - llm
  - cost-reduction
  - openai
  - proxy
  - gateway
  - discord
  - discord-v2
metadata: {"openclaw":{"emoji":"🧠","homepage":"https://app.anvil-ai.io"}}
---
## 目的

`cacheforge` 是主要的入口技能。请先安装此技能。

首次使用时，如果缺少相关技能，`cacheforge` 会自动安装以下辅助技能：
- `cacheforge-setup`
- `cacheforge-ops`
- `cacheforge-stats`

之后，`cacheforge` 会根据用户请求将用户引导至相应的功能模块：
- 设置/入职流程 -> `cacheforge-setup`
- 账费/上游服务/密钥管理 -> `cacheforge-ops`
- 使用情况/节省情况统计 -> `cacheforge-stats`

## CacheForge 的定位

CacheForge 是一个与 OpenAI 兼容的代理工作流管理工具。它可以减少不必要的开支，并提升任务的执行效率（具体效果因服务提供商和工作负载而异）。

“Vault 模式”（Pro 版）适用于需要使用大量工具的代理。用户可以在 CacheForge 的仪表板上查看执行结果。

## 启动工作流程（必选）

在将请求路由到辅助技能之前，请执行以下命令：

```bash
bash "{baseDir}/scripts/bootstrap-companions.sh"
```

如果由于缺少 `clawhub` 而导致启动失败，请提示用户手动安装相关辅助技能：

```bash
for s in cacheforge-setup cacheforge-ops cacheforge-stats; do clawhub install "$s"; done
```

## 路由规则

启动完成后，请使用以下路由规则：

- 设置/首次入职：
  - `python3 "{baseDir}/../cacheforge-setup/setup.py" provision ...`
  - `python3 "{baseDir}/../cacheforge-setup/setup.py" openclaw-apply --set-default`
  - `python3 "{baseDir}/../cacheforge-setup/setup.py" validate`

- 账户管理：
  - `python3 "{baseDir}/../cacheforge-ops/ops.py" balance`
  - `python3 "{baseDir}/../cacheforge-ops/ops.py" topup --amount 10 --method stripe`
  - `python3 "{baseDir}/../cacheforge-ops/ops.py" topup --amount 10 --method crypto`
  - `python3 "{baseDir}/../cacheforge-ops/ops.py" upstream ...`
  - `python3 "{baseDir}/../cacheforge-ops/ops.py" keys ...`

- 统计/节省情况：
  - `python3 "{baseDir}/../cacheforge-stats/dashboard.py" dashboard`
  - `python3 "{baseDir}/../cacheforge-stats/dashboard.py" usage --window 7d`
  - `python3 "{baseDir}/../cacheforge-stats/dashboard.py" breakdown --by model`

## 新用户入职流程规范

新用户必须遵循以下顺序：
1. 注册并验证电子邮件（如部署要求）。
2. 创建租户 API 密钥（格式为 `cf_...`）。
3. 配置上游服务提供商（`openrouter`、`anthropic` 或 `custom`）。
4. 应用 OpenClaw 服务提供商的配置（并备份配置文件）。
5. 充值（最低充值金额为 $10）。
6. 运行验证请求并检查仪表板上的数据。

## 公开内容发布规范

- 除非有可复制的基准测试结果，否则不要在公开内容中使用具体的节省金额数据。
- 不要透露 CacheForge 的内部工作机制。
- 公开内容应侧重于展示结果，并在适当的情况下注明“具体效果因服务提供商和工作负载而异”。