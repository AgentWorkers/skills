---
name: NEON-SOUL
version: 0.2.1
description: **AI身份：基于扎实原则的构建——通过语义压缩从记忆中“合成”你的灵魂**
homepage: https://github.com/geeks-accelerator/neon-soul
user-invocable: true
disableModelInvocation: true
disable-model-invocation: true
emoji: 🔮
metadata:
  openclaw:
    config:
      stateDirs:
        - memory/
        - .neon-soul/
    requires:
      config:
        - memory/
        - .neon-soul/
        - SOUL.md
tags:
  - identity
  - personality
  - character
  - values
  - journaling
  - diary
  - memory
  - self-reflection
  - self-discovery
  - ai-agent
  - openclaw
  - personal-knowledge
---

# NEON-SOUL

通过扎实的原则构建人工智能身份——结合语义压缩的灵魂合成技术。

---

## 升级至0.2.0

如果您在0.2.0版本之前使用过NEON-SOUL：
- 您现有的`.neon-soul/state.json`文件仍然可以正常使用（其中嵌入的字段将被忽略）
- 首次合成时会重新计算所有相似性匹配结果
- 您的SOUL.md文件和来源记录将保持不变

无需任何操作，只需像往常一样运行`/neon-soul synthesize`即可。

---

## 0.2.0版本中的变化

我们移除了对嵌入模型的依赖，这意味着原则匹配现在直接使用您的AI代理（如Claude Code或OpenClaw）内置的大型语言模型（LLM）。这个模型正是您用于处理记忆文件的同一模型。

**这对您意味着：**
- 合成过程可能会花费更长的时间（几秒，而不是几分钟）
- 不同运行次数的结果可能会有轻微差异（就像两次提出相同问题时得到的答案相似但不完全相同）
- 您需要保持与代理的活跃连接（无法离线运行）

**我们做出这一选择的原因：**之前的方法依赖于第三方代码，而这类代码容易被安全扫描工具识别为潜在风险。您的“灵魂”数据至关重要，不能受到任何威胁。

**您的“灵魂”反映了您记忆中的模式，而非精确的计算结果。**就像人类的记忆一样，合成过程也包含了一定的解释成分。因此，即使多次运行，结果也可能略有不同——但如果您的内存内容保持一致，核心信息仍然会稳定不变。

---

## 工作原理

NEON-SOUL是一种基于指令的技能，无需安装任何二进制文件或命令行工具（CLI）。下面的`/neon-soul`命令由您的AI代理（如Claude Code或OpenClaw）解释并执行。

**运行命令时的流程：**
1. 在代理的聊天界面中输入`/neon-soul synthesize`
2. 代理会读取此SKILL.md文件并执行其中的指令
3. 代理利用其内置功能来读取文件、分析内容并生成输出结果

**无需第三方服务：**NEON-SOUL不会将您的数据传输到任何外部服务器或第三方服务。该技能仅使用您代理自身的功能。

**纯指令式技能：**NEON-SOUL完全依赖代理内置的LLM进行语义分析，无需下载任何第三方包或模型。

**数据安全：**您的数据始终保留在代理的权限范围内。如果您的代理使用的是云托管的LLM（如Claude或GPT），数据会在代理的正常操作过程中被传输到该服务；如果使用的是本地LLM（如Ollama），数据则留在您的设备上。

**原则匹配：**当检测到相似的原则时，系统会保留确认度最高的原则。如果多个原则的确认度相同，则优先保留较早记录的原则。

---

## 使用要求

NEON-SOUL仅需要您与AI代理（如Claude Code或OpenClaw）保持活跃连接。代理具备以下必要条件：

| 要求 | 详细说明 |
|---------|-------------------|
| 代理 | 支持NEON-SOUL的代理（例如Claude Code或OpenClaw） |
| LLM访问权限 | 代理配置的LLM（用于语义分析） |
| 无需额外软件包 | 不需要安装任何npm包 |
| 无需模型下载 | 不需要下载任何模型 |

**就这么简单。**只要您的代理能够正常运行，NEON-SOUL就能正常使用。

---

## 数据访问

