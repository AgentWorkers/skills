---
name: alicloud-ai-entry-modelstudio
description: 将 Alibaba Cloud Model Studio 的请求路由到相应的本地技能（Qwen Image、Qwen Image Edit、Wan Video、Wan R2V、Qwen TTS、Qwen ASR 以及高级 TTS 变体）。当用户请求使用 Model Studio 但没有指定具体功能时，请使用此方法。
version: 1.0.0
---
**类别：任务**  
# 阿里云模型工作室入口（路由）  
将请求路由到现有的本地技能，以避免重复模型/参数信息。  

## 先决条件  
- 安装 SDK（建议使用虚拟环境，以避免 PEP 668 的限制）：  
```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install dashscope
```  
- 配置 `DASHSCOPE_API_KEY`（建议使用环境变量；或在 `~/.alibabacloud/credentials` 文件中设置 `dashscope_api_key`）。  

## 路由表（当前此仓库支持的路由）  
| 需求 | 目标技能 |  
| --- | --- |  
| 文本转图像/图像生成 | `skills/ai/image/alicloud-ai-image-qwen-image/` |  
| 图像编辑 | `skills/ai/image/alicloud-ai-image-qwen-image-edit/` |  
| 文本转视频/图像转视频（i2v） | `skills/ai/video/alicloud-ai-video-wan-video/` |  
| 参考视频（r2v） | `skills/ai/video/alicloud-ai-video-wan-r2v/` |  
| 文本转语音（TTS） | `skills/ai/audio/alicloud-ai-audio-tts/` |  
| 语音识别/转录（ASR） | `skills/ai/audio/alicloud-ai-audio-asr/` |  
| 实时语音识别 | `skills/ai/audio/alicloud-ai-audio-asr-realtime/` |  
| 实时 TTS | `skills/ai/audio/alicloud-ai-audio-tts-realtime/` |  
| 实时语音翻译 | `skills/ai/audio/alicloud-ai-audio-livetranslate/` |  
| CosyVoice 语音克隆 | `skills/ai/audio/alicloud-ai-audio-cosyvoice-voice-clone/` |  
| CosyVoice 语音设计 | `skills/ai/audio/alicloud-ai-audio-cosyvoice-voice-design/` |  
| 语音克隆 | `skills/ai/audio/alicloud-ai-audio-tts-voice-clone/` |  
| 语音设计 | `skills/ai/audio/alicloud-ai-audio-tts-voice-design/` |  
| 全模态交互 | `skills/ai/multimodal/alicloud-ai-multimodal-qwen-omni/` |  
| 视觉推理 | `skills/ai/multimodal/alicloud-ai-multimodal-qvq/` |  
| 文本嵌入 | `skills/ai/search/alicloud-ai-search-text-embedding/` |  
| 重新排序 | `skills/ai/search/alicloud-ai-search-rerank/` |  
| 向量检索 | `skills/ai/search/alicloud-ai-search-dashvector/` 或 `skills/ai/search/alicloud-ai-search-opensearch/` 或 `skills/ai/search/alicloud-ai-search-milvus/` |  
| 文本理解 | `skills/ai/text/alicloud-ai-text-document-mind/` |  
| 视频编辑 | `skills/ai/video/alicloud-ai-video-wan-edit/` |  
| 模型列表爬取/更新 | `skills/ai/misc/alicloud-ai-misc-crawl-and-skill/` |  

## 当请求未匹配时  
- 先明确模型的功能及输入/输出类型。  
- 如果仓库中缺少所需功能，请先添加新的技能。  

## 本仓库中常见的缺失功能（待补充）  
- 文本生成/聊天（LLM）  
- 多模态嵌入  
- OCR 专用提取和图像翻译  
- 虚拟试穿/数字人/高级视频人物模型  

- 对于多模态/ASR 下载失败的情况，请优先使用上述列出的公共 URL。  
- 如 ASR 参数出现错误，请在 `input_audio.data` 中使用数据 URI。  
- 如果多模态嵌入请求返回 400 错误，请确保 `input_contents` 是一个数组。  

## 异步任务轮询模板（针对长时间运行的任务）  
当 `X-DashScope-Async: enable` 返回 `task_id` 时，按以下方式轮询：  
```
GET https://dashscope.aliyuncs.com/api/v1/tasks/<task_id>
Authorization: Bearer $DASHSCOPE_API_KEY
```  

**示例结果字段（成功情况）：**  
```
{
  "output": {
    "task_status": "SUCCEEDED",
    "video_url": "https://..."
  }
}
```  

**注意事项：**  
- 建议的轮询间隔：15-20 秒，最多尝试 10 次。  
- 成功后，下载 `output.video_url`。  

## 需要澄清的问题（在不确定时询问）  
1. 您需要处理的是文本、图像、音频还是视频？  
2. 需要执行的是生成、编辑、理解还是检索操作？  
3. 您需要语音服务（TTS/ASR/实时翻译）还是数据检索（嵌入/重新排序/向量数据库）？  
4. 您是需要可执行的 SDK 脚本，还是仅需要 API/参数说明？  

## 参考资料  
- 模型列表及链接：`output/alicloud-model-studio-models-summary.md`  
- API/参数示例：请参阅目标子技能的 `SKILL.md` 文件及 `references/*.md`  
- 官方资源列表：`references/sources.md`  

## 验证方式  
```bash
mkdir -p output/alicloud-ai-entry-modelstudio
echo "validation_placeholder" > output/alicloud-ai-entry-modelstudio/validate.txt
```  
验证标准：命令执行成功（退出代码为 0），并且生成 `output/alicloud-ai-entry-modelstudio/validate.txt` 文件。  

## 输出与证据  
- 将生成的结果文件、命令输出及 API 响应摘要保存在 `output/alicloud-ai-entry-modelstudio/` 目录下。  
- 在证据文件中包含关键参数（区域/资源 ID/时间范围），以便重现问题。  

**工作流程：**  
1) 确认用户意图、区域、标识符以及操作是只读还是可修改的。  
2) 首先执行一个最小的只读查询，以验证连接性和权限。  
3) 使用明确的参数和有限的权限范围执行目标操作。  
4) 验证结果并保存输出文件和证据文件。