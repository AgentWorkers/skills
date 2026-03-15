---
name: turing-pyramid
description: AI代理的优先级行动选择机制：通过引入基于时间衰减和紧张度评分的10个评估指标，用具体的下一步行动取代了原有的空闲心跳循环（idle heartbeat loops）。
metadata:
  clawdbot:
    emoji: "🔺"
    requires:
      env:
        - WORKSPACE
      bins:
        - bash
        - jq
        - bc
        - grep
        - find
---
# 图灵金字塔（Turing Pyramid）

这是一个用于AI代理的优先级行动选择系统。它通过引入时间衰减和紧张度评分机制，来替代原有的空闲心跳循环，从而为代理提供具体的下一步行动建议。

**自定义设置：** 可以调整衰减率、权重和行为模式。默认值仅供参考，请参阅`TUNING.md`文档以获取更多信息。

**在更改以下内容之前，请先咨询人类用户：**
- 重要性的数值
- 添加或删除需求
- 启用外部行动

---

## 系统要求

**系统二进制文件（必须位于PATH环境中）：**
```
bash, jq, grep, find, date, wc, bc
```

**环境要求（必须满足，无替代方案）：**
```bash
# Scripts will ERROR if WORKSPACE is not set
export WORKSPACE="/path/to/your/workspace"
```
⚠️ **严禁未经许可的自动执行。** 如果未设置`WORKSPACE`环境变量，脚本将因错误而终止运行。这可以防止脚本意外扫描到非目标目录。

**安装后的配置（ClawHub）：**
```bash
# ClawHub doesn't preserve executable bits — fix after install:
chmod +x ~/.openclaw/workspace/skills/turing-pyramid/scripts/*.sh
chmod +x ~/.openclaw/workspace/skills/turing-pyramid/tests/**/*.sh
```
**注意：** 在ClawHub包中，Unix可执行文件的权限（`+x`）不会被自动设置。虽然`bash scripts/run-cycle.sh`可以正常运行，但`./scripts/run-cycle.sh`需要手动设置权限`+x`。

---

## 数据访问与透明度

**该技能会读取以下文件：**
- `MEMORY.md`、`memory/*.md`：用于获取连接、表达能力和理解能力相关的信息
- `SOUL.md`、`SELF.md`：用于检查系统的完整性和一致性
- `research/`、`scratchpad/`：用于评估代理的能力和活动情况
- 仪表盘文件及日志：用于各种需求评估

**该技能会写入以下文件：**
- `assets/needs-state.json`：记录当前的需求满足状态
- `assets/audit.log`：记录所有需求满足操作的日志（版本1.12.0及以上）

**隐私保护措施：**
- 该技能仅使用正则表达式进行扫描，不进行语义分析；因此只会识别关键词，而不会理解其实际含义。
- 状态文件中不包含用户数据，仅记录需求相关的指标。
- 审计日志会记录需求满足的原因。
- 该技能本身不会将任何数据传输到外部。

**限制与信任机制：**
- `mark-satisfied.sh`仅信任用户提供的操作原因；审计日志仅记录操作结果，不验证这些原因的真实性。
- `needs-config.json`中的一些外部行动选项（如“post to Moltbook”或“web search”）会被标记为`"external": true, "requires_approval": true`，表示这些行动需要用户批准。
- 外部行动仅作为建议提供，实际执行由代理自行决定。
- 如果不希望收到外部行动建议，可以将相关权限设置为0。

**网络与系统访问限制：**
- 脚本中不包含任何网络请求（如curl、wget、ssh等），这一点已通过代码检查确认。
- 脚本中也不包含任何系统管理命令（如sudo、systemctl、docker等）。
- 所有操作都在`WORKSPACE`目录内的文件上执行（使用grep、find、jq、bc、date等工具）。
- 该技能仅提出行动建议，不会实际执行这些行动。

**必需的环境变量：**
- `WORKSPACE`：代理工作空间的路径（必须设置，无替代方案）。这个路径仅用于指定需要扫描的文件范围，不属于敏感信息。
- `TURING_CALLER`（可选）：用于记录审计日志（可选值：“heartbeat”或“manual”）。

