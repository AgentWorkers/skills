# FIS（联邦智能系统）架构技能

> **版本**: 3.2.6  
> **名称**: 联邦智能系统  
> **描述**: 基于文件的多代理工作流框架。核心组件：JSON工单 + Markdown知识库（无需Python）。可选：`lib/`目录中的Python辅助工具用于徽章生成。支持与OpenClaw的QMD进行语义搜索集成。  

> **安全性**: 有关子进程使用、资源权限和沙箱化指南，请参阅[SECURITY.md](./SECURITY.md)。  

> **注意**: 旧版本的FIS 3.1组件（如`memory_manager`、`skillRegistry`等）保留在GitHub仓库的历史记录中，但未包含在此版本中。如需历史参考，请查看仓库。  
> **状态**: ✅ 稳定版本 — 架构简化，已集成QMD语义搜索功能。  

---

## 安装前须知

**核心工作流**: 完全基于文件（JSON工单，Markdown格式）。基本使用无需Python。  

**可选组件**（使用前请查看）：  
- `lib/*.py` — 徽章生成辅助工具（需要安装`pip install Pillow qrcode`）  
- `lib/fis_lifecycle.py` — 工单管理的命令行辅助工具  

**必需组件**: `mcporter`命令行工具（随OpenClaw一起提供），`openclaw`命令行工具  

**安全性**: 在运行Python脚本或授予工单资源权限之前，请务必阅读[SECURITY.md](./SECURITY.md)。  

---

## 核心原则：FIS负责管理工作流，QMD负责内容管理  

**FIS 3.2**是对FIS 3.1的重大简化。我们移除了与QMD（Query Model Direct）语义搜索功能重复的组件：  

| 组件 | FIS 3.1 | FIS 3.2 | 原因 |  
|-----------|---------|---------|--------|  
| 任务管理 | Python类 + `memory_manager` | JSON工单文件 | 更简单，更易于审计 |  
| 内存/检索 | `memory_manager.py` | **QMD** | QMD具备原生语义搜索功能 |  
| 技能发现 | `skillRegistry.py` | **SKILL.md + QMD** | QMD可索引SKILL.md文件 |  
| 知识图谱 | `experimental/kg/` | **QMD** | QMD支持知识发现功能 |  
| 死锁检测 | `deadlock_detector.py` | 简单的规则 | 实际应用中很少需要 |  

**保留的内容**: 仅保留FIS独有的工作流功能。  

---

## 3.2.0的新特性  

### 简化架构  
- **核心工作流**: 基于文件（JSON工单，Markdown知识库）——无需Python  
- **可选辅助工具**: `lib/`目录中的Python脚本用于徽章生成（可审计，可选）  
- **官方集成**: 支持使用OpenClaw的QMD进行语义搜索（详情请参见https://docs.openclaw.ai/concepts/memory）  
- **徽章生成器**: 为子代理生成视觉标识（需要安装Pillow库，可选）  

### 目录结构  

---  

## 快速入门  

### 1. 创建任务工单  

---  

**安全提示**: `resources`字段（例如`["file_read", "code_execute"]`）可以添加到工单中，但需谨慎使用。仅在必要时授予相应权限，并对所有自动化操作进行审计。  

### 2. 生成徽章图片  

---  

### 3. 完成并归档  

---  

## 工单格式  

---  

### 字段说明  

| 字段 | 类型 | 是否必填 | 说明 |  
|-------|------|----------|-------------|  
| `ticket_id` | 字符串 | ✅ | 唯一标识符：`TASK_{agent}_{YYYYMMDD}_{seq}` |  
| `agent_id` | 字符串 | ✅ | 分配的代理（例如：“pulse”、“worker-001”） |  
| `parent` | 字符串 | ✅ | 协调代理（例如：“cybermao”） |  
| `role` | 枚举 | ✅ | `worker`、`reviewer`、`researcher`、`formatter` |  
| `task` | 对象 | ✅ | `{description, created_at, deadline, status}` |  
| `objective` | 字符串 | ❌ | 任务的高层目标 |  
| `scope` | 对象 | ❌ | `{must_do[]`, `must_not_do[]}` 规则 |  
| `deliverables` | 数组 | ❌ | 预期输出/交付物 |  
| `resources` | 数组 | ❌ | 权限：`file_read`、`file_write`、`code_execute`、`web_search` |  
| `output_dir` | 字符串 | ❌ | 保存结果的路径 |  
| `notes` | 字符串 | 额外说明或警告 |  

---

## 工作流模式  

### 模式1：工作者 → 审核者流程  

---  

**工单示例**：  
1. `TASK_001_worker.json` → 活动状态 → 完成状态  
2. `TASK_002_reviewer.json` → 活动状态 → 完成状态  

### 模式2：并行工作者  

---  

### 模式3：研究 → 执行  

---  

## 何时使用子代理  

**在以下情况下使用子代理**：  
- 任务需要多个专业角色  
- 预计耗时超过10分钟  
- 失败可能导致严重后果  
- 需要批量处理多个文件  

