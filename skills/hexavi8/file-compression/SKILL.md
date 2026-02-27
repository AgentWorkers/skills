---
name: file-compression
description: >
  **压缩文件以减少存储空间和传输大小**  
  当用户需要缩小PDF文件或图片的体积、优化上传/分享时的文件大小，或者在保证质量的同时降低文件大小时，可以使用此技能。该工具支持使用Python进行PDF和图片压缩；当Python依赖项不可用时，会自动切换到Node.js作为备用方案。
metadata:
  {
    "clawdbot":
      {
        "requires":
          {
            "bins": ["python3", "node", "gs"],
            "packages": ["pikepdf", "pillow", "sharp"],
          },
        "primaryEnv": "python",
      },
  }
---
# 文件压缩

提供使用 Python 作为主要处理方式，以及 Node.js 作为备用处理方式的文件压缩功能。

## 支持的文件类型

- PDF：`.pdf`
- 图像：`.jpg`, `.jpeg`, `.png`, `.webp`

## 该功能可以做什么

- 使用预设的质量级别压缩 PDF 文件。
- 对图像进行压缩，并支持质量控制、尺寸调整和格式转换。
- 当依赖项缺失时，自动切换到备用处理方式。
- 检测到压缩效果不佳时，尝试使用更优化的策略重新压缩。

## 安装要求（运行前）

所需二进制文件：

- `python3`（建议版本 `>= 3.8`）
- `node`
- `gs`（Ghostscript，用于处理 PDF 文件）

**Python 安装说明：**

```bash
python3 -m pip install -r {baseDir}/requirements.txt
```

**Node.js 安装说明：**

```bash
cd {baseDir}
npm install
```

**Ghostscript 安装示例：**

- macOS：`brew install ghostscript`
- Ubuntu/Debian：`sudo apt-get update && sudo apt-get install -y ghostscript`

**安全提示：**

- 在执行每个安装命令之前，向用户说明正在安装第三方软件包。
- 如果安装失败，请报告失败的具体命令，并切换到可用的备用处理方式。

## 命令行选项速查表

**PDF 处理（`scripts/compress_pdf.py`）：**

- `--preset screen|ebook|printer|prepress`
- `--strategy auto|ghostscript|pikepdf`
- `--remove-metadata`
- `--no-linearize`
- `--overwrite`

**PDF 处理（Node.js 版本，`scripts/compress_pdf_node.mjs`）：**

- `--preset screen|ebook|printer|prepress`

**图像处理（`scripts/compress_image.py`）：**

- `--quality <1-100>`
- `--format keep|jpeg|png|webp`
- `--max-width <n>`
- `--max-height <n>`
- `--strategy auto|pillow|node`
- `--overwrite`

**图像处理（Node.js 版本，`scripts/compress_image_node.mjs`：**

- `--quality <1-100>`
- `--format keep|jpeg|png|webp`
- `--max-width <n>`
- `--max-height <n>`

## 示例代码（Python + Node.js 结合使用）**

- **PDF 默认压缩方式：**
```bash
python {baseDir}/scripts/compress_pdf.py in.pdf out.pdf
```

- **PDF 高效压缩方式：**
```bash
python {baseDir}/scripts/compress_pdf.py in.pdf out.pdf --preset screen --strategy ghostscript
```

- **使用 pikepdf 进行 PDF 压缩：**
```bash
python {baseDir}/scripts/compress_pdf.py in.pdf out.pdf --strategy pikepdf --remove-metadata
```

- **使用 Node.js 处理 PDF：**
```bash
node {baseDir}/scripts/compress_pdf_node.mjs in.pdf out.pdf --preset ebook
```

- **图像默认压缩方式：**
```bash
python {baseDir}/scripts/compress_image.py in.jpg out.jpg --quality 75
```

- **图像转换 + 尺寸调整：**
```bash
python {baseDir}/scripts/compress_image.py in.png out.webp --format webp --quality 72 --max-width 1920
```

- **强制使用 Node.js 处理图像：**
```bash
python {baseDir}/scripts/compress_image.py in.jpg out.jpg --strategy node --quality 70
```

- **直接使用 Node.js 处理图像：**
```bash
node {baseDir}/scripts/compress_image_node.mjs in.jpg out.jpg --quality 70 --max-width 1600
```

## 环境配置与备用方案

安装顺序如下：

1. 检查并安装 Python：`python3 --version`（如果 Python 3.8 无法使用，可尝试使用 3.11/3.10/3.9/3.8）
2. 检查并安装 Node.js：`node --version`
3. 检查并安装 Ghostscript：`gs --version`（用于处理 PDF 文件）
4. （如需要）安装 Python 的依赖库：
   - `pip install pikepdf`
   - `pip install pillow`
5. （如需要）安装 Node.js 的依赖库：
   - `npm install`

**备用方案：**

- 对于 PDF 文件：
  - 如果 Python 3.8 无法使用，依次尝试使用 `ghostscript`、`pikepdf`、`node-ghostscript`。
- 对于图像文件：
  - 依次尝试使用 `pillow`、`node-sharp`。

## 执行过程透明度

- 在执行每个操作前，务必向用户明确说明当前的操作内容。
- 在执行命令前，展示具体的命令内容。
- 对于耗时较长的操作（如 `pip install`、`npm install` 或处理大型 Ghostscript 文件），请告知用户当前正在等待。
- 每完成一个步骤后，报告结果及下一步的操作内容。

## 处理压缩失败的情况

- 如果压缩后的文件大小大于或等于原始文件大小，不要立即停止操作：
  - 提供压缩前后的文件大小以及压缩比率。
  - 分析可能的原因：
    - 对于 PDF 文件：可能是文件已经过优化、包含扫描图像、元数据过多或使用了不合适的预设设置。
    - 对于图像文件：可能是格式转换不合适、质量设置过高或文件本身体积较小导致额外开销。
  - 尝试使用其他压缩策略：
    - 对于 PDF 文件：将预设方式从“screen”改为“ebook”，或切换到其他压缩方式。
    - 对于图像文件：降低压缩质量、更换压缩工具（如从“node”切换到“pillow”），或尝试转换为其他格式（如“webp”并调整尺寸）。
  - 最终返回效果最佳的压缩结果，并说明使用的是哪个命令。

## 代理响应规范

- 每次完成压缩任务后，必须返回以下信息：
  - 压缩后的文件绝对路径。
  - 压缩前后的文件大小对比（`from <before_size> to <after_size>`）。
  - 文件大小减少了多少（`saved <delta_size> (<ratio>%)`）。
  - 使用的压缩工具（`Backend used`）。