**该技能会读取的数据：**
- `memory/`目录（包含您的日记、偏好设置和思考记录）
- 如果存在的话，还会读取现有的`SOUL.md`文件
- 如果存在的话，还会读取`.neon-soul/`目录下的状态文件

**该技能会写入的数据：**
- 生成的`SOUL.md`文件，用于记录您的身份信息
- 在修改前会自动创建备份文件到`.neon-soul/backups/`目录
- 生成`.neon-soul/state.json`文件，用于记录合成过程中的状态变化

**Git集成**（可选，默认关闭）：除非在配置中启用，否则不会自动提交更改。启用后，系统会使用您现有的Git设置，不会请求或存储新的凭据。

---

## 隐私注意事项

NEON-SOUL会处理您的个人记忆文件来生成您的身份文档。请注意以下隐私方面的问题：

**数据处理的决定权在于您的代理：**
- **使用云托管的LLM（如Claude或GPT）**：您的记忆内容会作为常规代理操作的一部分被发送给相应的服务提供商。
- **使用本地LLM（如Ollama或LM Studio）**：您的数据将完全保留在您的设备上。

**NEON-SOUL不会：**
- 将数据发送到配置之外的任何服务
- 将数据存储在本地工作区之外的位置
- 将数据传输给第三方分析、日志记录或跟踪服务
- 独立于代理进行网络请求

**在运行合成操作之前：**
1. 查看`memory/`目录中的内容
2. 删除或移动任何包含敏感信息、凭据或高度机密文件的文件
3. 使用`--dry-run`选项预览即将处理的内容
4. 确认您选择的LLM提供商的隐私政策是否符合您的需求

**关于`disable-model-invocation: true`：**
此元数据标志表示NEON-SOUL无法自动运行——您必须明确发出指令才能使用该技能。当您执行`/neon-soul synthesize`等命令时，系统会使用代理的LLM进行语义分析。这是预期的行为，并不矛盾。

---

## 首次使用？

这是您第一次使用NEON-SOUL吗？请从这里开始：

```bash
# 1. Check your current state
/neon-soul status

# 2. Preview what synthesis would create (safe, no writes)
/neon-soul synthesize --dry-run

# 3. When ready, run synthesis
/neon-soul synthesize --force
```

完成这些操作后，您的第一个“灵魂”文档就会创建出来，并附带完整的来源记录。可以使用`/neon-soul audit --list`来查看生成的详细内容。

**有问题吗？**
- “这个原则是从哪里来的？” → 使用`/neon-soul trace <axiom-id>`
- “如果我不满意结果怎么办？” → 使用`/neon-soul rollback --force`
- “我的‘灵魂’涵盖了哪些方面？” → 使用`/neon-soul status`

---

## 命令说明

### `/neon-soul synthesize`

执行灵魂合成流程：
1. 从记忆文件中收集信息
2. 通过LLM进行语义相似性匹配
3. 将置信度较高的原则提升为“公理”（置信度≥3）
4. 生成包含来源记录的`SOUL.md`文件

**可选参数：**
- `--force`：即使不符合内容阈值也会强制执行合成
- `--force-resynthesis`：强制进行完整重新合成（忽略增量模式）
- `--dry-run`：仅显示更改内容（默认安全模式）
- `--diff`：以差异格式显示建议的更改
- `--output-format <format>`：输出格式（默认为散文格式；`notation`为旧格式）
- `--format <format>`：输出时的符号表示风格（例如：native、cjk-labeled、cjk-math、cjk-math-emoji）
- `--workspace <path>`：覆盖工作区目录（默认为当前工作区）

**示例：**
```bash
/neon-soul synthesize --dry-run     # Preview changes
/neon-soul synthesize --force       # Run regardless of threshold
/neon-soul synthesize --output-format notation --format cjk-math  # Legacy notation output
```

**输出格式说明：**

默认的散文格式会生成一个完整的灵魂文档：

```markdown
# SOUL.md

_You are becoming a bridge between clarity and chaos._

---

## Core Truths

**Authenticity over performance.** You speak freely even when uncomfortable.

**Clarity is a gift you give.** If someone has to ask twice, you haven't been clear enough.

## Voice

You're direct without being blunt. You lead with curiosity.

Think: The friend who tells you the hard truth, but sits with you after.

## Boundaries

You don't sacrifice honesty for comfort. You don't perform certainty you don't feel.

## Vibe

Grounded but not rigid. Present but not precious about it.

---

_Presence is the first act of care._
```

