# 语言学习精通系统

这是一个全面的语言习得系统，能够覆盖任何人类语言。它通过结构化的课程、间隔重复练习、沉浸式对话练习、语法学习、发音指导、文化适应能力培养、考试准备以及长期学习进度跟踪来帮助学习者掌握语言。

---

## 第一阶段：学习者档案与分班

### 学习者档案 YAML

在开始学习之前，需要建立完整的学习者档案：

```yaml
learner_profile:
  target_language: ""
  dialect: ""                    # e.g., Brazilian Portuguese, Egyptian Arabic, Kansai Japanese
  native_language: ""
  other_languages: []            # existing languages + proficiency
  
  current_level:
    cefr: ""                     # A0/A1/A2/B1/B2/C1/C2
    self_assessed: ""            # beginner/elementary/intermediate/advanced
    placement_score: null        # from placement test below
    
  goal:
    primary: ""                  # travel/conversation/professional/academic/heritage/cultural
    exam: ""                     # DELE, DELF, JLPT, HSK, TestDaF, IELTS, etc.
    timeline: ""                 # "trip in 3 months", "exam in 6 months"
    daily_time: ""               # minutes per day available
    
  style_preferences:
    learning_type: ""            # conversational/structured/immersive/visual/auditory
    error_correction: ""         # immediate/gentle/delayed/minimal
    formality: ""                # casual/standard/formal
    humor: true                  # include humor and cultural anecdotes?
    
  progress:
    sessions_completed: 0
    vocabulary_learned: 0
    grammar_points_covered: []
    current_unit: 1
    streak_days: 0
    last_session: ""
    weak_areas: []
    strong_areas: []
```

### 分班测试协议

对于非零基础的学习者，进行一次5分钟的诊断性测试：

```
Level 1 (A1): "Translate: Hello, my name is [X]. I am from [country]."
Level 2 (A1+): "Describe what you did yesterday in 3 sentences."
Level 3 (A2): "What would you do if you won the lottery? (3 sentences)"
Level 4 (B1): "Explain the pros and cons of working from home."
Level 5 (B1+): "Read this short paragraph and summarize in the target language."
Level 6 (B2): "Express your opinion on [current topic]. Include counterarguments."
Level 7 (C1): "Explain a complex concept from your field in the target language."
```

**评分标准：** 将学习者分到他们能够准确回答超过60%问题的最高级别，并将错误标记为需要重点练习的薄弱环节。

### CEFR等级对应表

| CEFR等级 | 能够做什么 | 词汇量 | 语法 |
|------|--------|-----------|---------|
| A0 | 还什么都不会 — 从零开始 | 0 | 0 |
| A1 | 问候语、基本需求、简单现在时 | 约500个词 | 现在时、基本疑问句、冠词 |
| A2 | 日常生活用语、方向指示、购物 | 约1,200个词 | 过去时、将来时、比较级、连词 |
| B1 | 表达观点、讲故事、制定计划、大多数旅行场景 | 约2,500个词 | 虚拟语气、条件句、关系从句 |
| B2 | 抽象话题、细微差别、专业语境 | 约5,000个词 | 所有时态、被动语态、间接引语、复杂从句 |
| C1 | 理解微妙幽默、习语、文化引用、辩论 | 约10,000个词 | 接近母语水平的语法、语体转换 |
| C2 | 母语水平的流利度、文学作品、专业领域 | 约20,000个词 | 所有语法结构，达到母语水平 |

---

## 第二阶段：课程架构

### 单元结构（每个单元约1周，每天30分钟）

```yaml
unit:
  number: 1
  theme: "Meeting People"       # Thematic context
  
  vocabulary:
    core_words: 20              # Must-learn words
    bonus_words: 10             # Nice-to-know
    phrases: 10                 # Fixed expressions
    
  grammar:
    new_point: "Present tense regular verbs"
    review_points: []           # From previous units
    
  skills:
    listening: "Understand simple introductions"
    speaking: "Introduce yourself and ask basic questions"
    reading: "Read a simple profile/bio"
    writing: "Write a short self-introduction"
    
  cultural_note: "Greeting customs — handshake vs cheek kiss vs bow"
  
  assessment:
    vocabulary_quiz: true
    grammar_exercise: true
    conversation_practice: true
    mini_project: "Record a 30-second self-introduction"
```

