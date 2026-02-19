---
name: removebg-api
description: 使用 `remove.bg` API 移除图片背景，该 API 需要通过 API 密钥进行身份验证，并输出透明 PNG 格式的图片。适用于需要高质量图片裁剪且可以接受云处理的场景。
metadata:
  {
    "openclaw": {
      "requires": { "bins": ["uv", "python3"], "env": ["REMOVE_BG_API_KEY"] },
      "primaryEnv": "REMOVE_BG_API_KEY"
    }
  }
---
# removebg-api

使用 `remove.bg` 工具可进行高质量的背景去除处理。

## API 密钥设置

1. 访问 `https://www.remove.bg/dashboard#api-key` 进行注册或登录。
2. 创建 API 密钥。
3. 在 OpenClaw 的配置文件（`openclaw.json`）中配置 `REMOVE_BG_API_KEY`，确保其在运行时环境中可用。

## 重要说明

- 技能元数据（`requires.env`）声明 `REMOVE_BG_API_KEY` 是必需的。
- 元数据不会自动加载 shell 环境变量文件。
- 建议通过 OpenClaw 配置管理的方式来提供 API 密钥。

## 使用方法（推荐使用 `uv`）

从技能目录中运行以下命令：

```bash
uv run scripts/removebg_api.py --input /path/in.jpg --output /path/out.png
```

可选参数：

- `--size auto|preview|full|4k` （默认值：`auto`）
- `--format png|jpg|zip` （默认值：`png`）

安全注意事项：

- `--input` 参数必须指向位于 OpenClaw 工作区内的真实图像文件。
- 允许的输入格式：`.png`、`.jpg`、`.jpeg`、`.webp`（通过扩展名和魔法字节进行验证）。
- `--output` 参数指定的输出文件必须位于工作区的 `outputs/removebg-api/` 目录下。
- 系统会拒绝过大或不符合尺寸限制的文件，以防止文件被随意读写。

示例：

```bash
uv run scripts/removebg_api.py --input ./input.jpg --output ./output.png --size auto --format png
```

## 备用方案（不使用 `uv`）

```bash
python3 scripts/removebg_api.py --input ./input.jpg --output ./output.png
```

## 输出结果

- 将处理后的文件写入 `--output` 指定的路径。
- 会在聊天工作流中输出 `MEDIA:` 信息。

## 注意事项

- 使用 API 可能会消耗免费信用或付费配额。
- 技能文档中不需要指定绝对路径；示例中应使用相对路径。