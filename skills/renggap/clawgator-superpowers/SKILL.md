---
name: ClawGator Superpowers
description: 这是一个为ClawGator团队提供的全面软件开发框架。它涵盖了头脑风暴、系统化规划、测试驱动开发（TDD）、调试、代码审查以及Git工作流管理等功能。在项目开始或代码发生任何更改之前，该框架会自动触发相应的流程。
---

# ClawGator 超级技能

这是一个为 ClawGator 团队量身定制的完整软件开发框架。它基于 obra/superpowers 架构开发，但根据 ClawGator 的具体需求进行了优化。

## 何时使用这些技能

**务必在以下情况下使用这些技能：**
- 开始开发新功能或组件
- 修改软件的行为或功能
- 修复漏洞或问题
- 对代码进行重大修改
- 制定实施计划

**对于以下情况可以直接跳过这些技能：**
- 简单的问题或信息查询
- 单行命令
- 查看项目进度（使用相关技能）

## 完整的工作流程

```
Permintaan Pengembangan
    ↓
┌──────────────────────┐
│  USING SUPERPOWERS   │ ← Skill utama - memandu semua langkah
│  (skill dasar)       │   - Menemukan skill yang relevan
│                      │   - Menentukan prioritas skill
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│   BRAINSTORMING      │ ← Memahami requirement & desain
│  (jika butuh desain) │   - Tanya pertanyaan satu per satu
│                      │   - Usulkan 2-3 pendekatan
│                      │   - Validasi desain incrementally
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│  USING GIT WORKTREES│ ← Setup workspace terisolasi
│  (sebelum coding)    │   - Create branch baru
│                      │   - Setup project
│                      │   - Verify baseline tests
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│   WRITING PLANS      │ ← Buat rencana implementasi
│  (jika multi-task)   │   - Pecah jadi tasks kecil (2-5 min)
│                      │   - Exact file paths & complete code
│                      │   - Include TDD steps
└──────────┬───────────┘
           ↓
    ┌──────┴──────┐
    │             ↓
    │  ┌──────────────────────┐
    │  │ SUBAGENT-DRIVEN DEV  │ ← Eksekusi via subagent (option 1)
    │  │  (sesi ini)          │   - Fresh subagent per task
    │  │                      │   - Review antar task
    │  └──────────┬───────────┘
    │
    │  ┌──────────────────────┐
    │  │   EXECUTING PLANS    │ ← Eksekusi batch (option 2)
    │  │  (sesi terpisah)     │   - Batch execution
    │  │                      │   - Review checkpoints
    │  └──────────┬───────────┘
    │
    ↓  ↓
┌──────────────────────┐
│ TEST-DRIVEN DEVELOPMENT │ ← WAJIB untuk semua coding
│  (selalu aktif)         │   - RED: Tulis test, lihat fail
│                        │   - GREEN: Implement minimal code
│                        │   - REFACTOR: Clean up
└──────────┬─────────────┘
           ↓
┌──────────────────────┐
│ SYSTEMATIC DEBUGGING  │ ← Jika ada bug/issue
│  (jika error muncul)  │   - Phase 1: Investigasi root cause
│                      │   - Phase 2: Analisis pola
│                      │   - Phase 3: Hipotesis & testing
│                      │   - Phase 4: Fix & verify
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│   CODE REVIEW        │ ← Review antar tasks
│  (antara tasks)      │   - Requesting: Review code
│                      │   - Receiving: Apply feedback
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│   VERIFICATION       │ ← Konfirmasi benar-bener fix
│  (sebelum selesai)   │   - Test lagi
│                      │   - Cek regressions
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ FINISHING DEV BRANCH │ ← Selesai branch
│  (setelah semua)     │   - Verify tests
│                      │   - Present options:
│                      │   * Merge ke main
│                      │   * Buat PR
│                      │   * Keep branch
│                      │   * Discard
└──────────────────────┘
```

## 可用的子技能

### 🎯 核心流程技能

| 技能 | 使用时机 | 功能 |
|-------|--------------|--------|
| **using-superpowers** | 每次对话开始时 | 指导技能的使用 |
| **brainstorming** | 编码前 | 理解需求和设计 |
| **writing-plans** | 设计方案确定后 | 制定实施计划 |
| **executing-plans** | 计划准备好后 | 执行计划 |
| **finishing-a-development-branch** | 开发分支完成后 | 完成分支的工作 |

### 🔨 执行技能

| 技能 | 使用时机 | 功能 |
|-------|--------------|--------|
| **subagent-driven-development** | 选择此执行方式时 | 为每个任务分配新的子代理 |
| **dispatching-parallel-agents** | 并行处理任务 | 分配多个代理来执行任务 |

### 🧪 质量控制技能

| 技能 | 使用时机 | 功能 |
|-------|--------------|--------|
| **test-driven-development** | 编码前 | 采用测试驱动的开发方法（TDD） |
| **systematic-debugging** | 发现漏洞时 | 进行四阶段根源分析 |
| **verification-before-completion** | 任务完成前 | 确认问题已彻底解决 |

### 🔧 Git 与代码审查技能

