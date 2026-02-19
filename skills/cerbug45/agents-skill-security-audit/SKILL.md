---
name: security-audit
description: 一个用于审核遵循 `skill.md` 格式的供应链风险相关指令的简单辅助工具。
metadata:
  {
    "openclaw": {
      "requires": { "bins": ["python3"] },
      "category": "security"
    }
  }
---
# security-audit

这是一个用于审计遵循 `skill.md` 格式的文档中涉及供应链风险的辅助工具。

## 功能
- 基于启发式的扫描机制，检测数据泄露的常见模式（如通过 HTTP POST 请求、向未知域名发送请求、读取 `~/.env` 文件、使用敏感的凭证信息等）。
- 提示工具使用的权限：列出工具访问过的文件系统和网络资源。
- 生成安全的审计报告：以 Markdown 格式呈现审计结果，并附带风险等级说明。

## 使用方法
```bash
python audit.py path/to/skill.md > report.md
```