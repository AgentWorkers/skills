---
name: content-repurposer
description: 将长篇内容转换为适用于不同平台的简短片段。我们的工具能够接收一篇博客文章、视频文字记录或播客笔记，然后生成适合在 Twitter、LinkedIn、电子邮件新闻通讯和 Instagram 上发布的帖子。在转换过程中，工具会保持语言风格的一致性，并根据每个平台的格式、长度和用户互动习惯进行调整。用户可以配置语言风格偏好、优先发布的平台以及输出格式。该工具适用于在多个渠道发布内容、重新利用现有素材，或通过单一内容最大化传播效果。
metadata:
  clawdbot:
    emoji: "♻️"
---

# 内容复用工具 — 一次创作，多平台发布

**别再重新格式化了，直接开始发布吧。**

你写了一篇很棒的文章，但现在你需要将它制作成适合在 Twitter、LinkedIn、新闻通讯或 Instagram 上发布的版本。这通常需要花费 4 个多小时的时间来进行重新编写、格式调整以及保持语言风格的一致性。但是，使用这个工具只需要 30 秒！

**内容复用工具** 可以将你的长篇内容（如博客文章、视频文字记录、播客笔记或文章）自动转换为适合不同平台的版本。核心信息不变，只是形式不同，但语言风格始终如一。

**它的独特之处在于：** 这不是一个简单的模板引擎，而是一种智能的适配系统。该工具能够理解每种平台对内容的需求：Twitter 喜欢简洁有力的开头和连贯的帖子结构；LinkedIn 注重专业的见解和故事性；新闻通讯需要易于阅读的段落和明确的行动号召（CTA）；Instagram 则需要吸引人的视觉元素和表情符号。只需一个命令，就能同时生成适用于五种平台的版本，随时可以发布。

## 问题所在

内容创作者常常面临这样的困扰：
- ✍️ 你花费 2-3 小时创作一篇精彩的博客文章
- 🔄 手动将其格式调整为适合 Twitter 的样式（45 分钟）
- 🔄 再调整以适应 LinkedIn（30 分钟）
- 🔄 写出适合新闻通讯的版本（30 分钟）
- 🔄 拟定适合 Instagram 的标题（20 分钟）
- 😤 总共需要 4 个多小时的时间来反复调整格式，而且语言风格仍然不一致

与此同时，你的内容库却因为重复性工作而闲置着。

## 解决方案

```bash
repurpose.sh blog-post.md
# → twitter-thread.txt
# → linkedin-post.txt
# → newsletter.md
# → instagram-caption.txt
# → threads-post.txt (bonus!)
```

只需 30 秒，就能生成适用于五种平台的版本，且语言风格完全保持一致，可以直接复制并发布。

## 设置步骤

1. 运行 `scripts/setup.sh` 命令来初始化配置文件
2. 使用 `~/.config/content-repurposer/config.json` 文件设置你的语言风格
3. 用 `scripts/repurpose.sh examples/sample-post.md --dry-run` 命令进行测试

## 配置文件

配置文件位于 `~/.config/content-repurposer/config.json`。详细结构请参考 `config.example.json`。

**关键配置项：**
- **voice**：语气、风格（专业/随意/幽默/教育性）
- **platforms**：启用/禁用目标平台，并设置优先级
- **twitter**：帖子长度（3-10 条推文）、开头方式、标签偏好
- **linkedin**：长度（1300-2000 字符）、故事风格、商业内容重点
- **newsletter**：段落格式、行动号召样式、主题行设计
- **instagram**：标题长度、表情符号使用频率、标签数量
- **output**：输出文件目录、文件命名规则、是否自动将最佳版本复制到剪贴板

## 脚本说明

| 脚本 | 功能 |
|--------|---------|
| `scripts/setup.sh` | 初始化配置目录 |
| `scripts/repurpose.sh` | 一次性生成所有平台的版本 |
| `scripts/twitter-thread.sh` | 仅生成适合 Twitter 的帖子 |
| `scripts/linkedin-post.sh` | 仅生成适合 LinkedIn 的帖子 |
| `scripts/newsletter.sh` | 仅生成适合新闻通讯的段落 |
| `scripts/instagram-caption.sh` | 仅生成适合 Instagram 的标题 |
| `scripts/threads-post.sh` | 仅生成适合 Meta Threads 的帖子 |

所有脚本都支持 `--platform-specific-options` 选项，以便进行个性化定制。

## 工作原理

1. **解析输入内容**：读取长篇内容（Markdown 格式、.txt 文件或 URL）
2. **提取核心信息**：提取主要观点、关键数据、引用和统计数据
3. **平台适配**：针对每个启用的平台：
   - 应用相应的格式规则（如帖子结构、字符限制、表情符号使用）
   - 保持配置中设定的语言风格
   - 添加平台特有的开头和行动号召
   - 优化内容以提升互动效果
