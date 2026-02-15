---
name: xkcd
description: **功能说明：**  
- **获取 xkcd 漫画**：可以按最新、随机、编号顺序获取 xkcd 漫画，也可以通过关键词进行搜索。  
- **显示漫画信息**：每幅漫画会显示标题、图片以及隐藏的幽默文字（alt text）。  
- **生成自定义漫画**：利用图像生成技术，用户可以自定义漫画的样式和内容，打造属于自己风格的 xkcd 风格漫画。  
- **应用场景**：非常适合通过 cron 任务实现每日自动推送漫画、根据需求随时查看漫画，或创作受 xkcd 风格启发的原创内容。
homepage: https://xkcd.com
metadata: {"clawdbot":{"emoji":"📊","requires":{"bins":["uv"]}}}
---

# xkcd

从 xkcd.com 获取漫画或生成 xkcd 风格的图片。

## 命令

### 最新漫画
```bash
uv run {baseDir}/scripts/xkcd.py
```

### 随机漫画
```bash
uv run {baseDir}/scripts/xkcd.py --random
```

### 指定漫画
```bash
uv run {baseDir}/scripts/xkcd.py 327         # Bobby Tables
uv run {baseDir}/scripts/xkcd.py 353         # Python
uv run {baseDir}/scripts/xkcd.py 1053        # Ten Thousand
```

### 按关键词搜索
```bash
uv run {baseDir}/scripts/xkcd.py --search "python"
uv run {baseDir}/scripts/xkcd.py --search "space" --limit 3
```

### JSON 输出
```bash
uv run {baseDir}/scripts/xkcd.py --format json
uv run {baseDir}/scripts/xkcd.py --random --format json
```

## 输出格式

默认的 Markdown 输出格式包括：
- **标题**：漫画标题及编号
- **图片**：漫画的直接 URL
- **替代文本**：鼠标悬停时显示的文本（通常是最有趣的部分！）
- **链接**：xkcd.com 的永久链接

## 生成自定义的 xkcd 风格漫画

使用图像生成工具（例如 nano-banana-pro），并使用以下提示格式：

```
Create an xkcd-style comic: [your scene description]

Style: simple black and white stick figures, hand-drawn wobbly lines,
minimal background, clean white background, comic panel layout
```

示例提示：
```
Create an xkcd-style comic: Two programmers at computers. First says
"I spent 6 hours automating a task." Second: "How long did the task take?"
First: "5 minutes." Second: "How often do you do it?" First: "Once a year."
```

## Cron 任务示例

```bash
# Daily latest comic at 9 AM
cron add --schedule "0 9 * * *" --task "Fetch latest xkcd and send via Telegram"

# Random classic every Monday
cron add --schedule "0 10 * * 1" --task "Fetch random xkcd comic and share"
```

## 经典漫画

- **#327** “妈妈的诡计” — Bobby Tables / SQL 注入攻击
- **#353** “Python” — 使用 `import antigravity` 功能
- **#303** “编译代码” — 在代码编译过程中进行剑术对决
- **#386** “责任在召唤” — 网络上总有人犯错
- **#1053** “一万次” — 一万次尝试后终于学会新东西
- **#979** **古代的智慧** — 未得到回复的论坛帖子
- **#927** **标准** — 标准是如何传播的

## API

使用官方的 [xkcd JSON API](https://xkcd.com/json.html)（无需认证）：
- 获取最新漫画：`https://xkcd.com/info.0.json`
- 获取指定漫画的信息：`https://xkcd.com/{num}/info.0.json`