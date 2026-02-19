---
name: control4-home
description: 通过 `pyControl4` 使用本地的 Python 封装库来控制 Control4 智能家居系统（包括灯光、继电器以及房间内的媒体设备）。适用于用户需要控制设备、调整设备参数、切换继电器状态、更换房间媒体源或查看 Control4 设备映射信息的情况。
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["python3"] },
        "install":
          [
            {
              "id": "pycontrol4",
              "kind": "python",
              "packages": ["pyControl4==1.6.0"],
              "venv": ".venv-control4",
              "label": "Install pyControl4 in local virtualenv"
            }
          ]
      }
  }
---
# Control4 主页

请使用 `scripts/` 目录中的脚本来本地控制 Control4。

## 文件

- `scripts/control4_cli.py` — 用于执行 Control4 的低级命令（发现设备/列表设备/调整灯光/切换继电器/控制房间设备/媒体设备以及通用方法调用）
- `scripts/nl_control4.py` — 用于处理自然语言指令的脚本（控制灯光、继电器、房间媒体设备、静音/取消静音、调节音量）
- `scripts/device_map.example.json` — 用于将设备名称映射到 Control4 设备 ID 的别名模板

## 设置

1. 创建一个 Python 虚拟环境（示例）：
   - `python3 -m venv .venv-control4`
2. 安装依赖项：
   - `.venv-control4/bin/pip install pyControl4`
3. 创建 `scripts/.env` 文件（或通过环境变量设置）：
   - `CONTROL4_USERNAME`
   - `CONTROL4_PASSWORD`
   - `CONTROL4_CONTROLLER_IP`
   - `CONTROL4_controller_NAME`（如果只有一个控制器，则可选）
4. 复制并自定义设备别名映射文件：
   - `cp scripts/device_map.example.json scripts/device_map.json`

## 常用命令

- 发现控制器/账户：
  - `.venv-control4/bin/python scripts/control4_cli.py discover`
- 列出设备：
  - `.venv-control4/bin/python scripts/control4_cli.py list-items --compact`
- 调节灯光亮度：
  - `.venv-control4/bin/python scripts/control4_cli.py light-set --id 229 --level 40`
- 切换继电器状态：
  - `.venv-control4/bin/python scripts/control4_cli.py relay-toggle --id 571`
- 使用自然语言指令：
  - `.venv-control4/bin/python scripts/nl_control4.py "关闭厨房的灯光"`
  - `.venv-control4/bin/python scripts/nl_control4.py "在主卧室观看苹果电视"`
  - `.venv-control4/bin/python scripts/nl_control4.py "将主卧室的声音设置为静音"`
- 列出某个设备的所有可用方法：
  - `.venv-control4/bin/python scripts/control4_cli.py methods --entity room --id 45`
- 调用任何可用的 `pyControl4` 方法：
  - `.venv-control4/bin/python scripts/control4_cli.py call --entity climate --id 752 --method getCurrentTemperatureC`
  - `.venv-control4/bin/python scripts/control4_cli.py call --entity light --id 229 --method rampToLevel --args-json "[25,1000]`
- 部分敏感方法需要明确授权：
    - `.venv-control4/bin/python scripts/control4_cli.py call --entity security-panel --id <id> --method setArm --allow-sensitive`

## 安全注意事项

- 将门禁/报警继电器相关的操作视为敏感操作。
- 在执行高风险命令前，请确认用户的意图是否明确。
- 请勿将敏感信息（如密码/令牌）保存到 Git 仓库中。