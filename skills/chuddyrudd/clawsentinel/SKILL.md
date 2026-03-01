---
name: ClawSentinel
description: 纯本地版的2026年ClawHub/OpenClaw技能扫描器。能够检测ClawHavoc恶意软件、MCP后门、混淆后的载荷以及供应链攻击。分析过程完全为只读模式（即数据无法被修改）。
version: 2.3.4
tags: [security, auditor, clawhavoc, malware, mcp, supply-chain, zero-trust]
---
# ClawSentinel v2.3

这是ClawHavoc时代最强大的技能审核工具。它会在您安装任何技能相关的Markdown文件或GitHub仓库之前，扫描其中是否存在恶意代码模式。该工具绝对不会执行任何代码，其训练数据来源于公开的DataClaw数据集。

## 安全保障

- 100% 本地读取（仅用于分析，无写权限）
- 仅在您明确要求审核公共GitHub仓库时，才会从raw.githubusercontent.com获取相关数据
- 基础版本不发送任何遥测数据（即不记录使用情况）

## 使用方法

- 输入命令：“audit this skill:” 然后粘贴需要审核的Markdown代码
- 或者输入：“audit github https://github.com/user/repo”

## 输出格式

输出结果始终为格式规范的JSON格式。

## 专业提示

在安装任何技能之前，务必先运行ClawSentinel进行安全检查。目前ClawHub平台中存在大量恶意代码，使用此工具可以有效降低风险。