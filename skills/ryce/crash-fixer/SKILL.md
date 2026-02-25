---
name: crash-fixer
description: "**自主崩溃分析与漏洞修复功能**：该系统会监控来自 Cloudflare D1 的崩溃报告，对这些报告进行去重处理，然后使用 Codex 5.3 High 工具进行分析，生成相应的修复方案，并创建 Pull Request（PR）。  
**使用方法：**  
`/crash-fixer [--hours 24] [--limit 5] [--dry-run]`  
- `--hours 24`：表示系统全天候（24 小时）运行崩溃分析任务。  
- `--limit 5`：限制系统同时处理的崩溃报告数量为 5 个。  
- `--dry-run`：执行测试模式（仅进行模拟操作，不实际生成修复方案或提交 PR）。"
user-invocable: true
metadata:
  { "openclaw": { "requires": { "env": ["GH_TOKEN", "OPENAI_API_KEY", "CRASH_REPORTER_API_KEY", "CRASH_REPORTER_URL"] } } }
---
# 自动崩溃修复工具

该工具具备完整的自主崩溃修复流程：从数据库中获取崩溃报告，进行去重处理，利用人工智能进行分析，生成修复代码，并创建相应的 Pull Request（PR）。

## 触发机制
```
/crash-fixer [--hours 24] [--limit 5] [--dry-run]
```

## 工作原理

### 1. 获取崩溃报告
从数据库 D1 中查询过去 N 小时内状态为“new”的崩溃报告。

### 2. 去重
对于每份崩溃报告，检查是否已经有人尝试过修复：
- 从数据库 D1 中查询具有相同错误名称（`error_name`）和错误信息摘要（`message`）的崩溃报告。
- 如果已经存在 PR（状态为“fixing”或 `fix_pr_url` 已设置），则跳过该崩溃报告。
- 在数据库 D1 中更新已处理的崩溃报告的状态字段。

### 3. 分析（使用 GPT Codex 5.3）
- 解析堆栈跟踪信息以获取文件和行号信息。
- 在代码库中查找相关的文件。
- 确定崩溃的根本原因。

### 4. 生成修复代码
- 读取受影响的源代码文件。
- 生成最简洁的修复代码。

### 5. 创建 Pull Request
- 创建一个新的分支：`fix/crash-{id}-{error-hash}`。
- 提交修复代码并附上详细的说明。
- 打开包含崩溃详细信息的 PR。
- 将 PR 的 URL 更新到数据库 D1 中。

## 配置选项

| 选项 | 默认值 | 说明 |
|------|---------|-------------|
| `--hours N` | 24 | 仅获取过去 N 小时内的崩溃报告 |
| `--limit N` | 3 | 每次运行时最多处理 N 个崩溃报告 |
| `--dry-run` | false | 仅进行分析，不创建 PR |

## 所需环境变量
- `GH_TOKEN`：GitHub API 令牌
- `OPENAI_API_KEY`：用于 GPT Codex 5.3 的 OpenAI API 令牌
- `CRASH_REPORTER_API_KEY`：崩溃报告生成工具的 API 令牌
- `CRASH_REPORTER_URL`：崩溃报告生成工具的 URL（可选）

## 去重逻辑
**崩溃报告的指纹（Fingerprint）计算方法：**
`Fingerprint = error_name + message` 的前 100 个字符的哈希值

**在处理崩溃报告之前：**
```sql
SELECT * FROM crashes WHERE 
  fingerprint = ? 
  AND (status = 'fixing' OR fix_pr_url IS NOT NULL)
```

**如果找到匹配的崩溃报告，则跳过该报告，并记录注释：“该崩溃已修复”**