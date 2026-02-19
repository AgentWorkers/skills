---
name: mixtiles-it
description: 将照片发送到 Mixtiles 以订购墙砖。当用户转发/发送一张照片并希望将其订购为 Mixtile、将其添加到他们的 Mixtiles 购物车中，或者说出“将这张照片制成 Mixtile”之类的指令时，可以使用此功能。该功能也支持处理图片的 URL。
---
# Mixtiles It

可以将任何照片转换为 Mixtiles 的订单链接。用户发送照片（或图片 URL），系统会返回一个可直接用于下单的 Mixtiles 购物车链接。

## 工作原理

1. 用户发送或转发一张照片或图片的 URL。
2. 运行上传脚本以获取该图片的公共 URL 和 Mixtiles 购物车链接。
3. 将购物车链接发送给用户，用户点击该链接即可自定义图片尺寸、框架并完成下单。

## 使用方法

```bash
# Single photo
python3 scripts/mixtiles-cart.py <local-file-or-url> [--size SIZE]

# Multiple photos (one cart link with all photos)
python3 scripts/mixtiles-cart.py --batch <image1> <image2> ... [--size SIZE]
```

该脚本支持以下操作：
- **本地文件**：将文件上传到 Cloudinary（Mixtiles 仅支持从 Cloudinary 服务器加载图片）。
- **URL**：首先下载图片，再将其上传到 Cloudinary。
- **批量模式**：一次性上传多张图片，并生成一个包含所有图片的购物车链接。
- **输出结果**：将生成的 Mixtiles 购物车链接输出到标准输出（stdout）。

### 图片尺寸选项

默认尺寸为 `RECTANGLE_12X16`。Mixtiles 还提供其他尺寸选项：
- `SQUARE_8X8` — 经典正方形尺寸
- `RECTANGLE_12X16` — 纵向矩形尺寸（默认值）
- `RECTANGLE_16X12` — 横向矩形尺寸

### 环境变量（可选）

- `CLOUDINARY_CLOUD` — Cloudinary 云服务名称（默认值：`demo`）
- `CLOUDINARY_PRESET` — Cloudinary 上传预设设置（默认值：`unsigned`）
- `MIXTILES_UPLOAD_URL` — 用于覆盖上传 API 的地址（备用方案）
- `MIXTILES_UPLOAD_KEY` — 用于覆盖上传 API 的密钥（备用方案）

## 工作流程

当用户发送一张照片并希望将其用于 Mixtiles 时，系统会执行以下步骤：
1. 确定图片文件的路径（来自媒体附件）或 URL。
2. 运行命令：`python3 <skill-dir>/scripts/mixtiles-cart.py <path-or-url>`
3. 将生成的购物车链接发送给用户，并附上提示信息：“这是您的 Mixtiles 链接！🖼️ 点击即可自定义尺寸和框架并下单。”

如果用户发送了多张照片，可以使用 `--batch` 选项来生成包含所有图片的单一购物车链接：
`python3 <skill-dir>/scripts/mixtiles-cart.py --batch <path1> <path2> ...`