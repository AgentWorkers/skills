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

通过LIFX HTTP API，使用自然语言控制LIFX智能灯泡。

## 参考资料

- `lifx-api.sh` — 用于所有LIFX API调用的Bash脚本包装器
- `scene-status.py` — 场景匹配和活动检测功能
- `setup.sh` — 设备发现和技能配置工具

## 配置

设置您的LIFX API令牌（可在https://cloud.lifx.com/settings获取）：

```bash
bash setup.sh <your-token>
```

该脚本会自动发现您的灯泡、分组和场景，并根据您的设备信息生成一个个性化的`SKILL.md`文件。

## 设备信息

位置：**Maple Lane** — 共24个灯泡，分布在11个房间中，支持17个场景，包含1个多区域设备。

### 房间与灯泡

| 房间 | 分组ID | 灯泡 |
|------|----------|--------|
| 地下室 | `486968148dc96708c4010c4d1ad6f3ed` | 地下室C区前部1号灯、地下室C区后部1号灯、地下室C区后部2号灯、地下室C区前部2号灯 |
| 卧室 | `a68393c4103078091d0cb5cea4fd465b` | 卧室角落灯、风扇1、风扇3、风扇2、床头灯 |
| 入口 | `900c5c64f69c820f2877df19dc5e3ca1` | 入口天花板2号灯、入口天花板1号灯 |
| 车库 | `2492b04f914e7980fb0bddf3555cd851` | 车库 |
| 厨房 | `3a51cbe016ce411745f6fb5984cd1373` | 水槽灯 |
| 客厅 | `db5356b4e4166c73c6a7da4b9742a5ce` | 银色吊灯、背景灯 |
| 主浴室 | `e8eaecec90582c1b390267bce3401a73` | 浴室1号淋浴灯、浴室2号淋浴灯 |
| 办公室 | `4033b4e975c7fba7ffbbb32de0e3da3c` | 办公室角落灯 |
| 门廊 | `55bf10fe4f5617b1d076cb4cab00446d` | 门廊灯 |
| 阅读室 | `8e2fabffaa3b12212bb8a5c94a9f28eb` | 阅读室书架灯、阅读室落地灯、阅读室射灯（支持多区域控制） |
| 楼梯间 | `e6040214e4199c2c3e1366ec08741370` | 上层走廊2号灯、上层走廊1号灯 |

### 场景

| 场景 | UUID |
|-------|------|
| 地下室电影模式 | `eace4433-ce88-46d3-a037-d97f97542c3f` |
| 地下室中性光 | `715de535-2fd7-4470-9632-abda96029ce4` |
| 卧室浴室渐变光 | `2ce39722-287c-49f9-bee0-6ee7ae8f616b` |
| 卧室舒适光 | `b5193a0c-d31f-44de-afd8-5075440b58f3` |
| 卧室中性光 | `0cbc6f4e-8bc0-4e39-8372-c6e9237e874d` |
| 卧室睡眠光 | `e471b043-70c4-48ec-b2c0-6828ecc18289` |
| 走廊中性光 | `251d43fc-f3d1-4dc5-a218-7f0ca81d83ca` |
| 全屋睡眠模式 | `865a609b-5e5d-4cfd-b362-f6bc0ff29cfe` |
| 全屋星尘光 | `3e8c665f-adef-4042-8fd8-ab70f134ad2f` |
| 客厅蓝色夜晚光 | `3a4b1b2c-cd69-41ae-8c43-cc54bc97bf08` |
| 客厅日光色灯光 | `f27ad3d6-2ee6-4d00-851c-6a716c9f6b0b` |
| 客厅中性光 | `801c2f77-1b2c-4cc3-9942-7a3b315fe63e` |
| 阅读室游戏模式 | `1c0d09d5-f550-4be3-b46a-01f30798b3eb` |
| 阅读室海洋光 | `4b1989fc-7001-4de8-a579-c485d09df780` |
| 阅读室红色光 | `c7abe95f-5489-4f7c-a7fb-3f9b9278cac6` |
| 阅读室白色光 | `77d3c13d-bb28-409f-92e1-b97a2d3da7be` |
| 洗浴室动感光 | `e20e70fe-b4d1-46fc-b565-30f5b24e586b` |

### 多区域设备

- **阅读室射灯**（`id:d073d5d0a7d9`） — 支持基于区域的渐变效果

## 如何控制灯光

### 发现灯泡

```bash
bash lifx-api.sh discover
```

按房间显示所有灯泡的信息，包括电源状态、颜色和亮度。

### 开/关灯泡

```bash
bash lifx-api.sh toggle <selector>
```

选择方式：
- 单个灯泡：`id:<灯泡ID>`
- 分组/房间：`group_id:<分组ID>`
- 所有灯泡：`all`

### 设置灯泡状态（颜色、亮度、电源）

```bash
bash lifx-api.sh state <selector> '{"power":"on","color":"blue","brightness":0.75,"duration":1.0}'
```

颜色格式：
- 常见名称：`red`（红色）、`blue`（蓝色）、`green`（绿色）、`white`（白色）、`warm white`（暖白色）、`purple`（紫色）、`orange`（橙色）
- 十六进制颜色代码：`#ff6b35`
- 开尔文温度：`kelvin:2700`（暖色调）至 `kelvin:6500`（冷色调）
- HSB颜色模型：`hue:240 saturation:1.0`

**设置颜色时必须包含`"power":"on"`和亮度值**，否则亮度为0的灯泡将不可见。

### 激活场景

```bash
bash lifx-api.sh scene <scene_uuid>
```

### 切换房间灯光

```bash
bash lifx-api.sh group-toggle <group_id>
```

### 多区域渐变效果（适用于射灯/条形灯）

多区域设备支持单独控制每个区域。通过设置不同的区域范围来实现渐变效果：

```bash
bash lifx-api.sh state 'id:<light_id>|0-4' '{"power":"on","color":"purple","brightness":1.0,"duration":1.0}'
bash lifx-api.sh state 'id:<light_id>|5-9' '{"power":"on","color":"red","brightness":1.0,"duration":1.0}'
```

区域选择器中的“|”符号会自动被脚本转换为URL编码。

### 检查场景状态

```bash
python3 scene-status.py all    # Show all active scenes
python3 scene-status.py check <uuid>  # Check specific scene
```

### 列出当前灯光状态

```bash
bash lifx-api.sh list    # Full JSON
bash lifx-api.sh groups  # Summary by room
```

## 行为规范

- 当用户提及房间名称时，系统会从上述设备信息中匹配相应的分组ID。
- 设置颜色时，默认亮度为1.0（100%），除非用户另有指定。
- 过渡效果默认持续1.0秒。
- 对于“关闭”命令，使用`{"power":"off"`；避免使用简单的开关操作（因为可能引起混淆）。
- 对于“打开”命令，使用`{"power":"on","brightness":1.0}`以确保灯泡可见。
- 当用户询问当前开启的灯光或活动场景时，建议使用`scene-status`工具或`discover`命令获取信息。
- 在反馈结果时使用自然语言描述，例如：“已成功，卧室灯光现在设置为蓝色，亮度为75%”。