---
name: song-recognition
description: 使用 iFlytek 的 Query By ACRCloud 技术，可以通过唱歌或音频文件来识别歌曲。
homepage: https://www.xfyun.cn/doc/voiceservice/music_recognition/API.html
metadata:
  {
    "openclaw":
      {
        "emoji": "🎵",
        "requires": {
          "bins": ["python3"],
          "env": ["XF_SONG_APP_ID", "XF_SONG_API_KEY", "XF_SONG_API_SECRET"]
        },
        "primaryEnv": "XF_SONG_APP_ID"
      }
  }
---
# 🎵 歌曲识别

通过唱歌或使用音频文件，利用 iFlytek 的先进 ACRCloud 查询技术来识别歌曲。  

该技术专为音乐识别、歌曲发现和音频识别场景设计。  

---

## ✨ 主要功能  

- 唱歌识别  
- 音频文件识别  
- 高精度歌曲匹配  
- 实时同步检测  
- 支持多种音频格式  
- 支持输入 URL 和文件路径  

---

## 🚀 使用方法  

**使用音频文件路径：**  
```bash  
python {baseDir}/scripts/index.py "<audio_path>"  
```  

示例：  
```bash  
python {baseDir}/scripts/index.py "humming.wav"  
```  

## 📋 输入要求  

### 音频要求  

- 支持的格式：MP3  
- 采样率：16000Hz  
- 音频编码：lame  
- 建议时长：5-30 秒  
- 需要包含清晰的旋律  

---  

## ⚠ 限制条件  

- 音频中必须包含清晰的旋律  
- 需要配置 API 凭据  
- 需要网络连接  
- 实时处理，可立即获得结果  
- 音频质量会影响识别精度  

---  

## 🔧 环境配置  

**必备条件：**  
- 系统路径中包含 Python  
- 需要配置以下环境变量：  
```bash  
export XF_SONG_APP_ID=your_app_id  
export XF_SONG_API_KEY=your_api_key  
export XF_SONG_API_SECRET=your_api_secret  
```  

或者可以在 `~/.openclaw/openclaw.json` 中进行配置：  
```json  
{  
    "env": {  
        "XF_SONG_APP_ID": "your_app_id",  
        "XF_SONG_API_KEY": "your_api_key",  
        "XF_SONG_API_SECRET": "your_api_secret"  
    }  
}  
```  

---  

## 📦 输出结果  

返回 JSON 格式的信息，包括：  
- 歌曲名称  
- 艺人名称  
- 专辑信息  
- 识别置信度  
- 匹配详情  

---  

## 🎯 目标应用场景  

- 音乐识别应用程序  
- 歌曲发现平台  
- 卡拉OK 应用  
- 音乐教育工具  
- 音频内容识别  
- 版权检测  
- 音乐搜索引擎  

---  

## 🛠 可扩展性  

未来可能的功能改进包括：  
- 批量音频处理  
- 实时流媒体识别  
- 自定义音乐库  
- 多语言歌曲支持  
- 流派分类  

---  

专为自动化工作流程和基于 AI 的音乐识别而设计。