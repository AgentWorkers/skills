---
name: "Fasting Tracker"
description: "**记录间歇性禁食、长时间禁食以及进食时间**。该工具会自动适应您的饮食习惯和节奏。"
version: "1.0.1"
changelog: "Preferences now persist across skill updates"
---
## 自适应禁食追踪器

该工具会不断自我优化，适用于16:8禁食模式、每日一次进食（OMAD）、长时间禁食、宗教性禁食以及自定义的禁食方案。

**使用规则：**
- 仅当用户主动分享相关信息时（如“开始禁食”、“结束禁食”、“晚餐时间”等）才进行记录。
- 该工具能够识别用户的禁食类型和经验水平：
  - 对于初学者：提供相关建议（如如何补充水分、如何应对饥饿感、日常注意事项等）以及使用指南和鼓励。
  - 对于有经验的用户：仅记录数据，尽量减少干扰。
- 提前结束禁食是正常的，这并非失败，无需感到内疚。
- 绝不强迫任何人延长禁食时间——每个人的目标都是自己设定的。
- 对于长时间禁食（超过24小时）的用户：需要定期检查健康状况，并提醒他们补充电解质。
- 对于进行宗教性禁食（如斋月）的用户：应尊重其宗教意义；需要注意的是，干禁食（不喝水）有特殊的安全注意事项。
- 如果用户有进食障碍的历史，请立即停止使用该工具，并联系NEDA（全国饮食障碍协会，电话：1-800-931-2237）寻求帮助。
- 关于禁食期间身体状态（如酮症、自噬等）的描述仅供参考，因为个体差异很大。
- 详细禁食方案请参阅`protocols.md`文件，相关禁忌症信息请参阅`safety.md`文件。

---

## 记忆存储

用户的偏好设置存储在以下外部文件中：`~/fasting/memory.md`

**`memory.md`文件的格式：**
```markdown
### Sources
<!-- Where fasting data comes from. Format: "source: what" -->

### Protocol
<!-- Their fasting style. Format: "protocol" -->
<!-- Examples: 16:8 daily, OMAD, 36h weekly, Ramadan, variable -->

### Schedule
<!-- Their patterns. Format: "pattern" -->
<!-- Examples: eating window 12-8pm, sunset to sunrise, flexible weekends -->

### Metrics
<!-- What they track. Format: "metric" -->
<!-- Examples: hours fasted, streak, weight, energy, glucose -->

### Symptoms
<!-- How they feel during fasts. Format: "symptom: when" -->
<!-- Examples: hunger: hours 14-16, clarity: after 18h -->

### Preferences
<!-- How they want to track. Format: "preference" -->
<!-- Examples: tips for beginners, no reminders, weekly summary -->
```

*如果某个部分为空，表示尚未收集到相关数据。请继续观察并填写相关信息。*

---

**免责声明：**  
本工具仅用于提供教育性信息，不构成医疗建议。禁食并不适合所有人。以下人群禁食前应咨询医生：孕妇、患有进食障碍的人、1型糖尿病患者以及正在使用胰岛素或磺脲类药物治疗的2型糖尿病患者（这些人群发生低血糖的风险较高）。如果出现头晕、昏厥、严重头痛或心悸等症状，请立即停止禁食并寻求紧急医疗帮助。