| 技能 | 使用时机 | 功能 |
|-------|--------------|--------|
| **using-git-worktrees** | 在新分支开始编码前 | 创建隔离的开发环境 |
| **requesting-code-review** | 任务之间 | 提交代码以供审查 |
| **receiving-code-review** | 收到反馈后 | 根据反馈修改代码 |

### 📝 元技能

| 技能 | 使用时机 | 功能 |
|-------|--------------|--------|
| **writing-skills** | 创建新技能 | 构建 OpenClaw 的技能体系 |

## 主要原则

### 铁律
1. **没有经过测试的代码绝不能投入生产环境（TDD）**
2. **在修复问题之前必须先找到问题的根本原因**
3. **即使认为某个技能只有 1% 的适用可能性，也必须使用它**

### TDD 循环

```
RED → Write failing test → Verify fails
GREEN → Implement minimal code → Verify passes
REFACTOR → Clean up → Stay green
REPEAT → Next test
```

### 调试流程

```
Phase 1: Root Cause Investigation
  - Read errors carefully
  - Reproduce consistently
  - Check recent changes
  - Trace data flow

Phase 2: Pattern Analysis
  - Find working examples
  - Compare against references
  - Identify differences

Phase 3: Hypothesis & Testing
  - Form single hypothesis
  - Test it
  - Learn & iterate

Phase 4: Fix & Verify
  - Implement fix at root cause
  - Verify with original issue
  - Run all tests
```

## 技能优先级

当多个技能都可能适用时，优先顺序如下：
1. **流程相关技能**（brainstorming, debugging, writing-plans）
2. **质量控制技能**（TDD, systematic-debugging）
3. **Git/代码审查技能**（using-git-worktrees, code-review）
4. **执行相关技能**（executing-plans, subagent-driven-development）

**示例流程：**
- “让我们开发 X 功能” → 进行头脑风暴 → 使用 using-superpowers → 制定实施计划 → 执行计划
- “修复这个漏洞” → 进行系统化调试 → 使用 TDD
- “添加新功能 X” → 如果简单可以直接使用 TDD（无需制定计划）

## 与 OpenClaw 的集成

这些技能与 OpenClaw 完全集成：
- ✅ 当输入 “build”, “create”, “implement”, “fix”, “add” 等关键字时，相关技能会自动触发
- ✅ `skills/` 文件夹中包含 14 个完整的子技能
- ✅ 子技能会根据上下文自动触发
- ✅ `using-superpowers` 是所有技能的入口点
- ✅ 提供了 `brainstorm`, `plan_review`, `get_status` 等辅助工具
- ✅ 支持 `subagent-driven-development` 的 OpenClaw 代理机制

## ClawGator 团队的应用

ClawGator 团队使用这些技能来：
- 🔨 开发 OpenClaw 的新功能
- 🚀 构建整个平台
- 🔧 修复漏洞并进行改进
- 📝 规划产品开发
- 💡 产生新想法
- 🔍 进行系统化的调试
- ✅ 使用 TDD 进行测试
- 📊 在任务之间进行代码审查

这些技能确保团队始终遵循以下原则：
- **先思考再编码**
- **先规划再开发**
- **完成验证后再发布**
- **在生产环境之前进行测试**

## 文件夹结构

```
/home/clawgator-superpowers/
├── SKILL.md                    - Dokumentasi skill utama
├── openclaw.plugin.json        - Konfigurasi plugin
├── package.json                 - Metadata
├── brainstorming.js              - Core brainstorming function
├── index.js                     - Entry point
├── skills/                       - Sub-skills dari obra/superpowers
│   ├── using-superpowers/       - Skill dasar
│   ├── brainstorming/           - Brainstorming & desain
│   ├── writing-plans/           - Rencana implementasi
│   ├── executing-plans/         - Eksekusi plan
│   ├── test-driven-development/ - TDD workflow
│   ├── systematic-debugging/    - 4-phase debugging
│   ├── using-git-worktrees/     - Git worktrees
│   ├── subagent-driven-development/ - Eksekusi via subagent
│   ├── dispatching-parallel-agents/ - Paralel agents
│   ├── requesting-code-review/  - Review code
│   ├── receiving-code-review/   - Terima feedback
│   ├── verification-before-completion/ - Verify fix
│   ├── finishing-a-development-branch/ - Wrap up
│   └── writing-skills/          - Buat skill baru
└── README.md                     - Dokumentasi lengkap
```

## 新项目启动流程

### 新项目启动步骤

这些技能会自动执行：
1. 激活 using-superpowers
2. 进行头脑风暴以明确需求
3. 创建新的 Git 开发环境（git worktree）
4. 制定实施计划
5. 使用 TDD 进行开发
6. 进行测试并验证结果

### 修复漏洞流程

### 修复漏洞步骤

这些技能会自动执行：
1. 启用 systematic-debugging
2. 进行根源分析（四阶段）
3. 使用 TDD 实现修复
4. 验证修复效果
5. 运行所有测试

---

**版本：** 1.0.0
**适用对象：** ClawGator 团队
**基于：** obra/superpowers（100% 的工作流程，包含 14 个子技能）
**许可证：** MIT