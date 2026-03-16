---
name: security-audit
description: 针对Clawdbot部署的全面安全审计：扫描暴露的凭据、开放的端口、配置漏洞以及安全风险。支持自动修复功能。
---

# 安全审计技能

## 使用场景

在部署 Clawdbot 之前，或按照预定时间表运行安全审计，以识别系统中的安全漏洞。使用自动修复功能来自动处理常见问题。

## 设置要求

无需任何外部依赖项；在系统支持的情况下，使用原生的系统工具即可完成审计。

## 使用方法

### 快速审计（针对常见问题）

```bash
node skills/security-audit/scripts/audit.cjs
```

### 全面审计（深度扫描）

```bash
node skills/security-audit/scripts/audit.cjs --full
```

### 自动修复常见问题

```bash
node skills/security-audit/scripts/audit.cjs --fix
```

### 审计特定区域

```bash
node skills/security-audit/scripts/audit.cjs --credentials      # Check for exposed API keys
node skills/security-audit/scripts/audit.cjs --ports            # Scan for open ports
node skills/security-audit/scripts/audit.cjs --configs          # Validate configuration
node skills/security-audit/scripts/audit.cjs --permissions      # Check file permissions
node skills/security-audit/scripts/audit.cjs --docker           # Docker security checks
```

### 生成报告

```bash
node skills/security-audit/scripts/audit.cjs --full --json > audit-report.json
```

## 审计结果

审计会生成一份报告，其中包含以下信息：

| 等级 | 描述                |
|-------|-------------------|
| 🔴 严重（CRITICAL）| 需立即采取行动（例如：凭证泄露） |
| 🟠 高风险（HIGH）| 风险较高，请尽快修复       |
| 🟡 中等风险（MEDIUM）| 需要关注             |
| 🟢 信息提示（INFO）| 无需采取任何行动         |

## 检查内容

### 凭证信息
- 环境配置文件中的 API 密钥
- 命令历史记录中的令牌
- 代码中硬编码的敏感信息
- 弱密码模式

### 端口
- 意外开放的端口
- 暴露在互联网上的服务
- 未配置的防火墙规则

### 配置设置
- 未设置速率限制
- 认证功能被禁用
- 使用默认凭证
- 开启了 CORS 政策

### 文件
- 公开可读的文件
- 任何用户均可执行的文件
- 存放在公共目录中的敏感文件

### Docker 容器
- 具有特殊权限的容器
- 未设置资源使用限制
- 容器中使用了 root 用户权限

## 自动修复功能

`--fix` 选项可自动执行以下操作：
- 设置严格的文件权限（例如：.env 文件的权限设置为 600）
- 保护敏感的配置文件
- 如果缺少 `.gitignore` 文件，则自动生成该文件
- 启用基本的安全头部信息

## 相关技能

- `security-monitor` - 实时监控工具（可单独使用）