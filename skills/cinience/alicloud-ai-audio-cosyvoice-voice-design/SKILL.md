---
name: alicloud-ai-audio-cosyvoice-voice-design
description: 在使用 Alibaba Cloud Model Studio 的 CosyVoice 定制模型（尤其是 cosyvoice-v3.5-plus 或 cosyvoice-v3.5-flash）设计自定义语音时，建议先根据语音提示生成预览文本，然后再使用返回的 `voice_id` 进行文本转语音（TTS）操作。
version: 1.0.0
---
**类别：提供者（Provider）**  
**# Model Studio CosyVoice 语音设计（Model Studio CosyVoice Voice Design）**  

使用 CosyVoice 语音注册 API，根据自然语言描述创建定制化的语音。  

## 关键模型名称（Critical Model Names）  
使用 `model="voice-enrollment"` 以及以下 `target_model` 值之一：  
- `cosyvoice-v3.5-plus`  
- `cosyvoice-v3.5-flash`  
- `cosyvoice-v3-plus`  
- `cosyvoice-v3-flash`  

**本仓库推荐的默认值：**  
`target_model="cosyvoice-v3.5-plus"`  

## 地区与兼容性（Region and Compatibility）  
- `cosyvoice-v3.5-plus` 和 `cosyvoice-v3-flash` 仅支持在中国大陆的部署模式（北京端点）。  
- 在国际部署模式（新加坡端点）下，`cosyvoice-v3.5-plus` 和 `cosyvoice-v3-flash` 不支持语音克隆/设计功能。  
- `target_model` 必须与实际使用的语音合成模型相匹配。  

## 端点（Endpoint）  
- 国内：`https://dashscope.aliyuncs.com/api/v1/services/audio/tts/customization`  
- 国际：`https://dashscope-intl.aliyuncs.com/api/v1/services/audio/tts/customization`  

## 先决条件（Prerequisites）  
- 在您的环境中设置 `DASHSCOPE_API_KEY`，或将 `dashscope_api_key` 添加到 `~/.alibabacloud/credentials` 文件中。  

## 标准化接口（Standardized Interface）  
### 请求（Request）  
- `model`（字符串，可选）：固定为 `voice-enrollment`  
- `target_model`（字符串，可选）：默认值为 `cosyvoice-v3.5-plus`  
- `prefix`（字符串，必填）：仅允许字母和数字，最多 10 个字符  
- `voice_prompt`（字符串，必填）：最多 500 个字符，仅支持中文或英文  
- `preview_text`（字符串，必填）：最多 200 个字符，仅支持中文或英文  
- `language_hints`（字符串数组，可选）：`zh` 或 `en`，且应与 `preview_text` 语言一致  
- `sample_rate`（整数，可选）：例如 `24000`  
- `response_format`（字符串，可选）：例如 `wav`  

### 响应（Response）  
- `voice_id`（字符串）  
- `request_id`（字符串）  
- `status`（字符串，可选）  

## 操作指南（Operational Guidelines）  
- 请确保 `voice_prompt` 中明确指定语音的音色、年龄范围、语速、情感、发音方式以及使用场景。  
- 如果使用了 `language_hints`，其语言应与 `preview_text` 保持一致。  
- 定制化语音的名称在生成的文件名中会包含 `-vd-` 标识。  

## 本地辅助脚本（Local Helper Script）  
准备一个格式化的请求 JSON 数据：  
```bash
python skills/ai/audio/alicloud-ai-audio-cosyvoice-voice-design/scripts/prepare_cosyvoice_design_request.py \
  --target-model cosyvoice-v3.5-plus \
  --prefix announcer \
  --voice-prompt "沉稳的中年男性播音员，低沉有磁性，语速平稳，吐字清晰。" \
  --preview-text "各位听众朋友，大家好，欢迎收听晚间新闻。" \
  --language-hint zh
```  

## 验证（Validation）  
执行相关命令后，如果命令返回 0 且生成了 `output/alicloud-ai-audio-cosyvoice-voice-design/validate.txt` 文件，则验证通过。  

## 输出与证据（Output and Evidence）  
- 将所有生成的文件、命令输出结果以及 API 响应摘要保存在 `output/alicloud-ai-audio-cosyvoice-voice-design/` 目录下。  
- 确保在证据文件中包含 `target_model`、`prefix`、`voice_prompt` 和 `preview_text` 的信息。  

## 参考资料（References）  
- `references/api_reference.md`  
- `references/sources.md`