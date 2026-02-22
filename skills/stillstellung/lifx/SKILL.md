---
name: lifx
description: "通过自然语言控制 LIFX 智能灯泡：可以切换灯泡状态、设置颜色/亮度、激活预设场景，以及在多区域设备上创建渐变效果。"
homepage: https://github.com/Stillstellung/via-clara-claw
metadata:
  openclaw:
    emoji: "💡"
    requires:
      env: ["LIFX_TOKEN"]
---
# LIFX灯光控制

通过LIFX HTTP API，使用自然语言来控制LIFX智能灯泡。

## 参考资料

- `lifx-api.sh` — 用于所有LIFX API调用的Bash封装脚本
- `scene-status.py` — 场景匹配与活跃状态检测
- `setup.sh` — 设备发现与技能配置

## 配置

设置您的LIFX API令牌（可在https://cloud.lifx.com/settings获取）：

```bash
bash setup.sh <your-token>
```

该脚本会检测您的灯泡、分组和场景信息，然后根据您的设备配置生成一个个性化的`SKILL.md`文件。

## 设备信息

> **运行 `bash setup.sh <您的令牌>` 以填写本节中的灯泡、房间和场景信息。**
> 设置脚本会查询LIFX API，并根据您的设备信息更新此文件。

位置：*(未配置)*

### 房间和灯泡

*(由setup.sh填充)*

### 场景

*(由setup.sh填充)*

### 多区域设备

*(由setup.sh填充)*

## 如何控制灯泡

### 检测灯泡

```bash
bash lifx-api.sh discover
```

按房间显示所有灯泡的信息，包括电源状态、颜色和亮度。

### 开/关灯泡

```bash
bash lifx-api.sh toggle <selector>
```

选择方式：
- 单个灯泡：`id:<灯泡_id>`
- 组/房间：`group_id:<组_id>`
- 所有灯泡：`all`

### 设置灯泡状态（颜色、亮度、电源）

```bash
bash lifx-api.sh state <selector> '{"power":"on","color":"blue","brightness":0.75,"duration":1.0}'
```

颜色格式：
- 常见名称：`red`（红色）、`blue`（蓝色）、`green`（绿色）、`white`（白色）、`warm white`（暖白）、`purple`（紫色）、`orange`（橙色）
- 十六进制颜色代码：`#ff6b35`
- 开尔文温度：`kelvin:2700`（暖光）至 `kelvin:6500`（冷日光）
- HSB颜色模型：`hue:240 saturation:1.0`

**设置颜色时必须包含 `"power":"on"` 和亮度值**，否则亮度为0的灯泡将不可见。

### 激活场景

```bash
bash lifx-api.sh scene <scene_uuid>
```

### 切换房间

```bash
bash lifx-api.sh group-toggle <group_id>
```

### 多区域渐变（Beam/Strip设备）

多区域设备支持单独控制各个区域。通过设置不同的区域范围来实现渐变效果：

```bash
bash lifx-api.sh state 'id:<light_id>|0-4' '{"power":"on","color":"purple","brightness":1.0,"duration":1.0}'
bash lifx-api.sh state 'id:<light_id>|5-9' '{"power":"on","color":"red","brightness":1.0,"duration":1.0}'
```

区域选择器中的管道符号（`|`）会自动被脚本转换为URL编码格式。

### 检查场景状态

```bash
python3 scene-status.py all    # Show all active scenes
python3 scene-status.py check <uuid>  # Check specific scene
```

### 列出当前灯泡状态

```bash
bash lifx-api.sh list    # Full JSON
bash lifx-api.sh groups  # Summary by room
```

## 行为规范

- 当用户提及房间名称时，系统会从设备信息中匹配相应的组ID。
- 设置颜色时，默认亮度为1.0（100%），除非用户另有指定。
- 过渡效果默认持续1.0秒。
- 对于“关闭”命令，使用 `{"power":"off"}` — 避免产生混淆（切换操作可能引起误解）。
- 对于“打开”命令，使用 `{"power":"on","brightness":1.0}` 以确保灯泡可见。
- 当用户询问当前开启的灯泡或场景时，可以使用`scene-status`工具或`discover`命令获取信息。
- 在反馈结果时请使用自然语言：例如“已完成，卧室现在显示为75%的蓝色”，而不是“API返回207”。