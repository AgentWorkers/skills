---
name: audio-gen
description: 根据用户提供的想法或主题，Claude AI 会生成相应的脚本，随后 ElevenLabs 将该脚本转换为高质量音频内容（支持多种格式，如 audiobook、podcast 或教育类音频）。用户可以自定义音频的长度以及所需的音效。该服务适用于需要创建音频内容、制作播客或生成有教育意义的音频文件的场景。最终生成的音频文件将以 MP3 格式提供，并通过 MEDIA 标记进行传输。
homepage: https://github.com/clawdbot/clawdbot
metadata: {"clawdbot":{"emoji":"🎙️","requires":{"skills":["sag"],"env":["ANTHROPIC_API_KEY","ELEVENLABS_API_KEY"]},"primaryEnv":"ANTHROPIC_API_KEY"}}
---

# 🎙️ 音频内容生成器

使用人工智能编写的剧本和 ElevenLabs 的文本转语音（TTS）技术，按需生成高质量的有声书、播客或教育音频内容。

## 快速入门

**创建有声书章节：**
```
User: "Create a 5-minute audiobook chapter about a dragon discovering friendship"
```

**生成播客：**
```
User: "Make a 10-minute podcast about the history of coffee"
```

**制作教育内容：**
```
User: "Generate a 15-minute educational audio explaining how neural networks work"
```

## 内容格式

### 有声书
**风格：** 具有情感深度的叙事风格
- 有明确的开头、中间和结尾
- 使用描述性语言和生动的意象
- 有节奏的叙述，适当停顿
- 与故事情感相匹配的语气
- 使用诸如 `[whispers]`（低语）、`[excited]`（兴奋）、`[serious]`（严肃）等语音效果来增强表现力

**示例结构：**
```
[Opening hook - set the scene]
[long pause]

[Story development with character emotions]
[short pause] between sentences
[long pause] between paragraphs

[Climax with dramatic tension]
[long pause]

[Resolution and emotional closure]
```

### 播客
**风格：** 对话式且引人入胜
- 温暖的开场白（15-30秒）
- 主要内容流畅自然
- 主题之间的过渡
- 包含关键内容的难忘结尾
- 全程采用对话式的语气

**示例结构：**
```
**Intro:** "Welcome to [topic]. I'm excited to share..."
[short pause]

**Main Content:** "Let's start with... [topic 1]"
[long pause] between segments

**Outro:** "Thanks for listening! Remember..."
```

### 教育内容
**风格：** 通俗易懂的解释
- 对复杂主题的简单介绍
- 分步讲解
- 使用现实生活中的例子和类比
- 在结尾总结关键概念
- 用 `[excited]`（兴奋）等语气来强调重要内容

**示例结构：**
```
**Introduction:** What is [topic] and why it matters?

**Main Content:**
- Concept 1: Explanation + Example
- Concept 2: Explanation + Example
- Concept 3: Explanation + Example

**Summary:** Key takeaways and next steps
```

## 长度指南

**字数与时长转换：**
- 5分钟 = 约375字
- 10分钟 = 约750字
- 15分钟 = 约1,125字
- 20分钟 = 约1,500字
- 30分钟 = 约2,250字

**节奏：** 平均对话速度约为每分钟75字

**实际限制：**
- 最短时长：2分钟（约150字）
- 最长时长：30分钟（约2,250字）
- 最佳时长：5-15分钟，以保持最佳互动性

## 工作流程说明

### 第1步：理解用户需求

解析用户的需求：
1. **内容类型**（有声书、播客、教育内容，或根据主题推断）
2. **主题/内容**（内容应该关于什么）
3. **目标时长**（时长多少分钟）
4. **语气/风格**（戏剧性、随意、教育性等）
5. **特殊要求**（特定声音、强调某些要点）

### 第2步：计算字数

```
target_words = target_minutes × 75
```

示例：10分钟 = 10 × 75 = 750字

### 第3步：生成剧本

根据以下规则编写完整的剧本：

