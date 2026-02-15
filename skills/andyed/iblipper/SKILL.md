---
name: iblipper
description: 生成动态文字动画，以实现更具表现力的代理（agent）与人类之间的沟通。适用于需要通过视觉效果来传递信息的场景——例如公告、提醒、问候语、戏剧性的内容展示，或是任何需要超越纯文本表达效果的消息。生成的动画可以提供可分享的URL，也可以在画布（canvas）上显示。
---

# iBlipper - 动态文本合成器

iBlipper 可生成动画形式的动态文本，以更富有表现力、更吸引人的方式与用户交流。

**基础网址：** `https://andyed.github.io/iblipper2025/`

## 两种输出方式

### 方式 1：超链接（快速、通用）
生成一个可点击的链接——接收者在浏览器中查看动画效果。

```markdown
[▶️ MESSAGE TEXT](https://andyed.github.io/iblipper2025/#text=MESSAGE+TEXT&emotion=emphatic&dark=true&share=yes)
```

### 方式 2：GIF 文件下载（需要浏览器支持）
生成一个可下载的动画 GIF 文件，可附加到消息中。

```
https://andyed.github.io/iblipper2025/?export=gif#text=MESSAGE+TEXT&emotion=emphatic&dark=true
```

## URL 参数

所有参数都放在 **哈希片段** 中（`#param=value&param2=value2`）。

| 参数 | 类型 | 说明 | 默认值 |
|-----------|------|-------------|---------|
| `text` | 字符串 | 要显示的消息（URL 编码，空格用 `+` 表示） | — |
| `wpm` | 数字 | 每分钟显示的单词数（30-2500） | 300 |
| `density` | 数字 | 每帧显示的单词数（0.1-500） | 1 |
| `fill` | 布尔值 | 自动调整文本大小以填充屏幕 | true |
| `theme` | 数字 | 颜色主题索引（0-3） | 0 |
| `dark` | 布尔值 | 深色模式 | true |
| `emotion` | 字符串 | 动画样式预设（见下文） | neutral |
| `share` | 字符串 | 加载时自动播放（`yes`） | — |

## 动画样式预设（适用于正式场合）

| 动画样式 | 氛围 | 适用场景 |
|---------|------|----------|
| `neutral` | 清晰、专业 | 默认样式，适用于公告 |
| `hurry` | 快速、紧急 | 适用于时间敏感的警报 |
| `idyllic` | 慢速、梦幻、轻松 | 适用于诗意或平静的消息 |
| `question` | 好奇、引人思考 | 适用于疑问或需要思考的消息 |
| `response_required` | 紧急、有节奏感 | 适用于需要立即行动的消息 |
| `excited` | 活跃、充满激情 | 适用于庆祝或表达兴奋的情绪 |
| `playful` | 有趣、轻松愉快 | 适用于幽默或轻松的场合 |
| `emphatic` | 强烈、引人注目 | 适用于重要的声明 |
| `casual` | 手写风格、轻松随意 | 适用于友好的聊天 |
| `electric` | 有视觉冲击力的效果 | 适用于科技或现代风格的场景 |
| `wobbly` | 动态效果 | 适用于幽默或轻松的场合 |

*注：`matrix` 动画样式仍处于预发布阶段，请暂时避免使用。*

## 超链接示例

**重要公告：**
```markdown
[▶️ BREAKING NEWS](https://andyed.github.io/iblipper2025/#text=BREAKING+NEWS&emotion=emphatic&dark=true&share=yes)
```

**友好问候：**
```markdown
[▶️ Hey there!](https://andyed.github.io/iblipper2025/#text=Hey+there!&emotion=casual&dark=false&share=yes)
```

**庆祝活动：**
```markdown
[▶️ Congratulations!](https://andyed.github.io/iblipper2025/#text=Congratulations!&emotion=excited&share=yes)
```

## GIF 文件导出流程（需要浏览器支持）

1. 在浏览器中打开导出链接：
   ```
   browser action=open targetUrl="https://andyed.github.io/iblipper2025/?export=gif#text=Hello&emotion=emphatic" profile=chrome
   ```

2. 等待约 15-20 秒，直到动画生成并完成编码。

3. 找到下载的 GIF 文件：
   ```
   ls -t ~/Downloads/iblipper_*.gif | head -1
   ```

4. 将文件阅读或附加到您的消息中。

## 导出参数

| 参数 | 类型 | 说明 | 默认值 |
|-----------|------|-------------|---------|
| `export` | 字符串 | 格式：`gif`、`apng`、`png` | — |
| `width` | 数字 | 输出宽度（像素） | 480 |
| `fps` | 数字 | 每秒帧数（8、15、30） | 15 |

## 适用场景

✅ **适合用于：**
- 问候语和介绍
- 重要公告
- 庆祝活动
- 强烈的视觉效果
- 为消息增添个性

❌ **不适用的场景：**
- 长篇内容（建议使用 1-10 个单词）
- 紧急的安全提示（纯文本更快捷）

## 命令行脚本

如需快速生成链接，可使用附带的 shell 脚本：

```bash
# Basic usage
./scripts/iblipper.sh "Hello World"
# https://andyed.github.io/iblipper2025/#text=Hello+World&emotion=emphatic&dark=true&share=yes

# With emotion
./scripts/iblipper.sh "Breaking News" hurry

# Light mode
./scripts/iblipper.sh "Good Morning" idyllic light

# As markdown link
./scripts/iblipper.sh -m "Click me!" excited
# [▶️ Click me!](https://...)

# GIF export URL
./scripts/iblipper.sh --gif "Export this" playful
```

## 额外资源

- **[references/examples.md](references/examples.md)** — 按类别划分的实际使用案例
- **[references/emotions.md](references/emotions.md)** — 深入了解每种动画样式及其使用场景

## 使用建议

- **保持文本简洁** — 1-5 个单词最具效果
- **默认使用超链接** — 更快捷，适用于所有平台
- **选择 GIF 格式用于 Signal/iMessage** — 内嵌图片效果更佳
- **务必设置 `share=yes`** — 可避免跳转至额外页面
- **根据消息内容选择合适的动画样式** — 例如，庆祝场合使用 `excited`，重要信息使用 `emphatic`
- **开启深色模式** — 通常 `dark=true` 更适合阅读
- **谨慎使用动画效果** — 如果每条消息都使用动画，反而会失去独特性