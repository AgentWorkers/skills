---
name: turing-pyramid
description: 10. 人工智能代理需要具备心理层次结构（即不同的行为优先级）。通过心跳检测来运行代理程序，从而确定应优先执行的操作。
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
    primaryEnv: WORKSPACE
---
# 图灵金字塔（Turing Pyramid）

AI代理需要具备心理层次结构。通过心跳信号来运行，以确定优先执行的动作。

**自定义设置：** 可调整衰减率、权重和模式。默认值仅供参考。详情请参阅 `TUNING.md`。

**在修改以下内容前，请先咨询人类用户：**  
- 更改需求的重要性值；  
- 添加或删除需求；  
- 启用外部动作。

---

## 系统要求

**系统二进制文件（必须位于 PATH 变量路径中）：**  
```
bash, jq, grep, find, date, wc, bc
```

**环境配置（必须满足，无备用方案）：**  
```bash
# Scripts will ERROR if WORKSPACE is not set
export WORKSPACE="/path/to/your/workspace"
```  
⚠️ **严禁未经许可的自动执行。** 如果 `WORKSPACE` 变量未设置，脚本将错误退出。  
这样可以防止脚本意外扫描到非目标目录。

**安装后的配置（ClawHub）：**  
```bash
# ClawHub doesn't preserve executable bits — fix after install:
chmod +x ~/.openclaw/workspace/skills/turing-pyramid/scripts/*.sh
chmod +x ~/.openclaw/workspace/skills/turing-pyramid/tests/**/*.sh
```  
**原因：** Unix 可执行文件的权限（`+x`）在 ClawHub 包中不会被保留。  
脚本使用 `bash scripts/run-cycle.sh` 时可以正常运行，但直接运行 `./scripts/run-cycle.sh` 时需要设置权限 `+x`。

---

## 数据访问与透明度

**该技能会读取以下文件内容：**  
- `MEMORY.md`、`memory/*.md`：用于获取连接信息、表达能力和理解需求的相关数据；  
- `SOUL.md`、`SELF.md`：用于检查系统的完整性和连贯性；  
- `research/`、`scratchpad/`：用于评估代理的能力和活动情况；  
- 仪表盘文件和日志：用于各种需求评估。

**该技能会写入以下文件：**  
- `assets/needs-state.json`：记录当前的满足/未满足需求的状态；  
- `assets/audit.log`：记录所有需求满足操作的日志（版本 1.12.0 及以上）。

**隐私保护措施：**  
- 扫描过程使用正则表达式（grep），而非语义分析；因此只识别关键词，不理解其实际含义；  
- 状态文件中不包含用户个人信息，仅记录需求相关数据；  
- 审计日志会记录需求满足的原因；  
- 该技能本身不会将任何数据传输到外部。

**限制与信任机制：**  
- `mark-satisfied.sh` 信任用户提供的操作原因；审计日志仅记录操作内容，不验证其真实性；  
- `needs-config.json` 中的一些操作会引用外部服务（如 Moltbook、网络搜索），这些操作会标记为 `"external": true, "requires_approval": true`；  
- 外部操作仅作为建议提供，由代理自行决定是否执行；  
- 如果不希望接收外部操作建议，可将相关权重设置为 0。

**网络与系统访问限制：**  
- 脚本中不包含任何网络请求（如 curl、wget、ssh 等）；  
- 脚本中不包含任何系统管理命令（如 sudo、systemctl、docker 等）；  
- 所有操作都在工作目录（WORKSPACE）内完成，使用工具如 grep、find、jq、bc、date；  
- 该技能仅提出操作建议，从不实际执行这些操作。

**所需环境变量：**  
- `WORKSPACE`：代理的工作目录路径（必须设置）；  
- `TURING_CALLER`：可选，用于记录审计痕迹（可选值：`heartbeat`、`manual`）。

**审计记录（版本 1.12.0 及以上）：**  
所有 `mark-satisfied.sh` 的调用操作都会被记录，包括：  
- 时间戳、需求类型、操作影响、需求满足前的状态以及满足后的状态；  
- 操作原因（会被过滤掉敏感信息）；  
- 调用者类型（心跳信号或手动操作）。

