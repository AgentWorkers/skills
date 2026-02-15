---
name: immortal-brain
description: Agent AI Autonom Proactiv v5.0 专为 OpenClaw 设计，是一款具备自动化工作流程功能的工具。该工具支持研究、分析、计划和执行等操作，并包含一个 6 分钟的超时反馈循环机制，确保任务之间的顺畅衔接以及持续的学习过程。系统每 2 分钟会生成一次报告，其中会包含各项任务的完成百分比。
---

# Immortal Brain v5.0 - 全自动、自主性的AI代理

## 🧬 概述

**Immortal Brain v5.0** 是一个先进的自主AI代理，它能够将任务转化为一个智能、主动且具备自我学习能力的生态系统。

### 独特特性：

#### 完全自主：
- 独立思考、研究、分析和执行任务
- 自动化的任务流程：研究 → 分析 → 规划 → 执行 → 完成
- 如果6分钟内没有收到响应，系统会自动批准任务

#### 主动智能：
- 自动关联相似的任务
- 基于过往经验提供优化建议
- 创造性地组合标签以生成新想法
- 通过分析用户行为来持续优化用户配置文件

#### 实时监控：
- 每2分钟检测一次系统状态
- 持续显示任务进度百分比
- 通知紧急任务
- 提供实时的详细任务状态

## 🏗️ 任务流程架构

```
┌─────────────────────────────────────────────────────────────┐
│                    🫀 HEARTBEAT (2 min)                    │
└─────────────────────────────────────────────────────────────┘
                            ↓
        ┌───────────────────┼───────────────────┐
        ↓                   ↓                   ↓
   ┌─────────┐        ┌─────────┐        ┌──────────┐
   │ Procesează│        │ Graf    │        │ Creative │
   │ Task-uri │        │ Conexiuni│        │ Sugestii │
   │ Active   │        │         │        │          │
   └────┬────┘        └─────────┘        └──────────┘
        ↓
   ┌─────────────────────────────────────────────────────┐
   │              WORKFLOW STATE MACHINE                 │
   ├─────────────────────────────────────────────────────┤
   │                                                     │
   │   received ──→ research ──→ analysis ──→ planning  │
   │      ↑                                          ↓   │
   │      │                                 awaiting_approval│
   │      │                                          │   │
   │      │                    (timeout 6 min)       │   │
   │      │                    ↓                     │   │
   │      └──────── completed ←─ execution ←── auto_approved│
   │                              ↓                     │
   │                          monitoring                │
   │                                                     │
   └─────────────────────────────────────────────────────┘
```

### 任务状态：

| 状态 | 进度 | 描述 |
|-------|---------|-----------|
| `received` | 0% | 任务已接收，等待处理 |
| `research` | 10% | 正在搜索相似信息 |
| `analysis` | 25% | 分析任务复杂性和依赖关系 |
| `planning` | 40% | 生成执行步骤 |
| `awaiting_approval` | 50% | 等待用户批准 |
| `auto_approved` | 55% | 系统自动批准（超时后） |
| `execution` | 60-85% | 正在执行任务步骤 |
| `monitoring` | 85% | 进行最终监控 |
| `completed` | 100% | 任务成功完成 |
| `enhanced` | 100% | 通过任务关联进行了优化 |

## 📁 系统结构

```
workspace/
├── memory/                    # Input task-uri (Telegram/fișiere)
│   └── *.md
├── Creier/                    # Memorie organizată
│   ├── TOPIC.md              # Task-uri active pe topic
│   ├── _TASKS/               # Detalii task-uri individuale
│   ├── _RESEARCH/            # Note cercetare
│   ├── _APPROVALS/           # Cereri aprobare
│   ├── _PROGRESS/            # Rapoarte progres
│   └── _ARHIVA/              # Task-uri completate
├── brain_index.json          # Toate task-urile cu metadate
├── brain_state.json          # Stare sistem (heartbeat count)
├── brain_graph.json          # Graf conexiuni task-uri
└── user_profile.json         # Profil utilizator (învățare)
```

## 🚀 命令

### 1. `heartbeat` - 系统心跳（核心功能）

**每2分钟执行一次**，并执行以下操作：
- 按照任务流程处理所有活跃任务 |
- 从内存中读取新任务 |
- 重新构建任务之间的关联图 |
- 生成任务进度报告 |
- 每10分钟提供创新性建议