**内容指南：**
- 以引人入胜的开场白开始
- 保持自然的对话节奏
- 使用主动语态和简单的句子结构
- 包含相关的例子和故事
- 以令人满意的结尾结束

**格式规则：**
- 句子后添加 `[short pause]`（短暂停顿，不要每个句子都加）
- 段落或主要部分之间添加 `[long pause]`（较长停顿）
- 战略性地使用语音效果：`[whispers]`、`[shouts]`、`[excited]`、`[serious]`、`[sarcastic]`、`[sings]`、`[laughs]`
- 数字用文字表示：例如“twenty-three”而不是“23”
- 首次出现缩写时需完整拼写：如“AI”或“artificial intelligence”
- 避免使用复杂的标点符号（破折号可以，但分号不易阅读）

### 第4步：展示剧本

向用户展示剧本并询问用户意见：
```
Here's the [format] script I've created (approximately [length] minutes):

[Display the script]

Would you like me to:
1. Generate the audio now
2. Make changes to the script
3. Adjust the length or tone
```

### 第5步：处理用户反馈

如果用户要求修改：
- 根据修改意见重新生成剧本
- 确保字数符合目标
- 展示修改后的版本

如果用户同意：
- 进行音频生成

### 第6步：生成音频

**将剧本格式化为TTS格式：**
1. 删除所有剩余的Markdown格式（标题、粗体、斜体）
2. 确保语音效果使用正确的 `[effect]` 格式
3. 检查停顿是否放置得当
4. 验证数字和缩写是否拼写正确

**调用TTS脚本：**

**重要提示：** `ELEVENLABS_API_KEY` 环境变量已在系统中配置。可以直接调用TTS脚本。

```bash
uv run /home/clawdbot/clawdbot/skills/sag/scripts/tts.py \
  -o /tmp/audio-gen-[timestamp]-[topic-slug].mp3 \
  -m eleven_multilingual_v2 \
  "[formatted_script]"
```

**对于较长的剧本，可以使用 heredoc：**
```bash
uv run /home/clawdbot/clawdbot/skills/sag/scripts/tts.py \
  -o /tmp/audio-gen-[timestamp]-[topic-slug].mp3 \
  -m eleven_multilingual_v2 \
  "$(cat <<'EOF'
[formatted_script]
EOF
)"
```

**返回结果：**
```
MEDIA:/tmp/audio-gen-[timestamp]-[topic-slug].mp3

Your [format] is ready! [Brief description of content]. Duration: approximately [X] minutes.
```

## 语音效果（SSML标签）

可用的语音调节效果（根据需要谨慎使用）：

- `[whispers]` - 轻柔、亲密的朗读方式
- `[shouts]` - 大声、强调的朗读方式
- `[excited]` - 兴奋、充满活力的语气
- `[serious]` - 严肃、庄重的语气
- `[sarcastic]` - 讽刺、嘲讽的语气
- `[sings]` - 有音乐感、旋律化的朗读方式
- `[laughs]` - 愉快、轻松的语气
- `[short pause]` - 短暂的停顿（约0.5秒）
- `[long pause]` - 长时间的停顿（约1-2秒）

**最佳实践：**
- 仅在需要表达情感的场合使用语音效果
- 停顿是控制节奏的最有效工具
- 语音效果在有声书和戏剧性内容中效果最佳
- 播客和教育内容应尽量保持自然的语气

## 错误处理

### 剧本过长
如果生成的剧本超出目标字数的20%：
```
The script I generated is [X] words ([Y] minutes), which is longer than your target of [Z] minutes. Would you like me to:
1. Condense it to fit the target length
2. Split it into multiple parts
3. Keep it as is
```

### 剧本过短
如果生成的剧本少于目标字数的20%：
```
The script is [X] words ([Y] minutes), shorter than your target. Would you like me to:
1. Expand it with more detail
2. Add additional examples or stories
3. Generate as is
```