**敏感数据处理（版本 1.12.3 及以上）：**  
在写入审计日志之前，会处理敏感信息：  
- 长字符串（超过 20 个字符）会被替换为 `[REDACTED]`；  
- 信用卡相关信息会被替换为 `[CARD]`；  
- 电子邮件地址会被替换为 `[EMAIL]`；  
- 密码/密钥等敏感信息会被替换为 `[REDACTED]`；  
- 代币信息会被替换为 `Bearer [REDACTED]`。  
查看审计记录的命令：`cat assets/audit.log | jq`。

---

## 快速入门指南  
```bash
./scripts/init.sh                        # First time
./scripts/run-cycle.sh                   # Every heartbeat  
./scripts/mark-satisfied.sh <need> [impact]  # After action
```

---

## 十项基本需求  
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

**需求满足度：** 0.0–3.0（最低值为 0.5，防止系统陷入停滞）  
**紧张程度：** `重要性 × (3 - 满足度)`  

### 动作执行概率（版本 1.13.0）  
系统支持 6 级别的需求满足度评估：  
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

**紧张程度加成：** `加成 = (紧张程度 × 50) / 最大紧张程度`  

### 动作选择机制（版本 1.13.0）  
采用 6 级别的需求满足度矩阵，确保动作选择的平滑过渡：  
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
- **危机状态（0.5）**：所有需求都必须通过重大行动来满足；  
- **完美状态（3.0）**：跳过动作选择，避免浪费资源在已满足的需求上。  

**处理方式：**  
- 执行动作后，`mark-satisfied.sh` 会记录该操作；  
- 被记录的动作会被标记为“已执行”。  

---

## 保护机制  
```
┌─────────────┬───────┬────────────────────────────────────────┐
│ Mechanism   │ Value │ Purpose                                │
├─────────────┼───────┼────────────────────────────────────────┤
│ Floor       │  0.5  │ Minimum sat — prevents collapse        │
│ Ceiling     │  3.0  │ Maximum sat — prevents runaway         │
│ Cooldown    │   4h  │ Deprivation cascades once per 4h       │
│ Threshold   │  1.0  │ Deprivation only when sat ≤ 1.0        │
└─────────────┴───────┴────────────────────────────────────────┘
```  
**日夜模式（版本 1.11.0）：** 在夜间降低衰减速度，以减轻休息时的压力；  
- 配置方式：`assets/decay-config.json`；  
- 默认设置：06:01–22:00 为白天模式（衰减系数为 1.0），22:01–06:00 为夜间模式（衰减系数为 0.5）；  
- 可通过设置 `"day_night_mode": false` 来禁用此功能。  

**基础需求的优先级：**  
- 安全需求（权重 10）和完整性需求（权重 9）具有较高优先级；  
- 它们会影响其他较低级别的需求；  
- 仅允许 `integrity → security`（权重 +0.15）和 `autonomy → integrity`（权重 +0.20）之间的相互影响。  

## 需求之间的相互影响  

- **满足需求后：** 相关需求会得到提升；  
- **需求未满足时：** 低满足度会导致其他需求也处于较低状态。  
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
- **利用需求之间的关联：** 如果某个需求的满足能提升其他需求的表达能力，优先处理该需求（权重 +0.20）；  
- **注意潜在的恶性循环：** 表达能力和被认可度的变化可能导致相互抑制；  
- **保持自主性：** 自主性需求从多个来源获得支持，需保持其健康状态（权重 +0.20）；  
- **苏格拉底式对话：** 有效的沟通有助于增进理解（权重 -0.05）。  
完整的需求影响矩阵：`assets/cross-need-impact.json`。

---

## 示例操作流程  
```
🔺 Turing Pyramid — Cycle at Tue Feb 25 05:36
======================================

⚠️ Deprivation cascades:
   autonomy (sat=0.5) → integrity: -0.25 (now: 1.75)
   autonomy (sat=0.5) → expression: -0.20 (now: 0.80)

Current tensions:
  closure: tension=21 (sat=0, dep=3)
  connection: tension=15 (sat=0, dep=3)

📋 Decisions:

▶ ACTION: closure (tension=21, sat=0.00)
  → coherence: +0.20, competence: +0.15, autonomy: +0.10

▶ ACTION: connection (tension=15, sat=0.00)
  → expression: +0.20, recognition: +0.15
  → understanding: -0.05 (Socratic effect)
```

---

## 集成方式  
将该技能集成到 `HEARTBEAT.md` 文件中：  
```bash
/path/to/skills/turing-pyramid/scripts/run-cycle.sh
```

---

## 自定义设置  