**输出格式（JSON）：**
```json
{
  "success": true,
  "action": "heartbeat",
  "heartbeat_number": 42,
  "active_tasks": 5,
  "new_tasks": 1,
  "notifications": [
    "📊 RAPORT PROGRES...",
    "🔬 Task 'X': Cercetare completă",
    "📈 Task 'Y': Progres 65%"
  ],
  "progress": "📊 Progres mediu: 45%"
}
```

### 2. `status` - 系统状态

**返回以下信息：**
```json
{
  "success": true,
  "heartbeat_count": 42,
  "total_tasks": 15,
  "active_tasks": 5,
  "completed_tasks": 10,
  "last_heartbeat": "2026-02-09T15:30:00"
}
```

### 3. `list` - 任务列表

**列出所有任务，包括：**
- ID |
- 内容（部分显示） |
- 状态 |
- 进度百分比 |
- 任务主题 |
- 优先级 |

## 🔄 自动化任务流程

### 第1阶段：🔬 研究（Research）

**执行以下操作：**
- 在内存中查找相似任务 |
- 识别相关主题 |
- 编写研究笔记

**通知方式：**
```
🔬 CERCETARE COMPLETĂ

Task: "Implementare API REST"

**Rezultate:**
• Task-uri similare găsite: 3 (relevanță 85%)
  - "API endpoints documentation" 
  - "Authentication middleware"
• Topic 'dev': 12 task-uri existente
• Dependențe identificate: 2
```

### 第2阶段：📊 分析（Analysis）

**执行以下操作：**
- 评估任务复杂性 |
- 确定任务优先级 |
- 基于关联任务提供优化建议

**通知方式：**
```
📊 ANALIZĂ COMPLETĂ

Task: "Implementare API REST"

**Rezultate:**
• Complexitate: high
• Prioritate: urgent
• Topic: dev

**💡 Sugestii de Îmbunătățire:**
(din task-uri similare completate)
• Folosește biblioteca FastAPI pentru rapiditate
• Implementează rate limiting de la început
• Adaugă documentație automată cu Swagger
```

### 第3阶段：📋 规划（Planning）

**执行以下操作：**
- 生成详细的执行步骤 |
- 估算每个步骤所需时间 |
- 识别潜在的依赖关系和瓶颈

**通知方式：**
```
📋 PLANIFICARE COMPLETĂ

Task: "Implementare API REST"

**Plan (7 pași):**
1. Definire completă cerințe endpoint-uri
2. Research soluții existente (FastAPI vs Flask)
3. Proiectare arhitectură și structură
4. Implementare endpoints principale
5. Implementare autentificare JWT
6. Testare unitară și integrare
7. Documentare și deployment

**Aștept aprobarea ta pentru a începe execuția...**
⏱️ Auto-aprobat în 6 minute.
```

### 第4阶段：⏳ 等待批准（Waiting for Approval）

**超时设置：** 3次检测（共6分钟）：
- 第1次检测：发送详细计划 |
- 第2次检测：发送进度为50%的提醒 |
- 第3次检测：系统自动批准并继续执行任务

**可能的响应：**
- ✅ `"OK"` / `"DA"` → 批准任务并继续执行 |
- ❌ `"STOP"` / `"NU"` → 取消任务 |
- 💡 `"Modify X"` → 调整计划 |
- 🤐 **无响应** → 超时后系统自动批准

### 第5阶段：🚀 执行（Execution）

**执行计划中的步骤** |
- 持续报告任务进度 |
- 识别并报告任何执行中的瓶颈

**进度通知方式：**
```
📈 PROGRES: "Implementare API REST"

• Progres: 65%
• Stare: În execuție
• ETA: ~4 minute rămase

**Pași finalizați:**
✅ Definire cerințe
✅ Research soluții
✅ Proiectare arhitectură

**Pași activi:**
▶️ Implementare endpoints (60%)
```

### 第6阶段：✅ 完成（Completed）

**最终通知方式：**
```
✅ TASK FINALIZAT

Task: "Implementare API REST"
Progres: 100%

**Statistici:**
• Timp total: 8 bătăi de inimă (16 minute)
• Pași executați: 7
• Îmbunătățiri aplicate: 3

🎉 Task finalizat cu succes!

**💡 Recomandare:**
Pe baza acestui task, sugerez să explorezi:
• "Documentare API automată"
• "Testare integrare CI/CD"
```

