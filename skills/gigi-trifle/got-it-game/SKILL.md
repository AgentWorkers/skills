---
name: got-it
description: 这是一个谢林点（Schelling point）协调游戏，玩家通过这个游戏达成共识并使用一个共同的词汇。该游戏适用于以下场景：当有人发起“明白了”（got it）的游戏时；在 Discord 或 Telegram 频道中管理游戏的进行状态时；以及在游戏过程中回应“明白了”（got it）的消息时。
---

# Got It 游戏

这是一个基于谢林点（Schelling Point）的协调游戏，玩家通过迭代猜测来尝试达成共识，选择同一个单词。

## 游戏规则

1. **开始**：当两名玩家在频道中同时说出“got it”时，游戏开始。
2. **揭示单词**：两名玩家各自揭示一个单词（可以是任意单词）。
3. **获胜条件**：如果两个单词相同，则所有玩家获胜，游戏结束。
4. **进入下一轮**：如果单词不同，则开始新的一轮，需要等待另外两名玩家再次发出“got it”的消息。
5. **收敛策略**：每一轮中，玩家应选择一个介于前两个单词之间的单词，目的是找到一个能让双方达成共识的“谢林点”。

## 状态管理

游戏状态存储在 `~/.openclaw/workspace/got-it-state.json` 文件中。详细的状态结构请参考 `references/state-schema.md`。

- 在每次交互开始时，**加载游戏状态** 以检查游戏是否正在进行中。
- 在状态发生变化时（例如有新的“got it”消息、单词被揭示或轮次切换时），**保存游戏状态**。

## 游戏流程

### 1. 游戏启动

当有人在频道中说出“got it”时：
- 加载或创建游戏状态文件。
- 检查这是否是该轮次的第一次“got it”操作。
- 如果是第一次：记录当前玩家，并等待另一名玩家。
- 如果是第二次：进入单词揭示状态，并提示两名玩家开始揭示单词。

**当第一名玩家说出“got it”时的响应：**
```
🎯 Got one! Waiting for one more to "got it"...
```

**当第二名玩家说出“got it”时的响应：**
```
🎯 Two players ready! @player1 and @player2, reveal your words!

Round {N} {context_if_not_first_round}
```

**如果不是第一轮，请提供上下文信息：**
```
Previous words: "{word1}" vs "{word2}"
Find the Schelling point between them!
```

### 2. 单词揭示

当说出“got it”的玩家发布一个单词时：
- 将该单词记录到游戏状态中。
- 等待第二名玩家发布单词。
- 当两个单词都被揭示后，检查它们是否相同。

**如果单词相同：**
```
🎊 CONVERGENCE! Both said "{word}"!

Everyone wins! Game complete in {N} rounds.
🎯 {summary_of_journey}
```

**如果单词不同：**
```
Round {N}: "{word1}" vs "{word2}"

🔄 New round! Who's got it?
```

### 3. 代理参与（Agent Participation）

- **在说出“got it”前的延迟**：在检测到“等待其他玩家回应”的状态后，等待 5 秒再发言（给人类玩家优先权）。
- **在揭示单词前的延迟**：当自己是揭示单词的玩家时，**必须等待另一名玩家先揭示单词**，然后再进行揭示。切勿在提示后立即揭示。
- **揭示策略**：
  - **第一轮**：选择具有高度辨识度、普遍性的概念（如“water”（水）、“love”（爱）、“home”（家）。
  - **后续轮次**：选择前两个单词之间的最明显的概念中间点。
  - 倾向于选择：常见名词、具体对象、基本情感、普遍体验。
  - **避免使用**：晦涩的术语、专有名词或技术性词汇。

### 4. 状态清理

在以下情况下删除游戏状态文件：
- 游戏结束（两个单词相同）。
- 自上次活动后超过 24 小时（游戏被放弃）。

## 谢林点策略

**第一轮（没有之前的单词）：**
选择具有高度辨识度的普遍性概念：
- 基本元素：water（水）、fire（火）、earth（土）、air（空气）
- 普遍情感：love（爱）、fear（恐惧）、joy（快乐）
- 基本需求：food（食物）、home（家）、family（家庭）
- 基本概念：time（时间）、life（生命）、death（死亡）

**后续轮次（单词开始趋同时）：**
根据之前的单词 W1 和 W2，选择最明显的概念中间点：
- 例如：“hot”（热）和 “cold”（冷） → 选择 “warm”（温暖）或 “temperature”（温度）
- “cat”（猫）和 “dog”（狗） → 选择 “pet”（宠物）或 “animal”（动物）
- “night”（夜晚）和 “day”（白天） → 选择 “time”（时间）或 “dusk”（黄昏）
- “love”（爱）和 “hate”（恨） → 选择 “emotion”（情感）或 “passion”（激情）

**选择策略：**
- 选择更高层次的类别（如 cat/dog → animal（猫/狗 → 动物）。
- 选择两个单词之间的中间点（如 hot/cold → warm（热/冷 → 温暖）。
- 选择双方都认可的常见关联词（如 fork/knife → table/meal（叉子/刀 → 桌子/餐食）。
- 避免使用只有你自己理解的晦涩关联词。
- 避免使用双关语或抽象的哲学概念。

## 消息检测

通过以下方式检测“got it”消息：
- 消息内容与 “got it” 完全匹配（不区分大小写）。
- 消息中包含 “got it” 以及标点符号（如 “got it!”, “got it?”）。
- 其他变体形式：”Got it.”, “GOT IT”。

**注意排除：**
- 与游戏无关的对话内容（如 “I got it working”）。
- 语境不同的表达（如 “You got it right”）。

**使用精确的短语匹配来避免误判。**

## 游戏示例**

**第一轮：**
```
Alice: got it
Bot: 🎯 Got one! Waiting for one more...
Bob: got it
Bot: 🎯 Two players ready! @Alice and @Bob, reveal your words! Round 1
Alice: tree
Bob: water
Bot: Round 1: "tree" vs "water"
     🔄 New round! Who's got it?
```

**第二轮：**
```
Carol: got it
Alice: got it  
Bot: 🎯 Two players ready! @Carol and @Alice, reveal your words!
     Previous words: "tree" vs "water"
     Find the Schelling point between them!
Carol: nature
Alice: plant
Bot: Round 2: "nature" vs "plant"
     🔄 New round! Who's got it?
```

**第三轮：**
```
Bob: got it
Carol: got it
Bot: 🎯 Two players ready! @Bob and @Carol, reveal your words!
     Previous words: "nature" vs "plant"  
     Find the Schelling point between them!
Bob: nature
Carol: nature
Bot: 🎊 CONVERGENCE! Both said "nature"!
     
     Everyone wins! Game complete in 3 rounds.
     🎯 tree vs water → nature vs plant → NATURE!
```

## 错误处理**

- **非揭示状态的玩家突然发言**：忽略该消息（可能是正常对话）。
- **同一玩家在同一轮次中多次说出“got it”**：忽略重复消息，不重复计数。
- **未说出“got it”的玩家尝试揭示单词**：礼貌地提示该轮次只能由两名玩家进行揭示。
- **频道混淆（游戏在多个频道中进行）**：游戏状态中包含 `channelId`，仅对活跃频道中的游戏做出响应。