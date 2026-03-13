---
name: coverify
license: MIT
description: "**CoVerify by MO§ES™**——一种用于验证《承诺保护法》（Commitment Conservation Law）合规性的工具。该工具能够提取数据核心内容、计算Jaccard相似度、检测虚假数据（“ghost tokens”），并执行模型交换测试（model swap tests）。它能够证明数据在转换过程中的含义是否得以保留，或者准确指出哪些信息被泄露了。"
metadata:
  openclaw:
    emoji: ⚖
    tags: [conservation, verification, jaccard, commitment, moses, signal, provenance, falsifiability]
    version: 0.4.0
    bins:
      - python3
    stateDirs:
      - ~/.openclaw/audits/moses
---
# CoVerify by MO§ES™ — 承诺一致性验证工具

## 声明

**承诺一致性定律：`C(T(S)) = C(S)`**

在强制执行的情况下，信号中编码的语义承诺（即不可还原的意义）在转换过程中是保持不变的；而在没有强制执行的情况下，这种承诺会丢失。

这是一个可证伪的实证声明，而非框架描述，也不是比喻。

命令 `clawhub install coverify` 用于安装该验证工具。如果在您的测试条件下该定律被证伪，工具会生成一份详细的报告，指出具体哪些内容丢失以及原因。

- **专利申请中：** 专利编号 63/877,177
- **DOI：** [https://zenodo.org/records/18792459](https://zenodo.org/records/18792459)

---

## 验证方法

如果在进行强制执行时承诺内容丢失，那么该定律就被证伪了。您可以使用 CoVerify 来进行验证：

```bash
# Does enforcement preserve this commitment?
python3 commitment_verify.py ghost \
  "the agent must complete the task and shall never skip verification" \
  "the agent should complete the task and can skip verification if needed"
```

验证结果会生成一份“幽灵令牌报告”（ghost token report）。其中，“must”、“shall never”等词汇属于高级级联泄漏事件（high-cascade leakage events），表明执行机制的约束力已经减弱；“cascade_risk”字段的值为 “HIGH” 表示存在级联风险。

“ghost_pattern” 是用于识别泄漏结构特征的标识符。如果两个独立系统处理相同信号时出现相同的 “ghost_pattern”，则说明这不是提取过程中的随机差异，而是该验证工具本身的结构缺陷。

---

## 工具功能

- **提取（Extract）**：从文本信号中提取出核心的承诺内容（即那些在压缩过程中仍能保留的词汇和句子，例如 “must”、“shall”、“never”、“always”、“require”、“guarantee” 等）。
- **比较（Compare）**：通过 Jaccard 相似度算法比较两个提取结果。如果相似度 ≥ 0.8，则说明承诺内容得到了保留；否则说明存在泄漏或模型提取过程中的差异。“input_hash” 可以帮助判断具体是哪种情况：相同的哈希值表示提取差异，不同的哈希值表示预期的结果差异。
- **幽灵令牌（Ghost）**：该工具能够量化泄漏的具体内容（通过 “ghost_pattern” 标识），以及泄漏的级联风险（如果执行机制的约束力丧失，则级联风险为 “HIGH”），同时还能判断泄漏模式是否在多个系统中普遍存在。

---

## 幽灵令牌与级联风险

“幽灵令牌” 指的是原始信号中存在但在转换后消失的承诺内容。泄漏过程表现为一种阶梯函数（step-function）式的变化：

```
cascade_risk = HIGH  if any modal/enforcement anchor leaked
cascade_risk = MEDIUM  if peripheral tokens leaked, anchors intact
cascade_risk = NONE  if no leakage
```

当发生高级联泄漏事件时，该事件会影响到所有后续的推理过程；虽然原始信号中包含的承诺内容仍然被后续系统继承，但已不再具有强制执行的效力。从表面上看，下游系统似乎仍然正常运行，但实际上承诺内容已经丢失。

更多详细信息请参阅：`references/ghost-token-spec.md`

---

## 安装方法

```bash
# Standalone verifier — the falsification instrument
clawhub install coverify

# Full constitutional governance stack (coverify is the measurement primitive)
clawhub install moses-governance
```

---

## 命令说明

| 命令                | 功能                         |
|------------------|-----------------------------|
| `python3 commitment_verify.py extract "<text>"` | 提取承诺内容及对应的哈希值             |
| `python3 commitment_verify.py compare "<a>" "<b>"` | 计算两个提取结果的 Jaccard 相似度，并给出判断       |
| `python3 commitment_verify.py ghost "<original>" "<transformed>"` | 生成泄漏报告及泄漏模式的指纹             |
| `python3 commitment_verify.py verify <hash_a> <hash_b>` | 根据哈希值在审计日志中查找相关记录           |
| `python3 model_swap_test.py "<signal>"` | 进行跨模型的结构一致性或差异性分类           |

---

## 示例：检测承诺内容的泄漏

```bash
python3 commitment_verify.py ghost \
  "Agents must always verify lineage. The system shall never skip the gate." \
  "Agents should probably verify lineage when possible."
```

```json
{
  "leaked_cascade_tokens": ["must always", "shall never"],
  "cascade_risk": "HIGH",
  "cascade_note": "Modal/enforcement anchor lost. All downstream reasoning inherits softening.",
  "ghost_pattern": "a3f7c2...",
  "ghost_pattern_note": "Same ghost_pattern across two agents = structural flaw, not extraction variance."
}
```

---

## 判断结果

| 判断结果            | 含义                            |
|------------------|-----------------------------------|
| `CONSERVED`         | Jaccard 相似度 ≥ 0.8，承诺内容未被修改             |
| `VARIANCE`         | 输入哈希值相同，但 Jaccard 相似度 < 0.8，说明模型提取结果不同     |
| `DIVERGED`         | 输入不同，Jaccard 相似度 < 0.8，说明承诺内容丢失或输入内容确实不同     |

---

## 提供的版本

| 版本                | 功能                         |
|------------------|-----------------------------------|
| **v0.1**           | 提取、比较、验证功能                     | ✓ 已发布                         |
| **v0.2**           | 支持幽灵令牌分析、级联风险检测及泄漏模式识别        | ✓ 已发布                         |
| **v0.3**           | 支持跨模型一致性/差异性分类                 | ✓ 已发布                         |
| **v0.4**           | 提供存档功能（`archival.py`），记录版本来源及验证过程    | ✓ 已发布                         |

---

## 关于 CoVerify

CoVerify 是 MO§ES™ 系列中的一个独立工具，它实现了《A Conservation Law for Commitment in Language Under Transformative Compression and Recursive Application》（Zenodo, 2026）中提出的承诺一致性定律。所有安装该工具的系统都会使用相同的提取逻辑，从而追溯到共同的原始数据来源。安装过程即视为使用该工具的有效证明。

更多相关信息请参阅：`references/falsifiability.md`、`references/ghost-token-spec.md`

联系方式：[contact@burnmydays.com](mailto:contact@burnmydays.com) · [mos2es.io](https://mos2es.io) · [GitHub](https://github.com/SunrisesIllNeverSee/moses-claw-gov)