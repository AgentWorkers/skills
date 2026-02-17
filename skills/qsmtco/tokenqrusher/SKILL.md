---
metadata:
  name: tokenQrusher
  slug: tokenQrusher
  description: Token optimization system for OpenClaw reducing costs 50-80%
  version: 2.0.0
  author: qsmtco
  license: MIT
  homepage: https://github.com/qsmtco/tokenQrusher
  repository: https://github.com/qsmtco/tokenQrusher
  keywords: 
    - openclaw
    - token-cost
    - optimization
    - cost-reduction
    - budget
    - usage-tracking
  badges:
    - "MIT License"
    - "170 unit tests"
    - "Production-ready"
  requires:
    openclaw: ">=2.0.0"
    runtime:
      bins: ["python3", "node"]
  documentation: README.md
---

# tokenQrusher 技能

## 概述

tokenQrusher 是一个针对 OpenClaw 的全面性令牌成本优化系统，通过智能的上下文过滤、模型路由、自动化调度和心跳优化，可将 API 成本降低 50-80%。

## 组件

### 1. 上下文过滤器 (`token-context`)

**事件:** `agent:bootstrap`

根据消息的复杂性过滤工作区文件。

**配置:** `~/.openclaw/hooks/token-context/config.json`

**说明:** 简单的消息（如问候语）只需要身份信息；复杂的任务则需要完整的上下文信息。

**节省成本:** 对于简单消息，可节省约 99% 的成本（从 50,000 令牌减少到 500 令牌）。

### 2. 模型路由器 (`token-model`)

**事件:** `agent:bootstrap`

根据任务的复杂性记录模型层的推荐结果。

**配置:** `~/.openclaw/hooks/token-model/config.json`

**注意:** 这些钩子不能直接修改模型。请使用 `openclaw.json` 中的回退机制：

**说明:** 通过为简单任务使用免费模型层，最多可节省 92% 的成本。

### 3. 使用情况跟踪器 (`token-usage`)

**事件:** `agent:bootstrap`

监控使用情况并记录预算状态。

**配置:** `~/.openclaw/hooks/token-usage/config.json`

**环境覆盖:** （此处为示例代码，实际应用中可能有所不同）

**状态图标:**
- ✅ 状态良好（<80%）
- 🟡 警告（80-95%）
- 🔴 严重（95-100%）
- 🚨 超过预算（>100%）

### 4. 定时任务优化器 (`token-cron`)

**事件:** `gateway:startup`

在系统启动时自动运行优化任务。

**配置:** `~/.openclaw/hooks/token-cron/config.json`

**调度任务:**
| 任务 | 间隔 | 描述 |
|-----|----------|-------------|
| optimize | 3600s (1小时) | 运行优化分析 |
| rotate_model | 7200s (2小时) | 根据预算情况轮换模型 |
| check_budget | 300s (5分钟) | 检查预算阈值 |

**实现:** `scripts/cron-optimizer/optimizer.py`

这些都是纯函数，支持线程安全，并且输出结果具有确定性。

### 5. 心跳优化器 (`token-heartbeat`)

**事件:** `agent:bootstrap`（用于心跳检测）

优化心跳调度的频率，以减少 API 调用次数。

**配置:** `~/.openclaw/hooks/token-heartbeat/config.json`

**优化对比表:**
| 优化方式 | 优化前 | 优化后 | 成本降低比例 |
|-------|--------|-------|-----------|
| 邮件 | 每 60分钟 | 每 120分钟 | 50% |
| 日历 | 每 60分钟 | 每 240分钟 | 75% |
| 天气 | 每 60分钟 | 每 240分钟 | 75% |
| 监控 | 每 30分钟 | 每 120分钟 | 75% |

**结果:** 每天从 48 次检查减少到 12 次检查（API 调用次数减少了 75%）。

## 命令行接口 (CLI) 命令

安装完成后，可以使用 `tokenqrusher` 命令：

### `tokenqrusher context <提示>`

根据提供的提示推荐合适的上下文文件。

### `tokenqrusher model <提示>`

根据提供的提示推荐合适的模型层。

### `tokenqrusher budget [--period daily|weekly|monthly]`

显示带有状态图标的预算状态。

### `tokenqrusher usage [--days N]`

显示使用情况摘要。

### `tokenqrusher optimize [--dry-run] [--json]`

运行优化操作。

### `tokenqrusher status [--verbose] [--json]`

显示系统的完整状态。

### `tokenqrusher install [--hooks] [--cron] [--all]`

安装钩子和定时任务。

## 设计原则

该技能遵循严格的工程标准：