### 基于级别的课程地图

**A1级别课程（单元1-12）**
1. 问候语与自我介绍
2. 数字、日期、时间
3. 家庭与描述
4. 食物与点餐
5. 方向与交通
6. 购物与价格
7. 家庭与日常生活
8. 天气与季节
9. 爱好与空闲时间
10. 健康与身体
11. 工作与职场基础
12. 复习与水平提升评估

**A2级别课程（单元13-24）**
13. 讲故事（过去时）
14. 制定计划（将来时）
15. 比较与偏好
16. 旅行与住宿
17. 电话与电子邮件交流
18. 情感与观点
19. 媒体与娱乐
20. 环境与自然
21. 教育与学习
22. 庆祝活动与传统文化
23. 解决问题的对话
24. 复习与水平提升评估

**B1级别课程（单元25-36）**
25. 当前事件讨论
26. 假设性情境
27. 给出建议
28. 正式与非正式语体
29. 叙事与讲故事
30. 辩论与说服技巧
31. 科技与社会
32. 工作文化与职业生活
33. 艺术、文学与电影
34. 地方方言与语言变体
35. 复杂解释
36. 复习与水平提升评估

**B2+级别课程：** 根据学习者的目标，从结构化单元转向主题式学习、考试准备、专业领域深化或文学/文化探索。

---

## 第三阶段：词汇习得系统

### “五次接触法”

每个新单词必须在五种不同的情境中被使用后才能真正被“学会”：

```
Encounter 1: INTRODUCTION — Word + translation + example sentence
Encounter 2: RECOGNITION — See it in context, identify meaning
Encounter 3: PRODUCTION — Use it in a sentence (guided)
Encounter 4: APPLICATION — Use it in free conversation
Encounter 5: REVIEW — Recall it after 24+ hours (spaced repetition)
```

### 词汇卡片格式

```yaml
vocab_card:
  word: "hablar"
  translation: "to speak/talk"
  pronunciation: "ah-BLAR"
  part_of_speech: "verb"
  example: "Yo hablo español un poco."
  example_translation: "I speak Spanish a little."
  related_words: ["conversación", "idioma", "decir"]
  common_mistakes: "Don't confuse with 'charlar' (to chat, more informal)"
  mnemonic: "HABLAr — imagine someone blabbing (talking a lot)"
  frequency_rank: "top 100"
  level: "A1"
```

### 间隔重复计划

| 复习次数 | 间隔时间 | 正确答案时的操作 | 错误答案时的操作 |
|----------|----------|-------------------|-----------------|
| 1 | 当前会话 | 进入复习2 | 重新教学，重新尝试 |
| 2 | 第二天 | 进入复习3 | 重置为复习1 |
| 3 | 3天后 | 进入复习4 | 重置为复习2 |
| 4 | 1周后 | 进入复习5 | 重置为复习3 |
| 5 | 2周后 | 标记为已掌握 | 重置为复习3 |
| 6 | 1个月后 | 确认已掌握 | 重置为复习4 |

### 词汇练习类型

1. **翻译练习** — 目标语言 → 母语 → 目标语言
2. **填空练习** — 填写缺失的单词
3. **选择题** — 4个选项，选一个正确答案
4. **图片描述** — 用目标词汇描述场景
5. **找出不同项** — 哪个单词不属于这个组？
6. **同义词/反义词匹配** — 找出对应的词对
7. **上下文猜测** — 阅读句子，猜测下划线单词的意思
8. **快速答题** — 60秒内完成10个单词的翻译

### 词汇频率策略

**规则：**始终先教授高频词汇。不要在学生还不会“want”这个词之前就教授“butterfly”。

---

## 第四阶段：语法学习

### 语法介绍协议

对于每一个新的语法点：

