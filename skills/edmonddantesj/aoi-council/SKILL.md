---
name: aoi-council
version: 0.1.0
description: AOI Council — 多视角决策合成模板（公开安全版）。
author: Aoineco & Co.
license: MIT
---
# AOI 委员会（AOI Council）

S-DNA: `AOI-2026-0215-SDNA-CNSL01`

## 功能介绍  
这是一个公开且安全的委员会工作流程，可帮助您从多个角度对决策进行压力测试（stress-testing）。  

## 来源与原创性  
- AOI 的实现完全基于原创代码（未复制任何第三方代码）。  
- 其设计理念借鉴了传统的“委员会/多视角评审”工作流程模式。  

## 使用说明  
该技能采用模板驱动的方式运行：  
- 不会对外发布任何数据；  
- 不会修改用户的钱包（wallets）；  
- 不会更改系统配置（system config）。  

## 委员会成员（默认配置）  
该技能会自动加载 `agents/` 目录下的所有 `.md` 文件，包括以下成员角色：  
- **唱反调者（Devil’s Advocate）**  
- **架构师（Architect）**  
- **工程师（Engineer）**  
- **安全审核员（Security Reviewer）**  
- **操作员（Operator/Ops）**  
- **撰写者（Writer/Comms）**  

## 使用方式  
只需输入以下命令即可：  
- `AOI council: <主题>`  
- `Send to council: <计划>`  

## 输出结果  
- 首先提供决策的**综合分析**（简明扼要的总结）；  
- 然后分别展示每个成员的观点、意见及建议；  
- 最后列出未解决的问题及后续行动方案。  

## 技术支持  
- 如有疑问、漏洞或需求，请访问：[https://github.com/edmonddantesj/aoi-skills/issues](https://github.com/edmonddantesj/aoi-skills/issues)  
- 请在问题描述中注明技能名称：`aoi-council`。  

## 管理机制（公开透明）  
我们免费提供这些技能，并持续对其进行优化。每次更新都必须通过我们的安全审查流程，并附带可审计的变更记录。我们绝不会发布任何会降低安全性的更新或影响许可条款的版本。若多次违反规定，系统将逐步采取限制措施（从警告开始，直至暂停发布或最终归档该技能）。