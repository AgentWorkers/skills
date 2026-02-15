# Ollama x/z-image-turbo 技能

## 描述
通过 **Ollama**（`x/z-image-turbo` 模型）生成图像，并将其发送到 WhatsApp。

## 触发方式
当用户请求**生成/创建/绘制图像**（或类似操作）时，请按照以下步骤操作：

### 第一步 — 生成图像
使用 `exec` 命令，并设置 `pty=true`（必须）：
```bash
python3 /Users/openclaw/.openclaw/skills/ollama-x-z-image-turbo/runner.py \
  --prompt "<PROMPT>" \
  --width 1024 --height 1024 --steps 20 \
  --out /Users/openclaw/.openclaw/workspace/tmp/ollama_image.png -v
```

**重要提示**：
- `pty=true` 是必须的（Ollama 需要 TTY 接口）
- 建议设置 `timeout=120`（最短延迟时间）
- 根据用户需求调整 `--width`、`--height`、`--steps` 参数

### 第二步 — 发送到 WhatsApp
使用 **message** 工具发送图像：
```
action: send
channel: whatsapp
to: <numéro>
message: <légende>
filePath: /Users/openclaw/.openclaw/workspace/tmp/ollama_image.png
```

## 可用参数
| 参数          | 默认值    | 描述                        |
|--------------|---------|---------------------------|
| --prompt     | 必填     | 图像的描述                    |
| --width       | 1024     | 图像的宽度（像素）                |
| --height      | 1024     | 图像的高度（像素）                |
| --steps      | 20       | 图像的去噪步骤数                |
| --seed       | random    | 用于保证图像一致性的随机种子值         |
| --negative    | optional | 是否使用负数提示（例如：“-”）           |
| --timeout     | 300      | 超时时间（秒）                    |

## 用户示例请求：
- “生成一张宇航员和猫的图片”
- “为我画一幅日落的插图”
- “在森林里画一个机器人”
- “制作一张……的图片”

## 前提条件：
- Ollama 已在 `http://127.0.0.1:11434` 上运行
- 安装了 `x/z-image-turbo:latest` 模型