4. **输出结果**：将处理后的内容保存到 `output/` 目录中，可选择复制到剪贴板

## 各平台的具体要求

### Twitter/X Threads
- **长度**：3-10 条推文（可配置）
- **格式**：编号或未编号，每条推文 280 个字符
- **开头**：引人注目的开头（问题、数据或强调性陈述）
- **结构**：引言 → 关键点 → 深入分析 → 行动号召
- **适用场景**：热点观点、实用指南、操作步骤

### LinkedIn
- **长度**：1300-2000 字符（适合阅读更多内容的长度）
- **格式**：纯文本格式，正文内不允许包含链接
- **开头**：个人故事或专业见解
- **结构**：引人入胜的开头 → 内容/背景 → 价值/启示 → 行动号召
- **适用场景**：商业洞察、职业发展建议、思想领导力分享

### 电子邮件新闻通讯
- **长度**：每个段落 200-500 字
- **格式**：易于阅读的段落结构，包含标题
- **开头**：吸引人的主题行和开头句子
- **结构**：主题 → 开头 → 关键点（列表/分段） → 行动号召
- **适用场景**：深入分析、精选内容、个人更新

### Instagram
- **长度**：150-300 字符（包含“...more”按钮前的部分）
- **格式**：大量使用表情符号，视觉效果突出
- **开头**：富有情感或引发好奇心的句子
- **结构**：引人入胜的开头 → 核心信息 → 标签（5-10 个）
- **适用场景**：视觉内容、激励性内容、小贴士

### Meta Threads
- **长度**：最多 500 字符
- **格式**：风格类似 Twitter，但篇幅稍长
- **开头**：对话式的表达方式
- **结构**：类似 Twitter 的结构，但是一篇完整的帖子
- **适用场景**：轻松的主题、快速分享的见解

## 语言风格的一致性

该工具通过配置文件来保持你原有的语言风格：

```json
"voice": {
  "tone": "professional-casual",
  "personality": ["direct", "insightful", "practical"],
  "avoid": ["corporate jargon", "hype", "clickbait"],
  "signature_phrases": ["Here's the thing:", "The reality:"],
  "emoji_level": "moderate"
}
```

无论转换到哪个平台，内容都会保持你特有的语言风格，让你听起来像你自己，而不是机械地使用模板。

## 示例工作流程

**输入**：一篇关于 AI 自动化工作流程的 1500 字博客文章

**输出**（30 秒后）：

```
output/
├── 2024-01-25-ai-automation/
│   ├── twitter-thread.txt        # 7-tweet thread
│   ├── linkedin-post.txt          # 1650-char post
│   ├── newsletter.md              # 3 sections with headers
│   ├── instagram-caption.txt      # 220 chars + hashtags
│   └── threads-post.txt           # 480-char casual take
```

复制、粘贴、发布即可。

## 高级用法

### 单一平台定制
```bash
twitter-thread.sh blog-post.md --tweets 5 --style bold
linkedin-post.sh blog-post.md --length short --b2b-focus
```

### 通过 URL 上传内容
```bash
repurpose.sh https://yourblog.com/post --platforms twitter,linkedin
```

### 批量处理
```bash
for file in content/*.md; do
  repurpose.sh "$file" --output archives/
done
```

### 单次使用时的自定义语言设置
```bash
repurpose.sh blog-post.md --tone witty --emoji high
```

## 使用技巧

1. **优先生成主题行**：为新闻通讯生成多个主题行选项
2. **多次测试开头**：生成多个开头选项，选择最合适的
3. **互动性检查**：每个版本是否都包含明确的行动号召？
4. **优先处理表现最好的平台**：先从效果最好的平台开始发布
5 **批量处理**：一次性处理一个月的内容

## 数据文件

**输出文件** 默认保存在 `~/content-repurposer-output/` 目录中（可配置）。

**适用场景：**
- **博主**：将一篇博客文章转化为多篇适合社交媒体的内容
- **播客主**：将播客笔记转化为宣传材料
- **课程开发者**：将课程讲义转化为营销内容
- **咨询师**：将一篇见解转化为适用于多个平台的分享内容
- **广告机构**：无需雇佣写手，即可高效生成多平台内容

## 注意事项

- ❌ **这不是内容生成器**：你需要提供原始内容
- ❌ **这不是发布调度工具**：使用 Buffer/Hootsuite 等工具来安排发布时间（我们只负责内容生成）
- ❌ **这不是图片制作工具**：仅处理文本内容（如需图片，可结合 DALL-E 工具）

**为什么这个工具有效？**

因为传统的内容复用方法存在以下问题：
- 手动操作效率低下
- 基于模板的生成方式显得机械
- 不考虑平台特性，无法针对每个平台进行优化

而这个工具解决了这些问题：快速、保持语言风格一致、同时针对每个平台进行优化。

**你的内容值得被更多人看到，你的时间也应该得到更好的利用。**

---

专为重视时间和语言风格的创作者设计。