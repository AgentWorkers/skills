---
name: fitbit
description: **Fitbit 健康数据集成**  
当用户需要获取健康数据洞察、锻炼总结、步数统计、心率数据、睡眠分析，或对自身的 Fitbit 活动数据有疑问时，可使用此功能。该服务提供基于人工智能的健康指标分析。
---

# Fitbit健身洞察

从您的Fitbit数据中获取由AI驱动的洞察。查询您的健身指标，分析趋势，并对您的活动提出问题。

## 功能

- 📊 每日活动总结（步数、卡路里、距离、活跃时间）
- 💓 心率数据和心率区间
- 😴 睡眠追踪与分析
- 🏃 锻炼/活动日志
- 📈 每周和趋势分析
- 🤖 由AI驱动的洞察和问答

## 先决条件

**需要：** Fitbit OAuth访问令牌

设置步骤请参考 `references/fitbit-oauth-setup.md`

## 命令

### 获取个人资料
```bash
FITBIT_ACCESS_TOKEN="..." python3 scripts/fitbit_api.py profile
```

### 每日活动
```bash
python3 scripts/fitbit_api.py daily [date]
# Examples:
python3 scripts/fitbit_api.py daily              # Today
python3 scripts/fitbit_api.py daily 2026-02-08   # Specific date
```

返回：步数、距离、卡路里、活跃时间（非常活跃/较为活跃/轻度活跃/久坐）

### 步数范围
```bash
python3 scripts/fitbit_api.py steps <start_date> <end_date>
```

示例：
```bash
python3 scripts/fitbit_api.py steps 2026-02-01 2026-02-07
```

返回：总步数、平均步数、每日分解

### 心率
```bash
python3 scripts/fitbit_api.py heart [date]
```

返回：静息心率、各心率区间及其对应的时长

### 睡眠数据
```bash
python3 scripts/fitbit_api.py sleep [date]
```

返回：睡眠时长、睡眠效率、开始/结束时间、睡眠阶段

### 记录的活动
```bash
python3 scripts/fitbit_api.py activities [date]
```

返回：记录的锻炼/活动（名称、时长、卡路里、距离）

### 每周总结
```bash
python3 scripts/fitbit_api.py weekly
```

返回：7天的步数和关键指标总结

## AI洞察的使用

当用户提出健身相关问题时，使用API获取相关数据，然后提供洞察：

**示例查询：**
- “我昨晚的睡眠情况如何？” → 获取睡眠数据，分析睡眠质量
- “我这周达到步数目标了吗？” → 获取每周总结，与目标进行比较
- “我锻炼时的平均心率是多少？” → 获取心率数据及锻炼记录，进行分析
- “我工作日还是周末更活跃？” → 获取活动数据，比较活动模式

**分析步骤：**
1. 确定所需数据
2. 通过相应的API命令获取数据
3. 分析数据
4. 以对话形式提供洞察

## 示例回复

**用户：“我这周表现如何？”**

**智能助手：**
1. 获取每周总结
2. 获取最近的睡眠数据
3. 回答：“您这周表现不错！平均每天8,234步（比上周增加了12%）。7天中有4天达到了1万步的目标。睡眠时长为7.2小时，睡眠效率为85%。周一、周三和周五的CrossFit训练表现稳定！”

**用户：“我今天锻炼了吗？”**

**智能助手：**
1. 获取每日活动记录
2. 获取每日活动总结（活跃时间）
3. 回答：“是的！您今天早上进行了45分钟的CrossFit训练，消耗了312卡路里。全天还有28分钟的非常活跃时间。”

## 需要关注的数据洞察

- **趋势：** 周与周之间的变化、活动模式的一致性
- **目标：** 与1万步的目标、锻炼频率、睡眠目标进行比较
- **相关性：** 睡眠质量与活动量、休息日与表现之间的关系
- **异常情况：** 不寻常的波动或下降
- **成就：** 个人最佳记录、连续锻炼的天数、重要里程碑

## 令牌管理

该技能会自动从 `/root/clawd/fitbit-config.json` 中加载令牌，并在令牌过期时（每8小时）自动刷新。

**自动刷新：** 令牌会自动更新，无需手动操作！

**手动刷新（如需）：**
```bash
python3 scripts/refresh_token.py force
```

**通过环境变量覆盖设置：**
```bash
export FITBIT_ACCESS_TOKEN="manual_token"
```

## 错误处理

- **令牌缺失：** 提示用户设置 FITBIT_ACCESS_TOKEN
- **API错误：** 检查令牌的有效性，可能需要刷新令牌
- **无数据：** 有些日子可能没有记录活动或缺少指标数据

有关令牌管理的详细信息，请参阅 `references/fitbit-oauth-setup.md`。