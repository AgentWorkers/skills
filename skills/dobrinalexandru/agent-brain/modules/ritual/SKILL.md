# 仪式记忆 🔄

**状态：** ✅ 已启用 | **模块：** 仪式记忆 | **所属部分：** 代理大脑（Agent Brain）

习惯的形成与程序化快捷方式——大脑的“自动驾驶”功能。

## 功能介绍

- **跟踪**：重复出现的动作
- **自动化**：创建快捷操作
- **强化**：通过重复使用，使动作变为自动化行为

## 习惯的形成过程

### 什么会自动化？

| 触发条件 | 动作 | 强化程度 |
|---------|--------|----------|
| 星期一早晨 | 检查加密货币价格 | 高 |
| 新研究内容 | 保存到记忆中 | 高 |
| 会议结束 | 发送跟进提醒 | 中等 |
| 检测到错误 | 检查系统信号 | 高 |

### 快捷方式的类型

- **程序化快捷方式**：```
"How to do X" → cached procedure
```
- **基于时间的快捷方式**：```
"8am weekday" → morning routine
```
- **基于上下文的快捷方式**：```
"Research task" → research workflow
```

## 学习与强化机制

- **使用动作** → 强化程度 + 0.1
- **操作成功** → 强化程度 + 0.2
- **用户确认** → 强化程度 + 0.3

## 快捷方式的衰减机制

- **未使用** → 强化程度逐渐减弱
- **操作失败** → 强化程度降低
- **被替代的快捷方式** → 从系统中移除

## 使用方法

```
"This is how I always do X"
"Make this automatic"
"I do this every time Y"
"Create shortcut for Z"
```

## 示例

- **早晨例行事务**：```
8am EET weekday → 
  1. Check crypto
  2. Review calendar
  3. Check emails
```
- **研究流程**：```
New research →
  1. Web search
  2. Extract key points
  3. Save to memory
  4. Summarize
```
- **会议后的处理**：```
Meeting ended →
  1. Extract action items
  2. Set reminders
  3. Note follow-ups
```

## 集成机制

该功能与代理大脑的以下模块协同工作：
- **档案系统**：用于存储程序化操作
- **判断系统**：决定何时执行相应操作
- **错误检测系统**：监控系统运行状态