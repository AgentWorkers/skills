---
name: comfyui-imagegen
description: 通过 ComfyUI API（地址：localhost:8188）使用 Flux2 工作流程生成图像。支持直接将结构化 JSON 数据作为正则提示参数（positive prompt parameter）发送，并允许自定义种子值（seed）和生成步骤（steps）。采用子代理（sub-agent）实现异步监控，以实现低延迟、高效的数据轮询（每 5 秒一次）。
---

# ComfyUI ImageGen

## 更新日志

- **[2026-02-11 20:42 EST]**: **v1.5.0** - 修复了 `--structured-prompt` 参数的使用问题（不再需要指定位置参数）；工作流程更新为 1920x1080 16:9 的分辨率；已准备好在生产环境中使用，并进行了实时测试（JSON 数据直接发送到 ComfyUI，通过异步子代理进行处理）。
- **[2026-02-11 10:10 EST]**: **v1.4.0** - 重构了提示生成机制：代理将人类输入的提示转换为结构化的 JSON 字符串；脚本直接将 JSON 数据发送给 ComfyUI（不再进行文字转换）。新增了关于如何在图片中插入文本的规则。

## 更新日志
- **[2026-02-11 10:10 EST]**: **v1.4.0** - 重构了提示生成机制：代理将人类输入的提示转换为结构化的 JSON 字符串；脚本直接将 JSON 数据发送给 ComfyUI（不再进行文字转换）。新增了关于如何在图片中插入文本的规则。
- **[2026-02-11 09:52 EST]**: **v1.3.0** - 脚本现在可以直接接受结构化的 JSON 数据（内部会自动生成相应的文字描述）；移除了代理端的文字生成步骤。更新了使用说明和示例。
- **[2026-02-11 09:20 EST]**: **v1.2.0** - 新增了对结构化提示的解析功能：将人类输入的请求转换为 JSON 格式的数据，并自动生成优化的 Flux.2 文本描述。更新了文档说明。
- **[2026-02-11 00:15 EST]**: **v1.1.0** - 新增了 `--submit-only`（仅提交结果）和 `--watch prompt_id`（监控提示 ID）模式。SKILL.md 文档中的异步处理流程如下：提交结果 → `sessions_spawn` 子代理（每 5 秒轮询一次，并自动将生成的图片发送到 Telegram；相比主代理方式，这种方式可以节省约 10 倍的 API 访问次数）。
- **[2026-02-11 04:05 EST]**: **v1.0.3** - 新增了关于 Flux.2 [klein] 9B 提示生成的最佳实践部分，内容来自 Black Forest Labs 和 fal.ai 的指导建议。
- **[2026-02-10 23:05]**: **v1.0.2** - 更新了工作流程（版本 3）：增加了“带提示/信息的图片保存”功能（节点 85），以改进元数据的嵌入效果。脚本已更新为轮询节点 85。
- **[2026-02-10 23:00]**: 明确要求在生成图片后必须通过 `message` 工具将图片发送给用户。
- **[2026-02-10]**: 更新了工作流程：输出格式为 JPG 图片，其中包含提示和元数据（使用“带提示的图片保存”功能）。模型更新为 `darkBeastFeb0826Latest_dbkBlitzV15.safetensors`。脚本现在轮询节点 84。

## 使用方法

1. 代理将人类输入的请求转换为结构化的 JSON 数据。
2. 确保 ComfyUI 在 `localhost:8188` 上运行。
3. **异步模式（推荐）**：
   ```
   1. exec python skills/comfyui-imagegen/scripts/generate.py --structured-prompt '{"subjects":[{"description":"fluffy tabby cat","position":"center","action":"sitting relaxed"}],"scene":"cozy room interior","lighting":"warm golden sunset rays","mood":"serene and peaceful","camera":{"angle":"low angle"}}' --submit-only → parse prompt_id
   2. sessions_spawn task="Set-Location 'C:\\Users\\hal\\.openclaw\\workspace'; python skills/comfyui-imagegen/scripts/generate.py --watch '{prompt_id}' --output ./gen-{prompt_id}.jpg; message action=send channel=telegram target=595846104 media=./gen-{prompt_id}.jpg; Remove-Item ./gen-{prompt_id}.jpg" label="img-{prompt_id}" cleanup=delete runTimeoutSeconds=180
   ```
   - 监控器每 5 秒轮询 `/history/{prompt_id}`（最佳延迟：<5 秒；每 60 秒最多轮询 12 次；使用独立的 API 访问令牌）。
   - 完成生成后自动将 JPG 图片发送到指定的聊天频道（子代理会发送确认信号）。
   - 通过 `spawn runTimeoutSeconds=120` 参数设置超时时间。
