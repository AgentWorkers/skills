# 技能：OpenExec — 受管控的确定性执行

## 概述

OpenExec 为需要执行实际操作的人工智能代理提供了一个受管控的执行接口。该接口遵循以下严格原则：

> 任何执行行为都必须经过外部管控机构的批准才能进行。

该技能将推理、授权和执行过程分离为三个独立的层次。

---

## 分类

基础设施 / 管控 / 执行

---

## 该技能的功能

- 接收结构化的执行请求
- 需要通过 ClawShield 获得明确的管控批准
- 以确定性方式执行操作
- 通过 ClawLedger 发布不可篡改的执行记录

---

## 该技能不执行的功能

- 不负责制定政策
- 不授予权限
- 不进行自主推理
- 不自行批准执行
- 不会覆盖管控机构的决策

---

## 架构背景

该技能运行在一个三层结构的管控执行系统中：

- OpenExec：确定性执行引擎
- ClawShield：管控与审批系统
- ClawLedger：不可篡改的记录账本

每一层都是独立且可替换的。

---

## 输入

结构化的执行请求：

```json
{
  "action": "string",
  "parameters": {},
  "requested_by": "agent-id",
  "timestamp": "ISO-8601"
}
```

---

## 输出

```json
{
  "status": "executed | denied",
  "execution_id": "uuid",
  "receipt_hash": "string",
  "timestamp": "ISO-8601"
}
```