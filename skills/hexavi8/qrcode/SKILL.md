---
name: qrcode
description: Generate styled QR codes (SVG/PNG/JPG) with custom colors, shapes, and error correction. Agent should display generated files. Secure: all outputs saved to workspace root.
homepage: https://github.com/HeXavi8/skills
metadata:
  {
    "clawdbot":
      {
        "emoji": "",
        "requires": { "bins": ["node"], "packages": ["qrcode", "sharp"] },
        "primaryEnv": null,
      },
  }
---

# QR码生成器

本工具可生成基于文本或URL的可定制QR码，支持SVG/PNG/JPG多种格式，并提供丰富的样式选项。

## 使用说明

**生成QR码后，您必须：**

1. 使用适当的Markdown语法展示生成的文件：
   - 对于PNG/JPG格式的图片：`![QR码](sandbox:/path/to/file.png)`
   - 对于SVG格式的文件：可以直接显示图片或提供下载链接。
2. 向用户确认文件的路径和格式。
3. 如有需要，可提供重新生成QR码并调整样式的选项。

## 快速入门

```bash
# Basic usage (auto-generated filename)
node {baseDir}/scripts/generate.mjs "Hello World"

# Custom styled QR code
node {baseDir}/scripts/generate.mjs "https://example.com" -o myqr.svg --dot circle --eye rounded --color "#2563eb"

# High-resolution transparent PNG
node {baseDir}/scripts/generate.mjs "Contact Info" --format png --size 2048 --transparent

# Print-quality JPEG
node {baseDir}/scripts/generate.mjs "https://example.com" --format jpg -o qr.jpg --size 2048 --quality 95
```

## 参数选项

### 输出设置

- `-o, --out <文件名>` - 输出文件的路径（仅限工作区根目录）。默认格式为：`qrcode_<文本>_<时间戳>.<扩展名>`
- `--format <svg|png|jpg>` - 输出格式（默认为SVG）

### 尺寸设置

- `--size <像素>` - 基本像素大小（默认为1024，最大为10000）
- `--scale <倍数>` - 图像缩放比例（默认为1，最大为10）
- `--margin <像素>` - 静态区域大小（默认为4，最大为100）

### 样式设置

- `--dot <形状>` - 数据模块的形状（默认为方形）
- `--eye <形状>` - QR码中心点的形状（默认为方形）
- `--color <颜色代码>` - 前景颜色（默认为#000000）
- `--background <颜色代码>` - 背景颜色（默认为#ffffff）
- `--transparent` - 透明背景（仅适用于PNG格式，SVG/JPG格式忽略此选项）

### 图像质量设置

- `--ec <级别>` - 错误校正级别：低/中/高（默认为中等，M级）
  - **L（约7%）**：适合干净环境，最大数据容量
  - **M（约15%）**：通用场景，平衡容量与可靠性
  - **Q（约25%）**：适用于带样式的QR码，具有较好的抗损能力
  - **H（约30%）**：适合嵌入Logo、复杂样式或户外使用

- `--quality <数值>` - JPEG压缩质量（默认为80）

## 文件管理规则

- 所有生成的文件仅保存在工作区根目录。
- 文件路径会被自动简化（例如：`-o ../path/file.svg` 会被处理为 `workspace/file.svg`）。
- 自动生成的文件名包含经过清理的文本和时间戳。
- 文本长度限制为4096个字符。

## 安装说明

```bash
cd {baseDir}
npm install
```

**依赖库：** `qrcode`（用于生成QR码图像）、`sharp`（用于图像转换）

