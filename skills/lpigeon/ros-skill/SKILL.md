---
name: ros-skill
description: "通过 `rosbridge` 的 WebSocket CLI 来控制 ROS/ROS2 机器人。当用户需要查询 ROS 主题（topics）、服务（services）、节点（nodes）、参数（parameters）、动作（actions）、机器人运动（robot movement）、传感器数据（sensor data）或任何与 ROS/ROS2 机器人相关的交互时，可以使用该工具。"
license: Apache-2.0
compatibility: "Requires python3, websocket-client pip package, and rosbridge running on the robot (default port 9090)"
user-invocable: true
metadata: {"openclaw": {"emoji": "🤖", "requires": {"bins": ["python3"], "pip": ["websocket-client"]}, "category": "robotics", "tags": ["ros", "ros2", "robotics", "rosbridge"]}, "author": "lpigeon", "version": "1.0.1"}
---
# ROS 技能

通过 rosbridge WebSocket 控制和监控 ROS/ROS2 机器人。

**架构：** 客户端 → `ros_cli.py` → rosbridge (WebSocket :9090) → ROS/ROS2 机器人

所有命令的输出均为 JSON 格式。错误信息包含 `{"error": "..."}`。

有关命令的完整参考（包括参数、选项和输出示例），请参阅 [references/COMMANDS.md](references/COMMANDS.md)。

---

## 设置

### 1. 安装依赖项

```bash
pip install websocket-client
```

### 2. 在机器人上启动 rosbridge

**ROS 1：**
```bash
sudo apt install ros-${ROS_DISTRO}-rosbridge-server
roslaunch rosbridge_server rosbridge_websocket.launch
```

**ROS 2：**
```bash
sudo apt install ros-${ROS_DISTRO}-rosbridge-server
ros2 launch rosbridge_server rosbridge_websocket_launch.xml
```

---

## 重要提示：**务必先建立连接**

在任何操作之前，请先测试连接是否正常：

```bash
python {baseDir}/scripts/ros_cli.py connect
python {baseDir}/scripts/ros_cli.py --ip <ROBOT_IP> connect
```

---

## 全局选项

| 标志 | 默认值 | 描述 |
|------|---------|-------------|
| `--ip` | `127.0.0.1` | Rosbridge 的 IP 地址 |
| `--port` | `9090` | Rosbridge 的端口号 |
| `--timeout` | `5.0` | 连接和请求的超时时间（秒） |

---

## 命令快速参考

| 类别 | 命令 | 描述 |
|----------|---------|-------------|
| 连接 | `connect` | 测试 rosbridge 的连接性（ping、端口、WebSocket） |
| 连接 | `version` | 检测 ROS 的版本和发行版 |
| 主题 | `topics list` | 列出所有活跃的主题及其类型 |
| 主题 | `topics type <topic>` | 获取指定主题的消息类型 |
| 主题 | `topics details <topic>` | 获取主题的发布者/订阅者信息 |
| 主题 | `topics message <msg_type>` | 获取消息的字段结构 |
| 主题 | `topics subscribe <topic> <msg_type>` | 订阅并接收指定主题的消息 |
| 主题 | `topics publish <topic> <msg_type> <json>` | 向指定主题发布消息 |
| 主题 | `topics publish-sequence <topic> <msg_type> <msgs> <durs>` | 以指定的频率重复发布消息序列 |
| 服务 | `services list` | 列出所有可用的服务 |
| 服务 | `services type <service>` | 获取服务的类型 |
| 服务 | `services details <service>` | 获取服务的请求/响应字段 |
| 服务 | `services call <service> <type> <json>` | 调用服务 |
| 节点 | `nodes list` | 列出所有活跃的节点 |
| 节点 | `nodes details <node>` | 获取节点的主题和服务信息 |
| 参数 | `params list <node>` | 列出节点的参数（仅限 ROS 2） |
| 参数 | `params get <node:param>` | 获取节点参数的值（仅限 ROS 2） |
| 参数 | `params set <node:param> <value>` | 设置节点参数的值（仅限 ROS 2） |
| 动作 | `actions list` | 列出可用的动作服务器 |
| 动作 | `actions details <action>` | 获取动作的目标/结果/反馈信息（仅限 ROS 2） |
| 动作 | `actions send <action> <type> <json>` | 发送动作指令（仅限 ROS 2） |

---

## 关键命令

### connect

```bash
python {baseDir}/scripts/ros_cli.py connect
python {baseDir}/scripts/ros_cli.py --ip <ROBOT_IP> connect
```

### version

```bash
python {baseDir}/scripts/ros_cli.py version
```

### topics list / type / details / message

```bash
python {baseDir}/scripts/ros_cli.py topics list
python {baseDir}/scripts/ros_cli.py topics type /turtle1/cmd_vel
python {baseDir}/scripts/ros_cli.py topics details /turtle1/cmd_vel
python {baseDir}/scripts/ros_cli.py topics message geometry_msgs/Twist
```

