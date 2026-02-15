---
name: Azure
description: 使用经过实战验证的方法来部署、监控和管理 Azure 服务。
metadata: {"clawdbot":{"emoji":"🔷","requires":{"anyBins":["az"]},"os":["linux","darwin","win32"]}}
---

# Azure 生产环境规则

## 成本陷阱
- 已关闭的虚拟机（VM）仍会继续支付所连接的磁盘和公共 IP 的费用——请使用 `az vm deallocate` 命令彻底释放资源，而不仅仅是通过门户界面停止使用它们。
- 新创建的虚拟机默认使用高级（Premium）SSD——在开发/测试环境中应切换为标准（Standard）SSD，可节省 50% 以上的成本。
- Log Analytics 的工作区默认提供 30 天的免费存储空间，之后按 GB 收费——在生产环境之前，请设置数据保留策略和每日使用上限。
- 区域间的带宽费用是双向收取的——请确保相关资源位于同一区域内；如需跨区域通信，请使用 Private Link。
- 即使在空闲状态下，Cosmos DB 也会根据配置的 RU（资源单位）收费——对于突发性工作负载，建议使用无服务器（serverless）解决方案或配置最小 RU 的自动扩展功能。

## 安全规则
- 资源组（Resource Groups）本身不提供网络隔离功能——NSG（Network Security Groups）和 Private Endpoints 才能实现网络隔离。资源组主要用于管理，而非定义安全边界。
- “管理身份”（Managed Identity）功能可消除 Azure 之间的身份验证过程中的密钥管理需求——对于单个资源，使用系统分配的身份（System Assigned）；对于需要共享身份的场景，使用用户分配的身份（User Assigned）。
- Key Vault 默认启用“软删除”功能（数据保留 90 天）——在数据被彻底清除之前，无法重复使用相同的密钥库名称，请提前规划命名策略。
- Azure AD 的条件访问策略不适用于服务主体（Service Principals）——建议使用带有证书认证的应用程序注册（App Registrations）而非客户端密钥。
- Private Endpoints 不会自动更新 DNS 设置——请配置 Private DNS 区域，并将其与虚拟网络（VNet）关联，否则可能导致解析失败。

## 网络配置
- NSG 规则按优先级执行（优先级数字越低，规则越先生效）——默认规则（优先级 65000 以上）总是会被自定义规则覆盖。
- Application Gateway v2 需要专用的子网——建议为自动扩展配置至少 /24 的子网规模。
- 使用 Azure Firewall 的高级（Premium）版本才能进行 TLS 检查和入侵防御（IDPS）——标准版本无法检测加密流量。
- 虚拟网络（VNet）之间的对等连接（peering）不具备传递性——采用“中心辐射”（hub-and-spoke）架构时，每个分支节点都需要单独配置路由；或者使用 Azure Virtual WAN。
- 服务端点（Service Endpoints）会暴露整个服务给虚拟网络，而 Private Endpoints 为特定资源实例提供私有 IP 地址。

## 性能优化
- Azure Functions 的消费计划存在冷启动现象——对于对延迟敏感的应用，建议选择高级（Premium）计划并配置最少实例数。
- Cosmos DB 的分区键（partition key）选择是永久性的，会影响系统的扩展能力——更改分区键需要重新创建容器。
- App Service 的资源密度设置：P1v3 计划最多支持约 10 个服务实例，更多实例可能导致资源竞争——请监控每个实例的 CPU 和内存使用情况。
- Azure Cache for Redis 的标准（Standard）层级没有复制相关的 SLA 保障——如需持久性和集群功能，请选择高级（Premium）层级。
- 对于频繁访问的数据，建议使用 Blob Storage 的“热层级”（hot tier）；“冷层级”数据至少保留 30 天，归档数据则保留 180 天，并且恢复数据需要较长时间。

## 监控与日志管理
- 当数据量较大时，Application Insights 的数据采样频率会降低——这可能导致某些间歇性错误被忽略，请调整 `MaxTelemetryItemsPerSecond` 参数。
- Azure Monitor 的警报规则按跟踪的指标数量计费——对于复杂的警报需求，建议将多个指标整合到 Log Analytics 中进行统一管理。
- 活动日志（Activity Log）仅显示控制平面（control plane）的操作信息——若需要监控数据平面（如 blob 存取、SQL 查询）的操作，需启用相应的诊断功能。
- 警报动作组（Alert Action Groups）有使用频率限制：每个组每 5 分钟最多发送 1 条短信、1 条语音邮件或 100 封电子邮件。
- Log Analytics 的查询超时时间为 10 分钟——建议先使用时间过滤器优化查询语句，再考虑其他筛选条件。

## 基础设施即代码（Infrastructure as Code）
- 当某些属性发生变化时，ARM（Azure Resource Manager）模板可能不会立即显示错误信息——请使用“what-if”部署模式预览更改效果。
- Terraform 的 `azurerm` 提供者会将配置信息以明文形式存储——建议使用带有加密功能的远程后端（如 Azure Storage 和客户自定的密钥）来保护这些信息。
- Bicep 是 ARM 的替代工具，具有更好的开发体验，适用于新项目。
- 资源锁定机制可以防止意外删除操作，但某些操作仍可能被阻止——即使被锁定，某些操作仍然可以执行（例如 `CanNotDelete` 操作）。
- Azure Policy 会在资源创建和更新时自动应用相应的规则——对于不符合要求的现有资源，需要执行修复操作。

## 身份与访问控制
- 角色分配（RBAC）的生效可能需要最多 30 分钟——在分配后立即执行可能失败。
- 如果 PIM（Principal Identity Management）要求审批流程，所有者角色（Owner Role）无法直接管理角色分配——请使用专门的“用户访问管理员”（User Access Administrator）角色。
- 服务主体的密钥默认有效期为 1 年——请设置定期提醒或使用有效期更长的证书。
- Azure AD 的 B2C（Business-to-Customer）服务与普通 Azure AD 服务是分开的——它们属于不同的租户，使用不同的 API 和定价策略。