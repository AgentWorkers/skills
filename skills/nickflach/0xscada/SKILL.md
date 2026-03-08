---
name: 0xscada
description: **去中心化工业控制架构**：该架构将SCADA系统与基于区块链的审计追踪功能以及Kannaka内存技术相结合，提供了统一的API，用于实现遥测数据传输、几何形状分类以及工业状态的验证。
metadata:
  openclaw:
    requires:
      bins:
        - name: node
          label: "Node.js 18+  required to run the server"
        - name: npm
          label: "npm  required for installation"
      env: []
    optional:
      bins:
        - name: docker
          label: "Docker  optional for local database/redis"
      env:
        - name: SCADA_PORT
          label: "HTTP port for the 0xSCADA server (default: 5000)"
        - name: DATABASE_URL
          label: "PostgreSQL connection string"
    data_destinations:
      - id: scada-local
        description: "Local industrial telemetry"
        remote: false
    install:
      - id: npm-install
        kind: command
        label: "Install dependencies"
        command: "npm install"
---
# 0xSCADA 技能

该技能用于将分散式工业控制架构中的元素（atoms）映射为具体的比特（bits），并能够与 Kannaka 内存生态系统（基于 84 类 SGA Fano 几何结构的系统）进行原生集成。

## 先决条件

- 确保 Node.js 18 及更高版本已安装在系统的 PATH 环境变量中。
- npm（Node.js 的包管理工具）也必须安装在 PATH 环境变量中。
- PostgreSQL 数据库（可选；如果未配置，则默认使用 SQLite 数据库）。

## 设置

```bash
cd ~/workspace/skills/0xscada
npm install
```

## 快速入门

```bash
# Start 0xSCADA
./scripts/0xscada.sh start

# Check status
./scripts/0xscada.sh status
```