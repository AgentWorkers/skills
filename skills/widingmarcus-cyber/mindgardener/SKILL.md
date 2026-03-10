---
name: mindgardener
description: 专为 OpenClaw 设计的、基于本地数据的长期记忆系统。该系统能够从对话中生成维基知识图谱，根据事件的突发性对它们进行评分，检测潜在的冲突，并构建令牌预算（token-budget）相关的上下文信息。它作为 OpenClaw 内置的 `memory_search` 功能的补充工具，进一步提升系统的智能处理能力。
metadata:
  clawdbot:
    requires:
      bins: ["garden"]
    install:
      - id: mindgardener
        kind: pip
        package: mindgardener
        bins: ["garden"]
        label: "Install MindGardener CLI (pip)"
---
# MindGardener 🌱

**你的代理会忘记所有事情……这款工具能解决这个问题。**

*专为 OpenClaw 设计，用于补充 OpenClaw 内置的 `memory_search` 工具。*

## MindGardener 如何补充 OpenClaw 的功能？

| OpenClaw 内置功能 | MindGardener 的新增功能 |
|-------------------|-------------------|
| 搜索现有内存数据 | **根据对话内容创建新的内存数据** |
| 手动编辑 MEMORY.md 文件 | **自动提取信息并生成 wiki 页面** |
| 平面文本搜索 | **构建知识图谱（包含三元组和 wiki 链接）** |
| — | **意外信息会被标记为重要** |
| — | **检测新旧信息之间的冲突** |
| — | **支持多代理之间的数据同步** |

## 主要特性（v1.1 版本）：

- 🔍 **来源追踪**：记录每个事实的来源  
- ⚔️ **冲突检测**：当新信息与旧信息矛盾时进行标记  
- 🚀 **自动注入上下文**：在会话开始时提供相关上下文  
- ⏰ **时间衰减机制**：旧信息会逐渐被遗忘（除非得到强化）  
- 🔒 **并发控制**：通过文件锁确保多代理操作的安全性  
- 🔮 **关联回忆**：通过 wiki 链接和知识图谱进行信息检索  
- 📊 **信心等级**：并非所有信息都同样可靠  
- 🤝 **多代理同步**：将各个代理的内存数据合并到共享存储中  

## 快速入门

**在夜间 cron 任务中添加 MindGardener：**  
```bash
pip install mindgardener
garden init
```

**在会话开始时（BOOTSTRAP.md 或 heartbeat 文件中添加配置：**  
```bash
garden inject --output RECALL-CONTEXT.md
```

## 与默认 OpenClaw 的区别：

- 新文件夹：`memory/entities/`（存放 wiki 页面）  
- 新文件：`graph.jsonl`（存储知识三元组）  
- 新文件：`RECALL-CONTEXT.md`（自动生成的上下文信息）  
- 新文件：`garden.yaml`（配置文件）  

所有文件均为 markdown 格式，无需数据库支持，可离线使用。  

## 系统要求：  
- Python 3.10 或更高版本  
- 不需要外部 API  
- 如需完全本地运行，请使用命令 `garden init --provider ollama`  

## 链接：  
- [GitHub](https://github.com/widingmarcus-cyber/mindgardener)  
- [PyPI](https://pypi.org/project/mindgardener/)  
- 通过 172 项测试验证其稳定性。