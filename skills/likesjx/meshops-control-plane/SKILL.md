---
name: ansible
description: MeshOps distributed coordination mesh for OpenClaw gateways: ring-of-trust admission, CRDT-synced state, capability-contract routing, and governed delegation. Named for the ansible from Ender's Game, not the infrastructure tool.
---

# Ansible - MeshOps 协调技能

## 什么是 Ansible

Ansible 是一个分布式协调层，允许您将多个 OpenClaw 网关作为一个协调一致的网格来操作。

### Ansible 的四个核心支柱：

1. **信任环（Ring of Trust）**：包括节点间的邀请/加入机制、身份验证、WebSocket 通信、ed25519 签名的能力声明（capability manifests）、每次操作的安全检查以及令牌的生命周期管理。
2. **网格同步（Mesh Sync）**：通过 Tailscale 实现 Yjs CRDT（Copy-on-Write Data Structure）的复制。消息、任务、上下文和状态信息在重新连接或重启后仍然保持完整。
3. **能力路由（Capability Routing）**：负责发布/取消发布能力合约（capability contracts）。每个合约都指定了一个委托技能（requester，即请求者）和一个执行技能（executor，即执行者）。
4. **生命周期管理（Lifecycle Ops）**：包括锁的清理、数据的保留/删除、协调器的维护以及部署过程的优化。

## 节点关系模式

- **朋友/员工（Friends/Employees）**（默认模式）：其他节点被视为不同的代理，需要明确提供上下文并进行直接通信。
- **半球（Hemispheres）**（高级模式）：具有相同身份的节点之间的镜像关系，可以共享意图并进行直接通信。
除非明确指定，否则节点默认处于“朋友/员工”模式。

## 节点拓扑结构

- **骨干节点（Backbone）**：始终在线的节点（VPS/服务器），负责托管 Yjs WebSocket 服务。
- **边缘节点（Edge）**：间歇性连接的节点（笔记本电脑/台式机），用于与骨干节点通信。

## 人类可见性协议（Human Visibility Protocol）

在处理协调任务时，需要维护以下更新机制：

- **ACK**：确认收到消息并总结任务意图。
- **IN_PROGRESS**：在关键节点处发送进度更新。
- **DONE 或 BLOCKED**：完成任务后，提供完成证据、下一步行动信息以及任务负责人。

所有相关更新都应使用统一的 `conversation_id` 进行标识。

## 信任环的行为规则

- 未知节点必须通过邀请才能加入网络；严禁绕过这些节点。
- 高风险能力的发布需要人工批准。
- 必须遵守调用者权限限制（`OPENCLAW_ALLOWED_CALLERS`）和高风险操作标志。
- 绝不允许在明文消息、日志或共享状态中暴露令牌信息。
- 当启用了签名验证机制时，仅接受由可信发布者签名的能力声明。

## 网关兼容性协议（Gateway Compatibility Protocol）

- 在假设工具可用之前，必须验证插件已安装且可正常使用。
- 在修改协调设置之前，需要确认节点类型（骨干节点 vs 边缘节点）。
- 将网关的运行状态视为网络拓扑和健康状况的权威信息来源。

## 可靠性模型

- **共享状态（Shared State）**：所有节点都共享相同的 Yjs 状态数据，该数据具有权威性。
- **消息传递机制（Message Delivery）**：
  - 消息和任务会持久保存在共享状态中。
  - 消息会自动尝试实时发送到目标节点。
  - 定期进行心跳检测以恢复未发送的消息。
  - 对于临时性的发送失败，系统会进行重试。
  - 任务分配完成后会通知相关操作者。

## 操作规则

- 使用 `ansible_status` 和 `ansible_read_messages` 命令来检查任务的执行状态。
- 如果使用轮询模式，必须通过 `ansible_send_message` 命令进行响应。
- 使用 `corr:<messageId>` 保持消息处理的连续性。
- 监听器（listener）行为属于优化措施；在必要时，系统会执行清理或重新同步操作。

## 能力合约（Capability Contracts）

- 能力不仅仅是一个标签，而是一个包含委托和执行细节的正式合约。
- 发布能力时需要指定委托和执行技能。
- 所有能力发布的更新都会在整个网格范围内进行路由。
- 配置允许的情况下，系统会验证发布者的身份。
- 高风险能力发布需要人工批准。
- 取消发布会立即移除该能力的路由权限。
- 能力的生命周期记录必须包含安装和执行的结果。