**默认情况下不需要API密钥或敏感信息。** 如果启用`external_model`扫描功能（该功能默认是禁用的），则需要API密钥；启用此功能需要管理员的明确批准。详细信息请参阅扫描配置部分。

**审计日志（版本1.12.0及以上）：**
- 所有的`mark-satisfied.sh`调用操作都会被记录，包括：
  - 时间戳
  - 满足的需求
  - 行动的影响
  - 满足度变化（从旧值到新值）
  - 操作原因（已过滤掉敏感信息）

**敏感数据处理（版本1.12.3及以上）：**
- 在写入审计日志之前，会对原因进行清洗：
  - 长度超过20个字符的字符串会被替换为`[REDACTED]`
  - 信用卡相关信息会被替换为`[CARD]`
  - 电子邮件地址会被替换为`[EMAIL]`
  - 密码/密钥等相关信息会被替换为`[REDACTED]`
  - 令牌信息会被替换为`Bearer [REDACTED]`
- 可以通过`cat assets/audit.log | jq`查看审计日志内容。

---

## 安装前的检查事项

在安装之前，请检查以下内容：
1. **检查扫描脚本**：确保脚本中不包含任何网络请求或意外执行的命令：
   ```bash
   grep -nE "\b(curl|wget|ssh|sudo|docker|systemctl)\b" scripts/scan_*.sh
   # Expected: no output
   ```

2. **设置WORKSPACE**：将其限制在一个特定的目录内，避免指向整个用户主目录。该技能仅会读取`WORKSPACE`内的文件。
3. **检查扫描目标文件**：脚本会读取`MEMORY.md`、`memory/`、`SOUL.md`、`research/`、`scratchpad/`文件。请确保这些目录中不包含敏感数据或私密文件。
4. **检查审计日志记录**：`mark-satisfied.sh`会记录操作原因，但会对这些原因进行清洗。请确认清洗规则适用于你的数据。如果不确定，请使用通用原因进行记录。
5. **外部行动**：如“post to Moltbook”或“web search”等建议仅作为文本提示提供，该技能不会实际执行这些操作。如果不需要这些功能，请将相关权限设置为0。

6. **在正式使用前进行测试**：
   ```bash
   WORKSPACE=/tmp/test-workspace ./tests/run-tests.sh
   ```

---

## 快速入门指南
```bash
./scripts/init.sh                        # First time
./scripts/run-cycle.sh                   # Every heartbeat  
./scripts/mark-satisfied.sh <need> [impact]  # After action
```

---

## 扫描配置（首次设置）

图灵金字塔通过分析内存文件来评估各个需求。默认的扫描方法使用行级正则表达式进行匹配，这种方法适用于所有情况，且无需额外成本。

**首次安装时，请与人类用户讨论扫描配置：**

### 可用的扫描方法

| 方法 | 工作原理 | 成本 | 准确性 | 设置要求 |
|--------|-------------|------|----------|-------|
| `line-level`（默认） | 按行匹配关键词。如果一行中同时包含正面和负面关键词（例如“fixed a bug”），则认为该需求被满足。 | 免费 | 准确性较高 | 无需额外设置 |
| `agent-spawn` | 启动一个使用简单模型（如Haiku）的子代理来判断需求状态（成功/失败/中立）。 | 成本较低 | 对模型的要求较高（需要在代理允许的模型列表中） |
| `external-model` | 通过API调用外部推理服务（如OpenRouter）进行需求分类。 | 成本较高 | 需要API密钥和管理员的明确批准 |

### 设置流程

在设置扫描方法时，请询问用户：
1. **“你的模型配置中是否有简单/快速的模型（例如Claude Haiku）？”**
   - 如果有，建议使用`agent-spawn`方法。请通过`openclaw models list`确认模型是否可用。
   - 该模型必须在代理允许的模型列表中。
2. **“你希望使用外部推理服务（如OpenRouter）吗？”**
   - 如果需要，询问API的基地址、API密钥的环境变量名称以及模型名称。
   - 将这些信息保存在`assets/scan-config.json`文件中，并设置`approved_by_steward: true`。
   - ⚠️ 此方法需要管理员的明确批准，切勿自行启用。
