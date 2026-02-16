---
name: grc-scan
description: 安全扫描菜单（头部信息/SSL/GDPR）
user-invocable: true
metadata: {"openclaw":{"requires":{"bins":["python3"]}}}
---# GRC扫描

启动安全扫描。

## 操作步骤
使用 `auditclaw-grc` 技能，询问用户希望扫描的内容：
1. **安全头部（Security Headers）**：检查 HTTP 安全头部
2. **SSL/TLS**：证书和协议分析
3. **GDPR**：Cookie 同意设置及隐私合规性

之后，根据用户提供的 URL 执行所选的扫描任务。