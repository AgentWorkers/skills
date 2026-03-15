---
name: pre-publish-security
description: 针对 GitHub/ClawHub 的发布版本，我们采用了多层安全审计系统。该系统能够防止凭证泄露、检测安全漏洞、验证相关文档的完整性，并根据需求（快速扫描、历史扫描或依赖项扫描）执行定期扫描。系统还能自动阻止恶意代码的推送。
version: 2.0.0
author: solmas
homepage: https://github.com/solmas/openclaw-pre-publish-security
license: MIT
tags:
  - security
  - git
  - audit
  - credentials
  - publishing
  - dependencies
  - cve
metadata:
  openclaw:
    requires: 
      bins: [git, jq, grep]
      optional: [npm, pip, safety, shellcheck]
    install:
      - { id: jq, kind: apt, package: jq }
user-invocable: true
---
# 预发布安全协议

**防止在开源项目中因泄露凭证而导致的安全漏洞。**

## 特点

✅ **多层次扫描**  
- 快速扫描：每次提交时（约5秒）  
- 历史扫描：每月进行一次深入检查（约2-5分钟）  
- 依赖项漏洞检查：每周检查npm/Python依赖项（约30秒）  
- 全面审计：按需进行（约3-6分钟）  

✅ **智能频率管理**  
- 跟踪每次扫描的运行时间  
- 自动判断需要执行的扫描类型  
- 避免重复检查  

✅ **检测内容**  
- GitHub个人访问令牌（PATs）、API密钥、密码、私钥  
- Git历史记录中的敏感信息（即使已被删除）  
- npm/Python依赖项的漏洞  
- 不安全的代码模式（如`eval`、`exec`）  
- 文档中的占位符（如`[ORG]`、`example.com`）  
- 缺失的`LICENSE`/`README`文件  
- 包含敏感信息的导出环境变量  

✅ **自动化保护**  
- Git预推送钩子阻止错误提交  
- 根据严重程度返回退出代码（CRITICAL/HIGH/MEDIUM/LOW）  
- 提供包含可操作修复建议的Markdown报告  

## 快速入门  

### 安装预推送钩子  
```bash
# Automatic protection on every push
./install-hooks.sh /path/to/your/repo
```  

### 运行首次历史扫描  
```bash
# One-time deep dive (or monthly)
./audit-full.sh /path/to/repo history
```  

### 检查状态  
```bash
# See when scans last ran
./schedule.sh status
```  

### 运行定时审计  
```bash
# Auto-determines what to run based on time
./schedule.sh run /path/to/repo
```  

## 手动扫描  
```bash
# Quick scan (every push)
./audit-simple.sh /path/to/repo

# Git history scan (monthly)
./audit-full.sh /path/to/repo history

# Dependency scan (weekly)
./audit-full.sh /path/to/repo dependencies

# Full audit (before releases)
./audit-full.sh /path/to/repo full
```  

## 扫描范围  

### 快速扫描（每次提交）  
- 当前文件中的敏感信息  
- 文档中的占位符  
- 基本的许可证/`README`文件是否存在  
- **执行时间：**约5秒  

### 历史扫描（每月一次）  
- 完整的Git提交历史记录  
- 被删除但仍可访问的凭证  
- 历史上的安全问题  
- **执行时间：**2-5分钟  

### 依赖项扫描（每周一次）  
- npm漏洞检查（Node.js相关）  
- Python安全检查  
- 已知的漏洞  
- **执行时间：**约30秒  

### 全面审计（按需）  
- 上述所有内容  
- 环境变量泄露  
- 提交前钩子验证  
- 代码质量检查  
- **执行时间：**3-6分钟  

## 严重程度等级  

- **CRITICAL** → 阻止提交（存在敏感信息或凭证）  
- **HIGH** → 需要审批（存在漏洞或缺少许可证）  
- **MEDIUM** → 警告（有待处理的事项或缺少`README`文件）  
- **LOW** → 仅提供信息提示  

## 集成方式  

### 推荐使用预推送钩子  
```bash
./install-hooks.sh ~/my-repo
git push  # Automatic security check
```  

### 每周定时任务  
```bash
# Add to OpenClaw cron
openclaw cron add \
  --name "weekly-repo-scan" \
  --cron "0 3 * * 1" \
  --announce \
  --message "Run: ~/.openclaw/workspace/skills/pre-publish-security/schedule.sh run ~/repo"
```  

### 手动预发布检查  
```bash
# Before clawhub publish
./audit-full.sh ~/skills/my-skill full
clawhub publish skills/my-skill --version 1.0.1
```  

## 相关文件  
- `audit-simple.sh` - 快速预推送扫描工具  
- `audit-full.sh` - 全面扫描工具（包含跟踪功能）  
- `schedule.sh` - 状态监控与自动化脚本  
- `install-hooks.sh` - Git钩子安装脚本  
- `audit-state.json` - 状态跟踪文件（自动生成）  
- `AUDIT-SCHEDULE.md` - 审计频率指南  
- `README.md` - 完整的使用说明  
- `agents/` - 子代理定义（未来使用）  

## 所需软件  
- git  
- jq  
- grep  

## 可选扩展功能（增强检测能力）：  
- npm（Node.js依赖项扫描）  
- pip + safety（Python依赖项扫描）  
- shellcheck（用于验证bash脚本）  

## 状态跟踪  
- 自动记录：  
  - 每种扫描类型的最后一次执行时间  
  - 总扫描次数  
  - 按严重程度分类的发现结果  

- 通过`./schedule.sh status`查看状态  

## 退出代码  
- `0` - 无问题（或仅发现低/中等严重程度的问题）  
- `1` - 严重问题（阻止提交）  
- `2` - 高风险问题（需要审核）  

## 实际应用示例  
**问题：** 不小心在Git远程URL中推送了GitHub个人访问令牌  
**解决方案：** 该工具检测到问题并阻止了提交  
**结果：** 凭据未被公开泄露  

## 使用场景  
1. **个人开发者**：通过预推送钩子防止操作失误  
2. **开源项目**：保护贡献者的错误  
3. **ClawHub Skills**：在发布前进行验证  
4. **持续集成/持续交付（CI/CD）**：集成到GitHub Actions中以实现自动化检查  
5. **安全审计**：对仓库进行全面审查  

## 该工具的诞生背景  
2026年3月15日，有人在Git配置文件中意外泄露了个人访问令牌。该协议确保此类事件不再发生。  

## 许可证  
MIT许可证——欢迎自由使用、改进或分享。  

## 贡献方式  
如有问题或建议，请提交PR至：  
https://github.com/solmas/pre-publish-security