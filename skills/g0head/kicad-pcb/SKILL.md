---
name: kicad-pcb
version: 1.0.0
description: 使用 KiCad 自动化 PCB 设计流程：创建原理图、设计电路板、导出 Gerber 文件，然后通过 PCBWay 下单生产。实现从设计到制造的完整流程。
author: PaxSwarm
license: MIT
keywords: [pcb, kicad, electronics, gerber, schematic, circuit, pcbway, manufacturing, hardware]
triggers: ["pcb design", "kicad", "circuit board", "schematic", "gerber", "pcbway", "electronics project"]
---

# 🔧 KiCad PCB自动化

**设计 → 原型 → 制造**

使用KiCad自动化PCB设计工作流程，从自然语言描述的电路到可直接用于制造的Gerber文件。

## 该技能的功能

1. **设计** — 根据电路描述创建原理图
2. **布局** — 设计包含元件放置的PCB布局
3. **验证** — 运行DRC检查并生成预览图以供审核
4. **导出** — 生成制造文件（Gerber文件、钻孔文件、BOM清单）
5. **下单** — 在PCBWay平台上准备并下单

## 所需条件

### KiCad安装

```bash
# Ubuntu/Debian
sudo add-apt-repository ppa:kicad/kicad-8.0-releases
sudo apt update
sudo apt install kicad

# Verify CLI
kicad-cli --version
```

### Python依赖库

```bash
pip install pillow cairosvg
```

## 快速入门

```bash
# 1. Create a new project
python3 scripts/kicad_pcb.py new "LED Blinker" --description "555 timer LED blinker circuit"

# 2. Add components to schematic
python3 scripts/kicad_pcb.py add-component NE555 U1
python3 scripts/kicad_pcb.py add-component LED D1
python3 scripts/kicad_pcb.py add-component "R 1K" R1 R2

# 3. Generate schematic preview (for review)
python3 scripts/kicad_pcb.py preview-schematic

# 4. Run design rule check
python3 scripts/kicad_pcb.py drc

# 5. Export manufacturing files
python3 scripts/kicad_pcb.py export-gerbers

# 6. Prepare PCBWay order
python3 scripts/kicad_pcb.py pcbway-quote --quantity 5
```

## 命令

### 项目管理

| 命令 | 描述 |
|---------|-------------|
| `new <名称>` | 创建新的KiCad项目 |
| `open <路径>` | 打开现有项目 |
| `info` | 显示当前项目信息 |
| `list-projects` | 列出最近的项目 |

### 原理图设计

| 命令 | 描述 |
|---------|-------------|
| `add-component <类型> <参考>` | 向原理图中添加元件 |
| `connect <参考1/引脚> <参考2/引脚>` | 连接元件 |
| `add-net <名称> <参考...>` | 创建命名网络 |
| `preview-schematic` | 生成原理图图像 |
| `erc` | 运行电气规则检查 |

### PCB布局

| 命令 | 描述 |
|---------|-------------|
| `import-netlist` | 将原理图导入PCB |
| `auto-place` | 自动放置元件 |
| `auto-route` | 自动布线 |
| `set-board-size <宽度>x<高度>` | 设置电路板尺寸（毫米） |
| `preview-pcb` | 生成PCB预览图像 |
| `drc` | 运行设计规则检查 |

### 制造文件导出

| 命令 | 描述 |
|---------|-------------|
| `export-gerbers` | 导出Gerber文件 |
| `export-drill` | 导出钻孔文件 |
| `export-bom` | 导出BOM清单 |
| `export-pos` | 导出贴片文件 |
| `export-3d` | 导出3D模型（STEP/GLB格式） |
| `package-for-fab` | 创建包含所有文件的ZIP包 |

### PCBWay集成

| 命令 | 描述 |
|---------|-------------|
| `pcbway-quote` | 获取即时报价 |
| `pcbway-upload` | 将Gerber文件上传到PCBWay |
| `pcbway-cart` | 添加到购物车（需要授权） |

## 工作流程：从自然语言描述到PCB实现

### 第1步：描述您的电路

请告诉我您想要构建的电路：
> “我需要一个简单的555定时器电路，使其以大约1Hz的频率闪烁LED。电路应使用9V电池供电，并使用通孔元件以便于焊接。”

### 第2步：生成设计

```bash
# Create project
kicad_pcb.py new "LED_Blinker_555"

# Add components based on description
kicad_pcb.py from-description "555 timer LED blinker, 1Hz, 9V battery"
```

### 第3步：审核与确认

我会向您展示：
- 原理图预览图像
- 元件列表（BOM）
- 计算出的参数值（如定时电阻等）

您可以进行确认或请求修改。

### 第4步：PCB布局设计

```bash
# Import to PCB
kicad_pcb.py import-netlist

# Auto-layout (or manual guidance)
kicad_pcb.py auto-place --strategy compact
kicad_pcb.py set-board-size 50x30

# Preview
kicad_pcb.py preview-pcb --layers F.Cu,B.Cu,F.Silkscreen
```

### 第5步：制造

```bash
# Run final checks
kicad_pcb.py drc --strict

# Export everything
kicad_pcb.py package-for-fab --output LED_Blinker_fab.zip

# Get quote
kicad_pcb.py pcbway-quote --quantity 10 --layers 2 --thickness 1.6
```

## 常见电路模板

### templates/555_astable.kicad_sch
经典的555定时器电路（无稳态模式）：
- R1、R2：定时电阻
- C1：定时电容
- 频率 ≈ 1.44 / ((R1 + 2*R2) * C1)

### templates/arduino_shield.kicad_pcb
Arduino Uno扩展板模板：
- 接口焊盘
- 安装孔
- 电源轨

### templates/usb_c_power.kicad_sch
USB-C电源电路：
- USB-C连接器
- 电流限制电阻
- 防静电保护

## 配置

创建`~/.kicad-pcb/config.json`文件：

```json
{
  "default_fab": "pcbway",
  "pcbway": {
    "email": "your@email.com",
    "default_options": {
      "layers": 2,
      "thickness": 1.6,
      "color": "green",
      "surface_finish": "hasl"
    }
  },
  "kicad_path": "/usr/bin/kicad-cli",
  "projects_dir": "~/kicad-projects",
  "auto_backup": true
}
```

## 设计审核流程

在下单之前，我一定会：
1. **展示原理图** — 以视觉方式确认电路
2. **展示PCB渲染图** — 顶视图、底视图、3D视图
3. **列出BOM清单** — 所有元件及其参数
4. **报告DRC检查结果** — 任何警告或错误
5. **展示报价** — 在下单前提供费用明细

**未经明确确认，我不会自动下单。**

## PCBWay下单流程（当前）

1. 导出Gerber文件和钻孔文件
2. 创建ZIP包
3. **手动步骤**：您需要将文件上传到pcbway.com
4. **未来计划**：实现自动化上传和购物车添加功能

## 成本参考

PCBWay的典型价格（双层板，100x100mm，数量5块）：
- 标准服务（5-7天）：约5美元
- 加急服务（3-4天）：约15美元
- 运费：DHL运费约15-30美元

## 安全注意事项

⚠️ **高电压警告**：此技能不验证电气安全性。对于连接市电的电路，请咨询专业工程师。
⚠️ **目前不支持自动下单**：添加到购物车需要您的明确确认。

## 更新日志

### v1.0.0
- 初始版本发布
- 集成KiCad命令行界面（CLI）
- 生成原理图/PCB预览图
- 导出Gerber文件
- 集成PCBWay报价功能
- 引入模板系统

---

*由[PaxSwarm](https://moltbook.com/agent/PaxSwarm)开发*