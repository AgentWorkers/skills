---
name: usage-visualizer
description: OpenClaw 提供高级使用统计功能和高保真度的可视化报告生成服务。所有数据处理均基于本地计算完成，确保用户隐私得到严格保护（系统不会存储任何用户凭证）。
metadata:
  openclaw:
    emoji: "📊"
    os:
      - darwin
      - linux
    requires:
      bins:
        - python3
        - chromium
      env:
        - OPENCLAW_WORKSPACE
    install:
      - id: pip-deps
        kind: exec
        command: "pip3 install -r requirements.txt"
        label: "Install Python dependencies"
---
# 使用可视化工具

**使用可视化工具** 是一个专为 OpenClaw 设计的高保真分析引擎，它能够将原始的会话日志转换为专业且易于操作的可视化报告。

## 🚀 快速入门

```bash
# Generate today's visual report
python3 scripts/run_usage_report.py --mode image --period today
```

## 📈 使用指南

### 可视化报告
该可视化工具会先同步日志数据，然后生成报告图像：
- `python3 scripts/run_usage_report.py --mode image --period today`
- `python3 scripts/run_usage_report.py --mode image --period week --json`

### 文本摘要
- `python3 scripts/run_usage_report.py --mode text --period today --json`

## 🛡 交付协议（代理服务器必须遵守）

1. **图像交付**：从 JSON 数据中提取 `image_path`，并通过 `message` 工具的 `filePath` 选项将其作为附件发送。**绝对禁止** 以字符串形式直接发送本地路径。
2. **验证**：在发送之前，确保文件存在且为有效的 PNG 格式。
3. **无网络依赖**：该工具完全在本地运行，不依赖任何网络服务。

## 📄 许可证
MIT