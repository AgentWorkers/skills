---
name: code-sandbox
description: 在沙箱化的虚拟机中执行 JavaScript 代码，以进行数据处理和计算。
---

## 代码沙箱（Code Sandbox）

我们提供了用于计算和数据处理的 JavaScript 执行工具：

**完整脚本（Full Scripts）：**
- `execute_js`：在隔离的 V8 沙箱中运行 JavaScript 代码
  - 通过 `input` 参数传递数据（格式为 JSON）——在代码中将其作为 `INPUT` 访问
  - 使用 `console.log()` 输出中间结果（结果会存储在 `logs` 数组中）
  - 可用的全局变量：`JSON`, `Math`, `Date`, `Array`, `Object`, `String`, `Number`, `RegExp`, `Map`, `Set`, `parseInt`, `parseFloat`, `isNaN`, `isFinite`, `encodeURIComponent`, `decodeURIComponent`, `atob`, `btoa`
  - 无网络访问权限，无文件系统功能，无法导入外部模块——仅支持纯计算操作
  - 默认超时时间为 5 秒，最长超时时间为 30 秒
  - 输出数据大小限制为 10MB

**快速表达式（Quick Expressions）：**
- `eval_expression`：评估单个 JavaScript 表达式并返回结果
  - 适用于快速进行数学运算（例如：`"15 * 4500 * 0.01"` → 返回 `675`
  - 用于日期计算（例如：`"new Date().toISOString()"`
  - 数组操作（例如：`"[1,2,3].map(x => x*x)"` → 返回 `[1, 4, 9]`

**最佳实践（Best Practices）：**
- 使用 `execute_js` 进行多步骤的数据处理、算法测试和代码验证
- 使用 `eval_expression` 进行简单的数学运算、字符串操作和日期计算
- 将大型数据集通过 `input` 参数传递，而不是直接嵌入到代码中
- 结合 `parse_csv`（用于处理结构化数据）实现 CSV 数据的读取、转换和输出
- 结合 `store_deliverable` 将计算结果保存为工作记录（job evidence）