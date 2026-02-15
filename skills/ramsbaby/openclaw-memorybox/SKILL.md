---
name: memorybox
description: OpenClaw的零依赖内存管理命令行工具（CLI）。通过三层层次结构保持MEMORY.md文件的简洁性。该工具可与Mem0、Supermemory、QMD配合使用，也可独立运行。只需安装一次，即可无需再担心内存管理问题。
---

# MemoryBox

这是一个专为 OpenClaw 代理设计的、完全独立于其他组件的内存管理工具。

## 功能介绍

通过将内存数据分为三个层级来防止 MEMORY.md 文件变得过于庞大：
- **第一层级**：MEMORY.md（文件大小≤10KB，每次会话时都会被加载）
- **第二层级**：memory/domains/*.md（按需查询）
- **第三层级**：memory/archive/（存放旧的每日日志）

该工具可以与 Mem0、Supermemory、QMD 一起使用，也可以独立运行。它仅修改文件结构，而不会影响配置文件或插件。

## 安装方法

```bash
git clone https://github.com/Ramsbaby/openclaw-memorybox.git
cd openclaw-memorybox && chmod +x bin/memorybox
sudo ln -sf "$(pwd)/bin/memorybox" /usr/local/bin/memorybox
```

## 使用方法

```bash
memorybox doctor ~/openclaw    # Full diagnostic (start here)
memorybox split ~/openclaw     # Interactive: move bloated sections to domain files
memorybox health ~/openclaw    # Quick health score (0-100)
memorybox archive ~/openclaw   # Archive old daily logs (14+ days)
memorybox dedupe ~/openclaw    # Find duplicate content
memorybox stale ~/openclaw     # Detect outdated content
memorybox analyze ~/openclaw   # Section-by-section size breakdown
memorybox suggest ~/openclaw   # Improvement recommendations
memorybox report ~/openclaw    # Before/after token savings
memorybox init ~/openclaw      # Set up 3-tier directory structure
```

## 如何在代理中配置该工具

将相关配置添加到 AGENTS.md 文件中：

```markdown
## Memory Protocol
- **MEMORY.md** (≤10KB): Core facts only. Loaded everywhere — keep it lean.
- **memory/domains/*.md**: Detailed reference. Use `memory_search` to find.
- **memory/archive/**: Old logs. Rarely needed.
```

## 实际效果

在真实生产环境中进行了测试（7 个 Discord 频道，48 个定时任务）：
- MEMORY.md 文件大小从 20KB 降至 3.5KB（减少了 83%）
- 内存使用压力从 98% 降至 7%
- 配置时间：5 分钟

## 链接

- GitHub 仓库：https://github.com/Ramsbaby/openclaw-memorybox
- 相关项目：https://github.com/Ramsbaby/openclaw-self-healing