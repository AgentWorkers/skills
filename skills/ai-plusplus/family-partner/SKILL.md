---
name: family-partner
description: >
  **家庭伴侣——基于AI的家庭助理技能套件**  
  这是一个包含11项家庭管理功能的综合工具集，涵盖日历管理、任务安排、记忆辅助、劳动时间跟踪、重要事件提醒、纪念日管理、投票功能以及各种挑战设置等。
version: 1.0.0
author: AI-PlusPlus
license: MIT
emoji: 🏠
metadata:
  openclaw:
    requires:
      bins:
        - sqlite3
    primaryEnv: ""
---
# 家庭伙伴技能套件

## 概述

Family Partner 是一款由人工智能驱动的全面家庭管理解决方案。它包含了11项集成技能，这些技能协同工作，帮助家庭组织日常生活、跟踪重要信息并创造美好的回忆。

## 包含的技能

### 1. 家庭日历 (📅)
**用途：** 创建、查看和管理家庭日程安排及事件。
**主要功能：**
- 查看今日/明日/本周的日程
- 创建包含参与者和地点的新事件
- 删除或修改现有事件
- 按参与者查询事件

**使用场景：**
- 用户询问今日/明日的日程安排
- 用户想要创建或删除事件
- 用户想要查看某人的日程安排

**示例：**
```bash
sqlite3 ~/.openclaw/family-partner/family.db \
  "SELECT time(start_time), title, participants, location \
   FROM events \
   WHERE date(start_time) = date('now') \
   ORDER BY start_time"
```

---

### 2. 家庭任务 (✅)
**用途：** 管理家庭的待办事项和购物清单。
**主要功能：**
- 添加、查看、完成和删除任务
- 将任务分配给家庭成员
- 支持待办事项和购物清单类型
- 批量添加购物项目

**使用场景：**
- 用户想要添加待办事项
- 用户想要查看任务列表
- 用户想要完成任务或删除任务
- 用户想要将任务分配给某人

**示例：**
```bash
sqlite3 ~/.openclaw/family-partner/family.db \
  "INSERT INTO tasks (id, title, type, assignee) \
   VALUES ('t20260302150000', 'Doctor appointment', 'todo', 'Mom')"
```

---

### 3. 家庭记忆 (💭)
**用途：** 记录和查询家庭成员的偏好、过敏情况以及重要信息。
**主要功能：**
- 存储偏好、不喜欢的事物和过敏信息
- 记录重要信息（医疗、学校、工作相关）
- 跟踪习惯和目标
- 可按成员或类型快速查找

**使用场景：**
- 用户想要记录家庭成员的偏好或过敏情况
- 用户询问某人的偏好
- 用户说“提醒我……”

**示例：**
```bash
sqlite3 ~/.openclaw/family-partner/family.db \
  "INSERT INTO memories (id, member_name, type, content) \
   VALUES ('m20260302150000', 'Ethan', 'allergy', 'Allergic to peanuts')"
```

---

### 4. 家庭劳动 (📊)
**用途：** 记录家务劳动并分析劳动分配的公平性。
**主要功能：**
- 记录家务劳动的时长
- 查看每日/每周/每月的统计数据
- 分析劳动分配的公平性
- 跟踪不同类型的家务劳动（烹饪、清洁、照顾孩子等）

**使用场景：**
- 用户想要记录家务劳动
- 用户想要查看劳动统计信息
- 用户想要分析劳动分配的公平性

**示例：**
```bash
sqlite3 ~/.openclaw/family-partner/family.db \
  "INSERT INTO labor (id, member_name, type, duration, date) \
   VALUES ('l20260302150000', 'Mom', 'cooking', 60, date('now'))"
```

---

### 5. 家庭时光 (⏰)
**用途：** 记录和回顾家庭共度的高质量时光。
**主要功能：**
- 记录家庭活动（晚餐、看电影、外出等）
- 查看活动历史
- 提供家庭共度时光的统计数据
- 进行年度家庭活动回顾

**使用场景：**
- 用户想要记录家庭活动
- 用户想要回顾家庭时光
- 用户想要了解家庭共度时光的统计数据

**示例：**
```bash
sqlite3 ~/.openclaw/family-partner/family.db \
  "INSERT INTO family_time (id, activity, participants, duration, date) \
   VALUES ('f20260302150000', 'Watch movie', 'Dad,Mom,Ethan', 120, date('now'))"
```

---

### 6. 家庭晨报 (🌅)
**用途：** 每日提供包含所有重要家庭信息的晨间简报。
**主要功能：**
- 今日日程概览
- 待办事项总结
- 购物清单
- 即将到来的纪念日提醒
- 天气提示（如果集成了API）

