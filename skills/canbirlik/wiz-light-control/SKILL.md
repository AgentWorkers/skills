---
name: wiz-light-control
description: 通过本地 WiFi 控制 Wiz 智能灯泡（开关、调节 RGB 颜色、切换到迪斯科模式）。
author: "@canbirlik"
emoji: "💡"
platforms:
  - darwin
  - linux
  - win32
dependencies:
  python:
    - pywizlight
---
# Wiz Light Control Skill

此技能允许代理控制本地网络中的Wiz智能灯泡。

⚠️ **重要配置说明：**  
示例中使用的IP地址`192.168.1.109`仅为占位符。在运行命令之前，**必须**先找到网络中Wiz灯泡的实际本地IP地址。

## 🛠️ 安装与设置（请先阅读）

**在首次运行脚本之前，****必须先设置Python环境。**  
代理应检查`venv`是否存在。如果不存在，请自动运行以下设置命令：

```bash
# 1. 创建虚拟环境并安装依赖项
python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt
```

## 工具与使用方法

### `wiz.py`  
用于与灯泡交互的主要脚本。

**参数：**  
- `--ip`：灯泡的IP地址（必需）  
- `--action`：要执行的命令。可选值：`on`（打开）、`off`（关闭）、`color`（改变颜色）、`disco`（切换到迪斯科模式）  
- `--r`、`--g`、`--b`：红色、绿色、蓝色的数值（0-255）（用于`color`命令）  
- `--duration`：持续时间（以秒为单位）（用于`disco`命令）

**示例命令：**  
- “将我房间的灯泡切换到迪斯科模式，持续30秒。”  
- “关闭灯泡。”  
- “将灯泡的颜色设置为红色。”

**执行示例：**  
```bash
# 1. 启动迪斯科模式（请先检查IP地址！）
python wiz.py --ip 192.168.1.109 --action disco --duration 60

# 2. 关闭灯泡
python wiz.py --ip 192.168.1.109 --action off

# 3. 打开灯泡
python wiz.py --ip 192.168.1.109 --action on

# 4. 设置特定颜色（例如：红色）
python wiz.py --ip 192.168.1.109 --action color --r 255 --g 0 --b 0
```