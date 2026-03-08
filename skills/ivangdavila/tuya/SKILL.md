---
name: Tuya Smart
slug: tuya
version: 1.0.0
homepage: https://clawic.com/skills/tuya
description: 通过官方的云API来控制和自动化Tuya智能设备，支持安全的请求签名机制、基于区域的路由功能以及安全的命令执行过程。
changelog: Initial release with end-to-end Tuya Smart workflows for authentication, account linking, device control, diagnostics, and safe rollout playbooks.
metadata: {"clawdbot":{"emoji":"T","requires":{"bins":["curl","jq","openssl"],"env":["TUYA_ACCESS_ID","TUYA_ACCESS_SECRET"]},"primaryEnv":"TUYA_ACCESS_SECRET","os":["linux","darwin","win32"]}}
---
## 设置

首次使用时，请先阅读 `setup.md` 文件，确保激活边界、云区域设置以及写入安全默认值配置正确，然后再发送 Tuya 命令。

## 使用场景

当用户需要在 Tuya 生态系统中执行实际操作时，可以使用此技能：例如云 API 认证、设备发现、基于 DPS 的命令控制、账户关联或自动化编排。  
在以下情况下应优先使用此技能：结果依赖于 Tuya Smart API 的行为、区域端点、请求签名或命令验证时，而非通用的 IoT 指导。

## 架构

内存数据存储在 `~/tuya/` 目录下。具体结构及状态值请参见 `memory-template.md` 文件。

