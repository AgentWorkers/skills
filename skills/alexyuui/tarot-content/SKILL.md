---
name: tarot-content
description: 为社交媒体生成塔罗牌与占星术相关的内容——包括每周运势解析脚本、塔罗牌占卜图解、视频脚本以及封面设计。当收到“创建塔罗牌内容”、“每周运势”、“塔罗牌解读脚本”、“黄道带相关视频”、“占星术内容日历”、“塔罗牌占卜图设计”或“运势视频脚本”等请求时，均可使用这些资源。支持为12个星座提供每周运势解读，以及针对特殊事件（如行星逆行、日食、行星合相）制作的专题内容，并支持多种平台格式（YouTube Shorts、TikTok、Instagram、博客等）。
---
# Tarot内容生成器

该工具能够大规模地为社交媒体生成专业的塔罗牌与占星内容。

## 功能

1. **每周12星座运势解读** — 通过塔罗牌抽选制作的运势视频
2. **基于事件的专题内容** — 针对重要天文现象（如行星逆行、日食、合相）的内容
3. **自定义塔罗牌布局** — 提供可解读的塔罗牌布局设计
4. **视频脚本** — 适合语音合成（TTS）的脚本，包含屏幕文字提示
5. **封面图片** — 由Pillow生成的适合移动设备的缩略图
6. **内容日程表** — 根据占星事件自动安排内容发布

## 快速入门

### 每周12星座运势解读

```
Generate a weekly tarot reading for all 12 signs.
Date range: {start} to {end}
Style: conversational, no jargon
Format: video script with screen text cues
```

该工具将：
1. 获取真实的星历数据（行星位置、相位关系）
2. 将行星位置映射到每个星座的宫位系统中
3. 抽选塔罗牌（“挑战”、“指引”或“祝福”布局）
4. 用自然、引人入胜的语气撰写解读脚本

### 基于事件的专题内容

```
Create a special video about {transit/event}.
Example: Saturn conjunct Neptune in Aries
Include: what it means, historical context, 12-sign breakdown
```

## 内容框架

### 三张牌塔罗牌布局（“挑战”、“指引”或“祝福”）

这是一种经过验证的每周运势解读框架：

| 位置 | 含义 | 语气 |
|----------|---------|------|
| 挑战 | 需要警惕的事项 | 诚实、不吓人 |
| 指引 | 应该关注的重点 | 可操作的建议 |
| 祝福 | 即将发生的事情 | 充满希望、鼓舞人心 |

### 脚本结构（每个星座，60-90秒）

```
1. Opening hook (5s) — "Hey {Sign}, this week is about..."
2. Transit context (10s) — What planets are doing in their house
3. Card 1: Challenge (15s) — The obstacle + real-life scenario
4. Card 2: Guidance (15s) — Practical advice
5. Card 3: Blessing (10s) — The reward / positive outcome
6. CTA (5s) — "Follow for your sign's weekly reading"
```

### 写作风格指南

- **像朋友一样表达，而不是像算命师一样** — 例如：“你可能会感到停滞不前”，而不是“塔罗牌显示你正处于停滞状态”
- **使用具体场景** — 例如：“那个同事之间的纷争？是时候设定界限了”，而不是“人际关系中的冲突”
- **用文字代替数字** — 例如“二十二点二十六分”，而不是“2026”
- **避免制造恐惧** — 即使是负面的牌，也要给出建设性的解读
- **杜绝陈词滥调** — 禁止使用“宇宙自有安排”、“相信这个过程”、“一切都有其原因”之类的说法

## 星历数据

### 推荐使用pyswisseph工具

```python
import swisseph as swe
from datetime import datetime

def get_planet_position(planet_id, dt):
    """Get planet longitude in zodiac."""
    jd = swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute/60)
    pos = swe.calc_ut(jd, planet_id)[0]
    longitude = pos[0]
    sign_num = int(longitude / 30)
    degree = longitude % 30
    signs = ['Aries','Taurus','Gemini','Cancer','Leo','Virgo',
             'Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces']
    return signs[sign_num], degree

# Planet IDs: SUN=0, MOON=1, MERCURY=2, VENUS=3, MARS=4,
#             JUPITER=5, SATURN=6, URANUS=7, NEPTUNE=8, PLUTO=9
```

