---
name: cron-writer
description: 将自然语言转换为 Cron 表达式。当您需要安排任务时可以使用这种方法。
---

# Cron 编写工具

Cron 语法看起来很简单，但当你真正需要编写一个 Cron 任务时，就会发现其实并不容易。五个星号（*）让人感到困惑，而且你可能记不清哪个字段代表星期几。这个工具可以将像“每周二下午 3 点”这样的普通英文描述转换成精确的 Cron 表达式。它还会显示下几次任务的执行时间，以便你验证其正确性。

**只需一个命令，无需任何配置，即可使用。**

## 快速入门

```bash
npx ai-cron-gen "every day at midnight"
```

## 功能介绍

- 将普通的英文时间表描述转换为 Cron 表达式
- 以人类可读的方式解释生成的 Cron 表达式的含义
- 列出下几次预定的执行时间以供验证
- 支持复杂的调度规则（如“每隔一个星期五”或“每月的第一个星期一”）
- 无需任何配置即可立即使用

## 使用示例

```bash
# Simple schedule
npx ai-cron-gen "every day at midnight"

# Complex schedule
npx ai-cron-gen "every weekday at 9am and 5pm"

# Specific pattern
npx ai-cron-gen "first Monday of every month at 10:30am"
```

## 最佳实践

- **通过预览结果进行验证**：务必检查预览结果，确保时间表符合你的需求
- **明确指定时区**：Cron 表达式不包含时区信息，请确保你知道服务器所在的时区
- **测试特殊情况**：像“每隔一个星期”这样的调度规则可能比较复杂，请务必仔细核对预览结果
- **直接复制到 crontab 中**：生成的 Cron 表达式可以直接粘贴到你的 crontab 或调度器中

## 适用场景

- 设置新的 Cron 任务时忘记了语法
- 配置持续集成/持续交付（CI/CD）的调度流程
- 构建任务调度器时需要验证 Cron 表达式
- 以人类可读的格式记录现有的 Cron 任务

## 该工具属于 LXGIC 开发工具包

这是 LXGIC Studios 开发的 110 多个免费开发者工具之一。免费版本没有任何付费门槛、注册要求或 API 密钥，只提供实用的功能。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgic.dev

## 系统要求

无需安装，只需使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。

```bash
npx ai-cron-gen --help
```

## 工作原理

该工具会将你的时间表描述发送给一个能够理解 Cron 语法和时间模式的 AI 模型。模型会生成相应的 Cron 表达式，并用通俗的语言解释其含义，同时计算出下几次执行的时间，以便你验证时间表的正确性。

## 许可证

采用 MIT 许可证，永久免费。你可以随意使用该工具。