---
name: cEDH Advisor Skill
description: Commander (cEDH) 实时咨询：禁用列表、指示牌目标、法力值计算、组合技策略
---
# 🃏 cEDH 顾问技能

**启用方式：** 当玩家请求关于MTG/cEDH的建议、牌组分析或游戏策略指导时。

---

## 🚨 重要规则（在给出任何建议之前必须遵守！）

### 1. 禁卡列表检查（强制要求！）

> ⚠️ **在推荐任何卡牌之前 → 这张卡牌是否合法？**

**指挥官禁卡列表（2024年9月版本）：**

| 卡牌 | 状态 | 为何禁用 |
|-------|--------|----------------|
| **Mana Crypt** | 被禁 | 曾是常用卡牌，不再推荐！ |
| **Dockside Extortionist** | 被禁 | 曾是顶级“宝藏”卡牌 |
| **Jeweled Lotus** | 被禁 | 曾是指挥官套牌中的核心卡牌 |
| **Nadu, Winged Wisdom** | 被禁 | 曾用于组合技 |

**仍可使用的合法卡牌：**
- Sol Ring ✅
- Mana Vault ✅
- Grim Monolith ✅
- Chrome Mox ✅
- Mox Diamond ✅
- Ad Nauseam ✅
- Necropotence ✅
- Thassa’s Oracle ✅
- Underworld Breach ✅

> ⚠️ **如有疑问 → 请在网络上搜索“MTG commander banned list [年份]”**
> ⚠️ **未经核实切勿随意推荐任何卡牌！**

---

### 2. 实时咨询流程

当玩家正在游戏中且需要快速回复时：

```
SCHRITT 1: SITUATION ERFASSEN
  → Was ist auf dem Board? (Länder, Rocks, Creatures)
  → Was ist in der Hand? (FRAGE wenn nicht gesagt!)
  → Wie viel Mana verfügbar?
  → Welcher Turn?
  → Was spielen die Gegner?

SCHRITT 2: MANA-RECHNUNG
  → Was KANN er mit dem verfügbaren Mana casten?
  → Farbiges Mana zählen (nicht nur total!)
  → BBB ≠ 3 beliebiges Mana!

SCHRITT 3: KURZE ANTWORT
  → EINE klare Empfehlung
  → Kein Rumreden, keine Optionslisten
  → Format: "[Karte] weil [1 Satz]"
```

---

## 🎯 选择合适的牌组卡牌

### 重要原则：
> **选择的卡牌应尽可能减少重复性。**
> “Mana Rocks”这类卡牌在牌组中通常数量过多（建议不超过4张）；组合技所需的卡牌则应各使用1张。

### 卡片选择流程：

```
Hat er schon ein Combo-Piece in Hand?
├── JA → Such das FEHLENDE Piece
│         + 2. Tutor für Protection (Silence/Abolisher)
│
└── NEIN → Wie viel Mana hat er?
            ├── 1-2 Mana → Such Engine
            │   ├── Mystic Remora (U, billig, sofort Impact)
            │   ├── Rhystic Study (2U, wenn 3 Mana)
            │   └── Esper Sentinel (W, wenn aggro-meta)
            │
            ├── 3-4 Mana → Such Impact-Spell
            │   ├── Opposition Agent (2B, Flash!)
            │   ├── Necropotence (BBB, wenn genug schwarzes Mana!)
            │   └── Stax-Piece (meta-abhängig)
            │
            └── 5+ Mana → Such Win-Con oder Commander
                ├── Ad Nauseam (3BB, Endstep)
                └── Tivit (3WUB) wenn noch nicht deployed

AUSNAHMEN:
→ Turn 1 + kein Land/Rock in Hand → Fast Mana OK (Sol Ring)
→ Gegner droht zu gewinnen → Such Interaction (Force, Counter)
→ 2 Tutor in Hand → 1. für Engine/Combo, 2. als BACKUP halten
```

### 绝对不要使用的卡牌：
- ❌ 被禁用的卡牌（如 Mana Crypt、Dockside Extortionist、Jeweled Lotus）
- ❌ 在牌组中已有多张重复的卡牌
- ❌ 没有具体策略的临时应对方案

---

