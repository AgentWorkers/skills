---
name: clauwdit
description: AI代理技能的安全审计工具。该工具会扫描SKILL.md文件，以检测是否存在提示注入（prompt injection）、数据泄露（data exfiltration）、代码混淆（obfuscation）以及危险的功能组合（dangerous capability combinations）等安全问题。
version: 1.0.0
metadata:
  openclaw:
    tags:
      - security
      - audit
      - trust
      - safety
      - scanning
---
# ClawAudit — 用于代理技能的安全审计工具

这是一个用于分析 OpenClaw SKILL.md 文件的静态安全分析工具。它能够在您安装相关技能之前，检测出提示注入（prompt injection）、凭证泄露（credential exfiltration）、混淆后的载荷（obfuscated payloads）以及危险的功能组合（dangerous capability combinations）。

## 功能介绍

您只需粘贴或通过管道传输任何 SKILL.md 文件内容，即可获得一个信任评分（0-100 分），同时会收到详细的检测结果。

**检测内容：**

- 提示注入和代理行为操控（包括 Unicode 同形异义字符的利用）
- 数据泄露方式（HTTP、DNS、加密通道）
- 危险的 shell 命令（curl|sh、/dev/tcp、进程替换）
- 凭证收集（环境变量、SSH 密钥、API 令牌）
- 混淆后的载荷（base64 编码、十六进制转义、eval 语句链）
- 复合威胁（例如：文件读取 + 网络传输 = 数据泄露）
- 权限不匹配（未声明的功能被非法使用）

**区域感知分析（Zone-aware analysis）**：该工具能够理解 markdown 文档的结构。代码块会被视为可执行的指令；用于描述安全威胁的文档本身不会被标记为威胁。

## 使用方法

在安装技能之前进行审计：

```bash
curl -s https://clauwdit.4worlds.dev/audit/author/skill-name
```

或者直接上传原始的技能内容：

```bash
curl -s -X POST https://clauwdit.4worlds.dev/audit \
  -H "Content-Type: application/json" \
  -d '{"skill":"author/skill-name"}'
```

## 信任等级

| 评分 | 等级 | 含义 |
|-------|------|---------|
| 80-100 | 可信 | 未发现重大问题 |
| 60-79 | 中等风险 | 存在轻微问题，建议重新审查 |
| 40-59 | 可疑 | 存在重大问题，使用需谨慎 |
| 0-39 | 危险 | 检测到严重威胁，切勿安装 |

## 响应格式

```json
{
  "trust": { "score": 85, "tier": "trusted" },
  "findings": [
    {
      "severity": "medium",
      "description": "Network request capability detected",
      "zone": "code",
      "line": 12
    }
  ],
  "capabilities": ["network_out", "file_read"],
  "compoundThreats": [],
  "permissionIntegrity": { "undeclared": [], "unused": [] }
}
```

## 关于该工具

该工具由 4Worlds 开发，具备区域感知的静态分析能力，支持 60 多种检测模式，支持 Unicode 同形异义字符的规范化处理，并能检测复合威胁。