**平台说明：** macOS系统需要Xcode命令行工具。其他平台的安装方法请参考[sharp文档](https://sharp.pixelplumbing.com/install)。

## 示例

- **WiFi QR码生成**
- **带样式的名片**
- **高分辨率打印版QR码**
- **带有透明Logo的QR码**
- **嵌入Logo的QR码**

## 安全特性

- ✅ **路径限制**：所有输出文件必须保存在工作区根目录。
- ✅ **防止符号链接攻击**：采用原子写入操作并进行验证。
- ✅ **输入验证**：限制文本长度（4096个字符）并仅允许特定字符。
- ✅ **文件名清理**：去除文件名中的危险字符。
- ✅ **资源限制**：限制文件大小和分辨率，以防止DoS攻击。

## 常见问题及解决方法

| 问题 | 解决方案                                                                                                                         |
|------|-------------------------------------------------------------------------------------------------------------------------|
| `npm install` 失败 | 安装构建工具：`xcode-select --install`（macOS系统）或参考[sharp安装指南](https://sharp.pixelplumbing.com/install) |
| QR码无法扫描 | 增加`--size`参数，或选择更高的错误校正级别`--ec H`，或简化QR码样式 |
| 颜色显示不正确 | 使用十六进制颜色代码`#RRGGBB`（例如`#FF5733`），避免使用RGB或颜色名称 |
| 文件过大 | 减小`--size`或`--scale`参数，或提高JPG格式的`--quality`参数 |
| 没有权限访问文件 | 检查工作区目录的写入权限 |

## 错误校正级别说明

错误校正功能可确保QR码在部分损坏或被遮挡的情况下仍可被扫描：

| 错误校正级别 | 数据恢复能力 | 数据容量 | 适用场景                                      |
|---------|--------------|---------|---------------------------------------------------------|
| L       | 约7%的损坏       | 最大容量    | 干净的环境、屏幕显示、最大数据量                         |
| M       | 约15%的损坏       | 中等容量    | 通用场景（默认设置）、标准打印                          |
| Q       | 约25%的损坏       | 中等容量    | 带样式的QR码、轻微损坏                         |
| H       | 约30%的损坏       | 最小容量    | 嵌入Logo、户外使用、复杂样式                         |

**使用高错误校正级别（H级）的场合：**

- 嵌入Logo（Logo覆盖面积约为QR码的20-30%）
- 使用圆形或圆角的中心点设计
- 在户外或环境恶劣的环境中使用
- 需要高质量打印的场合

## 格式对比

| 格式    | 透明度     | 图像质量   | 文件大小    | 适用场景                                      |
|---------|-----------|---------|---------------------------------------------------------|
| SVG     | 支持透明     | 无损压缩   | 最小文件大小 | 网页、可缩放图形                             |
| PNG     | 支持透明     | 有损压缩   | 中等文件大小 | 数字显示屏、叠加层                         |
| JPG     | 不支持透明   | 有损压缩   | 最小文件大小（压缩后） | 打印、照片、电子邮件                         |

**使用建议：**

- **扫描距离**：移动设备使用`--size 1024`，打印或海报使用`--size 2048+`。
- **样式与可靠性**：更高的`--ec`级别可以弥补`--dot square`或`--eye rounded`设置带来的性能影响。
- **透明背景**：使用PNG格式并设置`--transparent`；JPG格式默认使用白色或指定背景颜色。
- **文件大小优化**：网页使用SVG格式，打印文件使用`--quality 80-85`的JPG格式。
- **数据容量**：不同错误校正级别对应不同的最大字符容量：L级约4296个字符，M级约3391个字符，Q级约2420个字符，H级约1852个字符（基于版本40）。
- **Logo放置**：使用`--ec H`并将QR码中心区域留空（约占QR码面积的30%）。

## 常见使用场景及推荐设置

| 使用场景          | 推荐参数设置                                                                                         |
|------------------|-------------------------------------------------------------------------------------------------------------------------|
| 网站URL          | `--format png --size 1024 --ec M`                                                                                   |
| WiFi密码         | `--format png --size 1024 --ec M`                                                                                   |
| 名片（vCard）        | `--format svg --dot circle --eye rounded --ec Q`                                                                                   |
| 打印海报         | `--format jpg --size 4096 --quality 95 --ec H`                                                                                   |
| Logo叠加层         | `--format png --size 2048 --ec H --transparent`                                                                                   |
| 电子邮件签名       | `--format png --size 512 --ec M`                                                                                   |
| 产品包装         | `--format svg --ec H`                                                                                   |
| 户外标识         | `--format jpg --size 2048+ --ec H --quality 90`                                                                                   |
| 社交媒体头像       | `--format png --size 1024 --transparent --dot circle --ec Q`                                                                                   |
| 支付二维码（高密度）     | `--format png --size 2048 --ec L --margin 2`                                                                                   |