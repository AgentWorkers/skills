---
name: qr-gen
description: >
  **生成二维码的功能：**  
  能够从文本、URL、WiFi密码、vCard（电子名片）或任何数据生成二维码。适用于用户需要创建可扫描的二维码、分享链接、生成WiFi登录二维码、创建联系人/电子名片二维码，或生成其他可扫描的条形码图像的场景。支持输出格式包括PNG、SVG和ASCII艺术（ASCII art）。
---
# QR码生成器

通过随附的Python脚本生成QR码。

## 快速入门

```bash
python3 scripts/generate_qr.py "https://example.com" -o qr.png
```

## 常见用途

### URL或文本
```bash
python3 scripts/generate_qr.py "https://example.com" -o link.png
```

### WiFi网络（手机可扫描）
```bash
python3 scripts/generate_qr.py "wifi" --wifi-ssid "MyNetwork" --wifi-pass "secret123" -o wifi.png
```

### vCard联系人信息
生成vCard格式的字符串并输出：
```bash
python3 scripts/generate_qr.py "BEGIN:VCARD
VERSION:3.0
FN:Jane Smith
TEL:+1234567890
EMAIL:jane@example.com
END:VCARD" -o contact.png
```

### ASCII艺术（终端预览）
```bash
python3 scripts/generate_qr.py "hello" --format ascii
```

### SVG格式（可缩放，适合网页显示）
```bash
python3 scripts/generate_qr.py "data" -o code.svg
```

## 参数选项

- `-o FILE` — 输出文件路径（默认：qr.png）
- `-s N` — 图框大小（单位：像素）（默认：10）
- `--border N` — 边框宽度（单位：像素）（默认：4）
- `--format png|svg|ascii` — 强制指定输出格式（根据文件扩展名自动判断）
- `--error-correction L|M|Q|H` — 错误校正级别（默认：M；H适用于对图像损坏有较高容忍度的场景）

## 依赖库

如果系统中没有`qrcode[pil]`库，脚本会通过pip自动安装该库。无需手动配置。