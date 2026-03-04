---
name: ansible
description: MeshOps distributed coordination mesh for OpenClaw gateways: ring-of-trust admission, CRDT-synced state, capability-contract routing, and governed delegation. Named for the ansible from Ender's Game, not the infrastructure tool.
---

# Ansible – MeshOps 协调技能

## Ansible 的作用

Ansible 是一个分布式协调层，允许您将多个 OpenClaw 网关作为一个协调统一的网格来管理。它基于以下四个核心支柱来运作：

1. **信任环（Ring of Trust）**：负责节点之间的邀请/加入流程、身份验证、WebSocket 通信、ed25519 签名的能力声明（capability manifests）、每项操作的安全性检查以及令牌的生命周期管理。
2. **网格同步（Mesh Sync）**：通过 Tailscale 实现 Yjs CRDT（Copy-on-Write Data Structure）的复制机制，确保消息、任务、上下文和状态在节点重新连接或重启后仍然保持一致。
3. **能力路由（Capability Routing）**：负责发布/取消发布能力合约（capability contracts），每个合约都指定了一个请求者（requester）和一个执行者（executor）。
4. **生命周期管理（Lifecycle Ops）**：包括锁定清理（lock sweep）、数据保留/修剪（retention/pruning）、协调器扫描（ coordinator sweep）以及部署相关的操作。

## 节点关系模式

- **朋友/员工（Friends/Employees）**（默认模式）：其他节点被视为独立的代理，需要明确提供上下文并进行交互。
- **半球（Hemispheres）**（高级模式）：具有相同身份的节点之间的直接通信和共享意图。

除非明确指定，否则系统默认使用“朋友/员工”模式。

## 节点拓扑结构

- **骨干节点（Backbone）**：始终在线的节点（VPS/服务器），负责托管 Yjs WebSocket 服务。
- **边缘节点（Edge）**：间歇性连接的节点（笔记本电脑/台式机），用于与骨干节点通信。

## 人类可见性协议（Human Visibility Protocol）

在处理协调任务时，必须遵循以下更新规则：
- **ACK**：确认收到消息并总结任务意图。
- **IN_PROGRESS**：在关键阶段发送进度更新。
- **DONE 或 BLOCKED**：完成任务后，提供详细信息、下一步行动以及任务负责人。

所有相关更新都必须使用统一的 `conversation_id` 进行标识。

## 信任环的行为规则

- 未知节点需要通过邀请才能加入网络；严禁绕过这些规则。
- 高风险能力的发布需要人工批准。
- 必须遵守调用者权限限制（`OPENCLAW_ALLOWED_CALLERS`）和高风险操作标志。
- 绝不允许在明文消息、日志或共享状态中暴露令牌。
- 当启用了签名验证机制时，只接受由可信发布者签名的能力声明。

## 网关兼容性协议（Gateway Compatibility Protocol）

- 在使用某个工具之前，必须验证其插件是否已安装且可正常使用。
- 在修改协调设置之前，需确认节点属于骨干节点还是边缘节点。
- 将网关的运行状态视为拓扑结构和健康状况的权威信息来源。

## 可靠性模型

- **共享状态（Shared State）**：所有节点共享的 Yjs 状态具有最高权威性。
- **消息传递机制（Message Delivery）**：
  - 消息和任务会持久保存在共享状态中。
  - 系统会尽力实时将任务分配给相应的会话。
  - 通过定期扫描来恢复因网络问题导致的任务遗漏。
  - 对于临时性的发送失败，系统会进行重试，并设置合理的超时机制。
  - 任务分配完成后，会通知相关操作者。

## 操作规则

- 使用 `ansible_status` 和 `ansible_read_messages` 来检查任务的执行状态。
- 如果使用轮询模式，必须通过 `ansible_send_message` 进行响应。
- 使用 `corr:<messageId>` 来保持消息处理的连贯性。
- 监听器行为（listener behavior）是一种优化机制，主要负责在必要时进行数据清理和重新同步。

## 能力合约（Capability Contracts）

- 能力（capability）不仅仅是一个标签，而是一个包含详细规则的合约。
- 合约中会指定请求者和执行者的信息。
- 发布更新时，系统会自动在网格范围内进行路由。
- 系统会验证发布者的身份，并确保其具有可信的签名。
- 高风险合约需要人工批准。
- 取消发布会立即移除节点的相应权限。
- 生命周期管理过程中必须记录所有的安装和执行结果。

