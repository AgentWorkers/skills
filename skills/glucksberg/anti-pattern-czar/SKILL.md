---
name: anti-pattern-czar
description: "使用状态持久化和审批工作流来检测并修复 TypeScript 中的错误处理反模式。适用于扫描代码库时发现潜在的错误问题，例如：无声的错误处理、空catch语句、被忽略的Promise异常，以及未记录在日志中的错误。该工具支持五种模式：  
1. **扫描（Scan）**：检测所有错误处理相关的问题；  
2. **审核（Review）**：提供交互式的修复功能；  
3. **自动修复（Auto）**：通过预设规则批量修复错误；  
4. **继续上次会话（Resume）**：从上一次扫描或修复会话中继续执行；  
5. **报告（Report）**：显示扫描进度和发现的问题。  
可通过以下命令触发该工具：  
`scan for anti-patterns`、`fix error handling`、`find empty catches`、`anti-pattern czar` 或 `check error handling`。"
---
# 反模式识别工具（Anti-Pattern Czar）

这是一个自主运行的代理程序，能够系统地识别并修复 TypeScript 中的错误处理反模式（即不符合最佳实践的代码编写方式）。

## 检测器（Detector）

无需安装，可直接使用 Bun 运行：

```bash
bunx antipattern-czar
bunx antipattern-czar --src lib
bunx antipattern-czar --config my-config.json
```

配置方式：通过 `.antipatternrc.json` 文件进行设置：
```json
{
  "srcDir": "src",
  "criticalPaths": ["DatabaseService.ts", "AuthHandler.ts"],
  "skipDirectories": ["node_modules", "dist", ".git"]
}
```

## 模式选择（Mode Selection）

根据用户指令选择相应的操作模式：

| 用户指令 | 模式       | 动作              |
|-----------|-------------|-------------------|
| "scan"     | SCAN         | 运行检测器并保存当前状态       |
| "detect"    | DETECT       | 仅检测问题           |
| "find"     | FIND         | 查找所有问题           |
| "review"    | REVIEW       | 进行交互式修复         |
| "fix"      | FIX          | 自动修复问题           |
| "auto"     | AUTO         | 批量修复问题（使用预设模板）     |
| "resume"    | RESUME       | 从上次暂停的位置继续修复     |
| "report"    | REPORT       | 显示当前修复进度         |
| "status"    | STATUS       | 查看系统状态           |
| "progress"   | PROGRESS     | 显示整体修复进度         |

## 状态文件（State File）

系统始终会检查项目根目录下的 `.anti-pattern-state.json` 文件。首次执行 `SCAN` 模式时，如果该文件存在，系统会询问用户是否要从中恢复上一次的修复进度。

```json
{
  "session_id": "<uuid>",
  "started_at": "<ISO>",
  "target_path": "<path>",
  "issues": [],
  "history": []
}
```

问题数据结构：`id`, `file`, `line`, `pattern`, `severity`（严重/高/中），`is_critical_path`（是否为关键路径），`status`（待处理/已修复/已批准/跳过），`code_snippet`（问题相关的代码片段）。

## 各模式的处理流程（Workflow by Mode）

详细的工作流程请参见 [workflows.md](references/workflows.md)。简要说明如下：

- **SCAN**：运行检测器 → 解析问题 → 分类问题的严重程度 → 保存状态 → 显示问题汇总。
- **REVIEW**：加载状态信息 → 按关键路径和严重程度排序问题 → 阅读问题相关的代码 → 提出修复建议 → 应用已批准的修复方案 → 更新状态。
- **AUTO**：先与用户确认 → 使用预设模板自动修复非关键路径的问题 → 对于关键路径的问题切换到 **REVIEW** 模式进行处理 → 显示修复总结。
- **RESUME**：加载 `.anti-pattern-state.json` 文件 → 从第一个待处理的问题开始继续修复。
- **REPORT**：显示修复会话的统计信息、问题严重程度统计表、最近的修复记录以及下一步需要执行的操作。

## 仅在满足以下条件时建议用户批准问题修复：

- 该错误是 **预期中的且频繁出现** 的。
- 记录这些错误不会导致 **过多的日志信息**。
- 系统中已有 **明确的恢复/回退逻辑**。
- 问题的原因 **具体且具有技术性**。

**在关键路径上，除非用户明确同意，否则 **绝不要** 批准任何修复操作**。

**批准修复的格式要求**：
```typescript
} catch {
  // [APPROVED_OVERRIDE] <specific technical reason>
  // Fallback: <what happens instead>
}
```

## 修复模板（Fix Templates）

完整的错误模式列表（包括严重程度、是否适合自动修复以及对应的修复模板）请参见 [patterns.md](references/patterns.md)。

## 修复进度输出格式（Progress Output Format）

每次修复完成后，系统会输出相应的进度信息：
```
✅ Fixed: src/services/example.ts:42
   Pattern: NO_LOGGING_IN_CATCH
   Solution: Added logger.error() with context

Progress: 4/28 issues remaining ━━━━━━━ 14%
```