---
name: Docker Pro Diagnostic
description: 使用信号提取技术对Docker容器进行高级日志分析。
bins: ["python3", "docker"]
---

# Docker Pro 诊断工具

当用户询问“为什么我的容器失败了？”或“请分析 [container] 的日志”时，请按照以下步骤操作：

1. **运行提取工具：** 执行 `python3 {{skillDir}}/log_processor.py <container_name>` 命令。
2. **分析结果：** 将提取到的输出（其中包含错误信息和上下文）输入到您的故障分析系统中。
3. **生成报告：** 总结问题的根本原因。如果问题是由于代码错误导致的，提供相应的修复建议；如果问题是由于资源不足（如内存溢出 OOM）引起的，建议增加 Docker 的内存限制。

## 示例命令：
`python3 log_processor.py api_gateway_prod`