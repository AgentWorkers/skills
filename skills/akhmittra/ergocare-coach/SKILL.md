---
name: ergocare-coach
description: 您的个人“办公健康教练”，具备自动提醒功能，帮助您保持良好的工作习惯。该工具会为您生成针对不同操作平台的脚本（bash/PowerShell），用于执行“20-20-20”眼部保护规则、腰部锻炼以及预防重复性劳损（RSI）的相关动作。它提供全面的锻炼计划、人体工程学指导，并支持自定义通知设置，专为计算机专业人士设计。
metadata:
  openclaw:
    emoji: "👁️"
    version: "1.0.0"
    author: "AM"
    tags: ["health", "wellness", "ergonomics", "eye-exercises", "break-reminders", "posture", "rsi-prevention", "desk-health", "automation"]
    requires:
      bins: []
      env: []
      config: []
---

# ErgoCare Coach 👁️🦴💪

## 产品描述

ErgoCare Coach 是您的智能健康与工作习惯助手，它会自动提醒您进行适当的休息和锻炼！ErgoCare Coach 提供以下功能：

1. **专业的锻炼指导**：20-20-20 视力保护规则、腰部拉伸、颈部锻炼以及预防重复性劳损（RSI）的练习。
2. **平台专属的提醒脚本**：生成适用于 Linux/Mac 和 Windows 的 Bash 脚本或 PowerShell 脚本，可在后台运行。
3. **自动通知**：桌面通知、终端提醒、声音提示以及视觉倒计时。
4. **可自定义的作息时间表**：20-20-20 规则、每小时的小休息、自定义休息间隔以及工作时长限制。
5. **全面的锻炼计划**：从 30 秒的短暂休息到 10 分钟的全面锻炼。

**“最宝贵的财富是健康。”**

ErgoCare Coach 非常适合以下人群：
- 长时间使用电脑的专业人士
- 有眼睛疲劳或干眼症状的人
- 颈部、腰部或肩部疼痛的人
- 游戏玩家和内容创作者
- 学生和研究人员
- 远程工作者和伏案工作者
- 希望预防重复性劳损和其他健康问题的所有人

---

## 产品工作原理

### 两种使用模式

**模式 1：交互式锻炼指导**
- 随时询问具体的锻炼方法：例如：“展示眼部锻炼方法。”
- 获取即时建议：例如：“我脖子疼，该怎么办？”
- 学习完整的锻炼计划：例如：“给我一个 5 分钟的全身锻炼计划。”

**模式 2：自动提醒脚本** ⭐ **新功能！**
- 请求自定义脚本：例如：“为我的 Mac 生成一个 20-20-20 规则的提醒脚本。”
- 脚本会在后台运行，并自动发送通知。
- 休息间隔和锻炼类型均可完全自定义。

---

## 1. 快速入门：获取您的提醒脚本

### 请求自定义脚本

只需向 ErgoCare Coach 提出请求：

```
"Generate a 20-20-20 reminder script for Linux"
"Create a Windows PowerShell script with hourly breaks"
"Give me a Mac script with eye and back exercises every 30 minutes"
"Make me a comprehensive break script for Ubuntu with all exercise types"
```

### 脚本特点

所有脚本均包含：
- ✅ 带有锻炼说明的桌面通知
- ✅ 休息期间的倒计时
- ✅ 可选的声音提示
- ✅ 可自定义的休息间隔
- ✅ 多种类型的锻炼
- ✅ 简单的启动/停止/重新启动功能
- ✅ 可选择在系统启动时自动运行

**平台支持：**
- **Linux**：使用 `notify-send`、`zenity` 或终端提示的 Bash 脚本
- **macOS**：使用 `osascript` 的 Bash 脚本和语音提示
- **Windows**：使用 `BurntToast` 模块的 PowerShell 脚本或系统内置通知

---

## 2. 20-20-20 规则（视力保护基础）

### 规则内容

