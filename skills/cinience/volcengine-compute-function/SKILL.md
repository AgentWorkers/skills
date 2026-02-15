---
name: volcengine-compute-function
description: 构建并运行 Volcengine 的函数计算工作负载。适用于用户需要函数部署、事件触发、运行时配置或无服务器（serverless）故障排查的场景。
---

# volcengine-compute-function

用于部署和排查服务器less函数的工具，具备可预测的打包机制以及运行时检查功能。

## 执行检查清单

1. 确认运行时环境、触发类型和区域。
2. 构建函数包并验证环境变量。
3. 部署函数并验证最新版本。
4. 调用测试事件并返回日志及延迟统计信息。

## 可靠性规则

- 对部署生成的文件进行版本控制。
- 将配置文件与代码分离。
- 在输出结果中包含回滚目标信息。

## 参考资料

- `references/sources.md`