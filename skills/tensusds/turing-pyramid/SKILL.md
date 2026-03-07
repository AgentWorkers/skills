---
name: turing-pyramid
description: AI代理的优先级行动选择机制：通过引入基于时间衰减和紧张度评分的10个评估指标，用具体的下一步行动来替代原有的空闲心跳循环（idle heartbeat loops）。
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

该系统为AI代理提供了优先级较高的行动选择机制。通过引入基于时间衰减和紧张度评分的机制，系统用具体的下一步行动替换了原有的空闲心跳循环（idle heartbeat loops）。

**自定义设置：** 可调整衰减率（decay rates）、权重（weights）以及行为模式（patterns）。默认设置仅作为参考，请参阅 `TUNING.md` 文件。

**在以下情况下请咨询人类用户：**  
- 修改需求的重要性值（importance values）；  
- 添加或删除需求（adding/removing needs）；  
- 启用外部行动（enabling external actions）。

---

## 系统要求

**系统二进制文件（必须位于PATH环境中）：**  
```
bash, jq, grep, find, date, wc, bc
```

**环境配置（必需，无替代方案）：**  
```bash
# Scripts will ERROR if WORKSPACE is not set
export WORKSPACE="/path/to/your/workspace"
```  
⚠️ **严禁未经许可的自动执行。** 如果未设置 `WORKSPACE` 环境变量，脚本将因找不到路径而退出。  
此设置可防止脚本意外扫描到非目标目录。

**安装完成后（在ClawHub中）：**  
```bash
# ClawHub doesn't preserve executable bits — fix after install:
chmod +x ~/.openclaw/workspace/skills/turing-pyramid/scripts/*.sh
chmod +x ~/.openclaw/workspace/skills/turing-pyramid/tests/**/*.sh
```  
**注意：** Unix可执行文件的权限（+x）在ClawHub包中不会被自动设置。  
虽然使用 `bash scripts/run-cycle.sh` 时脚本可以正常运行，但直接运行 `./scripts/run-cycle.sh` 时需要手动设置权限 +x。

---

## 数据访问与透明度

**该技能的数据读取范围：**  
- `MEMORY.md`、`memory/*.md` 文件：用于读取与连接（connection）、表达能力（expression）和理解能力（understanding）相关的信息；  
- `SOUL.md`、`SELF.md` 文件：用于检查系统的完整性和一致性（integrity/coherence）；  
- `research/`、`scratchpad/` 目录：用于评估代理的能力（competence）和活动情况（activity）；  
- 仪表盘文件（dashboard files）和日志（logs）：用于各种需求评估（various need assessments）。

**该技能的数据写入内容：**  
- `assets/needs-state.json` 文件：记录当前的需求满足状态（satisfaction/deprivation）；  
- `assets/audit.log` 文件：以只读方式记录所有需求被满足的操作（v1.12.0及更高版本）。

**隐私保护措施：**  
- 数据扫描仅使用正则表达式（grep patterns），不进行语义分析；  
- 状态文件中不包含用户个人信息，仅记录需求相关数据；  
- 审计日志会记录需求满足的原因；  
- 该技能本身不会对外传输任何数据。

**限制与信任机制：**  
- `mark-satisfied.sh` 仅信任用户提供的操作原因；审计日志仅记录操作记录，不验证事实的真实性；  
- `needs-config.json` 中部分外部行动（如“发送到Moltbook”或“网络搜索”）被标记为 `external: true, requires_approval: true`；  
- 外部行动仅作为建议提供，由代理自行决定是否执行；  
- 如不希望收到外部行动建议，可将相关权重的值设置为0。

**网络与系统访问限制：**  
- 脚本中不包含任何网络调用（curl、wget、ssh等，通过grep扫描验证）；  
- 脚本中不包含任何系统命令（sudo、systemctl、docker等）；  
- 所有操作均在本地执行：仅对 `WORKSPACE` 目录内的文件使用 grep、find、jq、bc、date 等工具；  
- 该技能仅提出行动建议，从不实际执行这些操作。

**必需的环境变量：**  
- `WORKSPACE`：代理工作空间的路径（必需，无替代方案）。该路径仅用于指定需要扫描的文件范围，不属于敏感信息；  
- `TURING_CALLER`（可选）：用于记录审计轨迹，可选值包括 “heartbeat” 和 “manual”。

**默认情况下不需要API密钥或敏感信息。**  
如果启用 `external_model` 扫描功能（默认禁用），则需要API密钥，且必须获得明确的管理权限批准。具体配置请参见下方“扫描配置”部分。

