# FIS（联邦智能系统）架构技能

> **版本**: 3.2.4-lite  
> **名称**: 联邦智能系统（Federal Intelligence System）  
> **描述**: 基于文件的多代理工作流框架。核心组件：JSON工单 + Markdown知识库（无需Python）。可选：`lib/`目录中的Python辅助工具用于徽章生成。支持与OpenClaw的QMD集成以实现语义搜索。  

> **注意**: 旧版本的FIS 3.1组件（如`memory_manager`、`skillRegistry`等）保留于GitHub仓库历史记录中，但未包含在此版本中。如需查看历史信息，请参考仓库。  
> **状态**: ✅ 稳定版本 — 架构简化，已集成QMD语义搜索功能。  

---

## 安装前须知  

**核心工作流**: 完全基于文件（JSON工单、Markdown格式），基本使用无需Python。  

**可选组件**（使用前请确认是否需要）：  
- `lib/*.py` — 徽章生成辅助工具（需安装`pip install Pillow qrcode`）  
- `lib/fis_lifecycle.py` — 用于工单管理的命令行工具（CLI）  

**依赖**: 需要`mcporter` CLI工具以集成QMD搜索功能（[OpenClaw QMD文档](https://docs.openclaw.ai/concepts/memory)）。  

**安全提示**: 在执行Python脚本前请仔细检查。核心功能可独立于这些脚本运行。  

---

## 核心原理：FIS负责管理工作流，QMD负责内容管理  

**FIS 3.2**是对FIS 3.1的重大简化。我们移除了与QMD（Query Model Direct）语义搜索功能重复的组件：  

| 组件 | FIS 3.1 | FIS 3.2 | 原因 |  
|---------|---------|---------|--------|  
| 任务管理 | Python类 + `memory_manager` | JSON格式的工单文件 | 更简洁，更易于审计 |  
| 内存/检索 | `memory_manager.py` | **QMD** | QMD具备原生语义搜索功能 |  
| 技能发现 | `skillRegistry.py` | **SKILL.md + QMD** | QMD可索引SKILL.md文件 |  
| 知识图谱 | `experimental/kg/` | **QMD** | QMD支持知识发现功能 |  
| 死锁检测 | `deadlock_detector.py` | 简化后的处理方式 | 实际应用中很少需要 |  

**保留的内容**: 仅保留FIS独有的工作流相关功能。  

---

## 3.2.0的新特性  

### 简化架构  
- **核心工作流**: 完全基于文件（JSON工单、Markdown知识库），无需Python  
- **可选辅助工具**: `lib/`目录中的Python脚本用于徽章生成（可审计，非强制使用）  
- **官方集成**: 支持与OpenClaw的QMD集成以实现语义搜索（详情见[https://docs.openclaw.ai/concepts/memory]）  
- **徽章生成器**: 为子代理生成视觉标识（需安装`Pillow`库，可选）  

### 目录结构  

---

## 快速入门  

### 1. 创建任务工单  
```bash
# Create ticket manually or use helper
cat > ~/.openclaw/fis-hub/tickets/active/TASK_EXAMPLE_001.json << 'EOF'
{
  "ticket_id": "TASK_EXAMPLE_001",
  "agent_id": "worker-001",
  "parent": "cybermao",
  "role": "worker",
  "task": "Analyze GPR signal patterns",
  "status": "active",
  "created_at": "2026-02-19T21:00:00",
  "timeout_minutes": 60
}
EOF
```  

**安全提示**: `resources`字段（例如`["file_read", "code_execute"]`）可添加到工单中，但需谨慎使用。仅在对自动化操作进行审计时才授予相应权限。  

### 2. 生成徽章图片  
```bash
cd ~/.openclaw/workspace/skills/fis-architecture/lib
python3 badge_generator_v7.py

# Output: ~/.openclaw/output/badges/TASK_*.png
```  

### 3. 完成任务并归档  
```bash
# Move from active to completed
mv ~/.openclaw/fis-hub/tickets/active/TASK_EXAMPLE_001.json \
   ~/.openclaw/fis-hub/tickets/completed/
```  

---

## 工单格式  
```json
{
  "ticket_id": "TASK_CYBERMAO_20260219_001",
  "agent_id": "worker-001",
  "parent": "cybermao",
  "role": "worker|reviewer|researcher|formatter",
  "task": "Task description",
  "status": "active|completed|timeout",
  "created_at": "2026-02-19T21:00:00",
  "completed_at": null,
  "timeout_minutes": 60,
  "resources": ["file_read", "file_write", "web_search"],
  "output_dir": "results/TASK_001/"
}
```  

---

## 工作流模式  

### 模式1：工作者 → 审核者流程  
```
CyberMao (Coordinator)
    ↓ spawn
Worker (Task execution)
    ↓ complete
Reviewer (Quality check)
    ↓ approve
Archive
```  
- `TASK_001_worker.json` → 进行中 → 完成  
- `TASK_002_reviewer.json` → 进行中 → 完成  

### 模式2：并行处理  
```
CyberMao
    ↓ spawn 4x
Worker-A (chunk 1)
Worker-B (chunk 2)
Worker-C (chunk 3)
Worker-D (chunk 4)
    ↓ all complete
Aggregator (combine results)
```  

### 模式3：研究 → 执行  
```
Researcher (investigate options)
    ↓ deliver report
Worker (implement chosen option)
    ↓ deliver code
Reviewer (verify quality)
```  

---

## 何时使用子代理  

**在以下情况下使用子代理**:  
- 任务需要多个专业角色协作  
- 预计耗时超过10分钟  
- 失败可能产生重大后果  
- 需要批量处理多个文件  

**直接处理的情况**:  
- 快速问答（<5分钟）  
- 简单的解释或查询  
- 单步操作  

---

## 决策树  
```
User Request
    ↓
┌─────────────────────────────────────────┐
│ 1. Needs multiple specialist roles?     │
│ 2. Duration > 10 minutes?               │
│ 3. Failure impact is high?              │
│ 4. Batch processing needed?             │
└─────────────────────────────────────────┘
    ↓ Any YES
Delegate to SubAgent
    ↓ All NO
Handle directly
```  

---

## QMD集成（内容管理）  

**QMD（Query Model Direct）**支持对所有内容进行语义搜索：  
```bash
# Search knowledge base
mcporter call 'exa.web_search_exa(query: "GPR signal processing", numResults: 5)'

# Search for skills
mcporter call 'exa.web_search_exa(query: "SKILL.md image processing", numResults: 5)'
```  
- 将Markdown文件放入`knowledge/`子目录  
- QMD会自动对其进行索引  
- 无需手动注册  

---

## 工具参考  

### 徽章生成器v7  
**位置**: `lib/badge_generator_v7.py`  
**特性**:  
- 生成复古像素艺术风格的头像  
- 支持中英文显示  
- 动态显示OpenClaw版本信息  
- 工单详情包含二维码和条形码  
- 美观的渐变设计  

**使用方法**:  
```bash
cd ~/.openclaw/workspace/skills/fis-architecture/lib
python3 badge_generator_v7.py

# Interactive prompts for task details
# Output: ~/.openclaw/output/badges/Badge_{TICKET_ID}_{TIMESTAMP}.png
```  

### 命令行辅助工具（可选）  
```bash
# Create ticket with helper
python3 fis_subagent_tool.py full \
  --agent "Worker-001" \
  --task "Task description" \
  --role "worker"

# Complete ticket
python3 fis_subagent_tool.py complete \
  --ticket-id "TASK_CYBERMAO_20260219_001"
```  

---

## 从FIS 3.1迁移  

如果您使用的是FIS 3.1版本：  
1. **已迁移的组件**位于`archive/fis3.1-full/`和`archive/fis3.1-legacy/`目录  
2. **工单文件**格式保持不变（仍为JSON）  
3. **技能发现**功能：使用QMD替代`skillRegistry.py`  
4. **内存查询**：使用QMD替代`memory_manager.py`  

---

## 设计原则  

1. **FIS负责管理工作流，QMD负责内容管理**  
   - 工单用于记录任务状态  
   - QMD用于知识检索  
2. **基于文件的架构**  
   - 无需依赖服务或数据库  
   - 100%基于文件操作  
   - 适合Git版本控制  
3. **避免核心文件被修改**  
   - 禁止修改其他组件的`MEMORY.md`/`HEARTBEAT.md`文件  
   - 扩展文件仅保存在`.fis3.1/`目录  
4. **质量优先于数量**  
   - 组件数量少但功能强大  
   - 移除QMD已提供的功能  

---

## 更新日志  

### 2026-02-20: v3.2.4-lite  
- **安全改进**: 完全移除了`archive/`目录（旧版本组件仅保留于GitHub仓库历史记录）  
- **文档更新**: 添加了关于旧版本组件的说明  

### 2026-02-20: v3.2.3-lite  
- **文档优化**: 明确区分核心工作流和可选的Python辅助工具  
- **新增内容**: 添加了安装前的安全提示和组件说明  
- **元数据更新**: 将`mcporter`列为必需的二进制文件  
- **链接更新**: 添加了OpenClaw QMD的官方文档链接  
- **修复错误**: 更正了关于“核心功能是否使用Python”的描述  

### 2026-02-20: v3.2.2-lite  
- **安全与文档改进**:  
  - 移除了`archive/deprecated/`目录  
  - 明确指出核心功能不依赖Python  
  - 添加了关于`resources`字段的安全警告  
  - 在`INSTALL_CHECKLIST.md`中添加了安全检查清单  
  - 更正了关于“无Python依赖”的误导性描述  

### 2026-02-20: v3.2.1-lite  
- **文档改进**:  
  - 添加了故障排除指南  
  - 提供了工单命名和知识组织的最佳实践  
  - 增加了实际使用示例  
  - 更清晰地说明了何时使用/不使用子代理  

### 2026-02-19: v3.2.0-lite  
- **架构简化**:  
  - 移除了`memory_manager.py`，改用QMD  
  - 移除了`skillRegistry.py`，改用SKILL.md和QMD  
  - 移除了`deadlock_detector.py`，相关功能由QMD承担  
  - 保留了工单系统和徽章生成器  
  - 更新了架构说明  

### 2026-02-18: v3.1.3  
- 移除了个人配置示例  
- 创建了公共GitHub仓库  

---

## 文件位置  
```
~/.openclaw/workspace/skills/fis-architecture/
├── SKILL.md                    # This file
├── README.md                   # Repository readme
├── QUICK_REFERENCE.md          # Quick command reference
├── AGENT_GUIDE.md              # Agent usage guide
├── lib/                        # Tools (not core)
│   ├── badge_generator_v7.py   # ✅ Kept: Badge generation
│   ├── fis_lifecycle.py        # ✅ Kept: Lifecycle helpers
│   ├── fis_subagent_tool.py    # ✅ Kept: CLI helper
│   ├── memory_manager.py       # ❌ Deprecated (QMD replaces)
│   ├── skill_registry.py       # ❌ Deprecated (QMD replaces)
│   └── deadlock_detector.py    # ❌ Deprecated
└── examples/                   # Usage examples
```  

*FIS 3.2.0-lite — 架构简化，功能清晰*  
*设计者：CyberMao 🐱⚡*  

---

## 故障排除  

### 问题：找不到工单  
**现象**: `cat: tickets/active/TASK_001.json: 未找到该文件或目录`  
**解决方法**:  
```bash
# Check if directory exists
ls ~/.openclaw/fis-hub/tickets/active/

# Create if missing
mkdir -p ~/.openclaw/fis-hub/tickets/{active,completed}
```  

### 问题：徽章生成失败  
**现象**: `ModuleNotFoundError: 未找到名为‘PIL’的模块`  
**解决方法**:  
```bash
pip3 install Pillow qrcode
```  

### 问题：QMD搜索无结果  
**现象**: `mcporter call 'exa.web_search_exa(...)'`返回空结果**  
**解决方法**:  
- 检查Exa MCP配置：`mcporter list exa`  
- 确认知识文件位于`fis-hub/knowledge/`目录  
- 确保文件扩展名为`.md`  

### 问题：无法写入工单文件  
**现象**: 无法写入`tickets/active/`目录  
**解决方法**:  
```bash
chmod -R u+rw ~/.openclaw/fis-hub/tickets/
```  

---

## 最佳实践  

### 工单命名  
```
Good:  TASK_UAV_20260220_001_interference_analysis
Bad:   task1, new_task, test
```  

### 知识组织  
```
knowledge/
├── papers/           # Research papers and notes
├── methods/          # Methodology documentation
├── tools/            # Tool usage guides
└── projects/         # Project-specific knowledge
```  

### 定期维护  
```bash
# Weekly: Archive completed tickets older than 30 days
find ~/.openclaw/fis-hub/tickets/completed/ -name "*.json" -mtime +30 -exec mv {} archive/old_tickets/ \;

# Monthly: Review and clean knowledge/
ls ~/.openclaw/fis-hub/knowledge/ | wc -l  # Keep count reasonable
```