### topics subscribe

- 不使用 `--duration`：仅返回第一条消息。
- 使用 `--duration`：持续接收消息。

```bash
python {baseDir}/scripts/ros_cli.py topics subscribe /turtle1/pose turtlesim/Pose
python {baseDir}/scripts/ros_cli.py topics subscribe /odom nav_msgs/Odometry --duration 10 --max-messages 50
python {baseDir}/scripts/ros_cli.py topics subscribe /scan sensor_msgs/LaserScan --timeout 10
```

### topics publish

- 不使用 `--duration`：一次性发布消息。
- 使用 `--duration`：以指定的频率重复发布消息。**对于控制速度的命令，请务必使用 `--duration`**——因为大多数机器人控制器在未收到连续的 `cmd_vel` 消息时会停止响应。

```bash
# Single-shot
python {baseDir}/scripts/ros_cli.py topics publish /trigger std_msgs/Empty '{}'

# Move forward 3 seconds (velocity — use --duration)
python {baseDir}/scripts/ros_cli.py topics publish /cmd_vel geometry_msgs/Twist \
  '{"linear":{"x":1.0,"y":0,"z":0},"angular":{"x":0,"y":0,"z":0}}' --duration 3

# Rotate left 2 seconds
python {baseDir}/scripts/ros_cli.py topics publish /cmd_vel geometry_msgs/Twist \
  '{"linear":{"x":0,"y":0,"z":0},"angular":{"x":0,"y":0,"z":0.5}}' --duration 2

# Stop
python {baseDir}/scripts/ros_cli.py topics publish /cmd_vel geometry_msgs/Twist \
  '{"linear":{"x":0,"y":0,"z":0},"angular":{"x":0,"y":0,"z":0}}'
```

选项：`--duration`（秒），`--rate`（赫兹，默认值 10）

### topics publish-sequence

按指定的频率重复发布一系列消息。数组的长度必须相同。

```bash
# Forward 3s then stop
python {baseDir}/scripts/ros_cli.py topics publish-sequence /cmd_vel geometry_msgs/Twist \
  '[{"linear":{"x":1.0,"y":0,"z":0},"angular":{"x":0,"y":0,"z":0}},{"linear":{"x":0,"y":0,"z":0},"angular":{"x":0,"y":0,"z":0}}]' \
  '[3.0, 0.5]'

# Draw a square (turtlesim)
python {baseDir}/scripts/ros_cli.py topics publish-sequence /turtle1/cmd_vel geometry_msgs/Twist \
  '[{"linear":{"x":2},"angular":{"z":0}},{"linear":{"x":0},"angular":{"z":1.5708}},{"linear":{"x":2},"angular":{"z":0}},{"linear":{"x":0},"angular":{"z":1.5708}},{"linear":{"x":2},"angular":{"z":0}},{"linear":{"x":0},"angular":{"z":1.5708}},{"linear":{"x":2},"angular":{"z":0}},{"linear":{"x":0},"angular":{"z":1.5708}},{"linear":{"x":0},"angular":{"z":0}}]' \
  '[1,1,1,1,1,1,1,1,0.5]'
```

选项：`--rate`（赫兹，默认值 10）

### services list / type / details

```bash
python {baseDir}/scripts/ros_cli.py services list
python {baseDir}/scripts/ros_cli.py services type /spawn
python {baseDir}/scripts/ros_cli.py services details /spawn
```

### services call

```bash
python {baseDir}/scripts/ros_cli.py services call /reset std_srvs/Empty '{}'
python {baseDir}/scripts/ros_cli.py services call /spawn turtlesim/Spawn \
  '{"x":3.0,"y":3.0,"theta":0.0,"name":"turtle2"}'
python {baseDir}/scripts/ros_cli.py services call /turtle1/set_pen turtlesim/srv/SetPen \
  '{"r":255,"g":0,"b":0,"width":3,"off":0}'
```

### nodes list / details

```bash
python {baseDir}/scripts/ros_cli.py nodes list
python {baseDir}/scripts/ros_cli.py nodes details /turtlesim
```

### params list / get / set（仅限 ROS 2）

使用 `params list` 输出中的 `node:param_name` 格式。

```bash
python {baseDir}/scripts/ros_cli.py params list /turtlesim
python {baseDir}/scripts/ros_cli.py params get /turtlesim:background_r
python {baseDir}/scripts/ros_cli.py params set /turtlesim:background_r 255
```

### actions list / details / send（仅限 ROS 2）

```bash
python {baseDir}/scripts/ros_cli.py actions list
python {baseDir}/scripts/ros_cli.py actions details /turtle1/rotate_absolute
python {baseDir}/scripts/ros_cli.py actions send /turtle1/rotate_absolute \
  turtlesim/action/RotateAbsolute '{"theta":3.14}'
```

---

## 工作流程示例

### 1. 探索机器人系统