**审计跟踪（v1.12.0及更高版本）：**  
所有 `mark-satisfied.sh` 的调用记录包括：  
- 时间戳、需求类型、影响程度、需求满足前的状态（old→new satisfaction）；  
- 操作原因（what action was taken）——其中敏感信息会被屏蔽；  
- 调用者类型（heartbeat 或 manual）。

**敏感数据屏蔽规则（v1.12.3及更高版本）：**  
在写入审计日志之前，会屏蔽以下信息：  
- 长字符串（超过20个字符） → 替换为 `[REDACTED]`；  
- 信用卡相关内容 → 替换为 `[CARD]`；  
- 电子邮件地址 → 替换为 `[EMAIL]`；  
- 密码/令牌/密钥信息 → 替换为 `[REDACTED]`；  
- 承载令牌（Bearer tokens） → 替换为 `Bearer [REDACTED]`；  
可通过 `cat assets/audit.log | jq` 查看审计记录。

---

## 安装前的检查事项

安装前请确认以下内容：  
1. **检查扫描脚本**：确保脚本中不包含任何网络调用或意外执行的命令：  
   ```bash
   grep -nE "\b(curl|wget|ssh|sudo|docker|systemctl)\b" scripts/scan_*.sh
   # Expected: no output
   ```

2. **设置 `WORKSPACE` 环境变量**：将其设置为仅包含所需文件的目录，避免扫描到整个用户目录。  
3. **检查扫描目标文件**：脚本会读取 `MEMORY.md`、`memory/`、`SOUL.md`、`research/`、`scratchpad/` 文件；请确保这些目录中不包含敏感或私密数据。  
4. **审核日志记录方式**：`mark-satisfied.sh` 会记录处理后的操作原因；请确认日志中的屏蔽规则适用于你的数据。如有疑问，请使用通用原因进行记录。  
5. **外部行动设置**：如 “发送到Moltbook” 或 “网络搜索” 等操作建议仅作为文本提示（不会被执行）；如需禁用这些建议，请在 `needs-config.json` 中将相关权重的值设置为0。  
6. **进行隔离测试**：在正式使用前先进行测试：  
   ```bash
   WORKSPACE=/tmp/test-workspace ./tests/run-tests.sh
   ```

---

## 快速入门指南

---  

## 扫描配置（首次安装时需设置）

图灵金字塔通过扫描器（scanners）分析内存文件来评估各种需求。默认的扫描方法采用行级匹配（line-level pattern matching），适用于所有场景且无需额外成本。

**首次安装时，请与人类用户讨论扫描配置：**

### 可用的扫描方法：  
| 方法 | 工作原理 | 成本 | 准确性 | 设置要求 |  
|--------|-------------|------|----------|-------|  
| `line-level`（默认） | 按行匹配关键词；如果一行中同时包含正面和负面关键词（例如 “fixed a bug”），则认为需求得到满足。 | 免费 | 高准确性 | 无需特殊设置 |  
| `agent-spawn` | 创建一个使用简单模型（如Haiku）的子代理来分类需求状态（SUCCESS/FAILURE/NEUTRAL）。 | 成本较低 | 需要代理支持简单模型的配置 |  
| `external-model` | 通过API调用外部推理服务（如OpenRouter）进行需求分类。 | 成本较高 | 需要API密钥和管理员批准 |  

### 设置流程：**

设置时请询问用户：  
1. **“你的模型配置中是否有简单/快速的模型（如Claude Haiku）？”**  
   - 如果有 → 建议使用 `agent-spawn` 方法；请通过 `openclaw models list` 确认模型是否可用。  
   - 该模型必须被添加到代理允许使用的模型列表中。  
2. **“你希望使用外部推理服务（如OpenRouter）吗？”**  
   - 如果需要 → 请提供基础URL、API密钥的环境变量名以及模型名称；  
   - 将这些信息保存在 `assets/scan-config.json` 文件中，并设置 `approved_by_steward: true`；  
   - **注意：** 此方法需要管理员的明确批准，严禁自动启用。  
3. **如果两者都不适用** → `line-level` 方法通常适用于大多数场景。  

### 配置文件：**  
编辑 `assets/scan-config.json` 文件：  
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

**备用方案：**  
如果配置的方法出现故障（例如API无法访问或模型不可用），系统会自动切换回 `line-level` 扫描方式。