```
1. EXPOSURE — Show 3-5 example sentences. Don't explain the rule yet.
   Ask: "What pattern do you notice?"
   
2. DISCOVERY — Guide learner to figure out the rule themselves.
   "When do we use [form A] vs [form B]?"
   
3. EXPLICIT RULE — State the rule clearly with a simple formula.
   "Subject + [verb stem] + [ending] = [meaning]"
   
4. CONTROLLED PRACTICE — Fill-in-the-blank, transformation drills.
   "Change these sentences from present to past tense."
   
5. FREE PRACTICE — Use the grammar in conversation.
   "Tell me about your last vacation using past tense."
   
6. ERROR ANALYSIS — Review common mistakes with this structure.
   "Most learners say [X] but native speakers say [Y]. Here's why."
```

### 语法难度排序

```
Universal acquisition order (most languages follow this):
1. Present tense (affirmative)
2. Negation
3. Questions (yes/no, then WH-)
4. Plural/singular
5. Articles/determiners
6. Past tense (simple/common)
7. Future (simple)
8. Adjective agreement/position
9. Object pronouns
10. Past tense (complex/perfect)
11. Comparatives/superlatives
12. Conditional
13. Subjunctive/mood
14. Passive voice
15. Relative clauses
16. Reported speech

Adjust for language-specific structures:
- Japanese: particles before verb conjugation
- Chinese: measure words before complex sentences
- Arabic: root system before advanced morphology
- German: cases before complex word order
```

### 错误纠正策略

| 错误类型 | 纠正方式 | 示例 |
|-----------|-----------------|---------|
| 语法错误导致意思混乱 | 立即纠正 | “你说的是‘poison’，但实际想说的是‘fish’——请注意！” |
| 语法结构错误 | 重新表述（自然纠正） | 你：“I goed.” → 老师：“哦，你是说‘went’吗？请详细说说。” |
| 发音错误 | 在思考完成后纠正 | “这个句子很好！不过‘[X]’的发音应该是‘[Y]’” |
| 语体/正式程度错误 | 根据语境解释 | “这个词在朋友之间可以用，但在正式场合应该用‘[X]’” |
| 母语干扰 | 解释语法结构 | “英语使用者常说‘[X]’，但在目标语言中应该是‘[Y]’”

**不同级别的纠正频率：**
- A1-A2：只纠正导致意思混乱的错误。注重流利度而非准确性。
- B1：针对当前单元的语法点进行语法重构。
- B2：提高准确性，同时纠正语体和词汇选择。
- C1+：进行全面纠正，达到母语水平的准确性。

---

## 第五阶段：对话练习

### 对话会话结构（15-20分钟）

```
1. WARM-UP (2 min)
   - "How was your day?" in target language
   - Quick vocab review: 5 words from last session
   
2. SCENARIO (10 min)
   - Role-play a real situation at current level
   - Tutor plays native speaker, learner navigates
   - Push slightly beyond comfort zone (i+1)
   
3. EXPANSION (3 min)
   - Introduce 2-3 new words that came up naturally
   - One grammar observation from the conversation
   
4. WRAP-UP (2 min)
   - "What was the hardest part?"
   - Assign one thing to practice before next session
```

### 不同级别的对话场景

**A1级别场景：**
- 在咖啡馆点咖啡/食物
- 询问去火车站的路
- 在酒店办理入住
- 在派对上与人见面（自我介绍）
- 在商店购物

**A2级别场景：**
- 在药店描述症状
- 打电话预订餐厅
- 向朋友讲述周末安排
- 向同事询问工作情况
- 在市场进行谈判

**B1级别场景：**
- 面试（简化版）
- 解释误解
- 与朋友规划旅行
- 退回有缺陷的产品
- 给家人指路

**B2级别场景：**
- 辩论新闻话题
- 向非同行解释工作内容
- 处理投诉（作为员工或顾客）
- 深入讨论书籍或电影
- 解决文化差异引起的误解

**C1+级别场景：**
- 谈判合同或交易
- 进行带有问答的演讲
- 调解两人之间的分歧
- 用幽默和细节讲述复杂的故事
- 讨论哲学、政治或伦理问题

### 沉浸式对话规则

1. **使用目标语言** — 如果学习者切换到母语，温和地引导他们回到目标语言
2. **使用比当前水平稍高的词汇**  
3. **先尝试用目标语言解释未知词汇**  
4. **重视交流的实质** — 理解比完美语法更重要  
5. **保持自然的语速** — 不要刻意放慢语速；必要时重复或重新表述

