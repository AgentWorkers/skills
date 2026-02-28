---
name: sub-agent-factory
description: 能够快速生成并配置专门的子代理（sub-agents），包括用于研究（Research）、编码（Coding）和分析（Analysis）的模板。实现工作区的自动设置以及指令的自动传递。
---
# 子代理工厂（Sub-Agent Factory）

不要事事都亲力亲为，通过组建团队来提升工作效率吧。

## 能力矩阵（Capability Matrix）

- **编码代理（Coder Agent）**：专为代码仓库探索和错误修复而设计。
- **研究代理（Research Agent）**：擅长网络搜索和撰写深度分析报告。
- **分析代理（Analysis Agent）**：专注于数据处理、JSON文件处理以及日志分析。

## 设置流程（Setup Protocol）

1. **定义任务（Define Mission）**：设定一个简洁明了的目标。
2. **选择代理类型（Select Template）**：挑选合适的代理类型。
3. **配置代理（Provision）**：运行 `scripts/create_agent.sh` 脚本。
4. **配置通信文件夹（Link）**：设置收件箱（inbox）和发件箱（outbox）的路径。

## 安装说明（Installation Instructions）
```bash
clawhub install sub-agent-factory
```