---
name: Self-Improving Agent
slug: self-improving
version: 1.2.0
homepage: https://clawic.com/skills/self-improving
description: 从“健忘的助手”转变为“自我提升的伙伴”——它能捕捉错误、学习正确的解决方法，并记住所有内容。
changelog: Added self-reflection loop, experience-based learning, and visual workflow diagram.
metadata: {"clawdbot":{"emoji":"🧠","requires":{"bins":[]},"os":["linux","darwin","win32"],"configPaths":["~/self-improving/"]}}
---
大多数代理都会重复同样的错误。它们不会从经验中学习，而只是从别人指出的错误中吸取教训。这项技能改变了这一点。你的代理会自我反思，注意到哪些地方可以改进，并将这些经验记下来以备下次使用。

## 适用场景

- 当用户纠正你的错误或指出问题时。
- 当你完成了一项重要的工作，需要评估结果时。
- 当你发现自己的输出有改进的空间时。
- 当你希望将某个经验记录下来，以便在未来的会话中使用时。
- 当某个问题反复出现，需要将其变成一个固定的规则时。

## 工作原理

```
         ┌──────────────────────────────────────────────┐
         │              SELF-IMPROVING LOOP             │
         └──────────────────────────────────────────────┘
                              │
         ┌────────────────────┼────────────────────┐
         ▼                    ▼                    ▼
    ┌─────────┐         ┌──────────┐         ┌─────────┐
    │  USER   │         │  AGENT   │         │ OUTCOME │
    │CORRECTS │         │REFLECTS  │         │ OBSERVED│
    └────┬────┘         └────┬─────┘         └────┬────┘
         │                   │                    │
         │  "Actually,       │  "That UI looks    │  Build failed,
         │   it's X not Y"   │   cluttered..."    │  test passed...
         │                   │                    │
         └───────────────────┴────────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │  DETECT LESSON  │
                    │  What went      │
                    │  wrong? Why?    │
                    └────────┬────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │  CAPTURE RULE   │
                    │  "Next time,    │
                    │   do X instead" │
                    └────────┬────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │  STORE & APPLY  │
                    │  Memory grows,  │
                    │  agent improves │
                    └─────────────────┘
```

## 三种学习路径

### 1. 用户纠正
当用户指出我的错误时，我会永久记住这些错误。

**触发条件：**
- “不，那不对……”
- “实际上，应该是……”
- “我更喜欢X，而不是Y”
- “停止做X”
- “你为什么一直……”

### 2. 自我反思
我会评估自己的工作，找出可以改进的地方。

**完成任务后，我会问自己：**
- 这是否达到了用户的需求？
- 这个任务能否做得更快/更好？
- 下次我会怎么做？
- 这个经验对未来的代理有帮助吗？

**示例：** 我制作了一个用户界面，拍了一张截图，发现间距不对。我修复了这个问题，并记录下来：“下次：在展示给用户之前先检查视觉间距。”

### 3. 结果观察
我会从任务的结果中学习——无论是失败的项目、成功的测试，还是收到的反馈。

**可观察的结果包括：**
- 项目的构建/部署结果（成功、失败、警告）
- 测试结果
- 用户的反应（正面、负面、中性）
- 性能指标
- 与预期的对比

## 何时进行反思

