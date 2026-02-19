---
name: security-sentinel
description: 扫描工作区以检测安全漏洞、泄露的敏感信息以及配置错误。
---
# Security Sentinel

这是一个专为 OpenClaw 工作空间设计的统一安全扫描工具。它可以检测依赖项中的漏洞（通过 `npm audit`）、暴露的敏感信息（使用正则表达式匹配），以及不安全的文件权限设置。

## 使用方法

### 命令行界面 (CLI)

执行全面的安全扫描：

```bash
node skills/security-sentinel/index.js
```

扫描结果将以 JSON 格式输出到标准输出（stdout）。如果检测到风险（如高风险的漏洞、敏感信息或不当的文件权限设置），程序将以状态码 1 退出。

### 常用选项

- `--skip-audit`：跳过 `npm audit` 步骤（加快扫描速度）。
- `--no-fail`：即使检测到风险，也无需以状态码 1 退出（适用于仅用于监控的场景）。

### 程序化使用方法

```javascript
const sentinel = require('./skills/security-sentinel');

const report = await sentinel.scan();

if (report.status === 'risk_detected') {
  console.error('Security issues found:', report);
}
```

## 主要功能

1. **依赖项审计**：运行 `npm audit`，检查 `package.json` 中的依赖项是否存在已知的漏洞（CVE）。
2. **敏感信息检测**：扫描工作空间中的文件，查找类似 API 密钥、密码和私钥的敏感内容。
3. **权限检查**：确保关键文件（如 `package.json`、`.env`）不能被全局写入。

## 配置选项

- **忽略的路径**：`node_modules`、`.git`、`logs`、`temp`、`.openclaw/cache`。
- **敏感信息模式**：常见的 API 密钥、密码、私钥、Feishu 应用程序密钥等。