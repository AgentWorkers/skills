---
name: symbolic-memory
description: 使用 SQL 数据 + 标准语义实现的无状态符号记忆效应，通过符号和即时编译（JIT）机制激活（基于 PostgreSQL 和 Ollama 技术）。
metadata: {"openclaw":{"emoji":"🧠","homepage":"https://github.com/Th3Hypn0tist/random/blob/main/LLM-symbolic-memory.md","requires":{"bins":["psql","python3"],"env":["PG_DSN","OLLAMA_HOST","OLLAMA_MODEL"],"config":[]}}}
user-invocable: true
version: 1.0
---

# 符号化内存（Symbolic Memory）

## 目的

提供一个无状态的符号化内存工作流程：
- 将事实数据及其规范语义存储在 PostgreSQL 数据库中；
- 将这些数据的引用以符号的形式暴露出来；
- 按需（在预算允许的范围内）动态地解析这些符号的含义；
- 仅将已被解析含义的数据发送给大型语言模型（如 Ollama）。

**原则**：
- 仅存储语义数据，避免混淆语义数据与数据本身的含义。

**注意**：
该功能不依赖于代理本地的持久化内存来存储长期状态。  
持久化的知识被存储在一个共享的、可版本控制的符号化内存系统中（具体实现遵循 JIT 符号化内存设计模式）。
虽然该功能可以在没有符号化内存的情况下运行，但只有在使用符号化内存时，才能保证数据的长期一致性和多代理之间的协同性。

## 设计模式**：
https://github.com/Th3Hypn0tist/random/blob/main/jit-symbolic-memory-design-pattern