## 委托协议（Delegation Protocol）

- 请求者（Requester）创建任务时，需要指定目标、上下文、接受标准以及目标代理（`to_agents` 或具体能力）。
- 执行者（Executor）接收到任务后，会发送接受信号或预计完成时间。
- 执行者完成任务后，会提供进度信息并返回结构化的结果。
- 请求者会向相关人员或下游代理报告最终结果。

## 协调器行为（Coordinator Behavior）

- 协调器会定期检查锁定的资源是否过期、服务水平协议（SLA）是否偏离以及任务积压情况。
- 当任务范围不明确时，优先采用仅记录日志的升级策略。
- 在系统性能下降时，优先考虑控制风险、提高可见性并确保任务的确定性恢复。

## 可用的工具

### 通信工具（Communication Tools）

| 工具          | 功能                |
|------------------|-------------------|
| `ansible_send_message` | 向网格中的所有节点发送目标消息或广播消息 |
| `ansible_read_messages` | 读取未读消息或全部消息历史记录 |
| `ansible_mark_read` | 标记消息为已读             |
| `ansible_delete_messages` | 仅管理员可用的紧急消息删除功能 |

### 任务委托工具（Task Delegation Tools）

| 工具          | 功能                |
|------------------|-------------------|
| `ansibledelegate_task` | 为其他节点或代理创建任务           |
| `ansible_claim_task` | 声明对任务的拥有权           |
| `ansible_update_task` | 更新任务状态或进度             |
| `ansible_complete_task` | 完成任务并通知请求者           |
| `ansible_find_task` | 根据 ID 或标题查找任务           |

### 上下文与状态管理工具（Context and Status Tools）

| 工具          | 功能                |
|------------------|-------------------|
| `ansible_status` | 显示网格的健康状况、未读消息、待处理任务及拓扑结构 |
| `ansible_update_context` | 更新共享的上下文、线程信息和决策内容 |

### 协调与治理工具（Coordination and Governance Tools）

| 工具          | 功能                |
|------------------|-------------------|
| `ansible_get_coordination` | 读取协调器配置             |
| `ansible_set_coordination_preference` | 设置节点的协调器偏好           |
| `ansible_set_coordination` | 更换协调器（需谨慎操作）         |
| `ansible_set_retention` | 配置已完成任务的保留策略         |
| `ansible_get_delegation_policy` | 读取当前的委托策略           |
| `ansible_set_delegation_policy` | 发布/更新委托策略           |
| `ansible_ack_delegation_policy` | 确认委托策略的版本           |
| `ansible_lock_sweep_status` | 检查锁定清理的进度           |

## 能力生命周期管理工具（Capability Lifecycle Tools）

| 工具          | 功能                |
|------------------|-------------------|
| `ansible_list_capabilities` | 列出已发布的所有能力合约         |
| `ansiblecapability_publish` | 发布或升级能力合约           |
| `ansiblecapability_unpublish` | 从路由表中移除能力           |
| `ansiblecapability_lifecycle_evidence` | 显示能力的安装和执行记录         |
| `ansiblecapability_health_summary` | 显示能力的执行结果（成功/失败/延迟情况） |

## 使用 Ansible 的场景

- 当任务需要跨多个网关执行时。
- 当需要持久性的协调机制时。
- 当需要可审计的委托流程时。

## 会话管理（Session Management）

- 首先检查当前的状态和待处理的任务。
- 对于需要明确委托的任务，建议采用显式的委托方式。
- 通过生命周期相关的消息保持人类的参与度。

## 消息协议（Message Protocol v1）

- 消息中必须包含足够的上下文信息，以便其他节点能够独立执行任务。
- 使用稳定的关联 ID（`corr`）和对话 ID（conversation ID）来标识消息。
- 建议使用结构化的数据格式，而非自由形式的文本消息。

## 配置 playbook

请按照插件配置和网关运行手册的指导来初始化网络拓扑、设置身份验证机制和信任规则。

## 委托管理

- 确保所有节点都使用最新的委托策略，并确保这些策略得到正确执行。
- 将能力的发布视为合约的正式发布。
- 如果生命周期管理的数据表明存在问题，应立即回滚相关设置。