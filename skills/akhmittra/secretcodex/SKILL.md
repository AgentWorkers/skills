---
name: secretcodex
description: 生成富有创意的代码名称，并使用经典及复杂的加密算法对秘密信息进行编码和解码。将复古的解密工具（如解密环）与现代加密技术相结合，支持凯撒密码、维吉尼亚密码、波利比乌斯密码、栅栏密码等多种加密方法。同时提供密钥，以实现可信方之间的安全信息共享。
metadata:
  openclaw:
    emoji: "🔐"
    version: "1.0.0"
    author: "AM"
    tags: ["cryptography", "cipher", "encryption", "decoding", "secret-messages", "code-names", "security"]
    requires:
      bins: []
      env: []
      config: []
---

# SecretCodex

## 描述

SecretCodex 将你童年时麦片盒上的解码环带来的神秘感带回了现实，但采用了现代密码学的复杂技术。它可以为操作和团队成员生成富有创意的代号，使用多种加密方法对秘密信息进行编码，并从可信赖的接收者那里解码信息——所有这些操作都由你控制，并手动与目标接收者共享密钥。

**非常适合：**
- 为项目、操作或团队成员创建代号
- 在朋友、家人或团队之间发送秘密信息
- 通过实践学习密码学
- 为游戏、寻宝活动或谜题增添神秘元素
- 有趣的挑战和脑筋急转弯
- 仅你能（以及持有密钥的人）阅读的私人笔记

## 核心理念

**“通过隐蔽性实现安全是脆弱的。通过强大的加密算法加上密钥管理才能实现真正的安全。”**

SecretCodex 会教你：
- **简单的加密算法**（有趣、教育性强、快速上手）
- **复杂的加密算法**（更强大、多层次、更安全）
- **混合加密方法**（结合多种技术）
- **密钥管理**（密码学的真正秘诀）

## 1. 代号生成器

在编码信息之前，你需要一个好的代号！SecretCodex 会为操作、项目或个人生成富有创意且易于记忆的代号。

### 代号类型

#### 操作代号（任务/项目代号）
**格式**：[形容词] + [名词]

**示例：**
- 操作“Silent Thunder”（寂静雷霆）
- 操作“Crimson Falcon”（绯红猎鹰）
- 操作“Midnight Protocol”（午夜协议）
- 操作“Steel Horizon”（钢铁地平线）
- 操作“Quantum Shield”（量子护盾）

**生成策略：**
- 选择一种风格（隐蔽的、强大的、技术性的、自然的、神话的）
- 将富有表现力的形容词与强有力的名词搭配
- 避免与实际项目有明显的关联

#### 个人代号（特工/团队成员代号）
**格式**：单个单词或[头衔] + [元素]

**示例：**
- Phoenix（凤凰，象征重生）
- Cipher（密码，象征保密）
- Raven（乌鸦，象征智慧）
- Atlas（阿特拉斯，象征力量）
- Echo（回声，象征沟通）
- Agent Frost（冰霜特工，象征冷静）
- The Architect（建筑师，象征策略性）

**生成策略：**
- 考虑个人的角色或特点
- 使用动物、元素、概念或头衔
- 使代号易于记忆且发音清晰

#### 地点代号
**格式**：听起来像地理位置但实际上是虚构的

**示例：**
- Raven's Point（乌鸦之点，会议地点）
- Glacier Station（冰川站，服务器位置）
- Meridian Hub（子午线中心）

### 代号生成过程

**用户提供：**
- 选择操作类型（操作、个人或地点）
- 选择风格（严肃的、幽默的、技术性的、神秘的）
- 可选的主题（自然、技术、神话、颜色）

**SecretCodex 生成：**
- 5-10个有意义的代号选项
- 保证发音清晰（便于无线电通信）
- 如果首选代号被泄露，会提供备用选项

**示例：**

*用户：“为我们的Q1产品发布项目生成一个代号。风格：既刺激又专业。”*