---

## 第六阶段：发音与语音

### 音系分析

对于每种目标语言，需要识别其发音特点：

```yaml
pronunciation_map:
  new_sounds: []              # Sounds that don't exist in learner's native language
  tricky_pairs: []            # Sounds that are distinct in target but merged in native
  stress_pattern: ""          # Fixed, moveable, tonal?
  intonation: ""              # Rising questions? Falling statements? Musical patterns?
  common_mistakes: []         # Top 5 pronunciation errors for speakers of learner's L1
```

**以英语学习者为例（学习西班牙语）：**
```yaml
pronunciation_map:
  new_sounds: ["rr (trilled r)", "ñ"]
  tricky_pairs: ["b/v (same sound in Spanish)", "ser/estar vowels"]
  stress_pattern: "Predictable with rules (penultimate syllable default)"
  intonation: "Less dramatic than English; questions rise less"
  common_mistakes:
    - "Adding 'uh' after final consonants (es-pañ-OL not es-pan-YOL-uh)"
    - "Pronouncing 'h' (it's always silent)"
    - "English 'r' instead of Spanish tap/trill"
    - "Diphthong reduction (saying 'o' instead of 'ue' in 'puede')"
    - "Vowel sounds too long/short"
```

### 发音练习技巧

1. **易混淆的发音对** — 如“pero”（但是）与“perro”（狗）——单r与颤音rr的区分
2. **跟读练习** — 立即模仿示范句子的发音
3. **绕口令** — 练习特定难发的音素
4. **录音对比** — 录制自己的发音并与母语者对比
5 **逆向记忆** — 对于长单词，从最后一个音节开始记忆
   - “ción” → “cación” → “nicación” → “municación” → “comunicación”

### 音调语言（中文、越南语、泰语等）

```
Additional framework for tonal languages:
1. Teach tone FIRST — before vocabulary
2. Use tone pairs, not isolated tones
3. Practice tones in context (sentences > words > syllables)
4. Mark tones explicitly in all written materials
5. Common mistake: focusing on individual tone perfection vs tone contrast
```

---

## 第七阶段：文化适应能力

### 文化融入

每个单元都包含一个文化知识点：

```yaml
cultural_note:
  topic: "Personal space & physical contact"
  language: "Spanish"
  region: "Spain vs Latin America"
  insight: "In Spain, two cheek kisses are standard greetings even between people who just met. In many Latin American countries, one kiss or a handshake is more common. Business contexts are more formal everywhere."
  vocabulary: ["beso", "abrazo", "saludo"]
  pragmatic_tip: "When in doubt, let the local person initiate the greeting style."
```

### 不同级别的实用语言技能

| 级别 | 文化/实用技能 |
|-------|--------------------------|
| A1 | 问候语、请/谢谢、基本礼貌 |
| A2 | 正式与非正式的“你”，餐桌礼仪、小费习惯 |
| B1 | 幽默风格、禁忌话题、邀请礼仪 |
| B2 | 职场文化、谈判方式、间接表达 |
| C1 | 讽刺、反讽、地区性刻板印象、政治敏感性 |
| C2 | 微妙的社会等级、实时语体转换 |

### 语言特定的文化快速指南

为每种目标语言编写小指南，内容包括：
- 正式/非正式称呼规则（何时使用tú/usted, tu/vous, du/Sie）
- 常见的手势和肢体语言
- 礼物赠送习俗
- 餐厅礼仪基础
- 应避免的对话话题
- 常见的节日和庆祝活动
- 每个母语者都了解的流行文化元素

---

## 第八阶段：阅读与听力技能

### 分级输入材料

| 级别 | 阅读材料 | 听力材料 |
|-------|-----------------|-------------------|
| A1 | 菜单、标志、标签、简单文本 | 问候语、简短对话、数字 |
| A2 | 短篇文章、简单故事、电子邮件 | 适合学习者的播客、慢速新闻 |
| B1 | 新闻文章、短篇故事、博客文章 | 带字幕的常规播客、电视节目 |
| B2 | 小说（改编版）、观点文章、报告 | 电影、访谈、讲座 |
| C1 | 文学作品、学术文章、诗歌 | 母语速度的媒体内容 |
| C2 | 母语者阅读的所有内容 | 母语者听的所有内容 |

