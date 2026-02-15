---
name: Google Cloud
description: 使用经过实战验证的方法来部署、监控和管理 Google Cloud Platform (GCP) 服务。
metadata: {"clawdbot":{"emoji":"🌐","requires":{"anyBins":["gcloud"]},"os":["linux","darwin","win32"]}}
---

# Google Cloud 生产环境最佳实践

## 成本控制
- 已停止运行的 Compute Engine 虚拟机仍会支付持久磁盘和静态 IP 的费用——请删除磁盘或使用快照进行长期存储。
- Cloud NAT 会根据每个虚拟机处理的每 GB 数据量收费——建议使用 Private Google Access 来处理 GCP API 流量。
- BigQuery 的按需定价是基于扫描的字节数而非返回的行数——在开发环境中可以对表进行分区并使用 `LIMIT` 语句，但在生产环境中 `LIMIT` 无法降低扫描成本。
- 预备虚拟机（Preemptible VMs）可以节省 80% 的成本，但可能会随时被终止——仅适用于容错性要求较高的批处理工作负载。
- 出站到互联网的费用较高，而出站到同一区域内的数据传输是免费的——请将资源部署在同一区域内，并使用 Cloud CDN 进行全球分发。

## 安全性
- 服务账户同时扮演身份验证和资源管理的角色——一个服务账户可以通过 `roles/iam.serviceAccountTokenCreator` 来模拟另一个账户的权限。
- IAM 策略的继承顺序为：组织（Organization）→ 文件夹（Folder）→ 项目（Project）→ 资源（Resource）——在组织级别设置的拒绝策略会覆盖下层级别的允许策略。
- VPC 服务控制（VPC Service Controls）可以防止数据泄露——但如果未配置适当的访问权限，可能会导致 Cloud Console 访问失败。
- 默认的 Compute Engine 服务账户具有编辑者（Editor）权限——建议创建具有最小权限的专用服务账户。
- Workload Identity Federation 可以消除对服务账户密钥的需求——适用于 GitHub Actions、GitLab CI 等外部工作负载。

## 网络配置
- Google Cloud 的 VPC 是全球范围的，而子网（Subnets）是区域性的——与 AWS 不同，单个 VPC 可以覆盖所有区域。
- 防火墙规则默认设置为“仅允许”（allow-only）——即默认拒绝所有入站流量并允许所有出站流量。需要时请添加明确的拒绝规则来控制出站流量。
- Private Google Access 需要为每个子网单独配置——确保需要访问 GCP API 的子网都启用了该功能（尤其是那些没有公共 IP 的子网）。
- Cloud Load Balancer 有全局和区域两种类型——全局类型适用于多区域环境，而区域类型适用于单区域环境，且成本更低。
- 共享 VPC（Shared VPC）将网络管理权限与项目管理权限分开——项目所有者拥有网络资源，服务项目则使用这些网络资源。

## 性能优化
- Cloud Functions 第一代的默认超时时间为 9 分钟，第二代（基于 Cloud Run）支持 60 分钟的超时设置。
- Cloud SQL 的连接限制因实例大小而异——建议使用连接池（Connection Pooling）或 Cloud SQL Auth Proxy 来优化连接管理。
- Firestore 和 Datastore 应使用 UUID 或反向时间戳作为文档 ID，以避免热点访问（hotspotting）问题。
- GKE Autopilot 可简化配置，但会带来一些限制——例如不允许使用 DaemonSets、特权容器或访问主机网络。
- Cloud Storage 单个对象的存储上限为 5TB——对于较大的文件，请使用 `compose` 命令进行分块上传以提高上传速度。

## 监控与日志管理
- Cloud Logging 的默认保留时间为 30 天，某些合规性要求可能需要更长的保留周期（例如 400 天）——请创建自定义存储桶以满足这些需求。
- Cloud Monitoring 的警报策略会在 24 小时后自动关闭——即使问题仍然存在，警报也会自动消失——请配置通知渠道以便及时重发警报。
- 错误报告应按照堆栈跟踪（stack trace）进行分类——相同的错误如果显示不同的信息可能会导致重复报告。
- Cloud Trace 的采样是自动进行的——可能会遗漏一些罕见错误——可以根据需要增加采样频率以便于调试。
- 审计日志（Audit Logs）中，管理员活动日志始终开启，数据访问日志默认是关闭的——为确保安全合规性，请根据需要启用数据访问日志。

## 基础设施即代码（Infrastructure as Code）
- 使用 Terraform 配置 Google Cloud 时，必须在所有地方使用 `project_id` 参数——建议使用 `google_project` 数据源或变量，避免硬编码。
- `gcloud` 命令是进行基础设施管理的必备工具——建议使用 Deployment Manager 或 Terraform 来确保配置的可重复性。
- Cloud Build 会在代码推送时触发构建过程，但首次运行时可能需要设置 IAM 权限——请在首次部署前为 Cloud Build 服务账户授予必要的权限。
- 项目删除后有 30 天的恢复期——但项目 ID 是全局唯一的，无法重复使用。
- 标签（Labels）会影响到费用分配——建议使用统一的标签（如 `env`、`team`、`service`）来方便成本管理。

## IAM（身份与访问管理）最佳实践
- 原始的权限角色（Owner/Editor/Viewer）过于宽泛——建议使用预定义的角色，并根据实际需求创建具有最小权限的定制角色。
- 服务账户密钥存在安全隐患——建议使用 Workload Identity、身份模拟（Impersonation）或附加的服务账户来替代它们。
- `roles/iam.serviceAccountUser` 允许用户以服务账户的身份执行操作——但在授予此类权限时需谨慎。
- 组织级策略（Organization Policies）可以限制各个项目的操作范围——例如 `constraints/compute.vmExternalIpAccess` 可以阻止所有项目访问外部 IP。

这些最佳实践有助于提高 Google Cloud 生产环境的效率、安全性和成本控制。在实际部署过程中，请根据具体需求灵活应用这些规则。