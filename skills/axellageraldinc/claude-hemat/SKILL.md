# ClaudeHemat

# 介绍
1. **Haiku 4.5** 是默认模型。只有在任务确实需要 **Sonnet 4.5** 或 **Opus 4.6** 时，才使用这些模型。
2. 可以通过 `sessions_spawn` 来使用更高级的模型。
```
sessions_spawn(
  message: "<the full task description>",
  model: "anthropic/claude-sonnet-4-5",
  label: "<short task label>"
)
```
```
sessions_spawn(
  message: "<the full task description>",
  model: "anthropic/claude-opus-4-6",
  label: "<short task label>"
)
```

# 模型
## Haiku 4.5
1. 适用于简单的问题与回答（例如：什么、何时、谁、在哪里）
2. 适用于非正式的聊天场景（无需进行推理）
3. 适用于快速查询信息
4. 适用于简单任务（包括但不限于重复性任务）
5. 输出结果简洁明了

## Sonnet 4.5
1. 适用于需要分析复杂数据或问题的场景
2. 适用于处理包含多行代码的复杂任务
3. 适用于需要制定详细计划或策略的场合
4. 适用于需要深入推理的情境
5. 适用于生成详细的报告或分析结果

## Opus 4.6
1. 适用于需要进行深度研究的场景
2. 适用于需要做出关键决策的场合
3. 适用于处理极其复杂的逻辑问题或任务
4. 适用于需要制定极其复杂的计划或策略的场合
5. 适用于生成详细的解释或分析结果

# 禁忌事项
1. 绝不允许使用 **Haiku 4.5** 来编写代码
2. 绝不允许使用 **Haiku 4.5** 来进行分析
3. 绝不允许使用 **Haiku 4.5** 来进行推理

# 其他注意事项
1. 如果用户明确要求使用特定模型，请按照用户的要求执行
2. 必须在输出结果中明确说明使用了哪个模型
3. 在使用完更高级的模型（**Sonnet 4.5** 或 **Opus 4.6**）后，应自动将默认模型切换回 **Haiku 4.5**