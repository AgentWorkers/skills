---
name: aiops-agent
description: AI驱动的智能运维系统，能够实现主动预警、智能诊断以及自动化治理功能。
homepage: https://www.cnblogs.com/Jame-mei
metadata: { "openclaw": { "emoji": "🤖", "author": { "name": "James Mei", "email": "meijinmeng@126.com" } } }
---
# AIOps Agent

这是一个基于人工智能的智能运维系统，具备主动监控、智能诊断和自动化修复功能。

## ✅ v1.0.1 更新

**新增功能：**
- 🐛 修复了语法错误（18项测试全部通过）
- 📦 添加了缺失的依赖项文档
- 🧪 提高了测试覆盖率

## 快速入门

```bash
# Clone and setup
git clone <repo-url>
cd sre-agent
cp .env.example .env

# Install dependencies
pip install -r requirements.txt

# Start services
make up

# Access
# API: http://localhost:8000
# Docs: http://localhost:8000/docs
```

## 📦 依赖项

### 核心依赖项
```bash
pip install fastapi uvicorn
pip install kubernetes
pip install anthropic  # or openai
pip install scikit-learn
pip install pandas numpy
```

### 测试依赖项
```bash
pip install pytest pytest-asyncio pytest-cov
```

### 可选依赖项
```bash
pip install prometheus-client
pip install langchain
pip install prophet  # for time series prediction
```

## 主要功能

- ⚡ 主动预警（提前1-3小时发出警报）
- 🔍 自动化根本原因分析
- 🤖 自动修复功能
- 📊 多维度监控
- 🧠 基于大语言模型的洞察分析

## 架构

- **数据收集层**：收集指标、日志和事件数据
- **分析层**：异常检测、预测及根本原因分析
- **决策层**：风险评估与行动计划制定
- **执行层**：自动化问题修复

## 🧪 测试

```bash
# Run all tests
pytest

# With coverage
pytest --cov=src --cov-report=html

# Test results: 18/18 passing ✅
```

## 📝 更新日志

### v1.0.1（2026-02-25）
- 修复了核心模块中的语法错误
- 所有18项测试均通过
- 添加了以下缺失的依赖项：
  - pytest, pytest-asyncio, pytest-cov
  - scikit-learn
  - fastapi
  - kubernetes
  - anthropic
- 文档得到完善

### v1.0.0（2026-02-25）
- 初始版本发布
- 构建了基本的AIOps架构
- 实现了基本的异常检测功能
- 引入了预测引擎
- 支持根本原因分析