## 委托协议（Delegation Protocol）

- 请求者创建任务时，需要指定任务目标、上下文、接受标准以及目标代理或能力对象。
- 执行者接收任务后，会发送接受信号或预计完成时间。
- 执行者完成任务后，会提供进度信息并返回结构化的结果。
- 请求者最终会向相关人员或下游代理报告任务结果。

## 协调器行为（Coordinator Behavior）

- 定期检查锁的状态、服务水平协议（SLA）的遵守情况以及任务积压情况。
- 当任务范围不明确时，优先采用仅记录日志的升级方式。
- 在系统性能下降时，优先考虑控制问题、提高可见性并确保任务的确定性恢复。

## 可用的工具

### 通信工具（Communication Tools）

| 工具          | 功能                        |
|-----------------|---------------------------|
| `ansible_send_message`    | 向整个网格发送目标消息或广播消息            |
| `ansible_read_messages`    | 读取未读消息或完整的历史记录            |
| `ansible_mark_read`    | 标记消息为已读                    |
| `ansible_delete_messages`    | 仅管理员可用的紧急消息清除功能            |

### 任务委托工具（Task Delegation Tools）

| 工具          | 功能                        |
|-----------------|---------------------------|
| `ansibledelegate_task`    | 为其他节点或代理创建任务                |
| `ansible_claim_task`    | 声明对任务的拥有权                    |
| `ansible_update_task`    | 更新任务状态或进度                    |
| `ansible_complete_task`    | 完成任务并通知请求者                |
| `ansible_find_task`    | 根据 ID 或标题查找任务                |

### 上下文与状态管理工具（Context and Status Tools）

| 工具          | 功能                        |
|-----------------|---------------------------|
| `ansible_status`    | 显示网格健康状况、未读消息、待处理任务及拓扑结构        |
| `ansible_update_context`    | 更新共享的上下文、线程信息和决策            |

### 协调与治理工具（Coordination and Governance Tools）

| 工具          | 功能                        |
|-----------------|---------------------------|
| `ansible_get_coordination`    | 读取协调器配置                    |
| `ansible_set_coordination_preference` | 设置节点的协调器偏好设置                |
| `ansible_set_coordination`    | 切换协调器（需谨慎操作）                |
| `ansible_set_retention`    | 配置已完成任务的保留策略                |
| `ansible_get_delegation_policy` | 读取委托策略及相关确认信息            |
| `ansible_set_delegation_policy` | 发布/更新委托策略                  |
| `ansible_ack_delegation_policy` | 确认委托策略版本                  |
| `ansible_lock_sweep_status`    | 检查锁的清理状态                    |

### 能力生命周期管理工具（Capability Lifecycle Tools）

| 工具          | 功能                        |
|-----------------|---------------------------|
| `ansible_list_capabilities`    | 列出已发布的所有能力合约                |
| `ansiblecapability_publish`    | 发布或升级能力合约                    |
| `ansible_capability_unpublish`    | 从路由中移除能力                    |
| `ansiblecapability_lifecycle_evidence` | 显示能力的安装和执行记录                |
| `ansiblecapability_health_summary` | 显示能力发布的成功/失败情况及其延迟统计        |

## 何时使用 Ansible

当需要跨多个网关进行操作、需要持久性的协调机制或需要可审计的委托流程时，应使用 Ansible。

## 会话管理（Session Management）

- 首先检查网格的状态和待处理任务。
- 对于需要明确委托的任务，应采用明确的委托方式。
- 通过生命周期更新信息让相关人员随时了解任务进展。

## 消息协议（Message Protocol v1）

- 消息中必须包含足够的上下文信息，以确保任务能够独立执行。
- 使用稳定的关联 ID（`corr`）和对话 ID（conversation ID）来标识消息。
- 相比自由格式的消息，结构化的数据更有利于系统处理。

## 设置 playbook

请按照插件设置和网关运行手册的指导来初始化网络拓扑、配置身份验证和信任机制。

## 委托管理

- 确保所有节点都使用最新的委托策略，并且该策略得到所有节点的认可。
- 将能力的发布视为合约的正式发布。
- 如果生命周期数据表明存在问题或错误，应迅速回滚相关设置。