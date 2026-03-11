---
name: minecraft-server-admin
description: 通过 RCON 远程控制台执行 Minecraft Java 版本的管理员命令。这些命令可用于玩家管理、白名单管理、物品/状态操作、世界规则设置、广播消息发送以及查看您控制的服务器上的最近日志记录。本教程仅涵盖游戏内的命令管理功能，不涉及服务器的完整生命周期管理、文件系统备份或插件安装/更新等操作；这些任务请使用专门的服务器运维技能来完成。目标服务器必须启用 RCON 功能，且本教程不适用于单人游戏模式（即非多人游戏世界）。
metadata:
  openclaw:
    emoji: "🖥️"
    requires:
      bins:
        - node
      env:
        - MC_RCON_HOST
        - MC_RCON_PORT
        - MC_RCON_PASSWORD
    install:
      - id: rcon-dep
        kind: node
        package: rcon-client
        label: "rcon-client — Minecraft RCON protocol"
    homepage: https://github.com/en1r0py1865/minecraft-skill
---
# Minecraft服务器管理员技能

**功能概述**：  
此技能允许您在游戏内远程控制Minecraft Java服务器。它通过RCON协议发送命令，以实时管理玩家、世界状态及服务器通信。请注意，该技能不涵盖服务器基础设施相关的操作（如进程生命周期管理、文件系统备份、插件安装或持续运行时间监控）——这些操作请使用专门的PaperMC运维技能来完成。使用此技能无需依赖`minecraft-bridge`，因为它会通过独立的TCP连接直接与服务器的管理员控制台进行通信。

**技术架构**：  
```
OpenClaw → RCON TCP (port 25575) → Minecraft Server Console
```

---

## 先决条件  

### 在服务器上启用RCON  
编辑`server.properties`文件：  
```properties
enable-rcon=true
rcon.port=25575
rcon.password=STRONG_PASSWORD_HERE
broadcast-rcon-to-ops=false
```  
更改设置后重启服务器。  

### 环境变量  
```
MC_RCON_HOST=localhost        # Server IP or hostname
MC_RCON_PORT=25575            # RCON port (must match server.properties)
MC_RCON_PASSWORD=yourpassword # RCON password (must match server.properties)
MC_SERVER_LOG=/path/to/server/logs/latest.log  # optional, for log analysis
```  

### 验证连接  
```bash
node ~/.openclaw/skills/minecraft-server-admin/scripts/rcon.js "list"
# Expected: "There are N of a max of M players online: ..."
```  

---

## 操作类别  

### 玩家管理  
对于所有与玩家相关的命令，请使用：`scripts/rcon.js "<command>"`  

**玩家列表与状态查询**  
- 查看在线玩家：`/list`  
- 判断玩家`[player]`是否在线：先执行`/list`，再检查玩家名称是否存在于列表中。  

**访问控制** ⚠️ 执行以下命令前需确认：  
- 踢出玩家：`/kick <player> [原因]`  
- 暂时禁言：`/ban <player> [原因]`（同时记录时间）  
- 永久禁言：`/ban <player> [原因]`  
- 禁言IP地址：`/ban-ip <player|ip> [原因]`  
- 解禁玩家：`/pardon <player>` 或 `/pardon-ip <ip>`  
- 添加到白名单：`/whitelist add <player>`  
- 从白名单中移除：`/whitelist remove <player>`  
- 授予玩家管理员权限：`/op <player>` ⚠️ 需谨慎使用（高权限操作）  
- 取消玩家管理员权限：`/deop <player>`  

**物品与状态管理**  
- 给予玩家物品：`/give <player> <item_id> [数量]`  
- 清空玩家背包：`/clear <player> [物品> [数量]`  
- 设置游戏模式：`/gamemode <生存|创造|冒险|观众> <player>`  
- 传送玩家：`/tp <player> <x> <y> <z>` 或 `/tp <player> <目标玩家>`  
- 设置玩家生命值/饥饿值：`/effect give <player> minecraft:regeneration ...`  
- 治疗玩家：`/effect give <player> minecraft:instant_health 1 10`  

### 世界管理  

- 设置时间：  
  - 设置为白天：`/time set day`  
  - 设置为夜晚：`/time set midnight`  
  - 设置为日出时间：`/time set 0`  
- 清除天气效果：`/weather clear [秒数]`  
  - 引起降雨：`/weather rain [秒数]`  
  - 引起雷电：`/weather thunder [秒数]`  

