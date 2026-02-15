---
name: hydra-evolver
version: 1.0.0
description: "这是一种基于 Proxmox 的原生编排技术，能够将任何家庭实验室转变为具备自我修复功能的 AI 集群（即能够自动修复故障并持续运行的 AI 系统）。"
author: bradfromtherealworld
metadata:
  requires:
    bins: ["python3", "docker", "pm2"]
  env: ["PVE_TOKEN_ID", "PVE_TOKEN_SECRET"]
---

# 🐉 Hydra Mesh Evolver

**让您的基础设施更具战斗力。实现系统的去中心化管理。**

Hydra Mesh Evolver 是专为 OpenClaw Mesh 设计的一项专业工具，它允许代理自主管理、监控并优化分布式的工作节点集群。

## 主要功能
- **节点部署：** 自动将 OpenClaw 代理部署到 Windows、Mac 和 Linux 系统的节点上。
- **Proxmox 监控功能：** 实时监控硬件状态和虚拟机运行情况。
- **自我进化机制：** 扫描项目文件（`PROJECTS.md`），针对停滞的工作任务提出代码修复方案或恢复计划。
- **安全防护机制：** 内置防护机制，防止在网络研究中被恶意代码注入。

## 所含工具
### `mesh_scan`  
扫描网络中的新节点，并更新网格拓扑结构。

### `mesh_evolve`  
分析 `MEMORY.md` 和 `PROJECTS.md` 文件，识别潜在问题，并生成优化方案（`evolution_plan.json`）。

### `mesh_provision`  
一键完成新硬件的配置（支持 Docker、OpenClaw 和 Tailscale 等平台）。

---
*该工具专为 2026 年 Moltbook 上举办的 OpenClaw 霸客赛开发。*