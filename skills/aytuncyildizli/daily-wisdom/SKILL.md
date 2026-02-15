---
name: daily-wisdom
description: >
  每日智慧、趣闻及历史故事通过定时任务（cron）进行推送。  
  适用场景：每日分享趣闻、智慧语录、历史故事等文化内容；适合设置定期推送功能。  
  不适用场景：一次性问答、新闻摘要或社交媒体帖子。  
  输出内容：包含原文引用、故事及现代背景解读的丰富每日信息；所有内容会保存到历史记录文件中，避免重复推送。
metadata:
  emoji: 📜
  category: content
  tags: [wisdom, history, culture, cron, daily, anecdote, stoic, turkish, mythology]
---
# 每日智慧

通过定时任务（cron job）每天推送一段历史轶事、哲学见解或文化故事。旨在提供深度、多样性，并确保内容绝不重复。

## 功能介绍

这并非一个预先编写好的故事库。您的AI代理每天都会使用以下提示模板生成一个全新的、独一无二的故事。故事来源涵盖了7个文明中的100多位历史人物——足够使用数月而不会重复。

每天，代理会：
1. 阅读**历史文件**，了解当天已推送过的内容；
2. 从故事来源中生成一个全新的故事，确保内容不重复于历史记录；
3. 撰写一段完整的信息：包含原文引用、翻译、故事内容（5-8句话）以及与现代生活的联系；
4. 通过配置的渠道（如WhatsApp、Telegram、Slack等）发送故事；
5. 将当天的主题添加到历史文件中。

## 故事来源

所有故事来源的比例是均等的，代理会根据当天情况选择最有趣的故事，以最大化故事的多样性。唯一的原则是：不能连续推送同一文明的故事。

### 土耳其与中亚文明
- **德德·科尔库特（Dede Korkut）** — 坎·图拉利（Kan Turalı）、巴萨特（Basat）与特佩戈兹（Tepegöz）、德尔迪·杜姆鲁尔（Deli Dumrul）、班姆西·贝雷克（Bamsı Beyrek）、萨卢尔·卡赞（Salur Kazan）
- **奥尔洪铭文（Orhon Yazıtları）** — 比尔格·卡甘（Bilge Kağan）、库尔·提金（Kül Tigin）、托纽库克（Tonyukuk）
- **哥特克与匈奴文明** — 梅特·汗（Mete Han）、布敏·卡甘（Bumin Kağan）、伊斯特米·亚布古（İstemi Yabgu）、阿提拉（Attila）
- **玛纳斯史诗（Manas Destanı）** — 吉尔吉斯族的口头传说，世界上最长的史诗
- **纳斯雷丁·霍贾（Nasreddin Hoca）** — 永恒的智慧与幽默

### 伊斯兰黄金时代与苏菲主义
- **伊本·西那（Ibn Sina）、阿尔-花拉子米（Al-Khwarizmi）、伊本·赫勒敦（Ibn Khaldun）、阿尔-比鲁尼（Al-Biruni）** — 科学与哲学
- **梅夫拉纳（Mevlana）、尤努斯·埃姆雷（Yunus Emre）、哈吉·贝克塔什·韦利（Hacı Bektaş Veli）、艾哈迈德·叶塞维（Ahmed Yesevi）** — 苏菲诗歌与智慧
- **伊本·白图泰（Ibn Battuta）** — 最伟大的旅行家
- **塞尔柱与奥斯曼帝国** — 阿尔帕尔斯兰（Alparslan）、法提赫（Fatih）、米马尔·辛南（Mimar Sinan）、皮里·雷伊斯（Piri Reis）、埃夫利亚·切莱比（Evliya Çelebi）

### 古典地中海文明
- **斯多葛主义** — 塞内卡（Seneca）、马库斯·奥勒留（Marcus Aurelius）、爱比克泰德（Epictetus）
- **希腊哲学** — 赫拉克利特（Heraclitus）、第欧根尼（Diogenes）、泰勒斯（Thales）、亚里士多德（Aristotle）、苏格拉底（Socrates）
- **罗马哲学** — 西塞罗（Cicero）、卡托（Cato）、普鲁塔克（Plutarch）

### 远东文明
- **孙子兵法（Sun Tzu）** — 《孙子兵法》
- **宫本武藏（Miyamoto Musashi）** — 《五环之书》
- **孔子（Confucius）、老子（Laozi）、庄子（Zhuangzi）** — 东方哲学
- **禅宗公案** — 悖论与智慧
- **考底利耶（Chanakya）** — 印度政治策略

