---
name: clawdbites
description: 从 Instagram Reels 中提取食谱信息。当用户发送一个 Instagram Reel 链接并希望从中获取食谱内容时，该功能可以提取食谱的配料、制作步骤以及相关宏指令，并将其转换为格式清晰的文本。
homepage: https://github.com/kylelol/ClawdBites
metadata: {"clawdbot":{"emoji":"🦞","os":["darwin","linux"],"requires":{"bins":["yt-dlp","ffmpeg","whisper"]},"install":[{"id":"yt-dlp","kind":"brew","formula":"yt-dlp","bins":["yt-dlp"],"label":"Install yt-dlp via Homebrew"},{"id":"ffmpeg","kind":"brew","formula":"ffmpeg","bins":["ffmpeg"],"label":"Install ffmpeg via Homebrew"},{"id":"whisper","kind":"shell","command":"pip3 install --user openai-whisper","label":"Install Whisper (local, no API key)"}]}}
---

# Instagram食谱提取器

本工具采用多层次方法从Instagram视频中提取食谱信息：

1. **字幕解析**：首先快速检查视频的描述部分，以获取食谱的基本信息。
2. **音频转录**：使用本地工具`whisper`进行音频转录（无需API密钥）。
3. **帧分析**：利用视觉模型识别屏幕上显示的文字内容。

无需登录Instagram，适用于公开发布的视频。

## 使用场景

- 用户提供Instagram视频链接。
- 用户提及“Instagram食谱”或“保存此视频”。
- 用户希望从视频中提取食谱详情。

## 工作流程（必须遵循的步骤）

**请务必按照以下完整流程操作，即使字幕信息不完整也不要中断：**

1. 用户提供Instagram视频链接。
2. 使用`yt-dlp`工具提取视频元数据（`--dump-json`选项）。
3. 解析字幕以获取食谱详情。
4. **完整性检查**：字幕中是否同时包含食材和制作步骤？
   - ✅ **是**：显示食谱信息。
   - ❌ **否（缺少步骤或信息不完整）**：**自动进入音频转录步骤**，无需询问用户。

**如果需要音频转录：**
   - 下载视频：`yt-dlp -o "/tmp/reel.mp4" "URL"`
   - 提取音频：`ffmpeg -y -i /tmp/reel.mp4 -vn -acodec pcm_s16le -ar 16000 -ac 1 /tmp/reel.wav`
   - 转录音频：`whisper /tmp/reel.wav --model base --output_format txt --output_dir /tmp`
   - 将字幕中的食材信息与音频转录内容合并。
5. 以清晰、格式化的形式呈现提取到的食谱（根据需要结合字幕和音频内容）。
6. 用户可选择保存到笔记、添加到愿望清单等。

**完整性检查规则：**
- **食材**：字幕中应包含具体的数量和食材名称（例如：“1杯面粉”、“2磅鸡肉”）。
- **制作步骤**：字幕中应包含动词（如“搅拌”、“烹饪”、“烘烤”等）以及步骤顺序。

## 提取命令

```bash
yt-dlp --dump-json "https://www.instagram.com/reel/SHORTCODE/" 2>/dev/null
```

**JSON输出中的关键字段：**
- `description`：包含食谱信息的字幕内容。
- `uploader`：创作者的名称。
- `channel`：创作者的Instagram账号。
- `webpage_url`：视频的原始链接。
- `like_count`：视频的点赞数量（表示受欢迎程度）。

## 食谱解析规则

在字幕中查找以下信息：

- **宏量营养信息**：例如“X卡路里 | X克蛋白质 | X克碳水化合物 | X克脂肪”。
- **每份的宏量营养信息**。
- **食材**：以数量开头的行（如“1杯面粉”、“2汤匙”）。
- **测量单位**：如“盎司（oz）”、“杯（cup）”等。
- **列表格式**：使用表情符号（🥩 🌽 🧀等）标记的食材列表。

## 输出格式

以清晰、易于阅读的形式呈现提取到的食谱信息。

```
## [Recipe Name]
*From @[handle]*

**Macros (per serving):** X cal | Xg P | Xg C | Xg F

### Ingredients
- [ingredient 1]
- [ingredient 2]
...

### Instructions
1. [step 1]
2. [step 2]
...

---
Source: [original URL]
```

## 用户操作选项

提取完成后，用户可以选择以下操作：
- **保存到笔记**：将食谱保存到Apple Notes。
- **添加到愿望清单**：将食谱添加到`memory/recipe-wishlist.json`文件中。
- **仅查看**：仅显示食谱信息，不进行保存。
- **计划下周的餐食**：将食谱信息传递给 meal-planner 工具进行后续处理。

