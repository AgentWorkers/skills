---
name: code-generator
description: "多语言代码生成工具。能够生成函数、类、API接口、CRUD操作代码、测试代码、重构建议以及项目模板。支持Python、JavaScript、TypeScript、Go、Java等多种编程语言。适用于代码框架搭建、模板生成或语言之间的转换。触发条件：代码生成器（code generator）。"
---
# ⚡ 代码生成器 — 多语言代码框架

> 仅需描述您的需求，即可获得可运行的代码。支持多种语言。

## ✨ 主要功能

- 🔧 **函数生成** (`function`) — 根据描述生成带有注释的完整函数
- 🏗️ **类生成** (`class`) — 支持面向对象设计（包含构造函数和方法）
- 🌐 **API接口** (`api`) — 提供RESTful路由和处理器
- 📦 **CRUD操作** (`crud`) — 提供完整的创建/读取/更新/删除功能
- 🧪 **测试代码** (`test`) — 自动生成带有断言的单元测试
- 🔄 **代码重构** (`refactor`) — 提供重构建议及示例
- 🔀 **语言转换** (`convert`) — 支持Python/JavaScript/Go/Java之间的语言转换
- 📋 **项目模板** (`boilerplate`) — 提供快速启动的项目框架

## 🌍 支持的语言

Python · JavaScript · TypeScript · Go · Java · Rust · PHP · Ruby · C# · Shell

## 🚀 使用方法

```bash
bash scripts/codegen.sh <command> <description>
```

每个生成的代码文件包含以下内容：
1. 语言标签及建议的文件名
2. 完整的可运行代码
3. 内嵌注释
4. 使用示例

## 📂 脚本
- `scripts/codegen.sh` — 主脚本

---
💬 意见反馈与功能请求：https://bytesagain.com/feedback
由BytesAgain提供支持 | bytesagain.com

## 命令

运行 `code-generator help` 可查看所有可用命令。