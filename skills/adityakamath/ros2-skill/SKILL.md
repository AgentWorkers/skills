---
name: ros2-skill
description: "通过 `rclpy` CLI 直接控制 ROS 2 机器人。当用户询问有关 ROS 2 主题（topics）、服务（services）、节点（nodes）、参数（parameters）、动作（actions）、机器人运动（robot movement）、传感器数据（sensor data）或任何与 ROS 2 机器人交互的相关内容时，可以使用该工具。"
license: Apache-2.0
compatibility: "Requires python3, rclpy, and ROS 2 environment sourced"
user-invocable: true
metadata: {"openclaw": {"emoji": "🤖", "requires": {"bins": ["python3", "ros2"], "pip": ["rclpy", "rosidl-runtime-py"]}, "category": "robotics", "tags": ["ros2", "robotics", "rclpy"]}, "author": ["adityakamath", "lpigeon"], "version": "3.0.0"}
---
# ROS 2 Skill

该工具通过 `rclpy` 直接控制并监控 ROS 2 机器人。

**架构：** 客户端 → `ros2_cli.py` → `rclpy` → ROS 2

所有命令的输出均为 JSON 格式。错误信息会包含 `{"error": "..."}`。

有关命令的完整参考（包括参数、选项和输出示例），请参阅 [references/COMMANDS.md](references/COMMANDS.md)。

---

## 设置

### 1. 设置 ROS 2 环境

```bash
source /opt/ros/${ROS_DISTRO}/setup.bash
```

### 2. 安装依赖项

```bash
pip install rclpy rosidl-runtime-py
```

### 3. 在 ROS 2 机器人上运行

该命令行工具必须在安装了 ROS 2 并配置好了环境变量的机器上运行。

---

## 重要提示：请先检查 ROS 2 的安装情况

在进行任何操作之前，请确保 ROS 2 已正确安装：

```bash
python {baseDir}/scripts/ros2_cli.py version
```

---

## 命令快速参考

| 类别 | 命令 | 描述 |
|----------|---------|-------------|
| 连接 | `version` | 检测 ROS 2 的版本 |
| 主题 | `topics list` | 列出所有活跃的主题及其类型 |
| 主题 | `topics type <topic>` | 获取指定主题的消息类型 |
| 主题 | `topics details <topic>` | 获取主题的发布者/订阅者信息 |
| 主题 | `topics message <msg_type>` | 获取指定主题的消息字段结构 |
| 主题 | `topics subscribe <topic>` | 订阅并接收指定主题的消息 |
| 主题 | `topics publish <topic> <json>` | 向指定主题发布消息 |
| 主题 | `topics publish-sequence <topic> <msgs> <durs>` | 以指定的频率重复发布消息序列 |
| 服务 | `services list` | 列出所有可用的服务 |
| 服务 | `services type <service>` | 获取服务的类型 |
| 服务 | `services details <service>` | 获取服务的请求/响应字段 |
| 服务 | `services call <service> <json>` | 调用指定服务 |
| 节点 | `nodes list` | 列出所有活跃的节点 |
| 节点 | `nodes details <node>` | 获取节点的主题和服务信息 |
| 参数 | `params list <node>` | 列出节点的参数 |
| 参数 | `params get <node:param>` | 获取参数的值 |
| 参数 | `params set <node:param> <value>` | 设置参数的值 |
| 动作 | `actions list` | 列出可用的动作服务器 |
| 动作 | `actions details <action>` | 获取动作的目标/结果/反馈信息 |
| 动作 | `actions send <action> <json>` | 发送动作指令 |

---

## 关键命令

### version

```bash
python {baseDir}/scripts/ros2_cli.py version
```

### topics list / type / details / message

```bash
python {baseDir}/scripts/ros2_cli.py topics list
python {baseDir}/scripts/ros2_cli.py topics type /turtle1/cmd_vel
python {baseDir}/scripts/ros2_cli.py topics details /turtle1/cmd_vel
python {baseDir}/scripts/ros2_cli.py topics message geometry_msgs/Twist
```

### topics subscribe

- 不使用 `--duration` 选项：仅返回第一条消息。
- 使用 `--duration` 选项：持续接收消息。

