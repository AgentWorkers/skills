---
name: aoi-openclaw-security-toolkit-core
description: Fail-closed OpenClaw security toolkit (public-safe). Use to prevent accidental or unexpected data leakage by running local-only checks: default-deny allowlists, lightweight secret/token scans, egress-risk pattern scans, and prompt/document injection pattern scans. Use when preparing GitHub/ClawHub publishing, reviewing skills/scripts for risky behavior, or validating inbound text/doc content before tool execution.
---

# AOI OpenClaw 安全工具包（核心功能）

**用途**：通过快速、仅限本地的检查机制，防止“一次错误的提交”导致文件泄露或机密信息被公开。  
**适用场景**：在提交/推送代码之前、发布技能之前，以及审查脚本/技能是否存在异常数据泄露行为时使用。  
**使用方法**：运行一个命令即可获得“通过（PASS）”、“警告（WARN）”或“阻止（BLOCK）”的检测结果，同时还可以选择生成一份适合公开使用的报告。  
**功能范围**：仅限于检测和报告风险（不提供自动修复、上传或自动发布功能）。  
**快速入门**：`openclaw-sec check --preset repo --diff staged`  

这是一个**对公众安全无害**的工具包技能。  

- **功能**：检测并报告潜在的安全风险（分为“通过（PASS）”、“警告（WARN）”或“阻止（BLOCK）”三种结果）。  
- **不提供**：自动修复、自动上传数据或自动发布功能。  

## 命令行界面（CLI）  

二进制文件：`openclaw-sec`  

**常用命令**：  
（此处可添加常用的 CLI 命令示例）  

**退出代码说明**：  
- `0`：通过（PASS）  
- `1`：警告（WARN）  
- `2`：阻止（BLOCK）  

## 默认扫描范围**  
如果省略了 `--paths` 参数，系统会扫描以下目录中的文件：  
- `.`  
- `skills/`  
- `scripts/`  
- `context/`  

## 规则设置**  
规则文件存储在 `rules/` 目录下：  
- `secret_patterns.txt`：用于识别敏感文件模式  
- `egress_patterns.txt`：用于识别数据泄露模式  
- `prompt_injection_patterns.txt`：用于识别潜在的提示注入攻击模式  

您可以根据实际需求修改这些规则文件来调整系统的敏感度设置。