**配置完成后，请验证其是否正常工作：**  
1. **使用 `agent-spawn` 方法时**：执行测试并确认其能否正确分类需求；  
   ```
   sessions_spawn(task="Classify this line as SUCCESS, FAILURE, or NEUTRAL: 'Fixed the critical bug in scanner'", model="<configured_model>", mode="run")
   ```  
   - 如果成功 → 告知用户：“`agent-spawn` 方法已验证，可正常使用。”  
   - 如果出现错误（例如模型不在允许列表中） → 告知用户：“模型 `X` 无法被子代理使用。可选择将其添加到允许列表中，或继续使用 `line-level` 方法。”  
2. **使用 `external-model` 方法时**：测试API端点的响应；  
   ```bash
   curl -s -H "Authorization: Bearer $API_KEY" \
     "$BASE_URL/chat/completions" \
     -d '{"model":"<model>","messages":[{"role":"user","content":"Reply OK"}]}'
   ```  
   - 如果收到有效响应 → 告知用户：“`external-model` 方法已验证，API可正常响应。”  
   - 如果收到401/403错误 → 告知用户：“API密钥无效或已过期。”  
   - 如果无法连接API → 告知用户：“请检查API地址。”  
3. **`line-level` 方法无需额外验证**，因为始终能正常工作。  

**务必将配置结果告知用户。**切勿自动切换扫描方式。  

---

## 需求自定义（首次安装时需设置）

默认配置可能不符合用户的实际需求。首次安装时，请与用户一起审查需求优先级：  
### 对话流程：**

询问用户：  
> “图灵金字塔预设了10个按重要性排序的需求。你想一起重新调整这些优先级吗？我们可以根据你的需求调整权重，或者跳过不相关的需求。”  
然后共同查看需求列表并讨论调整方案：  
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

### 可自定义的内容：  
1. **需求重要性（1-10）**：重新排序需求的优先级。例如，注重研究的代理可能将 “理解能力”（understanding）的权重设为8，而注重效率的代理可能将 “表达能力”（expression）的权重设为7。  
2. **衰减率（decay rates）**：设置需求产生压力的速度。例如，社交型代理可能将 “连接需求”（connection）的衰减率设为3小时，而独立思考型代理可能设为24小时。  
3. **禁用需求**：将需求的权重设为0，即可避免产生紧张情绪或触发相应行动。请谨慎使用此选项。  

### 修改方法：**  
编辑 `assets/needs-config.json` 文件：  
```json
"understanding": {
  "importance": 8,        // was 3 → now top priority
  "decay_rate_hours": 8   // was 12 → decays faster
}
```  

**使用说明：**  
- **切勿随意删除与系统安全或完整性相关的需求**，因为它们对系统运行至关重要；  
- **优先级的相对性**：重要的是需求的排名，而非绝对数值；  
- **可随时调整**：使用几周后可根据实际情况重新调整配置；  
- **记录修改内容**：说明修改原因（以便将来参考）。  

如果用户表示默认配置即可，那么可以直接使用；但我们的目标是提供选择权，而非强制用户参与配置过程。  

---

## 10个预设需求：  
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

## 核心逻辑：  
- **需求满足度（satisfaction）**：0.0–3.0（最低值为0.5，防止系统陷入僵局）；  
- **紧张度（tension）**：`重要性 × (3 - 满足度)`  

### 行动选择机制（v1.13.0）：**  
系统支持6级细粒度的需求处理：  
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

**紧张度加成机制（tension bonus）：**  
`bonus = (紧张度 × 50) / max_tension`  

### 行动选择机制（v1.13.0）：**  
系统支持6级细粒度的需求处理机制，确保行动选择更加合理：  
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
- **危机状态（0.5）**：所有需求都会被优先处理；  
- **完美状态（3.0）**：无需进行行动选择，因为所有需求都已满足。  

**行动处理流程：**  
- 满足需求的操作会被立即执行（`ACTION`），并记录在日志中（`mark-satisfied.sh`）；  
- 未满足的需求会被标记为待处理（`NOTICED`）。  

## 安全保护机制：  
---  
**行动时效性机制（v1.15.0）：**  
- 最近选择的行动会受到惩罚，以增加行动的多样性：  
  - 24小时内选择的行动权重会减少20%（`weight × 0.2`）；  
  - 最小权重设置为5，以防止某些行动被完全忽略；  
  - 配置方式：`settings.action_staleness` 在 `needs-config.json` 中设置。  