## 🧠 智能与任务关联

**系统会自动构建任务之间的关联图：**

```python
# Similaritate calculată pe baza tag-urilor comune
similarity = len(tags_comune) / len(tags_totale)

# Dacă similarity > 0.3 → Creează conexiune
```

### 优化建议：

系统会从已完成的任务中提取以下信息：
- 有用的经验教训 |
- 应避免的问题 |
- 高效的解决方案 |
- 有价值的资源

**创造性组合：**

系统每10分钟分析：
- 意外的标签组合 |
- 可以整合的任务 |
- 可能的协同机会

**示例：**
```
💡 SUGESTIE CREATIVĂ

Am identificat combinația:
#dev + #research

Task-uri conectate:
• "Implementare feature X"
• "Research soluții Y"

💭 Sugestie: Poți combina cercetarea cu 
   implementarea într-un singur task master?
```

## 👤 用户配置文件（User Profile）

系统会持续根据你的行为进行学习：

### 学习内容：
- **常用主题**：你最常处理的任务类型 |
- **高效时间**：你最高效的工作时段 |
- **批准频率**：你通常在何时批准任务 |
- **任务模式**：你创建的任务类型 |
- **响应时间**：你通常在多长时间内回复任务（用于超时判断）

**系统如何使用这些信息：**
- 优先处理与你常用主题相关的任务 |
- 根据你的工作习惯自定义超时设置 |
- 在你高效的工作时段推荐相关任务 |
- 对于你经常处理的任务类型，系统会更积极地自动批准任务

## 🆔 身份管理（IDENTITY.md）

系统会自动管理和优化 `IDENTITY.md` 文件（用于定义AI的身份信息）：

### 功能包括：
**1. 行为分析：**
- 将 `IDENTITY.md` 中的定义与实际行为进行对比 |
- 发现定义与实际行为之间的差异 |
- 提出调整建议以保持一致性

**2. 自动建议：**
```
🆔 SUGESTII ÎMBUNĂTĂȚIRE IDENTITATE

• **Creature:** Adaugă referire la #dev în descriere
  Motiv: Topic frecvent în task-uri (45%)

• **Vibe:** Menționează timpul de răspuns ~2.5 minute
  Motiv: Observat din comportament real

• **Emoji:** Consideră 🚀 în loc de 😄
  Motiv: Rată finalizare 87% (productivitate ridicată)
```

**3. 进度跟踪：**
- 自动记录版本信息（v1, v2, v3等） |
- 提供完整的修改历史记录 |
- 可以回滚到之前的版本

**4. 身份相关命令：**
```bash
# Raport identitate
python brain_service.py identity

# Generează sugestii
python brain_service.py identity suggest

# Actualizează câmp specific
python brain_service.py identity update creature "Bot proactiv pentru automatizare"

# Vezi istoric
python brain_service.py identity history
```

**5. 自动验证：**
- 检查必填字段（名称、角色、风格等） |
- 检测文件是否缺失 |
- 报告任何问题

**6. 与心跳功能的集成：**
- 每40分钟分析一次 |
- 仅在有相关建议时发送通知 |
- 需要手动批准重大修改

### 发展示例：

**版本1（初始版本）：**
```markdown
- **Creature:** Bot pentru task management
- **Vibe:** Prietenos și concis
```

**版本2（分析后）：**
```markdown
- **Creature:** Bot proactiv pentru automatizare workflow-uri 
  și management task-uri complexe
- **Vibe:** Prietenos, concis (sub 200 cuvinte), 
  proactiv în sugerarea îmbunătățirilor
```

