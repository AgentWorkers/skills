---
name: minecraft-bridge
description: 本地HTTP桥接器，用于基于Mineflayer的Minecraft Java机器人的实时控制。当用户需要将机器人连接到自己的游戏世界、查看机器人的状态/库存/位置，或让机器人移动、采矿、制作物品、跟随玩家或在游戏中聊天时，可使用该工具。示例命令包括：“连接到我的游戏世界”、“启动Minecraft机器人”、“我的库存里有什么？”、“去采矿铁矿”、“制作一把镐”、“跟随我”、“Minecraft桥接器是否正在运行”。此外，当其他与Minecraft相关的操作需要实时游戏数据时，也可以使用该工具。但请注意：该工具不适用于与Minecraft相关的基础知识查询（请使用minecraft-wiki）、通过RCON或server.properties进行服务器管理，以及无关紧要的Minecraft讨论（请使用minecraft-server-admin）。
metadata:
  openclaw:
    emoji: "🎮"
    requires:
      bins:
        - node
      env:
        - MC_HOST
        - MC_PORT
        - MC_BOT_USERNAME
    install:
      - id: mineflayer
        kind: node
        package: mineflayer
        label: "Mineflayer — Minecraft bot API"
      - id: mineflayer-pathfinder
        kind: node
        package: mineflayer-pathfinder
        label: "Pathfinder — navigation plugin"
      - id: vec3
        kind: node
        package: vec3
        label: "Vec3 — 3D coordinate helper"
    homepage: https://github.com/en1r0py1865/minecraft-skill
---
# Minecraft Bridge

这是一个持久的本地HTTP服务，用于将OpenClaw与正在运行的Minecraft Java Edition机器人会话连接起来。该服务在`http://localhost:${MC_BRIDGE_PORT|3001}`上提供REST API，用于读取实时游戏状态和执行机器人操作。

**使用范围**：
- 用于实时机器人控制及实时游戏状态查询。
- 有关知识问题，请使用`minecraft-wiki`。
- 服务器管理（如RCON、修改`server.properties`文件、添加/移除玩家、执行服务器操作等）请使用`minecraft-server-admin`。

## 快速操作流程

- 使用`GET http://localhost:3001/status`命令查看当前状态。

---

## 首次使用前的设置

### 1. 环境变量配置
在`~/.openclaw/openclaw.json`中设置环境变量，或通过shell命令导出这些变量：

---

### 2. 启动Minecraft的局域网模式（单人模式）
- 按`ESC`键 → 选择“Open to LAN” → 启用作弊模式 → 启动局域网游戏世界。
- 注意显示的端口号（例如54321），并将其设置为`MC_PORT`环境变量的值。

### 3. 启动Minecraft Bridge服务
等待提示：“🎮 Bridge ready at http://localhost:3001”。

### 4. 验证服务是否正常运行

---

## 运行时操作

当用户发送游戏命令时：
1. **检查服务状态**：通过`GET /status`命令查询；如果服务不可用，请查看上述设置指南。
2. **执行命令**：调用相应的API端点（详见下方API参考文档）。
3. **返回结果**：以易于理解的方式格式化响应内容，包括坐标、物品名称及数量等信息。
4. **保存操作记录**：将重要操作信息保存到OpenClaw的内存中（例如获取的坐标、收集的物品、达成的目标等）。

### 解析 `/status` 响应
- `gameTime` 的取值范围为0–6000表示清晨，6000–12000表示白天，12000–18000表示黄昏/夜晚。
- `health` 的最大值为20.0；低于6表示服务处于危险状态。
- `food` 的最大值为20；低于6表示机器人无法冲刺，低于1表示正在受到伤害。

---

## API概述
完整的API规范请参见`references/api-spec.md`。

**核心API端点**：
- `GET /status`：查询桥接服务及机器人的连接状态。
- `GET /inventory`、`GET /position`、`GET /nearby`：读取实时游戏状态。
- `POST /move`、`POST /mine`、`POST /collect`、`POST /craft`、`POST /follow`、`POST /stop`：执行机器人操作。
- `POST /chat`：向游戏中发送聊天消息。
- `POST /command`：发送任意斜杠命令（请谨慎使用）。
> **安全提示**：`/command`接口会转发任意斜杠命令。在机器人具有高级权限的服务器上，这些命令可能具有破坏性或管理员级别的功能。建议使用`minecraft-server-admin`进行服务器管理。

---

## 依赖技能
在使用Minecraft Bridge之前，需要确保相关技能已正确配置并能够检查桥接服务的状态。请参阅`references/dependency-guide.md`以了解正确的依赖检查方法及故障处理方式。

---

## 错误处理
| 错误类型 | 原因 | 处理方法 |
|-------|-------|---------|
| `ECONNREFUSED` | 服务未启动 | 运行`node bridge-server.js`脚本。 |
| `{"connected":false}` | 服务已启动但机器人离线 | 重新启动Minecraft并检查`MC_HOST`及`PORT`配置。 |
| `{"error":"pathfinding failed"}` | 路径查找失败 | 尝试执行`/stop`命令后再使用其他坐标重新尝试。 |
| `{"error":"no crafting table"}` | 无工作台导致无法进行制作操作 | 先将机器人移动到工作台附近。 |
| 机器人陷入无限循环 | 路径查找功能出现故障 | 执行`/stop`命令后重新尝试。 |

**自动重连机制**：服务会在断开连接后每5秒自动重连一次。

---

## 其他资源
- `references/api-spec.md`：完整的API规范及所有请求/响应字段说明。
- `references/dependency-guide.md`：其他技能如何声明对Minecraft Bridge的依赖关系。
- `references/troubleshooting.md`：详细的错误诊断指南。
- `scripts/start.sh` / `scripts/stop.sh`：用于方便地启动/停止Minecraft Bridge服务的脚本。