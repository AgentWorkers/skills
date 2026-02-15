# xai-image-gen

使用 xAI 的 Grok API（grok-imagine-image 模型）生成图片。

## 说明

这是一个可用于生产环境的命令行工具（CLI），通过 xAI 的图像生成 API 生成图片。支持多种输出格式、分辨率以及批量生成功能。会自动生成 `MEDIA:` 路径，以便 OpenClaw 自动将其附加到消息中。

**特点：**
- 🎨 简单的 CLI 接口：`xai-gen "<prompt>"`
- 🖼️ 多种输出格式：URL 下载、base64 编码
- 🔢 批量生成（每个提示可生成多张图片）
- ⚡ 快速的、基于 API 的实现（兼容 Raspberry Pi）
- 🛡️ 强大的错误处理机制，提供友好的错误提示
- 📎 生成的图片会自动附加到 OpenClaw 中
- 🎯 使用 xAI 的原生分辨率（无需指定图片大小）

## 安装

```bash
# Navigate to skills directory
cd ~/.openclaw/workspace/skills

# Clone or copy this skill
# (or install via clawhub when published)

# Install dependencies
pip3 install requests

# Ensure the script is executable
chmod +x xai-image-gen/xai-gen
```

**设置您的 xAI API 密钥：**

```bash
export XAI_API_KEY="your-api-key-here"
```

将以下命令添加到您的 shell 配置文件（`~/.bashrc` 或 `~/.zshrc`）中，以便永久生效：

```bash
echo 'export XAI_API_KEY="your-api-key-here"' >> ~/.bashrc
```

## 使用方法

### 基本用法

```bash
# Generate with simple prompt
xai-gen "sunset over mountains"

# Custom filename
xai-gen "cyberpunk city" --filename city.png

# Generate multiple images
xai-gen "futuristic vehicle" --n 3

# Base64 output (no download)
xai-gen "logo design" --format b64

# Verbose mode
xai-gen "space station" --verbose
```

### 参数选项

```
positional arguments:
  prompt                Text description of the image to generate

options:
  -h, --help            Show help message
  --model MODEL         Model name (default: grok-imagine-image)
  --filename FILENAME   Output filename (default: out.png)
  --format {url,png,b64}
                        Response format: url (download), png (alias), b64 (base64)
  --n N                 Number of images to generate (default: 1)
  --verbose, -v         Show detailed progress
```

### 示例

**生成一张表情包：**
```bash
xai-gen "dumbest trade meme: YOLO panic fail" --filename trade_meme.png
```

**批量生成：**
```bash
xai-gen "logo variations for tech startup" --n 5
# Outputs: out_1.png, out_2.png, out_3.png, out_4.png, out_5.png
```

**生成高质量的艺术作品：**
```bash
xai-gen "photorealistic portrait of a cat astronaut" --filename cat_astronaut.png
```

### 与 OpenClaw 的集成

该工具会输出 `MEDIA: /path/to/image.png`，OpenClaw 会自动检测并将该图片附加到消息中。您可以在代理工作流程中使用该工具：

```bash
# In an agent skill or automation
xai-gen "chart showing Q1 sales data" --filename sales_chart.png
# → Image auto-attaches to response
```

## API 详细信息

- **端点：** `https://api.x.ai/v1/images/generations`
- **模型：** `grok-imagine-image`
- **认证方式：** 通过 `XAI_API_KEY` 使用 bearer token 进行认证
- **速率限制：** 遵循 xAI API 的限制（请参阅 xAI 的官方文档）
- **超时设置：** 生成时间为 60 秒，下载时间为 30 秒

## 错误处理

该工具能够优雅地处理以下常见错误：

- ❌ API 密钥缺失 → 提供清晰的提示
- ❌ 网络错误 → 显示详细的错误信息
- ❌ API 超时 → 提供重试建议
- ❌ 参数无效 → 提供使用提示
- ❌ 文件写入错误 → 检查权限是否足够

## 系统要求

- **Python：** 3.7 及以上版本
- **依赖库：** `requests`
- **API 密钥：** xAI 的 API 密钥（从 https://console.x.ai 获取）
- **网络连接：** 需要互联网连接

## 平台兼容性

- ✅ Linux（已在 Raspberry Pi 上测试通过）
- ✅ macOS
- ✅ Windows（通过 WSL 或原生 Python 运行）
- ✅ ARM64 / ARMv7（兼容 Raspberry Pi，基于纯 API 调用）

## 故障排除

**“XAI_API_KEY 未找到”**
```bash
export XAI_API_KEY="xai-..."
```

**“requests 库未找到”**
```bash
pip3 install requests
```

**权限被拒绝**
```bash
chmod +x xai-gen
```

**API 错误**
- 检查 API 密钥的有效性
- 确认账户是否有足够的信用额度
- 查看 xAI 的状态页面

## 许可证

MIT 许可证——免费使用和修改

## 开发者

由 subagent xAI Image Gen Skill Builder 为 OpenClaw 开发

## 版本

1.0.0 — 初始版本