### 安装pyswisseph

```bash
pip install pyswisseph
```

## 封面图片生成

### 使用Pillow工具生成封面图片（避免人工智能生成的文字瑕疵）

```python
from PIL import Image, ImageDraw, ImageFont
import os

def generate_cover(sign, hook_text, date_range, colors, output_path):
    """Generate a 1080x1920 Shorts cover."""
    W, H = 1080, 1920
    img = Image.new('RGB', (W, H))
    draw = ImageDraw.Draw(img)

    # Gradient background
    for y in range(H):
        r = int(colors[0][0] + (colors[1][0]-colors[0][0]) * y/H)
        g = int(colors[0][1] + (colors[1][1]-colors[0][1]) * y/H)
        b = int(colors[0][2] + (colors[1][2]-colors[0][2]) * y/H)
        draw.line([(0,y),(W,y)], fill=(r,g,b))

    # Load fonts (adjust paths for your system)
    font_lg = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 120)
    font_md = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 56)
    font_sm = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 40)

    # Sign name (large, centered)
    draw.text((W//2, H*0.35), sign.upper(), font=font_lg, fill='white', anchor='mm')

    # Date range
    draw.text((W//2, H*0.48), date_range, font=font_md, fill=(255,215,0), anchor='mm')

    # Hook text
    draw.text((W//2, H*0.62), hook_text, font=font_md, fill='white', anchor='mm')

    # Brand
    draw.text((W//2, H*0.78), "WEEKLY TAROT", font=font_sm, fill=(200,200,200), anchor='mm')

    img.save(output_path, quality=95)

# Color schemes per sign
SIGN_COLORS = {
    'aries':       [(220,50,30),  (120,20,60)],
    'taurus':      [(30,120,50),  (15,60,30)],
    'gemini':      [(230,200,40), (180,120,20)],
    'cancer':      [(150,180,220),(60,80,140)],
    'leo':         [(240,170,30), (200,100,10)],
    'virgo':       [(80,140,80),  (40,80,50)],
    'libra':       [(200,160,200),(120,80,150)],
    'scorpio':     [(140,20,40),  (60,10,40)],
    'sagittarius': [(160,80,180), (100,40,120)],
    'capricorn':   [(80,60,50),   (30,25,20)],
    'aquarius':    [(40,100,220), (20,50,140)],
    'pisces':      [(160,130,200),(80,60,130)],
}
```

### 封面设计规则
- ⚠️ **严禁使用Unicode形式的星座符号**（如♈♉等）——大多数字体会将其显示为☒
- 使用英文星座名称
- 文字必须在缩略图尺寸下仍可清晰阅读（适用于手机屏幕）
- 重要元素应避免出现在底部15%的区域内（以免被YouTube界面遮挡）

## 内容日程表

### 每周内容安排
| 时间 | 内容 | 平台 |
|-----|---------|----------|
| 周一 | 12星座运势解读（视频） | YouTube Shorts、TikTok |
| 周三 | 中期运势分析 | Instagram Reel |
| 周五 | 周末塔罗牌解读 | TikTok、YouTube Shorts |

### 基于星历事件的自动内容生成
- 水星逆行 → “生存指南”系列内容
- 满月/新月 → 月亮仪式 + 塔罗牌解读
- 日食期间 → “日食专题”内容
- 行星合相 → 深入解析 + 对12个星座的影响

## 敏感内容注意事项

不同平台的 content 政策各不相同。请避免以下内容：
- 健康/医疗方面的声明（例如“这张牌预示你会康复”）
- 财务建议（例如“现在投资，木星如此建议”）
- 令人恐惧的预测（例如“前方有危险”、“死亡牌意味着……”）
- 始终将运势解读视为一种反思工具，而非绝对的预言