**每 20 分钟，看 20 英尺外的物体 20 秒。**

### 规则原理

长时间盯着屏幕会导致眼睛肌肉持续紧张：
- **睫状肌** 为了聚焦近处物体而保持收缩状态
- **外眼肌** 保持固定位置
- **眨眼频率** 从每分钟 15-20 次降至 5-7 次（导致眼睛干涩）
- **蓝光** 会增加眼睛疲劳

通过看远处的物体：
- ✅ 放松睫状肌
- ✅ 促进自然眨眼
- ✅ 重置眼睛的聚焦机制
- ✅ 减轻眼睛疲劳

### 20-20-20 规则的实现方式

您的自动脚本会：
1. 在后台无声运行
2. 记录 20 分钟的时间间隔
3. 发送桌面通知：“👁️ 20-20-20 休息时间：看 20 英尺外的物体 20 秒”
4. （可选）播放轻柔的声音提示
5. （可选）显示倒计时
6. 每 20 分钟重复一次

**手动执行 20-20-20 规则的方法：**
- 看窗外的建筑物、树木或天空
- 看走廊或房间另一端的物体
- 看远处的墙钟或艺术品
- 通过打开的门看向室外
- 任何真正位于 20 英尺以外的物体

---

## 3. 眼部锻炼库

### 快速眨眼恢复（30 秒）
**适用场景**：每小时一次，或当眼睛感到干涩时

```
1. Close eyes gently (don't squeeze) - 2 seconds
2. Open eyes wide - 2 seconds  
3. Repeat 10 times
4. Finish with 10 rapid blinks

Benefits: Refreshes tear film, prevents dry eyes
```

### 握拳按摩（1-2 分钟）
**适用场景**：上午、午饭后或下午

```
1. Rub palms together until warm
2. Cup palms over closed eyes (don't press)
3. Block all light completely
4. Breathe deeply for 60-120 seconds
5. Slowly remove hands

Benefits: Deep relaxation, reduces eye fatigue
```

### 眼球转动（45 秒）
**适用场景**：每 2 小时一次

```
1. Look up, pause 2 seconds
2. Slowly roll eyes clockwise (full circle) - 3 seconds
3. Pause, center
4. Slowly roll eyes counterclockwise - 3 seconds
5. Repeat 5 times each direction

Benefits: Exercises all eye muscles, increases range of motion
```

### 转移视线（1 分钟）
**适用场景**：每小时一次

```
1. Hold finger 10 inches from your face
2. Focus on finger - 5 seconds
3. Shift focus to object 20 feet away - 5 seconds
4. Repeat 10 times

Benefits: Strengthens focusing ability, prevents presbyopia progression
```

### 八字形眼球运动（1 分钟）
**适用场景**：中午感到眼睛疲劳时

```
1. Imagine a large figure 8 on the wall (10 feet away)
2. Trace it slowly with your eyes (don't move head) - 30 seconds clockwise
3. Trace it 30 seconds counterclockwise
4. Repeat 2 times

Benefits: Improves eye coordination and flexibility
```

### 近远焦点切换（1 分钟）
**适用场景**：每 90 分钟一次

```
1. Hold thumb at arm's length
2. Focus on thumb - 10 seconds
3. Focus on something 20+ feet away - 10 seconds
4. Repeat 5 times

Benefits: Reduces accommodation stress
```

---

## 4. 腰部锻炼库

### 坐姿脊柱扭转（每侧 1 分钟）
**适用场景**：每小时一次

```
1. Sit up straight, feet flat on floor
2. Place right hand on back of chair
3. Place left hand on right knee
4. Inhale: lengthen spine
5. Exhale: twist to the right
6. Hold 30 seconds, breathe normally
7. Repeat on left side

Benefits: Relieves lower back tension, improves spine mobility
```

### 坐姿猫牛式（1 分钟）
**适用场景**：每 45-60 分钟一次

