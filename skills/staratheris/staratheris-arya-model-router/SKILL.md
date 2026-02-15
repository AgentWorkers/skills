---
name: arya-model-router
description: **Token节省型路由器：选择型号（经济型/标准型/高级型），并使用子代理来处理繁重任务。支持可选的压缩和简要信息功能。**
metadata:
  openclaw:
    emoji: "🧭"
    requires:
      bins: ["bash", "python3"]
---

# Arya Model Router（Token节省器）

这是一个用于OpenClaw的模型路由器，用于决定何时使用经济型模型，何时使用更强大的模型，从而降低成本和Token消耗。

## 目标

- 保持日常聊天使用的模型成本较低。
- 仅在任务需要时才升级到更高级的模型。
- 避免将大量上下文数据传递给高级模型：首先创建一个**简报**（brief）。

## 设计理念

- 主代理（main agent）始终使用经济型模型。
- 对于复杂任务，路由器会推荐或直接使用更高级的**子代理**（sub-agent）来处理。

## 默认模型级别

- cheap：`openai/gpt-4o-mini`
- default：`openai/gpt-4.1-mini`
- pro：`openai/gpt-4.1`

## 使用方式

- “Router：以经济型模型回答这个问题”（强制使用）
- “Router：分析这个问题”（自动选择模型）

## 相关文件

- `router.py`：模型选择逻辑及规则
- `rules.json`：可编辑的规则配置文件
- `README.md`：完整的使用说明文档