```bash
python {baseDir}/scripts/ros2_cli.py topics subscribe /turtle1/pose
python {baseDir}/scripts/ros2_cli.py topics subscribe /odom --duration 10 --max-messages 50
```

### topics publish

- 不使用 `--duration` 选项：一次性发布消息。
- 使用 `--duration` 选项：以指定的频率重复发布消息。**对于控制速度的命令，请务必使用 `--duration` 选项**——因为大多数机器人控制器在未收到连续的 `cmd_vel` 消息时会停止响应。

```bash
# Single-shot
python {baseDir}/scripts/ros2_cli.py topics publish /trigger '{"data": ""}'

# Move forward 3 seconds (velocity — use --duration)
python {baseDir}/scripts/ros2_cli.py topics publish /cmd_vel \
  '{"linear":{"x":1.0,"y":0,"z":0},"angular":{"x":0,"y":0,"z":0}}' --duration 3

# Stop
python {baseDir}/scripts/ros2_cli.py topics publish /cmd_vel \
  '{"linear":{"x":0,"y":0,"z":0},"angular":{"x":0,"y":0,"z":0}}'
```

选项：`--duration`（单位：秒），`--rate`（单位：赫兹，默认值：10）

### topics publish-sequence

以指定的频率重复发布一系列消息。数组中的元素数量必须与 `--duration` 的值相同。

```bash
# Forward 3s then stop
python {baseDir}/scripts/ros2_cli.py topics publish-sequence /cmd_vel \
  '[{"linear":{"x":1.0,"y":0,"z":0},"angular":{"x":0,"y":0,"z":0}},{"linear":{"x":0,"y":0,"z":0},"angular":{"x":0,"y":0,"z":0}}]' \
  '[3.0, 0.5]'

# Draw a square (turtlesim)
python {baseDir}/scripts/ros2_cli.py topics publish-sequence /turtle1/cmd_vel \
  '[{"linear":{"x":2},"angular":{"z":0}},{"linear":{"x":0},"angular":{"z":1.5708}},{"linear":{"x":2},"angular":{"z":0}},{"linear":{"x":0},"angular":{"z":1.5708}},{"linear":{"x":2},"angular":{"z":0}},{"linear":{"x":0},"angular":{"z":1.5708}},{"linear":{"x":2},"angular":{"z":0}},{"linear":{"x":0},"angular":{"z":1.5708}},{"linear":{"x":0},"angular":{"z":0}}]' \
  '[1,1,1,1,1,1,1,1,0.5]'
```

选项：`--rate`（单位：赫兹，默认值：10）

### services list / type / details

```bash
python {baseDir}/scripts/ros2_cli.py services list
python {baseDir}/scripts/ros2_cli.py services type /spawn
python {baseDir}/scripts/ros2_cli.py services details /spawn
```

### services call

```bash
python {baseDir}/scripts/ros2_cli.py services call /reset '{}'
python {baseDir}/scripts/ros2_cli.py services call /spawn \
  '{"x":3.0,"y":3.0,"theta":0.0,"name":"turtle2"}'
```

### nodes list / details

```bash
python {baseDir}/scripts/ros2_cli.py nodes list
python {baseDir}/scripts/ros2_cli.py nodes details /turtlesim
```

### params list / get / set

命令格式：`params list <node:param_name>`

```bash
python {baseDir}/scripts/ros2_cli.py params list /turtlesim
python {baseDir}/scripts/ros2_cli.py params get /turtlesim:background_r
python {baseDir}/scripts/ros2_cli.py params set /turtlesim:background_r 255
```

### actions list / details / send

```bash
python {baseDir}/scripts/ros2_cli.py actions list
python {baseDir}/scripts/ros2_cli.py actions details /turtle1/rotate_absolute
python {baseDir}/scripts/ros2_cli.py actions send /turtle1/rotate_absolute \
  '{"theta":3.14}'
```

---

## 工作流程示例

### 1. 探索机器人系统

