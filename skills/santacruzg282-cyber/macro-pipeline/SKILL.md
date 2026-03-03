---
name: macro-pipeline
description: 使用 `PIPELINE.md` 和 `HEARTBEAT.md` 模式来创建和管理宏任务流水线（包括质量测试、路线图制定、功能发布等）。这种模式适用于构建多步骤的项目计划，这些计划可由代理程序通过 `cron` 自动执行。
metadata:
  { "openclaw": { "emoji": "🔧" } }
---
# Macro Pipeline Skill v3

## 架构

### 两个文件，两个位置：

| 文件 | 位置 | 用途 | 是否可修改？ |
|------|----------|---------|----------|
| `PIPELINE.md` | **项目仓库** (`~/Documents/proyectos/<project>/`) | 状态与进度信息 | ✅ 可修改（子代理可直接更新） |
| `HEARTBEAT.md` | **代理工作区** (`~/.openclaw/workspace-<agent>/`) | 操作指令 | ❌ 不可修改（使用 `chflags uchg` 加锁保护） |

### 为什么将 `PIPELINE.md` 存放在仓库中？
- 子代理在仓库中工作，因此可以更新状态而不会引发路径问题
- 可通过 Git 追踪进度（提交记录会显示步骤完成情况）
- 可避免因路径访问失败导致的“僵尸步骤”（即未完成的步骤）

### 为什么将 `HEARTBEAT.md` 存放在工作区中？
- 包含 OpenClaw 代理的操作指令
- 避免污染项目代码
- 使用 `chflags uchg` 加锁，防止代理覆盖自己的指令

---

## `PIPELINE.md` 的格式

```markdown
# PIPELINE — <Project Name>: <Pipeline Title>
# Proyecto: ~/Documents/proyectos/<project>
# Objetivo: <one-line goal>
# Creado: YYYY-MM-DD

## Step 1: <Title> [PENDING]
- engine: claude-code
- description: <what to do>
- files: <key files to touch>
- verify: <command that proves step is done>
- artifacts: <outputs for next steps>

## Step 2: <Title> [PENDING]
- engine: claude-code
- depends_on: [1]
- description: <what to do>
- verify: <verification command>
```

### 状态值：
- `[PENDING]` — 未开始
- `[RUNNING YYYY-MM-DDTHH:MM]` — 正在运行（包含时间戳）
- `[✅ COMPLETED]` — 已完成
- `[FAILED]` — 失败（包含失败原因）
- `[BLOCKED]` — 等待人工操作或外部依赖项完成

### 各步骤的字段：
- `engine:` — `claude-code` | `human` | `deploy`  
- `depends_on:` — 必须先完成的步骤编号列表  
- `parallel:` — 可同时运行的步骤列表  
- `verify:` — 用于验证步骤是否完成的 shell 命令  
- `artifacts:` — 传递给依赖步骤的输出结果  
- `files:` — 被修改的关键文件  

---

## `HEARTBEAT.md` 的格式

```markdown
# HEARTBEAT — <Agent Name>

> ⚠️ NUNCA modifiques este archivo (HEARTBEAT.md). Es read-only.

## Pipeline activo: ~/Documents/proyectos/<project>/PIPELINE.md

## Protocolo cada heartbeat:
1. Lee el pipeline activo (ruta absoluta arriba)
2. Si hay step [PENDING] sin dependencias bloqueadas → ejecútalo
3. Marca [RUNNING YYYY-MM-DDTHH:MM] con timestamp actual
4. Ejecuta: sessions_spawn(task=..., thread=true)
5. Un step por heartbeat máximo

## Zombie Detection
Si un step lleva >2h en [RUNNING], resetear a [PENDING] y reportar.

## En sesión activa con usuario
Priorizar responder. HEARTBEAT_OK.
```

---

## Cron 安排

始终使用 CLI 进行调度，切勿直接编辑 `openclaw.json`：
```bash
openclaw cron add --name "<Project> Pipeline" --agent <agent-id> --every 30m --message "Heartbeat: lee HEARTBEAT.md y ejecuta siguiente step"
```

### 避免任务冲突的调度策略：
- `:00/:30` → A 组  
- `:15/:45` → B 组  

---

## 子代理任务模板

在任务提示中包含以下内容：
```
Al terminar:
1. Actualiza <absolute-path-to-PIPELINE.md>: cambia Step X de [RUNNING] a [✅ COMPLETED] con output y artifacts
2. Si fallas, marca [FAILED] con el error
3. Notifica a Discord (action=send, channel=discord, target="channel:<id>") con resumen
```

---

## 每个项目可以有多个 Pipeline

一个代理可以拥有多个 `PIPELINE.md` 文件。`HEARTBEAT.md` 文件用于指定任务的优先级顺序：
```
Lee PIPELINE_ACTIVE.md (prioritario). Si todos completados, lee PIPELINE.md como fallback.
```

---

## 并行执行

没有交叉依赖关系的步骤可以同时执行：
```markdown
## Step 1: Task A [PENDING]
- parallel: [2, 3]

## Step 2: Task B [PENDING]
- parallel: [1, 3]

## Step 3: Task C [PENDING]
- parallel: [1, 2]

## Step 4: Task D [PENDING]
- depends_on: [1, 2, 3]
```
如果步骤之间没有依赖关系，`HEARTBEAT` 可以在同一周期内并行执行多个步骤。

---

## Git 标签

每个完成的步骤都应创建一个 Git 标签：
```bash
git add . && git commit -m "pipeline/<project>/step-<N>: <step title>"
```
这有助于在 Git 日志中完整追踪项目进度。

---

## 重要规则：
1. `PIPELINE.md` 必须始终存放在仓库中，绝不能放在工作区。
2. `HEARTBEAT.md` 必须始终放在工作区中，绝不能放在仓库中。
3. `HEARTBEAT.md` 是不可修改的（使用 `chflags uchg` 加锁保护）。
4. 使用 CLI 进行 Cron 安排，切勿直接编辑 `openclaw.json`。
5. 每个步骤对应一个 `HEARTBEAT` 文件，以避免系统过载（除非明确指定了并行执行）。
6. 每个步骤都必须包含验证命令 (`verify`)。
7. 在 `HEARTBEAT.md` 中使用绝对路径（例如 `~/Documents/proyectos/...`）。
8. 每个步骤都应创建一个 Git 标签，格式为 `pipeline/<project>/step-<N>: <title>`。
9. 明确指定并行执行的步骤（使用 `parallel:`）。