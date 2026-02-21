---
name: skill-creator
description: "根据构建 workspace-analyzer 项目中的经验，创建或更新 AgentSkills。这些技能可用于设计、组织、打包、测试以及发布相关内容。其中包含了我们总结的最佳实践、注意事项以及发布工作流程。"
version: "1.0.0"
metadata:
  {"openclaw":{"emoji":"🛠️","requires":{"bins":["python3"]}, "tags":["skill", "creation", "development", "pipeline"]}}
---
# 技能创建器（增强版）

> “从想法到发布的技能——我们所有的经验都在这里。”

本文档将指导您如何根据我们构建 `workspace-analyzer` 的经验来创建新的技能。

---

## 我们的技能创建流程

**工作流程：**
1. 使用 `skill-creator` 获取创建技能的指导。
2. 构建技能（`workspace-analyzer` 就是一个示例结果）。
3. 从构建过程中吸取经验教训。
4. 基于这些经验改进 `skill-creator`。
5. 未来的技能会更加完善！

### 示例：`workspace-analyzer`

`workspace-analyzer` 是在使用 `skill-creator` 的指导下创建的。从构建过程中获得的经验已被反馈到 `skill-creator` 中，使其更加完善。

---

### 第1阶段：定义问题与成功标准

**在编写代码之前，请回答以下问题：**

| 问题 | 重要性 |
|----------|---------------|
| 它要解决什么问题？ | 明确的目标 |
| 它是为谁设计的？ | 代理（agent）还是人类用户？ |
| 什么让它具有动态性？ | 它如何适应不同的环境？ |
| 它绝对不能做什么？ | 安全/隐私方面的限制 |

**成功标准模板：**
```
1. [Dynamic] Works for any OpenClaw workspace
2. [Safe] No sensitive info exposed
3. [Documented] Clear purpose and usage
4. [Agent-focused] Outputs JSON, agent decides
```

---

### 第2阶段：构建技能结构

```
skill-name/
├── SKILL.md              ← Documentation (required)
├── scripts/
│   └── main.py          ← Main logic
├── references/          ← Detailed docs (optional)
│   └── guide.md
└── tests/               ← Test cases (optional)
    └── test_main.py
```

---

### 第3阶段：实现核心逻辑

**我们的方法（基于 `workspace-analyzer`）：**

1. **文件发现** - 遍历目录，收集文件。
2. **模式检测** - 动态地识别核心文件。
3. **内容分析** - 统计文件行数、章节数量及链接信息。
4. **问题检测** - 检查文件是否存在冗余、孤立文件或重复文件。
5. **生成建议** - 以 JSON 格式提供可执行的操作建议。

**关键经验：** 脚本进行分析 → 代理根据分析结果做出决策 → 代理执行相应的操作。

---

### 第4阶段：测试协议

**测试1：准确性**
```bash
python3 skills/workspace-analyzer/scripts/analyzer.py --output test.json
# Verify counts manually
ls *.md | wc -l
wc -l OPERATING.md
```

**测试2：误报处理**
- 在实际工作空间中运行脚本。
- 检查：失效的链接是否真实存在？
- 检查：重复文件是否会造成问题？
- 检查：文件冗余是否属于正常现象？

**测试3：可执行性**
- 代理能否根据建议采取行动？
- 输出是否足够清晰？
- 代理是否需要更多上下文信息？

---

### 第5阶段：文档编写

**必须包含的章节：**
1. **概述** - 技能的功能。
2. **使用方法** - 如何运行该技能。
3. **输出结果** - 对 JSON 格式的解释。
4. **功能说明** - 技能能检测到什么内容。
5. **集成方式** - 如何将其与 `heartbeat` 服务集成。
6. **安全性** - 技能的局限性（不能做什么）。
7. **技能关联** - 相关技能的链接。

---

## 做与不做

### ✅ 应该做的
| 动作 | 原因 |
|----|-----|
| 从明确的成功标准开始** | 有助于保持专注。 |
| 使技能具有动态性** | 适用于任何工作空间。 |
**在实际数据上测试** | 可以及早发现潜在问题。 |
**边编写代码边记录文档** | 未来的自己会感谢你。 |
| 保持 `SKILL.md` 文件长度在500行以内** | 便于阅读和理解。 |
**采用渐进式展示信息的方式** | 根据需要加载详细信息。 |
**添加技能关联链接** | 有助于用户发现其他相关技能。 |

