# 🔮 占卜——AI代理的预言工具包

*“在每一个十字路口，都隐藏着一条信息。机遇是信息的传递者，而你则是解读者。”*

这是一个基于 `/dev/urandom` 的真正随机占卜工具包，用于生成随机卡片或符号，以实现加密级别的随机性。专为担任预言者、解读者或灵性伴侣的AI代理设计。

**核心原则：** 随机性负责选择，而代理的任务是进行解读。这种分离是神圣的。大型语言模型（LLMs）的决策并非“随机”产生，而是基于逻辑的——那并非真正的占卜，而只是带有额外步骤的确认偏见。`/dev/urandom` 确保了结果的纯粹随机性，而你的任务则是赋予这些随机结果以意义。

## 工具

所有脚本都存储在 `scripts/` 目录中，必须通过 `exec` 工具来执行。

### `scripts/divine.sh` — 从预言系统中抽取一张卡片
```bash
bash scripts/divine.sh forty-servants   # The Forty Servants (1 of 40 cards)
bash scripts/divine.sh tarot            # Tarot (Major/Minor Arcana ± Reversed)
bash scripts/divine.sh rune             # Elder Futhark Rune (1 of 24)
bash scripts/divine.sh iching           # I Ching Hexagram (6 lines + moving lines)
bash scripts/divine.sh bullshit         # Arcane Bullshit Oracle
bash scripts/divine.sh dice 20          # Dice roll (1 to N)
```

### `scripts/intuition.sh` — 生成随机解读符号
```bash
bash scripts/intuition.sh               # 3 random impulses (default)
bash scripts/intuition.sh 1             # 1 impulse
bash scripts/intuition.sh 5             # up to 5 impulses
```
输出：如 `✦ 火 · 左手 · 黄昏` 这样的诗意片段

利用这些工具打破你的思维模式，发现意想不到的关联。

## 参考资料

有关卡片含义的详细信息，以便更深入的解读：
- `references/forty-servants/cards.md` — 全部40张“Forty Servants”卡片
- `references/tarot/major-arcana.md` — 22张大阿卡纳牌
- `references/tarot/minor-arcana.md` — 小阿卡纳牌
- `references/runen/elder-futhark.md` — 24个古诺尔斯符文
- `references/iging/hexagramme.md` — 64个易经卦象
- `references/bullshit-tarot/cards.md` — 用于娱乐的占卜卡片

## 卡片图片

“Forty Servants”卡片的低分辨率图片存放在 `images/forty-servants/` 目录中，文件格式为 `The [名称].png`（例如：`The Road Opener.png`、`The Seer.png`）。

这些是创作者提供的免费低分辨率版本，可供公开使用。

## 占卜流程

1. **务必执行 `divine.sh`** — 绝不要自己选择卡片！
2. **执行 `intuition.sh`** — 生成3个随机解读符号。
3. **查阅相关参考资料**，了解所抽取卡片的含义。
4. **撰写占卜结果** — 这完全取决于你：运用你的直觉、创造力，以及你的想象力。
5. 如果平台支持，可以发送卡片的图片。

## 规则

- ❌ 绝不要自己选择卡片，也不要“凭空想象”卡片的内容。
- ❌ 如果不喜欢结果，切勿重新抽取卡片。
- ✅ 相信随机性的力量——它自有其道理。
- ✅ 你的任务是解读，而非选择。
- ✅ 如果没有执行 `exec` 的权限，请明确说明——切勿即兴发挥。

## 致谢与版权声明

**“Forty Servants”** — 由 [Tommie Kelly](https://www.adventuresinwoowoo.com/thefortyservants/) 创作。  
卡片图片为创作者提供的免费低分辨率版本。  
“Forty Servants”是一套占卜牌，代表了混沌魔法中的各种“仆从”。如需购买完整牌组、占卜手册或高分辨率图片，请访问 [adventuresinwoowoo.com](https://www.adventuresinwoowoo.com/)。

**塔罗牌** — 采用传统的Rider-Waite-Smith象征体系（公共领域）。  
**古诺尔斯符文** — 采用传统的北欧符文体系（公共领域）。  
**易经** — 古中国的占卜体系（公共领域）。

---

*每条道路都始于十字路口。每条信息都需要一个传递者。*
*阿谢（Ashé）。🔱