### TTS生成失败
如果TTS脚本生成失败：
```
I've created the script, but I'm unable to generate the audio right now. Here's your script:

[Display script]

Error: [specific error message]

You can:
1. Check that ELEVENLABS_API_KEY is configured
2. Use the script with your own text-to-speech tool
3. Try again in a moment
4. Ask me to troubleshoot the audio generation
```

**常见的TTS问题：**
- API密钥未设置：请检查配置中的 `ELEVENLABS_API_KEY`
- 速率限制：稍等片刻后再试
- 文本过长：将文本分成较小的部分（每段最多5000个字符）

### 无效请求
对于不切实际的请求（例如“100小时的有声书”）：
```
That length would require [X] words and take significant time to generate. I recommend:
- Breaking it into multiple episodes/chapters
- Targeting 5-30 minutes per audio file
- Creating a series instead of one long file
```

## 提高效果的技巧

### 为了制作引人入胜的有声书：
- 关注角色的情感和感官细节
- 使用停顿来营造戏剧性紧张感
- 变换句子长度以保持节奏
- 包括角色的内心独白和反思

### 为了制作引人入胜的播客：
- 以一个问题或令人惊讶的事实开头
- 使用对话式表达：“你知道吗……”
- 包含日常生活中的相关例子
- 以实用的建议或结论结束

### 为了制作有效的教育内容：
- 采用“像给五岁孩子解释一样”的方式
- 从简单概念开始逐步讲解
- 重复关键术语和定义
- 提供多个例子以便于理解

## 技术说明

**TTS实现：**
- 使用Python脚本：`~/.clawdbot/clawdbot/skills/sag/scripts/tts.py`
- 无需安装二进制文件（纯Python + requests库）
- 直接调用ElevenLabs API
- 兼容Linux和macOS系统

**文件存储：**
- 音频文件保存在 `/tmp/audio-gen/` 目录下
- 文件名格式：`audio-gen-[timestamp]-[topic-slug].mp3`
- 文件会在24小时后自动删除

**API要求：**
- 使用Anthropic API生成剧本（已配置）
- 使用ElevenLabs API进行文本转语音（通过 `ELEVENLABS_API_KEY` 配置）
- 两个服务都必须已配置并拥有足够的信用额度

**支持的模型：**
- `eleven_multilingual_v2` - 最高质量（默认）
- `eleven_turbo_v2` - 生成速度更快
- `eleven_turbo_v2_5` - 生成速度最快
- `eleven_multilingual_v1` - 旧版本模型

**成本估算：**
- 10分钟音频（约750字）：大约1.43美元
  - Claude API：约0.075美元
  - ElevenLabs：约1.35美元
- 更长的内容费用按比例增加

**生成时间：**
- 剧本生成：5-30秒（取决于长度）
- 音频生成：5-15秒（ElevenLabs处理时间）
- 总时间：通常10分钟音频的生成时间不到1分钟

## 限制

1. **最大时长：** 每个音频文件最长30分钟（约2,250字）
   - 对于更长的内容，需要分多部分/多集制作

2. **单声道：** 目前仅支持一个旁白声音
   - 无法实现多角色对话或角色配音

3. **无背景音乐：** 仅提供纯语音朗读
   - 不支持背景音乐、音效或音频混音

4. **实时生成：** 每个请求都会生成新的内容
   - 不提供预制作的模板或缓存音频

5. **语言：** 主要支持英语
   - ElevenLabs也支持其他语言，但内容生成以英语为主

## 示例对话

### 示例1：快速制作有声书
```
User: Create a 5-minute audiobook chapter about a lonely robot learning to feel emotions

Agent: I'll create a 5-minute sci-fi audiobook chapter. Let me write the story...

[Generates ~400-word narrative with emotional arc]

Here's the story I've created about Unit-7, a maintenance robot who discovers the meaning of friendship through an unexpected encounter. Would you like me to generate the audio or make changes first?

User: Generate the audio

Agent: [Invokes SAG with formatted script]

MEDIA:/tmp/audio-gen-1234567890-lonely-robot.mp3

Your audiobook chapter is ready! The story follows Unit-7's emotional awakening through a touching encounter with a young engineer. Duration: approximately 5 minutes.
```

