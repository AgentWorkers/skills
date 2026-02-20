---
name: server-health-agent
description: 监控虚拟私有服务器（VPS）和服务器的健康指标，包括实时CPU使用率、内存利用率、磁盘使用情况以及Docker容器的状态。这些信息对于DevOps监控、排查性能问题以及进行基础设施健康检查非常有用。
runtime: node
entry: skill.js
permissions:
  - shell
---
# 服务器健康检查代理

服务器健康检查代理（Server Health Agent）是一款专为生产环境设计的 OpenClaw 技能，用于实时监控服务器的关键健康指标。它帮助开发人员、DevOps 工程师和系统管理员快速评估其虚拟专用服务器（VPS）或服务器的运行状况。

该技能执行安全的系统级只读命令来收集准确的健康指标，而不会修改系统配置。

---

# 主要功能

## 实时 CPU 监控
使用实时系统命令（`top`）来获取当前的 CPU 使用率，并提供备用机制以确保在受限环境中也能可靠地获取数据。

## 内存（RAM）监控
通过系统级命令和 Node.js 备用逻辑来报告准确的 RAM 使用百分比。

## 磁盘使用情况监控
提供根文件系统的磁盘使用情况，以便检测存储压力或容量问题。

## Docker 容器检测
当可以访问 Docker 套接字时，检测并报告正在运行的 Docker 容器及其状态；在无法访问 Docker 的环境中也能正常工作。

## 结构化输出
返回结构化的 JSON 输出，适用于 OpenClaw 自动化工作流程和后续处理。

---

# 使用场景

该技能适用于以下场景：

- VPS 健康监控
- DevOps 自动化工作流程
- 基础设施监控
- 故障排除（性能问题）
- 检测资源瓶颈
- 监控容器化环境
- 自动化的系统健康检查

---

# 示例输出

```json
{
  "success": true,
  "skill": "server-health-agent",
  "timestamp": "2026-02-20T12:00:00Z",
  "server_health": {
    "cpu_percent": "12.44",
    "ram_percent": "21.33",
    "disk_usage": "51%",
    "docker_status": "openclaw-openclaw-gateway-1: 运行中（已启动 2 小时）"
  }
}
```