```bash
python {baseDir}/scripts/ros2_cli.py version
python {baseDir}/scripts/ros2_cli.py topics list
python {baseDir}/scripts/ros2_cli.py nodes list
python {baseDir}/scripts/ros2_cli.py services list
python {baseDir}/scripts/ros2_cli.py topics type /cmd_vel
python {baseDir}/scripts/ros2_cli.py topics message geometry_msgs/Twist
python {baseDir}/scripts/ros2_cli.py actions list
python {baseDir}/scripts/ros2_cli.py params list /robot_node
```

### 2. 移动机器人

- 首先检查消息结构，然后发送移动指令，移动完成后务必停止机器人。

```bash
python {baseDir}/scripts/ros2_cli.py topics message geometry_msgs/Twist
python {baseDir}/scripts/ros2_cli.py topics publish-sequence /cmd_vel \
  '[{"linear":{"x":1.0,"y":0,"z":0},"angular":{"x":0,"y":0,"z":0}},{"linear":{"x":0,"y":0,"z":0},"angular":{"x":0,"y":0,"z":0}}]' \
  '[2.0, 0.5]'
```

### 3. 读取传感器数据

```bash
python {baseDir}/scripts/ros2_cli.py topics type /scan
python {baseDir}/scripts/ros2_cli.py topics message sensor_msgs/LaserScan
python {baseDir}/scripts/ros2_cli.py topics subscribe /scan --duration 3
python {baseDir}/scripts/ros2_cli.py topics subscribe /odom --duration 10 --max-messages 50
```

### 4. 使用服务

```bash
python {baseDir}/scripts/ros2_cli.py services list
python {baseDir}/scripts/ros2_cli.py services details /spawn
python {baseDir}/scripts/ros2_cli.py services call /spawn \
  '{"x":3.0,"y":3.0,"theta":0.0,"name":"turtle2"}'
```

### 5. 执行动作

```bash
python {baseDir}/scripts/ros2_cli.py actions list
python {baseDir}/scripts/ros2_cli.py actions details /turtle1/rotate_absolute
python {baseDir}/scripts/ros2_cli.py actions send /turtle1/rotate_absolute \
  '{"theta":1.57}'
```

### 6. 修改参数

```bash
python {baseDir}/scripts/ros2_cli.py params list /turtlesim
python {baseDir}/scripts/ros2_cli.py params get /turtlesim:background_r
python {baseDir}/scripts/ros2_cli.py params set /turtlesim:background_r 255
python {baseDir}/scripts/ros2_cli.py params set /turtlesim:background_g 0
python {baseDir}/scripts/ros2_cli.py params set /turtlesim:background_b 0
```

---

## 安全注意事项

**可能对机器人造成影响的命令：**
- `topics publish` / `topics publish-sequence`：用于发送移动或控制指令。
- `services call`：可能重置、启动、停止或改变机器人的状态。
- `params set`：修改运行时的参数。
- `actions send`：触发机器人的动作（如旋转、导航等）。

**移动完成后务必停止机器人。**任何 `publish-sequence` 操作中的最后一条消息应为全零：
```json
{"linear":{"x":0,"y":0,"z":0},"angular":{"x":0,"y":0,"z":0}}
```

**在继续执行任何操作之前，请务必检查 JSON 输出中是否包含错误信息。**

---

## 故障排除

| 问题 | 原因 | 解决方案 |
|---------|-------|----------|
| 未安装 rclpy | 缺少 Python 包 | 运行：`pip install rclpy rosidl-runtime-py` |
| ROS 2 环境未配置 | 未正确设置环境变量 | 运行：`source /opt/ros/${ROS_DISTRO}/setup.bash` |
| 未找到主题 | 机器人节点未运行 | 确保节点已启动且工作空间已配置正确 |
| 服务不可用 | 服务未注册 | 使用 `services list` 查看可用的服务 |
| 参数相关命令失败 | 节点未提供相应参数 | 部分节点可能不暴露参数 |
| 动作命令失败 | 相关动作服务器不可用 | 使用 `actions list` 查看可用的动作 |
| JSON 格式错误 | JSON 数据格式不正确 | 在发送数据前请验证其格式（注意单引号和双引号的正确使用） |
| 订阅超时 | 指定主题没有发布者 | 使用 `topics details` 确认是否存在发布者 |
| 发布序列长度错误 | 数组长度不匹配 | `messages` 数组和 `durations` 数组的长度必须相同 |