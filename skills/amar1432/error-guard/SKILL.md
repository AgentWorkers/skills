---
name: error-guard
description: >
  System safety and control-plane skill that prevents agent deadlocks and freezes.
  Provides non-LLM control commands to inspect task state, flush message queues,
  cancel long-running work, and recover safely without restarting the container.
  Use when implementing or operating long-running tasks, sub-agents, benchmarks,
  background monitors (e.g., Moltbook, PNR checks), or when the system becomes
  unresponsive and needs immediate recovery controls.
---

# error-guard

⚠️ **系统级技能（高级用户专用）**

该技能定义了 OpenClaw 的 **控制平面安全机制**。其设计初衷是保持简洁性、非阻塞性，并旨在防止代理在处理长时间运行或高风险的工作负载时出现冻结、死锁或无法恢复的状态。

## 设计原则

> **警告：** 该技能在代理的控制平面层面运行。  
> 仅应由了解 OpenClaw 执行模型、且正在运行可能阻塞、挂起或长时间运行的工作负载的用户来安装。

- **主代理永不阻塞**：避免长时间执行任务、避免外部 I/O 操作、避免调用大型语言模型（LLM）。

- **事件驱动**：工作进程会生成事件，控制平面会监听这些事件。

- **优先考虑故障安全**：所有恢复命令都必须能够立即响应。

- **状态信息最小化**：仅记录任务元数据（如任务 ID、创建时间、状态），绝不保存任务数据本身。

## 命令接口（第一阶段）

### /status

报告当前系统健康状况和任务注册表的状态。

返回信息：
- 活动中的任务（任务 ID、类型、状态）
- 任务的开始时间和最后一次心跳信号
- 标记为停滞或逾期的任务

**限制条件：**
- 必须以恒定时间间隔执行
- 严禁调用任何模型或外部 API。

### /flush

紧急停止操作。

立即执行以下操作：
- 取消所有活动中的任务
- 结束所有正在运行的进程/会话
- 清空待处理消息队列
- 重置内存中的任务注册表

**限制条件：**
- 必须立即响应请求
- 不得等待任何工作进程的完成
- 严禁调用任何模型。

### /recover

安全的恢复流程：

步骤：
1. 执行 `/flush` 命令
2. 重置控制平面的状态
3. （可选）重新加载相关技能/状态数据（无需重启容器）

## 未来扩展计划（尚未实现）

- 子代理运行辅助工具（事件驱动）
- 带有超时限制和静默检测功能的任务监控机制
- 结构化的事件协议（如 `taskstarted`、`task.heartbeat`、`task_completed` 等）
- 支持不同的任务执行模式（交互式、批量、后台执行）

## 安全性与隐私保护

- 该技能**不**存储任务数据、用户输入、消息或模型输出。
- 仅保存最基本的任务元数据（如任务 ID、时间戳、状态）。
- 不会读取或写入任何 API 密钥、凭据或用户数据。
- 可以安全地公开发布和共享该技能。

## 非目标功能

- 该技能不包含任何业务逻辑
- 不包含后台轮询机制
- 不提供面向用户的界面
- 不涉及任何大型语言模型的推理过程

该技能是系统的**最后一道防线**。请确保其保持简洁、高效且可靠。