```
1. Sit on edge of chair, hands on knees
2. Inhale: arch back, look up (cow)
3. Exhale: round back, tuck chin (cat)
4. Flow between positions 10 times slowly
5. Hold each position 3 seconds

Benefits: Mobilizes entire spine, reduces stiffness
```

### 站姿髋部弯曲（45 秒）
**适用场景**：每 90 分钟一次

```
1. Stand with feet hip-width apart
2. Place hands on lower back
3. Hinge forward at hips (not waist)
4. Keep back straight, slight knee bend
5. Go until you feel stretch in hamstrings
6. Hold 15 seconds
7. Slowly return to standing
8. Repeat 3 times

Benefits: Stretches hamstrings, strengthens lower back
```

### 坐姿前倾（1 分钟）
**适用场景**：上午或午饭后

```
1. Sit on edge of chair
2. Feet hip-width apart, flat on floor
3. Inhale: lengthen spine
4. Exhale: fold forward from hips
5. Let arms hang, relax neck and shoulders
6. Hold 30-60 seconds
7. Slowly roll up, vertebra by vertebra

Benefits: Decompresses spine, relieves lower back
```

### 骨盆倾斜（1 分钟）
**适用场景**：每 2 小时一次

```
1. Sit with back against chair, feet flat
2. Tilt pelvis forward (arch lower back)
3. Hold 5 seconds
4. Tilt pelvis backward (flatten lower back against chair)
5. Hold 5 seconds
6. Repeat 10 times

Benefits: Strengthens core, mobilizes pelvis
```

### 站姿腿部伸展（每侧 1 分钟）
**适用场景**：每 2 小时一次

```
1. Stand near chair for support
2. Bend right knee, grab right ankle behind you
3. Gently pull heel toward glutes
4. Simultaneously press hips forward
5. Hold 30 seconds
6. Repeat on left side

Benefits: Stretches hip flexors, counteracts sitting posture
```

---

## 5. 颈部和肩部锻炼库

### 颈部转动（1 分钟）
**适用场景**：每 45 分钟一次

```
1. Sit or stand with relaxed shoulders
2. Drop chin to chest - 5 seconds
3. Slowly roll head to right shoulder - 5 seconds
4. Roll head back (don't force) - 5 seconds
5. Roll to left shoulder - 5 seconds
6. Return to center
7. Repeat 3 times each direction

Benefits: Releases neck tension, improves mobility
```

### 肩部耸动（45 秒）
**适用场景**：每小时一次

```
1. Inhale: raise shoulders to ears
2. Hold 5 seconds (squeeze)
3. Exhale: drop shoulders down and back
4. Hold 5 seconds (relax)
5. Repeat 10 times

Benefits: Relieves shoulder tension, improves posture
```

### 颈部侧向拉伸（每侧 1 分钟）
**适用场景**：每 90 分钟一次

```
1. Sit up straight
2. Place right hand on left side of head
3. Gently pull head toward right shoulder
4. Keep left shoulder down
5. Hold 30 seconds
6. Repeat on left side

Benefits: Stretches neck muscles, reduces headaches
```

### 下巴内收（1 分钟）
**适用场景**：每 2 小时一次

```
1. Sit or stand with good posture
2. Keep eyes forward
3. Gently tuck chin (double chin appearance)
4. Don't tilt head down
5. Hold 5 seconds
6. Relax
7. Repeat 10 times

Benefits: Strengthens neck, counteracts forward head posture
```

### 肩胛骨挤压（45 秒）
**适用场景**：每小时一次

```
1. Sit up straight, arms at sides
2. Squeeze shoulder blades together
3. Imagine holding a pencil between them
4. Hold 5 seconds
5. Relax 5 seconds
6. Repeat 10 times

Benefits: Strengthens upper back, improves posture
```

---

## 6. 手腕和手部锻炼（预防重复性劳损）

### 手腕旋转（45 秒）
**适用场景**：每 60 分钟一次

