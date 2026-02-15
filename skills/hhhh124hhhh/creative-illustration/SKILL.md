---
name: creative-illustration
description: 通过 OpenAI Images API 生成多样化的创意插图，包括书籍插图、编辑艺术作品、儿童图书插图以及概念艺术图。当用户需要为故事、文章、演示文稿或艺术项目提供创意视觉内容时，可以使用该服务（例如：“为童话场景绘制插图”、“创作关于技术的编辑艺术作品”、“设计儿童图书插图”、“为故事生成概念艺术图”）。
---

# 创意插画工厂

为书籍、编辑内容、儿童故事和创意项目生成专业的插画。

## 设置

- 需要的环境变量：`OPENAI_API_KEY`

## 快速入门

- 生成一个简单的插画：
  ```bash
  ```bash
python3 ~/Projects/agent-scripts/skills/creative-illustration/scripts/illustrate.py \
  --subject "a cozy cottage in an enchanted forest"
```
  ```

- 以特定风格生成插画：
  ```bash
  ```bash
python3 ~/Projects/agent-scripts/skills/creative-illustration/scripts/illustrate.py \
  --subject "a robot learning to paint" \
  --style "watercolor" \
  --mood "whimsical"
```
  ```

- 生成故事序列的插画：
  ```bash
  ```bash
python3 ~/Projects/agent-scripts/skills/creative-illustration/scripts/illustrate.py \
  --subject "Alice discovers a tiny door" \
  --subject "Alice shrinks down" \
  --subject "Alice enters Wonderland" \
  --style "whimsical illustration" \
  --mood "magical"
```
  ```

## 插画类型

### 书籍插画
- `chapter-opener`：全页的章节开头场景
- `character-intro`：角色介绍肖像
- `landscape-scene`：广阔的风景背景
- `action-moment`：动态的动作或关键时刻
- `emotional-scene`：充满情感或戏剧性的场景
- `cover-art`：书籍封面插画

### 编辑/杂志插画
- `conceptual-art`：抽象的概念插画
- `info-graphic`：信息性插画
- `portrait-editorial`：人物肖像
- `spot-illustration`：小型的插画
- `full-page-spread`：杂志的全页插画

### 儿童图书插画
- `picture-book`：经典风格的儿童图书插画
- `whimsical`：充满想象力的插画风格
- `educational`：教育类图书插画
- `bedtime-story`：柔和、舒缓的睡前故事插画
- `adventure-map`：冒险地图或宝藏地图

### 概念艺术
- `environment-concept`：环境概念艺术
- `character-concept`：角色设计概念
- `prop-concept`：道具或物品设计
- `storyboard`：故事板风格的插画
- `mood-board`：情绪板风格的插画

## 插画风格

### 传统媒体风格
- `watercolor`：水彩画（边缘柔和）
- `oil-painting`：丰富的油画质感
- `charcoal-sketch`：炭笔素描
- `ink-wash`：水墨画风格
- `pastel`：柔和的粉彩画
- `colored-pencil`：彩色铅笔插画
- `gouache`：不透明的水粉画
- `acrylic`：丙烯画风格
- `lino-cut`：油印版画
- `woodcut`：木刻版画

### 数字风格
- `digital-painting`：数字绘画
- `vector-illustration`：干净的矢量插画
- `flat-design`：扁平设计风格
- `isometric`：等轴测视角
- `pixel-art`：复古像素艺术
- `concept-art`：游戏/电影概念艺术
- `cel-shaded`：赛璐珞阴影动画风格
- `low-poly`：低多边形3D风格

### 书籍与印刷风格
- `picture-book`：经典风格的儿童图书插画
- `storybook-illustration`：复古风格的插画
- `editorial-illustration`：杂志插画
- `newspaper-engraving`：报纸雕刻风格
- `poster-art`：复古海报设计
- `woodblock-print`：日本木版画
- `screen-print`：丝网印刷风格

## 情感氛围
- `whimsical`：充满想象力的
- `magical`：神奇而迷人的
- `mysterious`：神秘而引人入胜的
- `peaceful`：宁静而平和的
- `dramatic`：戏剧性且强烈的
- `nostalgic`：温暖而怀旧的
- `gloomy`：阴暗而富有氛围的
- `vibrant`：明亮而充满活力的
- `romantic`：柔和而浪漫的
- `quirky`：古怪而独特的

## 参数

