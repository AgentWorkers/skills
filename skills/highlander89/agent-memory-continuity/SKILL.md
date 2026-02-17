---
name: agent-memory-continuity
description: 通过采用“搜索优先”协议、自动内存同步以及上下文保留机制，解决“代理忘记所有信息”的问题。再也不用重新开始对话了！
homepage: https://sapconet.co.za
metadata: {"clawhub": {"emoji": "🧠", "tags": ["memory", "continuity", "agent-management", "enterprise"], "author": "SAPCONET", "version": "1.0.0"}}
---
# 代理内存连续性 🧠

## 问题
您的 OpenClaw 代理是否存在“对话遗忘”的问题？每次会话开始时都需要从头开始？忘记之前的讨论、决策和上下文？您并不孤单——这是 AI 代理最常见的问题之一。

## 解决方案
**代理内存连续性** 通过经过实战验证的 **搜索优先协议** 来解决对话片段化的问题，确保代理永远不会忘记之前的上下文。

## 为什么需要这项功能？
- ✅ **解决普遍存在的问题**：所有 OpenClaw 用户都面临内存相关的问题
- ✅ **经过实战验证的解决方案**：已在生产环境中得到验证
- ✅ **立竿见影的效果**：再也不用担心代理“崩溃并忘记所有内容”
- ✅ **企业级功能**：专业的记忆管理系统

## 适用场景
- 代理对话经常“从头开始”
- 会话之间丢失了之前的上下文
- 用户抱怨“我们之前已经讨论过这个问题”
- 需要对话连续性的企业环境
- 多会话代理的工作流程

## 不适用场景
- 一次性、无状态的交互
- 无需记录对话历史的代理
- 简单的查询/响应场景

## 功能特点

### 🔍 搜索优先协议
- 在回答正在进行的话题之前，必须先搜索内存
- 检测对话连续性中断的警告信号
- 从内存文件中自动重建上下文

### 📝 自动化内存同步
- 每 6 小时同步一次内存上下文
- 每日生成和更新内存文件
- 实现正在进行的项目和对话之间的交叉引用

### 🧠 上下文保留
- 每日记录内存数据
- 持续跟踪重要信息
- 维护对话的连贯性

### 🚨 中断检测
- 识别代理“忘记”之前上下文的情况
- 通过内存搜索自动恢复
- 防止用户感到沮丧

## 安装

```bash
# Install via ClawHub
npx clawhub install agent-memory-continuity

# Or clone directly
git clone https://github.com/sapconet/agent-memory-continuity.git
cd agent-memory-continuity
bash install.sh
```

## 快速入门

### 1. 初始化内存协议
```bash
# Set up memory structure
bash scripts/init-memory-protocol.sh

# Creates:
# - AGENT_MEMORY_PROTOCOL.md (search-first rules)
# - memory/YYYY-MM-DD.md (daily context files)
# - Memory sync cron jobs
```

### 2. 配置搜索优先行为
```bash
# Configure mandatory memory search
bash scripts/configure-search-first.sh

# Enables:
# - Pre-response memory searches
# - Context continuity checks
# - Automatic break recovery
```

### 3. 激活内存同步
```bash
# Start automated memory synchronization  
bash scripts/activate-memory-sync.sh

# Schedules:
# - 6-hourly context updates
# - Daily memory file creation
# - Ongoing project cross-referencing
```

## 使用方法

### 基本内存协议
该功能会自动：
1. 在回答正在进行的话题之前搜索内存
2. 检测警告信号（如“我们之前讨论过这个”、“记得是在什么时候”）
3. 在检测到中断时从内存文件中重建上下文
4. 将决策记录到每日内存文件中
5. 在不同会话之间同步上下文

### 高级配置

#### 自定义内存搜索模式
```bash
# Add custom search patterns
echo "project_name meeting decision" >> config/search-patterns.txt

# Configure search sensitivity
export MEMORY_SEARCH_THRESHOLD=0.7
```

#### 内存归档规则
```bash
# Configure archival timing
export MEMORY_ARCHIVE_DAYS=30
export MEMORY_RETENTION_MONTHS=12

# Set up automatic archival
bash scripts/setup-memory-archival.sh
```

## 文件结构

```
agent-memory-continuity/
├── SKILL.md
├── install.sh
├── scripts/
│   ├── init-memory-protocol.sh
│   ├── configure-search-first.sh
│   ├── activate-memory-sync.sh
│   ├── setup-memory-archival.sh
│   └── test-memory-continuity.sh
├── templates/
│   ├── AGENT_MEMORY_PROTOCOL.md
│   ├── daily-memory-template.md
│   └── cron-jobs-template.txt
├── config/
│   ├── search-patterns.txt
│   └── memory-config.json
└── docs/
    ├── troubleshooting.md
    └── enterprise-setup.md
```

## 实际应用效果

**使用代理内存连续性之前：**
- ❌ 代理“崩溃并忘记所有内容”
- 会话不断重新开始
- 上下文和决策丢失
- 用户感到沮丧，工作效率下降

**使用代理内存连续性之后：**
- ✅ 对话连续性完美
- 会话之间的上下文得到保留
- 决策和讨论被记住
- 用户满意度和信任度得到提升

## 企业级功能

### 生产环境部署
- 多代理内存同步
- 团队对话连续性
- 企业级内存管理
- 审计追踪和合规性保障

### 专业支持
- 实施咨询
- 定制内存搜索模式开发
- 企业级集成服务
- 24/7 技术支持

## 故障排除

### 常见问题

**代理仍然忘记对话内容：**
```bash
# Check memory search frequency
bash scripts/test-memory-continuity.sh

# Increase search sensitivity  
export MEMORY_SEARCH_THRESHOLD=0.5
```

**内存文件过大：**
```bash
# Enable automatic archival
bash scripts/setup-memory-archival.sh

# Configure retention policies
nano config/memory-config.json
```

**定时任务未运行：**
```bash
# Check cron status
crontab -l | grep memory

# Reinstall cron jobs
bash scripts/activate-memory-sync.sh --force
```

## 支持

### 社区支持
- GitHub 问题反馈：https://github.com/sapconet/agent-memory-continuity/issues
- 文档：https://docs.sapconet.co.za/memory-continuity
- 示例代码：https://github.com/sapconet/agent-memory-continuity/examples

### 企业级支持
- 电子邮件：support@sapconet.co.za
- 专业服务：https://sapconet.co.za/openclaw-consulting
- 电话：+27 (0)53 123 4567

## 关于 SAPCONET
我们是 OpenClaw 领域的企业级专家，拥有超过 6 个月的生产经验。我们解决的是其他人仍在探索的问题。

**服务范围：**
- 企业级 OpenClaw 部署
- 定制功能开发
- 代理团队咨询服务
- 24/7 技术支持

**官方网站：** https://sapconet.co.za
**联系方式：** hello@sapconet.co.za

---

*终结代理的“对话遗忘”问题，实现对话的连续性。由最早解决这一问题的团队打造。*