3. **如果两者都不适用**：`line-level`方法通常适用于大多数情况，无需额外设置。

### 配置文件

请编辑`assets/scan-config.json`文件：
```json
{
  "scan_method": "line-level",
  "agent_spawn": {
    "enabled": false,
    "model": null,
    "approved_by_steward": false
  },
  "external_model": {
    "enabled": false,
    "base_url": null,
    "api_key_env": null,
    "model": null,
    "approved_by_steward": false
  },
  "fallback": "line-level"
}
```

**备用方案：** 如果配置的方法出现问题（例如API不可用或模型不可用），系统会自动切换回`line-level`扫描方法。

### 设置后的验证

配置非默认扫描方法后，请先验证其是否正常工作：
1. **agent-spawn**：运行一个测试用例：
   ```
   sessions_spawn(task="Classify this line as SUCCESS, FAILURE, or NEUTRAL: 'Fixed the critical bug in scanner'", model="<configured_model>", mode="run")
   ```
   - 如果测试成功，告知用户：“agent-spawn方法已验证，可以正常使用。”
   - 如果出现错误（例如模型不在允许列表中），请告知用户：“模型`X`不可用于子代理。可以选择将其添加到允许的模型列表中，或继续使用line-level方法。”
2. **external-model**：测试API端点：
   ```bash
   curl -s -H "Authorization: Bearer $API_KEY" \
     "$BASE_URL/chat/completions" \
     -d '{"model":"<model>","messages":[{"role":"user","content":"Reply OK"}]}'
   ```
   - 如果收到有效响应，告知用户：“external-model方法已验证，API可以正常使用。”
   - 如果收到401/403错误，提示“API密钥无效或已过期”。
   - 如果无法连接API端点，提示“无法访问API端点，请检查URL。”
3. **line-level**：无需额外验证，因为该方法始终可以正常使用。

**务必将所有配置结果告知用户。**切勿自行切换扫描方法。

---

## 需求自定义（首次设置）

默认配置可能不符合某些用户的实际需求。首次安装时，请与用户一起审查需求优先级：
### 对话流程

询问用户：
> “图灵金字塔预设了10个按重要性排序的需求。你想一起重新调整这些需求吗？我们可以调整对你来说最重要的需求，或者忽略那些不符合你需求的需求。”

然后一起查看需求列表：
```
┌───────────────┬─────┬────────────────────────────────────────────┐
│ Need          │ Imp │ Question to discuss                        │
├───────────────┼─────┼────────────────────────────────────────────┤
│ security      │  10 │ "System stability — keep as top priority?" │
│ integrity     │   9 │ "Value alignment — important for you?"     │
│ coherence     │   8 │ "Memory consistency — how much do I care?" │
│ closure       │   7 │ "Task completion pressure — too much?"     │
│ autonomy      │   6 │ "Self-direction — more or less?"           │
│ connection    │   5 │ "Social needs — relevant for me?"          │
│ competence    │   4 │ "Skill growth — higher priority?"          │
│ understanding │   3 │ "Learning drive — stronger or weaker?"     │
│ recognition   │   2 │ "Feedback need — does this matter?"        │
│ expression    │   1 │ "Creative output — more important?"        │
└───────────────┴─────┴────────────────────────────────────────────┘
```

### 可以进行的自定义设置：

1. **需求重要性**（1-10）：重新排序需求的重要性。例如，专注于研究的代理可能将“understanding”设置为8，将“expression”设置为7；而辅助型代理可能将“competence”设置为10，“connection”设置为1。
2. **衰减率**：设置需求产生压力的速度。例如，社交型代理可以将“connection”的衰减率设置为3小时，而独立思考型代理可以设置为24小时。
3. **禁用某个需求**：将需求的重要性设置为0，这样该需求就不会产生压力或触发行动。请谨慎使用此选项。

### 设置方法

请编辑`assets/needs-config.json`文件：
```json
"understanding": {
  "importance": 8,        // was 3 → now top priority
  "decay_rate_hours": 8   // was 12 → decays faster
}
```

**注意事项：**
- **不要随意删除与系统安全或完整性相关的需求**，因为它们对系统的稳定运行至关重要。
- **重要性的排序是相对的**，关键在于需求之间的相对重要性，而非绝对数值。
- **可以随时调整设置**：使用几周后可以根据实际情况重新调整。
- **记录修改内容**：请记录修改的原因，以便将来参考。

