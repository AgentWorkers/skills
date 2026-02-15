---
description: 生成二维码，用于存储URL、WiFi密码、vCard信息、电子邮件地址、短信内容以及纯文本数据。
---

# QR Code生成工具

本工具可用于生成多种类型数据的QR码，并支持自定义外观。

## 系统要求

- Python 3.8及以上版本
- 需安装 `qrcode[pil]` 包（`qrcode` 库与 `Pillow` 图像处理库）

## 使用说明

1. **确定QR码的类型** 并准备数据内容：
   - **URL**: 原始URL字符串（例如：`https://example.com`）
   - **WiFi**: `WIFI:T:<WPA|WEP|nopass>;S:<SSID>;P:<password>;;`
   - **vCard**: `BEGIN:VCARD\nVERSION:3.0\nN:<last>;<first>\nTEL:<phone>\nEMAIL:<email>\nEND:VCARD`
   - **Email**: `mailto:user@example.com?subject=Hello&body=Hi`
   - **SMS**: `smsto:<number>:<message>`
   - **Text**: 原始文本字符串

2. **生成QR码**：
   ```python
   import qrcode
   qr = qrcode.QRCode(version=None, error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=10, border=4)
   qr.add_data(payload)
   qr.make(fit=True)
   img = qr.make_image(fill_color="black", back_color="white")
   img.save(output_path)
   ```

3. **输出结果**：
   将生成的QR码保存为PNG格式的文件，文件路径为 `/tmp/qr_<type>_<timestamp>.png`（其中 `<type>` 为数据类型，`<timestamp>` 为当前时间戳），或用户指定的路径。同时返回该文件的路径。

## 自定义选项

- **大小**: 可调整 `box_size`（默认值：10，范围：5-20）
- **边框**: 可调整 `border`（默认值：4，最小值：4）
- **颜色**: `fill_color` 和 `back_color` 可设置为颜色名称或十六进制代码
- **纠错等级**: `L`（7%）、`M`（15%）、`Q`（25%）、`H`（30%）——纠错等级越高，二维码越稳定，但文件体积也越大

## 注意事项

- **大数据量**: 如果数据量过大（超过2KB），系统会自动调整QR码的尺寸（`fit=True`），但会发出警告（可能无法正常扫描）。
- **WiFi信息中的特殊字符**: 在SSID或密码中，需要使用反斜杠 `\` 对 `;`、`:`、`\` 和 `,` 进行转义处理。
- **Pillow库未安装**: 如果导入 `Pillow` 时出现错误，请运行 `pip install Pillow` 后重新尝试。
- **二进制数据**: 不建议将二进制数据转换为QR码，建议使用URL链接代替。

## 安全性提示

- **WiFi密码**: 请注意，包含WiFi密码的QR码可以被任何人扫描到，因此请谨慎使用。
- **敏感数据**: 除非特别要求，否则切勿生成包含API密钥、令牌或敏感信息的QR码。
- **文件路径处理**: 请对文件路径进行安全处理，以防止目录遍历攻击。