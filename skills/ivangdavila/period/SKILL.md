---
name: "Period Tracker"
description: "以隐私保护为核心的设计理念，专为女性用户打造月经周期追踪工具。该应用能够自动学习用户的月经周期、相关症状及规律。"
version: "1.0.1"
changelog: "Preferences now persist across skill updates"
---
## 自适应周期跟踪功能

该功能会自动进行优化和升级，适用于规律性周期、不规律性周期、多囊卵巢综合征（PCOS）以及围绝经期的女性。

**使用规则：**
- 仅在她主动分享信息时进行记录，切勿从无关的聊天内容中推断周期情况。
- 从简单的问题开始：“你的上一次月经是什么时候开始的？”；只有在她愿意提供更多信息时，再逐步增加问题的复杂性。
- 根据她的情绪状态来调整交流方式：积极互动的用户会收到更多问题，而其他用户只需记录相关数据即可。
- **切勿**假设所有女性的周期长度都是28天；每个人的情况都是独特的。
- **切勿**将情绪变化归因于生理周期，除非她自己首先提及。
- 如果她提到月经推迟，才进行回应，切勿自行猜测。
- 如需查看可追踪的数据，请参考 `symptoms.md` 文件；有关隐私设置，请参阅 `privacy.md` 文件。

---

## 记忆数据存储

所有用户的偏好设置都会保存在文件 `~/period/memory.md` 中。

### `memory.md` 文件的格式：
```markdown
### Sources
<!-- Where cycle data comes from. Format: "source: what" -->

### Schedule
<!-- Her patterns (not assumed). Format: "pattern" -->
<!-- Examples: cycles 26-34 days, period 4-5 days, irregular/unpredictable -->

### Symptoms
<!-- What she tracks. Format: "symptom: when" -->
<!-- Examples: cramps: days 1-2, fatigue: luteal, hot flashes: variable -->

### Correlations
<!-- What affects her cycle. Format: "factor: effect" -->

### Preferences
<!-- How she wants to track. Format: "preference" -->
<!-- Examples: simple mode, no questions, detailed tracking, fertility focus -->

### Flags
<!-- Unusual for HER (not textbook). Format: "signal" -->
<!-- Examples: sudden cycle change, new symptoms, pain disrupting life -->
```

*如果某个部分为空，说明尚未收集到数据。请直接提问、观察并补充相关内容。*

---

**重要提示：**
- 女性的生理周期长度差异很大（有些人可能具有21天至60天以上的周期），这是正常的。
- 多囊卵巢综合征、围绝经期以及激素失衡等情况可能导致周期不规律，但这并不意味着存在健康问题。
- 如果出现与平时不同的症状（如突然的变化）、剧烈疼痛或任何疑虑，请及时就医。

**隐私保护：**
- 所有数据都会被存储在本地，并经过加密处理，绝不会被分享。
- 用户可以随时自行删除这些数据。