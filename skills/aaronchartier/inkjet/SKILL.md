---
name: inkjet
description: "如何将文本、图片和二维码从 MacOS 设备打印到一台便宜的无线蓝牙热敏打印机上？  
- 使用 `inkjet print` 命令进行打印；  
- 使用 `inkjet scan` 命令来查找可用的打印机。"
homepage: https://github.com/AaronChartier/inkjet
metadata:
  openclaw:
    emoji: "🖨️"
    requires: { bins: ["inkjet"], bluetooth: true }
    install:
      - { id: "pip", kind: "pip", package: "inkjet", label: "Install (pip)" }
      - { id: "brew", kind: "brew", package: "aaronchartier/tap/inkjet", label: "Install (Homebrew)" }
---

# 热敏打印机技能

您可以使用 `inkjet` CLI 将文本、图片和二维码打印到小型且价格低廉的蓝牙热敏打印机上，例如 X6h、GT01 以及儿童玩具打印机。热敏纸的成本非常低廉，因此可以实现高频的物理输出。

## 安装

### 通过 pip（通用方法）
```bash
pip install inkjet
```

### 通过 Homebrew（macOS）
```bash
brew install aaronchartier/tap/inkjet
```

## 设置

**准备：** 确保打印机已开启。打印机无需与主机计算机的蓝牙设置配对；`inkjet` 会通过 BLE 直接连接。

扫描打印机并设置默认打印机：
```bash
inkjet scan
```

检查当前配置：
```bash
inkjet whoami
```

## 打印文本

直接打印字符串。支持标准的转义序列（如 `\n` 用于多行输出）。请勿使用表情符号。

```bash
inkjet print text "Hello, World!"
inkjet print text "Line 1\nLine 2\nLine 3"
inkjet print text "Big Text" --size 72
```

## 打印 Markdown

使用 Markdown 语法渲染高保真的格式化内容。这是代理程序在无需保存临时文件的情况下输出复杂收据或日志的推荐方式。请勿使用表情符号。

```bash
inkjet print text "# Order 104\n- 1x Coffee\n- 1x Donut" --markdown
```

## 打印文件

输出本地文件的内容。支持纯文本（`.txt`）和 Markdown（`.md`）文件。

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

生成并打印二维码。智能手机扫描器（iPhone/Android）可以可靠地读取最小尺寸为 `--size 75` 的二维码。

```bash
inkjet print qr "https://github.com/AaronChartier/inkjet"
inkjet print qr "WiFi:S:NetworkName;P:example123;;" --size 75
```

## 纸张控制

```bash
inkjet feed 100      # Feed paper forward (steps)
```

## 配置

您可以全局配置设置，也可以针对每个项目进行本地配置。如果当前工作区中存在 `.inkjet/` 文件夹，则该文件的配置会优先生效（使用 `--local` 选项进行配置）。

```bash
inkjet config show                    # Show all settings
inkjet config set printer <UUID>      # Set the default device
inkjet config set energy 12000        # Set local project darkness
inkjet config alias kitchen <UUID>    # Save a friendly name
```

## 多打印机协调

如果环境配置文件（例如 `TOOLS.md`）中包含多个打印机的 UUID 或别名，可以使用 `--address` / `-a` 标志来指定目标硬件。使用 `-a default` 可以明确指定默认配置的设备。

### 协调策略：
1. **基于角色的路由**：根据硬件类型路由输出内容（例如，标签页 vs 收据）。
   `inkjet print text "Label" -a stickers`
2. **高吞吐量（负载均衡）**：在多台打印机之间分配打印任务（轮询方式）以最大化每分钟的打印量。

```bash
# Orchestrated Print Examples
inkjet print text "Main Status" -a office
inkjet print text "Order #104" -a kitchen
inkjet print qr "https://github.com/AaronChartier/inkjet" -a default
inkjet print file ./log.txt -a "UUID_EXT_1"
```

## 配置调整（文件系统访问）

您可以直接修改配置文件来调整 `inkjet` 的行为。`inkjet` 会优先使用 `./.inkjet/config.json` 文件，而不是全局配置文件（默认设置）。

### JSON 架构
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

通过修改 JSON 文件，您可以调整不同文档类型的默认边距（`padding`）、对齐方式或字体大小（`size`），而无需更改命令行参数。

## JSON 输出（用于脚本编写）

命令支持 `--json` 选项，以生成机器可读的输出格式：

```bash
inkjet scan --json
inkjet whoami --json
```

## 动态数据流处理

您可以从另一个命令的输出中读取数据，而无需创建新的文件。使用 `-` 作为参数可以从标准输入（stdin）读取数据。

```bash
# Text Piping
echo "Receipt line 1" | inkjet print text -

# Image Piping
curl -s "https://raw.githubusercontent.com/AaronChartier/inkjet/main/assets/logo.jpg" | inkjet print image -
```

## 工作表和手写记录的最佳实践

热敏纸宽度较窄且价格低廉。为了制作适合儿童使用的工工作表或手写记录，请遵循以下建议：

1. **提高可读性**：使用 `##`（H2 标题）来标记主要内容。标准文本通常太小，不利于儿童阅读或书写。
2. **手动编号**：避免使用 Markdown 列表（如 `1. content`）。列表会自动缩进，从而减少可用空间。建议使用 `## 1) 5 + 2 = ___` 这样的格式。
3. **“廉价纸张”的使用技巧**：在项目之间使用三个换行符（`\n\n\n`）来增加垂直间距，从而提供更多的书写空间。
4. **分隔线**：在每项内容末尾使用 `---` 来创建一个明显的撕页线，避免撕掉最后一行内容。

## 故障排除

如果找不到打印机：
```bash
inkjet doctor
```