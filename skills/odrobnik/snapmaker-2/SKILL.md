---
name: snapmaker-2
description: "通过 HTTP API 控制和监控 Snapmaker 2.0 3D 打印机：可以查看设备状态、管理打印任务、监控打印进度以及接收设备发出的事件通知。"
summary: "Snapmaker 2.0 3D printer control: status, jobs, monitoring."
version: 1.2.1
homepage: https://github.com/odrobnik/snapmaker-skill
metadata:
  {
    "openclaw":
      {
        "emoji": "🖨️",
        "requires": { "bins": ["python3"] },
      },
  }
---

# Snapmaker 2.0 技能

通过 HTTP API 控制和监控 Snapmaker 2.0 3D 打印机。

## 功能

- **状态监控** - 实时显示打印机状态（温度、进度、位置）
- **作业管理** - 发送、启动、暂停、恢复和停止打印作业
- **安全功能** - 在未经确认的情况下，禁止干扰正在进行的打印操作
- **进度监控** - 实时显示打印进度
- **通知支持** - 检测打印完成、耗材耗尽或出现错误

## 配置

在工作区的 `snapmaker/` 文件夹中创建 `config.json` 文件（例如：`~/clawd/snapmaker/config.json`）。
请参考 `config.json.example` 作为配置的起点。

### 获取令牌：

打开 Snapmaker Luban 应用程序，连接到您的打印机，在连接设置中找到令牌，并将其复制到 `config.json` 文件中。

## 使用方法

### 发现打印机（Discovery）

Snapmaker 使用 UDP 广播协议进行发现（无需认证）。如果 UDP 没有收到响应（例如，因为位于不同的子网中），则会切换到使用 HTTP 进行连接。

### 基本命令

### 作业控制

### 安全选项

- `--yes` - 跳过确认提示（请谨慎使用！）
- `--force` - 强制忽略安全检查（不推荐）

所有修改打印机状态的命令都需要确认，除非指定了 `--yes`。

## API 端点

该技能使用以下 Snapmaker HTTP API v1 端点：

- `POST /api/v1/connect` - 建立连接
- `GET /api/v1/status` - 获取打印机状态
- `POST /api/v1/prepare_print` - 上传文件
- `POST /api/v1/start_print` - 开始打印
- `POST /api/v1/pause` - 暂停打印
- `POST /api/v1/resume` - 恢复打印
- `POST /api/v1/stop` - 停止/取消打印
- `GET /api/v1/print_file` - 下载最后一个打印的文件

## 状态字段

`status` 命令返回以下信息：

- **status** - 总体状态（IDLE、RUNNING、PAUSED）
- **printStatus** - 当前是否正在打印
- **progress** - 打印进度（0.0 到 1.0）
- **fileName** - 当前/最后一个打印的文件名
- **currentLine** / **totalLines** - G-code 编程的进度
- **elapsedTime** / **remainingTime** - 已经过去的时间/剩余时间（以秒为单位）
- **nozzleTemperature1** / **nozzleTargetTemperature1** - 喷嘴温度
- **heatedBedTemperature** / **heatedBedTargetTemperature** - 加热床温度
- **x** / **y** / **z** - 当前位置
- **isFilamentOut** - 是否耗材耗尽
- **isEnclosureDoorOpen** - 机箱门状态

## 通知

### 事件检测

- **打印完成** - `status` 等于 "IDLE" 且 `progress` 大于或等于 0.99
- **耗材耗尽** - `isFilamentOut` 为 true
- **机箱门打开** - `isEnclosureDoorOpen` 为 true
- **错误** - 通过 `status` 字段检测错误

## 安全特性

1. **正在打印时的保护** - 打印过程中无法发送文件
2. **确认提示** - 所有可能破坏打印的操作都需要用户确认
3. **状态验证** - 命令执行前会检查打印机状态
4. **明确警告** - 停止命令会显示醒目的警告信息

## 示例

- **检查打印机是否忙碌**  
- **获取剩余时间**  
- **监控温度**  

## 故障排除

- **“机器尚未连接”（401 错误）**：
  - 在进行任何状态查询之前，必须先调用 `/api/v1/connect`。
  - 示例：`curl -X POST "http://192.168.0.32:8080/api/v1/connect?token=YOUR_TOKEN"`
  - Python 脚本会在首次请求时自动处理此情况。
  - 连接会建立会话，直到打印机关闭。
  - 如果使用原始的 curl 命令，请务必先调用 `connect`。

- **连接被拒绝**：
  - 验证打印机 IP 地址：`ping 192.168.0.32`
  - 确保打印机已开启
  - 确保您在同一个网络中。

- **令牌无效**：
  - 重新连接 Luban 应用程序到打印机（在触摸屏上接受新的令牌）
  - 从 Luban 的连接设置中复制新的令牌，并更新 `config.json` 文件。

- **无法发送文件**：
  - 检查打印机是否忙碌：`python3 scripts/snapmaker.py status`
  - 等待当前打印任务完成
  - 仅在绝对必要时使用 `--force`。

## 参考资料

- [Snapmaker 论坛：自动启动指南](https://forum.snapmaker.com/t/guide-automatic-start-via-drag-drop/29177)
- [Snapmaker 论坛：API 文档](https://forum.snapmaker.com/t/documentation-of-the-web-api/20976/16)

## 依赖项

- Python 3.6+
- `requests` 库（安装方法：`pip3 install requests`

## 许可证

本技能属于 OpenClaw 技能集合的一部分。