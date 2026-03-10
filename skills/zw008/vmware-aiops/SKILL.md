---
name: vmware-aiops
description: 基于人工智能的 VMware vCenter/ESXi 监控与运维工具。通过自然语言实现基础设施管理：库存查询、健康状态监控、虚拟机生命周期管理（创建、删除、启动/关闭、快照生成、克隆、迁移）、虚拟机部署（OVA、模板、链接克隆、批量部署）、数据存储浏览、vSAN 管理、Aria Operations 分析功能，以及对 Kubernetes 集群的支持和定时日志扫描。
installer:
  kind: uv
  package: vmware-aiops
metadata: {"openclaw":{"requires":{"env":["VMWARE_AIOPS_CONFIG"],"bins":["vmware-aiops"],"config":["~/.vmware-aiops/config.yaml"]},"primaryEnv":"VMWARE_AIOPS_CONFIG","homepage":"https://github.com/zw008/VMware-AIops"}}
---
# VMware AIops

这是一个由人工智能驱动的VMware vCenter和ESXi操作工具，允许您通过任何AI编码助手使用自然语言来管理整个VMware基础设施。

> **只需要只读监控功能吗？** 可以使用[VMware-Monitor](https://github.com/zw008/VMware-Monitor)——这是一个独立的仓库，其代码具有安全性（代码库中没有任何破坏性代码）。安装方法：`clawhub install vmware-monitor`

## 适用场景

- 查询虚拟机、主机、数据存储、集群和网络资源信息
- 检查健康状态、活动警报、硬件传感器和事件日志
- 执行虚拟机生命周期操作：开机/关机、创建、删除、快照、克隆、迁移
- 从OVA文件、模板、链接克隆或批量规格文件部署虚拟机
- 浏览数据存储并发现ISO/OVA/VMDK镜像
- 监控vSAN的健康状况、容量、磁盘组和性能
- 访问Aria Operations（VCF Operations）以获取历史指标、异常检测和容量规划信息
- 管理vSphere Kubernetes Service（VKS）集群
- 使用Webhook通知（Slack、Discord）执行定时扫描

## 快速安装

该工具兼容Claude Code、Cursor、Codex、Gemini CLI、Trae、Kimi以及30多种AI代理：

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

## 使用方式

根据您的环境选择最佳使用方式：

| 场景 | 推荐方式 | 原因 |
|----------|-----------------|-----|
| **云模型**（Claude、GPT-4o、Gemini） | MCP或CLI | 两者都适用；MCP提供结构化的JSON输入/输出 |
| **本地/小型模型**（Ollama、Llama、Qwen <32B） | **CLI** | 单位成本更低（约2K令牌对比约10K令牌），准确性更高——小型模型难以处理MCP工具的复杂架构 |
| **对令牌敏感的工作流程** | **CLI** | 通过SKILL.md使用的令牌量约为2K；MCP在每次对话中会加载约10K令牌来加载工具定义 |
| **自动化管道/代理链式调用** | **MCP** | 结构化的JSON输入/输出，类型安全的参数，无需shell解析 |

### 调用优先级

- **MCP原生工具**（Claude Code、Cursor）：优先使用MCP，CLI作为备用
- **本地模型/对令牌敏感的工具**：优先使用CLI（不需要MCP）
- **其他所有工具**：优先使用CLI

> **提示**：对于对令牌敏感的场景，请使用CLI模式——AI会读取SKILL.md文件（约2K令牌），并通过Bash执行命令。MCP模式会在每次对话中加载所有31个工具的配置（约10K令牌）。

### CLI示例

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

### MCP模式（可选）

对于偏好结构化工具调用的Claude Code/Cursor用户，请在`~/.claude/settings.json`中添加以下配置：

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

MCP提供了6个类别下的31个工具。所有工具都支持可选的`target`参数。

| 类别 | 工具 |
|----------|-------|
| 资源清单 | `list_virtual_machines`, `list_esxi_hosts`, `list_all_datastores`, `list_all_clusters` |
| 健康检查 | `get_alarms`, `get_events`, `vm_info` |
| 虚拟机生命周期 | `vm_power_on`, `vm_power_off`, `vm_set_ttl`, `vm_cancel_ttl`, `vm_list_ttl`, `vm_clean_slate` |
| 部署 | `deploy_vm_from_ova`, `deploy_vm_from_template`, `deploy_linked_clone`, `attach_iso_to_vm`, `convert_vm_to_template`, `batch_clone_vms`, `batch_linked_clone_vms`, `batch_deploy_from_spec` |
| 客户端操作 | `vm_guest_exec`, `vm_guest_upload`, `vm_guest_download` |
| 计划 → 应用 | `vm_create_plan`, `vm_apply_plan`, `vm_rollback_plan`, `vm_list_plans` |
| 数据存储 | `browse_datastore`, `scan_datastore_images`, `list_cached_images` |

当资源清单中的虚拟机数量超过50台时，`list_virtual_machines`会自动压缩（仅返回必要字段）。可以使用`limit`或`fields`参数进行自定义。

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

### 1. 资源清单

| 功能 | vCenter | ESXi | 详情 |
|---------|:-------:|:----:|---------|
| 列出虚拟机 | ✅ | ✅ | 名称、电源状态、CPU、内存、客户机操作系统、IP地址 |
| 列出主机 | ✅ | ⚠️ 仅适用于vCenter | CPU核心数、内存、ESXi版本、虚拟机数量、运行时间 |
| 列出数据存储 | ✅ | ✅ | 容量、可用/已用空间、类型（VMFS/NFS）、使用率 |
| 列出集群 | ✅ | ❌ | 主机数量、DRS/HA状态 |
| 列出网络 | ✅ | ✅ | 网络名称、关联的虚拟机数量 |

### 2. 健康与监控

| 功能 | vCenter | ESXi | 详情 |
|---------|:-------:|:----:|---------|
| 活动警报 | ✅ | ✅ | 警报级别、警报名称、相关实体、时间戳 |
| 事件/日志查询 | ✅ | ✅ | 可按时间范围和警报级别过滤；支持50多种事件类型 |
| 硬件传感器 | ✅ | ✅ | 温度、电压、风扇状态 |
| 主机服务 | ✅ | ✅ | hostd、vpxa的运行/停止状态 |

**监控的事件类型：**

| 类别 | 事件 |
|----------|--------|
| 虚拟机故障 | `VmFailedToPowerOnEvent`, `VmDiskFailedEvent`, `VmFailoverFailed` |
| 主机问题 | `HostConnectionLostEvent`, `HostShutdownEvent`, `HostIpChangedEvent` |
| 存储 | `DatastoreCapacityIncreasedEvent`, SCSI高延迟 |
| HA/DRS | `DasHostFailedEvent`, `DrsVmMigratedEvent`, `DrsSoftRuleViolationEvent` |
| 认证 | `UserLoginSessionEvent`, `BadUsernameSessionEvent` |

### 3. 虚拟机生命周期

| 操作 | 命令 | 需要确认 | vCenter | ESXi |
|-----------|---------|:------------:|:-------:|:----:|
| 开机 | `vm power-on <名称>` | — | ✅ | ✅ |
| 优雅关机 | `vm power-off <名称>` | ✅ | ✅ |
| 强制关机 | `vm power-off <名称> --force` | ✅ | ✅ |
| 重置 | `vm reset <名称>` | — | ✅ | ✅ |
| 暂停 | `vm suspend <名称>` | — | ✅ | ✅ |
| 虚拟机信息 | `vm info <名称>` | — | ✅ | ✅ |
| 创建虚拟机 | `vm create <名称> --cpu --memory --disk` | — | ✅ | ✅ |
| 删除虚拟机 | `vm delete <名称>` | ✅ | ✅ |
| 重新配置 | `vm reconfigure <名称> --cpu --memory` | ✅ | ✅ |
| 创建快照 | `vm snapshot-create <名称> --name <快照>` | — | ✅ | ✅ |
| 列出快照 | `vm snapshot-list <名称>` | — | ✅ | ✅ |
| 恢复快照 | `vm snapshot-revert <名称> --name <快照>` | — | ✅ | ✅ |
| 删除快照 | `vm snapshot-delete <名称> --name <快照>` | — | ✅ | ✅ |
| 克隆虚拟机 | `vm clone <名称> --new-name <新名称>` | — | ✅ | ✅ |
| vMotion | `vm migrate <名称> --to-host <主机>` | — | ✅ | ❌ |
| 设置TTL | `vm set-ttl <名称> --minutes <n>` | — | ✅ | ✅ |
| 取消TTL | `vm cancel-ttl <名称>` | — | ✅ | ✅ |
| 列出TTL | `vm list-ttl` | — | ✅ | ✅ |
| 清除虚拟机配置 | `vm clean-slate <名称> [--snapshot baseline]` | ✅ | ✅ |

### 计划 → 应用（多步骤操作）

对于涉及多个步骤或多个虚拟机的复杂操作，请使用计划/应用工作流程：

| 步骤 | MCP工具/CLI | 描述 |
|------|---------------|-------------|
| 1. 创建计划 | `vm_create_plan` | 验证操作，检查vSphere中的目标对象，生成包含回滚信息的计划 |
| 2. 审查 | — | AI向用户展示计划：步骤、受影响的虚拟机、不可逆操作 |
| 3. 应用 | `vm_apply_plan` | 顺序执行操作；失败时停止 |
| 4. 回滚（如果失败） | `vm_rollback_plan` | 请求用户确认，然后撤销已执行的操作（跳过不可逆操作） |

计划存储在`~/.vmware-aiops/plans/`目录下，成功执行后会被删除，24小时后自动清理。

### 4. 虚拟机部署与配置

| 操作 | 命令 | 执行速度 | vCenter | ESXi |
|-----------|---------|:-----:|:-------:|:----:|
| 从OVA文件部署 | `deploy ova <路径> --名称 <虚拟机>` | 分钟 | ✅ | ✅ |
| 从模板部署 | `deploy template <模板> --名称 <虚拟机>` | 分钟 | ✅ | ✅ |
| 链接克隆 | `deploy linked-clone --source <虚拟机> --snapshot <快照> --名称 <新名称>` | 秒钟 | ✅ | ✅ |
| 附加ISO镜像 | `deploy iso <虚拟机> --iso "[数据存储] 路径/to.iso"` | 即时 | ✅ | ✅ |
| 转换为模板 | `deploy mark-template <虚拟机>` | 即时 | ✅ | ✅ |
| 批量克隆 | `deploy batch-clone --source <虚拟机> --数量 <数量>` | 分钟 | ✅ | ✅ |
| 批量部署（YAML） | `deploy batch spec.yaml` | 自动 | ✅ | ✅ |

### 5. 数据存储浏览器

| 功能 | vCenter | ESXi | 详情 |
|---------|:-------:|:----:|---------|
| 浏览文件 | ✅ | ✅ | 列出任何数据存储路径下的文件/文件夹 |
| 扫描镜像 | ✅ | ✅ | 发现所有数据存储中的ISO、OVA、OVF、VMDK镜像 |
| 本地缓存 | ✅ | ✅ | 缓存信息存储在`~/.vmware-aiops/imageRegistry.json`文件中 |

### 6. vSAN管理

| 功能 | 详情 |
|---------|---------|
| 健康检查 | 集群范围内的健康状况总结，按组显示测试结果 |
| 容量 | 总容量/可用容量/已用容量及预测 |
| 磁盘组 | 每个主机的缓存SSD和容量磁盘 |
| 性能 | 每个集群/主机的IOPS、延迟、吞吐量 |

> 需要使用pyVmomi 8.0.3或更高版本（vSAN SDK已合并）。对于旧版本，请安装独立的vSAN管理SDK。

### 7. Aria Operations（VCF Operations）

| 功能 | 详情 |
|---------|---------|
| 历史指标 | 多个月的CPU、内存、磁盘、网络指标 |
| 异常检测 | 基于机器学习的动态基准线和异常警报 |
| 容量规划 | 假设分析、耗尽时间预测 |
| 容量调整 | 为每个虚拟机提供CPU/内存建议 |
| 智能警报 | 根本原因分析、修复建议 |

> REST API位于 `/suite-api/`。认证方式：`vRealizeOpsToken`。在VCF 9.0中重新命名为VCF Operations。

### 8. vSphere Kubernetes Service（VKS）

| 功能 | 详情 |
|---------|---------|
| 列出集群 | 显示Tanzu Kubernetes集群及其阶段状态 |
| 集群健康 | 显示InfrastructureReady、ControlPlaneAvailable、WorkersAvailable状态 |
| 调整工作节点数量 | 调整MachineDeployment副本数量 |
| 节点状态 | 显示节点状态、健康状况 |

> 通过kubectl/kubeconfig使用Kubernetes原生API。VKS 3.6及以上版本支持此功能。

### 9. 定时扫描与通知

| 功能 | 详情 |
|---------|---------|
| 定时任务 | 基于APScheduler，可配置扫描间隔（默认为15分钟） |
| 多目标扫描 | 顺序扫描所有配置的vCenter/ESXi目标 |
| 扫描内容 | 包括警报、事件和主机日志（hostd、vmkernel、vpxd） |
| 日志分析 | 支持正则表达式匹配：错误、失败、严重、恐慌、超时 |
| Webhook | 支持Slack、Discord或任何HTTP端点 |

## 安全特性

| 功能 | 详情 |
|---------|---------|
| 计划 → 确认 → 执行 → 记录日志 | 结构化的工作流程：显示当前状态、确认更改、执行操作、记录审计日志 |
| 双重确认 | 所有破坏性操作（关机、删除、重新配置、快照恢复/删除、克隆、迁移）都需要两次确认——不允许跳过确认步骤 |
| 拒绝记录 | 被拒绝的确认操作会记录在审计日志中以供安全审查 |
| 审计日志 | 所有操作都会记录在`~/.vmware-aiops/audit.log`（JSONL格式）文件中，包含操作前后的状态 |
| 输入验证 | 在执行前验证虚拟机名称的长度和格式、CPU（1-128位）、内存（128-1048576 MB）、磁盘（1-65536 GB） |
| 密码保护 | 从`.env`文件加载配置信息，不会显示在命令行或shell历史记录中；启动时检查文件权限 |
| SSL自签名证书支持 | `disableSslCertValidation`选项仅适用于使用自签名证书的ESXi主机（通常用于隔离实验室/家庭环境）。生产环境应使用具有完整TLS验证的CA签名证书 |
| 任务等待 | 所有异步操作都会等待完成并报告结果 |
| 状态验证 | 操作前会检查虚拟机是否存在以及其电源状态是否正确 |

## 版本兼容性

| vSphere版本 | 支持情况 | 备注 |
|----------------|---------|-------|
| 8.0 / 8.0U1-U3 | 完全支持 | `CreateSnapshot_Task`已被弃用，建议使用`CreateSnapshotEx_Task` |
| 7.0 / 7.0U1-U3 | 完全支持 | 所有API均可用 |
| 6.7 | 兼容 | 经过测试 |
| 6.5 | 兼容 | 经过测试 |

> pyVmomi会在SOAP握手过程中自动协商API版本——无需手动配置。

## 支持的AI平台

| 平台 | 支持情况 | 配置文件 |
|----------|--------|-------------|
| Claude Code | ✅ | 作为原生技能集成在`plugins/.../SKILL.md`中 |
| Gemini CLI | ✅ | 作为扩展集成在`gemini-extension/GEMINI.md`中 |
| OpenAI Codex CLI | ✅ | 作为技能集成在`codex-skill/AGENTS.md`中 |
| Aider | ✅ | 作为规则集成在`codex-skill/AGENTS.md`中 |
| Continue CLI | ✅ | 作为规则集成在`codex-skill/AGENTS.md`中 |
| Trae IDE | ✅ | 作为规则集成在`trae-rules/project_rules.md`中 |
| Kimi Code CLI | ✅ | 作为技能集成在`kimi-skill/SKILL.md`中 |
| MCP Server | ✅ | 通过标准IO协议与MCP服务器配合使用 |
| Python CLI | ✅ | 作为独立工具使用 |

### MCP服务器与本地代理的兼容性

MCP服务器可以通过标准IO与任何兼容的代理配合使用。配置模板位于`examples/mcp-configs/`目录下：

| 代理 | 支持的本地模型 | 配置文件 |
|-------|:----------:|-----------------|
| Goose (Block) | ✅ | Ollama、LM Studio | `goose.json` |
| LocalCowork (Liquid AI) | ✅ | 全离线模式 | `localcowork.json` |
| mcp-agent (LastMile AI) | ✅ | Ollama、vLLM | `mcp-agent.yaml` |
| VS Code Copilot | ✅ | `vscode-copilot.json` |
| Cursor | ✅ | `cursor.json` |
| Continue | ✅ | Ollama | `continue.yaml` |
| Claude Code | ✅ | `claude-code.json` |

```bash
# Example: Aider + Ollama (fully local, no cloud API)
aider --conventions codex-skill/AGENTS.md --model ollama/qwen2.5-coder:32b
```

## CLI参考

```bash
# Diagnostics
vmware-aiops doctor [--skip-auth]

# MCP Config Generator
vmware-aiops mcp-config generate --agent <goose|cursor|claude-code|continue|vscode-copilot|localcowork|mcp-agent>
vmware-aiops mcp-config list

# Inventory
vmware-aiops inventory vms [--target <name>] [--limit <n>] [--sort-by name|cpu|memory_mb|power_state] [--power-state poweredOn|poweredOff]
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
vmware-aiops vm set-ttl <vm-name> --minutes <n>
vmware-aiops vm cancel-ttl <vm-name>
vmware-aiops vm list-ttl
vmware-aiops vm clean-slate <vm-name> [--snapshot baseline]

# Guest Operations (requires VMware Tools)
vmware-aiops vm guest-exec <vm-name> --cmd /bin/bash --args "-c 'ls -la /tmp'" --user root
vmware-aiops vm guest-upload <vm-name> --local ./script.sh --guest /tmp/script.sh --user root
vmware-aiops vm guest-download <vm-name> --guest /var/log/syslog --local ./syslog.txt --user root

# Plan → Apply (multi-step operations)
vmware-aiops plan list

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

### 开发安装

```bash
git clone https://github.com/zw008/VMware-AIops.git
cd VMware-AIops
uv venv && source .venv/bin/activate
uv pip install -e .
```

## 安全性

- **源代码**：该工具完全开源，可在[github.com/zw008/VMware-AIops](https://github.com/zw008/VMware-AIops)获取。建议在部署到生产环境之前查看源代码和提交历史记录。
- **TLS验证**：默认启用。`disableSslCertValidation`选项仅适用于使用自签名证书的ESXi主机（常见于家庭实验室环境）。在生产环境中，务必使用具有完整TLS验证的CA签名证书。
- **配置文件内容**：`~/.vmware-aiops/config.yaml`文件存储目标主机名、端口以及`.env`文件的引用。该文件不包含密码或令牌。所有敏感信息（vCenter用户名/密码）都存储在`~/.vmware-aiops/.env`文件中（权限设置为`chmod 600`），并通过`python-dotenv`加载。建议使用权限最低的vCenter服务账户——如果仅需要监控功能，可以选择仅读权限的[VMware-Monitor](https://github.com/zw008/VMware-Monitor)工具。
- **Webhook数据范围**：Webhook通知默认是禁用的。启用后，它们只会将基础设施健康状况摘要（警报数量、事件类型、主机状态）发送到用户配置的URL（Slack、Discord或任何HTTP端点）。不会向第三方服务发送任何数据。Webhook消息中不包含凭据、IP地址或个人身份信息，仅包含聚合的警报元数据。
- **防止命令注入**：所有来自vCenter的内容（事件消息、主机日志）在输出前都会被截断、去除控制字符，并用边界标记`[VSPHERE_EVENT]`/`[VSPHERE_HOST_LOG`包裹，以防止被LLM代理误解读。
- **最小权限原则**：建议使用权限最低的vCenter服务账户。如果仅需要监控功能，推荐使用仅读权限的[VMware-Monitor](https://github.com/zw008/VMware-Monitor)工具，因为该工具的代码中没有任何破坏性操作。

## 许可证

MIT许可证