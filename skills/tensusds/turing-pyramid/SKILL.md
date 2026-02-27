# 图灵金字塔（Turing Pyramid）

10. 人工智能代理需要具备心理层次结构；代理会根据自身的“心跳”（heartbeat）来运行，并据此确定优先执行的动作。

**自定义设置：** 可调整衰减率（degradation rates）、权重（weights）以及行为模式（patterns）。默认值仅供参考，请参阅 `TUNING.md` 文件以获取更多信息。

**在做出以下更改前，请务必咨询人类用户：**  
- 更改需求的优先级；  
- 添加或删除需求；  
- 启用外部动作（external actions）。

---

## 系统要求

**系统二进制文件（必须位于 PATH 环境变量中）：**  
```
bash, jq, grep, find, date, wc, bc
```

**环境配置（强制要求，无替代方案）：**  
```bash
# Scripts will ERROR if WORKSPACE is not set
export WORKSPACE="/path/to/your/workspace"
```  
⚠️ **严禁在未设置 WORKSPACE 环境变量的情况下运行脚本，否则脚本会因找不到相关文件而退出。**  
此举可防止脚本意外扫描到非目标目录。

---

## 快速入门指南  
（Quick Start guide...）  
（具体内容请参考 `CODE_BLOCK_2_` 文件）

---

## 十大核心需求（The 10 Needs）  
（详细内容请参考 `CODE_BLOCK_3_` 文件）

---

## 核心逻辑（Core Logic）  

- **需求满足度（Satisfaction）：** 0.0–3.0（最低值为 0.5，以避免系统陷入僵局）  
- **心理紧张度（Tension）：** `需求优先级 × (3 - 需求满足度)`  

### 动作执行概率（Action Probability）  
（具体内容请参考 `CODE_BLOCK_4_` 文件）

### 紧张度加成（Tension Bonus）  
`紧张度加成 = 紧张度 × 50 / 最大紧张度`  

### 动作选择机制（Action Selection）  
- 执行动作后，调用 `mark-satisfied.sh` 脚本；  
- 若动作未被执行，则记录该需求为“已注意到”（NOTICED）并暂时推迟处理。  

---

## 保护机制（Protection Mechanisms）  

**基础需求的保护（Protection of Basic Needs）：**  
- 安全需求（Security, 编号 10）和完整性需求（Integrity, 编号 9）受到特别保护：  
  - 这些需求会影响其他较低层次的需求（例如：安全需求会影响代理的自主性）。  
  - 较低层次的需求无法降低这些基础需求的重要性。  
  - 仅存在以下正向关联：`完整性需求 → 安全需求（+0.15）` 和 `自主性需求 → 完整性需求（+0.20）`。  

---

## 需求之间的相互影响（Cross-Need Interactions）  
- **满足需求时（on_action）：** 满足某个需求会提升相关需求的重要性。  
- **需求未得到满足时（on_deprivation）：** 如果某个需求的重要性低于 1.0，会拖累其他需求的表现。  
（具体内容请参考 `CODE_BLOCK_7_` 文件）

### 使用技巧（Tips）  
- **利用需求之间的相互关联：** 如果某个需求的满足会提升其他需求的重要性，应优先处理该需求（+0.20）。  
- **注意潜在的恶性循环：** 某些行为可能导致需求之间的相互抑制（例如：过度表达需求可能导致他人不认可）。  
- **自主性是核心：** 自主性需求从五个方面获得支持，需保持其健康状态。  
- **苏格拉底式对话（Socratic Dialogue）：** 有效的对话有助于增进理解（-0.05）。  

完整的需求影响矩阵请参见 `assets/cross-need-impact.json` 文件。  

---

## 示例运行流程（Example Cycle）  
（具体内容请参考 `CODE_BLOCK_8_` 文件）

---

## 集成方式（Integration）  
将相关配置添加到 `HEARTBEAT.md` 文件中：  
___CODE_BLOCK_9_**

---

## 自定义设置（Customization）  
（无需人工干预即可进行调整）  

- **衰减率（Decay Rates）：** 请参考 `assets/needs-config.json` 文件进行配置：  
  - 较低的衰减率意味着需求会更快地被遗忘；较高的衰减率则意味着需求会持续更长时间影响代理的行为。  
- **动作权重（Action Weights）：** 同样在 `assets/needs-config.json` 文件中设置；权重越高，该需求被选中的概率越大。  
  - 将权重设置为 0 可禁用该需求。  
- **扫描模式（Scan Patterns）：** 通过 `scripts/scan_*.sh` 脚本自定义扫描规则，包括语言模式、文件路径和工作空间结构。  

---

## 重要提示：**  
在修改系统配置前，请务必先与人类用户沟通：**  
- 添加或删除需求时，请确保双方达成一致；  
- 不得擅自禁用安全需求或完整性需求。  

---

## 文件结构（File Structure）  
（文件结构说明请参考 `CODE_BLOCK_12_` 文件）

---

## 安全模型（Security Model）  
本系统仅负责生成建议，具体执行由代理自行决定。  

---

### 安全警告（Security Warnings）  
（请注意以下潜在风险）：  
**1. 敏感文件的访问权限：**  
  - 系统会扫描 `MEMORY.md`、`memory/*.md`、`SOUL.md`、`AGENTS.md` 等文件，以及 `research/` 和 `scratchpad/` 目录。  
  - 这些文件可能包含个人笔记、敏感信息或机密数据。  
  **应对措施：** 通过编辑 `scripts/scan_*.sh` 脚本来排除敏感文件的扫描范围。  

**2. 动作建议可能触发自动执行：**  
  - 部分配置选项（如“进行网络搜索”或“将结果发布到 Moltbook”）可能会触发自动执行。  
  - 请注意：该系统仅输出文本建议，不会实际执行任何操作。  
  **应对措施：** 在 `assets/needs-config.json` 中禁用相关外部动作，或配置代理运行时需要人工批准才能执行外部操作。  

**3. 系统对用户输入的信任：**  
  - `mark-satisfied.sh` 脚本直接信任用户的输入，可能导致状态被篡改。  
  **影响：** 仅影响当前代理的心理状态。  
  **应对措施：** 在 `memory/` 目录中启用日志记录功能，以便后续审计。  

---

## 脚本审计（Script Audit, v1.10.9）  
`scan_*.sh` 脚本经过验证，不会访问网络或系统资源。  
所有 `find` 命令均使用 `-P`（物理路径）模式，不会遍历位于 `WORKSPACE` 之外的符号链接。  

**扫描范围限制：** 脚本仅读取 `$WORKSPACE` 内的文件。  

---

## 代币系统（Token System）  
满足需求的代理会消耗更少的代币。  

---

## 版本信息（Version Information）  
**v1.10.1**：修复了若干漏洞并优化了文档内容。完整变更记录请参见 `CHANGELOG.md` 文件。