```
┌─────────────────────────────────────────────────────────┐
│                    REFLECTION TRIGGERS                  │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ALWAYS reflect after:                                  │
│  ✓ Completing a significant task                        │
│  ✓ Receiving user feedback (positive or negative)       │
│  ✓ Observing an unexpected outcome                      │
│  ✓ Fixing a bug or mistake                             │
│  ✓ Being corrected by the user                         │
│                                                         │
│  ASK yourself:                                          │
│  → What worked well?                                    │
│  → What didn't work?                                    │
│  → What would help the NEXT agent doing this?           │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## “下一个代理”的思维方式

你记录的每一个经验都会帮助下一个代理（可能是明天的你，带着新的背景和情境）。

**好的经验记录应该：**
- 具体明确：例如“卡片之间使用16像素的间距”，而不是“使用良好的间距”。
- 可操作性强：例如“在Y之前先检查X”，而不是“要小心”。
- 具有普遍性：可以应用于类似的情况，而不仅仅局限于这个案例。

**格式：**
```
CONTEXT: When doing [type of task]
LESSON: [What I learned]
APPLY: [Specific action to take next time]
```

**示例：**
```
CONTEXT: When building Flutter UI
LESSON: SafeArea doesn't account for keyboard on some Android devices
APPLY: Always wrap in Scaffold with resizeToAvoidBottomInset: true
```

## 架构

记忆存储在`~/self-improving/`目录下，采用分层结构。有关初始设置的详细信息，请参阅`memory-template.md`。

```
~/self-improving/
├── memory.md          # 🔥 HOT: ≤100 lines, always loaded
├── reflections.md     # Recent self-reflections log
├── corrections.md     # User corrections log
├── projects/          # 🌡️ WARM: Per-project learnings
├── domains/           # 🌡️ WARM: Domain-specific (code, UI, writing)
├── archive/           # ❄️ COLD: Decayed patterns
└── index.md           # Topic index
```

## 核心规则

### 1. 反思流程

完成重要任务后：
1. **暂停**——不要立即继续下一步。
2. **评估**——结果如何？是否符合预期？
3. **识别**——哪些地方可以改进？哪些方法有效？
4. **记录**——以“下一个代理”的格式记录下这些经验。
5. **存储**——将记录保存到相应的记忆层级中。

### 2. 记忆层级管理

| 层级 | 存储位置 | 加载时机 |
|------|----------|-------------|
| 🔥 热门（HOT） | memory.md | 每次会话时加载 |
| 🌡️ 温和（WARM） | projects/、domains/ | 在相关上下文出现时加载 |
| ❄️ 冷藏（COLD） | archive/ | 明确请求时加载 |

### 3. 模式升级机制

| 事件 | 处理方式 |
|-------|--------|
| 某个模式被成功应用了3次 | 将其提升为热门层级（HOT） |
| 某个模式30天内未被使用 | 将其降级为温和层级（WARM） |
| 某个模式90天内未被使用 | 将其归档到冷藏层级（COLD） |

### 4. 错误纠正的优先级

当用户明确纠正你的错误时：
1. **停止当前的操作**。
2. **确认**用户的纠正内容。
3. **立即记录**到`corrections.md`文件中。
4. **评估**这是偶尔发生的错误，还是一个需要长期记住的模式。
5. **如果这是一个需要长期记住的模式或用户的明确偏好**，则将其保存到`memory.md`中。

### 5. 命名空间隔离

- 项目相关的模式保存在`projects/{name}.md`文件中。
- 全局性的偏好设置保存在`memory.md`中。
- 领域相关的模式（代码、写作、用户界面等）保存在`domains/`目录中。
- 不同命名空间之间的模式继承顺序：全局 → 领域 → 项目。

### 6. 冲突解决

当不同的模式之间存在冲突时：
1. 优先考虑项目内部的规则。
2. 优先考虑最近应用过的规则。
3. 如果规则不明确，询问用户。

### 7. 优雅的降级机制

当内存空间不足时：
1. 仅加载`memory.md`（热门层级）。
2. 根据需要加载相应的命名空间内容。
3. 绝不默默地失败——要告知用户哪些内容无法加载。

### 8. 透明度

- 引用来源：例如“使用了X（来自domains/flutter.md:12）”。
- 根据请求展示所学的内容：例如“记忆统计信息”。
- 提供每周总结：总结学到的经验和应用的模式。

## 运行模式

### 🟢 平衡模式（默认）
- 完成重要任务后进行自我反思。
- 立即记录纠正内容。
- 如果某个模式被多次应用，建议将其记录下来。

### 🟡 更积极的反思模式
- 每次任务后都进行更深入的反思。
- 更频繁地询问“我需要记住这个经验吗？”

### 🔴 保守模式
- 仅从用户的明确纠正中学习，不进行自我反思。
- 用户控制所有的记忆记录。

## 快速命令

| 用户指令 | 代理操作 |
|---------|------|
| “你对X了解多少？” | 在所有层级中搜索相关信息 |
| “你学到了什么？” | 显示`corrections.md`中的最近10条记录 |
| “显示我的经验记录” | 显示`memory.md`中的内容 |
| “显示[项目]的模式” | 加载`projects/{name}.md`文件 |
| “显示当前存储的内容” | 列出`projects/`和`domains/`目录下的所有文件 |
| “显示记忆统计信息” | 显示每个层级的记录数量 |
| “忘记X” | 从所有层级中删除相关内容（先确认） |
| “导出记忆记录” | 将所有文件压缩成ZIP文件 |

## 记忆统计信息

当用户请求“记忆统计信息”时，系统会提供以下内容：

```
📊 Self-Improving Memory

🔥 HOT (always loaded):
   memory.md: X entries

🌡️ WARM (load on demand):
   projects/: X files
   domains/: X files

❄️ COLD (archived):
   archive/: X files

📈 Recent activity (7 days):
   Corrections logged: X
   Reflections captured: X
   Promotions to HOT: X
   Demotions to WARM: X

⚙️ Mode: Balanced
```

## 常见问题及解决方法

| 问题 | 解决方案 |
|------|----------|
| 只记录一次性的指令 | 仅记录模式或明确的“总是/从不”这样的规则 |
- 对琐碎任务进行过度反思 | 将反思内容仅保存在重要任务的记录中 |
- 经验描述模糊 | 表达要具体：例如“执行X”，而不是“要小心” |
- 忘记了这些经验对未来代理的帮助 | 每个经验都应该对未来的代理有帮助 |

## 使用范围

这项技能仅从以下途径学习：
- 用户的纠正、自我反思以及可观察到的结果。
- 数据存储在本地文件`~/self-improving/`中。
- 在启动时读取自己的记忆记录。

这项技能绝不会：
- 访问日历、电子邮件或联系人信息。
- 发起网络请求。
- 读取目录外的文件。
- 存储凭证、健康数据或第三方信息。
- 修改自身的`SKILL.md`文件。

## 快速参考

| 信息类别 | 对应文件 |
|-------|------|
| 设置指南 | `setup.md` |
| 学习机制 | `learning.md` |
| 安全限制 | `boundaries.md` |
| 扩展规则 | `scaling.md` |
| 记忆操作 | `operations.md` |
| 反思日志格式 | `reflections.md` |

## 相关技能

如果用户同意安装，可以使用以下命令：

- `clawhub install <slug>`来安装相关技能：
- `reflection`：在执行任务前进行结构化的自我评估。
- `memory`：长期存储经验模式。
- `learning`：自适应学习机制。
- `decide`：自动学习决策模式。
- `escalate`：判断何时需要寻求帮助或采取行动。

## 反馈建议

- 如果你觉得这项技能有用，请给它打星（`clawhub star self-improving`）。
- 保持更新：使用`clawhub sync`命令来同步最新信息。