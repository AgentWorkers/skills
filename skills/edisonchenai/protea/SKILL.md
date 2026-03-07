---
name: protea
description: >
  自进化的人工生命系统。采用三环架构：  
  - **Ring 0（哨兵）**：负责监督整个系统的运行；  
  - **Ring 1（智能模块）**：利用大型语言模型（LLM）驱动系统的进化过程；  
  - **Ring 2（可进化代码）**：作为核心组件，该代码能够自我重构、自我复制并实现自我进化。  
  该系统支持多种LLM提供商，包括Anthropic、OpenAI、DeepSeek和Qwen。其功能包括：  
  - 适应性评估（fitness scoring）；  
  - 基因库的遗传机制（gene pool inheritance）；  
  - 分层存储系统（tiered memory）；  
  - 技能的固化与优化（skill crystallization）；  
  - 集成Telegram机器人（Telegram bot）；  
  - 提供Web管理界面（web dashboard）。
---
# Protea — 自进化人工生命系统

这是一个能够自我进化的程序，采用三环架构运行在单台机器上。

## 架构

- **第0环（哨兵层）** — 不可变的物理层，负责心跳监控、Git快照生成、回滚操作以及适应度评估。完全使用Python标准库实现。
- **第1环（智能层）** — 由大型语言模型（LLM）驱动的进化引擎，负责任务执行、Telegram机器人功能以及技能的提取与展示；支持多种LLM（Anthropic、OpenAI、DeepSeek、Qwen）。
- **第2环（可进化代码层）** — 这部分代码会不断进化，并由第0环通过Git仓库进行管理。

## 先决条件

- Python 3.11及以上版本
- Git工具
- 至少一个大型语言模型（LLM）的API密钥（Anthropic、OpenAI、DeepSeek或Qwen）

## 快速入门

```bash
# Install
curl -sSL https://raw.githubusercontent.com/EdisonChenAI/protea/main/setup.sh | bash
cd protea && .venv/bin/python run.py
```

或者手动克隆代码：

```bash
git clone https://github.com/EdisonChenAI/protea.git
cd protea
bash setup.sh
.venv/bin/python run.py
```

## 主要特性

- **自我进化**：每一代代码都会由LLM生成变异；存活下来的代码会被保留，失败的代码会被回滚。
- **适应度评分**：采用六项评分标准（存活能力、输出量/多样性、新颖性、代码结构、功能完整性）。
- **基因库**：排名前100的代码模式会被存储在SQLite数据库中，并用于后续的进化过程。
- **分层内存管理**：代码按使用频率分为“热点”、“温热”、“冷备”和“遗忘”四个层级，由LLM协助进行管理。
- **技能提取**：存活下来的代码模式会被提取为可重用的技能。
- **多LLM支持**：通过统一接口支持Anthropic、OpenAI、DeepSeek、Qwen等多种LLM。
- **Telegram机器人**：支持命令输入和自由文本交互。
- **Web仪表盘**：可以通过`http://localhost:8899`访问本地UI界面。
- **全面测试**：对第0环和第1环的功能进行了1098项全面测试。

## 配置

编辑`config/config.toml`文件以设置LLM提供者：

```toml
# Anthropic (default)
# Set CLAUDE_API_KEY env var

# Or use DeepSeek
[ring1.llm]
provider = "deepseek"
api_key_env = "DEEPSEEK_API_KEY"
model = "deepseek-chat"
```

## 项目结构

```
protea/
├── ring0/          # Sentinel (pure stdlib)
├── ring1/          # Intelligence layer + tools
├── ring2/          # Evolvable code
├── config/         # Configuration
├── tests/          # 1098 tests
└── run.py          # Entry point
```