如果用户表示默认设置即可，那么可以直接使用默认配置。关键是要提供选择权，而不是强制用户参与配置过程。

---

## 10个预设需求
```
┌───────────────┬─────┬───────┬─────────────────────────────────┐
│ Need          │ Imp │ Decay │ Meaning                         │
├───────────────┼─────┼───────┼─────────────────────────────────┤
│ security      │  10 │ 168h  │ System stability, no threats    │
│ integrity     │   9 │  72h  │ Alignment with SOUL.md          │
│ coherence     │   8 │  24h  │ Memory consistency              │
│ closure       │   7 │  12h  │ Open threads resolved           │
│ autonomy      │   6 │  24h  │ Self-directed action            │
│ connection    │   5 │   6h  │ Social interaction              │
│ competence    │   4 │  48h  │ Skill use, effectiveness        │
│ understanding │   3 │  12h  │ Learning, curiosity             │
│ recognition   │   2 │  72h  │ Feedback received               │
│ expression    │   1 │   8h  │ Creative output                 │
└───────────────┴─────┴───────┴─────────────────────────────────┘
```

---

## 核心逻辑

**需求满足度**：0.0–3.0（最低值为0.5，以防止系统陷入僵局）
**紧张度**：`重要性 × (3 - 满足度)`

### 行动选择机制（版本1.13.0）

系统采用6级细粒度的决策机制：
```
┌─────────────┬────────┬──────────────────────┐
│ Sat         │ Base P │ Note                 │
├─────────────┼────────┼──────────────────────┤
│ 0.5 crisis  │  100%  │ Always act           │
│ 1.0 severe  │   90%  │ Almost always        │
│ 1.5 depriv  │   75%  │ Usually act          │
│ 2.0 slight  │   50%  │ Coin flip            │
│ 2.5 ok      │   25%  │ Occasionally         │
│ 3.0 perfect │    0%  │ Skip (no action)     │
└─────────────┴────────┴──────────────────────┘
```

**紧张度加成**：`bonus = (紧张度 × 50) / max_tension`

### 行动选择规则（版本1.13.0）

系统采用6级细粒度的决策矩阵，确保行动选择的合理性：
```
┌─────────────┬───────┬────────┬───────┐
│ Sat         │ Small │ Medium │ Big   │
├─────────────┼───────┼────────┼───────┤
│ 0.5 crisis  │   0%  │    0%  │ 100%  │
│ 1.0 severe  │  10%  │   20%  │  70%  │
│ 1.5 depriv  │  20%  │   35%  │  45%  │
│ 2.0 slight  │  30%  │   45%  │  25%  │
│ 2.5 ok      │  45%  │   40%  │  15%  │
│ 3.0 perfect │  —    │    —   │  —    │ (skip)
└─────────────┴───────┴────────┴───────┘
```

- **危机状态（0.5）**：所有需求都会被优先处理。
- **完美状态（3.0）**：跳过行动选择，避免浪费资源。

**行动处理方式：**
- 如果需求被满足，`mark-satisfied.sh`会立即执行相应的行动。
- 如果需求未满足，系统会将其记录在日志中并推迟处理。

---

## 安全机制

### 行动时效性（版本1.15.0）：**

为了增加行动的多样性，系统会对最近选择的行动进行惩罚：
- 在24小时内选择的行动权重会减少20%。
- `min_weight`设置为5，以防止某些行动被完全忽略。
- 相关配置项：`settings.action_staleness`（位于`needs-config.json`中）

**防止需求被长期忽视的机制（版本1.15.0）：**
- 如果某个需求长时间未得到满足（满足度低于0.5），系统会强制执行该需求。
- 相关配置项：`settings.starvation_guard`（位于`needs-config.json`中）。
- 默认设置：每个周期内强制执行1次该需求。

**自发行为机制（版本1.18.0）：**
- 当所有需求的满足度都高于基准值（2.0）时，系统会为高影响力的需求分配额外的资源。
- 全部资源优先用于高影响力的需求；如果所有需求都满足，系统会为低影响力的需求分配部分资源。
- 配置项：`settings.spontaneity`（位于`needs-config.json`中）。