**使用场景：**
- 用户请求“晨间简报”或“早上好”
- 定时触发（例如每天早上8点）
- 用户想要快速了解当天的计划

**示例输出：**
```
☀️ Good morning! Today is March 2, 2026, Monday

📅 Today's Schedule:
09:00 - Take Ethan to school (Dad)
14:00 - Parent meeting (Mom)
19:00 - Family dinner

📋 To-do Items:
□ Doctor appointment (Mom)
□ Clean garage (Dad)

🛒 Shopping List:
□ Milk
□ Eggs

🎂 Upcoming Anniversaries:
March 5 - Ethan's Birthday 🎉

Have a wonderful day! 🌟
```

---

### 7. 家庭纪念日 (🎉)
**用途：** 管理重要的家庭纪念日和生日。
**主要功能：**
- 记录生日、结婚纪念日等特殊日期
- 查看接下来的纪念日（未来7天内）
- 根据出生年份计算年龄
- 支持多种纪念日类型

**使用场景：**
- 用户想要记录纪念日
- 用户询问即将到来的生日
- 需要重要日期的提醒

**示例：**
```bash
sqlite3 ~/.openclaw/family-partner/family.db \
  "INSERT INTO anniversaries (id, member_name, title, date, year, type) \
   VALUES ('a20260302150000', 'Ethan', 'Ethan Birthday', '03-05', 2018, 'birthday')"
```

---

### 8. 家庭购物 (🛒)
**用途：** 根据购买历史预测购物需求。
**主要功能：**
- 向购物清单中添加物品
- 查看购物历史
- 分析购买频率
- 生成购物建议

**使用场景：**
- 用户想要添加购物项目
- 用户想要查看购物历史
- 用户需要购物建议

**示例：**
```bash
sqlite3 ~/.openclaw/family-partner/family.db \
  "INSERT INTO tasks (id, title, type, status) \
   VALUES ('t20260302150000', 'Milk', 'shopping', 'pending')"
```

---

### 9. 家庭投票 (🗳️)
**用途：** 创建和管理家庭决策投票。
**主要功能：**
- 为家庭决策创建投票
- 家庭成员可以投票
- 查看投票结果
- 跟踪正在进行和已完成的投票

**使用场景：**
- 用户想要发起家庭投票
- 家庭需要共同做出决策
- 用户想要查看投票结果

**示例：**
```bash
sqlite3 ~/.openclaw/family-partner/family.db \
  "INSERT INTO votes (id, title, description, status) \
   VALUES ('v20260302150000', 'Where to go this weekend?', 'Options: Park, Playground, Cinema', 'active')"
```

---

### 10. 家庭里程碑 (🏆)
**用途：** 记录家庭成员的重要里程碑事件。
**主要功能：**
- 记录首次尝试、成就和成长里程碑
- 按成员查看里程碑历史
- 对里程碑进行分类（首次尝试、成就、成长、技能、生活等）
- 回顾成长历程

**使用场景：**
- 用户想要记录重要的里程碑
- 用户想要查看某人的里程碑
- 发生重要事件（如首次走路、毕业等）

**示例：**
```bash
sqlite3 ~/.openclaw/family-partner/family.db \
  "INSERT INTO milestones (id, member_name, title, category, date) \
   VALUES ('m20260302150000', 'Ethan', 'First independent steps', 'first', date('now'))"
```

---

### 11. 家庭挑战 (🎯)
**用途：** 创建和管理家庭挑战活动。
**主要功能：**
- 创建挑战（如锻炼、阅读、养成习惯等）
- 跟踪参与者的进度
- 查看排行榜
- 设置和跟踪完成情况

**使用场景：**
- 用户想要发起家庭挑战
- 用户想要记录挑战进度
- 用户想要查看排名

**示例：**
```bash
sqlite3 ~/.openclaw/family-partner/family.db \
  "INSERT INTO challenges (id, title, goal, description, status, start_date) \
   VALUES ('c20260302150000', 'Monthly Exercise Challenge', 30, 'Participant Progress:', 'active', date('now'))"
```

## 技术规格

### 数据库路径
所有技能使用的数据库路径为：`~/.openclaw/family-partner/family.db`

### 跨平台支持
所有技能都使用标准SQL命令，完全兼容Windows、macOS和Linux。OpenClaw会自动处理路径转换。