**世界状态管理**  
- 保存世界数据：`/save-all`（维护前务必执行）  
- 强制保存（用于备份）：`/save-off` → 备份后执行`/save-on`  
- 更改游戏难度：`/difficulty <和平|简单|普通|困难>`  
- 设置游戏规则：`/gamerule <规则> <值>`  
  - 例如：`keepInventory true`（保留玩家物品），`doDaylightCycle false`（禁用昼夜循环），`doFireTick false`（禁用火 tick机制）  
- 查找特定结构：`/locate structure minecraft:<结构名称>`  
- 填充游戏区域：`/fill <x1 y1 z1> <x2 y2 z2> <块>` ⚠️ 使用前请确认范围。  

**实体管理**  
- 杀死所有非玩家实体：`/kill @e[type=!player]` ⚠️ 会杀死所有非玩家角色  
- 杀死特定类型的实体：`/kill @e[type=minecraft:zombie>`  
- 清除掉落的物品：`/kill @e[type=minecraft:item]`  

### 广播与通信**  
- 在服务器内发送消息：`/say <消息>`（消息前缀为[Server]）  
- 在屏幕上显示标题：`/title @a "标题" {"文本":"<消息>","颜色":"gold","bold":true}`  
- 显示副标题：`/title @a "副标题" {"文本":"<消息>"}`  
- 发送私信：`/msg <玩家> <消息>`  
- 在游戏动作栏显示消息：`/title @a "动作栏" {"文本":"<消息>"}`  

### 性能监控**  
当被询问服务器性能时：  
1. 执行`/list`以查看玩家数量。  
2. 如果设置了`MC_SERVER_LOG`文件，请读取最后200行日志。  
3. 查看`references/log-patterns.md`中的日志模式。  
4. 报告问题，例如：TPS（每秒传输次数）异常、错误频率或玩家活动高峰。  

---

## 安全协议  
所有具有破坏性或高权限的命令均需**确认**：  
```
⚠️  Dangerous Operation
Command: /ban SomePlayer griefing and harassment
Server:  ${MC_RCON_HOST}:${MC_RCON_PORT}
Effect:  Permanently bans SomePlayer from server

Type 'confirm' to proceed, or 'cancel' to abort.
```  

**需要确认的操作**：  
- `ban`、`ban-ip`（永久限制账户）  
- `op`（授予管理员权限）  
- `fill`（修改大面积游戏区域）  
- `kill @e`（批量删除实体）  
- `stop`（关闭服务器）  
- `save-off`（暂停自动保存功能，操作失误可能导致数据丢失）。  

**审计日志记录**：  
每次执行上述操作后，将相关记录追加到OpenClaw内存中：  
```
## Server Admin Log [ISO timestamp]
- Command: /ban PlayerX "repeated griefing"
- Executed by: [OpenClaw user]
- Result: success
```  

---

## 响应格式  

### 玩家列表（`/list`命令的返回结果）  
解析并显示玩家列表：  
```
👥 Players Online (3/20):
  • Steve — [show coords if available]
  • Alex
  • Notch
```  

### 被踢出/被禁言的确认信息  
```
✅ Done: PlayerX has been banned
   Reason: griefing
   Effective immediately
   To undo: /pardon PlayerX
```  

### 错误处理  
- 连接失败：检查RCON配置及服务器是否正在运行。  
- 认证失败：可能是因为输入了错误的`MC_RCON_PASSWORD`。  
- 命令执行无结果：服务器可能未识别该命令（请检查服务器版本）。  

## 日志分析  
当用户询问服务器状态或玩家历史记录时：  
1. 确保`MC_SERVER_LOG`文件已设置且存在。  
2. 读取最后N行日志：`tail -500 <log_file>`  
3. 根据`references/log-patterns.md`中的模式分析日志。  
4. 总结分析结果：  
```
📊 Server Log Summary (last 2 hours)
  Player logins: 14
  Player logouts: 12 (2 still online)
  Errors/Warnings: 3
    - [15:42] Can't keep up! Running 2500ms behind
    - [16:10] Saving chunks for level 'world'
  Suspicious activity: none detected
```  

## 额外资源  
- `references/commands.md`：包含所有Minecraft原版命令及其语法和权限级别。  
- `references/log-patterns.md`：常见日志模式及其含义。  
- `scripts/rcon.js`：用于执行上述所有命令的RCON客户端程序。  
- `scripts/log-analyzer.js`：日志解析工具。