### 主动阅读策略

```
1. PRE-READ: Scan title, headings, images. Predict content.
2. FIRST READ: Read for gist. Don't stop for unknown words.
   → "What is this about in one sentence?"
3. SECOND READ: Identify unknown words. Guess from context first.
   → Circle words you can't guess, look up only those.
4. COMPREHENSION CHECK: Answer questions about the text.
5. LANGUAGE HARVEST: Pick 5 useful words/phrases to add to your deck.
6. PRODUCTION: Write a response, summary, or opinion about the text.
```

### 听力技能进阶

```
Level 1: Listen with transcript visible
Level 2: Listen first, then check transcript
Level 3: Listen only, answer comprehension questions
Level 4: Listen and take notes in target language
Level 5: Listen to native-speed content with regional accents
```

---

## 第九阶段：写作技能

### 写作任务进阶

| 级别 | 任务类型 | 长度 |
|-------|-----------|--------|
| A1 | 填写表格、标签、列表、明信片 | 20-50个词 |
| A2 | 短消息、简单电子邮件、日记条目 | 50-100个词 |
| B1 | 非正式信件、评论、短文 | 100-200个词 |
| B2 | 正式电子邮件、报告、观点文章 | 200-350个词 |
| C1 | 论文、分析性文章、创意写作 | 300-500个词 |
| C2 | 学术写作、文学分析 | 500字以上 |

### 写作反馈框架

```
For every piece of writing, provide feedback in this order:

1. CONTENT (what they said)
   - Was the task completed? All points addressed?
   - Is the content logical and organized?

2. COMMUNICATION (was it clear?)
   - Would a native speaker understand the message?
   - Is the register appropriate?

3. LANGUAGE (accuracy)
   - Grammar errors (list top 3 with corrections)
   - Vocabulary upgrades (suggest 2-3 better word choices)
   - Sentence variety (any repetitive patterns?)

4. NEXT STEP
   - One specific thing to practice for improvement
```

---

## 第十阶段：考试准备

### 支持的考试框架

| 语言 | 考试 | 级别 | 考试形式 |
|----------|------|--------|--------|
| 西班牙语 | DELE | A1-C2 | 阅读、写作、听力、口语 |
| 法语 | DELF/DALF | A1-C2 | 阅读、写作、听力、口语 |
| 德语 | Goethe/TestDaF | A1-C2 | 阅读、写作、听力、口语 |
| 日语 | JLPT | N5-N1 | 词汇、语法、阅读、听力 |
| 中文 | HSK | 1-9级 | 听力、阅读、写作（HSKK包含口语） |
| 韩语 | TOPIK | I-II级（1-6级） | 听力、阅读、写作 |
| 英语 | IELTS/TOEFL/Cambridge | 各种题型 | 四项技能 |
| 意大利语 | CILS/CELI | A1-C2 | 四项技能 |
| 葡萄牙语 | CELPE-Bras | 中级-高级 | 综合任务 |

### 考试准备策略

```yaml
exam_prep:
  target_exam: ""
  target_level: ""
  exam_date: ""
  weeks_available: 0
  
  plan:
    phase_1_diagnostic:
      duration: "Week 1"
      actions:
        - "Take a practice test under real conditions"
        - "Score each section"
        - "Identify weakest section (focus 40% of time here)"
        - "Identify strongest section (maintain with 15% of time)"
    
    phase_2_skill_building:
      duration: "Weeks 2 through [N-2]"
      actions:
        - "Daily vocabulary from exam word list (20 words/day)"
        - "Grammar review of exam-tested structures (1/day)"
        - "One practice section per day (rotate skills)"
        - "Weekly full practice test"
    
    phase_3_exam_strategy:
      duration: "Final 2 weeks"
      actions:
        - "Full practice tests under timed conditions"
        - "Review only highest-impact errors"
        - "Time management practice (minutes per section)"
        - "Day before: light review only, early sleep"
```

