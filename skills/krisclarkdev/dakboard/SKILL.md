---
name: dakboard
description: 管理 DAKboard 的屏幕、设备，并推送自定义显示数据。
author: Kristopher Clark
homepage: https://github.com/krisclarkdev/dakboard-skill
files: ["scripts/*"]
metadata:
  clawdbot:
    requires:
      env:
        - DAKBOARD_API_KEY
---
# DAKboard 技能

该技能提供了一个命令行接口，用于与 DAKboard API 进行交互。它支持对设备和屏幕进行全面的管理，并允许推送自定义数据以实现动态显示。

## 设置

在使用此技能之前，您必须将您的 DAKboard API 密钥设置为环境变量。

```bash
export DAKBOARD_API_KEY="your_api_key_here"
```

该技能的主要工具是位于 `scripts/dakboard.py` 的 Python 脚本。

## 可用命令

### 1. 列出设备
检索与您的账户关联的所有 DAKboard 设备（例如 Raspberry Pi）。这有助于获取其他命令所需的 `device_id`。

**用法：**
```bash
python3 scripts/dakboard.py devices
```

### 2. 列出屏幕布局
检索所有可用的屏幕布局（例如 “Big Monthly”、“Two Column”）。这用于获取更改设备显示所需的 `screen_id`。

**用法：**
```bash
python3 scripts/dakboard.py screens
```

### 3. 更新设备屏幕
更改特定设备当前显示的屏幕布局。

**用法：**
```bash
# Usage: update-device <device_id> <screen_id>
python3 scripts/dakboard.py update-device "dev_0c3e1405a961" "scr_709367acf3d4"
```

### 4. 推送指标数据
将一个带有名称的数据点推送到 “DAKboard Metrics” 区块中。这非常适合显示实时数据，如传感器读数或统计信息。

**用法：**
```bash
# Usage: metric <key> <value>
python3 scripts/dakboard.py metric "indoor_temp" "72.5"
```

### 5. 推送完整数据对象
将一个完整的 JSON 对象推送到屏幕上的 “Fetch” 区块中。这用于显示更复杂、结构化的数据。

**用法：**
```bash
# Usage: fetch '<json_string>'
python3 scripts/dakboard.py fetch '{"tasks": ["Buy milk", "Walk the dog"], "priority": "high"}'
```

## 安全性与隐私

### 外部端点
| URL | 发送的数据 | 用途 |
| :--- | :--- | :--- |
| `https://dakboard.com/api/` | API 密钥、设备 ID、屏幕 ID、指标数据 | 用于与 DAKboard API 交互，以列出和更新设备信息，以及将指标数据推送到自定义块中。 |

### 数据处理
仅会将作为技能命令参数提供的数据（例如要在 DAKboard 上显示的消息或指标数据）以及您的 `DAKBOARD_API_KEY` 发送到 `dakboard.com`。不会读取或写入任何本地文件。

### 模型调用说明
该技能设计为由 OpenClaw 代理在用户请求时自动调用。您可以通过禁用此技能来选择不使用自动调用功能。

### 信任声明
使用此技能时，发送的数据仅限于提供的参数，并直接发送到 `dakboard.com`。只有在您信任 DAKboard 并愿意向其展示相关信息的情况下，才请安装此技能。