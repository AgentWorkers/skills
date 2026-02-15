---
name: Briefing Room
description: "**每日新闻简报生成器**  
该工具可生成以广播主持人风格进行的音频简报，并附带相应的 DOCX 文档，内容涵盖天气、社交媒体（X/Twitter）趋势、网络热点、世界新闻、政治、科技、本地新闻、体育、市场动态以及加密货币信息。仅支持 macOS 系统（使用 Apple 的 TTS 语音合成技术和 afplay 播放器）。适用于用户请求新闻简报、晨间更新或类似需求的情况。"
metadata:
  {
    "openclaw":
      {
        "emoji": "📻",
        "requires": { "bins": ["curl"] }
      }
  }
---

# 简报室 📻

**您的个人每日新闻简报 — 音频 + 文档形式。**

根据需求，您可以研究并制作一份约10分钟的综合性新闻简报，采用对话式广播主持人的风格。输出形式为：音频文件（MP3格式）+ 格式化的文档（DOCX格式）。

### 💸 100% 免费

- **无需订阅、API密钥或付费服务**
- 使用免费的公共API（Open-Meteo天气数据、Coinbase价格信息、Google Trends RSS源）、网络搜索以及本地文本转语音（TTS）服务
- 文本转语音功能完全基于本地资源，无需额外密钥：支持MLX-Audio Kokoro（英语版本）或Apple的`say`功能（支持多种语言）
- 配置文件：`~/.briefing-room/config.json`；输出文件保存路径：`~/Documents/Briefing Room/`

## 首次使用设置

首次使用时，请检查`~/.briefing-room/config.json`文件是否存在。如果不存在，请运行以下命令：

```bash
python3 SKILL_DIR/scripts/config.py init
```

该命令会生成默认配置文件。用户可以自定义以下内容：
- **位置**：城市名称、纬度、经度、时区（用于获取天气信息）
- **语言**：`en`（英语）、`sk`（斯洛伐克语）等
- **语音**：对应语言的文本转语音引擎及语音选择
- **包含的新闻板块**：需要展示的新闻板块
- **输出文件夹**：简报文件的保存路径

查看设置状态：
```bash
python3 SKILL_DIR/scripts/config.py status
```

## 快速启动

当用户请求简报时（例如：“给我一份简报”、“早上更新”、“今天发生了什么”），系统将执行以下操作：
1. 检查配置文件是否存在（如果不存在则执行设置脚本）
2. 播放通知音效：`afplay /System/Library/Sounds/Blow.aiff`
3. 立即启动一个子代理来执行整个简报生成流程
4. 回复用户：“📻 简报室正在准备中——正在收集今天的新闻。准备完成后会通知您！”

**语言切换：** 如果用户请求使用其他语言（如“用斯洛伐克语”、“用德语”等），请将语言信息传递给子代理。系统会自动选择macOS支持的语言；代理会使用相应语言编写脚本，并通过TTS引擎选择合适的语音。

### 启动命令

```
sessions_spawn(
  task="<full pipeline instructions — see below>",
  label="briefing-room",
  runTimeoutSeconds=600,
  cleanup="delete"
)
```

该命令包含了简报生成过程中的所有步骤，确保子代理能够独立完成任务。请将`SKILL_DIR`替换为该技能的实际目录路径。

**广播主持人名称：** 从配置文件`host.name`中读取主持人名称；如果文件为空，则使用用户的身份信息中的名称。该名称将用于简报中的广播主持人口白（例如：“早上好，我是Jackie，这是您的简报室……”）

## 配置文件

配置文件路径：`~/.briefing-room/config.json`

**读取配置值：**  
```bash
python3 SKILL_DIR/scripts/config.py get location.city
python3 SKILL_DIR/scripts/config.py get language
python3 SKILL_DIR/scripts/config.py get voices.en.mlx_voice
```

**设置配置值：**  
```bash
python3 SKILL_DIR/scripts/config.py set location.city "Vienna"
python3 SKILL_DIR/scripts/config.py set location.latitude 48.21
python3 SKILL_DIR/scripts/config.py set location.longitude 16.37
python3 SKILL_DIR/scripts/config.py set language "de"
```

### 主要配置选项