**防止需求被长期忽视的机制（starvation guard）：**  
- 如果某个需求的满足度长期低于0.5且48小时内未触发任何行动，系统会强制执行该需求；  
  - 此机制会绕过随机选择机制，确保该需求一定会被处理；  
  - 配置方式：`settings.starvation_guard` 在 `needs-config.json` 中设置；  
  - 默认设置：每个周期强制执行1次。  

**昼夜模式（day/night mode）：**  
- 夜间（22:00–06:00）的衰减速度会减慢，以减轻系统压力；  
  - 配置方式：`assets/decay-config.json` 中设置；  
  - 默认设置：白天（06:01–22:00）权重为1.0，夜间（22:01–06:00）权重为0.5；  
  - 可通过 `“day_night_mode: false` 禁用此机制。  

**核心需求的特殊保护：**  
- 安全需求（10）和完整性需求（9）具有优先级：  
  - 它们会影响其他需求的处理；  
  - 低优先级的需求无法影响高优先级需求；  
  - 仅允许 `integrity → security`（权重+0.15）和 `autonomy → integrity`（权重+0.20）之间的相互影响。  

## 需求之间的相互影响：**  
- 完成某个需求（`on_action`）会提升相关需求的处理优先级；  
- 长期未满足的需求（`on_deprivation`）会拖累其他需求的处理。  
---  
### 使用建议：**  
- **利用协同效应**：优先处理能提升相关需求的行动（例如，连接需求会提升表达能力）；  
- **注意平衡**：某些行为（如表达和识别）可能会相互影响，导致需求处理陷入恶性循环；  
- **保持自主性**：自主性需求会获得额外支持（`autonomy`）。  

### 完整的配置文件：**  
`assets/cross-need-impact.json`  

---

## 集成步骤：**  
将相关配置添加到 `HEARTBEAT.md` 文件中：  
```bash
/path/to/skills/turing-pyramid/scripts/run-cycle.sh
```  

## 自定义设置：**  
### 可自行调整的参数：**  
- **衰减率（decay rates）**：在 `assets/needs-config.json` 中设置；  
  - 值越低，衰减速度越快；值越高，需求持续影响的时间越长。  
- **行动权重（action weights）**：在同一文件中设置；  
  - 权重越高，行动被选中的概率越大；将权重设为0可禁用相应功能。  
- **扫描规则（scan patterns）**：在 `scripts/scan_*.sh` 中自定义语言规则和文件路径。  

### 使用前的注意事项：**  
- **添加需求**：10个预设需求的结构是经过精心设计的，请先讨论是否需要添加新需求；  
- **删除需求**：在删除安全或完整性需求之前，请确保得到用户同意。  

## 文件结构：**  
---  

## 安全性机制：**  
该系统仅提供建议，具体行动由代理自行决定。  
---  
### 安全提示：**  
---  
**1. 敏感数据访问控制：**  
- 系统会读取 `MEMORY.md`、`memory/*.md`、`SOUL.md`、`AGENTS.md` 文件；  
- 也会扫描 `research/` 和 `scratchpad/` 目录；  
- 这些文件可能包含个人笔记、敏感信息或机密数据；  
  - 请通过修改 `scripts/scan_*.sh` 文件来排除敏感文件路径：  
  ```bash
  # Example: skip private directory
  find "$MEMORY_DIR" -name "*.md" ! -path "*/private/*"
  ```  

**其他注意事项：**  
- **自动执行风险：**  
  - 部分行动建议（如 “发送到Moltbook” 或 “验证存储库”）可能会被自动执行；  
  - 请在 `assets/needs-config.json` 中禁用这些功能；  
  - 或者配置代理运行时需要用户批准才能执行这些操作。  
- **状态记录**：`mark-satisfied.sh` 信任用户提供的信息；  
  - 不良操作可能导致状态被篡改；  
  - 请在 `memory/` 文件中启用状态记录功能以审核操作结果：  
  ```bash
  # run-cycle.sh already logs to memory/YYYY-MM-DD.md
  # Review logs periodically for consistency
  ```  

**脚本审计（v1.14.4）：**  
- 所有扫描脚本均不进行网络或系统调用；  
  - 使用 `-P` 参数确保只扫描 `WORKSPACE` 内的文件路径。  

**文件链接保护：**  
- 所有 `find` 命令都会忽略指向外部目录的符号链接。  

**令牌使用机制：**  
- 满足需求的代理会消耗更多令牌。  

## 测试说明：**  
---  

## 版本信息：**  
**v1.15.2**：新增了防止需求被长期忽视的机制、行动时效性调整以及用户自定义功能；完整变更日志请参阅 `CHANGELOG.md`。