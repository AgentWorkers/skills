---
name: tokenQrusher
description: OpenClaw的令牌优化系统可将成本降低50%至80%
version: 2.0.6
author: qsmtco
license: MIT
homepage: https://github.com/qsmtco/tokenQrusher
metadata:
  openclaw:
    requires:
      env:
        - OPENROUTER_API_KEY
      bins:
        - python3
        - node
    emoji: "💰"
---
# tokenQrusher 技能

## 概述

tokenQrusher 是一个针对 OpenClaw 的全面性令牌成本优化系统，通过智能上下文过滤、模型路由、自动化调度和心跳优化，可将 API 成本降低 50-80%。

## 组件

### 1. 上下文钩子 (`token-context`)

**事件：`agent:bootstrap`

根据消息的复杂性过滤工作区文件。

**配置：`~/.openclaw/hooks/token-context/config.json`

**原理：**简单消息（如问候语）只需要身份信息；复杂任务才需要完整上下文。

**节省成本：**简单消息可节省约 99% 的成本（从 50,000 令牌减少到 500 令牌）

### 2. 模型路由器 (`token-model`)

**事件：`agent:bootstrap`

根据任务复杂性记录模型层级推荐。

**配置：`~/.openclaw/hooks/token-model/config.json`

**注意：**钩子不能直接修改模型。请使用 `openclaw.json` 中的回退机制：

**节省成本：**对于简单任务，使用免费层级可节省高达 92% 的成本。

### 3. 使用情况跟踪器 (`token-usage`)

**事件：`agent:bootstrap`

监控使用情况并记录预算状态。

**配置：`~/.openclaw/hooks/token-usage/config.json`

**环境覆盖：**

**状态表情符号：**
- ✅ 正常（<80%）
- 🟡 警告（80-95%）
- 🔴 危急（95-100%）
- 🚨 超过限制（>100%）

### 4. 定时任务优化器 (`token-cron`)

**事件：`gateway:startup`

在启动时运行自动化优化。

**配置：`~/.openclaw/hooks/token-cron/config.json`

**调度任务：**

| 任务 | 时间间隔 | 描述 |
|-----|----------|-------------|
| optimize | 3600s (1小时) | 运行优化分析 |
| rotate_model | 7200s (2小时) | 根据预算轮换模型 |
| check_budget | 300s (5分钟) | 检查预算阈值 |

**实现：`scripts/cron-optimizer/optimizer.py`

纯函数，线程安全，输出结果可预测。

### 5. 心跳优化器 (`token-heartbeat`)

**事件：`agent:bootstrap`（用于心跳轮询）

优化心跳调度以减少 API 调用次数。

**配置：`~/.openclaw/hooks/token-heartbeat/config.json`

**优化表：**

| 检查项 | 之前 | 之后 | 成本降低 |
|-------|--------|-------|-----------|
| Email | 60分钟 | 120分钟 | 50% |
| Calendar | 60分钟 | 240分钟 | 75% |
| Weather | 60分钟 | 240分钟 | 75% |
| Monitoring | 30分钟 | 120分钟 | 75% |

**结果：**每天检查次数从 48 次减少到 12 次（API 调用次数减少 75%）

## 命令行接口 (CLI) 命令

安装后，可以使用 `tokenqrusher` 命令：

### `tokenqrusher context <提示>`

为给定的提示推荐合适的上下文文件。

### `tokenqrusher model <提示>`

为给定的提示推荐合适的模型层级。

### `tokenqrusher budget [--period daily|weekly|monthly]`

显示带有表情符号的预算状态。

### `tokenqrusher usage [--days N]`

显示使用情况摘要。

### `tokenqrusher optimize [--dry-run] [--json]`

运行优化过程。

### `tokenqrusher status [--verbose] [--json]`

显示完整系统状态。

### `tokenqrusher install [--hooks] [--cron] [--all]`

安装钩子和定时任务。

## 设计原则

该技能遵循严格的工程标准：

- **确定性**：相同的输入始终产生相同的输出
- **纯函数**：除非明确指定，否则没有副作用
- **不可变性**：数据类是固定的；使用 JavaScript 的 `const` 声明
- **控制流不使用异常**：在 Python 中使用 `Either/Result`，在 JavaScript 中使用 `Maybe`
- **线程安全**：对共享状态使用 RLock 保护
- **全面的类型注解**：完全的类型提示，兼容 mypy
- **日志记录规范**：仅在入口、退出和出错时记录日志
- **编译时常量**：所有数值限制都定义为常量

## 架构决策

### 为什么使用多个钩子？

OpenClaw 的钩子系统允许在同一事件 (`agent:bootstrap`) 上挂多个独立的钩子。每个钩子都有单一的职责：

- `token-context`：仅过滤上下文文件
- `token-model`：仅记录模型推荐
- `token-usage`：仅报告预算状态

这种分离使得：
- 可以独立启用/禁用每个组件
- 明确了责任归属，便于调试
- 更容易进行测试

### 为什么使用 Python + JavaScript？

