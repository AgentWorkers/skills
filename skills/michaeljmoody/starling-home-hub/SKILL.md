---
name: starling-home-hub
description: 通过 Starling Home Hub 的本地 REST API 来控制 Nest 和 Google Home 智能家居设备。支持的功能包括：恒温器、摄像头、Nest Protect 安全设备、Nest × Yale 门锁、温度传感器、家庭/外出模式控制以及 Nest 天气服务。使用此功能可以管理 Nest/Google Home 设备，例如读取设备状态、设置温度、获取摄像头截图、锁门/开门、检查烟雾/一氧化碳报警信息，以及切换家庭/外出模式。
homepage: https://starlinghome.io
env:
  - name: STARLING_HUB_IP
    required: true
    secret: false
    description: Local IP address of your Starling Home Hub (e.g. 192.168.1.151)
  - name: STARLING_API_KEY
    required: true
    secret: true
    description: API key from the Starling Home Hub app (Developer Connect section)
---

# Starling Home Hub（Nest/Google Home）

> **这是一个社区技能工具，与Starling LLC、Google、Nest或Apple无关，也未得到它们的官方支持。** Nest是Google LLC的注册商标。Starling Home Hub是Starling LLC的产品。使用此技能需要一个运行在8.0及以上版本固件上的[Starling Home Hub](https://starlinghome.io)，并且必须启用了Developer Connect API。

## 概述

通过Starling Home Hub的Developer Connect（SDC）本地REST API，可以使用`starling.sh`脚本来控制Nest智能家居设备。

## 所需环境变量

| 变量          | 是否必需 | 是否为敏感信息 | 说明                          |
|------------------|---------|------------|--------------------------------------|
| `STARLING_HUB_IP`     | 是        | 否          | 你的Starling Home Hub的本地IP地址（例如`192.168.1.151`）     |
| `STARLING_API_KEY`    | 是        | 是          | 在Starling Home Hub应用程序（Developer Connect部分）中生成的API密钥 |

## 设置

请设置以下环境变量（切勿在脚本中直接硬编码密钥）：

```bash
export STARLING_HUB_IP="192.168.1.xxx"
export STARLING_API_KEY="your-api-key"     # From Starling Home Hub app
```

该脚本位于：`scripts/starling.sh`

可选参数：`--http`（降级为HTTP协议，不推荐使用），`--raw`（跳过jq格式化）

**默认使用HTTPS协议。** 除非指定了`--http`，否则脚本会使用端口3443。

## 安全性

### API密钥管理
- **始终使用`STARLING_API_KEY`环境变量** —— 绝不要通过`--key`参数传递密钥（该参数会在`ps`输出中显示）
- **切勿将密钥存储在脚本、SKILL.md文件或版本控制文件中**
- 使用权限受限的`.env`文件来存储密钥：`chmod 600 .env`
- 对于生产环境或自动化设置，可以考虑使用密钥管理工具

### 最小权限原则
- 在Starling Home Hub应用程序中创建具有最小权限要求的API密钥
- 除非需要设置设备属性或访问摄像头流，否则使用**只读权限的密钥**
- 如果可能的话，为不同的自动化任务创建不同的密钥

### TLS证书验证
- 默认使用HTTPS协议，但由于Starling Home Hub使用自签名证书，因此脚本使用了`curl -k`命令（跳过证书验证）
- 在**受信任的本地网络**中这是可以接受的，但在不受信任的网络中会增加中间人攻击的风险
- 如果需要固定设备的证书，请使用`starling.sh --cacert /path/to/hub-cert.pem status`命令
- 当提供了`--cacert`参数时，`-k`参数将不会被使用，此时会进行完整的证书验证

### URL中的API密钥
- Starling Developer Connect API要求将API密钥作为URL查询参数传递（格式为`?key=...`） —— 这是API的设计要求，并非该技能工具的可选设置
- URL查询参数会出现在访问日志和浏览器历史记录中，但由于该脚本仅在本机使用（没有中间代理/内容分发网络），因此可以降低风险
- 在本地网络中传输密钥时，始终使用HTTPS进行加密

### 网络安全
- Starling API的设计仅限于**本地网络**使用，不会暴露到云端
- **切勿将端口3080或3443映射到互联网**
- 始终使用HTTPS（默认设置）以防止本地网络中的密钥和设备数据被窃取

### 快照处理
- 摄像头快照包含敏感图像 —— 不要将快照文件存储在可被公众访问的位置
- 脚本会自动将快照文件的权限设置为`chmod 600`（仅允许所有者访问）
- 当不再需要快照文件时，会自动清理它们

## 最佳实践

### 先检查状态
在调用设备接口之前，请先确认设备是否已准备好：
```bash
scripts/starling.sh status
```
在继续操作之前，请确保`apiReady: true`且`connectedToNest: true`。

### 遵守速率限制
这些限制由Nest云端强制执行：
- **POST**（设置设备属性）：每个设备每秒最多一次请求
- **快照**：每个摄像头每10秒最多一次请求
- **GET**（读取设备属性/设备列表）：没有云端速率限制（使用本地缓存）

### 等幂操作
可以安全地重试操作而不会产生副作用：
- 所有的GET操作（获取状态、设备信息、设备详情、获取快照）
- 使用相同值的SET操作（例如，将温度设置为22°C）
- `stream-extend`操作（仅重置保持活动状态的计时器）

**非等幂操作：** `stream-start`操作（每次都会创建新的数据流）

### 错误处理
脚本会提供详细的错误信息：
- **401**：检查API密钥和权限 —— 错误信息中不会显示密钥
- **404**：验证设备ID和属性名称
- **400**：检查参数的值和类型

## 常见工作流程

### 列出所有设备
```bash
scripts/starling.sh devices
```

### 读取设备属性
```bash
scripts/starling.sh device <id>          # All properties
scripts/starling.sh get <id> <property>  # Single property
```

### 设置设备属性
```bash
scripts/starling.sh set <id> key=value [key=value...]
```

### 拍摄摄像头快照
```bash
scripts/starling.sh snapshot <id> --output photo.jpg --width 1280
```

### 摄像头流媒体（WebRTC）
```bash
scripts/starling.sh stream-start <id> <base64-sdp-offer>
scripts/starling.sh stream-extend <id> <stream-id>   # Every 60s
scripts/starling.sh stream-stop <id> <stream-id>
```

## 常见任务

**将恒温器温度设置为22°C：**
```bash
scripts/starling.sh set <thermostat-id> targetTemperature=22
```

**设置暖通空调模式：**
```bash
scripts/starling.sh set <thermostat-id> hvacMode=heat
```

**检查摄像头是否有运动：**
```bash
scripts/starling.sh get <camera-id> motionDetected
```

**锁门/开门：**
```bash
scripts/starling.sh set <lock-id> targetState=locked
```

**获取摄像头快照：**
```bash
scripts/starling.sh snapshot <camera-id> --output front-door.jpg
```

**检查烟雾/一氧化碳检测状态：**
```bash
scripts/starling.sh get <protect-id> smokeDetected
scripts/starling.sh get <protect-id> coDetected
```

**设置家庭/外出模式：**
```bash
scripts/starling.sh set <home-away-id> homeState=away
```

## API参考

有关设备属性的完整信息、可写属性、错误代码和端点文档，请参阅`references/api-reference.md`。