---
name: peaq-robotics
description: >
  **OpenClaw 的 peaq-robotics-ros2 核心运行时**  
  用于启动/停止 ROS 2 节点，并调用 DID（数据存储）、存储以及访问控制服务。适用于需要运行现有的 peaq ROS2 工作区的场景（不涉及安装、构建或资金传输等操作）。
metadata: {"openclaw":{"emoji":"robot","requires":{"bins":["ros2","python3"],"env":["PEAQ_ROS2_ROOT"]}}}
---
# peaq-robotics（核心功能）

## 该技能的用途

当机器已经具备可用的`peaq-robotics-ros2`工作空间，并且您希望OpenClaw能够运行ROS 2的核心节点并调用peaq服务时，可以使用此技能：
- 创建/读取DID（Digital Identity）
- 添加/读取存储数据
- 执行与角色/权限相关的操作

## 该技能不支持的功能

为了降低风险并简化在注册系统中的审批流程，该技能不支持以下功能：
- 仓库克隆/构建自动化
- 资金转移命令
- 钱包操作
- 通过环境变量覆盖来扩展可信设置/JSON配置

如果您需要自动化安装、初始化或管理资金，请使用配套的管理员技能（`peaq-robotics-admin`）。

## 必需的先决条件

在使用核心命令之前，请确保满足以下条件：
- 已安装ROS 2，并且ROS 2能够正常运行。
- `peaq-robotics-ros2`工作空间已经存在且已完成构建。
- `PEAQ_ROS2_ROOT`变量指向正确的仓库路径。
- 配置文件`PEAQ_ROS2_CONFIG_YAML`已配置，或者使用默认路径`<PEAQ_ROS2_ROOT>/peaq_ros2/examples/config/peaq_robot.yaml`。
- 当前shell会话已正确初始化ROS环境。

## 手动设置指南（无需安装脚本）

请根据`peaq-robotics-ros2`的官方文档，手动完成仓库克隆、构建和配置步骤，然后为OpenClaw运行时设置相应的环境变量：

```bash
export PEAQ_ROS2_ROOT="$HOME/peaq-robotics-ros2"
# optional
export PEAQ_ROS2_CONFIG_YAML="$HOME/peaq-robotics-ros2/peaq_ros2_examples/config/peaq_robot.yaml"
```

## 如果用户需要自定义辅助脚本

建议用户创建仅包含所需设置和明确配置的自定义脚本：

```bash
#!/usr/bin/env bash
set -euo pipefail
ros2 run peaq_ros2_core core_node --ros-args -p config.yaml_path:="$PEAQ_ROS2_CONFIG_YAML"
```

用户可以直接运行这些自定义脚本，或者继续使用该技能提供的命令来调用相关服务。

## 核心命令

### 节点生命周期相关命令
- `{baseDir}/scripts/peaq_ros2.sh core-start`：启动peaq-robotics核心服务
- `{baseDir}/scripts/peaq_ros2.sh core-configure`：配置peaq-robotics服务
- `{baseDir}/scripts/peaq_ros2.sh core-activate`：激活peaq-robotics服务
- `{baseDir}/scripts/peaq_ros2.sh core-stop`：停止peaq-robotics服务

### 身份管理相关命令
- `{baseDir}/scripts/peaq_ros2.sh did-create`：创建新的DID
- `{baseDir}/scripts/peaq_ros2.sh did-create '{"type":"robot"}`：创建类型为“robot”的DID
- `{baseDir}/scripts/peaq_ros2.sh did-create @/path/to/file.json`：创建指定路径的JSON文件
- `{baseDir}/scripts/peaq_ros2.sh did-read`：读取指定路径的JSON文件

### 存储管理相关命令
- `{baseDir}/scripts/peaq_ros2.sh store-add sensor_data '{"temp":25.5}' FAST`：快速存储传感器数据
- `{baseDir}/scripts/peaq_ros2.sh store-read sensor_data`：读取存储的数据

### 访问控制相关命令
- `{baseDir}/scripts/peaq_ros2.sh access-create-role operator 'Robot operator'`：创建名为“Robot operator”的角色
- `{baseDir}/scripts/peaq_ros2.sh access-create-permission move_robot`：为“Robot operator”角色分配“move_robot”权限
- `{baseDir}/scripts/peaq_ros2.sh access-assign-permission move_robot operator`：重新分配“move_robot”权限
- `{baseDir}/scripts/peaq_ros2.sh access-grant-role operator did:peaq:<address>`：向指定地址的账户授予权限

### 身份卡管理相关命令
- `{baseDir}/scripts/peaq_ros2.sh identity-card-json [name] [roles_csv] [endpoints_json] [metadata_json]`：生成身份卡信息
- `{baseDir}/scripts/peaq_ros2.sh identity-card-did-create [name] [roles_csv] [endpoints_json] [metadata_json]`：创建新的身份卡
- `{baseDir}/scripts/peaq_ros2.sh identity-card-did-read`：读取身份卡信息

### 资金请求相关命令（仅提供模板，不支持资金转移）
- `{baseDir}/scripts/peaq_ros2.sh fund-request [amount] [reason]`：提交资金请求

## 行为与安全注意事项
- 该技能本身不负责生成ROS配置脚本；环境初始化需在外部完成。
- 输入的`@/path/file.json`文件必须位于以下路径：
  - `peaq-robotics`技能文件夹
  - `PEAQ_ROS2_ROOT`目录
  - `peaq_ros2`工作空间下的`.peaq_robot`文件
- JSON参数在调用ROS 2服务之前会进行解析和验证。
- 服务请求的数据将以JSON对象的形式传递给`ros2 service call`（不支持Shell中的YAML插值）。

## 一键操作提示
- “启动peaq-robotics核心服务并创建我的DID。如果需要资金，请发送一条资金请求。”
- “读取我的DID信息，将其存储为`agent_state`，然后再读取出来。”
- “创建名为‘operator’的角色，为其分配‘move_robot’权限，并显示相应的响应。”

## 详细参考资料

有关所有服务名称和字段的详细信息，请参阅：
- `references/peaq_ros2_services.md`