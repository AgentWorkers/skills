# Toggl-Optimized

这是一个针对Toggl Track的高性能代理技能，旨在提升令牌使用效率并优化报告功能。

## 概述

该技能提供了一种与Toggl Track交互的简化方式，重点在于减少上下文数据的使用，并通过直接的API v3调用实现快速报告功能。

## 特点

- **令牌高效**：采用优化的API调用方式，降低大型语言模型（LLM）对上下文数据的需求。
- **快速报告**：提供Shell脚本，用于生成JSON和PDF格式的报告。
- **直接API访问**：包含使用`curl`命令直接与Toggl v3报告系统交互的示例。

## 设置

1. 从[Toggl个人资料设置](https://track.toggl.com/profile)获取您的API令牌。
2. 设置环境变量：
   ```bash
   export TOGGL_API_TOKEN="your-api-token"
   ```
3. （可选）设置您的工作区ID：
   ```bash
   export TOGGL_WORKSPACE_ID="your-workspace-id"
   ```

## 使用方法

### 优化后的报告脚本

使用提供的脚本快速生成报告摘要：
```bash
# Usage: bash scripts/toggl_report.sh <client_name> <start_date> <end_date> <format: json|pdf>
bash scripts/toggl_report.sh myclient 2026-02-01 2026-02-28 json
```