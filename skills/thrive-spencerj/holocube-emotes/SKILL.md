---
name: holocube-emotes
description: 将 GeekMagic 全息立方体显示器作为 AI 表情系统进行控制。使用 Gemini 工具生成全息精灵图像（sprite kits），将其上传到设备中，并根据代理的状态（空闲、工作、出错等）切换相应的表情。适用于用户拥有 GeekMagic 全息立方体（如 HelloCubic-Lite 或类似产品）的情况，希望他们的 AI 助手能够根据对话内容实时展示相应的面部表情。
---

# Holocube表情

将GeekMagic全息立方体设置为你的AI的“面孔”。生成全息角色精灵图像，上传到设备上，然后根据代理/会话的状态实时切换表情。

## 首次设置

### 0. 查找设备

自动检测网络中的全息立方体：

```bash
python3 scripts/holocube.py --discover
```

输出：`FOUND: 192.168.0.245 — HelloCubic-Lite V7.0.22`

如果检测失败，请在设备屏幕或路由器的客户端列表中查找设备的IP地址。

### 1. 生成精灵图像

使用`GEMINI_API_KEY`和`nano-banana-pro`技能生成完整的表情精灵包：

```bash
python3 scripts/generate_sprites.py --output-dir ./sprites
```

自定义角色：
```bash
python3 scripts/generate_sprites.py --output-dir ./sprites \
  --character "A glowing holographic cat floating in pure black void. Neon purple wireframe style."
```

这将生成7种表情（中立、快乐、思考、惊讶、担忧、大笑、睡眠），分别以240x240像素的静态JPG和动画GIF格式生成。

### 2. 上传到设备

```bash
python3 scripts/setup_device.py --sprites-dir ./sprites --clear --backup-dir ./backup
```

参数说明：
- `--clear`：删除现有图像（推荐使用——设备存储空间约为3MB）
- `--backup-dir`：在删除前备份现有文件
- `--ip`：如果未提供，则自动检测设备的IP地址；否则可手动指定

### 3. 配置WORKSPACE.md文件

将全息立方体的IP地址和表情映射添加到WORKSPACE.md文件中以供参考。详情请参见references/tools-example.md。

## 日常使用

### 直接设置表情

```bash
python3 scripts/holocube.py happy
python3 scripts/holocube.py thinking --static   # Use JPG instead of GIF
```

### 根据代理状态设置表情

```bash
python3 scripts/holocube.py working    # → thinking
python3 scripts/holocube.py complete   # → happy
python3 scripts/holocube.py error      # → concerned
python3 scripts/holocube.py opus       # → thinking (heavy model)
python3 scripts/holocube.py haiku      # → neutral (light model)
```

### 根据时间自动选择表情

```bash
python3 scripts/holocube.py --auto
```

- 晚上11点至早上7点 → 睡眠
- 早上7点至9点 → 快乐
- 其他时间 → 中立

### 检查设备状态

```bash
python3 scripts/holocube.py --status
python3 scripts/holocube.py --list
```

## 与HEARTBEAT.md集成

将上述设置添加到HEARTBEAT.md文件中，以实现表情的自动管理：

```markdown
## Holocube Emote Check
- Run `python3 scripts/holocube.py --auto` to set time-appropriate emote
```

## 何时设置表情

在以下情况下使用相应表情：

| 情境 | 命令 | 表情 |
|---|---|---|
| 空闲，等待输入 | `neutral` | 🤖 |
| 处理任务 | `thinking` 或 `working` | 🔧 |
| 任务完成 | `happy` 或 `complete` | 😊 |
| 发生错误 | `error`（→ surprised） | 😮 |
| 有趣时刻 | `laughing` 或 `funny` | 😂 |
| 非预期输入 | `surprised` 或 `unexpected` | 😮 |
| 夜间/不活跃状态 | `sleeping` 或 `night` | 😴 |
| 生成子代理 | `spawning`（→ thinking） | 🔧 |
| 根据需求自定义表情 | `custom` | ✨ |

## 自定义表情

设备上有一个预留的文件`adam-custom.gif`，可以随时覆盖它以使用自定义动画。生成GIF文件并上传为`adam-custom.gif`，然后运行`python3 holocube.py custom`命令。完成后可恢复为默认表情。

## 设备注意事项

- **型号：** GeekMagic HelloCubic-Lite（240x240像素玻璃显示屏）
- **格式：** GIF（动画）或JFIF/JPEG。建议使用Pillow处理JPEG格式（因为ffmpeg无法解析JFIF文件头）。
- **存储空间：** 总存储空间约为3MB。6个动画GIF占约1.5MB，剩余约500KB用于自定义表情。
- **艺术风格：** 使用深色/黑色背景，使玻璃效果更加明显。建议使用发光、全息或霓虹风格的元素。
- **⚠️ **严禁发送`/set?reset=1`命令**——该命令会导致设备恢复出厂设置，并清除WiFi配置。**

## 所需软件/环境

- 本地网络中的GeekMagic HelloCubic-Lite（或兼容设备）
- 安装了Python 3及Pillow库（`pip install Pillow`）
- 拥有`nano-banana-pro`技能及`GEMINI_API_KEY`（仅用于生成精灵图像）
- 安装`uv`库（`brew install uv`）（仅用于生成精灵图像）