---
name: proxmox
description: "管理 Proxmox VE 节点、虚拟机（VM）和容器。可以查看硬件统计信息、资源使用情况，并控制它们的电源状态（启动、停止、重启、关机）。"
metadata:
  requires:
    bins: ["python3"]
  env: ["PVE_HOST", "PVE_TOKEN_ID", "PVE_TOKEN_SECRET"]
---

# Proxmox 技能

该技能允许代理与 Proxmox VE 集群进行交互，以管理虚拟机和容器。

## 工具

### proxmox_list
列出 Proxmox 节点或整个集群中所有可用的虚拟机和容器。
- 命令：python3 {{skillDir}}/scripts/proxmox.py {{type}}
- 参数：
  - type: "nodes" 或 "vms"

### proxmox_node_health
获取特定物理节点的硬件级健康状况信息（CPU 使用率、内存、运行时间、版本）。
- 命令：python3 {{skillDir}}/scripts/proxmox.py node_health {{node}}
- 参数：
  - node: Proxmox 主机的名称（例如 "pve" 或 "hydra")

### proxmox_status
获取特定虚拟机或容器的实时状态。
- 命令：python3 {{skillDir}}/scripts/proxmox.py status {{node}} {{kind}} {{vmid}}
- 参数：
  - node: 资源所在的 Proxmox 节点名称
  - kind: "qemu"（用于虚拟机）,"lxc"（用于容器）
  - vmid: 资源的数字 ID（例如 "100")

### proxmox_power_action
执行电源管理操作。这些操作默认需要人工批准。
- 批准方式：true
- 命令：python3 {{skillDir}}/scripts/proxmox.py {{action}} {{node}} {{kind}} {{vmid}}
- 参数：
  - action: "start"（启动）、"stop"（停止）、"reboot"（重启）或 "shutdown"（关机）
  - node: Proxmox 节点名称
  - kind: "qemu" 或 "lxc"
  - vmid: 资源的 ID