```bash
python {baseDir}/scripts/ros_cli.py --ip <ROBOT_IP> connect
python {baseDir}/scripts/ros_cli.py --ip <ROBOT_IP> version
python {baseDir}/scripts/ros_cli.py --ip <ROBOT_IP> topics list
python {baseDir}/scripts/ros_cli.py --ip <ROBOT_IP> nodes list
python {baseDir}/scripts/ros_cli.py --ip <ROBOT_IP> services list
python {baseDir}/scripts/ros_cli.py --ip <ROBOT_IP> topics type /cmd_vel
python {baseDir}/scripts/ros_cli.py --ip <ROBOT_IP> topics message geometry_msgs/Twist
python {baseDir}/scripts/ros_cli.py --ip <ROBOT_IP> actions list
python {baseDir}/scripts/ros_cli.py --ip <ROBOT_IP> params list /robot_node
```

### 2. 移动机器人

- 首先检查消息结构，然后发布移动指令，移动完成后务必停止机器人。

```bash
python {baseDir}/scripts/ros_cli.py topics message geometry_msgs/Twist
python {baseDir}/scripts/ros_cli.py topics publish-sequence /cmd_vel geometry_msgs/Twist \
  '[{"linear":{"x":1.0,"y":0,"z":0},"angular":{"x":0,"y":0,"z":0}},{"linear":{"x":0,"y":0,"z":0},"angular":{"x":0,"y":0,"z":0}}]' \
  '[2.0, 0.5]'
```

### 3. 读取传感器数据

```bash
python {baseDir}/scripts/ros_cli.py topics type /scan
python {baseDir}/scripts/ros_cli.py topics message sensor_msgs/LaserScan
python {baseDir}/scripts/ros_cli.py topics subscribe /scan sensor_msgs/LaserScan --timeout 3
python {baseDir}/scripts/ros_cli.py topics subscribe /odom nav_msgs/Odometry --duration 10 --max-messages 50
```

### 4. 使用服务

```bash
python {baseDir}/scripts/ros_cli.py services list
python {baseDir}/scripts/ros_cli.py services details /spawn
python {baseDir}/scripts/ros_cli.py services call /spawn turtlesim/Spawn \
  '{"x":3.0,"y":3.0,"theta":0.0,"name":"turtle2"}'
```

### 5. ROS 2 动作

```bash
python {baseDir}/scripts/ros_cli.py actions list
python {baseDir}/scripts/ros_cli.py actions details /turtle1/rotate_absolute
python {baseDir}/scripts/ros_cli.py actions send /turtle1/rotate_absolute \
  turtlesim/action/RotateAbsolute '{"theta":1.57}'
```

### 6. 修改参数（仅限 ROS 2）

```bash
python {baseDir}/scripts/ros_cli.py params list /turtlesim
python {baseDir}/scripts/ros_cli.py params get /turtlesim:background_r
python {baseDir}/scripts/ros_cli.py params set /turtlesim:background_r 255
python {baseDir}/scripts/ros_cli.py params set /turtlesim:background_g 0
python {baseDir}/scripts/ros_cli.py params set /turtlesim:background_b 0
```

---

## 安全注意事项

**可能对机器人造成影响的命令：**
- `topics publish` / `topics publish-sequence`：发送移动或控制指令
- `services call`：可以重置、启动、停止或改变机器人的状态
- `params set`：修改运行时参数
- `actions send`：触发机器人的动作（如旋转、导航等）

**移动完成后务必停止机器人。**任何 `publish-sequence` 中的最后一条消息应为全零：
```json
{"linear":{"x":0,"y":0,"z":0},"angular":{"x":0,"y":0,"z":0}}
```

**在继续执行任何操作之前，请务必检查 JSON 输出中是否存在错误。**

---

## 故障排除

| 问题 | 原因 | 解决方案 |
|---------|-------|----------|
| 连接失败 | rosbridge 未运行 | 启动 rosbridge：`ros2 launch rosbridge_server rosbridge_websocket_launch.xml` |
| 超时错误 | 网络速度慢或数据量过大 | 增加超时时间：`--timeout 10` 或 `--timeout 30` |
| 未找到主题 | ROS 节点未运行 | 确保节点已启动且工作空间已加载 |
| 主题列表为空 | rosapi 未启用 | 验证 rosbridge 是否包含 rosapi（标准安装中已包含） |
| 参数命令失败 | 使用了 ROS 1 | `params` 命令仅适用于 ROS 2 |
| 动作命令失败 | 使用了 ROS 1 | `actions` 命令仅适用于 ROS 2 |
| JSON 格式错误 | 数据格式不正确 | 在发送前验证 JSON 数据（注意单引号和双引号的使用） |
| 订阅超时 | 指定主题没有发布者 | 使用 `topics details` 验证是否存在发布者 |
| 发布序列长度错误 | 数组长度不匹配 | `messages` 和 `durations` 数组的长度必须相同 |