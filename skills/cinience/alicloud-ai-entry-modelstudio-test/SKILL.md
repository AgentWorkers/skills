---
name: alicloud-ai-entry-modelstudio-test
description: 针对此仓库中存在的 Model Studio 技能（包括图像/视频/音频处理、实时语音处理、通用处理（omni）、视觉推理、嵌入技术、重新排序（rerank）以及编辑功能），运行一个最小的测试矩阵。针对每项技能执行一个简单的请求，并记录相应的结果。
version: 1.0.0
---
**类别：任务**  
# Model Studio技能最小测试  

针对当前仓库中可用的Model Studio技能，运行最小范围的验证并记录测试结果。  

## 先决条件  
- 安装SDK（建议使用虚拟环境以避免PEP 668的限制）：  
```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install dashscope
```  
- 配置`DASHSCOPE_API_KEY`（优先使用环境变量；或者从`~/.alibabacloud/credentials`文件中读取）。  

## 支持的测试项目（当前支持）  
1) 文本转图像 → `skills/ai/image/alicloud-ai-image-qwen-image/`  
2) 图像编辑 → `skills/ai/image/alicloud-ai-image-qwen-image-edit/`  
3) 文本转视频 / 图像转视频（i2v） → `skills/ai/video/alicloud-ai-video-wan-video/`  
4) 参考视频转视频（r2v） → `skills/ai/video/alicloud-ai-video-wan-r2v/`  
5) 文本转语音（TTS） → `skills/ai/audio/alicloud-ai-audio-tts/`  
6) 自动语音识别（ASR，非实时） → `skills/ai/audio/alicloud-ai-audio-asr/`  
7) 实时自动语音识别（ASR） → `skills/ai/audio/alicloud-ai-audio-asr-realtime/`  
8) 实时文本转语音（TTS） → `skills/ai/audio/alicloud-ai-audio-tts-realtime/`  
9) 实时语音翻译 → `skills/ai/audio/alicloud-ai-audio-livetranslate/`  
10) CosyVoice语音克隆 → `skills/ai/audio/alicloud-ai-audio-cosyvoice-voice-clone/`  
11) CosyVoice语音设计 → `skills/ai/audio/alicloud-ai-audio-cosyvoice-voice-design/`  
12) 语音克隆 → `skills/ai/audio/alicloud-ai-audio-tts-voice-clone/`  
13) 语音设计 → `skills/ai/audio/alicloud-ai-audio-tts-voice-design/`  
14) 全模态交互（Omni Multimodal） → `skills/ai/multimodal/alicloud-ai-multimodal-qwen-omni/`  
15) 视觉推理 → `skills/ai/multimodal/alicloud-ai-multimodal-qvq/`  
16) 文本嵌入 → `skills/ai/search/alicloud-ai-search-text-embedding/`  
17) 重新排序 → `skills/ai/search/alicloud-ai-search-rerank/`  
18) 视频编辑 → `skills/ai/video/alicloud-ai-video-wan-edit/`  

如果需要测试新的功能，请先创建相应的技能（使用`skills/ai/misc/alicloud-ai-misc-crawl-and-skill/`来更新模型列表）。  

## 每项功能的测试流程  
1. 打开目标子技能目录并读取`SKILL.md`文件。  
2. 选择一个最小的输入示例和推荐的模型。  
3. 运行SDK调用或相关脚本。  
4. 记录模型的运行结果、请求摘要、响应摘要、耗时以及状态。  

## 结果模板  
将测试结果保存为`output/alicloud-ai-entry-modelstudio-test-results.md`：  
```
# Model Studio Skill Test Results

- Date: YYYY-MM-DD
- Environment: region / API_BASE / auth method

| Capability | Sub-skill | Model | Request summary | Result summary | Status | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| Text-to-image | alicloud-ai-image-qwen-image | <model-id> | ... | ... | pass/fail | ... |
| Image editing | alicloud-ai-image-qwen-image-edit | <model-id> | ... | ... | pass/fail | ... |
| Image-to-video (i2v) | alicloud-ai-video-wan-video | <model-id> | ... | ... | pass/fail | ... |
| Reference-to-video (r2v) | alicloud-ai-video-wan-r2v | <model-id> | ... | ... | pass/fail | ... |
| TTS | alicloud-ai-audio-tts | <model-id> | ... | ... | pass/fail | ... |
| ASR (non-realtime) | alicloud-ai-audio-asr | <model-id> | ... | ... | pass/fail | ... |
| Realtime ASR | alicloud-ai-audio-asr-realtime | <model-id> | ... | ... | pass/fail | ... |
| Realtime TTS | alicloud-ai-audio-tts-realtime | <model-id> | ... | ... | pass/fail | ... |
| Live speech translation | alicloud-ai-audio-livetranslate | <model-id> | ... | ... | pass/fail | ... |
| CosyVoice voice clone | alicloud-ai-audio-cosyvoice-voice-clone | <model-id> | ... | ... | pass/fail | ... |
| CosyVoice voice design | alicloud-ai-audio-cosyvoice-voice-design | <model-id> | ... | ... | pass/fail | ... |
| Voice clone | alicloud-ai-audio-tts-voice-clone | <model-id> | ... | ... | pass/fail | ... |
| Voice design | alicloud-ai-audio-tts-voice-design | <model-id> | ... | ... | pass/fail | ... |
| Omni multimodal | alicloud-ai-multimodal-qwen-omni | <model-id> | ... | ... | pass/fail | ... |
| Visual reasoning | alicloud-ai-multimodal-qvq | <model-id> | ... | ... | pass/fail | ... |
| Text embedding | alicloud-ai-search-text-embedding | <model-id> | ... | ... | pass/fail | ... |
| Rerank | alicloud-ai-search-rerank | <model-id> | ... | ... | pass/fail | ... |
| Video editing | alicloud-ai-video-wan-edit | <model-id> | ... | ... | pass/fail | ... |
```  

## 失败处理  
- 如果参数不明确，请查阅目标子技能的`SKILL.md`文件或相关参考文档。  
- 如果模型不可用，请更新模型列表并重试。  
- 对于认证问题，请检查`DASHSCOPE_API_KEY`（环境变量或`~/.alibabacloud/credentials`文件中的设置）。  

## 验证标准  
测试通过的条件：命令执行成功（退出代码为0），并且生成`output/alicloud-ai-entry-modelstudio-test/validate.txt`文件。  

## 输出与证据  
- 将测试结果、命令输出以及API响应摘要保存在`output/alicloud-ai-entry-modelstudio-test/`目录下。  
- 在证据文件中包含关键参数（地区、资源ID、时间范围等信息），以便后续重现测试结果。  

## 工作流程  
1) 确认用户的操作意图、所在地区以及操作的类型（只读或可修改）。  
2) 首先运行一个只读查询，以验证连接性和权限。  
3) 使用明确的参数和有限的权限范围执行目标操作。  
4) 验证结果并保存输出文件和证据文件。  

## 参考资料  
- 资源列表：`references/sources.md`