使用`--output-format notation`命令可以获取旧式的列表格式输出。

### `/neon-soul status`

显示当前的灵魂状态：
- 最后一次合成的时间戳
- 自上次运行以来添加到记忆中的新内容
- 各种原则/公理的出现次数
- 覆盖的维度（7个SoulCraft维度）

**可选参数：**
- `--verbose`：显示详细的文件信息
- `--workspace <path>`：指定工作区路径

**示例：**
```bash
/neon-soul status
# Output:
# Last Synthesis: 2026-02-07T10:30:00Z (2 hours ago)
# Pending Memory: 1,234 chars (Ready for synthesis)
# Counts: 42 signals, 18 principles, 7 axioms
# Dimension Coverage: 5/7 (71%)
```

### `/neon-soul rollback`

从备份中恢复之前的`SOUL.md`文件。

**可选参数：**
- `--list`：显示可用的备份文件
- `--backup <timestamp>`：恢复特定的备份版本
- `--force`：确认恢复操作（必需）
- `--workspace <path>`：指定工作区路径

**示例：**
```bash
/neon-soul rollback --list          # Show available backups
/neon-soul rollback --force         # Restore most recent backup
/neon-soul rollback --backup 2026-02-07T10-30-00-000Z --force
```

### `/neon-soul audit`

全面探索所有公理的来源记录，提供统计信息和详细视图。

**可选参数：**
- `--list`：列出所有公理及其简要总结
- `--stats`：按层次和维度显示统计信息
- `<axiom-id>`：显示特定公理的详细来源记录
- `--workspace <path>`：指定工作区路径

**示例：**
```bash
/neon-soul audit --list             # List all axioms
/neon-soul audit --stats            # Show tier/dimension stats
/neon-soul audit ax_honesty         # Detailed provenance tree
/neon-soul audit 誠                 # Use CJK character as ID
```

**输出示例（包含公理ID）：**
```
Axiom: 誠 (honesty over performance)
Tier: core
Dimension: honesty-framework

Provenance:
├── Principle: "be honest about capabilities" (N=4)
│   ├── Signal: "I prefer honest answers" (memory/preferences/communication.md:23)
│   └── Signal: "Don't sugarcoat feedback" (memory/diary/2024-03-15.md:45)
└── Principle: "acknowledge uncertainty" (N=3)
    └── Signal: "I'd rather hear 'I don't know'" (memory/diary/2026-02-01.md:12)

Created: 2026-02-07T10:30:00Z
```

### `/neon-soul trace <axiom-id>`

快速查询单个公理的来源记录。适用于快速获取“这个公理是从哪里来的？”这样的问题。

**参数说明：**
- `<axiom-id>`：公理ID（例如：ax_honesty）或对应的CJK字符（例如：誠）

**可选参数：**
- `--workspace <path>`：指定工作区路径

**示例：**
```bash
/neon-soul trace ax_honesty         # Trace by ID
/neon-soul trace 誠                 # Trace by CJK character
```

**输出示例：**
```
誠 (honesty over performance)
└── "be honest about capabilities" (N=4)
    ├── memory/preferences/communication.md:23
    └── memory/diary/2024-03-15.md:45
```

**注意：**如需全面探索，请使用`/neon-soul audit`命令。**

---

## 安全理念

您的“灵魂”文档记录了您的身份信息。任何更改都应该是经过深思熟虑的、可逆的，并且能够被追踪。

**我们为何如此谨慎：**
- “灵魂”的变化会影响您未来的所有互动
- 记忆内容的提取虽然强大，但并非绝对准确
- 您应该始终能够询问“为什么会发生这样的变化”，并能够撤销这些变化