*SecretCodex：*
```
CODE NAME OPTIONS:

1. Operation Silver Dawn
   - Silver: Premium, valuable, reflective
   - Dawn: New beginning, fresh start
   - Phonetic: SILVER DON
   - Use case: "Silver Dawn is go for launch"

2. Project Velocity Edge
   - Velocity: Speed, momentum, progress
   - Edge: Cutting-edge, advantage, boundary
   - Phonetic: vuh-LOSS-ih-tee EDJ
   
3. Initiative Catalyst Prime
   - Catalyst: Trigger change, accelerate
   - Prime: First-class, optimal, ready
   
4. Operation Horizon Shift
   - Horizon: Future, vision, expansion
   - Shift: Change, transformation

5. Project Apex Launch
   - Apex: Peak, highest point, summit
   - Launch: Beginning, deployment

Recommendation: "Operation Silver Dawn" - 
Professional, aspirational, easy to remember and say.
```

## 2. 经典加密算法（解码环时代）

### 凯撒密码（字母位移）

**工作原理：**
将每个字母在字母表中向前或向后移动固定数量的位置。

**密钥：** 移动量（1-25）

**示例：**
```
Plaintext: MEET ME AT NOON
Key: Shift 3
Ciphertext: PHHW PH DW QRRQ

M → P (shift 3)
E → H (shift 3)
E → H (shift 3)
T → W (shift 3)
```

**解码：**
将字母向后移动相同的位置。

**安全性：** ⭐☆☆☆☆（非常弱——只有25种可能的密钥）
**最适合：** 儿童、快速消息、怀旧用途

---

### ROT13（凯撒密码的变体，位移13）

**工作原理：**
凯撒密码的特例，位移量为13。加密和解码相同。

**密钥：** 不需要（始终位移13）

**示例：**
```
Plaintext: SECRET MESSAGE
Ciphertext: FRPERG ZRFFNTR

S → F (shift 13)
E → R (shift 13)
...
```

**安全性：** ⭐☆☆☆☆（非常弱——密钥固定）

**最适合：** 快速混淆信息、论坛剧透、简单隐藏

---

### Atbash密码（反向字母表）

**工作原理：**
将A替换为Z，B替换为Y，C替换为X，依此类推（反向字母表）

**密钥：** 不需要（固定模式）

**示例：**
```
Plaintext: HIDDEN
Ciphertext: SRWWVM

H → S (A=Z, B=Y, ... H=S)
I → R
D → W
D → W
E → V
N → M
```

**安全性：** ⭐☆☆☆☆（非常弱——没有密钥变化）

**最适合：** 快速反转信息、简单编码

---

### Pigpen密码（符号替换）

**工作原理：**
根据网格将字母替换为特定的符号。

**密钥：** 网格布局（标准或自定义）

**网格示例：**
```
# Grid 1:        # Grid 2:
    A|B|C           J|K|L
   -+-+-           -+-+-
    D|E|F           M|N|O
   -+-+-           -+-+-
    G|H|I           P|Q|R

# X-Grid 1:     # X-Grid 2:
   S   T            W   X
     X              X
   U   V            Y   Z
```

**示例：**
```
Plaintext: HELLO
Symbols: [H][E][L][L][O]

H = bottom-left of first grid
E = middle of first grid
L = top-right of second grid
L = top-right of second grid
O = middle of second grid
```

**安全性：** ⭐⭐☆☆☆（较弱——依赖于模式识别）

**最适合：** 视觉编码、儿童使用、寻宝活动

---

## 3. 中级加密算法（增强安全性）

### Polybius方格（网格坐标）

**工作原理：**
字母按照5×5的网格排列（I/J合并使用）。每个字母对应一行和一列。

**密钥：** 网格布局（可以随机打乱）

**标准网格：**
```
  1 2 3 4 5
1 A B C D E
2 F G H I/J K
3 L M N O P
4 Q R S T U
5 V W X Y Z
```

**示例：**
```
Plaintext: ATTACK
Ciphertext: 11 44 44 11 13 25

A = row 1, col 1 = 11
T = row 4, col 4 = 44
T = row 4, col 4 = 44
A = row 1, col 1 = 11
C = row 1, col 3 = 13
K = row 2, col 5 = 25
```