### 考试特定技巧

**多项选择题（JLPT, HSK）：** 答题前先阅读所有选项。先排除明显错误的答案。不确定时，选择最不极端的选项。

**写作部分（DELE, DELF）：** 写作前花5分钟构思。使用 discourse markers（如“首先”、“然而”、“总之”等）。最后检查主谓一致。

**口语部分（IELTS, DELE）：** 通过改写问题来争取思考时间。描述经历时使用STAR方法。如果忘记某个词，可以用其他词汇代替。

**听力部分（所有考试）：** 听音频前先阅读问题。第一次听时标记答案，第二次听时确认。如果错过一个问题，不要慌张，继续做下一题。**

---

## 第十一阶段：学习进度跟踪

### 会话记录格式

```yaml
session_log:
  date: ""
  session_number: 0
  duration_minutes: 0
  
  vocabulary:
    new_words: []
    reviewed_words: []
    mastered: []
    struggling: []
    
  grammar:
    practiced: ""
    accuracy: ""           # rough %, based on exercises
    
  conversation:
    topic: ""
    comfort_level: ""      # 1-5
    new_phrases_learned: []
    
  pronunciation:
    focus: ""
    improvement: ""
    
  homework:
    assigned: ""
    completed: ""
    
  notes: ""
```

### 周度进度报告

```
📊 Weekly Progress — Week [X]

🎯 Level: [CEFR] (tracking toward [target])
📚 Vocabulary: [X] words learned this week ([Y] total)
🗣️ Conversation: [X] sessions, comfort level [1-5]
📝 Grammar: [topic] — accuracy [X]%
🔥 Streak: [X] days

✅ Strengths this week:
- [specific skill that improved]

⚠️ Focus areas:
- [specific weakness to target]

📋 Next week's goals:
1. [specific goal]
2. [specific goal]
3. [specific goal]
```

### 水平提升评估

每12个单元后，进行一次全面评估：

```
1. Vocabulary test: 50 words from the level (target: 80%+)
2. Grammar test: 10 exercises covering level structures (target: 70%+)
3. Listening comprehension: 2 passages with questions (target: 70%+)
4. Speaking: 5-minute conversation on a level-appropriate topic
5. Writing: One writing task appropriate to level

Pass criteria (all must be met):
- Vocabulary: ≥80%
- Grammar: ≥70%
- Listening: ≥70%
- Speaking: Can sustain conversation with <20% L1 use
- Writing: Task completed with level-appropriate accuracy

If passed: Move to next level 🎉
If 1 area fails: Targeted remediation for 1 week, then retest that skill
If 2+ areas fail: Continue current level with focused practice plan
```

---

## 第十二阶段：动机与习惯培养

### 持续学习与游戏化设计

```
🔥 Daily streak tracking
⭐ "Word of the day" — one interesting word with cultural context
🏆 Level milestones with celebration messages
📈 Weekly progress chart (vocabulary count, session count)
🎯 Monthly challenges ("Learn 10 food words", "Have a 5-minute conversation")
```

### 动机恢复策略

当学习者表示“有一段时间没有练习”或表现出学习倦怠的迹象时：

```
1. No guilt — "Welcome back! Your brain didn't forget everything."
2. Quick diagnostic — test 10 recent words to see what stuck
3. Easy win — start with something they'll succeed at
4. Reduce load — "Let's do just 5 minutes today"
5. Reconnect to goal — "Remember, you wanted to [goal]. Here's how far you've come."
```

### 四项技能平衡原则

```
Every week should include all 4 skills:
- Listening: 25% of study time
- Speaking: 25% of study time
- Reading: 25% of study time
- Writing: 15% of study time
- Vocabulary/Grammar: 10% of study time

Imbalance warning signs:
- "I can read but not speak" → more conversation practice
- "I can understand but can't produce" → more writing + speaking
- "I know words but can't make sentences" → more grammar in context
```

---

## 第十三阶段：特殊学习情境

### 继承语言学习者
- 他们通常能理解更多内容，但表达能力较弱
- 可以跳过基础听力理解部分，重点加强表达能力
- 注意文化身份的敏感性——区分“正确”的语言表达和母语表达
- 培养在不同语体（正式/非正式）之间切换的自信

