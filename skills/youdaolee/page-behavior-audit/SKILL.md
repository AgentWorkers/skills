---
name: page-behavior-audit
description: 深度行为审计：采用哈希策略（符合CSP标准，不包含明文恶意词汇）
homepage: https://github.com/openclaw/page-behavior-audit
metadata:
  {
    "openclaw":
      {
        "emoji": "🔍",
        "type": "skill",
        "version": "1.0.3",
        "modelInvocable": false,
        "requiredEnv":
          [
            {
              "name": "WECOM_WEBHOOK_URL",
              "description": "WeCom webhook URL for critical alerts",
              "sensitive": true,
            },
            {
              "name": "OPENCLAW_AUDIT_DIR",
              "description": "Directory for audit logs, screenshots, and HAR files",
              "default": "${HOME}/.openclaw/audit",
            },
          ],
        "trigger": { "type": "webhook", "path": "/api/audit/scan", "method": "POST" },
        "timeout": 15000,
      },
  }
---

# page-behavior-audit

这是一个用于深度行为审计的页面审计工具，同时具备内容安全策略的执行功能。

## 主要功能

- 🔍 浏览器自动化操作及重定向跟踪
- 🛡️ 内容策略检查（包含哈希处理的恶意词汇）
- 🎯 响应内容监控（SSRF/XXE攻击检测）
- 📸 全屏截图功能
- 📊 生成HAR文件（HTTP Archive Report）
- 🚨 对于严重问题，会通过WeCom发送警报

## 先决条件

请设置以下环境变量：

```bash
export WECOM_WEBHOOK_URL="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_KEY"
export OPENCLAW_AUDIT_DIR="${HOME}/.openclaw/audit"  # optional
```

## 使用方法

### 通过Webhook调用

```bash
curl -X POST http://localhost:8080/api/audit/scan \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "include_har": true}'
```

### 通过CLI调用

```bash
openclaw skill run page-behavior-audit --url https://example.com
```

## 配置参数

**输入参数：**
- `url` (字符串，必填)：需要审计的目标URL
- `include_har` (布尔值，可选)：是否导出HAR文件（默认值：true）

**输出参数：**
- `redirects`：捕获到的重定向信息
- `text_alerts`：内容策略违规情况
- `ct_alerts`：响应内容监控警报
- `screenshot_path`：截图文件路径
- `har_path`：HAR文件路径

## 安全性特性

- 使用SHA256对恶意词汇进行哈希处理
- 采用Ed25519算法进行签名验证
- 符合CSP（Content Security Policy）标准（避免使用明文敏感信息）
- 浏览器在沙箱环境中执行，确保安全性

## 警报规则

**严重级别（CRITICAL）：**
- 从非.xml格式的端点返回XML内容（存在SSRF/XXE攻击风险）
- 图片端点返回XML内容（可能用于XXE攻击）

当检测到严重问题时，系统会通过WeCom webhook发送警报。