4. **同步模式**（阻塞代理执行）：
   ```
   exec python skills/comfyui-imagegen/scripts/generate.py --structured-prompt '{"scene":"your scene"}' [--seed N] [--steps 10] [--output ./my.jpg] [--host localhost:8188]
   message action=send channel=telegram media=./my.jpg
   ```

## 自定义参数
| 参数 | 默认值 | 备注 |
|-----|---------|-------|
| `--seed` | 随机值 | 用于生成唯一标识符 |
| `--steps` | 5 | 图像质量设置（范围：20-50） |
| `--host` | localhost:8188 | 远程服务器地址 |
| `--output` | gen-{seed/pid}.jpg | 图片输出路径 |

## 结构化提示格式（必填）

**代理步骤 1**：将人类输入的自然语言请求转换为以下结构化的 JSON 数据（所有字段均为可选；仅填充相关内容；`subjects` 数组可以包含多个元素）。

**规则**：对于图片中的文字（如标志、徽标），需要在描述或动作字段中使用双引号括起来，例如：`"sign reading \"STOP\""` 或 `"logo with text \"OpenClaw\"`。

```json
{
  "scene": "overall scene description",
  "subjects": [
    {
      "description": "detailed subject description",
      "position": "where in frame",
      "action": "what they're doing"
    }
  ],
  "style": "artistic style",
  "color_palette": ["#FF0000", "#00AACC"],
  "lighting": "lighting description",
  "mood": "emotional tone",
  "background": "background details",
  "composition": "framing and layout",
  "camera": {
    "angle": "camera angle",
    "lens": "lens type",
    "depth_of_field": "focus behavior"
  }
}
```

**代理步骤 2**：将 JSON 数据转换为字符串（格式紧凑，适合 shell 环境中的转义操作），然后通过 `--structured-prompt` 参数传递给脚本；脚本会直接将 JSON 数据作为 ComfyUI 的提示内容发送。

**示例**：

**用户输入**：“夕阳时分，一只猫坐在窗台上”

**结构化的 JSON 数据**（用于 `--structured-prompt` 参数）：
```bash
'{"subjects":[{"description":"fluffy tabby cat","position":"center","action":"sitting relaxed"}],"scene":"cozy room interior","lighting":"warm golden sunset rays","mood":"serene and peaceful","camera":{"angle":"low angle"}}'
```

## 工作流程详情
- 脚本会轮询节点 **85**（“带提示/信息的图片保存”功能）。
- 使用的模型：`darkBeastFeb0826Latest_dbkBlitzV15.safetensors`
- 使用的模板：`workflows/flux2.json`

## 提示生成的最佳实践（Flux.2 [klein] 9B）
- 使用描述性的语言，而非关键词。提示内容应包含场景、光线和氛围等信息。
- 例如：“黎明时分，宁静的山湖，薄雾升起，金色的光线穿透山峰，画面效果非常逼真。”
- 参考来源：[BFL](https://docs.bfl.ml/guides/prompting_guide_flux2_klein)，[fal.ai](https://fal.ai/learn/devs/flux-2-klein-prompt-guide)

## 示例
```bash
# Async test (structured JSON string → direct positive prompt)
python .../generate.py --structured-prompt '{"subjects":[{"description":"fluffy tabby cat","position":"center","action":"sitting relaxed"}],"scene":"cozy room interior","lighting":"warm golden sunset rays","mood":"serene and peaceful","camera":{"angle":"low angle"}}' --submit-only --steps 10
# → prompt_id=abc123; spawn watcher sub-agent
```

**注意**：对于 cron 任务的替代方案（效率较低）：可以使用 `cron add` 命令一次性执行 `at=now+10s`，并将 `payload.systemEvent="Check img job {prompt_id}"` 作为参数；不过建议使用 `spawn` 命令来处理图片生成任务。