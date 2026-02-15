---
name: volcengine-ai-misc-model-discovery
description: 发现并利用 Volcengine AI 模型的功能。当用户询问应使用哪个模型、需要检查端点功能或请求模型选择矩阵时，请使用此功能。
---

# volcengine-ai-misc-model-discovery

该模块用于发现可用的模型，并将用户意图映射到最合适的端点。

## 执行流程

1. 确定任务类型及相关约束（如延迟、成本、质量要求）。
2. 根据模型/端点的功能对其进行分类。
3. 对各个选项进行评分，并推荐一个默认方案以及备用方案。
4. 输出决策表格和调用模板。

## 输出格式

- 任务类型
- 可选端点列表
- 推荐的端点
- 折中方案及备选方案

## 参考资料

- `references/sources.md`