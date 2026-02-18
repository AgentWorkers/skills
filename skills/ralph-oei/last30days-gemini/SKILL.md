---
name: last30days
description: "研究过去30天内的任何主题。资料来源包括：X（Twitter）、YouTube视频的文字记录以及网络搜索结果。利用Gemini工具生成专家简报，并提供相应的复制/粘贴提示。"
argument-hint: 'last30 AI agents, last30 marketing automation'
metadata: {"version": "2.1.0", "clawdbot":{"emoji":"🔍","requires":{"bins":["python3","node","yt-dlp"],"env":["AUTH_TOKEN","CT0","BRAVE_API_KEY"]}}, "original_repo": "https://github.com/mvanhorn/last30days-skill", "author": "mvanhorn", "license": "MIT"}
---
## 致谢：  
该技能基于 [@mvanhorn](https://x.com/mvanhorn) 开发的 [last30days](https://github.com/mvanhorn/last30days-skill) 项目。原技能会从 Reddit、X（Twitter）、YouTube 和网络上收集相关主题的信息。当前版本新增了 Gemini 合成功能，可用于生成简报和提示信息。  

## 原始技能：  
[github.com/mvanhorn/last30days-skill](https://github.com/mvanhorn/last30days-skill)  

### last30days v2.1  

该技能可搜索 X（Twitter）、YouTube 和网络上的任何主题，获取当前正在被讨论、推荐或争论的内容。  

## 设置（Setup）  
```bash
# Environment (should already be set)
export AUTH_TOKEN=your_x_auth_token
export CT0=your_x_ct0_token  
export BRAVE_API_KEY=your_brave_key

# Config
mkdir -p ~/.config/last30days
cat > ~/.config/last30days/.env << 'EOF'
BRAVE_API_KEY=your_key_here
EOF
```  

## 使用方法（Usage）  
```bash
# Quick research (faster, fewer sources)
python3 {baseDir}/scripts/last30days.py "AI agents" --quick

# Full research
python3 {baseDir}/scripts/last30days.py "AI agents" 

# Output formats
python3 {baseDir}/scripts/last30days.py "topic" --emit=json    # JSON for parsing
python3 {baseDir}/scripts/last30days.py "topic" --emit=compact  # Human readable
python3 {baseDir}/scripts/last30days.py "topic" --emit=md       # Full report
```  

## 用于 AI 合成的输出（Output for AI Synthesis）  
使用 `--emit=json` 标志可输出结构化的 JSON 数据，这些数据可以输入到 Gemini 中，用于：  
- 生成专家简报  
- 生成可直接复用的提示信息  
- 进行趋势分析  

## 数据来源（Sources）  
| 来源        | 认证方式      | 备注        |  
|-------------|-------------|-------------|  
| X/Twitter    | 使用 cookies     | 需要 `bird CLI` 和现有的 `AUTH_TOKEN/CT0` |  
| YouTube     | 无需认证      | 需要 `yt-dlp` 来获取视频字幕   |  
| 网络        | 使用 Brave API    | 需要 `BRAVE_API_KEY`    |  

## 数据合成（Synthesis）  
该技能会收集原始数据并返回结果。如需使用 AI 生成简报或提示信息，只需将 JSON 数据输出传递给 Gemini 即可：  
```bash
python3 {baseDir}/scripts/last30days.py "topic" --quick --emit=json | python3 -c "
import json, sys, os
import urllib.request, urllib.parse

data = json.load(sys.stdin)
prompt = f'Synthesize this research into an expert briefing and 3 copy-paste prompts:\\n{json.dumps(data)}'

body = json.dumps({
    'contents': [{'parts': [{'text': prompt}]}],
    'generationConfig': {'temperature': 0.7, 'maxOutputTokens': 2048}
})

req = urllib.request.Request(
    'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=' + os.environ.get('GEMINI_API_KEY'),
    data=body.encode(),
    headers={'Content-Type': 'application/json'}
)
print(json.load(urllib.request.urlopen(req))['candidates'][0]['content']['parts'][0]['text'])
"
```  

## 致谢与版权信息（Attribution）  
- **原作者：** [Mike Van Horn](https://x.com/mvanhorn) ([mvanhorn](https://github.com/mvanhorn))  
- **原始仓库：** [github.com/mvanhorn/last30days-skill](https://github.com/mvanhorn/last30days-skill)  
- **许可证：** MIT 许可证（遵循原作者的许可协议）  
- **贡献者：** 感谢 [@steipete](https://x.com/steipete) 提供的 `yt-dlp` 工具及总结建议  

该技能通过集成 Gemini 合成功能，实现了简报的自动生成。