**直接处理的情况**：  
- 快速问答（<5分钟）  
- 简单的解释或查找  
- 一步完成的操作  

---

## QMD集成（内容管理）  

**QMD（Query Model Direct）**支持对所有内容进行语义搜索：  

---  

**知识存储方式**：  
- 将Markdown文件放入`knowledge/`子目录  
- QMD会自动对其进行索引  
- 无需手动注册  

---

## 工具参考  

### 徽章生成器v7  

**位置**: `lib/badge_generator_v7.py`  

**功能**：  
- 生成复古像素艺术风格的头像  
- 支持中英文显示  
- 动态显示OpenClaw版本信息  
- 包含带有二维码和条形码的任务详情  
- 美观的渐变设计  

**使用方法**:  

---  

## 命令行辅助工具（可选）  

---  

---

## 从FIS 3.1迁移  

如果您使用的是FIS 3.1版本：  
1. **已归档的组件**位于`archive/fis3.1-full/`和`archive/fis3.1-legacy/`目录  
2. **工单文件**格式保持不变（仍为JSON格式）  
3. **技能发现**：使用QMD替代`skillRegistry.py`  
4. **内存查询**：使用QMD替代`memory_manager.py`  

---

## 设计原则  

1. **FIS负责管理工作流，QMD负责内容管理**  
   - 工单用于记录任务状态  
   - QMD用于知识检索  

2. **基于文件的架构**  
   - 无需服务或数据库  
   - 100%基于文件  
   - 适合Git版本控制  

3. **避免核心文件被修改**  
   - 绝不要修改其他代理的`MEMORY.md/HEARTBEAT.md`文件  
   - 扩展文件仅保存在`.fis3.1/`目录中  

4. **质量优先于数量**  
   - 组件数量少但功能更强大  
   - 移除QMD已提供的功能  

---

## 更新日志  

### 2026-02-20: v3.2.5-lite  
- 修复模块名称和卸载安全性问题  
  - 更改了危险的卸载命令（`rm -rf ~/.openclaw/fis-hub/`），确保仅删除与技能相关的文件  
  - 统一了所有`subagent_lifecycle`的引用  

### 2026-02-20: v3.2.4-lite  
- 移除了`archive/`目录  
  - 安全性：完全移除了`archive/`目录（旧版本组件仅保留于GitHub仓库历史记录中）  
  - 文档中添加了关于旧版本组件的说明  

### 2026-02-20: v3.2.3-lite  
- 优化了文档说明  
  - 清晰区分了核心工作流（基于文件）和可选的Python辅助工具  
  - 文档中添加了安装前的安全提示和组件说明  
  - 在`skill.json`中明确指出`mcporter`是必需的二进制文件  
  - 添加了OpenClaw QMD的官方文档链接  
  - 解决了文档中关于“核心功能不使用Python”与“包含Python辅助工具”的矛盾  

### 2026-02-20: v3.2.2-lite  
- 改进了安全性和文档内容  
  - 从发布的文档中移除了`archive/deprecated/`目录  
  - 明确说明了“核心功能不使用Python”与“包含Python辅助工具”的区别  
  - 添加了关于工单`resources`字段的安全警告  
  - 在`INSTALL_CHECKLIST.md`中添加了安全检查清单  
  - 更正了“无Python依赖”这一误导性描述  

### 2026-02-20: v3.2.1-lite  
- 文档得到了进一步优化：  
  - 添加了故障排除指南和常见问题的解决方案  
  - 添加了工单命名和知识组织的最佳实践  
  - 增加了实际使用案例  
  - 更清晰地说明了何时使用/不使用子代理  

### 2026-02-19: v3.2.0-lite  
- 进一步简化了架构：  
  - 移除了`memory_manager.py`，改用QMD  
  - 移除了`skillRegistry.py`，改用SKILL.md和QMD  
  - 移除了`deadlock_detector.py`，其功能由QMD接管  
  - 保留了工单系统和徽章生成器  
  - 更新了架构相关的文档  

### 2026-02-18: v3.1.3  
- 删除了个人配置示例  
- 创建了公开的GitHub仓库  

---

## 文件位置  

---  

*FIS 3.2.0-lite — 架构简化，功能清晰*  
*设计者：CyberMao 🐱⚡*  

---

## 故障排除  

### 问题：找不到工单  
**症状**：`cat: tickets/active/TASK_001.json: 未找到该文件或目录`  

**解决方法**：  

---  

### 问题：徽章生成失败  
**症状**：出现`ModuleNotFoundError: No module named 'PIL'`错误**  

**解决方法**：  

---  

### 问题：QMD搜索无结果  
**症状**：`mcporter call 'exa.web_search_exa(...)'`返回空结果**  

**解决方法**：  
- 检查Exa MCP配置：`mcporter list exa`  
- 确保知识文件位于`fis-hub/knowledge/`目录  
- 确保文件扩展名为`.md`  

### 问题：无法写入工单文件  
**症状**：无法写入`tickets/active/`目录  

**解决方法**：  

---  

## 最佳实践  

### 工单命名规范  

---  

### 知识组织方法  

---  

### 定期维护指南  

---