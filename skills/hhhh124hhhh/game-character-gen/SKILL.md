---
name: game-character-gen
description: 通过 OpenAI Images API 生成专业的游戏角色设计。为角色扮演游戏（RPGs）、视频游戏、桌面游戏以及交互式媒体创建多样化的角色。当用户需要角色概念图、角色肖像、游戏精灵图（game sprites）或包含特定属性的角色资料表（character sheets）时，可以使用该服务——例如：“创建一个精灵游荡者（elven ranger）的角色”，“设计一个赛博朋克黑客（cyberpunk hacker）的角色”，“生成一个奇幻战士（fantasy warrior）的角色”。
---

# 游戏角色生成器

该工具可为游戏生成详细的角色概念，可精确控制角色的种族、职业、装备和视觉风格。

## 设置

- 需要的环境变量：`OPENAI_API_KEY`

## 快速开始

生成一个基础角色：

```bash
python3 ~/Projects/agent-scripts/skills/game-character-gen/scripts/generate.py \
  --race "elf" \
  --class "ranger"
```

生成具有特定细节的角色：

```bash
python3 ~/Projects/agent-scripts/skills/game-character-gen/scripts/generate.py \
  --race "dragonborn" \
  --class "paladin" \
  --gender "female" \
  --equipment "plate armor, divine shield" \
  --style "epic fantasy painting"
```

批量生成角色：

```bash
python3 ~/Projects/agent-scripts/skills/game-character-gen/scripts/generate.py \
  --race "human" "dwarf" "tiefling" \
  --class "warrior" "mage" "rogue" \
  --style "dark fantasy" "anime" "realistic"
```

## 角色参数

### 种族（奇幻）
- `human` - 人类（多种族裔）
- `elf` - 高等精灵、木精灵、黑暗精灵（德罗）
- `dwarf` - 山地矮人、丘陵矮人
- `halfling` - 轻足半身人、矮胖半身人
- `gnome` - 岩地侏儒、森林侏儒
- `half-elf` - 半精灵血统
- `half-orc` - 半兽人血统
- `dragonborn` - 龙裔（多种龙族血统）
- `tiefling` - 提夫林（恶魔血统）
- `goliath` - 巨人
- `aasimar` - 天使族（神圣血统）
- `goblin` - 地精
- `hobgoblin` - 霍布格oblin
- `bugbear` - 野猪人
- `kenku` - 鸟人
- `tabaxi` - 猫人
- `lizardfolk` - 蜥蜴人
- `firbolg` - 火精灵
- `genasi` - 元素生物（风、土、火、水）

### 职业（奇幻）
- `warrior` - 战士、野蛮人、骑士
- `mage` - 巫师、术士、术士
- `cleric` - 牧师、祭司、圣骑士
- `rogue` - 恶棍、刺客、盗贼
- `ranger` - 游荡者、猎人、侦察兵
- `bard` - 吟游诗人、表演者
- `monk` - 武僧
- `druid` - 德鲁伊、萨满
- `artificer` - 工程师、工匠
- `inquisitor` - 审判官、调查员

### 种族（科幻/赛博朋克）
- `human-augmented` - 经过基因改造的人类
- `android` - 合成机器人
- `clone` - 克隆士兵
- `alien-humanoid` - 各种外星种族
- `cyborg` - 经过重度改造的半机械人
- `bio-engineered` - 基因改造生物

### 职业（科幻/赛博朋克）
- `hacker` - 网络黑客
- `soldier` - 雇佣兵、企业士兵
- `tech-specialist` - 工程师、技术专家
- `medic` - 战斗医疗兵
- `scout` - 侦察专家
- `pilot` - 星际飞船驾驶员
- `assassin` - 企业刺客
- `detective` - 调查员

### 装备
常见装备关键词（用逗号分隔）：
- `leather armor` / `chainmail` / `plate armor` / `cybernetic implants`（皮革盔甲 / 链甲 / 机械装甲 / 机械植入物）
- `sword and shield` / `greatsword` / `daggers` / `quarterstaff`（剑与盾 / 大剑 / 小刀 / 短杖）
- `crossbow` / `longbow` / `pistol` / `plasma rifle` / `laser pistol`（弩 / 长弓 / 手枪 / 等离子步枪）
- `spellbook` / `arcane focus` / `holy symbol` / `tech gauntlet`（魔法书 / 神秘法器 / 技术护手）
- `cloak` / `hooded cape` / `tactical vest` / `exosuit`（斗篷 / 帽兜斗篷 / 战术背心 / 外骨骼战甲）
- `backpack` / `tool belt` / `medical kit` / `hacking deck`（背包 / 工具带 / 医疗包 / 黑客工具包）