### ID生成规则
每个技能使用时间戳格式生成唯一ID：
- **日历：** `e` + YYYYMMDDHHMMSS（例如：`e20260302150000`）
- **任务：** `t` + YYYYMMDDHHMMSS（例如：`t20260302150000`）
- **记忆：** `m` + YYYYMMDDHHMMSS（例如：`m20260302150000`）
- **劳动：** `l` + YYYYMMDDHHMMSS（例如：`l20260302150000`）
- **家庭时光：** `f` + YYYYMMDDHHMMSS（例如：`f20260302150000`）
- **纪念日：** `a` + YYYYMMDDHHMMSS（例如：`a20260302150000`）
- **投票：** `v` + YYYYMMDDHHMMSS（例如：`v20260302150000`）
- **里程碑：** `m` + YYYYMMDDHHMMSS（例如：`m20260302150000`）
- **挑战：** `c` + YYYYMMDDHHMMSS（例如：`c20260302150000`）

### 异常情况处理
- 不存在的记录：返回“未找到”的提示信息
- 重复条目：警告用户并请求确认
- 结果为空：返回“无数据可用”的提示信息
- 输入无效：请求用户提供更多信息

## 示例交互

### 晨间例行事务
**用户：** 早上好
**AI：** ☀️ 早上好！今天是2026年3月2日，星期一。
  
  📅 今日日程：
  09:00 - 带伊桑去学校（爸爸）
  14:00 - 家长会议（妈妈）@ 学校
  19:00 - 家庭晚餐
  
  📋 待办事项：
  □ 看医生（妈妈）
  □ 清理车库（爸爸）
  
  🛒 购物清单：
  □ 牛奶
  □ 鸡蛋
  
  🎂 即将到来：
  3月5日 - 伊桑的生日 🎉
  
  祝你有美好的一天！🌟

### 任务管理
**用户：** 买牛奶和鸡蛋
**AI：** ✅ 已添加到购物清单：
    🛒 牛奶
    🛒 鸡蛋

**用户：** 购物清单里有什么？
**AI：** 🛒 购物清单：
    □ 牛奶
    □ 鸡蛋
    □ 面包

**用户：** 牛奶买好了
**AI：** ✅ 完成：牛奶 🎉

### 记录记忆
**用户：** 记得伊桑对花生过敏
**AI：** ✅ 已记录：伊桑对花生过敏 ⚠️
    未来的所有食物建议都会考虑这一点。

**用户：** 妈妈喜欢吃什么？
**AI：** ❤️ 妈妈的偏好：
    - 喜欢火锅
    - 喜欢拿铁咖啡
    - 喜欢紫色

### 劳动跟踪
**用户：** 妈妈今天做饭花了1小时
**AI：** ✅ 已记录：
    👤 妈妈
    🏠 做饭
    ⏱️ 60分钟

**用户：** 显示这个月的劳动统计
**AI：** 📊 本月的劳动贡献（总计：90小时）：
    👤 妈妈：45小时（50%）
    👤 爸爸：30小时（33%）
    👤 伊桑：15小时（17%）
    
    💡 建议：爸爸可以多承担一些家务~

### 创建事件
**用户：** 提醒爸爸下周六下午3点带伊桑去上舞蹈课
**AI：** ✅ 创建事件：
    📅 时间：3月8日（星期六）15:00
    📝 事件：舞蹈课
    👥 参与者：爸爸、伊桑

### 家庭投票
**用户：** 我们来投票决定这个周末去哪里吧
**AI：** ✅ 创建投票：
    📋 这个周末去哪里？
    
    选项：
    1️⃣ 公园
    2️⃣ 游乐场
    3️⃣ 电影院
    
    家庭成员可以开始投票！

### 里程碑记录
**用户：** 伊桑今天第一次独立走路了！
**AI：** ✅ 记录里程碑：
    👶 伊桑
    🎯 第一次独立行走
    📂 类别：首次尝试
    📅 2026年3月2日
    
    这是伊桑成长中的一个重要时刻！🎉

### 家庭挑战
**用户：** 开始一个每月的锻炼挑战
**AI：** ✅ 创建挑战：
    🏆 每月锻炼挑战
    🎯 目标：30次
    📅 开始日期：2026年3月2日
    
    家庭成员现在可以加入！

## 安装与设置

### 先决条件
- OpenClaw >= 0.8.0
- 已安装SQLite3

### 数据库初始化
该软件包包含用于数据库设置的 `init.sql` 文件。运行：
```bash
sqlite3 ~/.openclaw/family-partner/family.db < init.sql
```

## 许可证

MIT许可证 - 详情请参阅 LICENSE 文件。

## 支持

如有问题或疑问，请访问项目仓库。