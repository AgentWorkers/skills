---
name: agent-ros-bridge
version: 0.3.2
description: 一个通用的 ROS1/ROS2 桥梁，用于 AI 代理控制机器人和具身智能系统。
author: Agent ROS Bridge Team
homepage: https://github.com/webthree549-bot/agent-ros-bridge
repository: https://github.com/webthree549-bot/agent-ros-bridge.git
license: MIT
metadata:
  {
    "openclaw":
      {
        "emoji": "🤖",
        "requires": { "bins": ["python3"], "env": ["JWT_SECRET"] },
        "suggests": { "bins": ["docker"] },
        "env":
          {
            "JWT_SECRET":
              {
                "description": "Required: Secret key for JWT authentication. Bridge will fail to start without this.",
                "sensitive": true,
                "required": true,
              },
            "BRIDGE_HOST":
              {
                "description": "Optional: Bind address (default: 127.0.0.1 for security)",
                "sensitive": false,
                "required": false,
              },
          },
        "security":
          {
            "notes": "SECURITY-FIRST DESIGN: JWT authentication is always required and cannot be disabled. All examples run in Docker containers for isolation. Never expose to public networks without TLS and firewall rules.",
          },
        "install":
          [
            {
              "id": "python3",
              "kind": "manual",
              "label": "Python 3.8+",
              "instruction": "Install Python 3.8 or higher from https://python.org",
            },
            {
              "id": "docker",
              "kind": "manual",
              "label": "Docker Desktop (optional but recommended)",
              "instruction": "For running examples in isolated containers. Install from https://www.docker.com/products/docker-desktop",
            },
          ],
        "category": "robotics",
        "tags": ["ros", "ros2", "robotics", "iot", "automation", "bridge", "embodied-intelligence", "arm", "navigation"],
      },
  }

---

# 🤖 Agent ROS Bridge

**一个通用的 ROS1/ROS2 桥接器，用于 AI 代理控制机器人和具身智能系统。**

[![持续集成](https://github.com/webthree549-bot/agent-ros-bridge/actions/workflows/ci.yml/badge.svg)](https://github.com/webthree549-bot/agent-ros-bridge/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/agent-ros-bridge.svg)](https://pypi.org/project/agent-ros-bridge/)
[![许可证](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

---

## 🔐 安全优先的设计

**必须始终使用 JWT 进行身份验证，且无法禁用。**

**注意：** 如果没有 `JWT_SECRET`，该桥接器将无法启动。这是设计上的要求——安全是不可妥协的。

有关完整的安全指南，请参阅 [SECURITY.md](SECURITY.md)。

---

## 快速入门

### 选项 1：Docker 示例（推荐用于测试）

所有示例都在隔离的 Docker 容器中运行，其中包含模拟的机器人（无需安装 ROS）。

---

### 可用的示例

| 示例 | 描述 | 运行方式 |
|---------|-------------|-----|
| `examples/quickstart/` | 带有模拟机器人的基本桥接器 | `docker-compose up` |
| `examples/fleet/` | 多机器人舰队协调 | `docker-compose up` |
| `examples/arm/` | 机器人手臂控制模拟 | `docker-compose up` |

所有示例：
- 在隔离的 Docker 容器中运行
- 强制使用 JWT 进行身份验证
- 包含模拟机器人（无需硬件）
- 默认绑定到本地主机（127.0.0.1）

### 选项 2：原生安装（生产环境）

**要求：** 安装了 Ubuntu 20.04/22.04，并且已安装 ROS1 Noetic 或 ROS2 Humble/Jazzy。

**有关详细的原生安装说明，请参阅 [docs/NATIVE_ROS.md](docs/NATIVE_ROS.md)。**

---

## 特性

| 特性 | 描述 |
|---------|-------------|
| **🔐 安全性** | 必须使用 JWT 进行身份验证，无法绕过 |
| **🤖 多机器人** | 舰队编排与协调 |
| **🌐 多协议** | 支持 WebSocket、MQTT、gRPC |
| **🔄 多 ROS** | 同时支持 ROS1 和 ROS2 |
| **🦾 手臂控制** | 支持 UR、xArm、Franka 机器人 |
| **📊 监控** | 使用 Prometheus 和 Grafana 进行监控 |

---

## 文档

| 文档 | 描述 |
|----------|-------------|
| [用户手册](docs/USER_MANUAL.md) | 完整指南（23,000 多字） |
| [API 参考](docs/API_REFERENCE.md) | 完整的 API 文档 |
| [原生 ROS 安装](docs/NATIVE_ROS.md) | Ubuntu/ROS 安装指南 |
| [Docker 与原生安装的比较](docs/DOCKER_VS_NATIVE.md) | 部署方式对比 |
| [安全性政策](SECURITY.md) | 安全政策 |

---

## 使用方法

### Python API

---

### 命令行接口 (CLI)

---

## 链接

- **文档：** https://github.com/webthree549-bot/agent-ros-bridge/tree/main/docs
- **PyPI：** https://pypi.org/project/agent-ros-bridge/
- **GitHub：** https://github.com/webthree549-bot/agent-ros-bridge
- **问题报告：** https://github.com/webthree549-bot/agent-ros-bridge/issues

---

**安全至关重要。必须始终使用 JWT 进行身份验证。**