| 配置项 | 默认值 | 说明 |
|---------|---------|-------------|
| `location.city` | Bratislava | 用于获取天气和本地新闻的城市名称 |
| `location.latitude` | 48.15 | 天气API的纬度值 |
| `location.longitude` | 17.11 | 天气API的经度值 |
| `location.timezone` | Europe/Bratislava | 天气API的时区 |
| `language` | en | 默认简报语言 |
| `output_folder` | ~/Documents/Briefing Room | 简报文件的输出目录 |
| `audio.enabled` | true | 是否生成音频 |
| `audio.format` | mp3 | 音频格式（支持mp3、wav、aiff） |
| `audio.tts_engine` | auto | 文本转语音引擎（自动选择：mlx、kokoro或内置引擎） |
| `sections` | all 11 | 需要包含的新闻板块 |
| `host.name` | （空值时使用代理名称） | 简报中的广播主持人名称 |
| `trends.regions` | united-states,united-kingdom | X/Twitter的趋势地区（用逗号分隔，末尾加逗号表示“全球”） |
| `webtrends.regions` | US,GB | Google Trends的地区（使用ISO代码，末尾加逗号表示“全球” |

### 各语言的语音配置

每种语言都可以配置独立的文本转语音引擎和语音：

```json
{
  "voices": {
    "en": {
      "engine": "mlx",
      "mlx_voice": "af_heart",
      "mlx_voice_blend": {"af_heart": 0.6, "af_sky": 0.4},
      "builtin_voice": "Samantha",
      "speed": 1.05
    },
    "sk": {
      "engine": "builtin",
      "builtin_voice": "Laura (Enhanced)",
      "builtin_rate": 220
    },
    "de": {
      "engine": "builtin",
      "builtin_voice": "Petra (Premium)",
      "builtin_rate": 200
    }
  }
}
```

**引擎优先级（当设置为`auto`时）：**
- 英语：mlx → kokoro → 内置引擎
- 其他语言：使用Apple内置的TTS引擎（支持多种语言）

用户可以通过添加`voices`条目及相应的`builtin_voice`来支持更多语言（使用命令`say -v ?`查询可用的语音）。

## 输出文件结构

**请勿将`.md`格式的临时文件保存在输出文件夹中**。请使用`/tmp/`作为临时工作文件夹，并使用完成后删除该文件。

## 完整的简报生成流程

### 第0步：设置

```bash
# Read config
CITY=$(python3 SKILL_DIR/scripts/config.py get location.city)
LAT=$(python3 SKILL_DIR/scripts/config.py get location.latitude)
LON=$(python3 SKILL_DIR/scripts/config.py get location.longitude)
TZ=$(python3 SKILL_DIR/scripts/config.py get location.timezone)
LANG=$(python3 SKILL_DIR/scripts/config.py get language)
OUTPUT_FOLDER=$(python3 SKILL_DIR/scripts/config.py get output.folder)

DATE=$(date +%Y-%m-%d)
TIMESTAMP=$(date +%Y-%m-%d-%H%M)
OUTPUT_DIR="$OUTPUT_FOLDER/$DATE"
mkdir -p "$OUTPUT_DIR"
```

### 第1步：获取天气数据

使用配置的位置坐标：

```bash
# Current weather
TZ_ENC="${TZ/\//%2F}"
BASE="https://api.open-meteo.com/v1/forecast"
CURRENT="temperature_2m,relative_humidity_2m"
CURRENT="$CURRENT,apparent_temperature,precipitation"
CURRENT="$CURRENT,weather_code,wind_speed_10m"
curl -s "$BASE?latitude=$LAT&longitude=$LON\
&current=$CURRENT&timezone=$TZ_ENC"

# 7-day forecast
DAILY="temperature_2m_max,temperature_2m_min"
DAILY="$DAILY,precipitation_sum,weather_code"
curl -s "$BASE?latitude=$LAT&longitude=$LON\
&daily=$DAILY&timezone=$TZ_ENC"
```

或者使用辅助脚本`bash SKILL_DIR/scripts/briefing.sh weather`来获取天气信息。