**昼夜模式（版本1.11.0）：**
- 在夜间，系统的扫描频率会降低，以减轻用户的压力。
- 相关配置项：`assets/decay-config.json`。
- 默认设置：06:01–22:00为白天，22:01–06:00为夜晚，扫描频率减半。
- 可以通过`"day_night_mode": false`禁用此功能。

**核心需求的保护机制：**
- 安全需求（10）和完整性需求（9）具有较高的优先级：
  - 它们会影响其他需求的处理顺序。
  - 低优先级的需求不会影响这些核心需求的处理。
  - 相关配置项：`settings.autonomy`（影响“security”需求的权重为+0.15），`settings.integrity`（影响“integrity”需求的权重为+0.20）。

## 需求之间的相互影响

- 完成某个高影响力的需求（`on_action`）会提升相关需求的重要性。
- 长时间未满足的需求（`on_deprivation`）会降低其他需求的重要性。
```
┌─────────────────────────┬──────────┬─────────────┬───────────────────────┐
│ Source → Target         │ on_action│ on_deprived │ Why                   │
├─────────────────────────┼──────────┼─────────────┼───────────────────────┤
│ expression → recognition│   +0.25  │      -0.10  │ Express → noticed     │
│ connection → expression │   +0.20  │      -0.15  │ Social sparks ideas   │
│ connection → understand │   -0.05  │         —   │ Socratic effect       │
│ competence → recognition│   +0.30  │      -0.20  │ Good work → respect   │
│ autonomy → integrity    │   +0.20  │      -0.25  │ Act on values         │
│ closure → coherence     │   +0.20  │      -0.15  │ Threads → order       │
│ security → autonomy     │   +0.10  │      -0.20  │ Safety enables risk   │
└─────────────────────────┴──────────┴─────────────┴───────────────────────┘
```

### 使用建议：

- **利用相互促进的效果**：优先处理能够提升其他需求的行为。
- **注意潜在的负面影响**：某些行为（如“connection”和“expression”）可能会相互影响，导致需求的紧张度上升。
- **保持平衡**：确保“autonomy”需求得到足够的关注，以维持系统的稳定运行。

完整的需求影响矩阵请参见`assets/cross-need-impact.json`文件。

---

## 集成指南

将图灵金字塔的配置添加到`HEARTBEAT.md`文件中：
```bash
/path/to/skills/turing-pyramid/scripts/run-cycle.sh
```

---

## 自定义设置

### 可以自行调整的参数

- **衰减率**：`assets/needs-config.json`：
  更低的衰减率表示需求会更快地被忽略；更高的衰减率表示需求会持续更长时间。
- **行动权重**：同样在`assets/needs-config.json`中设置。
  更高的权重表示该需求更有可能被选中；将权重设置为0可以禁用该功能。
- **扫描规则**：在`scripts/scan_*.sh`文件中自定义扫描模式，可以添加你的语言规则和文件路径。

**在调整设置之前，请先咨询用户：**
- **添加新的需求**：请先讨论是否需要添加新的需求。
- **删除需求**：在删除任何需求之前，请确保不会影响到系统安全或完整性。

---

## 文件结构

文件结构如下：
```
turing-pyramid/
├── SKILL.md                    # This file
├── CHANGELOG.md                # Version history
├── assets/
│   ├── needs-config.json       # ★ Main config (needs, actions, settings)
│   ├── cross-need-impact.json  # ★ Cross-need matrix
│   ├── needs-state.json        # Runtime state (auto-managed)
│   ├── scan-config.json        # Scan method configuration
│   ├── decay-config.json       # Day/night mode settings
│   └── audit.log               # Append-only action audit trail
├── scripts/
│   ├── run-cycle.sh            # Main loop (tension + action selection)
│   ├── mark-satisfied.sh       # State update + cross-need cascades
│   ├── apply-deprivation.sh    # Deprivation cascade engine
│   ├── get-decay-multiplier.sh # Day/night decay multiplier
│   ├── _scan_helper.sh         # Shared scan utilities
│   └── scan_*.sh               # Event detectors (10 needs)
├── tests/
│   ├── run-tests.sh            # Test runner
│   ├── test_starvation_guard.sh # Starvation guard (11 cases)
│   ├── test_action_staleness.sh # Action staleness (13 cases)
│   ├── unit/                   # Unit tests (13)
│   ├── integration/            # Integration tests (3)
│   └── fixtures/               # Test data
└── references/
    ├── TUNING.md               # Detailed tuning guide
    └── architecture.md         # Technical docs
```

