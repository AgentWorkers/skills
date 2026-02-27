---
name: printpal-3d
description: 使用 PrintPal API，可以从图像或文本提示生成可用于 3D 打印的 3D 模型。当用户需要创建可 3D 打印的模型、将图像转换为 STL/GLB/OBJ 文件，或根据文本描述生成 3D 资产时，可以使用该 API。如果配置了 WAVESPEED_API_KEY，该 API 还支持通过 WaveSpeed 将文本转换为图像的功能。支持使用文件路径、URL，或直接在聊天中粘贴的图像作为输入。
credentials:
  - name: PRINTPAL_API_KEY
    required: true
    description: API key for PrintPal 3D generation (get from https://printpal.io/api-keys)
  - name: WAVESPEED_API_KEY
    required: false
    description: API key for text-to-image and product photo generation (get from https://wavespeed.ai/accesskey)
  - name: OPENROUTER_API_KEY
    required: false
    description: API key for SEO metadata generation (get from https://openrouter.ai/keys)
---
# PrintPal 3D模型生成器

该工具可以从图片或文本提示生成可用于3D打印的3D模型。

## 快速入门

**通过图片路径或URL生成：**
```bash
python3 {baseDir}/scripts/generate_3d.py --image /path/to/image.png
```

**通过文本提示生成：**
```bash
python3 {baseDir}/scripts/generate_3d.py --prompt "a cute robot toy"
```

## 安装

**所需的Python包：**
```bash
pip install printpal requests
```

**用于文本转图片和SEO功能的包：**
```bash
pip install wavespeed
```

**在OpenClaw设置（`~/.openclaw/openclaw.json`的`env`部分）中配置API密钥：**
- `PRINTPAL_API_KEY` - 用于3D模型生成
- `WAVESPEED_API_KEY` - 用于文本转图片和生成产品图片
- `OPENROUTER_API_KEY` - 用于生成SEO元数据

## 工作流程

1. **获取图片：**
   - 如果用户提供了文件路径，则直接使用该路径。
   - 如果用户提供了URL，则下载该图片。
   - 如果用户粘贴了图片，则直接使用该图片（系统会将其视为文件路径或URL）。
   - 如果用户提供了文本，则首先使用WaveSpeed工具生成图片。

2. **生成3D模型：**
   - 使用PrintPal API，设置质量为“super”（768立方体像素）。
   - 默认输出格式为STL。
   - 将模型保存在工作区的`printpal-output/`目录中。

3. **提供下载链接：**
   - 如有需要，启动文件服务器。
   - 提供可点击的下载链接。

## 默认设置

| 设置 | 默认值 | 可选值 |
|---------|---------|---------|
| 质量 | super | default, high, ultra, super, super_texture, superplus, superplus_texture |
| 格式 | stl | stl, glb, obj, ply, fbx |

## 脚本

### generate_3d.py

用于生成3D模型的主脚本。
```bash
python3 scripts/generate_3d.py [OPTIONS]

Options:
  -i, --image PATH      Input image file path or URL
  -p, --prompt TEXT     Text prompt (uses WaveSpeed to generate image first)
  -q, --quality TEXT    Quality level (default: super)
  -f, --format TEXT     Output format (default: stl)
  -o, --output-dir DIR  Output directory
  --json                Output results as JSON
```

### serve_files.py

用于启动文件下载的HTTP服务器。
```bash
python3 scripts/serve_files.py [OPTIONS]

Options:
  -d, --directory DIR   Directory to serve (default: printpal-output/)
  -p, --port PORT       Port number (default: 8765)
  --host HOST           Host to bind to (default: 127.0.0.1)
  --public              Bind to 0.0.0.0 to allow network access
  --url-only            Just print URL without starting server
```

## 质量级别

| 质量 | 分辨率 | 所需 Credits | 估计时间 |
|---------|-----------|---------|-----------|
| default | 256³ | 4 | 20秒 |
| high | 384³ | 6 | 30秒 |
| ultra | 512³ | 8 | 60秒 |
| super | 768³ | 20 | 3分钟 |
| superplus | 1024³ | 30 | 4分钟 |

## 输出格式

| 格式 | 适用场景 |
|--------|----------|
| STL | 适用于3D打印（默认） |
| GLB | 适用于网页和游戏 |
| OBJ | 具有通用兼容性 |
| PLY | 适用于点云数据 |
| FBX | 适用于Autodesk软件 |

## API密钥

**需要在`~/.openclaw/openclaw.json`的`env`部分配置的环境变量：**
- `PRINTPAL_API_KEY` - 从https://printpal.io/api-keys获取（用于3D模型生成）
- `WAVESPEED_API_KEY` - 从https://wavespeed.ai/accesskey获取（可选，用于文本转图片）
- `OPENROUTER_API_KEY` - 从https://openrouter.ai/keys获取（可选，用于生成SEO元数据）

## 输出目录

默认输出目录为工作区的`printpal-output/`。可以通过以下方式更改：
- 环境变量：`PRINTPAL_OUTPUT_DIR=/path/to/output`
- 命令选项：`--output-dir /path/to/output`

## 安全注意事项

- **文件服务器**：`serve_files.py`脚本默认使用本地主机（127.0.0.1）作为安全设置。如需公开访问，请使用`--public`参数。
- **第三方包**：脚本依赖于`printpal`、`wavespeed`和`requests`包。安装前请检查这些包的来源和安全性。
- **下载内容**：该工具会从用户提供的URL下载图片，请确保这些图片来源可靠。

## 错误处理

| 错误 | 解决方案 |
|-------|----------|
| WAVESPEED_API_KEY未设置 | 直接提供图片或配置API密钥 |
| PRINTPAL_API_KEY未设置 | 在OpenClaw设置中配置API密钥 |
| Credits不足 | 在printpal.io/buy-credits购买更多Credits |
| 包未安装 | 运行`pip install printpal wavespeed`进行安装 |

---

# SEO产品列表生成器

该工具可以为在Etsy、TikTok Shop等平台上销售3D模型/打印品生成优化的SEO元数据和产品图片。

## 快速入门

```bash
python3 scripts/seo_product_photos.py \
  --image /path/to/model_photo.jpg \
  --description "A cute dragon figurine" \
  --purpose "Collectible toy for fantasy fans" \
  --audience "Fantasy enthusiasts, collectors, parents buying for kids"
```

## 工作流程

1. **输入**：用户提供3D模型/打印品的图片、描述、用途和目标受众信息。
2. **SEO生成**：使用OpenRouter MiniMax生成优化的标题和描述。
3. **图片生成**：使用WaveSpeed工具生成5张精美的产品图片。
4. **输出**：生成包含元数据和图片的ZIP文件，并通过本地HTTP服务器提供下载链接。

## 所需的环境变量

```bash
# OpenRouter (for SEO generation)
OPENROUTER_API_KEY=your_openrouter_key

# WaveSpeed (for product photos)
WAVESPEED_API_KEY=your_wavespeed_key
```

**获取OpenRouter密钥：** https://openrouter.ai/keys
**获取WaveSpeed密钥：** https://wavespeed.ai/accesskey

## 选项

| 选项 | 参数 | 说明 | 默认值 |
|--------|-------|-------------|---------|
| --image | -i | 输入图片的路径或URL | 必需 |
| --description | -d | 3D模型/打印品的描述 | 必需 |
| --purpose | -p | 产品的用途 | 必需 |
| --audience | -a | 目标受众 | 必需 |
| --num-photos | -n | 生成的照片数量 | 5张 |
| --port | - | 下载服务器端口 | 8766 |
| --json | - | 是否以JSON格式输出结果 | 否 |

## 输出内容

脚本生成的文件包括：
- `seo_metadata.txt` - 完整的元数据（标题、描述、标签等）
- `product_photo_01.png` 至 `product_photo_05.png` - 生成的产品图片
- `seo_product_listing.zip` - 所有文件的压缩包

下载链接将在脚本执行后提供（例如：`http://hostname:8766/seo_product_listing.zip`）

## SEO元数据字段

生成的元数据包括：
- **title**：完整的SEO标题（最多140个字符，包含关键词）
- **short_title**：简洁的缩略图标题（最多40个字符）
- **description**：详细的商品描述（500-1000个单词）
- **tags**：15个优化的搜索标签
- **category**：主要的市场平台分类
- **search_terms**：5个高价值的搜索关键词
- **key_features**：产品的4个关键特性
- **target_marketplace**：推荐的销售平台

## 示例

```bash
# 为定制的3D打印杯垫生成SEO列表
python3 scripts/seo_product_photos.py \
  --image /workspace/my_mug_holder.jpg \
  --description "一个带有龙图案的定制3D打印杯垫" \
  --purpose "用于整理桌面或厨房的杯子，非常适合礼物" \
  --audience "办公室工作人员、咖啡爱好者、居家办公者"
```

## 故障排除

| 错误 | 解决方案 |
|-------|----------|
| OPENROUTER_API_KEY未设置 | 在OpenClaw设置中配置API密钥 |
| 图片生成失败 | 检查WAVESPEED_API_KEY和Credits是否正确配置 |
| 使用的端口已被占用 | 使用`--port`参数指定其他端口 |

## 参考文档

有关API的详细文档，请参阅[api-reference.md](references/api-reference.md)。