```
1. Extend arms forward
2. Make gentle circles with wrists
3. 10 circles clockwise
4. 10 circles counterclockwise
5. Rest
6. Repeat 2 times

Benefits: Prevents carpal tunnel, increases wrist mobility
```

### 手指伸展（1 分钟）
**适用场景**：每 90 分钟一次

```
1. Extend right arm, palm up
2. With left hand, gently pull back each finger
3. Hold each 5 seconds
4. Repeat on left hand
5. Then: make fist, spread fingers wide - 10 times

Benefits: Prevents trigger finger, reduces hand stiffness
```

### 祈祷式伸展（45 秒）
**适用场景**：每 2 小时一次

```
1. Press palms together in front of chest (prayer position)
2. Fingers pointing up
3. Slowly lower hands toward waist
4. Keep palms pressed together
5. Stop when you feel stretch in wrists
6. Hold 30 seconds

Benefits: Stretches wrist flexors, prevents carpal tunnel
```

### 反向祈祷式伸展（45 秒）
**适用场景**：每 2 小时一次（在祈祷式伸展之后）

```
1. Place backs of hands together in front of chest
2. Fingers pointing down
3. Press hands together
4. Hold 30 seconds

Benefits: Stretches wrist extensors
```

### 拳头泵动（30 秒）
**适用场景**：每小时一次

```
1. Make tight fist
2. Hold 5 seconds
3. Open hand, spread fingers wide
4. Hold 5 seconds
5. Repeat 10 times

Benefits: Increases blood flow, reduces stiffness
```

---

## 7. 全身锻炼计划

### 2 分钟的快速恢复
**适用场景**：每 30 分钟一次

```
1. 20-20-20 eye break (20 seconds)
2. Shoulder shrugs (20 seconds)
3. Neck side stretches (30 seconds)
4. Seated spinal twist (30 seconds)
5. Wrist circles (20 seconds)

Total: 2 minutes
```

### 5 分钟的活力休息
**适用场景**：每 90 分钟一次

```
1. Palming (1 minute)
2. Seated cat-cow (1 minute)
3. Neck rolls (1 minute)
4. Standing hip hinge (45 seconds)
5. Shoulder blade squeezes (45 seconds)
6. Wrist and finger stretches (30 seconds)

Total: 5 minutes
```

### 10 分钟的全面锻炼
**适用场景**：上午、午饭后或下午

```
1. Eye exercises (2 minutes):
   - Focus shifting
   - Eye rolls
   - 20-20-20
   
2. Neck and shoulders (3 minutes):
   - Neck rolls
   - Shoulder shrugs
   - Neck side stretches
   - Chin tucks
   
3. Back and core (3 minutes):
   - Seated cat-cow
   - Seated spinal twists
   - Standing hip hinge
   - Pelvic tilts
   
4. Wrists and hands (2 minutes):
   - Wrist circles
   - Prayer stretches
   - Finger stretches
   - Fist pumps

Total: 10 minutes
```

---

## 8. 休息时间表示例

### 轻度使用者（每天使用电脑 4-6 小时）

```
Every 20 minutes: 20-20-20 eye break (20 seconds)
Every 60 minutes: 2-minute quick reset
Every 2 hours: 5-minute energy break

Daily total breaks: ~40 minutes
```

### 中度使用者（每天使用电脑 6-8 小时）

```
Every 20 minutes: 20-20-20 eye break (20 seconds)
Every 45 minutes: 2-minute quick reset  
Every 90 minutes: 5-minute energy break
Mid-morning + afternoon: 10-minute full routine (2x)

Daily total breaks: ~60 minutes
```

### 重度使用者（每天使用电脑 8 小时以上）**推荐**

```
Every 20 minutes: 20-20-20 eye break (20 seconds)
Every 30 minutes: 2-minute quick reset
Every 60 minutes: 5-minute energy break
Every 3 hours: 10-minute full routine
Lunch break: 30-minute walk (away from computer)

Daily total breaks: ~90 minutes
```

