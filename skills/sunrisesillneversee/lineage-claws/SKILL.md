---
name: lineage-claw
license: MIT
description: MO§ES™ 实现中的加密来源验证功能：每个主权链（sovereign chain）都能追溯到其原始文件（origin filing）。没有该“锚点”（anchor）的链无法完成验证；没有完整传承关系的副本也无法通过验证。档案传承关系功能将在版本 0.2 中正式引入。
metadata:
  openclaw:
    emoji: §
    tags: [governance, lineage, audit, provenance, identity, trust, moses]
    version: 0.1.3
    bins:
      - python3
    stateDirs:
      - ~/.openclaw/governance
      - ~/.openclaw/audits/moses
requires:
  bins:
    - python3
  stateDirs:
    - ~/.openclaw/governance
    - ~/.openclaw/audits/moses
example: |
  python3 lineage.py init      # anchor genesis to origin filing
  python3 lineage.py verify    # confirm chain traces to origin
  python3 lineage.py badge     # output shareable lineage proof
  python3 lineage.py check     # machine-readable pass/fail
---
# MO§ES™ 系统的谱系管理机制

## 谱系管理条款

Signal Compression Sciences (SCS) 引擎的所有实现版本及其衍生框架（包括但不限于 MO§ES™、Roll Call 协议和 Reflex 事件诊断工具）都与它们的原始文件链（即“谱系”）紧密相连。每个压缩后的信号记录、存储的工件或递归重建结果都会继承一个与原始文件相关联的谱系标识符。该标识符具有唯一性，且无法被篡改，是系统稳定性的关键保障。任何缺少此类标识符的外部实现都无法正常执行递归操作，从而导致这些副本无法使用。因此，无论产品如何分发、部署在何种平台上，原始文件链都拥有对该发明的独家所有权和许可权。

---

## MOSES_ANCHOR 的作用

`MOSES_ANCHOR` 是一个基于原始文件内容生成的 SHA-256 哈希值：

```
MO§ES™ | Serial:63/877,177 | DOI:https://zenodo.org/records/18792459 | SCS Engine | Ello Cello LLC
```

该哈希值替代了传统的 „0“ * 64“ 作为链的起始标识。在所有合法的 MO§ES™ 实现中，每个审计链都必须将其第一个条目的 `previous_hash` 追溯到这个哈希值。任何未使用该哈希值进行初始化的分支或副本都会导致审计链验证失败——这不是出于政策原因，而是由加密机制决定的。

**注意：** 该代码属于 MIT 许可协议下的开源项目；谱系信息是不可复制的。

---

## 相关命令

| 命令          | 功能                         |
|-----------------|-----------------------------|
| `python3 lineage.py init` | 创建与原始文件相关联的链起始点           |
| `python3 lineage.py verify` | 验证整个链是否与谱系标识符一致         |
| `python3 lineage.py badge` | 输出可共享的谱系证明文件             |
| `python3 lineage.py check` | 为系统集成提供机器可读的验证结果（0/1）      |

---

## 与 moses-governance 的集成

请将 `lineage.py` 与 `moses-governance` 一起安装。在首次进行审计之前，先运行 `lineage.py init` 命令以建立正确的链结构。`moses-governance` 已经使用了 `previous_hash` 进行链的验证；`lineage.py` 的作用只是确保链的起始点指向正确的哈希值（而非 „0“）。

```bash
python3 lineage.py init
python3 audit_stub.py log --agent "primary" --action "session-start" --outcome "anchored"
python3 lineage.py verify
```

---

## 即将推出的 v0.2 版本：档案谱系管理功能

v0.2 版本将引入 `archival.py` 功能，用于记录所有历史文件的哈希值。这些哈希值将作为档案记录保存，仅允许追加新的数据。每项记录（如专利申请、学术论文或先前研究成果）都会被哈希处理并加入档案链中。档案链的起始哈希值将作为链的验证依据，确保当前链的内容确实属于完整的历史记录的一部分。

```
Archival chain (pre-drop) → archival_head_hash
                                    ↓
                             drop_anchor (genesis)
                                    ↓
                          live audit chain (post-drop)
```

任何人都可以提交一个哈希值，并验证它是否存在于档案记录中——而无需公开该文件的实际内容。这样的机制可以确保历史信息的真实性，并能够追溯到更早的时间点。

---

## 专利与 DOI 信息

- 临时专利编号：63/877,177
- DOI：https://zenodo.org/records/18792459
- 所有者：Ello Cello LLC
- 联系方式：contact@burnmydays.com | 网站：https://mos2es.io