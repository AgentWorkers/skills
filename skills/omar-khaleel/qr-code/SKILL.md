---
name: qr-code
description: 生成和读取二维码。适用于用户需要将文本/URL转换为二维码，或从图像文件中解码/读取二维码的场景。支持PNG/JPG格式的输出，并能够从截图或图像文件中读取二维码。
---

# QR码

本工具支持从文本或URL生成QR码，以及从图像中解码QR码。

## 功能

- 从任意文本、URL或数据生成QR码
- 自定义QR码的大小和纠错级别
- 可将生成的QR码保存为PNG格式文件，或在终端中显示
- 从PNG、JPG等图像文件中读取/解码QR码
- 从截图中读取QR码

## 安装要求

### 生成QR码所需依赖库

```bash
pip install qrcode pillow
```

### 解码QR码所需依赖库

```bash
pip install pillow pyzbar
```

在Windows系统上，使用pyzbar需要安装Visual C++ Redistributable。  
在macOS系统上：`brew install zbar`  
在Linux系统上：`apt install libzbar0`

## 生成QR码的命令

```bash
python scripts/qr_generate.py "https://example.com" output.png
```

选项说明：
- `--size`：QR码的边长（以像素为单位，默认值：10）
- `--border`：QR码边框的宽度（以像素为单位，默认值：4）
- `--error`：QR码的纠错级别（L/M/Q/H，默认值：M）

示例（包含选项）：

```bash
python scripts/qr_generate.py "Hello World" hello.png --size 15 --border 2
```

## 解码QR码的命令

```bash
python scripts/qr_read.py image.png
```

该命令会返回QR码中包含的文本或URL内容。

## 快速示例

- 为某个URL生成QR码：  
  ```python
import qrcode
img = qrcode.make("https://openclaw.ai")
img.save("openclaw.png")
```

- 从图像中读取QR码：  
  ```python
from pyzbar.pyzbar import decode
from PIL import Image
data = decode(Image.open("qr.png"))
print(data[0].data.decode())
```

## 相关脚本

- `scripts/qr_generate.py`：用于生成带有自定义参数的QR码  
- `scripts/qr_read.py`：用于从图像文件中解码QR码