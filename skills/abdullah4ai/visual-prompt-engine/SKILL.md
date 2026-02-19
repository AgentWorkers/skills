---
name: visual-prompt-engine
description: "生成多样化的、非重复性的图像提示，这些提示基于来自 Dribbble 和设计平台的真实视觉素材。  
**适用场景**：  
- 用户需要图像创意灵感；  
- 用户希望获得与设计相关的图像生成建议；  
- 用户希望避免使用重复性的人工智能生成的图像；  
- 用户请求“生成一个图像提示”或“给我一个创意的图像想法”。  
**不适用场景**：  
- 用户希望直接生成图像（请使用图像生成工具）；  
- 用户需要编辑现有的图像；  
- 用户仅需要文本内容。  
**特殊情况处理**：  
- 如果用户只是要求“生成一张图片”，建议先使用图像生成工具，然后再使用此功能来获取具体的图像生成提示。  
- 如果用户希望“改进现有的图像提示”，也可以使用此功能。  
- 如果用户经常收到重复性的人工智能生成的图像，使用此功能可以有效解决图像重复的问题。"
---
# Visual Prompt Engine

通过将真实的视觉参考资料输入到结构化的提示生成流程中，生成高质量、多样化的图像提示。

## 问题

AI代理在编写图像提示时往往会重复使用相同的视觉模式和陈词滥调。本技能通过将提示基于真实、流行的设计作品来打破这一循环。

## 架构

```
Dribbble Scraper → Style Cards → Prompt Generator → Quality Reviewer → Final Prompt
```

## 快速入门

### 1. 收集视觉参考资料

**推荐方法：基于浏览器的收集**（使用Dribbble插件自动请求）

使用浏览器工具（如Camofox、Playwright等）浏览`https://dribbble.com/shots/popular`，收集图片的URL、标题和图片文件URL，然后将其保存为JSON格式：

```bash
python3 scripts/scrape_dribbble.py --method import --import-file manual_shots.json --output data/references.json
```

**替代方法：RSS/HTML**（可能会被Web应用防火墙（WAF）阻止）

JSON导入格式示例：`[{"title": "...", "url": "https://dribbble.com/shots/...", "image_url": "..."}]`

### 2. 构建风格卡片

将原始的视觉参考资料转换为风格卡片：

```bash
python3 scripts/style_card.py build --input data/references.json --output data/style_cards.json
```

### 3. 生成提示

当用户请求图像提示时：

1. 从`data/style_cards.json`中读取可用的视觉参考资料
2. 选择1-3张与用户需求相关的风格卡片
3. 从`references/prompt-patterns.md`中读取多样化的提示结构
4. 从`references/visual-vocabulary.md`中获取精确的设计术语
5. 组合用户需求、风格卡片元素和不同的提示模式来生成新的提示
6. 检查`data/prompt_history.json`中是否有重复的提示，以避免重复
7. 将新生成的提示添加到历史记录中

### 4. 审查与交付

在交付提示之前，需要验证以下内容：
- 使用具体的视觉描述语言（而非泛泛的形容词）
- 提及风格卡片中的具体设计元素
- 使用的提示模式与前5个提示不同
- 包含构图、光线、色彩搭配和情感基调等元素

## 风格卡片规范

详细规范请参见`references/style-card-schema.md`。风格卡片包含以下字段：

| 字段 | 描述 |
|-------|-------------|
| `palette` | 从设计作品中提取的十六进制颜色 |
| `composition` | 布局结构（网格、不对称、居中等） |
| `typography` | 字体样式和粗细特征 |
| `mood` | 情感基调（强烈、极简、趣味等） |
| `textures` | 表面质感（玻璃、颗粒、哑光等） |
| `lighting` | 光线方向和性质 |
| `source_url` | 原始Dribbble图片的URL |
| `tags` | 设计类别 |

## 提示模式

详细的设计提示结构请参见`references/prompt-patterns.md`，其中包含12种以上的不同提示模式，以防止提示内容重复。

## 视觉术语

请参阅`references/visual-vocabulary.md`，其中包含了关于色彩、构图、光线、质感和字体的精确设计术语。使用这些专业术语，而非“漂亮”或“不错”之类的泛泛之词。

## 自动化（可选）

设置每日定时任务来更新视觉参考资料：

```bash
# Run daily to keep references current
python3 scripts/scrape_dribbble.py --output data/references.json --count 20
python3 scripts/style_card.py build --input data/references.json --output data/style_cards.json
```

## 数据目录

该工具将工作数据存储在`data/`目录下：

```
data/
├── references.json      # Raw Dribbble scrape results
├── style_cards.json     # Processed style cards
└── prompt_history.json  # Generated prompts (for deduplication)
```

如果`data/`目录不存在，请在首次运行时创建它。

## 依赖项

仅需要Python 3.9及以上版本及标准库。可选依赖项：`requests`和`beautifulsoup4`（用于实时数据抓取；如果未安装`beautifulsoup4`，则使用Dribbble的RSS接口）。

安装可选依赖项的命令如下：

```bash
pip install requests beautifulsoup4
```