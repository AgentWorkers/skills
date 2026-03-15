---
name: youtube-clipper-ko
description: 将韩语YouTube视频自动分割成病毒式传播的短片（viral clips）的技能。首先使用Whisper进行语音分析，然后利用Claude识别出视频中的病毒式传播片段，最后通过ffmpeg提取这些片段。该工具能够去除无声或呼吸声部分，并添加三色韩文字幕（使用SUIT字体），同时包含病毒式传播的评分以及相关说明文本。支持输入YouTube视频链接或本地文件；也可与Clawitzer管道系统进行集成使用。
triggers:
  - youtube 클립
  - 영상 클리핑
  - 바이럴 구간 추출
  - 쇼츠 변환
  - 롱폼 쇼츠
---
# YouTube Clipper KO  
**自动将韩语YouTube视频分割成病毒式短片的功能工具**  

## 概述  
1. 输入YouTube视频的URL或本地视频文件。  
2. 使用`yt-dlp`下载视频。  
3. 通过`Whisper API`提取所有字幕及字幕的时间戳信息。  
4. 利用`Claude Haiku`算法筛选出8–12个具有病毒式传播潜力的片段，并为每个片段生成评分及韩语字幕。  
5. 使用`ffmpeg`将每个片段剪辑成9:16的长度。  
6. 对音频进行处理（去除静音或呼吸声，设置`max_gap_sec=0.06`）。  
7. 为字幕添加三种颜色的背景（使用`SUIT ExtraBold`字体）。  
8. 将处理后的视频片段及其元数据保存到指定文件夹中。  

## 必需的工具  
在开始工作前，代理必须确认以下工具是否已安装：  
```bash
# yt-dlp
yt-dlp --version

# ffmpeg (libass 포함 여부 확인)
ffmpeg -filters 2>&1 | grep subtitles

# python 의존성
python3 -c "import openai, anthropic; print('OK')"

# SUIT 폰트
ls /usr/share/fonts/truetype/SUIT-ExtraBold.ttf 2>/dev/null || echo "MISSING"
```  

如果缺少以下工具，请安装：  
- `yt-dlp`: `pip install yt-dlp`  
- `ffmpeg`: `apt install ffmpeg` 或 `brew install ffmpeg`  
- `openai anthropic`: `pip install openai anthropic`  
- 如果没有`SUIT`字体，系统会自动使用`NotoSansCJK-Bold.ttc`作为替代字体。  

## 使用方法  
代理需要向用户询问以下信息：  
1. YouTube视频的URL或本地视频文件的路径。  
2. 视频片段的选取范围（可选：全部片段）。  
3. 每个片段的时长（可选：15–30秒 / 30–60秒 / 60–90秒 / 90–120秒，默认为30–60秒）。  
4. 字幕语言（可选：韩语 / 英语，默认为韩语）。  

获取这些信息后，运行`scripts/clip.py`脚本：  
```bash
python3 skills/youtube-clipper-ko/scripts/clip.py \
  --url "https://youtu.be/VIDEO_ID" \
  --clip-length 60 \
  --lang ko
```  

**或使用本地视频文件：**  
```bash
python3 skills/youtube-clipper-ko/scripts/clip.py \
  --file "/path/to/video.mp4" \
  --clip-length 60
```  

## 输出结果的结构  
```
outputs/YYYYMMDD_HHMMSS/
├── source.mp4           # 원본 (URL 입력 시 다운로드)
├── transcript.json      # Whisper 전체 자막 + 타임스탬프
├── viral_segments.json  # 바이럴 구간 분석 결과
├── clips/
│   ├── clip_01_[제목].mp4
│   ├── clip_02_[제목].mp4
│   └── ...
└── result.json          # 전체 메타데이터
```  

## `viral_segments.json`文件的结构  
```json
[
  {
    "rank": 1,
    "score": 87,
    "start": "03:14",
    "end": "04:02",
    "title": "월 200만원 자동화하는 방법",
    "reason": "구체적인 금액과 방법이 동시에 나옴. 첫 3초 안에 결론 제시.",
    "hook": "근데 진짜 이게 되거든요",
    "clip_file": "clips/clip_01_월200만원자동화.mp4"
  }
]
```  

## 如何将处理后的片段传递给Clawitzer  
完成片段提取后，需要将结果传递给`Clawitzer`处理流程：  
```bash
# 추출된 클립을 Clawitzer 소스로 사용
python3 projects/clawitzer/main.py \
  --video "skills/youtube-clipper-ko/outputs/TIMESTAMP/clips/clip_01.mp4" \
  --script-file "skills/youtube-clipper-ko/outputs/TIMESTAMP/clip_01_script.json"
```  
**注意：** `Clawitzer`不使用TTS功能（保留原始音频），仅支持字幕编辑功能。  

## API密钥  
- **OpenAI Whisper**: 需要使用OpenAI的API密钥（而非`TOOLS.md`中提供的Gemini密钥，如需获取请联系Dalbi）。  
- **Anthropic Claude**: 使用现有的配置文件中的`ANTROPIC_API_KEY`环境变量。  

## 筛选病毒式片段的标准（基于Claude模型的提示）  
1. **情感强度**：包含令人惊讶、共鸣、好奇或引发笑声的片段。  
2. **信息密度**：包含具体数字、金额或方法的片段。  
3. **完整性**：能够独立理解的片段。  
4. **吸引力**：片段开头3秒内是否包含能吸引观众的句子。  
5. **针对韩语观众的优化**：考虑韩语观众的观看习惯进行筛选。  

## 音频处理（借鉴Clawitzer的`editor.py`逻辑）  
- 使用`silenceremove`过滤器去除静音或呼吸声（`max_gap_sec=0.06`）。  
- 不完全删除音频，仅进行压缩处理以保持自然的语境连贯性。  
- 对呼吸声部分进行压缩（压缩时间为50毫秒）。  

## 字幕样式（遵循Clawitzer的三种颜色规则）  
- **默认字体颜色**：白色（#FFFFFF），字体大小为52像素。  
- **红色背景**：使用黄色（#FFFF00），字体大小为52像素。  
- **重点强调的关键词**：使用红色（#FF0000），字体大小为62像素（不允许连续显示）。  
- **使用的字体**：`SUIT ExtraBold`；如果该字体不可用，则使用`NotoSansCJKBold.ttc`作为替代。  
- **字间距**：设置为-1（表示字体更紧排）。  
- **字幕位置**：显示在屏幕中央（坐标：an5, Y=900/1920）。