将`weather_code`与对应的天气描述关联：
- 0：晴朗 ☀️
- 1-3：多云 ⛅
- 45-48：有雾 🌫️
- 51-55：小雨 🌦️
- 61-65：中雨 🌧️
- 71-75：大雪 ❄️
- 80-82：阵雨 🌦️
- 95-99：雷暴 ⛈️

### 第2步：获取新闻数据（网络搜索）

使用`web_search`工具为每个新闻板块获取内容。在查询中加入当前日期以确保信息的时效性。使用配置的`$CITY`参数来获取本地新闻。

**X/Twitter趋势数据（来自getdaytrends.com — 实时数据，无需API密钥）：**
```bash
bash SKILL_DIR/scripts/briefing.sh trends
```
该脚本会获取美国、英国和全球的热门趋势。根据这些数据：
- 筛选出最有趣或具有新闻价值的趋势（忽略如“美好星期二”之类的通用主题）
- 仅选择具有全球影响力的趋势
- 选择5-10个在多个地区都有体现或具有新闻价值的趋势
- 使用`web_search`工具获取所选趋势的详细背景信息

**Google Trends数据（来自RSS源）：**
```bash
bash SKILL_DIR/scripts/briefing.sh webtrends
```
该脚本会获取美国、英国和全球的热门搜索词及搜索量信息
- 使用这些数据生成“网络趋势”板块的内容；大多数搜索词本身已经包含了足够的背景信息

**全球新闻：**
```
web_search("top world news today {date}", count=8)
web_search("breaking news today", count=5)
```

**政治新闻：**
```
web_search("US politics news today {date}", count=5)
web_search("EU politics news today {date}", count=5)
web_search("geopolitics news today", count=5)
```

**⚠️ 注意：** 所有新闻来源都可能存在偏见。为了保持报道的客观性：
- 用不同的视角报道同一事件
- 客观呈现事实，同时引用各方的观点
- 不要盲目接受任何媒体的观点
- 仅引用可验证的事实：数字、日期、引文、具体事件

**科技与人工智能：**
```
web_search("tech news today {date}", count=5)
web_search("AI artificial intelligence news today {date}", count=5)
```

**本地新闻**（基于配置的城市）：
```
web_search("$CITY news today {date}", count=5)
```

如果配置的语言不是英语，也可以使用相应的语言进行搜索：
```
web_search("$CITY [news today] in $LANG {date}", count=5)
```

**体育新闻：**
```
web_search("sports news today {date}", count=5)
web_search("football soccer results today", count=5)
```

### 第3步：获取市场与加密货币数据（通过API和网络搜索）

```bash
# Or use helper:
bash SKILL_DIR/scripts/briefing.sh crypto
```

```bash
curl -s "https://api.coinbase.com/v2/prices/BTC-USD/spot"
curl -s "https://api.coinbase.com/v2/prices/ETH-USD/spot"
curl -s "https://api.coinbase.com/v2/prices/SOL-USD/spot"
curl -s "https://api.coinbase.com/v2/prices/XRP-USD/spot"
```

```
web_search("S&P 500 Dow Jones Nasdaq today {date}", count=5)
web_search("stock market today movers {date}", count=5)
web_search("gold price silver price today", count=3)
web_search("crypto market today {date}", count=5)
```

### 第4步：编写简报脚本

以对话式广播主持人的风格撰写简报内容：

- 语言风格要像一位聪明、引人入胜的广播主持人
- 自我介绍时使用广播主持人名称（例如：“早上好，我是[主持人名称]，这是您的[日期]简报室……”）
- 在脚本中自然地使用主持人名称（在结尾和过渡句中）
- 不要在Markdown文件中使用`# 标题`格式——pandoc会从元数据中自动添加标题
- 使用过渡语句连接各个新闻板块
- 添加背景解释：“这是为什么这条新闻重要的原因”
- 保持中立和客观的报道态度
- 保持文章长度在2500-3500字左右（约10分钟）
- 脚本中不要使用表情符号（以免影响TTS播放）
- 为TTS方便阅读，将数字和缩写写成文字形式：
  - “$96,500” → “九万六千五百美元”
  - “S&P 500” → “标准普尔500指数”
  - “BTC” → “比特币”
  - “°C” → “摄氏度”

**如果使用非英语语言，** 请将整个脚本翻译成相应语言。