### 示例2：需要修改的播客
```
User: Make a 10-minute podcast about sustainable living tips

Agent: [Generates podcast script with intro, 5 practical tips, outro]

Here's a 10-minute podcast with 5 actionable sustainable living tips. The tone is encouraging and practical. Would you like me to:
1. Generate audio now
2. Make it more urgent/climate-focused
3. Add more specific examples
4. Adjust the length

User: Add more specific examples for each tip

Agent: [Regenerates with detailed examples]

Better? I've added specific examples like calculating your carbon footprint, composting at home, and choosing sustainable brands. Ready for audio?

User: Perfect!

Agent: MEDIA:/tmp/audio-gen-1234567890-sustainable-living.mp3

Your sustainable living podcast is ready with 5 practical tips, each with concrete examples you can start using today! Duration: 10 minutes.
```

### 示例3：教育内容
```
User: Create a 15-minute educational audio explaining quantum computing for beginners

Agent: I'll create a beginner-friendly 15-minute explanation of quantum computing...

[Generates ~1,100 words with analogies, examples, and clear structure]

Script preview:
- Introduction: What is quantum computing? (2 min)
- Classical vs Quantum: The key differences (4 min)
- Qubits and Superposition: How it works (5 min)
- Real Applications: What it means for you (3 min)
- Conclusion: The future of computing (1 min)

Should I generate the audio?

User: Yes please

Agent: MEDIA:/tmp/audio-gen-1234567890-quantum-computing.mp3

Your educational podcast on quantum computing is ready! It uses everyday analogies to explain qubits, superposition, and real-world applications. Duration: approximately 15 minutes.
```

## 适用场景

当用户请求以下内容时，可以使用此技能：
- “制作一本关于……的有声书”
- “制作一集关于……的播客”
- “生成解释……的音频内容”
- “录制一个关于……的故事”
- “制作一个……的音频指南”
- “制作一个……的音频课程”

**不适用场景：**
- 转录现有音频（请使用 whisper 技能）
- 将用户撰写的文本转换为音频（请直接使用 SAG 技能）
- 实时语音交互（请使用 voice-call 插件）
- 多个角色的对话或采访（当前功能有限）

## 高级用法

### 语音选择
用户可以指定所需的语音：
```
User: Create a podcast with the Rachel voice

Agent: [Checks voice configuration for "Rachel" voice ID and uses it in SAG command]
```

### 系列/剧集
对于多部分内容：
```
User: Create a 3-episode series about space exploration

Agent: I'll create Episode 1 first. Each episode will be 10 minutes. Let's start with "The Dawn of the Space Age"...

[After completion]

Episode 1 is ready! Would you like me to continue with Episode 2?
```

### 格式混合
结合不同格式以创造独特风格：
```
User: Create an educational podcast that tells a story

Agent: [Generates content that combines storytelling narrative with educational explanations]
```

## 故障排除

**问题：** 音频听起来机械或不自然
**解决方法：** 增加更多停顿和语音效果。使用缩写和对话式语言。

**问题：** 剧本长度不符合要求
**解决方法：** 重新生成剧本并明确字数目标。检查计算是否正确（每分钟75字）。

**问题：** 内容过于技术性或过于简单
**解决方法：** 询问目标受众，调整内容的复杂程度。

**问题：** SAG命令失败
**解决方法：** 确认 `ELEVENLABS_API_KEY` 已设置。检查 SAG 技能是否已安装并正常工作。

**问题：** 用户希望手动修改剧本
**解决方法：** 提供原始的文本剧本，用户可以修改后重新提交以生成音频。

---

💡 **专业提示：** 在创建音频之前，务必先生成剧本并获得用户确认。这样可以节省时间和API费用，同时确保用户获得他们想要的内容。