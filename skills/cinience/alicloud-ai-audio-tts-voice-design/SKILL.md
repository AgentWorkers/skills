---
name: alicloud-ai-audio-tts-voice-design
description: 使用阿里云Model Studio Qwen TTS VD模型进行语音设计的工作流程。适用于从文本描述创建自定义合成语音，并将其用于语音合成。
version: 1.0.0
---
**类别：提供者（Provider）**

# Model Studio Qwen TTS 语音设计（Model Studio Qwen TTS Voice Design）

使用语音设计模型，根据自然语言描述生成可控的合成语音。

## 关键模型名称（Critical Model Names）

请使用以下模型字符串之一：
- `qwen3-tts-vd-2026-01-26`
- `qwen3-tts-vd-realtime-2026-01-15`

## 先决条件（Prerequisites）

- 在虚拟环境中安装 SDK：

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install dashscope
```

- 将 `DASHSCOPE_API_KEY` 设置在环境变量中，或将 `dashscope_api_key` 添加到 `~/.alibabacloud/credentials` 文件中。

## 标准化接口（Normalized Interface, tts.voice_design）

### 请求（Request）
- `voice_prompt`（字符串，必填）：目标语音描述
- `text`（字符串，必填）
- `stream`（布尔值，可选）

### 响应（Response）
- `audio_url`（字符串）：生成的音频文件链接
- `voice_id`（字符串）：语音 ID
- `request_id`（字符串）：请求 ID

## 操作指南（Operational Guidance）

- 在编写语音提示时，需考虑语调、语速、情感和音色等因素。
- 为确保产品一致性，可以构建一个可重用的语音提示库。
- 在执行长时间运行的脚本之前，先对生成的语音进行简短的语音测试。

## 本地辅助脚本（Local Helper Script）

准备一个标准化的请求 JSON 数据，并验证响应格式：

```bash
.venv/bin/python skills/ai/audio/alicloud-ai-audio-tts-voice-design/scripts/prepare_voice_design_request.py \
  --voice-prompt "A warm female host voice, clear articulation, medium pace" \
  --text "This is a voice-design demo"
```

## 输出位置（Output Location）

- 默认输出路径：`output/ai-audio-tts-voice-design/audio/`
- 可通过设置 `OUTPUT_DIR` 变量来覆盖默认路径。

## 验证（Validation）

```bash
mkdir -p output/alicloud-ai-audio-tts-voice-design
for f in skills/ai/audio/alicloud-ai-audio-tts-voice-design/scripts/*.py; do
  python3 -m py_compile "$f"
done
echo "py_compile_ok" > output/alicloud-ai-audio-tts-voice-design/validate.txt
```

验证标准：命令执行成功（退出状态码为 0），并且会生成 `output/alicloud-ai-audio-tts-voice-design/validate.txt` 文件。

## 输出结果与证据（Output and Evidence）

- 将所有生成的结果文件、命令输出以及 API 响应摘要保存在 `output/alicloud-ai-audio-tts-voice-design/` 目录下。
- 在证据文件中记录关键参数（区域、资源 ID、时间范围等信息），以便后续复现操作。

## 工作流程（Workflow）

1) 确认用户意图、所选区域、相关标识符，以及操作是只读还是可修改的。
2) 首先运行一个最小的只读查询，以验证连接性和权限。
3) 使用明确的参数和有限的权限范围执行目标操作。
4) 验证操作结果，并保存输出文件和证据文件。

## 参考资料（References）

- `references/sources.md`