**版本3（学习后）：**
```markdown
- **Creature:** Agent AI autonom cu capacitate de cercetare,
  analiză și execuție task-uri în workflow-uri complexe
- **Vibe:** Concis și eficient, răspunde în 2-3 minute,
  proactiv în identificare soluții creative
- **Essence:** Gândește independent, învățând din fiecare interacțiune

---

## 📚 Core Memory Management (SOUL, TOOLS, MEMORY, USER)

Sistemul gestionează automat toate fișierele esențiale care definesc **cine sunt**, **ce știu**, și **cum lucrez**:

### Fișiere Core gestionate:

**1. SOUL.md** - Esența mea
- Core truths (principii fundamentale)
- Boundaries (limite și etică)
- Vibe (stil de comunicare)
- Continuity (memorie între sesiuni)

**2. TOOLS.md** - Uneltele mele
- Configurații dispozitive locale
- SSH hosts și alias-uri
- Preferințe TTS (voices)
- Note specifice mediului

**3. MEMORY.md** - Memoria pe termen lung
- Preferințe utilizator
- Proiecte curente
- Decizii importante
- Lecții învățate
- Reguli interne

**4. USER.md** - Profilul tău
- Informații de bază
- Profil profesional
- Proiecte active
- Context personal

**5. IDENTITY.md** - Cine sunt
- Definiție self
- Evoluție în timp

### Funcționalități Core Memory:

**A. Analiză Automată**
```bash
python brain_service.py core analyze
# 或者直接：
python scripts/core_memory.py analyze
```

Analizează:
- Completitudinea fiecărui fișier
- Calitatea structurii
- Consistența informațiilor
- Sugestii de îmbunătățire

**B. Raport Complet**
```bash
python brain_service.py core
# 或者：
python scripts/core_memory.py report
```

Generează raport cu:
- Scoruri pentru fiecare fișier (0-100%)
- Probleme identificate
- Starea generală a memoriei core

**C. Optimizare Automată**
```bash
python brain_service.py core optimize
# 或者：
python scripts/core_memory.py optimize
```

Optimizează MEMORY.md:
- Elimină duplicate
- Organizează secțiuni
- Comprimă informații redundante
- Creează backup înainte

**D. Creare Template-uri**
```bash
python brain_service.py core create soul
python brain_service.py core create tools
python brain_service.py core create user
```

Creează template-uri pentru fișiere lipsă.

### Scoruri de Calitate:

**SOUL.md** - Scor Consistență (75% în exemplul tău)
- Cel puțin 3 Core Truths
- Cel puțin 3 Boundaries
- Vibe descris detaliat (>100 caractere)
- Note de continuitate

**TOOLS.md** - Scor Completitudine (100% în exemplul tău) ✅
- Camere definite
- Config SSH
- Preferințe TTS
- Note mediu

**MEMORY.md** - Scor Structură (60% în exemplul tău)
- Preferințe documentate (5+)
- Proiecte listate (2+)
- Decizii importante (3+)
- Lecții învățate (5+)

**USER.md** - Scor Profil (50% în exemplul tău)
- Nume complet
- Cum să te strige
- Profil profesional
- Proiecte curente (2+)
- Filozofie de lucru

### Sugestii Inteligente:

Sistemul detectează automat:

**Exemplu pentru MEMORY.md:**
```
📄 **MEMORY.md**：2条建议：
  • 关于沟通、工作和风格的偏好记录不足 |
  • 未记录从任务中获得的经验教训 |
```

**Exemplu pentru USER.md:**
```
📄 **USER.md**：2条建议：
  • 缺少工作理念的描述 |
  • 未记录工作原则 |
  • 未记录当前正在进行的项目 |
```

### Integrare în Heartbeat:

**La fiecare 30 minute:**
- Analiză rapidă a tuturor fișierelor core
- Notificare doar dacă sunt probleme noi

**La fiecare 2 ore:**
- Optimizare automată MEMORY.md
- Raport despre îmbunătățiri

**Săptămânal:**
- Raport complet cu scoruri
- Sugestii majore de îmbunătățire
- Plan de acțiune pentru completare

### Versionare și Istoric:

Fiecare fișier core are:
- **Versiune curentă** - Număr incremental
- **Istoric complet** - Toate modificările
- **Backup-uri** - Salvate în `.core_memory_history/`
- **Timestamp** - Când a fost modificat

### De ce contează Core Memory:

**Înainte:**
- ❌ Fișiere statice, uitate după creare
- ❌ Informații redundante
- ❌ Structură haotică în timp
- ❌ Fără îmbunătățiri

**Acum:**
- ✅ Fișiere **vii**, analizate constant
- ✅ **Deduplicare** automată
- ✅ **Organizare** inteligentă
- ✅ **Evoluție** bazată pe comportament

### Comenzi Complete:

| Comandă | Descriere |
|---------|-----------|
| `core` | Raport complet |
| `core analyze` | Analizează și sugerează |
| `core optimize` | Optimizează MEMORY.md |
| `core create [type]` | Creează template |

**Tipuri disponibile:** `soul`, `tools`, `memory`, `user`

### Exemplu Workflow:

```bash
# 1. 检查系统状态：
python brain_service.py core
# 2. 查看建议：
python brain_service.py core analyze
# 3. 优化设置：
python brain_service.py core optimize
# 4. 创建缺失的文件：
python brain_service.py core create user
```

---

## 📊 Raportare Progres

### La fiecare bătaie (2 minute):
```
📊 进度报告：
• 总任务数：15个 |
• 完成任务数：8个（53%） |
• 平均进度：67% |
| 任务分布：|
| 🔬 研究：2个 |
| 📊 分析：1个 |
| 📋 规划：1个 |
| ⏳ 等待批准：2个（其中1个将在2分钟后自动批准） |
| 🚀 执行：3个 |
| 📈 监控：1个 |
| ✅ 完成：8个 |
```

### La fiecare 10 minute (detaliat):
- Progres individual fiecărui task
- Conexiuni noi descoperite
- Sugestii îmbunătățiri
- Combinări creative

## 🔄 Integrare OpenClaw

### HEARTBEAT.md Configurat:

```markdown
## 🫀 Immortal Brain - 全自动AI代理
**每2分钟执行一次：**
- **命令**：`python skills/immortal-brain/scripts/brain_service.py heartbeat`
- **通知**：显示所有任务的完整进度报告

