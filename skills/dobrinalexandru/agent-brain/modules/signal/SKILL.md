# 信号记忆系统 ⚡

**状态：** ✅ 正在运行 | **模块：** signal | **所属部分：** 代理大脑（Agent Brain）

该系统负责冲突检测和错误监控，是代理大脑中的错误检测机制。

## 功能概述

- **检测**：识别矛盾或冲突现象
- **监控**：自动检查是否存在错误
- **警报**：在发现异常情况时发出提示

## 冲突类型

### 逻辑冲突
```
User: "I prefer short"
User: "Give me details"
→ Flag contradiction
```

### 事实冲突
```
Memory A: X happened in Feb
Memory B: X happened in Mar
→ Flag inconsistency
```

### 程序性冲突
```
Method A worked for X
Method B worked for Y
User wants Z (similar to both)
→ Ask for preference
```

### 预期与实际不符的冲突
```
User asked for short
User got 5-page response
→ Flag mismatch
```

## 检测方法

### 明确的冲突检测方式
- 用户指出错误
- 用户纠正你的说法
- 用户表现出沮丧情绪

### 隐性的冲突检测方式
- 重复提问
- 语气变化
- 回应后的沉默

### 系统性冲突检测
- 跨模块比较记忆信息
- 核对数据一致性
- 验证事实的准确性

## 错误监控机制

### 自我检查
- 我的回答是否正确？
- 是否存在矛盾？
- 自我评估准确性

### 反馈机制
- 接收用户反馈并据此进行更新
- 对用户的纠正表示认可
- 回复：“你说得对，我之前理解错了”

## 对冲突的处理方式

### 发现冲突时的应对措施
```
"Wait, I'm getting conflicting info:
- X says Y
- Z says W

Can you clarify?"
```

### 错误被确认时的处理
```
"I got that wrong. Correcting: ..."
```

### 面对不确定情况时的处理
```
"I'm not 100% sure. Want me to:
1. Check more
2. Make best guess
3. Ask for clarification"
```

## 使用方法

该系统作为代理大脑的一部分，与以下模块协同工作：
- **档案模块**（Archive）：用于检查数据一致性
- **信心评估模块**（Gauge）：用于调整系统的自我评估信心
- **情绪响应模块**（Vibe）：根据错误情况生成相应的情绪反馈