- `--subject`：插画的主题/描述（可批量重复使用）
- `--type`：插画类型（默认：插画）
- `--style`：艺术风格（默认：水彩）
- `--mood`：情感氛围（默认：宁静）
- `--palette`：颜色调色板建议
- `--composition`：构图指导（例如：“wide shot”（全景）、“close-up”（特写）
- `--count`：每个主题的变体数量（默认：1）
- `--out-dir`：输出目录（默认：~/Projects/tmp/creative-illustration-*)
- `--size`：图像尺寸：1024x1024、1792x1024、1024x1792（默认：1024x1024）
- `--quality`：高质量/标准质量（默认：高质量）
- `--model`：OpenAI图像模型（默认：gpt-image-1.5）
- `--api-key`：OpenAI API密钥（或使用环境变量 `OPENAI_API_KEY`）

## 高级示例

- 儿童图书页面：
  ```bash
  ```bash
python3 ~/Projects/agent-scripts/skills/creative-illustration/scripts/illustrate.py \
  --subject "a curious rabbit with a pocket watch" \
  --type "picture-book" \
  --style "watercolor" \
  --mood "whimsical" \
  --palette "pastel"
```
  ```

- 编辑概念艺术：
  ```bash
  ```bash
python3 ~/Projects/agent-scripts/skills/creative-illustration/scripts/illustrate.py \
  --subject "AI and humanity working together" \
  --type "conceptual-art" \
  --style "vector-illustration" \
  --mood "optimistic" \
  --composition "symbolic"
```
  ```

- 故事序列插画：
  ```bash
  ```bash
python3 ~/Projects/agent-scripts/skills/creative-illustration/scripts/illustrate.py \
  --subject "Hero finds an ancient map" \
  --subject "Hero deciphers mysterious symbols" \
  --subject "Hero discovers a hidden passage" \
  --subject "Hero enters the forgotten temple" \
  --style "storybook-illustration" \
  --mood "mysterious" \
  --palette "earth tones"
```
  ```

- 完全自定义的提示：
  ```bash
  ```bash
python3 ~/Projects/agent-scripts/skills/creative-illustration/scripts/illustrate.py \
  --prompt "A magical treehouse library nestled among ancient redwoods, spiral staircase winding up the trunk, lanterns hanging from branches, books floating in mid-air, warm golden light streaming through leaves, detailed watercolor illustration style, whimsical and enchanting"
```
  ```

## 颜色调色板
- `pastel`：柔和的粉彩色调
- `earth-tones`：自然的棕色、绿色、金色
- `vibrant`：鲜艳饱和的色彩
- `muted`：柔和、淡雅的色彩
- `monochrome`：单色变体
- `jewel-tones`：丰富的红宝石色、祖母绿色、蓝宝石色
- `autumn`：橙色、红色、黄色、棕色
- `winter`：蓝色、白色、银色、紫色
- `tropical`：明亮的绿色、青色、粉色
- `vintage`：温暖的棕褐色、褪色的色调

## 构图技巧
- `wide-shot`：广阔的风景背景
- `close-up`：亲密的特写
- `panoramic`：全景风景
- `rule-of-thirds`：三分法则
- `centered`：居中的主体
- `diagonal`：动态的对角线构图
- `triangular`：三角形的构图
- `circular`：圆形或螺旋形的构图
- `symmetrical`：完全对称的构图
- `asymmetrical`：不对称的构图

## 输出结果
- `*.png`：插画图像文件
- `prompts.json`：所有使用的提示信息
- `index.html`：插画画廊

## 项目模板

- **儿童图书（4-6张插画）**：
  ```bash
  ```bash
python3 ~/Projects/agent-scripts/skills/creative-illustration/scripts/illustrate.py \
  --subject "Girl finds a magical seed" \
  --subject "Seed grows into a glowing plant" \
  --subject "Plant reveals a tiny fairy" \
  --subject "Fairy shows girl a secret garden" \
  --subject "Girl shares garden with friends" \
  --type "picture-book" \
  --style "watercolor" \
  --mood "whimsical"
```
  ```

- **杂志编辑（1-2张插画）**：
  ```bash
  ```bash
python3 ~/Projects/agent-scripts/skills/creative-illustration/scripts/illustrate.py \
  --subject "The future of sustainable cities" \
  --type "conceptual-art" \
  --style "vector-illustration" \
  --mood "optimistic" \
  --count 2
```
  ```

- **奇幻故事章节开头（1张插画）**：
  ```bash
  ```bash
python3 ~/Projects/agent-scripts/skills/creative-illustration/scripts/illustrate.py \
  --subject "The dragon's treasure hoard under ancient runes" \
  --type "chapter-opener" \
  --style "oil-painting" \
  --mood "dramatic" \
  --palette "jewel tones"
```
  ```