## 愿望清单存储（可选）

用户可选择性地将感兴趣的食谱保存到`memory/recipe-wishlist.json`文件中。

```json
{
  "recipes": [
    {
      "name": "Recipe Name",
      "source": "instagram",
      "sourceUrl": "https://instagram.com/reel/...",
      "handle": "@creator",
      "addedDate": "2026-01-26",
      "tried": false,
      "macros": {
        "calories": 585,
        "protein": 56,
        "carbs": 25,
        "fat": 28,
        "servings": 3
      },
      "ingredients": [...],
      "instructions": [...]
    }
  ]
}
```

## 错误处理

- **如果`yt-dlp`执行失败**：检查提供的链接是否为有效的Instagram视频格式。
- 如果视频来自私人账号，会通知用户。
- 建议用户手动复制字幕内容作为备用方案。

**如果字幕中未找到食谱信息（非常重要）：**

提取完成后，再次检查字幕中的以下内容：
- 食材的数量和单位（如“盎司、杯、汤匙、磅”）。
- 食谱相关的部分（如“食材”、“制作步骤”等）。
- 厨饪动词（如“烘烤”、“搅拌”等）。
- 宏量营养信息（如卡路里、蛋白质、碳水化合物、脂肪）。

**如果仍未找到食谱信息，请明确告知用户：**

> “虽然提取了字幕，但看起来这里没有食谱信息——可能这只是视频的预告，或者食谱内容仅在视频中显示。以下是字幕内容：”
> 
> [显示字幕内容]
> 
> 有以下几种处理方式：
> 1. 查看评论区——有时创作者会在评论区发布完整食谱。
> 2. 查看创作者的个人简介链接——可能包含完整食谱。
> 3. 请描述你在视频中看到的内容，我会帮你找到类似的食谱。”

## 与meal-planner工具的集成

meal-planner工具可以参考此功能：
- 在规划餐食时，查看用户愿望清单中的未尝试过的食谱。
- 推荐与用户库存食材匹配的食谱。
- 在食谱被使用后，将其标记为“已尝试”。

## 音频转录（第二版）（强制执行的备用方案）

**如果字幕中缺少制作步骤，必须自动进行音频转录。**无需询问用户，直接执行此步骤。因为很多创作者会在字幕中列出食材，但会在音频中说明制作步骤。

**步骤1：下载视频**  
```bash
yt-dlp -o "/tmp/reel.mp4" "https://instagram.com/reel/XXX"
```

**步骤2：提取音频**  
```bash
ffmpeg -i /tmp/reel.mp4 -vn -acodec pcm_s16le -ar 16000 -ac 1 /tmp/reel.wav
```

**步骤3：使用whisper进行音频转录**  
```bash
/Users/kylekirkland/Library/Python/3.14/bin/whisper /tmp/reel.wav --model base --output_format txt --output_dir /tmp
```

**步骤4：从转录文本中提取食谱信息**  
查找音频中提到的制作步骤和食材信息。

## 缺少测量单位的处理规则

**当食谱中未提供具体数量时，必须进行估算。**切勿在没有数量信息的情况下直接呈现食谱，应根据上下文和标准包装规格进行估算。

### 不明确的语言对应的数量估算

| 用户描述 | 估算数量 |
|--------------|-------|
| “一些鸡肉” | 约1磅 |
| “少许大蒜” | 2-3瓣 |
| “一把菠菜” | 约2杯 |
| “少许油” | 1-2汤匙 |
| “适量调味料” | ½茶匙盐，¼茶匙胡椒 |
| “少许酱油” | 1-2汤匙 |
| “几汤匙” | 2-3汤匙 |
| “一些米饭” | 1杯干米 |
| “表面撒奶酪” | ½-1杯奶酪丝 |
| “切碎的洋葱” | 1个中等大小的洋葱 |
| “甜椒” | 2个甜椒 |

### 标准包装规格（当食材未指定数量时）

| 食材 | 标准包装规格 | 估算数量 |
|------------|------------------|-------|
| 膨皮 | 17盎司/张 | 1张 |
| 牛肉/火鸡末 | 1磅/包 | 1包 |
| 鸡胸肉 | 约1.5磅/包 | 1.5磅 |
- 香肠 | 14盎司/4-5根 | 1包 |
- 培根 | 12盎司/12片 | ½包（6片） |
- 奶酪丝 | 8盎司/袋 | 1-2杯 |
- 面饼 | 8-10张 | 1包 |
- 罐装豆类 | 15盎司/罐 | 1罐 |
- 高汤/汤料 | 32盎司/盒 | 1-2杯 |
- 意大利面 | 16盎司/盒 | 8盎司（半盒） |
- 米饭 | 2磅/袋 | 1-2杯干米 |