- **确定性**：相同的输入总是产生相同的输出。
- **纯函数**：除非明确指定，否则没有副作用。
- **不可变性**：数据类是不变的；使用 JavaScript 的 `const` 声明来实现。
- **控制流不使用异常**：在 Python 中使用 `Either/Result`，在 JavaScript 中使用 `Maybe`。
- **线程安全**：使用 RLock 保护共享状态。
- **全面的类型注解**：使用完整的类型提示，兼容 mypy。
- **日志记录**：仅在程序启动、退出或出现错误时记录日志。
- **编译时常量**：所有数值限制都定义为常量。

## 架构决策

### 为什么使用多个钩子？

OpenClaw 的钩子系统允许在同一事件（`agent:bootstrap`）上挂多个独立的钩子。每个钩子都有明确的职责：

- `token-context`：仅负责过滤上下文文件。
- `token-model`：仅负责记录模型推荐结果。
- `token-usage`：仅负责报告预算状态。

这种分离方式使得：
- 可以独立地启用或禁用每个组件。
- 明确了各个组件的职责，便于调试。
- 更容易进行测试。

### 为什么使用 Python 和 JavaScript？

- **Python**：适用于复杂的计算、数据处理和逻辑处理。
- **JavaScript**：钩子处理器需要在 OpenClaw 的 Node.js 环境中运行。

共享模块（如 `token-shared`）确保了代码的一致性。

### 为什么不直接修改模型？

OpenClaw 的钩子系统不允许在会话进行中修改模型选择。解决方法包括：
- 使用 `openclaw.json` 中的回退机制（自动处理）。
- 基于定时任务的模型轮换（自动化操作）。
- 通过 `/model` 命令进行手动配置。

## 测试

### 单元测试（共 170 个测试用例）

**测试覆盖率:** 超过 90%。

### 测试哲学

- **基于定理的测试**：验证数学属性（例如，“置信度始终在 0-1 之间”）。
- **确定性**：相同的输入总是产生相同的输出。
- **边缘情况**：测试 Unicode、空值和极端值。
- **模糊测试**：测试随机输入是否会导致程序崩溃。

## 性能

在典型硬件上的测试结果：

| 操作 | 延迟 | CPU 使用率 | 内存使用量 |
|-----------|---------|-----|--------|
| 上下文分类 | <1毫秒 | 0.01% | 0.5MB |
| 模型分类 | <1毫秒 | 0.01% | 0.5MB |
| 预算检查 | <10毫秒 | 0.05% | 1MB |
| 全面优化 | <200毫秒 | 0.1% | 5MB |

## 安全性

### 输入验证

- 所有文件名都使用严格的正则表达式进行验证（`/^[a-zA-Z0-9._-]+$/`）。
- 防止路径遍历。
- 对文件长度进行限制（最多 255 个字符）。

### 保密性

- 代码中不存储 API 密钥。
- 所有凭据都从环境变量或 OpenClaw 配置文件中获取。
- 不记录任何凭据信息。

### 资源限制

- 配置文件的读取操作有超时限制（子进程 5 秒，SSH 连接 10 秒）。
- 内存使用量受记录保留策略的限制（默认为 30 天）。
- 磁盘使用量受数据保留策略的限制。

## 故障排除

### 钩子未加载

**解决方法:** （此处为示例代码，实际应用中可能有所不同）

### 预算始终为 0

使用情况跟踪需要先生成相关记录。请先生成数据后再进行跟踪。

### CPU 使用率过高

检查是否存在无限循环。如果存在，请重启系统。

### 配置更改未生效

配置文件的缓存时间设置为 60 秒。请等待或重新启动系统。

## 迁移指南

### 从 v1.x 迁移到 v2.0

主要变化包括：
- **统一的 CLI**：现在使用 `tokenqrusher` 替代之前的独立脚本。
- **共享模块**：所有 JavaScript 钩子都使用 `token-shared/shared.js`。
- **线程安全**：Python 类现在使用 RLock 保证线程安全。
- **结果类型**：Python 中不再使用异常来控制程序流程。

**对 CLI 用户的影响:** 无重大影响。如果使用了自定义配置，可能需要重新配置钩子。

## 未来计划

- **v2.1**: 实现美元成本平均计算和预测性预算预测。
- **v2.2**: 支持多租户和团队预算管理。
- **v3.0**: 为集群提供分布式使用情况聚合功能。

## 许可证

采用 MIT 许可证。详细信息请参阅 LICENSE 文件。

## 支持方式

- **问题报告**: https://github.com/qsmtco/tokenQrusher/issues
- **Discord**: `#openclaw` 在 clawd.discord.gg
- **文档**: https://docs.tokenqrusher.openclaw.ai

## 致谢

- **设计**: Lieutenant Qrusher
- **实现**: Qrusher 团队 (qsmtco)
- **审查**: Captain JAQ (SMTCo)
- **框架**: OpenClaw 团队

该技能基于 OpenClaw Agent 框架开发：https://github.com/openclaw/openclaw