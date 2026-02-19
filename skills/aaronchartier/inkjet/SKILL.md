---
name: inkjet
description: "如何将文本、图片和二维码从 MacOS 设备打印到一台价格低廉的无线蓝牙热敏打印机上？  
使用 `inkjet print` 命令进行输出，通过 `inkjet scan` 命令来查找可用的打印机。"
homepage: https://pypi.org/project/inkjet/
metadata:
  openclaw:
    emoji: "🖨️"
    requires: { bins: ["inkjet"], bluetooth: true }
    install:
      - { id: "pip", kind: "pip", package: "inkjet", label: "Install (pip)" }
      - { id: "brew", kind: "brew", package: "aaronchartier/tap/inkjet", label: "Install (Homebrew)" }
---
# 热敏打印机技能

使用 `inkjet` CLI 命令，可以将文本、图片和二维码打印到像 X6h、GT01 这样的小型廉价蓝牙热敏打印机上，甚至可以打印到儿童玩具猫打印机上。热敏纸的成本非常低廉，因此能够实现高频的物理输出。

## 设置

**准备：** 确保打印机已开启。打印机无需与主机计算机的蓝牙设置配对；`inkjet` 命令会通过蓝牙低功耗（BLE）直接连接到打印机。

扫描可用打印机并设置默认打印机：
```bash
inkjet scan
```

检查当前配置：
```bash
inkjet whoami
```

## 打印文本

可以直接打印字符串。支持使用 `\n` 等标准转义序列来实现多行输出。请勿使用表情符号。

```bash
inkjet print text "Hello, World!"
inkjet print text "Line 1\nLine 2\nLine 3"
inkjet print text "Big Text" --size 72
```

## 打印 Markdown 内容

使用 Markdown 语法渲染高保真的格式化内容。这是代理程序在无需保存临时文件的情况下输出复杂收据或日志的推荐方式。请勿使用表情符号。

```bash
inkjet print text "# Order 104\n- 1x Coffee\n- 1x Donut" --markdown
```

## 打印文件

输出本地文件的内容。支持纯文本（`.txt`）和 Markdown 文件（`.md`）。

```bash
inkjet print file ./receipt.txt
inkjet print file ./README.md
```

## 打印图片

```bash
inkjet print image ./photo.png
inkjet print image ./logo.jpg --dither
```

## 打印二维码

生成并打印二维码。智能手机扫描器（iPhone/Android）可以可靠地识别最小尺寸为 `--size 75` 的二维码。

```bash
inkjet print qr "https://pypi.org/project/inkjet"
inkjet print qr "WiFi:S:NetworkName;P:example123;;" --size 75
```

## 纸张控制

```bash
inkjet feed 100      # Feed paper forward (steps)
```

## 配置

可以全局配置设置，也可以针对每个项目进行本地配置。如果当前工作区中存在 `.inkjet/` 文件夹，该文件中的配置将优先生效（使用 `--local` 选项进行配置）。

### 默认配置方案
```json
{
  "default_printer": "UUID",
  "printers": { "alias": "UUID" },
  "energy": 12000,
  "print_speed": 10,
  "quality": 3,
  "padding_left": 0,
  "padding_top": 10,
  "line_spacing": 8,
  "align": "left",
  "font_size": 18
}
```

## 多打印机协同工作

如果环境配置文件（例如 `TOOLS.md`）中包含多个打印机的 UUID 或别名，可以使用 `--address` / `-a` 标志来指定目标打印机。使用 `-a default` 可以明确指定默认配置的打印机。

### 协同工作策略：
1. **基于角色的路由**：根据打印机的用途（例如，贴纸还是收据）来路由打印任务。
   `inkjet print text "Label" -a stickers`
2. **高吞吐量（负载均衡）**：在多台打印机之间分配打印任务（采用轮询方式）以最大化每分钟的打印量。

```bash
# Orchestrated Print Examples
inkjet print text "Main Status" -a office
inkjet print text "Order #104" -a kitchen
inkjet print qr "https://pypi.org/project/inkjet" -a default
inkjet print file ./log.txt -a "UUID_EXT_1"
```

## JSON 输出（用于脚本编写）

`inkjet` 命令支持 `--json` 选项，以便生成机器可读的 JSON 输出格式。

```bash
inkjet scan --json
inkjet whoami --json
```

## 工作表和手写内容的最佳实践

由于热敏纸宽度较窄且成本较低，为了制作适合儿童使用的可读工作表或手写笔记，请遵循以下建议：
1. **提高可读性**：使用 `##`（H2 标题）来标注主要内容。标准文本对于儿童来说往往太小，难以舒适地阅读或书写。
2. **手动编号**：避免使用 Markdown 列表（如 `1. content`），因为它们会自动缩进并占用更多横向空间。建议使用 `## 1) 5 + 2 = ___` 这样的格式。
3. **“低成本纸张”的使用技巧**：在项目之间使用三行换行符（`\n\n\n`）来增加书写空间。热敏纸几乎免费，充分利用垂直空间可以提高书写效果。
4. **分隔线**：在每项内容末尾使用 `---` 来创建明显的撕页线，避免撕掉最后一项内容。

## 故障排除

如果找不到打印机：
```bash
inkjet doctor
```