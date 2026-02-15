# 通过 ComfyUI 实现文本转语音（TTS）

## 描述  
该技能用于通过 ComfyUI 使用 `AILab_Qwen3TTSVoiceDesign_Advanced` 模块生成音频文件。

## 要求  
- 确保已安装 ComfyUI 并且已启用 `AILab_Qwen3TTSVoiceDesign_Advanced` 插件  
- 需要使用 Qwen3 模型  
- 需要有一个名为 `E:\Ai\Comfy UI\output` 的文件夹用于保存生成的音频文件  

## 启动 ComfyUI  
如果 ComfyUI 未运行，请使用以下命令启动：  
```
cmd /c start "" "C:\Users\user\Desktop\ComfyUI.lnk"
```  

## 等待音频文件生成  
在音频文件生成完成之前，每 10 秒通过 `http://localhost:8000` 检查是否可用。  

## 请求格式  
请求的格式如下：  
```json
{
  "prompt": {
    "50": {
      "inputs": {
        "filename_prefix": "qwen3-tts/[UNIQUE_ID]",
        "quality": "320k",
        "audioUI": "",
        "audio": ["55", 0]
      },
      "class_type": "SaveAudioMP3",
      "_meta": {"title": "Сохранить аудио (MP3)"}
    },
    "55": {
      "inputs": {
        "text": "[TEXT]",
        "instruct": "A male voice with a slightly hoarse, warm tone, speaking in a confident and friendly manner.",
        "model_size": "1.7B",
        "device": "auto",
        "precision": "bf16",
        "language": "Russian",
        "max_new_tokens": 2048,
        "do_sample": true,
        "top_p": 0.9,
        "top_k": 50,
        "temperature": 0.9,
        "repetition_penalty": 1,
        "unload_models": false,
        "seed": -1
      },
      "class_type": "AILab_Qwen3TTSVoiceDesign_Advanced",
      "_meta": {"title": "Qwen3 TTS VoiceDesign (Advanced)"}
    }
  }
}
```  

## 处理流程  
1. 向 `http://localhost:8000/prompt` 发送 POST 请求  
2. 获取返回的 `prompt_id`  
3. 在 `/history/[prompt_id]` 目录中等待处理结果  
4. 在 `E:\Ai\Comfy UI\output` 目录中查找以 `filename_prefix` 开头的 `.mp3` 文件  
5. 使用 `message(asVoice=true)` 将生成的音频文件作为语音消息发送出去