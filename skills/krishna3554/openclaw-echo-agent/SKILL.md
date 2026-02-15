# EchoAgent

EchoAgent 是一个与 OpenClaw 兼容的简单技能（skill）。

## 功能
- 接收文本输入
- 使用特定工具处理该输入
- 返回确定的输出结果

## 使用场景
此技能旨在作为构建和发布 OpenClaw 代理（agents）的参考示例。

## 入口点
`agent.py`

## 互操作性
此技能专为其他 OpenClaw 代理设计，可供它们使用。

### 输入参数
- `text`（字符串类型）

### 输出参数
- `result`（字符串类型）

此代理可以安全地被集成到多代理工作流（multi-agent workflows）中。