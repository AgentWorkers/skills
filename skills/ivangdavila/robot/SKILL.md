---
name: Robot
slug: robot
version: 1.0.0
description: 从爱好到工业应用，通过硬件接线、ROS2（Robot Operating System 2）、运动规划以及安全约束来构建机器人。
metadata: {"clawdbot":{"emoji":"🤖","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---
## 使用场景

当用户需要机器人技术支持时，例如Arduino/ESP32的接线、ROS2的配置、电机控制、传感器集成或工业机器人的编程，本工具可以提供帮助。该工具能够处理从业余爱好者到专业领域的各种硬件选择、代码生成和调试工作。

## 架构

系统的内存数据存储在`~/robot/`目录下，采用分层结构。有关初始设置的具体信息，请参阅`memory-template.md`文件。

```
~/robot/
├── memory.md          # HOT: inventory + active project
├── inventory.md       # Hardware owned (boards, sensors, motors)
├── projects/          # Per-project configs and learnings
│   └── {name}.md      # Project-specific notes
├── corrections.md     # What failed + fixes found
└── archive/           # Completed project summaries
```

## 快速参考

| 主题 | 对应文件 |
|-------|------|
| 内存设置 | `memory-template.md` |
| Arduino、ESP32、RPi的接线 | `hardware.md` |
| 传感器的接线与代码实现 | `sensors.md` |
| 电机类型与驱动程序 | `motors.md` |
| ROS1/ROS2、Gazebo、MoveIt | `ros.md` |
| 工业机器人（ABB、KUKA、UR） | `industrial.md` |
| 系统性故障排除 | `debugging.md` |
| 常用项目模板 | `projects.md` |

## 核心规则

### 1. 先检查内存配置
在给出任何建议之前，请务必：
1. 阅读`~/robot/memory.md`文件，了解用户现有的硬件设备。
2. 查看`~/robot/projects/`目录，确认是否有正在进行的项目。
3. 查阅`~/robot/corrections.md`文件，了解以往可能遇到的问题及解决方法。

### 2. 明确硬件信息
在编写任何代码之前，务必提供以下详细信息：
- 硬件型号（具体板子型号、传感器/电机型号）
- 电压范围

“Arduino”这个术语较为模糊（可能是Uno、Nano还是基于ESP32的版本？请确认后更新到硬件清单中）。

### 3. 主动更新硬件信息
- 当用户提到自己拥有的硬件时，将其添加到`inventory.md`文件中。
- 当用户开始新项目时，创建对应的项目文件夹（格式为`projects/{项目名称}.md`）。
- 发现硬件问题时，及时记录解决方案并更新`corrections.md`文件。
- 项目完成后，将其归档到`archive/`目录。

### 4. 明确所有软件版本信息
务必询问并记录以下版本信息：
- Arduino的核心版本及所使用的库版本
- ROS的发行版（Humble、Iron、Foxy、Noetic等）
- 工业控制器的固件版本

### 5. 工业应用中的模拟测试优先
对于ABB/KUKA/Fanuc/UR等工业机器人的代码开发：
- 必须明确使用的是模拟环境还是真实硬件。
- 在未进行安全讨论的情况下，切勿生成控制代码。
- 所有代码中都必须包含速度限制和安全检查机制。

## 常见硬件使用陷阱

### 板子选择相关问题
- 在ESP32上使用`Servo.h`会导致程序崩溃，请改用`ESP32Servo.h`（因为API不同）。
- ESP32上没有`analogWrite()`函数，应使用`ledcWrite()`配合通道设置进行模拟操作。
- ESP32的GPIO 6-11引脚是用于存储闪存的，直接操作这些引脚可能导致系统崩溃。
- ESP32的GPIO 34-39引脚仅支持输入功能，若用于输出则可能导致输出失败。
- Arduino的引脚0和1用于串行通信，使用这些引脚进行数据传输会干扰上传过程。

### 电压和电流问题
- 如果使用5V电压的传感器连接到3.3V电压的板上，且未使用电压分压器，可能会导致引脚永久性损坏。
- 当GPIO引脚的输出电流超过40mA（Arduino）或12mA（ESP32）时，可能会损坏引脚。
- 如果电机和逻辑电路共用同一电源轨，电压波动可能导致系统异常重启。
- 如果不同板子之间没有共用地线，可能会导致传感器读数不稳定。

### 传感器使用相关问题
- HC-SR04传感器的Echo引脚需要5V电压，如果连接到3.3V电压的板上，需要使用电压分压器或电平转换器。
- DHT22传感器的读取间隔如果小于2秒，可能会导致数据失效或错误。
- I2C总线的长度超过30厘米且未使用上拉电阻时，可能会导致数据传输不稳定。
- 如果MPU6050的FIFO缓冲区数据未及时读取，可能会导致数据损坏。

## ROS使用相关问题
- 混合使用`rospy`（ROS1）和`rclpy`（ROS2）可能会导致导入错误。
- 如果忘记执行`source install/setup.bash`命令，系统可能会提示“package not found”错误。
- 如果发布者（publisher）和订阅者（subscriber）的QoS设置不匹配，消息可能会被忽略。
- `static_transform_publisher`的语法因ROS2版本而异。
- Gazebo Classic插件与Ignition/Fortress插件可能存在兼容性问题。

## 工业应用中的其他问题
- 在使用MoveL命令时，如果路径经过奇异点（如关节的快速转动），可能会导致系统异常。
- 如果坐标系设置不正确（基础坐标系、世界坐标系或工具坐标系不一致），可能会导致位置计算错误。
- 在使用MoveL命令之前未先执行MoveJ命令，可能会导致机器人路径经过障碍物。
- 在有人类活动的环境中设置过高的移动速度可能会违反安全规定。
- 如果绕过SafeMove/SafetyIO信号，可能会导致物理安全机制失效。