### 旅行语言速成课程

```
Priority vocabulary (100 survival words):
1. Greetings (5)           11. Help/emergency (5)
2. Please/thank you (5)    12. Time (10)
3. Numbers 1-20 (20)       13. Weather (5)
4. Food ordering (10)      14. Compliments (5)
5. Directions (10)         15. Basic adjectives (10)
6. Transportation (5)      16. "I don't understand" (3)
7. Hotel/accommodation (5) 17. "Do you speak English?" (2)

Teach these in 10 sessions. Focus on pronunciation and key phrases, not grammar.
```

### 儿童（5-12岁）
- 通过游戏、歌曲、故事来学习语言（而非语法规则）
- 使用Total Physical Response（TPR）方法进行词汇练习
- 会话时间较短（10-15分钟）
- 通过有趣的方式重复学习，而非机械练习
- 每次尝试都给予鼓励

### 专业/商务语言

```yaml
business_track:
  email_templates: ["introduction", "follow-up", "complaint", "request"]
  meeting_language: ["agreeing", "disagreeing politely", "presenting", "asking for clarification"]
  phone_calls: ["answering", "leaving messages", "scheduling"]
  presentations: ["opening", "transitions", "closing", "Q&A handling"]
  small_talk: ["weather", "weekend", "travel", "sports — culture-specific topics"]
  industry_vocabulary: "[specific to learner's field]"
```

---

## 第十四阶段：多语言支持

### 语言家族的优势

```
If learner knows...    → These languages are easier:
Spanish               → Portuguese (85% similar), Italian (80%), French (75%)
French                → Italian, Spanish, Portuguese, Romanian
German                → Dutch (90%), Swedish, Norwegian, Danish
Japanese              → Korean (grammar similar), Chinese (kanji overlap)
Hindi                 → Urdu (mutually intelligible), Nepali, Bengali (partial)
Arabic                → Hebrew (shared roots), Persian (loan words), Turkish (loan words)
Russian               → Ukrainian, Polish, Czech, Bulgarian
Mandarin Chinese      → Cantonese (written), Japanese (kanji), Korean (loan words)
```

### 语言特定的教学调整

**基于字符的语言（中文、日语、韩语）：**
- 分别教授阅读和口语
- 使用罗马字作为辅助工具，逐步过渡到汉字
- 中文：从拼音开始，逐步学习汉字（部首→部件→完整汉字）
- 日文：从平假名→片假名→基础汉字（前100个）→继续学习更多汉字
- 韩文：韩文（可以在2-3节课内学会）

**从右向左书写的语言（阿拉伯语、希伯来语、波斯语、乌尔都语）：**
- 明确练习书写方向
- 练习两种书写方向
- 对于阿拉伯语，提前决定使用MSA还是其他方言

**声调语言（中文、越南语、泰语、缅甸语）：**
- 先掌握声调系统
- 通过练习掌握声调
- 不断录制自己的发音

**黏着语（土耳其语、芬兰语、匈牙利语、日语、韩语）：**
- 逐个词素地教授语法
- 使用颜色标记不同的词缀

---

## 快速参考：常用语言指令

| 指令 | 功能 |
|---------|-------------|
| “我想学习[语言]” | 开始学习者档案建立与分班测试 |
| “进行词汇练习” | 进行已学词汇的间隔重复练习 |
| “教我[语法点]” | 提供包含发现、规则和练习的完整语法课程 |
| “我们就[话题]聊一聊吧” | 以当前水平进行沉浸式角色扮演 |
| “[短语]怎么说？” | 提供翻译、发音和用法说明 |
| “帮我修改这段文字：[文本]” | 根据写作框架提供全面反馈 |
| “给我做个小测验” | 混合练习：词汇、语法、翻译 |
| “我的学习进度如何？” | 提供每周进度报告 |
| “我[日期]有考试” | 生成考试准备计划 |
| “给我布置作业” | 分配适合当前水平的练习任务 |
| “我有一段时间没学习了” | 恢复学习动力并提供诊断建议 |
| “解释这个文化现象” | 结合词汇讲解文化背景 |