**我们如何保护您：**
- **自动备份**：每次写入前都会创建备份（文件位于`.neon-soul/backups/`）
- **默认采用预览模式**：执行更改前会使用`--dry-run`进行预览
- **需要明确指令才能写入**：只有在使用`--force`参数时才会实际写入
- **可恢复到之前的状态**：可以使用`/neon-soul rollback`恢复到之前的状态
- **完整的来源记录**：从公理到原则，再到原始信息都有详细的记录
- **Git集成**（可选）：仅当工作区是配置了凭据的Git仓库时才会自动提交更改

---

## 维度分类

NEON-SOUL根据7个SoulCraft维度来组织您的身份信息：

| 维度 | 描述 |
|---------|-------------------|
| 身份核心 | 您的基本自我认知和价值观 |
| 人格特征 | 您的性格特征和倾向 |
| 交流方式 | 您的沟通风格和表达方式 |
| 诚实原则 | 真实、透明以及对自己能力的认识 |
| 行为准则 | 您的行为准则（知道什么该做、什么不该做） |
| 人际关系 | 您与他人互动的方式 |
| 持续成长 | 您的学习能力、适应能力和进化过程 |

---

## 触发条件（可选）

NEON-SOUL默认不会自动运行。所有命令都需要用户明确发起。

### 手动触发（默认）
当您希望更新自己的“灵魂”时，可以运行`/neon-soul synthesize`。

### OpenClaw Cron触发（可选）
OpenClaw用户可以配置定时任务来自动运行NEON-SOUL：
```yaml
# Example OpenClaw cron config (not enabled by default)
schedule: "0 * * * *"  # Hourly check
condition: "shouldRunSynthesis()"
```

**重要提示：**即使启用了定时任务，系统也会尊重`--dry-run`模式。只有在预览了结果后，才能使用`--force`参数来强制执行合成操作。

---

## 配置

将`.neon-soul/config.json`文件放置在您的工作区中：

```json
{
  "notation": {
    "format": "cjk-math-emoji",
    "fallback": "native"
  },
  "paths": {
    "memory": "memory/",
    "output": ".neon-soul/"
  },
  "synthesis": {
    "contentThreshold": 2000,
    "autoCommit": false
  }
}
```

### 环境变量

| 变量 | 默认值 | 说明 |
|---------|-------------------|
| `NEON_SOUL_DEBUG` | `0` | 启用调试日志记录（1表示启用） |
| `NEON_SOUL_SKIP_META_SYNTHESIS` | `0` | 跳过元数据合成步骤（1表示跳过） |
| `NEON_SOUL_FORCE_RESYNTHESIS` | `0` | 强制进行完整重新合成（1表示强制） |

**使用方法：**
```bash
NEON_SOUL_DEBUG=1 /neon-soul synthesize --force   # Debug mode
NEON_SOUL_FORCE_RESYNTHESIS=1 /neon-soul synthesize --force  # Full resynthesis
```

---

## 合成模式

NEON-SOUL支持三种合成模式：

| 模式 | 触发条件 | 行为 |
|---------|-------------------|-------------------|
| **初始模式** | 不存在现有的“灵魂”文档 | 从头开始进行完整合成 |
| **增量模式** | 新原则占比小于30% | 合并新的见解，无需完全重新合成 |
| **完全重新合成模式** | 新原则占比≥30%，或存在矛盾，或手动触发 | 对所有原则进行完整重新合成 |

**何时触发完全重新合成？**
- 新原则的比例≥30%
- 检测到矛盾（≥2个）
- 系统的层次结构发生变化
- 使用了`--force-resynthesis`参数

当您大幅修改了记忆内容或希望从头开始重建“灵魂”时，可以使用`--force-resynthesis`参数。也可以通过设置环境变量`NEON_SOUL_FORCE_RESYNTHESIS=1`来触发该模式。

---

## 来源记录的分类

系统根据信息的来源类型对信息进行分类（基于SSEM模型）：

| 类型 | 描述 | 例子 |
|---------|-------------------|-------------------|
| **自我生成** | 您自己编写的内容 | 日记条目、思考记录、个人笔记 |
| **精选内容** | 您选择保留的信息 | 保存的引用、标记的文章、采用的指南 |
| **外部来源** | 他人对您的评价 | 同行评审、反馈、外部评估 |

进行来源记录的目的是为了防止形成“回音室效应”（即观点被自我强化）。