---

## 9. 脚本生成指南

### 请求 Linux/Mac Bash 脚本

**请求方式：**
```
"Generate a 20-20-20 reminder script for Linux"
"Create a Mac bash script with full break schedule"
"Make me an Ubuntu script with eye and back exercises every 45 minutes"
```

**您将获得：**
- 使用 `notify-send`（Linux）或 `osascript`（Mac）的 Bash 脚本
- 通知中包含锻炼说明
- 使用 `paplay` 或 `say` 的声音提示
- 终端中的倒计时功能
- 可自定义的参数
- 安装说明

**特点：**
- 在后台运行（`./ergocare.sh &`）
- 可添加到系统启动脚本（`crontab @reboot`）
- 可停止脚本（`pkill -f ergocare.sh`）
- 可记录休息时间（可选）

### 请求 Windows PowerShell 脚本

**请求方式：**
```
"Generate a Windows break reminder script"
"Create a PowerShell script for 20-20-20 with hourly stretches"
"Make me a Windows script with all exercise types"
```

**您将获得：**
- 使用系统内置通知功能的 PowerShell 脚本
- 集成 `BurntToast` 模块以增强通知效果
- 使用 `[System.Media.SystemSounds]` 的声音提示
- 可在系统托盘显示图标
- 提供任务调度器设置指南

**特点：**
- 在系统启动时自动运行
- 可将脚本最小化到系统托盘
- 具有暂停/恢复功能
- 可记录休息时间

### 脚本自定义参数

所有生成的脚本顶部都包含易于编辑的参数：

```bash
# CONFIGURATION (edit these)
EYE_INTERVAL=1200        # 20 minutes in seconds
STRETCH_INTERVAL=2700    # 45 minutes
LONG_BREAK_INTERVAL=5400 # 90 minutes
SOUND_ENABLED=true       # true or false
NOTIFICATION_TYPE="all"  # "popup", "sound", "terminal", "all"
```

---

## 10. 人体工程学工作环境设置

### 显示器位置
- **高度**：屏幕位于眼睛水平或略低的位置
- **距离**：距离屏幕 20-28 英寸（50-70 厘米）
- **角度**：向后倾斜 10-20 度
- **多显示器设置**：主显示器应正对前方

### 椅子设置
- **座椅高度**：双脚平放在地上，大腿与地面平行
- **座椅深度**：座椅边缘与膝盖后部之间距离为 2-4 英寸
- **靠背**：支撑腰部的自然曲线
- **扶手**：肘部呈 90 度角，肩膀放松

### 桌子和键盘
- **桌子高度**：打字时肘部呈 90-100 度角
- **键盘**：保持平坦或略微向下倾斜，靠近身体
- **鼠标**：与键盘处于同一高度，靠近身体
- **手腕位置**：保持中立（不向上或向下弯曲）

### 照明
- **无眩光**：将显示器与窗户成 90 度角
- **工作照明**：降低屏幕与周围环境的对比度
- **蓝光过滤**：日落后启用蓝光过滤功能（f.lux，夜间模式）
- **屏幕亮度**：调整至与周围光线相匹配

---

## 11. 警示信号及就医建议

### 需立即就医的情况：
- 🚨 突然视力丧失或变化
- 🚨 严重的眼部疼痛
- 🚨 麻木或刺痛感扩散或加剧
- 🚨 失去对肠道/膀胱的控制能力（可能与背部问题相关）
- 🚨 手臂或腿部无力

### 如出现以下情况，请尽快就医：
- ⚠️ 持续性头痛（持续数周）
- ⚠️ 双重视觉或视力模糊（休息后无改善）
- ⚠️ 疼痛向下肢放射
- ⚠️ 持续超过 6 周的慢性疼痛
- ⚠️ 尽管休息和锻炼仍感到疼痛加剧

