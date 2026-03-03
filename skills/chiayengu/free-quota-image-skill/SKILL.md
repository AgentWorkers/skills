---
name: free-quota-image-skill
description: 使用一个优先考虑免费配额的多服务提供商工作流程，将文本转换为图像。当用户需要文本到图像的转换服务（支持Hugging Face、Gitee、ModelScope、A4F以及兼容OpenAI的私有端点）时，可以使用此技能。该流程包括：在配额或授权失败时自动使用令牌池进行轮询；为Hugging Face提供公共API作为备用方案；对生成提示进行优化；支持通过单个命令批量生成图像；以及生成结构化的输出结果。
metadata: {"openclaw":{"homepage":"https://github.com/Amery2010/peinture"}}
---
# 免费配额图像生成技能

## 概述

使用此技能可以运行一个与特定提供商无关的文本到图像的生成流程，该流程优先使用免费配额，支持令牌轮换以及提示优化功能。

## 工作流程

1. 从 `{baseDir}/assets/config.example.yaml` 文件或用户提供的配置文件中加载配置信息。
2. 确定提供商的顺序（`--provider auto` 会遵循 `routing-provider_order` 的设置）。
3. 根据提供商选择合适的模型（优先顺序为：`requested` → `z-image-turbo` → 默认提供商）。
4. 为每次生成请求准备提示内容：
   - 可选：针对目标模型进行自动翻译。
   - 可选：使用提供商提供的文本模型对提示内容进行优化。
5. 执行图像生成请求。
6. 如果遇到配额或授权问题，系统会自动轮换使用的令牌；如果令牌用尽，则切换到下一个提供商。
7. 当 `--count` 大于 1 时，重复生成流程，并为每个图像随机选择不同的提供商和令牌以分散负载。
8. 输出稳定的 JSON 数据或直接提供图像的 URL。

## 命令

### 安装依赖项：

```bash
python -m pip install -r {baseDir}/scripts/requirements.txt
```

### 运行图像生成：

```bash
python {baseDir}/scripts/run_text2img.py --prompt "cinematic rainy tokyo alley" --json
```

### 指定提供商和模型运行：

```bash
python {baseDir}/scripts/run_text2img.py --prompt "a fox astronaut" --provider gitee --model flux-2 --json
```

### 将生成的图像保存到本地：

```bash
python {baseDir}/scripts/run_text2img.py --prompt "retro sci-fi city" --output ./out.png
```

### 一次性生成多张图像：

```bash
python {baseDir}/scripts/run_text2img.py --prompt "anime passport portrait" --count 4 --json
```

## 命令行接口（CLI）规范

使用 `{baseDir}/scripts/run_text2img.py` 命令，并遵循以下规范：

- `--prompt` （必填）：生成图像时使用的提示文本。
- `--provider` （可选值：`auto` | `huggingface` | `gitee` | `modelscope` | `a4f` | `openai_compatible`，默认为 `auto`）：指定使用的图像生成服务。
- `--model` （默认值：`z-image-turbo`）：指定使用的图像生成模型。
- `--aspect-ratio` （默认值：`1:1`）：指定图像的宽高比。
- `--seed` （可选整数）：用于生成图像的随机种子值。
- `--steps` （可选整数）：生成图像的步骤数。
- `--guidance-scale` （可选浮点数）：用于控制生成过程的指导性参数。
- `--enable-hd` （标志）：是否启用高清晰度图像生成。
- `--optimize-prompt` / `--no-optimize-prompt` （默认值为 `on`）：是否对提示内容进行优化。
- `--auto-translate` / `--no-auto-translate` （默认值为 `off`）：是否自动翻译提示文本。
- `--config` （默认值：`{baseDir}/assets/config.example.yaml`）：配置文件的路径。
- `--output` （可选）：输出文件的路径。
- `--count` （生成图像的数量，默认为 1）。
- `--json` （可选）：是否以 JSON 格式输出结果。

## 输出格式

- 当使用 `--json` 选项时，成功生成的图像会包含以下字段：
  - `id`：图像的唯一标识符。
  - `url`：图像的 URL。
  - `provider`：使用的图像生成服务。
  - `model`：使用的图像生成模型。
  - `prompt_original`：原始提示文本。
  - `prompt_final`：优化后的提示文本。
  - `seed`：用于生成图像的随机种子值。
  - `steps`：生成图像所使用的步骤数。
  - `guidance-scale`：生成过程中的指导性参数。
  - `aspect_ratio`：图像的宽高比。
  - `fallback_chain`：在生成过程中使用的备用模型链。

- 如果生成失败，会输出以下错误信息：
  - `error_type`：错误类型。
  - `error`：具体的错误信息。
  - `fallback_chain`：在失败时使用的备用生成服务。

- 当 `--count` 大于 1 时，JSON 输出会包含以下内容：
  - `count`：生成的图像数量。
  - `images`：一个包含所有成功生成图像的数组。
  - `elapsed_ms`：生成所有图像所花费的总时间（以毫秒为单位）。

## 参考资料

仅阅读以下相关资料：

- 提供商 API 接口文档：`references/provider-endpoints.md`
- 模型覆盖范围和备用方案：`references/model-matrix.md`
- 令牌轮换规则：`references/token-rotation-policy.md`
- 提示优化流程：`references/prompt-optimization-policy.md`
- OpenClaw 集成细节：`references/openclaw-integration.md`

## 范围限制

本技能仅专注于文本到图像的核心功能，不包含图像编辑、视频生成或云存储相关功能。