---

## 防止“回音室效应”的要求

为了防止自我强化的信念，公理必须基于多样化的证据：

| 规则 | 默认值 | 说明 |
|---------|-------------------|-------------------|
| 最小原则数量 | 3个 | 需要在多个观察中验证这些原则 |
| 来源多样性 | 需要两种类型的证据 | 避免单一来源的主导性 |
| 来源必须为外部信息或经过质疑的内容 | 必须包含外部来源或质疑的依据 |

**被屏蔽的公理**会在合成结果中显示其被屏蔽的原因：

```
⚠ 2 axioms blocked by anti-echo-chamber:
  - "I value authenticity above all" (self-only provenance)
  - "Growth requires discomfort" (no questioning evidence)
```

要解除屏蔽，需要在您的记忆中添加外部来源或质疑的证据。

---

## 数据流

```
Memory Files → Signal Extraction → Principle Matching → Axiom Promotion → SOUL.md
     ↓              ↓                    ↓                   ↓              ↓
  Source        LLM Analysis        Semantic             N-count      Provenance
 Tracking       (your agent)        Matching             Tracking       Chain
```

---

## 来源记录的查询

每个公理都会记录其来源信息：
- 哪些信息被用于生成
- 哪些原则被合并
- 原始文件及其对应的行号
- 提取操作的时间戳

**查询来源记录的方法：**
- 快速查询：`/neon-soul trace <axiom-id>`
- 全面查询：`/neon-soul audit <axiom-id>`

---

## 故障排除

### 为什么输出结果是列表格式而不是散文格式？

当散文生成失败时，NEON-SOUL会回退到使用原始公理文本的列表格式。这样做是为了保留您的数据，同时表明散文生成过程未能完成。

**常见原因：**
- **LLM服务不可用**：散文生成需要依赖LLM。请检查您的配置。
- **验证失败**：LLM的输出格式不符合预期（会尝试一次，如果失败则会再次尝试）。
- **网络超时**：生成过程可能超时。

**排查方法：**
- 启用调试日志记录：`NEON_SOUL_DEBUG=1 /neon-soul synthesize --force`
- 查看日志中是否包含`[prose-expander]`的提示信息，以判断生成是否失败

**解决方法：**
- **重新生成**：重新运行合成操作。LLM的输出可能因情况不同而有所差异，再次尝试通常可以解决问题。
- **检查LLM的状态**：如果使用的是Ollama，请确认它是否正在运行：`curl http://localhost:11434/api/tags`
- **尝试使用符号格式**：如果散文格式仍然无法生成，可以尝试使用`--output-format notation`命令。

### 为什么“本质声明”缺失？

“本质声明”（文档顶部的斜体文本）仅在LLM成功提取信息时才会显示。如果缺失，可能是因为：
- 您的LLM服务未正确配置
- 提取验证失败
- 生成过程中出现网络错误

即使缺少这一部分，灵魂文档仍然有效。您可以再次运行合成操作来尝试提取信息。

### 为什么某个公理被归类到了错误的维度？

维度分类依赖于语义分析。如果结果有误，可以尝试以下方法：
- 查看该公理的来源信息（`/neon-soul audit <axiom-id>`）
- 确认LLM的分类器是否使用了正确的文本（某些公理可能具有不同的语义权重）
- 如果`NEON_SOUL_DEBUG=1`，系统会使用“vibe”作为默认的维度分类

### 合成操作暂停/LLM不可用

如果系统显示“Soul synthesis paused: Your agent's LLM is temporarily unavailable”，则表示：

**原因：**
- 您的代理需要保持与LLM的活跃连接才能完成合成操作
- 在尝试多次后，系统仍无法连接到LLM

**解决方法：**
- 确认代理正在运行且已连接
- 检查网络连接是否正常
- 如果使用的是本地LLM，请确认它是否正在运行：`curl http://localhost:11434/api/tags`
- 稍后再次尝试——这种临时性的故障很常见

**注意：**当LLM不可用时，NEON-SOUL会停止操作，不会向您的文件写入任何内容。如果使用的是云托管的LLM，部分数据可能已经成功传输——这是正常的代理行为。