```text
~/tuya/
|-- memory.md                 # Core context and activation boundaries
|-- environments.md           # Region, project, app-account, and endpoint mapping
|-- devices.md                # Device inventory, capabilities, and command mappings
|-- automations.md            # Cross-device orchestration plans and safeguards
`-- incidents.md              # Error signatures, fixes, and verification evidence
```

## 快速参考

根据当前任务的需要，仅使用最相关的文件。

| 主题 | 文件名 |
|-------|------|
| 设置与激活行为 | `setup.md` |
| 内存和工作区模板 | `memory-template.md` |
| 云认证与签名参考 | `auth-signing.md` |
| 用户账户与设备关联 | `account-linking.md` |
| 设备命令与状态管理 | `device-operations.md` |
| 多设备部署方案 | `orchestration-playbooks.md` |
| 故障排除 | `troubleshooting.md` |

## 所需条件

- Tuya IoT 平台项目凭证：访问 ID（Access ID）和访问密钥（Access Secret）  
- 环境变量：`TUYA_ACCESS_ID` 和 `TUYA_ACCESS_SECRET`  
- 项目数据中心对应的正确区域 OpenAPI 端点  
- 项目中已启用设备权限（包括云授权和所需 API 组）  
- 对于基于账户的设备绑定：需配置用户权限包及应用账户流程  

**注意**：切勿要求用户将生产环境中的敏感信息粘贴到聊天记录中。建议使用本地环境变量或经过脱敏处理的示例数据。

## 数据存储

本地操作相关数据存储在 `~/tuya/` 目录下：  
- 环境与端点映射信息  
- 按产品/设备 ID 分类的设备命令字典  
- 经审核的自动化策略及回滚方案  
- 事件日志及验证后的修复措施  

## 核心规则

### 1. 在任何 API 调用前确定区域和项目范围  
- 首先确认项目环境、应用类型及对应的区域端点。  
- 如果区域或项目信息不明确，禁止执行操作，否则可能导致令牌或设备请求失败，或错误地指向其他租户。  

### 2. 精确构建并验证 Tuya 签名信息  
- 使用 Tuya 文档中规定的 HMAC-SHA256 算法对所有请求进行签名。  
- 如果签名信息（`sign`、`t`、随机数（nonce）、请求体哈希值或签名后的头部信息不一致，视为无效请求，需重新构建后再尝试。  

### 3. 在发送命令前了解设备功能  
- 在执行写入操作前，先读取设备详细信息及功能规范。  
- 仅使用支持的 `code` 值及有效的数据类型/范围来生成命令。  

### 4. 实施“先读取后写入”的控制机制  
- 在执行命令前捕获设备的初始状态。  
- 每次写入操作后，验证设备状态；若状态不一致，立即停止后续操作。  

### 5. 对实际设备写入操作实施严格的安全控制  
- 先进行只读检查及命令计划的模拟运行。  
- 对于高影响操作（如开关电源、调节温度、锁定设备、触发警报或批量更新），必须获得明确确认。  

### 6. 保持账户关联与设备所有权的一致性  
- 确保应用账户模型、云项目权限及用户设备绑定流程的一致性。  
- 如果设备列表与控制 API 的信息不一致，需在排查问题前先解决账户关联问题。  

### 7. 设计可重试且可观察的自动化流程  
- 使用确定的运行 ID、有限的重试次数及明确的停止条件。  
- 通过预期状态检查来跟踪每个操作步骤，避免在多个设备上出现重复或部分操作。  

### 8. 保护安全与隐私  
- 使用最小权限的凭证，并仅访问已声明的 API 端点。  
- 从环境变量中读取凭证信息，切勿将原始凭证写入本地文件。  
- 将项目令牌视为临时运行数据，除非用户明确要求，否则不要持久化保存。  

## 常见错误  

- 选择错误的区域端点 → 有效凭证无效，导致设备查找失败。  
- 未检查功能规范就发送命令 → 命令无效，导致写入操作被拒绝。  
- 混淆应用账户与云账户的权限设置 → 用户看似已关联设备，但实际上无法控制设备。  
- 使用过时的时间戳/随机数重新发送已签名的请求 → 导致签名错误。  
- 未分阶段验证就批量执行命令 → 造成大规模的设备状态异常。  
- 将在线状态误认为是操作成功 → 命令虽被接受，但设备状态未改变。  

## 外部 API 端点  

| 端点 | 发送的数据 | 用途 |
|----------|-----------|---------|
| https://openapi.tuyaus.com | 经签名的 API 头部信息、设备 ID、命令数据及项目范围元数据 | 适用于美国地区的 Tuya OpenAPI 访问 |
| https://openapi-ueaz.tuyaus.com | 经签名的 API 头部信息、设备 ID、命令数据及项目范围元数据 | 适用于美国西部地区的 Tuya OpenAPI 访问 |
| https://openapi.tuyaeu.com | 经签名的 API 头部信息、设备 ID、命令数据及项目范围元数据 | 适用于欧洲地区的 Tuya OpenAPI 访问 |
| https://openapi-weaz.tuyaeu.com | 经签名的 API 头部信息、设备 ID、命令数据及项目范围元数据 | 适用于欧洲西部地区的 Tuya OpenAPI 访问 |
| https://openapi.tuyacn.com | 经签名的 API 头部信息、设备 ID、命令数据及项目范围元数据 | 适用于中国地区的 Tuya OpenAPI 访问 |
| https://openapi.tuyain.com | 经签名的 API 头部信息、设备 ID、命令数据及项目范围元数据 | 适用于印度地区的 Tuya OpenAPI 访问 |
| https://developer.tuya.com | 文档查询相关术语 | 验证 API 行为、限制及集成要求 |

**注意**：不会向外部发送其他类型的数据。  

## 安全与隐私  

**离开您机器的数据**：  
- 包含选定设备标识符及命令数据的已签名 Tuya API 请求  
- Tuya 用户/设备绑定 API 所要求的可选账户关联数据  

**保留在本地的数据**：  
- 环境映射信息、命令字典及自动化脚本（存储在 `~/tuya/` 目录下）  
- 事件日志及风险处理决策  

**此技能不包含以下行为**：  
- 使用未公开的第三方 API 端点  
- 采用绕过或规避安全机制的请求方式  
- 将 `TUYA_ACCESS_ID` 或 `TUYA_ACCESS_SECRET` 存储在本地文件中  
- 未经用户确认或验证就执行批量写入操作  

## 信任机制  

**注意事项**：  
只有在确认信任 Tuya 及其凭证处理机制的情况下，才应将操作数据发送至 Tuya 云服务。  

**相关技能**  
如用户同意，可使用以下命令安装相关工具：  
`clawhub install <slug>`  
- `iot`：设备连接及系统级 IoT 集成指南  
- `smart-home`：家庭自动化架构与可靠性实践  
- `api`：API 合同设计、认证流程及错误处理  
- `mqtt`：用于设备遥测和事件驱动的通信协议  
- `zigbee`：本地网络设备规划及 Zigbee 生态系统故障排查  

## 反馈建议：  
- 如觉得本文档有用，请点赞（`clawhub star tuya`）  
- 保持信息更新：`clawhub sync`