### 根据上下文调整用量

- **根据食谱类型调整用量：**
  - 炒菜：1磅蛋白质，4杯蔬菜。
  - 汤/炖菜：1.5-2磅蛋白质，4杯高汤。
  - 平底锅菜肴：1.5磅蛋白质，3-4杯蔬菜。
- **根据份量调整：**
  - “可供4人食用”：按4人份量调整用量。
  - “为下周准备餐食”：假设5-8人份量。
- **根据用户设定的蛋白质目标调整：**
  - 每份40-50克蛋白质：每份约6-8盎司熟肉。

**输出格式**

始终明确标注估算的数量，让用户知道哪些信息来自字幕，哪些是估算值。

**综合提取流程**  
```
1. TRY CAPTION (instant)
   └── yt-dlp --dump-json → parse description
   └── Recipe found? → DONE ✅
   └── Check for "pinned" / "in comments" / "check comments" → FLAG
   
2. IF FLAGGED: CHECK FOR CREATOR COMMENT
   └── Look through comments for creator's username
   └── If creator comment found with recipe → DONE ✅
   └── If not found → continue + notify user

3. TRY AUDIO (30-60 sec)
   └── Download video
   └── Extract audio with ffmpeg
   └── Transcribe with Whisper (base model)
   └── Parse transcript for recipe
   └── Infer missing measurements
   └── Recipe found? → DONE ✅

4. PRESENT RESULTS + PROMPT IF NEEDED
   └── Show what was extracted from audio
   └── If "pinned" was flagged, tell user:
       "The creator mentioned the full recipe is pinned in the comments.
        I extracted what I could from the audio, but if you want the 
        exact measurements, paste the pinned comment here and I'll 
        merge it with what I found."
   
5. TRY FRAME ANALYSIS (if audio incomplete)
   └── Extract 5-8 key frames with ffmpeg
   └── Send to Claude vision
   └── Ask: "Extract any recipe text, ingredients, or measurements shown"
   └── Merge findings with audio transcript
   
6. FALLBACK (nothing found)
   └── Inform user: "Recipe wasn't in caption or audio/video"
   └── Offer: search for similar recipe based on video title/description
```

## 帧分析

提取关键帧，并使用视觉模型进行分析。

**提取帧内容：**  
```bash
# Extract 1 frame every 5 seconds
ffmpeg -i /tmp/reel.mp4 -vf "fps=1/5" /tmp/frame_%02d.jpg

# Or extract specific number of frames evenly distributed
ffmpeg -i /tmp/reel.mp4 -vf "select='not(mod(n,30))'" -vsync vfr /tmp/frame_%02d.jpg
```

**发送给视觉模型：**  
使用Claude图像分析工具解析每个帧：
- 视频中的食谱卡片/标题屏幕。
- 屏幕上显示的食材列表。
- 文本中的测量单位。
- 逐步显示的制作步骤。

**视觉模型处理指令：**  
```
Analyze this frame from a cooking video. Extract any:
- Recipe name or title
- Ingredients with quantities
- Cooking instructions
- Nutritional information / macros
- Any other recipe-related text shown

If no recipe text is visible, respond with "No recipe text found."
```

**信息合并策略：**
- 音频转录内容为主要信息来源（口头制作步骤）。
- 帧分析结果为补充信息（精确的测量数据和食谱卡片）。
- 优先使用视觉分析得到的具体测量数据，而非音频中的估算值。

## 检测评论中的固定食谱链接

在字幕中查找以下短语（不区分大小写）：
- “食谱已固定”。
- “评论中固定了食谱链接”。
- “查看评论”。
- “在评论区”。
- “评论中的食谱”。

如果检测到这些短语，在提取完成后通知用户：

> “注意：创作者表示食谱链接在评论区。虽然我已从音频中提取了部分信息，但由于无法登录Instagram，无法获取评论区的固定链接。如果您需要完整食谱，请复制评论内容并发送给我，我会为您整理好。”

## 所需软件**

- `yt-dlp`：`brew install yt-dlp`
- `ffmpeg`：`brew install ffmpeg`
- `whisper`：`pip3 install openai-whisper`（在本地运行，无需API密钥）
- 公开发布的视频无需Instagram登录即可使用。