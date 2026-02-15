---
name: openclaw-security-guard
description: OpenClaw的安全审计命令行工具（CLI）及实时监控仪表盘：可检测系统中的敏感信息泄露、配置错误、命令注入攻击、存在漏洞的依赖项以及未经验证的主控服务器（MCP servers）。该工具完全不收集任何用户数据（零数据传输，即“零遥测”）。
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - node
    install:
      - kind: node
        package: openclaw-security-guard
        bins: [openclaw-guard, openclaw-security-guard]
    emoji: "\U0001F6E1"
    homepage: https://github.com/2pidata/openclaw-security-guard
    os:
      - macos
      - linux
      - windows
---

# OpenClaw 安全防护工具

专为 OpenClaw 安装环境提供的缺失的安全防护层。

## 功能概述

运行 `openclaw-guard audit` 命令，可对您的 OpenClaw 环境进行以下 5 个方面的安全扫描：

- **秘密信息扫描器**：检测 API 密钥、令牌、密码（支持 15 种以上格式）并进行熵分析；
- **配置审核器**：检查沙箱模式、数据传输策略、网关绑定设置以及速率限制规则；
- **提示注入检测器**：识别 50 多种提示注入攻击模式（如指令覆盖、角色劫持等）；
- **依赖项扫描器**：扫描 npm 依赖项中的安全漏洞（CVE）；
- **MCP 服务器审核器**：根据允许列表验证已安装的 MCP 服务器。

## 快速入门

```bash
npm install -g openclaw-security-guard

# Full audit
openclaw-guard audit

# Fix issues automatically (with backup)
openclaw-guard fix --auto

# Launch live dashboard
openclaw-guard dashboard
```

## 主要特性

- **安全评分**（0-100 分）：直观显示您的系统安全状况；
- **自动加固功能**：支持交互式、自动执行或模拟执行模式；
- **实时监控面板**：通过 `localhost:18790` 查看系统运行状态；
- **提交前检测**：在代码提交前自动检查是否存在敏感信息；
- **多语言支持**：提供英语、法语和阿拉伯语版本；
- **零数据传输**：完全不发送任何网络请求，实现 100% 本地化运行。

## 链接

- **仓库地址**：https://github.com/2pidata/openclaw-security-guard
- **作者**：[Miloud Belarebia](https://github.com/miloudbelarebia) / [2PiData](https://2pidata.com)
- **许可证**：MIT 许可证