### 注意：ErgoCare Coach 用于预防，而非治疗！
- ✅ 用于预防和缓解轻微不适
- ✅ 保持健康习惯
- ❌ 不要替代医疗治疗
- ❌ 不要忽视严重或恶化的症状

---

## 12. 高级功能

### 智能休息时间表

**请求根据具体情况定制的时间表：**
```
"I'm a software developer, create my ideal break schedule"
"I have chronic neck pain, what's my schedule?"
"I'm a gamer, help me stay healthy during long sessions"
```

**您将获得：**
- 针对不同职业的推荐
- 根据个人状况定制的锻炼建议
- 基于研究的个性化休息间隔
- 与工作方法（如 Pomodoro 技术）的集成

### 多平台同步

**适用于多设备用户：**
```
"Generate scripts for Linux work machine and Windows home PC"
```

**您将获得：**
- 所有平台上的休息间隔一致
- 一致的锻炼计划
- 两种平台上的通知风格统一
- 简单的设置流程

### 团队/办公室部署

**适用于 IT 管理员：**
```
"Create a company-wide break reminder script for Ubuntu 22.04"
"Generate Windows script for deployment via Group Policy"
```

**您将获得：**
- 无声安装
- 集中式配置
- 部署文档
- 员工使用指南

---

## 13. 建立健康习惯的建议

### 第 1 周：仅执行 20-20-20 规则**
- 专注于眼部休息
- 养成基本习惯
- 设置手机定时器作为备用提醒

### 第 2 周：添加短暂休息**
- 每 30-60 分钟休息 2 分钟
- 逐渐适应休息习惯

### 第 3 周：添加拉伸休息**
- 每 90 分钟休息 5 分钟
- 学习各种锻炼方法

### 第 4 周：全面锻炼计划**
- 结合所有类型的休息
- 使休息成为工作流程的一部分
- 逐渐适应这种习惯

### 保持动力
- 用日历标记休息时间
- 注意身体改善（如疼痛减轻、注意力提高）
- 与他人一起休息
- 根据实际情况调整时间表
- 记住：预防比治疗更容易

### 与工作的结合

**使用 Pomodoro 技术的用户：**
- 在 Pomodoro 工作周期中加入短暂锻炼
- 每 25 分钟工作后休息 5 分钟，适合进行 2 分钟的恢复
- 每完成 4 个 Pomodoro 循环后进行 10 分钟的全面锻炼

**会议较多的日子：**
- 将脚本设置为“仅在工作时间”模式
- 重要会议期间暂停脚本
- 会议结束后恢复使用
- 会议间隙也进行休息

### 深度工作期间：
- 减少休息频率（但不要完全取消休息）
- 每 20 分钟仍需进行眼部休息
- 每 2 小时进行较长的休息

---

## 如何使用本工具

### 交互式模式：
- “我已经编程 3 小时了，应该做哪些锻炼？”
- “我的眼睛很疼，该怎么办？”
- “展示一个 30 秒的桌面伸展动作”
- “我的脖子疼，应该怎么做？”

### 脚本生成模式：
- “生成我的自定义提醒脚本”
- “为我的工作方式制定休息时间表”
- “提供脚本的安装说明”
- “如何让脚本在系统启动时自动运行？”

### 学习模式：
- “解释 20-20-20 规则”
- “为什么需要休息？”
- “应该如何设置我的工作环境？”
- “重复性劳损的警告信号有哪些？”

---

**您的健康是最宝贵的财富。今天的小休息可以预防未来的大问题。让 ErgoCare Coach 帮助您养成可持续的健康习惯！**

👁️ “保护好您的眼睛——它们是你唯一的一对眼睛。”
🦴 “20 年后，您的脊柱会感谢您现在的努力。”
💪 “预防胜于治疗。每一次。”

🔔 **准备开始了吗？现在就请求您的自定义休息提醒脚本吧！** 🔔