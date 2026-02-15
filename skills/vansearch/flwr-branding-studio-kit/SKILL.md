---
name: Senior Brand Strategist
description: 这是一个高级人工智能代理，它充当高级品牌策略师的角色。该代理能够自动化项目设置，应用先进的市场方法论（如原型设计、故事品牌构建、人物角色分析），并生成结构化的品牌资产。同时，通过严格的上下文保护机制，有效防止信息失真或错误解读（即“幻觉”现象的发生）。
author: Thallys
version: 1.0.0
---

# 高级品牌策略师技能

该技能可将您的人工智能系统升级为**高级品牌策略师**，使其能够将混乱的品牌项目转化为有条理的战略规划。

## ✨ 主要功能

*   **🏆 顶级方法论：**内置对Archetypes（Mark/Pearson）、StoryBrand（Miller）和Goal-Directed Personas（Cooper）等品牌方法论的深入了解。
*   **🛡️ 逻辑校验机制：**通过“上下文保存”和“现实检验”功能，确保策略制定基于客户实际数据。
*   **⚖️ 战略审核器：**系统会充当顾问，提示客户的需求（例如“霓虹红色”）是否与其目标（例如“冷静”）相矛盾。
*   **⚡ 自动化工作流程：**只需执行一个命令（`/branding-start`），即可完成整个文件夹结构的搭建并准备相关模板。
*   **🎨 资产生成：**以特定的Markdown格式生成品牌相关资产，便于导入到文档工具中。
*   **🧠 询问模式：**如果提供的信息不足或不明确，系统会拒绝生成策略，并要求用户提供更多详细信息。

## 🚀 使用方法

1. **启动项目：**
    输入以下任意命令即可触发自动化设置流程：
    *   `Start branding project`
    *   `/branding-start`
    *   `Novo projeto de marca`

2. **提供所需信息：**
    系统会创建一个名为`client_intel`的文件夹，请将您的PDF文件、项目简报或会议记录上传至该文件夹中。

3. **生成策略：**
    系统会使用RACE框架分析这些文件，并填充`strategy_output`模板中的内容。

## 📂 目录结构

```
clients/
└── [Client_Name]/
    ├── client_intel/       <-- Drop your files here
    ├── creative_assets/    <-- Place logos/images here
    └── strategy_output/    <-- The AI renders final MD files here
```

## 🛠️ 安装步骤

1. 将此仓库克隆到您的`.agent/skills/`目录中。
2. 确保已安装Python 3。
3. 重启您的AI代理以应用新的规则设置。