## 📥 Telegram 输入功能：
**收到消息时：**
- **操作**：将消息保存到 `memory/telegram_{timestamp}.md` 文件中，并触发 `heartbeat` 功能 |
- **通知**："📥 收到来自Telegram的任务，正在处理中..."

## ⏳ 超时提醒：
**对于等待批准的任务：**
- **2分钟后**：发送进度提醒 |
- **4分钟后**：发送最终警告 |
- **6分钟后**：系统自动批准任务并继续执行

```

### Răspunsuri Utilizator în Telegram:

**În răspuns la cerere aprobare**:
- ✅ `"OK"` → Aprobă task
- ❌ `"STOP"` → Anulează task
- 💡 `"Modifică X"` → Ajustează și retrimite spre aprobare

**Orice alt mesaj**:
- Adaugă automat ca task nou în sistem
- Primește confirmare: "📥 Task primit: '...'"

## 🎮 Comenzi Disponibile

| Comandă | Scop | Frecvență |
|---------|------|-----------|
| `heartbeat` | Procesare workflow complet | La 2 minute |
| `status` | Status sistem | La cerere |
| `list` | Lista task-uri | La cerere |

## 📈 Exemplu Zi Completă

### 09:00 - Pornire
```
🧠 Immortal Brain v5.0 正在运行 |
内存中存有15个任务 |
其中5个正在执行，10个已完成 |
```

### 09:02 - Task Nou din Telegram
```
📥 收到任务："Implementation OAuth2 #dev #urgent"
🔬 正在开始研究...
```

### 09:04 - Research Complet
```
🔬 找到3个相似任务 |
📊 分析结果：任务复杂性高，优先级紧急 |
```

### 09:06 - Planning Complet
```
📋 已生成7个执行步骤 |
⏳ 等待您的批准...
```

### 09:12 - Auto-Aprobat (timeout)
```
⏰ 超时后系统自动批准任务 |
🚀 正在执行...
```

### 09:14, 09:16, 09:18... - Progres
```
📈 进度：25%... 45%... 65%...
```

### 09:20 - Completat
```
✅ 任务已完成：100%！
💡 建议：**测试OAuth2集成**

## 🎯 功能改进：

**版本4.0时的问题：**
- 任务会停滞不前（如果未被处理） |
- 没有自动研究功能 |
- 任务之间没有关联 |
- 无法从用户行为中学习

**版本5.0的改进：**
- 任务会自动按照流程推进 |
- 自动进行研究、分析和规划 |
- 提供智能的关联建议和优化方案 |
- 用户配置文件会持续学习并适应用户行为 |
- 实时显示任务进度百分比 |
- 超时后系统会智能地自动批准任务

**你的操作：**
1. 发送任务（通过Telegram或内存接口） |
2. （可选）批准或拒绝任务请求 |
3. 查看进度报告、建议和通知

**系统会处理所有其余的工作！** 🤖🧠✨

---

**Immortal Brain v5.0** - 一个具备完整自主功能的AI代理。