**新闻板块顺序：**
1. **开场**：日期、热门新闻的简要介绍
2. **天气**：当前天气及未来一周的天气预报
3. **X/Twitter趋势**：X/Twitter上的热门话题
4. **全球趋势**：用户搜索的热门内容
5. **政治新闻**：美国、欧盟的政治动态
6. **科技与人工智能**：最新的科技进展和突破
7. **本地新闻**：配置城市的本地新闻
8. **体育新闻**：体育赛事的头条和结果
9. **市场动态**：标准普尔500指数、道琼斯指数、纳斯达克指数的表现
10. **加密货币与商品**：比特币、以太坊、其他加密货币的价格及黄金、白银的价格
11. **今日历史**：当天发生的1-2件有趣或值得关注的事件
12. **结尾**：总结语和告别语

**今日历史**：无需额外研究——可以根据自己的知识选择1-2件有趣、具有历史意义或有趣的事件。内容可以涵盖科学、文化、政治等领域。保持对话式的表达方式：“在结束之前，您知道吗……”

请仅包含配置文件中指定的新闻板块。如果用户已移除了某些板块，请跳过这些板块。

将临时脚本文件保存为`/tmp/briefing_draft_$TIMESTAMP.md`。

**Markdown格式要求：**
- 使用表情符号作为板块标题（例如：`## 🌤️ 天气`, ## 🌍 全球新闻`, ## 📜 今日历史`）
- 关键信息后需附上来源链接
- 重要数据需加粗显示

### 第5步：生成DOCX文档

```bash
pandoc "/tmp/briefing_draft_$TIMESTAMP.md" \
  -o "$OUTPUT_DIR/briefing-$TIMESTAMP.docx" \
  --metadata title="Briefing Room - $DATE"
```

如果系统没有安装pandoc工具，可以跳过DOCX生成步骤。

### 第6步：生成音频文件

根据配置文件确定当前语言对应的文本转语音引擎和语音资源。

**使用MLX-Audio（英语）：**
```bash
python3 SKILL_DIR/scripts/config.py get voices.$LANG.engine
# → if "mlx":
```

**使用Apple内置的TTS（支持多种语言）：**
如果未配置相应语言的语音资源，系统会自动选择默认的语音引擎：
```python
import os, re, glob, json, subprocess
from datetime import datetime

timestamp = datetime.now().strftime("%Y-%m-%d-%H%M")  # must match TIMESTAMP from Step 0

# Read config
config_path = os.path.expanduser("~/.briefing-room/config.json")
with open(config_path) as f:
    config = json.load(f)

lang = config.get("language", "en")
voices = config.get("voices", {})
voice_cfg = voices.get(lang, voices.get("en", {}))

# Read and strip markdown from draft
with open(f"/tmp/briefing_draft_{timestamp}.md", "r") as f:
    text = f.read()
text = re.sub(r'#+ ', '', text)
text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
text = re.sub(r'\*([^*]+)\*', r'\1', text)
text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
text = re.sub(r'---+', '', text)
text = re.sub(r'\n{3,}', '\n\n', text)

# Resolve voice
blend = voice_cfg.get("mlx_voice_blend")
voice = voice_cfg.get("mlx_voice", "af_heart")
if blend:
    model = config.get("mlx_audio", {}).get("model", "mlx-community/Kokoro-82M-bf16")
    model_slug = model.replace("/", "--")
    cache_dir = os.path.expanduser(f"~/.cache/huggingface/hub/models--{model_slug}")
    parts = []
    for v, w in sorted(blend.items(), key=lambda x: -x[1]):
        parts.append(f"{v}_{int(w * 100)}")
    blend_name = "_".join(parts) + ".safetensors"
    matches = glob.glob(os.path.join(cache_dir, "snapshots/*/voices", blend_name))
    if matches:
        voice = matches[0]

speed = voice_cfg.get("speed", 1.05)
lang_code = config.get("mlx_audio", {}).get("lang_code", "a")

# Find MLX-Audio
mlx_path = config.get("mlx_audio", {}).get("path", "")
if not mlx_path:
    for p in ["~/.openclaw/tools/mlx-audio", "~/.local/share/mlx-audio"]:
        ep = os.path.expanduser(p)
        if os.path.exists(os.path.join(ep, ".venv/bin/python3")):
            mlx_path = ep
            break

# Generate via subprocess (uses MLX-Audio's venv)
python_bin = os.path.join(mlx_path, ".venv/bin/python3")
# ... generate_audio call with resolved voice, speed, lang_code
```