- **Python**：用于处理大量计算、数据加工和复杂逻辑
- **JavaScript**：钩子处理程序需要在 OpenClaw 的 Node.js 环境中运行

共享模块确保了代码的一致性（例如，`token-shared` 中的正则表达式模式）。

### 为什么不直接控制模型？

OpenClaw 的钩子系统无法在会话中途修改模型选择。解决方法包括：
- 使用 `openclaw.json` 中的回退机制（自动处理）
- 基于定时的模型轮换（自动化）
- 通过 `/model` 命令进行手动覆盖

## 测试

### 单元测试（共 170 个测试）

**覆盖率：**90% 以上

### 测试哲学

- **基于定理的测试**：测试验证数学属性（例如，“置信度始终在 0-1 之间”）
- **确定性**：相同的输入产生相同的输出
- **边缘情况**：处理 Unicode、空值和极端值
- **模糊测试**：随机输入不会导致程序崩溃

## 性能

在典型硬件上的基准测试结果：

| 操作 | 延迟 | CPU 使用率 | 内存使用率 |
|-----------|---------|-----|--------|
| 上下文分类 | <1毫秒 | 0.01% | 0.5MB |
| 模型分类 | <1毫秒 | 0.01% | 0.5MB |
| 预算检查 | <10毫秒 | 0.05% | 1MB |
| 全面优化 | <200毫秒 | 0.1% | 5MB |

## 安全性

### 输入验证

- 所有文件名都使用严格的正则表达式进行验证 (`/^[a-zA-Z0-9._-]+$/`)
- 防止路径遍历
- 强制限制文件长度（最多 255 个字符）

### 保密性

- 代码中不存储 API 密钥
- 所有凭据都来自环境变量或 OpenClaw 配置文件
- 不记录任何凭据信息

### 资源限制

- 配置文件读取有超时限制（子进程 5 秒，SSH 10 秒）
- 内存使用受记录保留策略限制（默认为 30 天）
- 磁盘使用受保留策略限制

## 故障排除

### 钩子未加载

### 预算始终为 0

使用情况跟踪需要相关记录。请先生成活动数据：

### CPU 使用率过高

检查是否存在无限循环。重启 gateway：

### 配置更改未生效

配置缓存的 TTL 为 60 秒。请等待或重启：

## 迁移指南

### 从 v1.x 迁移到 v2.0

主要变化包括：

1. **统一的 CLI**：现在使用 `tokenqrusher` 而不是单独的脚本
2. **共享模块**：所有 JavaScript 钩子都使用 `token-shared/shared.js`
3. **线程安全**：Python 类现在使用 RLock
4. **结果类型**：Python 中不再使用异常来控制流程

对于 CLI 用户来说，没有重大变化。如果使用了自定义配置，可能需要迁移钩子设置。

## 未来计划

- **v2.1**：计算平均成本、预测预算
- **v2.2**：支持多租户、团队预算
- **v3.0**：为集群提供分布式使用情况聚合功能

## 许可证

MIT 许可证。详见 LICENSE 文件。

## 支持

- **问题报告**：https://github.com/qsmtco/tokenQrusher/issues
- **Discord**：`#openclaw` 在 clawd.discord.gg
- **文档**：https://docs.tokenqrusher.openclaw.ai

## 致谢

- **设计**：Lieutenant Qrusher
- **实现**：Qrusher 团队 (qsmtco)
- **审核**：Captain JAQ (SMTCo)
- **框架**：OpenClaw 团队

该技能基于 OpenClaw Agent 框架构建：https://github.com/openclaw/openclaw

---

## 外部端点

在获取模型价格时，此技能可以选择性地联系以下外部端点：

| 端点 | 用途 | 使用场景 |
|----------|---------|-----------|
| `https://openrouter.ai/api/v1/models` | 获取当前模型价格 | 当运行 `tokenqrusher budget` 或 `tokenqrusher optimize` 且价格数据未缓存时，且设置了 `OPENROUTER_API_KEY` |

如果未设置 `OPENROUTER_API_KEY`，则使用内置默认值，不会进行外部调用。所有钩子和其他组件都将完全在本地运行。

## 安全性与隐私

- **核心功能（钩子）完全在本地运行** —— 不需要网络访问
- **可选的价格获取**：仅在明确触发且提供了 API 密钥的情况下才会联系 OpenRouter
- **不会传输任何用户数据**（工作区文件、消息）
- 所有配置都从本地文件 (`~/.openclaw/hooks/`) 读取
- 使用情况跟踪仅读取 OpenClaw 的内部日志
- CLI 工具 (`tokenqrusher`) 分析本地工作区文件和 OpenClaw 的状态

## 模型调用说明

钩子 (`token-context`、`token-model`、`token-usage`、`token-cron`、`token-heartbeat`) 会在代理启动和网关启动时自动触发。这是预期的行为；用户无需执行任何操作，只需启用这些钩子即可。

## 信任声明

使用此技能时，所有操作都仅在您的机器上完成。不会向外部服务器发送任何数据。只有在您信任代码及其作者的情况下才进行安装。