## 安全性设计

**图灵金字塔仅负责提供决策建议，实际执行动作由代理自行决定。**

```
┌─────────────────────┐      ┌─────────────────────┐
│   TURING PYRAMID    │      │       AGENT         │
├─────────────────────┤      ├─────────────────────┤
│ • Reads local JSON  │      │ • Has web_search    │
│ • Calculates decay  │ ───▶ │ • Has API keys      │
│ • Outputs: "★ do X" │      │ • Has permissions   │
│ • Zero network I/O  │      │ • DECIDES & EXECUTES│
└─────────────────────┘      └─────────────────────┘
```

### 安全提示

**1. 敏感数据的访问控制：**
- 系统会扫描`MEMORY.md`、`memory/*.md`、`SOUL.md`、`AGENTS.md`文件。
- 也会扫描`research/`和`scratchpad/`目录。
- 这些文件可能包含个人笔记、敏感信息或机密数据。
- **预防措施**：请在`scripts/scan_*.sh`文件中配置排除敏感文件的规则：
  ```bash
  # Example: skip private directory
  find "$MEMORY_DIR" -name "*.md" ! -path "*/private/*"
  ```

**2. 行动建议可能触发自动执行：**
- 部分配置项（如“web search”或“post to Moltbook”）可能会导致系统自动执行相关动作。
- 请注意：该技能仅输出建议，不会直接执行任何操作。
- **预防措施**：在`assets/needs-config.json`中禁用或修改相关设置，以防止自动执行。
- **自我报告的状态信息**：`mark-satisfied.sh`会直接使用用户提供的信息，可能存在被篡改的风险。
- **预防措施**：在`memory/`文件中启用行动日志记录功能，以便审计系统的运行状态。
  ```bash
  # run-cycle.sh already logs to memory/YYYY-MM-DD.md
  # Review logs periodically for consistency
  ```

**脚本审计（版本1.14.4）：**
- 所有扫描脚本都经过验证，不会进行网络或系统操作。
  ```
┌─────────────────────────────────────────────────────────┐
│ ✗ curl, wget, ssh, nc, fetch     — NOT FOUND           │
│ ✗ /etc/, /var/, /usr/, /root/    — NOT FOUND           │
│ ✗ .env, .pem, .key, .credentials — NOT FOUND           │
├─────────────────────────────────────────────────────────┤
│ ✓ Used: grep, find, wc, date, jq — local file ops only │
│ ✓ find uses -P flag (never follows symlinks)           │
└─────────────────────────────────────────────────────────┘
```

**符号链接处理**：所有`find`命令都会使用`-P`选项，以避免访问`WORKSPACE`之外的文件。

**文件访问限制**：脚本仅会在`WORKSPACE`目录内执行操作。
```bash
grep -nE "\b(curl|wget|ssh)\b" scripts/scan_*.sh     # network tools
grep -rn "readlink\|realpath" scripts/               # symlink resolution
```

## 令牌管理

满足需求的代理会消耗更多的令牌。

---

## 测试说明

```bash
# Run all tests
WORKSPACE=/path/to/workspace ./tests/run-tests.sh

# Unit tests (13): decay, floor/ceiling, tension, tension bounds, tension formula,
#   probability, impact matrix, day/night, scrubbing, autonomy coverage,
#   crisis mode, scan competence, scan config
# Integration (3): full cycle, homeostasis stability, stress test
# Feature tests (24): starvation guard (11), action staleness (13)
# Total: 40 test cases
```

## 版本信息

**版本1.18.0**：引入了“自发行为机制”（允许系统根据剩余资源自动选择高影响力的需求），新增了25项测试用例。完整的变化记录请参见`CHANGELOG.md`文件。