---
name: log-scrubber
description: 自动从工作区日志和内存文件中删除 API 密钥、令牌及敏感信息。
homepage: https://github.com/Heather-Herbert/openclaw-log-scrubber
metadata:
  clawdbot:
    requires:
      env: []
    files: ["scripts/*"]
---
# 日志清洗工具

该工具会自动扫描 `/root/.openclaw/workspace/` 目录下的环境日志文件和内存日志文件，以检测并删除其中包含的敏感信息（如 API 密钥、令牌和凭据）。

## 主要功能
- **主动扫描**：通过正则表达式识别常见的敏感信息模式。
- **自动清洗**：在原文件保留备份（例如带有 `.bak` 扩展名的备份文件）的情况下，直接对文件进行清洗操作。
- **模拟运行模式**：允许您在不修改文件的情况下测试清洗效果。
- **安全性**：确保敏感信息不会意外地被写入发送给服务提供商的日志中，也不会以明文形式存储在内存文件中。

## 使用方法
- 要进行模拟运行（检查修改前的效果）：
  `python3 /root/.openclaw/workspace/skills/log-scrubber/scripts/scrub.py --dry-run`

- 要应用修改：
  `python3 /root/.openclaw/workspace/skills/log-scrubber/scripts/scrub.py`

## 外部接口
- 该工具不调用任何外部接口，所有操作均在本地完成。

## 安全性与隐私保护
- 所有清洗操作都在您的本地机器上执行，不会向外部服务器传输任何数据。

## 模型调用
- 该工具仅在本地运行，不会自主调用 OpenClaw 代理之外的其他模型。

## 使用声明
- 使用该工具即表示您同意它将用清洗后的版本替换您工作空间中的文件。请务必备份重要数据。