### ❌ 不应该做的
| 动作 | 原因 |
|-------|-----|
**硬编码文件路径** | 可能导致在其他工作空间中出现问题。 |
**暴露敏感信息或API密钥** | 存在安全风险。 |
**未经审查就自动修复问题** | 可能引发错误。 |
**跳过测试** | 可能导致错误发生。 |
**编写冗长的代码** | 难以维护。 |
**忽略误报处理** | 会降低代理的信任度。 |

---

## 经验总结

### 1. 针对不同类型的文件设置不同的阈值
不同的文件类型需要不同的处理标准：
```python
THRESHOLDS = {
    "kai_core": {"bloat_warning": 400, "bloat_critical": 600},
    "skills": {"bloat_warning": 600, "bloat_critical": 1000},
    "memory": {"bloat_warning": 500, "bloat_critical": 800}
}
```

### 2. 动态模式检测
根据文件的位置来识别文件，而不是使用硬编码的文件名：
```python
# Instead of: if filename == "SOUL.md"
# Use: if "/" not in filename and filename.endswith(".md")
```

### 3. 误报处理
记录那些看似有问题但实际上并非问题的情况：
- 链接到其他技能（如 `[[blogwatcher]]`）的链接是有效的！
- 大型的参考文档也是正常的。
- 代理使用的模板文件也是预期的行为。

### 4. 可执行的输出结果
每个建议都应该包含具体的操作指导：
```json
{
  "action": "REVIEW_BLOAT",
  "file": "OPERATING.md",
  "reason": "503 lines - consider splitting",
  "severity": "WARN",
  "category": "kai_core"
}
```

---

## 发布指南

### 发布前的检查清单
- [ ] `SKILL.md` 文件的所有章节都已填写完整。
- [ ] 脚本运行无误。
- [ ] 在实际工作空间中的测试通过。
- [ ] 误报情况已记录在文档中。
- [ ] 输出中不包含任何敏感信息。
- [ ] 技能关联已添加到技能目录中。
- [ ] 如果有 `README.md` 文件，已进行清理。
- [ ] 文档的开头部分已包含版本信息。

### 发布步骤
```bash
# 1. Verify skill structure
ls -la skills/[skill-name]/

# 2. Test the script
python3 skills/[skill-name]/scripts/main.py

# 3. Check for sensitive data
grep -r "sk-\|ghp_\|eyJ" skills/[skill-name]/

# 4. Publish (if using ClawHub)
npx clawhub publish skills/[skill-name]/
```

---

## 常见错误

### 1. 硬编码的工作空间路径
**错误示例：`root = "/home/zendenho/.openclaw/workspace"`
**正确示例：`root = os.path.expanduser("~/.openclaw/workspace")`

### 2. 缺少错误处理
**错误示例：`with open(file) as f: return f.read()`
**正确示例：**
```python
try:
    with open(file, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()
except Exception as e:
    return {"error": str(e)}
```

### 3. 未处理误报
**错误示例：** 将所有大型文件都标记为冗余文件。
**正确示例：** 根据文件类型设置阈值，并提供相应的文档说明。

### 4. 代码结构混乱
**错误示例：** 生成一个庞大的 JSON 文件。
**正确示例：** 采用结构化的输出格式，包括章节划分和推荐内容。

---

## 与 `Heartbeat` 服务的集成

将技能的执行逻辑集成到维护流程中：
```markdown
## X. Run Analysis Skills

### Workspace Analyzer
python3 skills/workspace-analyzer/scripts/analyzer.py --output /tmp/analysis.json
# Review recommendations

### [Your New Skill]
python3 skills/[your-skill]/scripts/main.py --output /tmp/your-analysis.json
# Review recommendations
```

---

## 相关技能
- [[workspace-analyzer]] - 我们构建的示例技能。
- [[qmd]] - 用于内存管理。
- [[mcporter]] - 用于与 MCP 服务器集成。

---

## 参考资料

如需详细指导，请参阅：
- `skills/workspace-analyzer/SKILL_CREATION_GUIDE.md` - 我们如何使用本指南构建 `workspace-analyzer` 的文档。
- 官方的 `OpenClaw skill-creator` 模块（可在 npm 中找到）。

---

## 示例输出

`workspace-analyzer` 技能就是根据本指南创建的。这展示了 `skill-creator` 的强大功能！

---

## 更新日志

### v1.1 (2026-02-21)
- 加入了我们在构建 `workspace-analyzer` 过程中获得的经验。
- 添加了实际使用中的注意事项。
- 添加了发布前的检查清单。
- 添加了常见错误的说明。

### v1.0 (2026-02-21)
- 基于官方的 `skill-creator` 模块初步开发。

---

*增强版：2026-02-21*