**无需人工干预即可进行调整：**  
- **衰减率：** 在 `assets/needs-config.json` 中设置；  
  更低的衰减率意味着需求更快消失；更高的衰减率意味着需求持续更长时间。  
- **动作权重：** 同样在该文件中设置；  
  更高的权重意味着该动作更有可能被选中；将权重设置为 0 可禁用该动作。  
- **扫描模式：** 在 `scripts/scan_*.sh` 中配置语言模式、文件路径和工作目录结构。  

**修改需求时请先咨询用户：**  
- **添加新需求：** 这十项需求是有序排列的，修改前请先讨论；  
- **删除需求：** 未经同意，不得禁用安全或完整性需求。  

---

## 文件结构  
```
turing-pyramid/
├── SKILL.md                    # This file
├── CHANGELOG.md                # Version history
├── assets/
│   ├── needs-config.json       # ★ Main config (tune this!)
│   ├── cross-need-impact.json  # ★ Cross-need matrix
│   └── needs-state.json        # Runtime state (auto)
├── scripts/
│   ├── run-cycle.sh            # Main loop
│   ├── mark-satisfied.sh       # State + cascades
│   ├── apply-deprivation.sh    # Deprivation cascade
│   └── scan_*.sh               # Event detectors (10)
└── references/
    ├── TUNING.md               # Detailed tuning guide
    └── architecture.md         # Technical docs
```

---

## 安全模型  
**该技能仅提供建议，实际执行由代理决定。**  

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

### 安全提示：  
```
┌────────────────────────────────────────────────────────────────┐
│ THIS SKILL READS WORKSPACE FILES THAT MAY CONTAIN PII         │
│ AND OUTPUTS ACTION SUGGESTIONS THAT CAPABLE AGENTS MAY        │
│ AUTO-EXECUTE USING THEIR OWN CREDENTIALS.                     │
└────────────────────────────────────────────────────────────────┘
```  
1. **对敏感文件的访问：** 无需使用特殊令牌；  
  该技能会读取 `MEMORY.md`、`memory/*.md`、`SOUL.md`、`AGENTS.md` 文件；  
  也会扫描 `research/` 和 `scratchpad/` 目录；  
  **风险：** 这些文件可能包含个人笔记、敏感信息或机密数据；  
  **应对措施：** 在 `scripts/scan_*.sh` 中配置排除敏感文件路径。  

2. **动作建议可能触发自动执行：**  
  配置中包含某些动作（如“网络搜索”、“发送到 Moltbook”等）；  
  该技能仅输出文本，不会执行任何操作；  
  **风险：** 如果代理运行时启用了自动执行功能，可能会根据建议执行操作；  
  **应对措施：** 在 `assets/needs-config.json` 中禁用或配置外部动作。  

3. **用户提供的状态信息未经验证：**  
  `mark-satisfied.sh` 直接使用用户提供的信息；  
  **风险：** 用户可能提供虚假信息；  
  **影响：** 仅影响当前代理的心理状态；  
  **应对措施：** 在 `memory/` 文件中记录操作日志以供审计。  

### 脚本审计（版本 1.14.4）  
`scan_*.sh` 脚本经过验证，不会进行网络或系统访问；  
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

**符号链接保护：** 所有 `find` 命令都使用 `-P` 参数（仅扫描工作目录内的文件）；  
**扫描范围限制：** 脚本仅读取 `$WORKSPACE` 内的文件路径。  

## 令牌管理  
满足需求的代理会消耗较少令牌。  
```
┌──────────────┬─────────────┬────────────┐
│ Interval     │ Tokens/mo   │ Est. cost  │
├──────────────┼─────────────┼────────────┤
│ 30 min       │ 1.4M-3.6M   │ $2-6       │
│ 1 hour       │ 720k-1.8M   │ $1-3       │
│ 2 hours      │ 360k-900k   │ $0.5-1.5   │
└──────────────┴─────────────┴────────────┘
```

## 测试说明  
```bash
# Run all tests
WORKSPACE=/path/to/workspace ./tests/run-tests.sh

# Unit tests (9): decay, floor/ceiling, tension, probability, impact matrix, day/night, scrubbing
# Integration (3): full cycle, homeostasis stability, stress test
```

---

## 版本信息  
**版本 1.14.1**：新增了多级需求评估机制和扩展的测试覆盖范围。完整变更日志请参阅 `CHANGELOG.md`。