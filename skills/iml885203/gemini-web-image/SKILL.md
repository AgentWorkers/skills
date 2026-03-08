---
name: gemini-web-image
description: "通过 Gemini Web API 使用 Google AI Pro 订阅服务生成图像。该服务使用浏览器 cookies 进行身份验证（无需 API 密钥）。适用场景：  
(1) 用户需要生成、创建、绘制或可视化任何内容；  
(2) 制作产品原型图、图表或概念艺术；  
(3) 使用类似“帮我画”、“生成一张图片”、“制作一张……的图像”等指令。  
**不适用于**：编辑或修改现有图像，以及视频生成。"
license: MIT
metadata:
  {
    "openclaw":
      {
        "emoji": "🎨",
        "requires":
          {
            "bins": ["uv"],
            "optionalPaths": ["~/.config/gemini/cookies.json"],
          },
        "install":
          [
            {
              "id": "uv",
              "kind": "brew",
              "formula": "uv",
              "bins": ["uv"],
              "label": "Install uv (brew)",
            },
          ],
      },
  }
---
# Gemini Web Image (Google AI Pro)

通过 Gemini Web API 使用 Gemini 3 Pro Image 生成图片。该脚本使用 Google AI Pro 的订阅 cookie 而非 API 密钥，因此无需支付费用或担心 API 配额限制。

## 设置

您需要拥有 **Google AI Pro 订阅**，并且确保 Chrome 浏览器已登录到 `gemini.google.com`。

**选项 A：自动方式（推荐）**
脚本会通过 `browser-cookie3` 自动读取 Chrome 浏览器中的 cookie。请确保在运行脚本的机器上 Chrome 已登录到 `gemini.google.com`。

**选项 B：手动管理 cookie（无头服务器）**
如果无法访问 Chrome 浏览器的 cookie，请参考以下代码块（```bash
mkdir -p ~/.config/gemini
# Get these values from Chrome DevTools → Application → Cookies → gemini.google.com
cat > ~/.config/gemini/cookies.json << 'EOF'
{"secure_1psid": "YOUR_VALUE", "secure_1psidts": "YOUR_VALUE"}
EOF
chmod 600 ~/.config/gemini/cookies.json
```）进行配置。

### Cookie 安全性

- ⚠️ **Cookie 是敏感信息**——它们用于访问您的 Google 账户会话。请仅在您控制的受信任机器上运行此脚本。
- Cookie 仅用于在 `gemini.google.com` 上进行身份验证，绝不会传输到第三方服务器。
- 脚本使用 `browser-cookie3`（读取 Chrome 的本地 cookie 存储）或手动提供的 JSON 文件来获取 cookie。所有 cookie 仅传输到 Google 自己的 API，不会离开您的机器。
- **请勿在共享或不受信任的系统中安装此脚本。**

### Python 依赖库

脚本使用 `uv` 来自动管理依赖关系。首次运行时，`uv` 会安装以下库：
- `gemini-webapi`：Gemini Web API 客户端
- `browser-cookie3`：用于读取 Chrome cookie 的工具
- `Pillow`：用于图像处理
- `numpy`：用于数组操作

无需手动执行 `pip install`，`uv run` 会自动完成所有依赖库的安装。

## 生成图片

```bash
uv run {baseDir}/scripts/generate.py --prompt "your image description" --output "output.png"
```

## 编辑图片（使用输入的图片文件）

```bash
uv run {baseDir}/scripts/generate.py --prompt "edit instructions" --output "output.png" --input "/path/to/input.png"
```

## 命令行参数

| 参数 | 说明 |
|------|-------------|
| `--prompt` | 图片描述或编辑指令 |
| `--output` | 输出文件路径（默认：在当前工作目录下自动生成） |
| `--input` | 需要编辑的输入图片文件（可选） |
| `--keep-chat` | 生成图片后保留 Gemini 的对话记录 |

## 注意事项

- 使用 Google AI Pro 的订阅配额，无需支付 API 使用费用 |
- 每次运行脚本时都会重新读取 Chrome 的 cookie，无需手动管理 cookie |
- 脚本会输出 `MEDIA:` 标签，以便 OpenClaw 在支持的聊天工具中自动插入图片 |
- 生成图片后 Gemini 的对话记录会自动删除，以避免文件杂乱（如需保留对话记录，请使用 `--keep-chat` 参数） |
- 文件名格式为 `yyyy-mm-dd-hh-mm-ss-name.png`，其中包含时间戳 |
- 通过消息工具发送图片后，请删除原始图片文件以节省存储空间 |

## 去水印

脚本支持通过反向 Alpha 混合（无损处理）技术自动去除图片中的水印。为此脚本提供了参考图片（`scripts/bg_48.png` 和 `scripts/bg_96.png`）。

独立使用方式：`uv run {baseDir}/scripts/remove_watermark.py input.png -o clean.png`

⚠️ **免责声明**：去除水印的功能可能违反 Google 的服务条款。此功能仅供个人使用，请用户确保遵守相关条款和当地法律法规。