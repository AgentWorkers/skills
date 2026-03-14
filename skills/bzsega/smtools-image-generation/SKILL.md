---
name: smtools-image-generation
description: 使用 OpenRouter 或 Kie.ai 等 AI 模型根据文本提示生成图像。当用户请求生成、创建、绘制或说明图像时，可以使用此功能。
metadata:
  openclaw:
    requires:
      bins:
        - python3
      env:
        - OPENROUTER_API_KEY
    primaryEnv: OPENROUTER_API_KEY
    optionalEnv:
      - KIE_API_KEY
---
# 图像生成技能

该技能可根据文本提示生成图像。默认提供者是 **OpenRouter**（同步方式），也可使用 **Kie.ai**（异步方式，基于任务执行）。

## 何时激活

当用户需要执行以下操作时，激活此技能：
- 生成图像、绘制图形、创作插画或渲染图像
- 制作图片、艺术作品、照片或插画
- 将某些内容以图像形式呈现

## 使用方法

请使用绝对路径运行生成脚本，以避免出现目录路径变更的提示：

```bash
bash SKILL_DIR/scripts/run.sh --prompt "PROMPT" [OPTIONS]
```

请将 `SKILL_DIR` 替换为该技能根目录的绝对路径。

### 配置选项

| 标志 | 描述 |
|------|-------------|
| `-p, --prompt` | 文本提示（必需） |
| `--provider` | `openrouter`（默认）或 `kie` |
| `-m, --model` | 模型名称（取决于所选提供者） |
| `-o, --output` | 输出文件路径 |
| `-c, --config` | 配置文件（config.json）的路径 |
| `--list-models` | 显示可用模型列表 |
| `-v, --verbose` | 将调试信息输出到标准错误流（stderr） |

### 输出结果

脚本会将生成的图像信息以 JSON 格式输出到标准输出（stdout）：

```json
{"status": "ok", "image_path": "/absolute/path/to/image.png", "model": "google/gemini-3.1-flash-image-preview", "provider": "openrouter"}
```

生成成功后，向用户显示图像的路径，并确认图像已成功创建。

## 提供者选择

- **OpenRouter**（默认）：处理速度快，操作同步。支持的模型包括：`google/gemini-3.1-flash-image-preview`、`google/imagen-4`、`stabilityai/stable-diffusion-3`。需要配置 `OPENROUTER_API_KEY`。
- **Kie.ai**：基于异步任务执行。支持的模型包括：`flux-ai`、`midjourney`、`google-4o-image`、`ghibli-ai`。需要配置 `KIE_API_KEY`。仅在用户明确要求使用 Kie.ai 或其特定模型时使用。

## 使用示例

- 基本生成示例：
```bash
bash SKILL_DIR/scripts/run.sh -p "A serene mountain lake at sunset"
```

- 使用特定模型生成图像：
```bash
bash SKILL_DIR/scripts/run.sh -p "Cyberpunk cityscape" -m "google/imagen-4"
```

- 使用 Kie.ai 生成图像：
```bash
bash SKILL_DIR/scripts/run.sh -p "Studio Ghibli forest" --provider kie -m ghibli-ai
```

- 指定自定义输出路径：
```bash
bash SKILL_DIR/scripts/run.sh -p "A red fox" -o /tmp/fox.png
```

## 错误处理

| 错误类型 | 处理方式 |
|-------|--------|
| API 密钥缺失 | 告知用户设置环境变量 `OPENROUTER_API_KEY` 或 `KIE_API_KEY` |
- 网络连接/超时错误 | 重试一次；如果仍无法解决问题，通知用户 |
- 生成失败（无图像返回） | 显示 JSON 输出中的错误信息 |
- Kie.ai 任务超时 | 告知用户生成过程耗时过长，建议用户重新尝试

## 设置说明

如果该技能尚未配置，请运行以下命令进行初始化：
```bash
bash SKILL_DIR/setup.sh
```

## 安全注意事项

- 绝不要显示或记录 API 密钥 |
- 未经用户许可，严禁修改配置文件（config.json）。