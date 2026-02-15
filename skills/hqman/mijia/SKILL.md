---
name: mijia
description: **控制小米米家智能家居设备**  
当用户需要控制台灯、智能插座或其他米家设备时，可以使用此技能。支持开关灯、调节亮度、设置色温、切换模式等操作。
invocable: true
---

# 米家智能家居控制

通过 `mijiaAPI` 控制小米米家智能设备。

## 设置

在使用此技能之前，您需要完成以下步骤：

1. 安装依赖项：
```bash
cd /path/to/mijia-skill
uv sync
```

2. 将您的设备 ID 设置为环境变量：
```bash
export MIJIA_LAMP_DID="your_device_id"
```

3. 首次运行时，系统会提示您通过二维码登录小米账户。

## 查找设备 ID

要查找您的设备 ID，请使用 `mijia-api` 库：
```python
from mijiaAPI import mijiaAPI
api = mijiaAPI()
api.login()
devices = api.get_device_list()
for d in devices:
    print(f"{d['name']}: {d['did']}")
```

## 使用方法

技能路径：`~/.clawdbot/skills/mijia`

### 灯具控制命令

```bash
# Navigate to skill directory
cd ~/.claude/skills/mijia

# Check status
uv run python scripts/lamp_cli.py status

# Turn on/off
uv run python scripts/lamp_cli.py on
uv run python scripts/lamp_cli.py off
uv run python scripts/lamp_cli.py toggle

# Adjust brightness (1-100%)
uv run python scripts/lamp_cli.py brightness 50

# Adjust color temperature (2700-6500K)
uv run python scripts/lamp_cli.py temp 4000

# Set mode
uv run python scripts/lamp_cli.py mode reading    # Reading mode
uv run python scripts/lamp_cli.py mode computer   # Computer mode
uv run python scripts/lamp_cli.py mode night      # Night reading
uv run python scripts/lamp_cli.py mode antiblue   # Anti-blue light
uv run python scripts/lamp_cli.py mode work       # Work mode
uv run python scripts/lamp_cli.py mode candle     # Candle effect
uv run python scripts/lamp_cli.py mode twinkle    # Twinkle alert
```

## 自然语言理解

当用户说出以下指令时，系统会执行相应的命令：

| 用户指令 | 命令             |
|-----------|-------------------|
| 打开灯       | `scripts/lamp_cli.py on`       |
| 关闭灯       | `scripts/lamp_cli.py off`       |
| 切换灯的状态   | `scripts/lamp_cli.py toggle`     |
| 调亮灯光     | 先检查状态，然后增加 20-30% 的亮度 |
| 调暗灯光     | 先检查状态，然后减少 20-30% 的亮度 |
| 最大亮度     | `scripts/lamp_cli.py brightness 100`     |
| 最小亮度     | `scripts/lamp_cli.py brightness 1`     |
| 温暖光       | `scripts/lamp_cli.py temp 2700`     |
| 冷白光       | `scripts/lamp_cli.py temp 6500`     |
| 读书模式     | `scripts/lamp_cli.py mode reading`    |
| 电脑模式     | `scripts/lamp_cli.py mode computer`    |
| 夜间模式     | `scripts/lamp_cli.py mode night`     |
| 查看灯的状态   | `scripts/lamp_cli.py status`     |

## 执行前准备

1. 导航到技能目录：`cd ~/.clawdbot/skills/mijia`
2. 确保 `MIJIA_LAMP_DID` 环境变量已设置
3. 使用 `uv` 命令运行脚本：`uv run python scripts/lamp_cli.py <命令>`
4. 执行完成后向用户报告结果