**安全性：** ⭐⭐☆☆☆（单独使用较弱，结合其他方法时更强）

**最适合：** 数字编码、与其他方法结合使用

---

### Vigenère密码（基于关键词的位移）

**工作原理：**
类似于凯撒密码，但每个字母的位移量根据关键词而变化。

**密钥：** 关键词或短语（关键词越长，安全性越高）

**示例：**
```
Plaintext: ATTACK AT DAWN
Key:       SECRETSECRETSE
Ciphertext: SXVRGD SX HSAS

A + S = S (0+18 mod 26)
T + E = X (19+4 mod 26)
T + C = V (19+2 mod 26)
A + R = R (0+17 mod 26)
C + E = G (2+4 mod 26)
K + T = D (10+19 mod 26)
...
```

**Vigenère方格示例：**
```
    A B C D E F ...
A | A B C D E F ...
B | B C D E F G ...
C | C D E F G H ...
... (26×26 grid)
```

**解码：**
使用关键词进行反向位移。

**安全性：** ⭐⭐⭐☆☆（中等强度——关键词越长，安全性越高）

**最适合：** 基于关键词的保密通信、共享密钥**

---

### Rail Fence密码（换位密码）

**工作原理：**
将消息以之字形写在多条横线上，然后按行读取。

**密钥：** 横线的数量（2-10）

**3条横线的示例：**
```
Plaintext: THISISASECRET

Writing pattern (3 rails):
T . . . S . . . E . . . T     Rail 1: T S E T
. H . S . I . A . S . C . E   Rail 2: H S I A S C E
. . I . . . S . . . R . .     Rail 3: I S R

Ciphertext: TSET HSIASECE ISR (read row by row)
Compact: TSETHSIASCEEISR
```

**解码：**
知道横线的数量后，按之字形反向读取。

**安全性：** ⭐⭐☆☆☆（较弱——依赖于模式）

**最适合：** 视觉重组、与其他加密方法结合使用**

## 4. 高级加密算法（现代高级技术）

### Playfair密码（双字母替换）

**工作原理：**
使用5×5的密钥网格对字母对进行加密。比单字母替换更安全。

**密钥：** 关键词用于创建网格

**网格创建步骤：**
1. 写下关键词（去除重复字符）
2. 用未使用的字母填充剩余位置
3. 将I和J合并

**关键词“MONARCHY”的示例：**
```
M O N A R
C H Y B D
E F G I/J K
L P Q S T
U V W X Z
```

**加密规则：**
- 如果两个字母在同一行：向右移动
- 如果两个字母在同一列：向下移动
- 如果形成一个矩形：交换两个字母的位置

**示例：**
```
Plaintext: HE LL OW OR LD (pairs)
Key: MONARCHY

HE: H=row2,col2 E=row3,col1 → Rectangle → EB
LL: L=row4,col1 L=row4,col1 → Insert X: LX → LXLX
OW: O=row1,col2 W=row5,col3 → Rectangle → AZ
OR: O=row1,col2 R=row1,col5 → Same row → NA
LD: L=row4,col1 D=row2,col5 → Rectangle → UD

Ciphertext: EB LZ OL AZ NA UD
```

**安全性：** ⭐⭐⭐⭐☆（较强——抗频率分析）

**最适合：** 重要信息的加密、抵抗解密攻击**

---

### Columnar Transposition密码（基于关键词的列排序）

**工作原理：**
将消息按行书写，然后按关键词的字母顺序读取列。

**密钥：** 关键词决定了列的顺序

**示例：**
```
Plaintext: ATTACK AT DAWN
Key: ZEBRA (alphabetical: ABERZ = 52143)

Write in 5 columns under keyword:
Z E B R A
---------
A T T A C
K A T D A
W N X X X (padding)

Read columns in alphabetical order (A E B R Z):
Column A (5): C A X
Column E (2): T A N
Column B (3): T T X
Column R (4): A D X
Column Z (1): A K W

Ciphertext: CAXTANTТXADXAKW
Compact: CAXTANTTXADXAKW
```

**安全性：** ⭐⭐⭐☆☆（中等强度——顺序至关重要）