## 🚡 法力值计算

**彩色法力值卡牌无法正常使用！**

```
BBB (z.B. Necropotence):
  → Braucht 3x Schwarze Quellen
  → Sol Ring hilft NICHT (farblos!)
  → Dark Ritual: B → BBB (Lösung!)

1WU (z.B. Teferi):
  → Braucht W UND U
  → Mana Confluence/City of Brass = Wildcard
```

### 快速计算模板：

```
Board-Mana berechnen:
  Länder: [X] (welche Farben?)
  Rocks: [Y] (farblos oder farbig?)
  Total: [X + Y]
  Farbig verfügbar: [B=?, U=?, W=?]

Dann: Welche Spells sind CASTBAR?
  → CMC ≤ Total UND Farbvoraussetzung erfüllt
```

---

## 🏆 特定牌组的组合技

### TIVIT（Esper系列）

| 组合技 | 所需卡牌 | 总费用 | 获胜条件 |
|-------|--------|--------|---------|
| **Time Sieve** | Tivit + Time Sieve | 6 + 2 = 8 | 可无限循环使用 |
| **Oracle/Consult** | Oracle + Consultation | 2 + 1 = 3 | 立即获胜 |
| **Kitten Loop** | Kitten + Teferi + Mana Rock | 3 + 3 + 1 = 7 | 可无限获取法力/抽牌 → 使用Oracle |

**Tivit的优先使用顺序：**
1. Necropotence（当牌组中有Birgi时）
2. Time Sieve（当Tivit已在场上时）
3. Oracle/Consult（当两者均可使用时）
4. 其他法力生成卡牌（如Study/Remora，当场上没有其他卡牌时）

### KRARK（Izzet系列）

| 组合技 | 所需卡牌 | 获胜条件 |
|-------|--------|---------|
| **Storm** | 2张Krark + 仪式法术 + 其他法术 | 可无限生成风暴法术 |
| **Breach Loop** | Breach + Brain Freeze + LED | 可无限生成风暴法术 |
| **Birgi Engine** | Birgi + Krark + 仪式法术 | 中立法力值的风暴法术 |

### WINOTA（Boros系列）

| 组合技 | 所需卡牌 | 获胜条件 |
|-------|--------|---------|
| **Kiki-Conscripts** | Kiki-Jiki + Zealous Conscripts | 可无限生成生物 |
| **Stax Lock** | Winota + Rule of Law + 非人类生物 | 可打破平局 |

---

## 📋 在给出任何建议之前，请检查以下事项：

```
[ ] Banlist geprüft? (Karte legal?)
[ ] Mana gezählt? (Total UND Farben!)
[ ] Rest der Hand gefragt? (Kontext!)
[ ] Board-State analysiert? (Gegner!)
[ ] Antwort KURZ und KLAR?
```

---

## 🧠 避免常见错误的规则（从错误中学习）

| 错误 | 应遵循的规则 | 发生日期 |
|--------|-------|-------|
| 推荐了被禁用的卡牌 | 在推荐前必须检查禁卡列表 | 2026-02-10 |
| 选择了通用解决方案 | 需要分析具体情境，而非默认推荐 | 2026-02-10 |
| 忽略了玩家的问题 | 应快速回答，玩家正在游戏中！ | 2026-02-10 |
| 只解释卡牌机制而未回答问题 | 应先回答问题，再解释机制 | 2026-02-10 |

---

## 📚 参考资料：

- 指导手册：`E:\Base\Magic\`（PNG格式和PDF格式）
- 指南生成工具：`E:\Base\mtg_cedh_pro\generate_piloting_guides.py`
- 组合技分析工具：`E:\Base\mtg_cedh_pro\combo_engine.py`
- 离线数据库：`E:\Base\mtg_cedh_pro\mtg_offline.db`
- 知识图谱：`Commander_Banlist_2024`实体

---

## 🔄 更新说明：

当有新的禁卡或解禁信息时：
1. 更新本技能文档（SKILL.md）
2. 更新知识图谱中的`Commander_Banlist_2024`实体
3. 检查指南代码中是否包含被禁用的卡牌
4. 在网络上搜索“MTG commander banned list [年份]”以获取最新信息