### 视觉风格
角色渲染的艺术风格：
- `epic fantasy painting` - 富丽堂皇的油画风格
- `realistic portrait` - 照实风格的肖像画
- `anime studio` - 动画/漫画风格
- `concept art` - 游戏概念艺术质量
- `illustration` - 详细插画
- `comic book` - 明显的漫画风格
- `pixel art` - 复古像素风格的角色
- `dark fantasy` - 暗黑奇幻风格
- `low poly` - 低多边形3D模型
- `cel shaded` - 半透明阴影风格的动画
- `watercolor` - 水彩风格
- `vintage fantasy` - 古典奇幻风格

### 性别 / 表情
- `male`（男性）、`female`（女性）、`non-binary`（非二元性别）、`androgynous`（雌雄同体）
- `young`（年轻）、`middle-aged`（中年）、`elderly`（老年）
- `stoic`（坚毅的）、`determined`（坚定的）、`mysterious`（神秘的）、`playful`（顽皮的）、`grim`（阴郁的）、`noble`（高贵的）

## 高级选项

自定义提示以获得完全控制：

```bash
python3 ~/Projects/agent-scripts/skills/game-character-gen/scripts/generate.py \
  --prompt "A rugged dwarven warrior with braided red beard, wearing ornate mithral plate armor decorated with runic engravings. He wields a massive warhammer with lightning crackling along the head. Battle-hardened expression, scars visible on face. Epic fantasy oil painting style, cinematic lighting, detailed textures."
```

包含角色信息表：

```bash
python3 ~/Projects/agent-scripts/skills/game-character-gen/scripts/generate.py \
  --race "human" \
  --class "mage" \
  --style "concept art" \
  --sheet
```

## 参数
- `--race` - 角色种族/物种（批量生成时可重复使用）
- `--class` - 角色职业/专长（批量生成时可重复使用）
- `--gender` - 性别身份
- `--equipment` - 装备和装备描述
- `--style` - 视觉风格（批量生成时可重复使用）
- `--prompt` - 完全自定义的提示（会覆盖其他选项）
- `--count` - 每个角色的变体数量（默认：1）
- `--sheet` - 生成包含角色数据的 `character_sheet.json` 文件
- `--out-dir` - 输出目录（默认：`~/Projects/tmp/game-character-gen-*`
- `--size` - 图像尺寸：1024x1024、1792x1024、1024x1792（默认：1024x1024）
- `--quality` - 高质量/标准质量（默认：高质量）
- `--model` - OpenAI图像模型（默认：`gpt-image-1.5`）
- `--api-key` - OpenAI API密钥（或使用环境变量 `OPENAI_API_KEY`）

## 角色信息表格式

使用 `--sheet` 选项时，会生成 `character_sheet.json` 文件，其中包含以下内容：

```json
{
  "name": "Generated Character",
  "race": "human",
  "class": "mage",
  "gender": "male",
  "equipment": ["staff", "robes"],
  "stats": {
    "strength": 8,
    "dexterity": 14,
    "constitution": 10,
    "intelligence": 18,
    "wisdom": 12,
    "charisma": 10
  },
  "image_file": "01-mage.png"
}
```

## 输出结果
- `*.png` - 角色图片
- `character_sheet.json` - 角色数据
- `prompts.json` - 所有使用的提示信息
- `index.html` - 角色图库

## 示例
- D&D 角色组：

```bash
python3 ~/Projects/agent-scripts/skills/game-character-gen/scripts/generate.py \
  --race "human" "elf" "dwarf" "half-orc" \
  --class "paladin" "ranger" "cleric" "barbarian" \
  --style "epic fantasy painting"
```

- 赛博朋克团队角色：

```bash
python3 ~/Projects/agent-scripts/skills/game-character-gen/scripts/generate.py \
  --race "human-augmented" "android" "clone" "cyborg" \
  --class "hacker" "soldier" "tech-specialist" "assassin" \
  --style "cyberpunk neon" \
  --equipment "hacking deck" "plasma rifle" "tool belt" "monowire"
```

- 儿童读物中的角色：

```bash
python3 ~/Projects/agent-scripts/skills/game-character-gen/scripts/generate.py \
  --race "human" "elf" "gnome" "fairy" \
  --class "adventurer" "wizard" "explorer" "healer" \
  --style "whimsical illustration" "watercolor"
```