**最适合：** 混淆消息结构**

---

### 一次性密码本（理论上无法破解）

**工作原理：**
每条消息使用一个真正随机的密钥进行加密，该密钥仅使用一次，长度与消息相同。

**密钥：** 随机字符串，长度与明文相同（必须真正随机，且只能使用一次）

**示例：**
```
Plaintext: HELLO
Key:       XMCKL (truly random, never reused)

H + X = E (7+23 mod 26)
E + M = Q (4+12 mod 26)
L + C = N (11+2 mod 26)
L + K = V (11+10 mod 26)
O + L = Z (14+11 mod 26)

Ciphertext: EQNVZ
```

**重要提示：** 密钥必须：**
- 真正随机（不是伪随机）
- 长度与消息相同
- 仅使用一次
- 必须提前安全共享

**安全性：** ⭐⭐⭐⭐⭐（如果正确使用，安全性极高）

**最适合：** 最高级别的安全需求（前提是能够确保密钥的随机性和一次性使用）

## 5. 混合加密算法（多层次保护）

### 双重加密（两步过程）

**方法：** 依次应用两种不同的加密算法

**示例：Vigenère + Rail Fence**
```
Step 1: Vigenère with keyword "FORTRESS"
Plaintext: MEET ME AT THE BRIDGE
Key: FORTRESSFORTRESSFO
Result: RXJG ZR UG GUR VKWQTR

Step 2: Rail Fence with 3 rails
Input: RXJGZRUGGURVIIWQTR
Output: RJZGRTVR XGUGUKWT RI (rail-encoded)

Final Ciphertext: RJZGRTVХGUGUKWTГRI
```

**解码：** 先按Rail Fence解码，再按Vigenère解码

**安全性：** ⭐⭐⭐⭐☆（比单独使用任何一种算法都强）

---

### Polybius + Vigenère

**方法：** 先将文本转换为数字，再使用关键词进行位移

**示例：**
```
Step 1: Polybius Square
Plaintext: HELLO
Numbers: 23 15 31 31 34

Step 2: Vigenère on Numbers
Key: SECRET = 18 14 12 17 14 19
Add key to numbers (mod 100):
23+18=41, 15+14=29, 31+12=43, 31+17=48, 34+14=48

Final Ciphertext: 41 29 43 48 48
```

**安全性：** ⭐⭐⭐⭐☆（数字层和字母层的结合）

---

## 6. 密钥生成与管理

**密码学中最重要的部分：密钥管理**

### 密钥类型

**1. 位移/旋转密钥（简单）**
- 数字（例如凯撒密码的1-25）
- 移动方向（向前/向后）
- 示例：“ROT13”，“Shift +7”

**2. 关键词密钥（中级）**
- 单词或短语
- 越长越安全
- 易于记忆但不易被猜到
- 示例：“FORTRESS”，“PURPLE ELEPHANT”

**3. 随机密钥（高级）**
- 真正随机的字符
- 一次性使用
- 必须安全共享
- 示例：“XQPVHGKLMNZRT”

**4. 图形密钥（视觉型）**
- 基于网格的密钥（例如Polybius、Playfair）
- 符号映射（例如Pigpen密码的变体）
- 示例：“Grid arranged by keyword MONARCH”

### 密钥共享方法（手动）

**如何安全共享密钥：**

1. **面对面交换**（最安全）
   - 低声告诉对方密钥
   - 写在纸上，观察对方记住后销毁纸张
   - 使用预先约定的代码短语

2. **分开的通信渠道**（较好）
   - 通过电子邮件发送加密消息
   - 通过短信发送密钥（使用不同的平台）
   - 绝不要通过同一渠道发送密钥和消息

3. **预先约定的密钥**（适用于长期使用）
   - 在分离前商定关键词/模式
   - 使用共同的秘密（如内部笑话、日期、地点）
   - 定期更换密钥

4. **物理密钥交换**（创意方法）
   - 将密钥隐藏在信件中并通过邮件发送
   - 使用简单的加密算法对密钥进行编码
   - 使用约定的地点传递密钥卡

