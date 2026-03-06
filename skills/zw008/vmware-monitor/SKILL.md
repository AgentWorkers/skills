---
name: vmware-monitor
description: VMware vCenter/ESXi 的只读监控功能。该代码库严格执行安全措施，确保不存在任何可能造成系统损坏的操作。支持查询虚拟机资源清单、检查虚拟机的运行状态/警报/事件记录、查看虚拟机信息及快照，以及扫描日志文件。
installer:
  kind: uv
  package: vmware-monitor
---
# VMware Monitor（仅限读取）

这是一个安全的、仅限读取的 VMware vCenter 和 ESXi 监控工具。您可以通过任何 AI 编码助手使用自然语言查询整个 VMware 基础设施，而无需担心意外修改的风险。

> **代码级安全性**：这是一个独立的仓库（`zw008/VMware-Monitor`）。代码库中不存在任何具有破坏性的操作——没有关闭电源、删除、创建、重新配置、创建/恢复/删除快照、克隆或迁移的功能。如需进行完整操作，请使用单独的 [VMware-AIops](https://github.com/zw008/VMware-AIops) 仓库。安装方法：`clawhub install vmware-aiops`。

## 适用场景

- 查询虚拟机（VM）、主机、数据存储（datastore）、集群（cluster）和网络（network）的库存信息
- 检查健康状态、活动警报、硬件传感器和事件日志
- 查看虚拟机详细信息及现有的快照列表（仅限读取）
- 运行定时日志扫描，并通过 webhook 通知结果（Slack、Discord）

> **您需要零风险的监控**——绝对不会出现意外关闭电源、删除或重新配置的情况。

## 快速安装

该工具支持 Claude Code、Cursor、Codex、Gemini CLI、Trae、Kimi 等 30 多种 AI 工具：

```bash
# Via Skills.sh
npx skills add zw008/VMware-Monitor

# Via ClawHub
clawhub install vmware-monitor
```

### Claude Code

```
/plugin marketplace add zw008/VMware-Monitor
/plugin install vmware-monitor
/vmware-monitor:vmware-monitor
```

## 使用方式

根据您的 AI 工具选择最佳使用模式：

| 平台 | 推荐模式 | 原因 |
|----------|-----------------|-----|
| Claude Code、Cursor | **MCP** | 结构化的工具调用，无需交互式确认，使用体验流畅 |
| Aider、Codex、Gemini CLI、Continue | **CLI** | 体积轻量，上下文开销低，兼容性高 |
| Ollama + 本地模型 | **CLI** | 对模型大小要求低，适用性广 |

### 调用优先级

- **MCP原生工具**（Claude Code、Cursor）：优先使用 MCP，CLI 作为备用方案
- **其他所有工具**：优先使用 CLI（无需使用 MCP）

> **提示**：如果您的 AI 工具支持 MCP，请检查 `vmware-monitor` MCP 服务器是否已加载（在 Claude Code 中通过 `/mcp` 查看）。如果没有，请先进行配置——MCP 可提供最佳的无干扰使用体验。

### CLI 示例

```bash
# Activate venv first
source /path/to/VMware-Monitor/.venv/bin/activate

# Inventory
vmware-monitor inventory vms --target home-esxi
vmware-monitor inventory hosts --target home-esxi

# Health
vmware-monitor health alarms --target home-esxi
vmware-monitor health events --hours 24 --severity warning --target home-esxi

# VM info (read-only)
vmware-monitor vm info my-vm --target home-esxi
```

### MCP 模式（可选）

对于偏好结构化工具调用的 Claude Code/Cursor 用户，请在 `~/.claude/settings.json` 中添加以下配置：

```json
{
  "mcpServers": {
    "vmware-monitor": {
      "command": "/path/to/VMware-Monitor/.venv/bin/python",
      "args": ["-m", "mcp_server"],
      "cwd": "/path/to/VMware-Monitor",
      "env": {
        "VMWARE_MONITOR_CONFIG": "~/.vmware-monitor/config.yaml"
      }
    }
  }
}
```

MCP 提供了 7 个仅限读取的工具：`list_virtual_machines`、`list_esxi_hosts`、`list_all_datastores`、`list_all_clusters`、`get_alarms`、`get_events`、`vm_info`。所有这些工具都支持可选的 `target` 参数。

## 架构

```
User (Natural Language)
  ↓
AI Tool (Claude Code / Aider / Gemini / Codex / Cursor / Trae / Kimi)
  ↓
  ├─ CLI mode (default): vmware-monitor CLI ──→ pyVmomi ──→ vSphere API
  │
  └─ MCP mode (optional): MCP Server (stdio) ──→ pyVmomi ──→ vSphere API
  ↓
vCenter Server ──→ ESXi Clusters ──→ VMs
    or
ESXi Standalone ──→ VMs
```

## 首次使用：环境选择

当用户开始对话时，**务必先询问**：

1. **他们希望监控哪个环境？**（vCenter 服务器还是独立的 ESXi 主机）
2. **从他们的配置中选择哪个目标？**（例如：`prod-vcenter`、`lab-esxi`）
3. 如果尚未配置，请指导他们创建 `~/.vmware-monitor/config.yaml` 文件。

## 功能（仅限读取）

### 1. 库存管理

| 功能 | vCenter | ESXi | 详情 |
|---------|:-------:|:----:|---------|
| 列出虚拟机 | ✅ | ✅ | 名称、电源状态、CPU、内存、客户机操作系统（guest OS）、IP 地址 |
| 列出主机 | ✅ | ⚠️ 仅适用于 ESXi | CPU 核心数量、内存、ESXi 版本、虚拟机数量、运行时间 |
| 列出数据存储 | ✅ | ✅ | 容量、可用/已用空间、类型（VMFS/NFS）、使用率 |
| 列出集群 | ✅ | ❌ | 主机数量、DRS/HA 状态 |
| 列出网络 | ✅ | ✅ | 网络名称、关联的虚拟机数量 |

### 2. 健康与监控

| 功能 | vCenter | ESXi | 详情 |
|---------|:-------:|:----:|---------|
| 活动警报 | ✅ | ✅ | 警报级别、警报名称、相关实体、时间戳 |
| 事件/日志查询 | ✅ | ✅ | 可按时间范围和警报级别过滤；支持 50 多种事件类型 |
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

### 3. 虚拟机信息及快照列表（仅限读取）

| 功能 | 详情 |
|---------|---------|
| 虚拟机信息 | 名称、电源状态、客户机操作系统、CPU、内存、IP 地址、VMware 工具、磁盘、网卡（NICs） |
| 快照列表 | 显示现有快照的名称和创建时间（不支持创建/恢复/删除操作） |

### 4. 定时扫描与通知

| 功能 | 详情 |
|---------|---------|
| 定时任务 | 基于 APScheduler，可配置扫描间隔（默认为 15 分钟） |
| 多目标扫描 | 顺序扫描所有配置的 vCenter/ESXi 目标 |
| 扫描内容 | 包括警报、事件和主机日志（hostd、vmkernel、vpxd） |
| 日志分析 | 支持正则表达式匹配：错误、失败、严重、紧急、超时等日志类型 |
| Webhook | 通知方式：Slack、Discord 或任何 HTTP 端点 |

## **禁止的操作（代码库中不存在）**

这些操作**无法**通过此工具执行——代码库中不存在任何具有破坏性的代码：

- ❌ 关闭/开启虚拟机电源（`vm power-on/off`）、`vm reset`、`vm suspend`
- ❌ 创建/删除/重新配置虚拟机（`vm create/delete/reconfigure`）
- ❌ 创建/恢复/删除虚拟机快照（`vm snapshot-create/revert/delete`）
- ❌ 克隆/迁移虚拟机（`vm clone/migrate`）

对于这些操作，请使用 **VMware-AIops**（`clawhub install vmware-aiops`）。

## 安全特性

| 功能 | 详情 |
|---------|---------|
| 代码级隔离 | 代码库为独立仓库，不存在任何具有破坏性的功能 |
| 审计追踪 | 所有查询都会被记录到 `~/.vmware-monitor/audit.log`（JSONL 格式） |
| 密码保护 | 通过 `.env` 文件加载配置文件，并进行权限检查（如果文件权限不是 600，则会发出警告） |
| SSL 自签名证书支持 | 可通过 `disableSslCertValidation` 选项禁用 SSL 证书验证——**仅**适用于使用自签名证书的 ESXi 主机（常见于实验室环境）。生产环境应使用经过 CA 签名的证书，并启用完整的 TLS 验证。 |

## 版本兼容性

| vSphere 版本 | 支持情况 | 备注 |
|----------------|---------|-------|
| 8.0 / 8.0U1-U3 | 完全支持 | 需 pyVmomi 8.0.3 或更高版本 |
| 7.0 / 7.0U1-U3 | 完全支持 | 所有仅限读取的 API 都被支持 |
| 6.7 | 兼容 | 经过测试，支持向后兼容 |
| 6.5 | 兼容 | 经过测试，支持向后兼容 |

> pyVmomi 会在 SOAP 握手过程中自动协商 API 版本——无需手动配置。

## 支持的 AI 平台

| 平台 | 支持情况 | 配置文件 |
|----------|--------|-------------|
| Claude Code | ✅ | 原生支持 | `plugins/.../SKILL.md` |
| Gemini CLI | ✅ | 作为扩展支持 | `gemini-extension/GEMINI.md` |
| OpenAI Codex CLI | ✅ | 通过 `codex-skill/AGENTS.md` 支持 |
| Aider | ✅ | 通过 `codex-skill/AGENTS.md` 支持 |
| Continue CLI | ✅ | 通过 `codex-skill/AGENTS.md` 支持 |
| Trae IDE | ✅ | 通过 `trae-rules/project_rules.md` 支持 |
| Kimi Code CLI | ✅ | 作为独立技能支持 | `kimi-skill/SKILL.md` |
| MCP Server | ✅ | 通过 `mcp_server/` 支持 |
| Python CLI | ✅ | 作为独立工具支持 | 不需要额外配置 |

## CLI 参考文档

```bash
# Inventory
vmware-monitor inventory vms [--target <name>]
vmware-monitor inventory hosts [--target <name>]
vmware-monitor inventory datastores [--target <name>]
vmware-monitor inventory clusters [--target <name>]

# Health
vmware-monitor health alarms [--target <name>]
vmware-monitor health events [--hours 24] [--severity warning]

# VM Info (read-only)
vmware-monitor vm info <vm-name>
vmware-monitor vm snapshot-list <vm-name>

# Scanning & Daemon
vmware-monitor scan now [--target <name>]
vmware-monitor daemon start
vmware-monitor daemon stop
vmware-monitor daemon status
```

## 设置

```bash
# 1. Install via uv (recommended) or pip
uv tool install vmware-monitor
# Or: pip install vmware-monitor

# 2. Configure
mkdir -p ~/.vmware-monitor
vmware-monitor init  # generates config.yaml and .env templates
chmod 600 ~/.vmware-monitor/.env
# Edit ~/.vmware-monitor/config.yaml and .env with your target details
```

### 开发环境安装

```bash
git clone https://github.com/zw008/VMware-Monitor.git
cd VMware-Monitor
uv venv && source .venv/bin/activate
uv pip install -e .
```

## 安全性

- **设计初衷：仅限读取**：这是一个独立的仓库，代码库中不存在任何具有破坏性的操作。
- **TLS 验证**：默认启用。`disableSslCertValidation` 选项仅适用于使用自签名证书的 ESXi 主机（常见于实验室环境）。在生产环境中，必须使用经过 CA 签名的证书，并启用完整的 TLS 验证。
- **凭证管理**：凭证仅通过 `.env` 文件从环境变量中加载（权限设置为 600）。切勿通过 CLI 参数、配置文件或 MCP 消息传递凭证。
- **Webhook 数据范围**：Webhook 通知仅发送到用户配置的 URL（Slack、Discord 或您控制的任何 HTTP 端点）。默认情况下，不会向第三方服务发送任何数据。
- **防止注入攻击**：所有来自 vSphere 的内容（事件消息、主机日志）在输出前都会被截断、去除控制字符，并用边界标记包裹。
- **代码审查**：建议在部署到生产环境之前审查源代码和提交历史记录。建议在隔离环境中进行初步测试。

## 许可证

MIT 许可证