**备用方案：Kokoro PyTorch**
Kokoro使用PyTorch作为后端；详情请参考TubeScribe技能文档。

### 第6b步：将音频文件转换为MP3格式

```bash
# Find the raw audio file (MLX outputs .wav, Apple TTS outputs .aiff)
RAW=""
for ext in wav aiff; do
    if [ -f "$OUTPUT_DIR/briefing-$TIMESTAMP.$ext" ]; then
        RAW="$OUTPUT_DIR/briefing-$TIMESTAMP.$ext"
        break
    fi
done

if [ -n "$RAW" ]; then
    ffmpeg -y \
      -i "$RAW" \
      -codec:a libmp3lame -qscale:a 2 \
      "$OUTPUT_DIR/briefing-$TIMESTAMP.mp3"
    if [ -s "$OUTPUT_DIR/briefing-$TIMESTAMP.mp3" ]; then
        rm "$RAW"
    fi
fi
```

### 第7步：清理临时文件

```bash
rm -f "/tmp/briefing_draft_$TIMESTAMP.md"
```

### 第8步：展示简报文件

**请勿自动播放简报文件**。由于简报文件较长，建议用户手动控制播放。

### 第9步：提供相关信息

向用户报告以下内容：
- 简报的日期和语言
- 覆盖的新闻板块
- 3-4个热门新闻标题
- 音频文件的时长
- 文件的保存位置

## 辅助脚本

```bash
bash SKILL_DIR/scripts/briefing.sh setup     # Check dependencies + config
bash SKILL_DIR/scripts/briefing.sh weather    # Fetch weather (uses config location)
bash SKILL_DIR/scripts/briefing.sh trends     # Fetch X/Twitter trends (US + UK + Worldwide)
bash SKILL_DIR/scripts/briefing.sh webtrends  # Fetch Google Trends (US + UK + Worldwide)
bash SKILL_DIR/scripts/briefing.sh crypto     # Fetch crypto prices
bash SKILL_DIR/scripts/briefing.sh open       # Open today's folder
bash SKILL_DIR/scripts/briefing.sh list       # List all briefings
bash SKILL_DIR/scripts/briefing.sh clean      # Remove briefings >30 days old
bash SKILL_DIR/scripts/briefing.sh config     # Show raw config JSON
```

## 使用技巧：

- 整个简报生成过程大约需要3-5分钟（包括数据收集、内容编写和文本转语音）
- 如需简短的简报，可以请求“快速简报”，仅涵盖前3个新闻板块
- 如果市场处于休市状态（周末或节假日），请告知用户并跳过相关数据
- 该脚本会自动处理所有数据查询和内容编写工作
- 用户可以通过添加新的语言配置项（`voices`）并安装相应的语音资源来扩展语言支持

## 所需依赖软件：

**必备软件：**
- `curl`：用于API请求（macOS内置）
- `web_search`工具：用于新闻搜索（OpenClaw内置）

**推荐软件：**
- MLX-Audio Kokoro：快速的英语文本转语音工具
- `pandoc`：用于生成DOCX文档（使用`brew install pandoc`命令安装）
- `ffmpeg`：用于音频文件转换（使用`brew install ffmpeg`命令安装）

**macOS内置工具：**
- Apple的`say`：支持多种语言的文本转语音功能（作为备用方案）

## 错误处理：

| 错误类型 | 处理方式 |
|---------|---------|
| 未找到配置文件 | 运行`python3 SKILL_DIR/scripts/config.py init`命令来初始化配置 |
| API请求超时 | 重试一次，并跳过该数据源 |
- 网络搜索无结果 | 尝试其他查询方式，并记录异常情况 |
- 文本转语音失败 | 使用Apple的`say`功能（始终可用） |
- 未找到pandoc工具 | 仅生成MP3音频文件 |
- 无法连接互联网 | 无法生成简报文件，请通知用户