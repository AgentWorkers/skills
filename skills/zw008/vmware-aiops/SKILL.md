---
name: vmware-aiops
description: 基于人工智能的 VMware vCenter/ESXi 监控与运维工具。支持通过自然语言进行基础设施管理：包括库存查询、健康状态监控、虚拟机生命周期管理（创建、删除、启动/关闭、快照生成、克隆、迁移）、虚拟机部署（使用 OVA、模板或链接克隆方式）、数据存储管理、vSAN 系统管理、Aria Operations 分析工具、Kubernetes 集群管理，以及定期日志扫描功能。
installer:
  kind: uv
  package: vmware-aiops
---
# VMware AIops

这是一个由人工智能驱动的 VMware vCenter 和 ESXi 操作工具，支持通过任何 AI 编码助手使用自然语言来管理您的整个 VMware 基础设施。

> **只需要只读监控功能吗？** 可以使用 [VMware-Monitor](https://github.com/zw008/VMware-Monitor)——这是一个代码级别安全的独立仓库（代码库中没有任何破坏性代码）。安装方法：`clawhub install vmware-monitor`

## 适用场景

- 查询虚拟机（VM）、主机、数据存储（datastore）、集群（cluster）和网络（network）的库存信息
- 检查健康状态、活动警报、硬件传感器和事件日志
- 执行虚拟机的生命周期操作：开机/关机、创建、删除、快照、克隆、迁移
- 从 OVA（Open Virtual Appliance）、模板、链接克隆或批量规格文件（batch specs）部署虚拟机
- 浏览数据存储，并发现 ISO/OVA/VMDK 镜像
- 监控 vSAN 的健康状况、容量、磁盘组和性能
- 访问 Aria Operations（VCF Operations）以获取历史指标、异常检测和容量规划信息
- 管理 vSphere Kubernetes Service（VKS）集群
- 运行带有 Webhook 通知（Slack、Discord）的定时扫描

## 快速安装

该工具兼容 Claude Code、Cursor、Codex、Gemini CLI、Trae、Kimi 以及 30 多种 AI 代理：

```bash
# Via Skills.sh
npx skills add zw008/VMware-AIops

# Via ClawHub
clawhub install vmware-aiops
```

### Claude Code

```
/plugin marketplace add zw008/VMware-AIops
/plugin install vmware-ops
/vmware-ops:vmware-aiops
```

## 使用模式

根据您的 AI 工具选择最佳模式：

| 平台 | 推荐模式 | 原因 |
|----------|-----------------|-----|
| Claude Code、Cursor | **MCP** | 结构化的工具调用，无需交互式确认，体验流畅 |
| Aider、Codex、Gemini CLI、Continue | **CLI** | 体积轻量，上下文开销低，兼容性广泛 |
| Ollama + 本地模型 | **CLI** | 对模型大小要求低，适用性高 |

### 调用优先级

- **MCP 内置工具**（Claude Code、Cursor）：优先使用 MCP，CLI 作为备用方案
- **其他所有工具**：优先使用 CLI（无需 MCP）

> **提示**：如果您的 AI 工具支持 MCP，请检查 `vmware-aiops` MCP 服务器是否已加载（在 Claude Code 中为 `/mcp`）。如果没有，请先配置它——MCP 可提供最佳的无操作员干预体验。

### CLI 示例

```bash
# Activate venv first
source /path/to/VMware-AIops/.venv/bin/activate

# Inventory
vmware-aiops inventory vms --target home-esxi
vmware-aiops inventory hosts --target home-esxi

# Health
vmware-aiops health alarms --target home-esxi

# VM operations
vmware-aiops vm info my-vm --target home-esxi
vmware-aiops vm power-on my-vm --target home-esxi
```

### MCP 模式（可选）

对于偏好结构化工具调用的 Claude Code/Cursor 用户，请在 `~/.claude/settings.json` 中添加以下配置：

```json
{
  "mcpServers": {
    "vmware-aiops": {
      "command": "/path/to/VMware-AIops/.venv/bin/python",
      "args": ["-m", "mcp_server"],
      "cwd": "/path/to/VMware-AIops",
      "env": {
        "VMWARE_AIOPS_CONFIG": "~/.vmware-aiops/config.yaml"
      }
    }
  }
}
```

MCP 提供了 20 个工具：`list_virtual_machines`、`list_esxi_hosts`、`list_all_datastores`、`list_all_clusters`、`get_alarms`、`get_events`、`vm_info`、`vm_power_on`、`vm_power_off`、`browse_datastore`、`scan_datastore_images`、`list_cached_images`、`deploy_vm_from_ova`、`deploy_vm_from_template`、`deploy_linked_clone`、`attach_iso_to_vm`、`convert_vm_to_template`、`batch_clone_vms`、`batch_linked_clone_vms`、`batch_deploy_from_spec`。所有这些工具都支持可选的 `target` 参数。

## 架构

```
User (Natural Language)
  ↓
AI Tool (Claude Code / Aider / Gemini / Codex / Cursor / Trae / Kimi)
  ↓
  ├─ CLI mode (default): vmware-aiops CLI ──→ pyVmomi ──→ vSphere API
  │
  └─ MCP mode (optional): MCP Server (stdio) ──→ pyVmomi ──→ vSphere API
  ↓
vCenter Server ──→ ESXi Clusters ──→ VMs
    or
ESXi Standalone ──→ VMs
```

## 功能

### 1. 库存管理

| 功能 | vCenter | ESXi | 详情 |
|---------|:-------:|:----:|---------|
| 列出虚拟机 | ✅ | ✅ | 名称、电源状态、CPU、内存、客户机操作系统（guest OS）、IP 地址 |
| 列出主机 | ✅ | ⚠️ 仅适用于 ESXi | CPU 核心数、内存、ESXi 版本、虚拟机数量、运行时间 |
| 列出数据存储 | ✅ | ✅ | 容量、可用/已用空间、类型（VMFS/NFS）、使用率 |
| 列出集群 | ✅ | ❌ | 主机数量、DRS/HA 状态 |
| 列出网络 | ✅ | ✅ | 网络名称、关联的虚拟机数量 |

### 2. 健康与监控

| 功能 | vCenter | ESXi | 详情 |
|---------|:-------:|:----:|---------|
| 活动警报 | ✅ | ✅ | 严重程度、警报名称、相关实体、时间戳 |
| 事件/日志查询 | ✅ | ✅ | 可按时间范围和严重程度过滤；支持 50 多种事件类型 |
| 硬件传感器 | ✅ | ✅ | 温度、电压、风扇状态 |
| 主机服务 | ✅ | ✅ | hostd、vpxa 的运行/停止状态 |

**监控的事件类型：**

| 类别 | 事件类型 |
|----------|--------|
| 虚拟机故障 | `VmFailedToPowerOnEvent`、`VmDiskFailedEvent`、`VmFailoverFailed` |
| 主机问题 | `HostConnectionLostEvent`、`HostShutdownEvent`、`HostIpChangedEvent` |
| 存储 | `DatastoreCapacityIncreasedEvent`、SCSI 高延迟 |
| HA/DRS | `DasHostFailedEvent`、`DrsVmMigratedEvent`、`DrsSoftRuleViolationEvent` |
| 认证 | `UserLoginSessionEvent`、`BadUsernameSessionEvent` |

### 3. 虚拟机生命周期管理

| 操作 | 命令 | 需要确认 | vCenter | ESXi |
|-----------|---------|:------------:|:-------:|:----:|
| 开机 | `vm power-on <名称>` | — | ✅ | ✅ |
| 优雅关机 | `vm power-off <名称>` | 双重确认 | ✅ | ✅ |
| 强制关机 | `vm power-off <名称> --force` | 双重确认 | ✅ | ✅ |
| 重置 | `vm reset <名称>` | — | ✅ | ✅ |
| 暂停 | `vm suspend <名称>` | — | ✅ | ✅ |
| 虚拟机信息 | `vm info <名称>` | — | ✅ | ✅ |
| 创建虚拟机 | `vm create <名称> --cpu --memory --disk` | — | ✅ | ✅ |
| 删除虚拟机 | `vm delete <名称>` | 双重确认 | ✅ | ✅ |
| 重新配置 | `vm reconfigure <名称> --cpu --memory` | 双重确认 | ✅ | ✅ |
| 创建快照 | `vm snapshot-create <名称> --name <快照名称>` | — | ✅ | ✅ |
| 列出快照 | `vm snapshot-list <名称>` | — | ✅ | ✅ |
| 恢复快照 | `vm snapshot-revert <名称> --name <快照名称>` | — | ✅ | ✅ |
| 删除快照 | `vm snapshot-delete <名称> --name <快照名称>` | — | ✅ | ✅ |
| 克隆虚拟机 | `vm clone <名称> --new-name <新名称>` | — | ✅ | ✅ |
| vMotion | `vm migrate <名称> --to-host <目标主机>` | — | ✅ | ❌ |

### 4. 虚拟机部署与配置

| 操作 | 命令 | 执行速度 | vCenter | ESXi |
|-----------|---------|:-----:|:-------:|:----:|
| 从 OVA 部署 | `deploy ova <路径> --名称 <虚拟机>` | 几分钟 | ✅ | ✅ |
| 从模板部署 | `deploy template <模板> --名称 <虚拟机>` | 几分钟 | ✅ | ✅ |
| 链接克隆 | `deploy linked-clone --源虚拟机 <源虚拟机> --快照 <快照名称> --名称 <新名称>` | 几秒 | ✅ | ✅ |
| 附加 ISO 镜像 | `deploy iso <虚拟机> --iso "[数据存储路径]/[ISO 文件路径]"` | 即时 | ✅ | ✅ |
| 转换为模板 | `deploy mark-template <虚拟机>` | 即时 | ✅ | ✅ |
| 批量克隆 | `deploy batch-clone --源虚拟机 <源虚拟机> --数量 <数量>` | 几分钟 | ✅ | ✅ |
| 批量部署（YAML） | `deploy batch spec.yaml` | 自动 | ✅ | ✅ |

### 5. 数据存储浏览器

| 功能 | vCenter | ESXi | 详情 |
|---------|:-------:|:----:|---------|
| 浏览文件 | ✅ | ✅ | 可以浏览任何数据存储路径下的文件/文件夹 |
| 扫描镜像 | ✅ | ✅ | 可发现所有数据存储中的 ISO、OVA、OVF、VMDK 镜像 |
| 本地缓存 | ✅ | ✅ | 缓存信息存储在 `~/.vmware-aiops/imageRegistry.json` 文件中 |

### 6. vSAN 管理

| 功能 | 详情 |
|---------|---------|
| 健康检查 | 集群范围内的健康状况总结，按组显示测试结果 |
| 容量 | 总容量/可用容量/已用容量及预测 |
| 磁盘组 | 每个主机的缓存 SSD 和容量磁盘 |
| 性能 | 每个集群/主机的 IOPS、延迟、吞吐量 |

> 需要 pyVmomi 8.0.3 或更高版本（vSAN SDK 已合并）。对于旧版本，请安装独立的 vSAN Management SDK。

### 7. Aria Operations（VCF Operations）

| 功能 | 详情 |
|---------|---------|
| 历史指标 | 提供几个月的历史数据，包括 CPU、内存、磁盘和网络指标 |
| 异常检测 | 基于机器学习的动态基准和异常警报 |
| 容量规划 | 可进行假设分析、预测资源耗尽时间 |
| 容量调整 | 为每个虚拟机提供 CPU/内存建议 |
| 智能警报 | 提供根本原因分析和修复建议 |

> REST API 地址为 `/suite-api/`。认证方式：`vRealizeOpsToken`。在 VCF 9.0 中更名为 VCF Operations。

### 8. vSphere Kubernetes Service (VKS)

| 功能 | 详情 |
|---------|---------|
| 列出集群 | 显示 Tanzu Kubernetes 集群及其阶段状态 |
| 集群健康 | 显示基础设施就绪情况、控制平面可用性、工作节点可用性 |
| 调整工作节点数量 | 可调整机器部署的副本数量 |
| 节点状态 | 显示节点状态及健康状况 |

> 通过 kubectl/kubeconfig 使用 Kubernetes 原生 API。VKS 3.6 及更高版本支持 Cluster API 规范。

### 9. 定时扫描与通知

| 功能 | 详情 |
|---------|---------|
| 定时扫描 | 基于 APScheduler，可配置扫描间隔（默认为 15 分钟） |
| 多目标扫描 | 依次扫描所有配置的 vCenter/ESXi 目标 |
| 扫描内容 | 包括警报、事件和主机日志（hostd、vmkernel、vpxd） |
| 日志分析 | 支持正则表达式匹配：错误、失败、严重、恐慌、超时等日志类型 |
| Webhook | 可发送通知到 Slack、Discord 或任何 HTTP 端点 |

## 安全特性

| 功能 | 详情 |
|---------|---------|
| 计划 → 确认 → 执行 → 记录日志 | 采用结构化的工作流程：显示当前状态、确认更改、执行操作、记录审计日志 |
| 双重确认 | 所有具有破坏性的操作（关机、删除、重新配置、恢复快照/删除、克隆、迁移）都需要两次确认——不允许跳过确认步骤 |
| 拒绝记录 | 被拒绝的确认操作会记录在审计日志中，以便安全审查 |
| 审计日志 | 所有操作都会记录在 `~/.vmware-aiops/audit.log`（JSONL 格式）文件中，包括操作前后的状态 |
| 输入验证 | 在执行前会验证虚拟机名称的长度和格式、CPU（1-128）、内存（128-1048576 MB）、磁盘（1-65536 GB） |
| 密码保护 | 密码通过 `.env` 文件加载，不会出现在命令行或 shell 历史记录中；启动时会检查文件权限 |
| SSL 自签名证书支持 | `disableSslCertValidation` 选项仅适用于使用自签名证书的 ESXi 主机（常见于实验室/家庭环境）。生产环境应使用经过 CA 签名的证书，并启用完整的 TLS 验证 |
| 任务等待 | 所有异步操作都会等待完成并报告结果 |
| 状态验证 | 操作前会检查虚拟机是否存在以及其电源状态是否正确 |

## 版本兼容性

| vSphere 版本 | 支持情况 | 备注 |
|----------------|---------|-------|
| 8.0 / 8.0U1-U3 | 完全支持 | `CreateSnapshot_Task` 方法已被弃用，建议使用 `CreateSnapshotEx_Task` |
| 7.0 / 7.0U1-U3 | 完全支持 | 所有 API 都可用 |
| 6.7 | 兼容 | 经过测试，支持向后兼容 |
| 6.5 | 兼容 | 经过测试，支持向后兼容 |

> pyVmomi 会在 SOAP 握手过程中自动协商 API 版本——无需手动配置。

## 支持的 AI 平台

| 平台 | 支持情况 | 配置文件 |
|----------|--------|-------------|
| Claude Code | ✅ | 内置支持 | `plugins/.../SKILL.md` |
| Gemini CLI | ✅ | 作为扩展支持 | `gemini-extension/GEMINI.md` |
| OpenAI Codex CLI | ✅ | 通过 AGENTS.md 文件支持 | `codex-skill/AGENTS.md` |
| Aider | ✅ | 通过 conventions 文件支持 | `codex-skill/AGENTS.md` |
| Continue CLI | ✅ | 通过 rules 文件支持 | `codex-skill/AGENTS.md` |
| Trae IDE | ✅ | 通过 rules 文件支持 | `trae-rules/project_rules.md` |
| Kimi Code CLI | ✅ | 作为独立技能支持 | `kimi-skill/SKILL.md` |
| MCP Server | ✅ | 通过 MCP 协议支持 | `mcp_server/` |
| Python CLI | ✅ | 作为独立工具支持 | 不需要额外配置 |

## CLI 参考文档

```bash
# Inventory
vmware-aiops inventory vms [--target <name>]
vmware-aiops inventory hosts [--target <name>]
vmware-aiops inventory datastores [--target <name>]
vmware-aiops inventory clusters [--target <name>]

# Health
vmware-aiops health alarms [--target <name>]
vmware-aiops health events [--hours 24] [--severity warning]

# VM Operations
vmware-aiops vm info <vm-name>
vmware-aiops vm power-on <vm-name>
vmware-aiops vm power-off <vm-name> [--force]
vmware-aiops vm create <name> [--cpu <n>] [--memory <mb>] [--disk <gb>]
vmware-aiops vm delete <vm-name> [--confirm]
vmware-aiops vm reconfigure <vm-name> [--cpu <n>] [--memory <mb>]
vmware-aiops vm snapshot-create <vm-name> --name <snap-name>
vmware-aiops vm snapshot-list <vm-name>
vmware-aiops vm snapshot-revert <vm-name> --name <snap-name>
vmware-aiops vm snapshot-delete <vm-name> --name <snap-name>
vmware-aiops vm clone <vm-name> --new-name <name>
vmware-aiops vm migrate <vm-name> --to-host <host>

# Deploy
vmware-aiops deploy ova <path> --name <vm-name> [--datastore <ds>] [--network <net>]
vmware-aiops deploy template <template-name> --name <vm-name> [--datastore <ds>]
vmware-aiops deploy linked-clone --source <vm> --snapshot <snap> --name <new-name>
vmware-aiops deploy iso <vm-name> --iso "[datastore] path/file.iso"
vmware-aiops deploy mark-template <vm-name>
vmware-aiops deploy batch-clone --source <vm> --count <n> [--prefix <prefix>]
vmware-aiops deploy batch <spec.yaml>

# Datastore
vmware-aiops datastore browse <ds-name> [--path <subdir>]
vmware-aiops datastore scan-images [--target <name>]
vmware-aiops datastore images [--type ova|iso|vmdk] [--ds <name>]

# vSAN
vmware-aiops vsan health [--target <name>]
vmware-aiops vsan capacity [--target <name>]
vmware-aiops vsan disks [--target <name>]
vmware-aiops vsan performance [--hours 1]

# Aria Operations
vmware-aiops ops alerts [--severity critical]
vmware-aiops ops metrics <resource-name> [--hours 24]
vmware-aiops ops recommendations [--target <name>]
vmware-aiops ops capacity <cluster-name>

# VKS (Kubernetes)
vmware-aiops vks clusters [--namespace default]
vmware-aiops vks health <cluster-name>
vmware-aiops vks scale <machine-deployment> --replicas <n>
vmware-aiops vks nodes <cluster-name>

# Scanning & Daemon
vmware-aiops scan now [--target <name>]
vmware-aiops daemon start
vmware-aiops daemon stop
vmware-aiops daemon status
```

## 设置

```bash
# 1. Install via uv (recommended) or pip
uv tool install vmware-aiops
# Or: pip install vmware-aiops

# 2. Configure
mkdir -p ~/.vmware-aiops
vmware-aiops init  # generates config.yaml and .env templates
chmod 600 ~/.vmware-aiops/.env
# Edit ~/.vmware-aiops/config.yaml and .env with your target details
```

### 开发环境安装

```bash
git clone https://github.com/zw008/VMware-AIops.git
cd VMware-AIops
uv venv && source .venv/bin/activate
uv pip install -e .
```

## 安全性

- **TLS 验证**：默认启用。`disableSslCertValidation` 选项仅适用于使用自签名证书的 ESXi 主机（常见于实验室环境）。在生产环境中，必须使用经过 CA 签名的证书，并启用完整的 TLS 验证。
- **凭证管理**：凭证仅从 `.env` 文件中的环境变量加载（使用 `chmod 600` 设置权限）。切勿通过 CLI 参数、配置文件或 MCP 消息传递凭证。
- **Webhook 数据范围**：Webhook 通知仅发送到用户配置的 URL（Slack、Discord 或任何您控制的 HTTP 端点）。默认情况下，不会向第三方服务发送任何数据。
- **防止注入攻击**：所有来自 vSphere 的内容（事件消息、主机日志）在输出前都会被截断、去除控制字符，并用边界标记包裹。
- **代码审查**：建议在部署到生产环境之前审查源代码和提交历史记录。建议在隔离环境中进行初步测试。

## 许可证

MIT