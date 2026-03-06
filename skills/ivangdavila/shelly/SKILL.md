---
name: Shelly
slug: shelly
version: 1.0.0
homepage: https://clawic.com/skills/shelly
description: 通过本地 RPC 工作流程、安全的访问模式、云 API 协调以及多设备的安全执行方式，实现对 Shelly 设备的控制和自动化操作。
changelog: Initial release with Shelly local and cloud operations for discovery, command control, telemetry checks, orchestration, and incident-safe rollouts.
metadata: {"clawdbot":{"emoji":"S","requires":{"bins":["curl","jq"],"env":["SHELLY_CLOUD_TOKEN"]},"primaryEnv":"SHELLY_CLOUD_TOKEN","os":["linux","darwin","win32"]}}
---
## 设置（Setup）

首次使用时，请阅读 `setup.md` 文件，明确激活边界、本地网络范围以及写入安全的默认设置，然后再发送 Shelly 命令。

## 使用场景（When to Use）

当用户需要实际执行 Shelly 操作时，可以使用此技能：例如进行本地 RPC 控制、状态和遥测数据读取、云辅助操作、设备分组或分阶段自动化等。如果结果依赖于 Shelly 特定的 RPC 行为、传输通道选择或安全的多设备部署策略，应优先使用此技能，而非通用的 IoT 解决方案。

## 架构（Architecture）

内存数据存储在 `~/shelly/` 目录下。具体结构及状态值请参阅 `memory-template.md` 文件。

```text
~/shelly/
|-- memory.md                 # Core context and activation boundaries
|-- environments.md           # LAN segments, cloud context, and endpoint mapping
|-- devices.md                # Device registry, components, and command patterns
|-- automations.md            # Sequencing rules, schedules, and rollback plans
`-- incidents.md              # Failure signatures and validated recoveries
```

## 快速参考（Quick Reference）

根据当前任务的需要，仅使用最相关的文件。

| 主题 | 文件名       |
|-------|------------|
| 设置与激活行为 | setup.md      |
| 内存与工作区模板 | memory-template.md |
| 协议与传输方式 | protocol-matrix.md |
| 访问与认证机制 | auth-and-access.md |
| 设备命令与状态管理 | device-operations.md |
| 多设备部署方案 | orchestration-playbooks.md |
| 故障排除 | troubleshooting.md |

## 必备条件（Requirements）

- 确保 Shelly 设备可以在目标本地网络中访问；或具备云账户访问权限（适用于云模式）
- 对于云操作，需在环境变量中设置 `SHELLY_CLOUD_TOKEN`
- 为了实现可靠的自动化，需要稳定的设备 ID、组件 ID 以及明确的执行边界

**注意**：切勿要求用户在聊天记录中输入生产环境中的敏感信息。建议使用本地环境变量或经过脱敏处理的示例数据。

## 数据存储（Data Storage）

将本地操作相关的数据保存在 `~/shelly/` 目录下：
- 网络配置与端点信息
- 设备组件映射及经过验证的 RPC 方法
- 自动化策略、执行顺序及回滚规则
- 事件日志及相应的应对措施

## 核心规则（Core Rules）

### 1. 在执行操作前选择正确的控制方式
- 在发出命令之前，明确选择仅限本地操作、云辅助操作或混合操作模式。
- 如果控制方式不明确（导致状态和命令结果不一致），应阻止操作的执行。

### 2. 根据任务需求选择合适的传输通道
- 使用本地 HTTP RPC 进行直接控制和确定性数据读取。
- 对于需要实时状态更新的场景，使用 WebSocket 通知；对于需要集成消息代理的事件处理，使用 MQTT。

### 3. 在写入数据前先识别设备组件及其功能
- 在生成命令之前，先读取设备状态和组件信息。
- 仅针对存在的组件 ID 及支持的方法参数执行写入操作。

### 4. 采用“先读取后写入”的机制
- 每次写入数据前先捕获设备基线状态。
- 执行后验证设备状态，如状态不一致则停止后续操作。

### 5. 对高影响操作实施明确的安全限制
- 对于可能带来重大影响的操作（如电源切换、加热控制、锁定、报警或批量更新），必须获得明确确认。

### 6. 保持本地视图与云视图的一致性
- 当本地 RPC 与云端的响应不一致时，需重新核对设备状态。
- 如果设备可访问，优先使用本地状态数据进行即时决策。

### 7. 设计可重试且可观察的自动化流程
- 使用唯一的执行 ID、有限的重试次数以及明确的停止条件。
- 记录每个执行步骤及预期的状态变化，以避免重复或部分操作。

### 8. 保护安全与隐私
- 使用最小权限的认证信息，并仅访问已声明的端点。
- 从环境变量中获取云访问令牌，切勿将原始凭证保存在本地文件中。

## 常见错误（Common Traps）

- 未明确优先级的情况下混合使用本地和云控制方式，可能导致状态冲突或数据重复写入。
- 在未验证组件 ID 的情况下发送 RPC 请求，可能导致请求被拒绝或目标设备行为异常。
- 将传输通道视为可互换的，可能在负载情况下导致延迟或可靠性问题。
- 在未进行测试的情况下批量执行操作，可能导致某个配置错误的操作影响整个系统。
- 误认为通知流表示操作成功，但实际上并未达到预期状态。
- 将云访问令牌以明文形式保存在本地文件中，可能导致不必要的安全风险。

## 外部端点（External Endpoints）

| 端点地址 | 发送的数据 | 功能       |
|------------|------------|-----------|
| http://<device-ip>/rpc | RPC 方法名称、参数及请求标识符 | 本地 Shelly 设备控制与状态查询 |
| ws://<device-ip>/rpc | RPC 消息及事件订阅 | 本地 WebSocket 通知与事件流处理 |
| mqtt://<broker> | 设备状态及命令主题（含数据 payload） | 基于 MQTT 的事件处理与自动化集成 |
| https://*.shelly.cloud | 账户级别的 API 请求、设备元数据及命令数据 | Shelly 云服务控制与远程设备操作 |
| https://shelly-api-docs.shelly.cloud | 文档查询 | 验证 Shelly API 的行为与方法限制 |

**注意**：不会向外部发送其他类型的数据。

## 安全与隐私（Security & Privacy）

**离开您系统的数据：**
- 用于执行 Shelly 操作的本地 RPC 或云 API 数据
- 用户配置的 MQTT 发布/订阅数据（可选）

**保留在本地的数据：**
- 环境配置信息、设备功能说明及自动化脚本（位于 `~/shelly/` 目录下）
- 事件日志及回滚策略

**此技能不会：**
- 使用未声明的第三方端点
- 采用绕过安全机制的技巧
- 将 `SHELLY_CLOUD_TOKEN` 保存在本地文件中
- 在未经用户确认的情况下执行批量写入操作

## 信任机制（Trust）

此技能会在获得授权后，将操作数据发送到 Shelly 设备或云服务。只有在您信任网络环境、代理设置以及 Shelly 账户权限的情况下，才建议安装此技能。

**相关技能（Related Skills）**

如用户同意，可使用以下命令进行安装：
- `clawhub install <slug>`：
  - `iot`：设备连接性与 IoT 系统集成
  - `smart-home`：家庭自动化架构与可靠性实践
  - `api`：API 设计与高效请求处理
  - `mqtt`：用于遥测和事件驱动的通信协议
  - `home-server`：自托管服务操作与网络可靠性管理

## 反馈建议（Feedback）

- 如此技能对您有帮助，请点赞：`clawhub star shelly`
- 保持更新：`clawhub sync`