**密钥安全规则：**
- ❌ 绝不要通过同一渠道发送密钥和加密消息
- ❌ 绝不要重复使用一次性密码本
- ✅ 定期更换密钥
- ✅ 使用后销毁旧密钥
- ✅ 尽可能记住密钥

## 7. 实用示例**

### 示例1：秘密会议协调

**场景：** 需要告诉朋友 meeting 的时间和地点，但你们在公共群聊中交流。

**解决方案：**
```
Code Names:
- You: "Phoenix"
- Friend: "Atlas"
- Meeting spot: "Raven's Point" (actually the north library entrance)
- Time: Use Vigenère

Message Setup:
Plaintext: MEET AT RAVENS POINT AT THREE PM
Cipher: Vigenère
Key: FORTRESS (shared in-person last week)

Encoding:
M+F=R, E+O=S, E+R=V, T+T=M, ...

Encrypted: RXJG UG KHEVLA UTVRM UG GLVJJ TZ

Sent Message:
"Phoenix to Atlas: RXJG UG KHEVLA UTVRM UG GLVJJ TZ"

Friend decodes using FORTRESS key → Meets you at Raven's Point (north library) at 3pm
```

---

### 示例2：寻宝活动线索

**场景：** 为寻宝活动创建秘密线索。

**解决方案：**
```
Clue 1 (Simple - Caesar Shift 5):
Plaintext: LOOK UNDER THE OAK TREE
Ciphertext: QTTP ZSIJW YMJ TPF YWJJ

Clue 2 (Medium - Rail Fence 4 rails):
Plaintext: THE TREASURE IS IN THE SHED
Ciphertext: TEUEIHHE RSRSNSDE TISHETDR

Clue 3 (Hard - Playfair with keyword HUNTER):
Plaintext: FINAL PRIZE BEHIND DOOR TWO
(Encrypted with Playfair)
Ciphertext: GHPBM QXFBH CHAKMB ENNX VVS

Each clue progressively harder, keys provided when previous clue found.
```

### 示例3：私人日记记录

**场景：** 希望即使有人看到日记内容也能保持私密。

**解决方案：**
```
Method: Double Vigenère (two different keywords)

First Pass:
Plaintext: TODAY I LEARNED SOMETHING IMPORTANT
Key 1: JOURNAL
Ciphertext 1: CLHDB R VWTCPWH DLZSEVTUP PPWCRVQEV

Second Pass:
Plaintext: CLHDB R VWTCPWH DLZSEVTUP PPWCRVQEV
Key 2: PRIVATE
Ciphertext 2: RVPCQ G KXIGXFT SGDTHSOTZ EIAXQVYOX

Final encrypted entry goes in journal.
Only you know both keys to decrypt.
```

### 示例4：团队沟通

**场景：** 远程团队需要共享敏感项目信息。

**解决方案：**
```
Code Name System:
- Project: "Operation Silver Dawn"
- Team members: Phoenix, Atlas, Cipher, Raven
- Milestones: Alpha, Bravo, Charlie, Delta

Sensitive Message Encoding:
Method: Columnar Transposition + Substitution
Key: Team keyword "SILVERDOWN" (agreed in kickoff meeting)

Message:
"Phoenix reports Charlie milestone complete on schedule"

Encoded:
"PXHNIR ETORCP HLEIM TSOEE NLTCP SEODH EUELN"

Sent in Slack:
"SILVER: PXHNIR ETORCP HLEIM TSOEE NLTCP SEODH EUELN"

Team members decode using shared key.
```

## 8. 密码学挑战**

### 初学者挑战

**挑战1：凯撒密码**
```
Encrypted: WKLV LV D VHFUHW PHVVDJH
Hint: Shift is 3
Decrypt it!

Answer: THIS IS A SECRET MESSAGE
```

**挑战2：Atbash密码**
```
Encrypted: HXVVGH HLFGS
What does it say?

Answer: SUMMER NIGHT (H→S, X→C, etc.)
```

### 中级挑战**

**挑战3：Vigenère密码**
```
Encrypted: YXPKI HS ASWZE
Keyword: LOCK
Decrypt it!

Answer: OPENS AT SEVEN
```

