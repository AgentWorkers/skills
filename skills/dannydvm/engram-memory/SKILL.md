---
name: engram
description: "用于AI代理的持久性语义记忆系统——本地化、速度快且免费。当代理需要回顾过去的决策、存储新的信息或偏好设置、搜索对话历史记录，或在不同会话之间保持上下文时，可以使用该系统。"
metadata:
  openclaw:
    emoji: "🧠"
    requires:
      bins: ["engram"]
    install:
      - id: node
        kind: node
        package: engram-memory
        bins: ["engram"]
        label: "Install Engram (npm)"
---

# Engram — 代理内存系统

Engram 是一个基于生物记忆机制构建的本地语义记忆系统，支持类型化的记忆存储以及记忆之间的关联关系表示。该系统不使用 API 密钥，也不依赖于云端存储。

## 启动序列

```bash
engram search "<current task or context>" --limit 10
```

在使用系统之前，请务必先进行记忆的检索。被检索过的记忆会提升其显著性（即被标记为更重要的记忆）。

## 存储机制

```bash
engram add "Client uses React with TypeScript" --type fact --tags react,client
engram add "We decided to pause ads" --type decision --tags ads
echo "Raw conversation text" | engram ingest
```

记忆的类型包括：事实（fact）、决策（decision）、偏好（preference）、事件（event）和关系（relationship）。

## 搜索功能

```bash
engram search "what tech stack"
engram search "pricing decisions" --type decision
engram search "client status" --agent client-agent
```

## 记忆之间的关系

```bash
engram relate <src> <tgt> --type supports
engram auto-relate <id>
engram relations <id>
```

记忆之间的关系类型包括：相关于（related_to）、支持（supports）、矛盾（contradicts）、由……引起（caused_by）、取代（supersedes）、属于……的一部分（part_of）以及引用（references）。

## 关键概念

- **记忆衰减**：未被使用的记忆会随着时间的推移而逐渐丧失显著性；被检索过的记忆则会提升其显著性。
- **记忆类型**：系统支持根据记忆的类型（事实、决策、偏好、事件、关系）进行过滤。
- **记忆范围**：记忆可以分为全局（global）、代理私有（agent-private）和共享（shared）三种类型。
- **去重机制**：当记忆之间的相似度超过 92% 时，系统会自动合并这些重复的记忆。

## 快速参考

```bash
engram stats
engram recall --limit 10
engram export > backup.json
engram import backup.json
```