---
name: qr-generator
description: **将文本或URL转换为可用于手机扫描的QR码**
---
# QR生成器

该工具可根据给定的文本或URL生成QR码图像（格式为PNG或SVG），或以ASCII艺术的形式输出到终端。非常适合用于通过Feishu将长链接、WiFi密码或文本片段传输到移动设备上（用户只需扫描生成的QR码即可接收信息）。

## 使用方法

```bash
# Generate a QR code image
node skills/qr-generator/index.js --text "https://openclaw.ai" --output "qr_code.png"

# Generate to terminal (ASCII art)
node skills/qr-generator/index.js --text "Hello World" --terminal
```

## 参数选项

- `-t, --text <text>`：需要编码的文本或URL（必选参数）。
- `-o, --output <path>`：输出文件的路径（例如：`code.png`、`code.svg`）。
- `--terminal`：以ASCII艺术的形式将QR码输出到终端。
- `--width <number>`：图像的宽度（默认值：500像素）。
- `--color-dark <hex>`：二维码的背景颜色（十六进制代码，例如：`#000000`，默认值：黑色）。
- `--color-light <hex>`：二维码的文字颜色（十六进制代码，例如：`#ffffff`，默认值：白色）。

## 示例：将QR码发送到Feishu

```bash
# 1. Generate QR code
node skills/qr-generator/index.js --text "https://example.com" --output "temp_qr.png"

# 2. Send to user via Feishu
node skills/feishu-image/send.js --target "ou_xxx" --file "temp_qr.png"

# 3. Clean up
rm temp_qr.png
```