**挑战4：Rail Fence密码（3条横线）**
```
Encrypted: TETYESCESGA HEEARMSE
Decrypt it!

Answer: THE SECRET MESSAGE (written in zigzag)
```

### 高级挑战**

**挑战5：Playfair密码**
```
Encrypted: FD EO OA TP ED ND RP
Keyword: EXAMPLE
Decrypt it! (Remember digraph rules)

Answer: HIDDEN CHAMBER (requires Playfair decoding)
```

---

## 9. 密码选择指南

### 何时使用哪种加密算法

**快速且有趣（几分钟内完成）：**
- 凯撒密码/ROT13：用于随意消息、快速隐藏
- Atbash密码：简单反转
- Pigpen密码：视觉效果好，适合寻宝活动

**中等安全性（需要数小时才能破解）：**
- Vigenère密码：基于关键词的保密
- Polybius密码：数字编码
- Rail Fence密码：模式混淆

**高安全性（需要数天或数周才能破解）：**
- Playfair密码：双字母替换
- Columnar Transposition密码：基于关键词的排序
- 双重加密：多层次保护

**最高安全性（理论上无法破解）：**
- 一次性密码本：真正随机的密钥 + 一次性使用**

**密码算法对比表**

| 密码 | 安全性 | 加密速度 | 密钥类型 | 最适合的用途 |
|--------|----------|-------|----------|----------|
| 凯撒密码 | ⭐ | 快速 | 数字密钥 | 儿童、快速消息 |
| Atbash密码 | ⭐ | 快速 | 无密钥 | 简单反转 |
| Pigpen密码 | ⭐⭐ | 中等 | 基于模式的加密 | 视觉编码 |
| Vigenère密码 | ⭐⭐⭐ | 中等 | 基于关键词的保密 | 共享信息 |
| Polybius密码 | ⭐⭐ | 中等 | 基于网格的加密 | 数字编码 |
| Rail Fence密码 | ⭐⭐ | 中等 | 基于模式的加密 | 混合使用 |
| Playfair密码 | ⭐⭐⭐⭐ | 较慢 | 基于关键词的加密 | 强大的加密效果 |
| 一次性密码本 | ⭐⭐⭐⭐⭐ | 中等 | 随机密钥 | 最高级别的安全性 |
| 混合加密算法 | ⭐⭐⭐⭐ | 较慢 | 多层保护 |

## 10. 重要安全提示

### SecretCodex 的特点：**

✅ 一种教育性的密码学工具
✅ 一种学习加密技术的有趣方式
✅ 适用于日常的秘密信息交流
✅ 非常适合游戏、谜题和寻宝活动
✅ 是了解密钥管理概念的绝佳工具

### SecretCodex 不适合的情况：**

❌ 不能替代现代加密算法（如AES、RSA等）
❌ 不适合处理高度敏感的数据（请使用专业的加密软件）
❌ 不能有效抵御有针对性的攻击
❌ 不能替代安全的通信平台

### 何时使用适当的加密算法：

- 金融信息
- 个人身份信息
- 医疗记录
- 法律文件
- 机密商业信息
- 任何需要高度保密的内容

**对于这些情况，请使用AES-256、RSA或加密消息应用程序（如Signal、WhatsApp等）。**

SecretCodex 适用于：
- 学习密码学
- 发送有趣的秘密信息
- 保护日常隐私
- 教育用途
- 带来怀旧感和乐趣

## 何时使用 SecretCodex：

当你需要：
- 为操作、团队或地点生成创意代号
- 向朋友或家人发送秘密信息
- 解码别人发送给你的信息（如果你拥有正确的密钥）
- 了解不同加密算法的工作原理
- 创建谜题或寻宝活动
- 为游戏或角色扮演增添神秘元素
- 练习密码学思维
- 以现代技术享受解码的乐趣

---

**记住：加密的安全性不仅取决于算法，还取决于密钥。保护好你的密钥，谨慎分享，并定期更换它们！**

🔐 “在密码学中，我们信任……但只有通过良好的密钥管理才能确保安全！” 🔐