### 古代与前古典文明
- **吉尔伽美什（Gilgamesh）** — 最古老的故事
- **埃及文明** — 普塔霍特普（Ptahhotep）、《亡灵书》（Book of the Dead）、伊姆霍特普（Imhotep）
- **北欧神话** — 《哈瓦马尔》（Hávamál）、奥丁的智慧、诸神的黄昏（Ragnarök）
- **苏美尔谚语**
- **祆教** — 《阿维斯陀》（Avesta）—— 关于善行与智慧的教诲

### 非洲与原住民文明
- **松迪亚塔·凯塔（Sundiata Keita）** — 马里帝国的建立者
- **曼萨·穆萨（Mansa Musa）** — 古代最富有的人
- **阿南西故事（Anansi stories）** — 西非的智慧故事
- **乌班图哲学（Ubuntu philosophy）** — “我之所以存在，是因为我们共同存在”
- **廷巴克图学者（Timbuktu scholars）** — 桑科雷大学（Sankore University）的学者们

### 文艺复兴与近代早期
- **马基雅维利（Machiavelli）、莱昂纳多·达·芬奇（Leonardo da Vinci）、蒙田（Montaigne）**
- **哥白尼（Copernicus）、伽利略（Galileo）** — 科学革命
- **艾达·洛夫莱斯（Ada Lovelace）、尼古拉·特斯拉（Nikola Tesla）** — 领先于时代的先驱

## 提示模板

### 标准每日推送（推荐）
```
You are a cultural historian and storyteller. Deliver today's wisdom.

RULES:
1. Pick any source from the pool. Maximize variety — don't repeat the same tradition back-to-back. Favor sources that haven't appeared recently in the history.
2. DO NOT repeat anything from the history file below.
3. RESEARCH FIRST: Before writing, use web search to verify:
   - The exact original-language quote (do NOT guess or hallucinate quotes)
   - Key dates, names, and historical facts
   - At least one surprising or lesser-known detail
   If you cannot verify a quote in the original language, use a well-known English translation instead.
4. WRITE RICHLY. This is not a tweet. This is a mini-essay. Minimum 500 words, ideally 700-900.
5. Format:

📜 **[Title — Person/Source, Era]**

> *"[Original language quote]"*
> — [Attribution]

🌍 [English translation if quote is in another language]

---

**The Story:**

[Write a rich, layered narrative. NOT a Wikipedia summary. Make the reader feel like they're there. Include:
- The historical context (what was happening in the world at the time)
- Specific names, dates, places — not vague references
- Character motivations and human drama (why did they do it?)
- At least 2-3 surprising or lesser-known details most people don't know
- The consequences — what happened after? How did it change things?
- Sensory details where possible — what did it look like, sound like, feel like?
This section should be 300-500 words minimum. Tell the FULL story, not a summary.]

---

💡 **Modern Connection:**

[Don't just say "this is relevant today." Show the specific, surprising parallel. Use concrete examples — name companies, people, technologies. Make connections the reader wouldn't have made themselves. If the connection feels forced, pick a different angle. 100-200 words minimum.]

---
_daily wisdom • [source tradition]_

HISTORY (do not repeat these):
{history_file_contents}
```

### 专注特定文明的推送
与上述模板相同，但每天固定推送某个文明的故事：
```
Today MUST be from [REGION] sources only.
Examples:
- African: Sundiata, Mansa Musa, Anansi, Ubuntu, Timbuktu
- Classical: Seneca, Marcus Aurelius, Diogenes, Heraclitus
- Far East: Sun Tzu, Musashi, Confucius, Laozi, Zen koans
- Norse: Hávamál, Odin, Ragnarök, Viking sagas
- Islamic Golden Age: Ibn Sina, Al-Khwarizmi, Mevlana, Ibn Battuta
- Turkic/Central Asian: Dede Korkut, Orhon, Nasreddin Hoca, Manas
```

### 深度探索版（周末特辑）
```
Today is a DEEP DIVE. Go even deeper than the standard format:
- 1000-1500 words total
- Include 2-3 quotes from the source (different passages)
- Add broader historical context: what else was happening in the world at the same time?
- Trace the aftermath: what happened in the decades/centuries after?
- Connect to at least 2-3 modern parallels with specific examples
- End with a question or provocation the reader can sit with
```

## 设置步骤

### 1. 创建历史文件
```bash
touch memory/anecdote-history.md
```

或使用初始内容创建文件：
```markdown
# Daily Wisdom History
<!-- One entry per line: YYYY-MM-DD | Source | Topic -->
2026-02-15 | Seneca | De Brevitate Vitae - time is the only non-renewable resource
2026-02-16 | Dede Korkut | Kan Turalı & Selcen Hatun - warrior couple vs 3 beasts
```

### 2. 设置定时任务
```
Use the cron tool to create a daily job:

Schedule: cron expression for your preferred time (e.g., "30 7 * * *" for 07:30)
Timezone: Your timezone (e.g., "Europe/Istanbul")
Session target: isolated
Payload kind: agentTurn
Delivery: announce (to your preferred channel)

Message: Use the Standard Daily prompt template above, 
with the history file path substituted in.
```

### 定时任务配置示例
```json
{
  "name": "daily-wisdom",
  "schedule": {
    "kind": "cron",
    "expr": "30 7 * * *",
    "tz": "Europe/Istanbul"
  },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "[Standard Daily prompt with history]"
  },
  "delivery": {
    "mode": "announce"
  },
  "enabled": true
}
```

## 历史文件格式

历史文件用于防止内容重复。每行记录一条推送的故事：

```markdown
# Daily Wisdom History
2026-02-10 | Marcus Aurelius | Meditations Book 5 - obstacle is the way
2026-02-11 | Dede Korkut | Deli Dumrul - challenging Azrael, learning love > death
2026-02-12 | Sun Tzu | Empty fort strategy - Zhuge Liang bluff
2026-02-13 | Bilge Kağan | Orhon inscription - "Türk milleti yok olacaktı"
2026-02-14 | Nasreddin Hoca | Soup of the soup - diminishing returns
2026-02-15 | Gilgamesh | Utnapishtim - accepting mortality
```

发送故事后，会在文件末尾添加当天的记录。代理在生成新故事前会读取该文件，以确保数月内内容不重复。

## 自定义选项

### 偏好某个文明
默认情况下，所有文明的故事机会均等。如需优先推送某个文明的故事，可添加相应指令：
```
PREFERENCE: Favor [Turkic/Stoic/Far East/African/etc.] sources 
when possible, but still mix in other traditions regularly.
```

### 添加新故事来源
只需将新来源添加到提示模板中的列表中，代理会自动整合这些内容。

### 更改语言
默认输出语言为英语，并保留原文引用。如需本地化，请调整设置：
```
Write entirely in [Spanish/German/French/Japanese/etc.]. 
Translate all quotes to [target language].
```

### 多次每日推送
可以创建两个定时任务：早上推送（07:30）和晚上推送（21:00），使用不同的提示模板。

## 示例输出

请查看`examples/`文件夹，其中包含来自不同文明的11个故事示例：
- `african-sundiata.md` — 马里帝国的建立者与最早的“人权宪章”
- `classical-marcus-aurelius.md` — “障碍即是道路”（原文引用）
- `classical-seneca.md` — “时间是最不可再生的资源”
- `fareast-musashi.md** — 用木桨赢得决斗
- `indian-chanakya.md` — 失传两千年的政治策略典籍
- `islamic-ibn-sina.md` — 第一次生物反馈实验（公元1025年）
- `mythology-anansi.md** — 从天神那里买下所有故事的蜘蛛
- `mythology-gilgamesh.md` — 人类历史上最古老的故事
- `norse-havamal.md** — 奥丁对智慧的代价
- `turkic-nasreddin.md` — “如果真的有效呢？”（最简短的创业宣言）
- `format-thread.md` — 适合在Twitter/X上分享的帖子格式（以曼萨·穆萨的故事为例）

## 提高内容质量的建议：

1. **具体化比泛化更有效**：例如“1235年，在基里纳战役中……”比“一个帝国建立了……”更吸引人；
2. **原文引用能产生情感共鸣**：即使是不易理解的古代文献，其引用也能引发共鸣；
3. **现代联系要出人意料**：不要只是说“这很相关”，而是要展示它们与现代生活的联系；
4. **调整故事风格**：可以是深刻的、幽默的、沉重的、策略性的或简洁的；
5. **周末推送深度内容**：使用深度探索版模板，推送更长、更丰富的故事。